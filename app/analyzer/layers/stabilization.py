from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

from .candidates import analyze_layered_alpha32, _project

# Generic families must never displace a more specific, already licensed grammar
# covering the same source range.
GENERIC_GRAMMAR_IDS = {
    "TE_IRU_CHAIN",
}
SPECIFICITY = {
    "TE_IRU_PAST": 50,
    "TE_IRU_NEGATIVE": 50,
    "TE_IRU_POLITE": 50,
    "DE_IRU_PAST": 50,
    "TE_IRU_CHAIN": 10,
}

DISCOURSE_WINDOWS = {
    ("で", "も"): ("でも", "でも"),
}
BOUNDARY_PUNCT = {"。", "！", "？", "!", "?", "、", "，", ",", "…", "……", "─", "──", "―", "――", "「", "『", "（", "("}


def _snapshot(items: list[dict[str, Any]]) -> str:
    payload = repr([
        (x.get("id"), x.get("start"), x.get("end"), x.get("surface"), x.get("lemma"), x.get("pos"), x.get("tag"))
        for x in items
    ])
    return sha256(payload.encode("utf-8")).hexdigest()


def _stabilize_grammar(grammar: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retain every annotation but make specificity explicit for projection.

    Alpha 3.2 annotations remain present and unchanged in grammar_matches_alpha32.
    This function works on a copy for the Alpha 3.2.1 projection only.
    """
    out = deepcopy(grammar)
    by_range: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for g in out:
        by_range.setdefault((g["start"], g["end"]), []).append(g)

    for same_range in by_range.values():
        best_specificity = max((SPECIFICITY.get(g.get("grammar_id"), 25) for g in same_range), default=25)
        for g in same_range:
            gid = g.get("grammar_id")
            current_specificity = SPECIFICITY.get(gid, 25)
            g["projection_specificity_alpha321"] = current_specificity
            if gid in GENERIC_GRAMMAR_IDS and current_specificity < best_specificity:
                # Lower only the copied projection priority. The original record is preserved.
                g["priority"] = min(int(g.get("priority", 0)), 70)
                g.setdefault("evidence", []).append({
                    "source": "alpha3.2.1-specificity-policy",
                    "detail": "generic grammar retained but projection yields to a more specific annotation on the same range",
                    "confidence": 1.0,
                })
    return out


def _is_clause_boundary(text: str, start: int) -> bool:
    if start == 0:
        return True
    prefix = text[:start].rstrip()
    if not prefix:
        return True
    return prefix[-1] in BOUNDARY_PUNCT


def _discourse_windows(text: str, morphemes: list[dict[str, Any]], existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add contextual multi-morpheme discourse connectives without mutating Alpha 3.2 records."""
    out = deepcopy(existing)
    seen = {(d["start"], d["end"], d["surface"]) for d in out}
    ms = sorted(morphemes, key=lambda x: (x["start"], x["end"]))

    for i in range(len(ms) - 1):
        first, second = ms[i], ms[i + 1]
        if first["end"] != second["start"]:
            continue
        key = (first["surface"], second["surface"])
        if key not in DISCOURSE_WINDOWS:
            continue
        if not _is_clause_boundary(text, first["start"]):
            continue
        surface, headword = DISCOURSE_WINDOWS[key]
        if text[first["start"]:second["end"]] != surface:
            continue
        identity = (first["start"], second["end"], surface)
        if identity in seen:
            continue
        out.append({
            "id": f"a321disc{len(out)}",
            "start": first["start"],
            "end": second["end"],
            "surface": surface,
            "role": "discourse-connective",
            "headword": headword,
            "morpheme_ids": [first["id"], second["id"]],
            "confidence": 0.96,
            "evidence": [{
                "source": "alpha3.2.1-contextual-discourse-window",
                "detail": "adjacent morphemes at sentence/clause boundary",
                "confidence": 0.96,
            }],
        })
        seen.add(identity)
    return out


def analyze_layered_alpha321(text, nlp, dictionary_evidence=None):
    base = analyze_layered_alpha32(text, nlp, dictionary_evidence)
    result = deepcopy(base)
    morphemes = deepcopy(result["morphemes"])
    before = _snapshot(morphemes)

    grammar = _stabilize_grammar(result["grammar_matches_alpha32"])
    discourse = _discourse_windows(text, morphemes, result["discourse_connectives_alpha32"])

    colors, decisions = _project(
        text,
        morphemes,
        result["orthographic_spans"],
        result["person_references"],
        grammar,
        result["lexical_items_alpha32"],
        result["numeral_expressions_alpha32"],
        discourse,
    )

    diagnostics = []
    if before != _snapshot(morphemes):
        diagnostics.append({
            "severity": "error",
            "code": "MORPHOLOGY_MUTATED",
            "message": "Alpha 3.2.1 changed Layer 0 morphology.",
        })
    if "".join(span["surface"] for span in colors) != text:
        diagnostics.append({
            "severity": "error",
            "code": "A321_COLOR_INCOMPLETE",
            "message": "Alpha 3.2.1 projection does not reconstruct source text.",
        })

    result.update({
        "version": "8.0.0-alpha3.2.1",
        "grammar_matches_alpha321": grammar,
        "discourse_connectives_alpha321": discourse,
        "reader_decisions_alpha321": decisions,
        "color_spans_alpha321": colors,
        "diagnostics_alpha321": diagnostics,
        "layer0_snapshot_alpha321": before,
        "alpha321_contract": {
            "non_destructive": True,
            "alpha32_preserved": True,
            "only_reader_projection_is_exclusive": True,
            "specific_grammar_outranks_generic_same_range": True,
        },
    })
    return result


analyze = analyze_layered_alpha321
