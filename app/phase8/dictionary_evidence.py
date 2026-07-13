from __future__ import annotations

import json
import sqlite3
import unicodedata
from collections import Counter
from typing import Any, Iterable

from .dictionary_store import DB_PATH

# Dictionary types remain evidence dimensions. They never become final roles here.
KNOWN_TYPES = ("term", "expression", "name", "grammar", "frequency", "unknown")


def normalize_lookup_text(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value or "")).strip()


def _connect_readonly() -> sqlite3.Connection:
    # The sync step creates the DB. Opening normally also makes the evidence endpoint
    # return a clean not-ready result if the cache was cleared.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    return con


def dictionary_ready() -> bool:
    if not DB_PATH.exists():
        return False
    try:
        with _connect_readonly() as con:
            row = con.execute(
                "SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='lexicon_entries'"
            ).fetchone()
            if not row or not row["n"]:
                return False
            count = con.execute("SELECT COUNT(*) AS n FROM lexicon_entries").fetchone()["n"]
            return count > 0
    except sqlite3.Error:
        return False


def _query_form(con: sqlite3.Connection, form: str, limit: int) -> list[dict[str, Any]]:
    rows = con.execute(
        """
        SELECT id, dictionary_id, dictionary_title, dictionary_type,
               dictionary_priority, term, reading, tags_json, rules_json,
               score, sequence, name_type, grammar_type, expression_type
        FROM lexicon_entries
        WHERE term = ?
        ORDER BY dictionary_priority ASC, score DESC, id ASC
        LIMIT ?
        """,
        (form, limit),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        for key in ("tags_json", "rules_json"):
            try:
                item[key[:-5]] = json.loads(item.pop(key) or "[]")
            except (TypeError, json.JSONDecodeError):
                item[key[:-5]] = []
        out.append(item)
    return out


def _candidate_lookup_forms(candidate: dict[str, Any]) -> list[dict[str, str]]:
    raw = candidate.get("lookup_forms") or candidate.get("lookupForms") or []
    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(value: Any, kind: str) -> None:
        text = normalize_lookup_text(value)
        if text and text not in seen:
            seen.add(text)
            out.append({"text": text, "type": kind})

    # Candidate surface is always first, followed by analyzer-provided forms.
    add(candidate.get("surface"), "surface")
    for index, value in enumerate(raw):
        if isinstance(value, dict):
            add(value.get("text") or value.get("value"), str(value.get("type") or "analyzer-form"))
        else:
            add(value, "surface" if index == 0 else "analyzer-form")
    add(candidate.get("lemma"), "lemma")
    add(candidate.get("normalized"), "normalized")
    return out


def _pos_compatibility(parser_pos: str | None, entries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Conservative compatibility signal; never rejects a candidate.

    Yomitan tags/rules differ by dictionary. This method only emits positive or
    conflicting hints when recognizable markers are present. Unknown is normal.
    """
    pos = str(parser_pos or "").upper()
    markers = " ".join(
        str(value).lower()
        for entry in entries
        for value in (*entry.get("tags", []), *entry.get("rules", []), entry.get("name_type", ""), entry.get("grammar_type", ""))
        if value
    )
    families = {
        "VERB": ("verb", "v1", "v5", "vs", "vk", "vz"),
        "NOUN": ("noun", "n", "n-", "名詞"),
        "PROPN": ("name", "proper", "surname", "given", "人名"),
        "ADJ": ("adj", "形容"),
        "ADV": ("adv", "副詞"),
        "PRON": ("pron", "代名詞"),
        "NUM": ("num", "numeric", "数詞"),
    }
    expected = families.get(pos)
    if not pos or not expected or not markers:
        return {"status": "unknown", "parserPos": parser_pos, "reason": "Insufficient normalized POS metadata"}
    compatible = any(marker in markers for marker in expected)
    return {
        "status": "compatible" if compatible else "unknown",
        "parserPos": parser_pos,
        "reason": "Recognized dictionary POS/rule marker" if compatible else "No contradictory normalized marker was asserted",
    }


def evaluate_candidate(
    candidate: dict[str, Any],
    parser_pos: str | None = None,
    per_form_limit: int = 250,
) -> dict[str, Any]:
    candidate_id = str(candidate.get("id") or candidate.get("candidate_id") or candidate.get("candidateId") or "")
    forms = _candidate_lookup_forms(candidate)
    attempts: list[dict[str, Any]] = []
    all_entries: list[dict[str, Any]] = []
    selected_form: dict[str, str] | None = None

    if not dictionary_ready():
        return {
            "candidate_id": candidate_id,
            "start": candidate.get("start"),
            "end": candidate.get("end"),
            "surface": candidate.get("surface", ""),
            "matched": False,
            "dictionary_ready": False,
            "lookup_attempts": [],
            "selected_lookup_form": None,
            "match_type": "dictionary-not-ready",
            "entry_count": 0,
            "independent_source_count": 0,
            "dictionary_type_counts": {},
            "matched_headwords": [],
            "source_names": [],
            "pos_compatibility": {"status": "unknown", "parserPos": parser_pos},
            "confidence": None,
            "meaning": "Dictionary cache is unavailable; this is not a candidate rejection.",
        }

    with _connect_readonly() as con:
        for form in forms:
            entries = _query_form(con, form["text"], per_form_limit)
            attempts.append({
                "form": form["text"],
                "form_type": form["type"],
                "match_count": len(entries),
            })
            if entries and selected_form is None:
                selected_form = form
            all_entries.extend(entries)

    # Deduplicate a source entry found through more than one equivalent lookup form.
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for entry in all_entries:
        key = (
            entry.get("dictionary_id"), entry.get("term"), entry.get("reading"),
            entry.get("sequence"), entry.get("dictionary_type"), entry.get("id"),
        )
        unique[key] = entry
    entries = list(unique.values())

    type_counts = Counter(str(e.get("dictionary_type") or "unknown") for e in entries)
    sources = sorted({str(e.get("dictionary_title") or "unknown") for e in entries})
    source_ids = {str(e.get("dictionary_id") or e.get("dictionary_title") or "unknown") for e in entries}
    headwords = sorted({str(e.get("term") or "") for e in entries if e.get("term")})
    pos_signal = _pos_compatibility(parser_pos, entries)

    matched = bool(entries)
    if matched and selected_form:
        match_type = f"{selected_form['type']}-exact"
        # Confidence is evidence strength only, not final sentence confidence.
        source_strength = min(1.0, 0.65 + 0.08 * len(source_ids))
        type_bonus = 0.05 if type_counts.get("term") or type_counts.get("expression") else 0.0
        pos_bonus = 0.05 if pos_signal.get("status") == "compatible" else 0.0
        confidence = round(min(0.99, source_strength + type_bonus + pos_bonus), 3)
    else:
        match_type = "none"
        confidence = None

    # Entry details are deliberately compact; no definitions/glossary content.
    compact_entries = [
        {
            "dictionary_id": e.get("dictionary_id"),
            "dictionary_title": e.get("dictionary_title"),
            "dictionary_type": e.get("dictionary_type"),
            "dictionary_priority": e.get("dictionary_priority"),
            "term": e.get("term"),
            "reading": e.get("reading"),
            "tags": e.get("tags", []),
            "rules": e.get("rules", []),
            "score": e.get("score"),
            "sequence": e.get("sequence"),
            "name_type": e.get("name_type"),
            "grammar_type": e.get("grammar_type"),
            "expression_type": e.get("expression_type"),
        }
        for e in entries[:100]
    ]

    return {
        "candidate_id": candidate_id,
        "start": candidate.get("start"),
        "end": candidate.get("end"),
        "surface": candidate.get("surface", ""),
        "candidate_type": candidate.get("candidate_type"),
        "matched": matched,
        "dictionary_ready": True,
        "lookup_attempts": attempts,
        "selected_lookup_form": selected_form["text"] if selected_form else None,
        "selected_lookup_form_type": selected_form["type"] if selected_form else None,
        "match_type": match_type,
        "entry_count": len(entries),
        "independent_source_count": len(source_ids),
        "dictionary_type_counts": dict(type_counts),
        "matched_headwords": headwords,
        "source_names": sources,
        "pos_compatibility": pos_signal,
        "confidence": confidence,
        "entries": compact_entries,
        "meaning": "Positive dictionary evidence" if matched else "No positive dictionary evidence; this is not a candidate rejection.",
    }


def _parser_pos_for_candidate(candidate: dict[str, Any], morphemes: list[dict[str, Any]]) -> str | None:
    a, b = candidate.get("start"), candidate.get("end")
    covered = [m for m in morphemes if m.get("start", -1) >= a and m.get("end", -1) <= b]
    if len(covered) == 1:
        return covered[0].get("pos")
    lexical = [m for m in covered if m.get("pos") in {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}]
    return lexical[-1].get("pos") if lexical else None


def evaluate_analysis_candidates(analysis: dict[str, Any]) -> dict[str, Any]:
    candidates = (
        analysis.get("dictionary_candidates_alpha31")
        or analysis.get("dictionary_candidates_alpha3")
        or analysis.get("dictionary_candidates")
        or []
    )
    morphemes = analysis.get("morphemes") or []
    evidence = [
        evaluate_candidate(candidate, _parser_pos_for_candidate(candidate, morphemes))
        for candidate in candidates
    ]
    matched = [item for item in evidence if item.get("matched")]
    by_type = Counter()
    for item in matched:
        by_type.update(item.get("dictionary_type_counts") or {})
    return {
        "dictionary_ready": dictionary_ready(),
        "candidate_count": len(candidates),
        "matched_candidate_count": len(matched),
        "unmatched_candidate_count": len(candidates) - len(matched),
        "dictionary_type_evidence_counts": dict(by_type),
        "evidence": evidence,
        "contract": {
            "evidence_only": True,
            "morphology_unchanged": True,
            "grammar_unchanged": True,
            "entities_unchanged": True,
            "reader_projection_unchanged": True,
            "dictionary_miss_is_not_rejection": True,
        },
    }
