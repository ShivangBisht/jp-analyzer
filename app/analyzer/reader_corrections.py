from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "reader_corrections.sqlite3"
_lock = threading.RLock()
_ALLOWED_ROLES = {
    "lexical",
    "lexical-compound",
    "name",
    "learnable-grammar",
    "function",
    "punctuation",
    "unresolved",
}
_ALLOWED_ACTIONS = {
    "show-as-one-unit",
    "mark-unresolved",
    # Reserved structural actions for the later frontend.
    "split",
    "mark-vocabulary",
    "mark-grammar",
    "mark-function",
    "mark-name",
}
_PUNCTUATION = set("、。！？!?「」『』（）()……─―～")

SCHEMA = """
CREATE TABLE IF NOT EXISTS reader_corrections(
 correction_id TEXT PRIMARY KEY, sentence_text TEXT NOT NULL, sentence_fingerprint TEXT NOT NULL,
 start INTEGER NOT NULL, end INTEGER NOT NULL, surface TEXT NOT NULL, action TEXT NOT NULL,
 display_role TEXT NOT NULL, headword TEXT, known_lookup_key TEXT, frequency_lookup_key TEXT,
 grammar_id TEXT, unknown_color_policy TEXT, scope TEXT NOT NULL,
 analyzer_version TEXT NOT NULL, reader_span_schema_version TEXT NOT NULL,
 original_spans_json TEXT NOT NULL, feature_snapshot_json TEXT NOT NULL,
 created_at TEXT NOT NULL, deactivated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_reader_corrections_occurrence
 ON reader_corrections(sentence_fingerprint,start,end,deactivated_at);
"""


def sentence_fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@contextmanager
def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    try:
        with con:
            yield con
    finally:
        con.close()


def _aligned_overlaps(
    text: str,
    start: int,
    end: int,
    baseline: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not baseline:
        raise ValueError("baselineReaderSpans is required")
    overlaps = [
        item for item in baseline
        if item.get("start", -1) < end and start < item.get("end", -1)
    ]
    if (
        not overlaps
        or min(item["start"] for item in overlaps) != start
        or max(item["end"] for item in overlaps) != end
    ):
        raise ValueError("Correction range must align to complete existing reader spans")
    if "".join(item.get("surface", "") for item in overlaps) != text[start:end]:
        raise ValueError("Correction range does not reconstruct selected source")
    return overlaps


def _unique(values: list[Any]) -> list[str]:
    return list(dict.fromkeys(str(value) for value in values if value))


def _candidate_snapshot(
    start: int,
    end: int,
    reader_candidates: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    candidates = []
    for candidate in reader_candidates or []:
        if candidate.get("start", -1) < end and start < candidate.get("end", -1):
            candidates.append({
                "candidateId": candidate.get("candidateId"),
                "start": candidate.get("start"),
                "end": candidate.get("end"),
                "surface": candidate.get("surface"),
                "candidateFamily": candidate.get("candidateFamily"),
                "proposedRole": candidate.get("proposedRole"),
                "grammarId": candidate.get("grammarId"),
                "possibleLookupKeys": candidate.get("possibleLookupKeys") or [],
                "selected": candidate.get("selected"),
                "rankingStatus": candidate.get("rankingStatus"),
                "selectionReason": candidate.get("selectionReason"),
                "abstentionReasons": candidate.get("abstentionReasons") or [],
                "dictionaryEvaluation": candidate.get("dictionaryEvaluation") or {},
                "candidateStructuralEvidence": candidate.get("candidateStructuralEvidence") or {},
            })
    return {"overlappingReaderCandidates": candidates}


def derive_structural_correction(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate user structural intent and derive identities from analyzer output.

    The user supplies boundaries/action and may supply a broad role. Dictionary keys,
    headwords, grammar IDs, and grammar-focus ranges are analyzer-derived only.
    """
    text = str(data.get("sentence") or "")
    start, end = data.get("start"), data.get("end")
    surface = str(data.get("surface") or "")
    scope = str(data.get("scope") or "occurrence")
    action = str(data.get("action") or "show-as-one-unit")
    requested_role = data.get("displayRole")

    if scope != "occurrence":
        raise ValueError("Structural teaching currently supports occurrence scope only")
    if action not in _ALLOWED_ACTIONS:
        raise ValueError("Unknown structural correction action")
    if action == "split":
        raise ValueError("Split teaching is reserved for the frontend phase")
    if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= len(text)):
        raise ValueError("Invalid correction range")
    if text[start:end] != surface:
        raise ValueError("Correction surface does not match sentence range")
    if any(ch in _PUNCTUATION for ch in surface):
        raise ValueError("Correction cannot cross or include protected punctuation")

    overlaps = _aligned_overlaps(text, start, end, baseline)
    grammar_ids = _unique([item.get("grammarId") for item in overlaps])
    lexical_keys = _unique([
        item.get("knownLookupKey") or item.get("headword")
        for item in overlaps
        if item.get("displayRole") in {"lexical", "lexical-compound"}
    ])
    grammar_focus_ranges = [
        {
            "start": item["start"],
            "end": item["end"],
            "surface": item.get("surface", ""),
            "grammarId": item.get("grammarId"),
        }
        for item in overlaps
        if item.get("displayRole") == "learnable-grammar"
    ]

    if action == "mark-unresolved":
        role = "unresolved"
    elif requested_role:
        role = str(requested_role)
    elif grammar_ids:
        role = "learnable-grammar"
    elif any(item.get("displayRole") == "lexical-compound" for item in overlaps):
        role = "lexical-compound"
    elif lexical_keys:
        role = "lexical"
    else:
        role = "unresolved"

    if role not in _ALLOWED_ROLES:
        raise ValueError("Unknown displayRole")

    grammar_id = grammar_ids[0] if len(grammar_ids) == 1 else None
    host_lookup_key = lexical_keys[0] if len(lexical_keys) == 1 else None
    lookup = host_lookup_key if role in {"lexical", "lexical-compound"} else None

    # A taught lexical unit without a defensible analyzer identity remains neutral.
    if role in {"lexical", "lexical-compound"} and not lookup:
        role = "unresolved"
    # A grammar correction may be structurally taught without a known catalog ID,
    # but when the analyzer has one, it is preserved as evidence.

    snapshot = dict(data.get("featureSnapshot") or {})
    snapshot.update({
        "teachingContractVersion": "1.0",
        "userSuppliedLookupKeys": False,
        "originalPartition": [
            {
                "start": item.get("start"),
                "end": item.get("end"),
                "surface": item.get("surface"),
                "displayRole": item.get("displayRole"),
                "grammarId": item.get("grammarId"),
                "knownLookupKey": item.get("knownLookupKey"),
                "projectionStatus": item.get("projectionStatus"),
            }
            for item in overlaps
        ],
        "derivedEvidence": {
            "grammarIds": grammar_ids,
            "hostLookupKeys": lexical_keys,
            "grammarFocusRanges": grammar_focus_ranges,
        },
        "readerSelection": reader_selection or {},
        **_candidate_snapshot(start, end, reader_candidates),
    })

    return {
        "sentence": text,
        "start": start,
        "end": end,
        "surface": surface,
        "scope": "occurrence",
        "action": action,
        "displayRole": role,
        "headword": lookup,
        "knownLookupKey": lookup,
        "frequencyLookupKey": lookup,
        "grammarId": grammar_id,
        "hostLookupKey": host_lookup_key,
        "grammarFocusRanges": grammar_focus_ranges,
        "unknownColorPolicy": "frequency" if role in {"lexical", "lexical-compound"} else None,
        "featureSnapshot": snapshot,
    }


def corrected_span(data: dict[str, Any], correction_id: str | None = None) -> dict[str, Any]:
    role = data["displayRole"]
    color = {
        "lexical": "known-or-frequency",
        "lexical-compound": "known-or-frequency",
        "name": "name",
        "learnable-grammar": "grammar",
        "function": "muted",
        "punctuation": "neutral",
        "unresolved": "neutral",
    }[role]
    return {
        "start": data["start"],
        "end": data["end"],
        "surface": data["surface"],
        "displayRole": role,
        "lexicalType": "compound" if role == "lexical-compound" else "term" if role == "lexical" else None,
        "colorPolicy": color,
        "unknownColorPolicy": data.get("unknownColorPolicy"),
        "knownLookupKey": data.get("knownLookupKey"),
        "frequencyLookupKey": data.get("frequencyLookupKey"),
        "headword": data.get("headword"),
        "grammarId": data.get("grammarId"),
        "hostLookupKey": data.get("hostLookupKey"),
        "grammarFocusRanges": data.get("grammarFocusRanges") or [],
        "confidence": 1.0,
        "countsForComprehension": role in {"lexical", "lexical-compound"},
        "showInNewWords": role in {"lexical", "lexical-compound"},
        "eligibleForMining": role in {"lexical", "lexical-compound", "name", "learnable-grammar"},
        "sourceSpanIds": [],
        "sourceLayer": "user-correction",
        "projectionStatus": "user-corrected-preview" if not correction_id else "user-corrected",
        "correctionId": correction_id,
        "correctionScope": "occurrence",
        "correctionAction": data.get("action"),
    }


def _replace_range(
    text: str,
    baseline: list[dict[str, Any]],
    data: dict[str, Any],
    correction_id: str | None,
) -> list[dict[str, Any]]:
    start, end = data["start"], data["end"]
    _aligned_overlaps(text, start, end, baseline)
    left = [item for item in baseline if item["end"] <= start]
    right = [item for item in baseline if item["start"] >= end]
    spans = left + [corrected_span(data, correction_id)] + right
    from .reader_projection import validate_reader_spans
    validate_reader_spans(text, spans)
    return spans


def preview(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    derived = derive_structural_correction(
        data,
        baseline,
        reader_candidates=reader_candidates,
        reader_selection=reader_selection,
    )
    spans = _replace_range(derived["sentence"], baseline, derived, None)
    return {
        "sentenceFingerprint": sentence_fingerprint(derived["sentence"]),
        "originalReaderSpans": baseline,
        "previewReaderSpans": spans,
        "derivedCorrection": derived,
        "saved": False,
    }


def save(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    analyzer_version: str,
    schema_version: str,
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = preview(
        data,
        baseline,
        reader_candidates=reader_candidates,
        reader_selection=reader_selection,
    )
    derived = result["derivedCorrection"]
    correction_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        con.execute(
            "INSERT INTO reader_corrections VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL)",
            (
                correction_id,
                derived["sentence"],
                sentence_fingerprint(derived["sentence"]),
                derived["start"],
                derived["end"],
                derived["surface"],
                derived["action"],
                derived["displayRole"],
                derived.get("headword"),
                derived.get("knownLookupKey"),
                derived.get("frequencyLookupKey"),
                derived.get("grammarId"),
                derived.get("unknownColorPolicy"),
                "occurrence",
                analyzer_version,
                schema_version,
                json.dumps(baseline, ensure_ascii=False),
                json.dumps(derived.get("featureSnapshot") or {}, ensure_ascii=False),
                now,
            ),
        )
    result["saved"] = True
    result["correctionId"] = correction_id
    result["previewReaderSpans"] = _replace_range(
        derived["sentence"], baseline, derived, correction_id
    )
    return result


def list_corrections(include_inactive: bool = False) -> list[dict[str, Any]]:
    with _lock, _db() as con:
        rows = con.execute(
            "SELECT * FROM reader_corrections"
            + ("" if include_inactive else " WHERE deactivated_at IS NULL")
            + " ORDER BY created_at"
        ).fetchall()
    return [dict(item) for item in rows]


def _row_to_derived(row: dict[str, Any]) -> dict[str, Any]:
    snapshot = json.loads(row.get("feature_snapshot_json") or "{}")
    evidence = snapshot.get("derivedEvidence") or {}
    host_keys = evidence.get("hostLookupKeys") or []
    return {
        "sentence": row["sentence_text"],
        "start": row["start"],
        "end": row["end"],
        "surface": row["surface"],
        "scope": row["scope"],
        "action": row["action"],
        "displayRole": row["display_role"],
        "headword": row.get("headword"),
        "knownLookupKey": row.get("known_lookup_key"),
        "frequencyLookupKey": row.get("frequency_lookup_key"),
        "grammarId": row.get("grammar_id"),
        "hostLookupKey": host_keys[0] if len(host_keys) == 1 else None,
        "grammarFocusRanges": evidence.get("grammarFocusRanges") or [],
        "unknownColorPolicy": row.get("unknown_color_policy"),
        "featureSnapshot": snapshot,
    }



def correction_revision() -> str:
    """Return a deterministic revision for the active correction set.

    The revision changes when an active correction is added, replaced, or
    deactivated. It is independent of SQLite row order and database timestamps
    that do not affect reader output.
    """
    import hashlib
    import json

    active = []
    for record in list_corrections(include_inactive=False):
        active.append({
            "correctionId": record.get("correctionId"),
            "sentenceFingerprint": record.get("sentenceFingerprint"),
            "start": record.get("start"),
            "end": record.get("end"),
            "surface": record.get("surface"),
            "action": record.get("action"),
            "displayRole": record.get("displayRole"),
            "scope": record.get("scope"),
            "replacementReaderSpans": record.get("replacementReaderSpans") or [],
        })
    active.sort(key=lambda item: str(item.get("correctionId") or ""))
    payload = json.dumps(active, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def apply_active_corrections(
    text: str,
    baseline: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply active exact-occurrence corrections after normal reader selection."""
    fingerprint = sentence_fingerprint(text)
    with _lock, _db() as con:
        rows = con.execute(
            "SELECT * FROM reader_corrections "
            "WHERE sentence_fingerprint=? AND deactivated_at IS NULL "
            "ORDER BY created_at",
            (fingerprint,),
        ).fetchall()
    spans = list(baseline)
    applied: list[dict[str, Any]] = []
    for sqlite_row in rows:
        row = dict(sqlite_row)
        if row["sentence_text"] != text:
            continue
        derived = _row_to_derived(row)
        try:
            spans = _replace_range(text, spans, derived, row["correction_id"])
        except ValueError:
            # Stale corrections never corrupt output; they remain in audit history.
            continue
        applied.append({
            "correctionId": row["correction_id"],
            "action": row["action"],
            "start": row["start"],
            "end": row["end"],
            "surface": row["surface"],
            "displayRole": row["display_role"],
            "scope": row["scope"],
        })
    return spans, applied


def deactivate(correction_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        cursor = con.execute(
            "UPDATE reader_corrections SET deactivated_at=? "
            "WHERE correction_id=? AND deactivated_at IS NULL",
            (now, correction_id),
        )
    if cursor.rowcount != 1:
        raise ValueError("Active correction not found")
    return {"correctionId": correction_id, "active": False, "deactivatedAt": now}
