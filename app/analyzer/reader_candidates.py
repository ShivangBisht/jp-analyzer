from __future__ import annotations
from typing import Any

from .reader_candidate_generation import generate_reader_candidates

READER_CANDIDATE_SCHEMA_VERSION = "1.2"


def _existing_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    selected = {
        str(item.get("selected_candidate_id"))
        for item in (result.get("resolved_spans_alpha2") or [])
        if item.get("selected_candidate_id")
    }
    out: list[dict[str, Any]] = []
    for item in result.get("resolver_candidates_alpha2") or []:
        candidate_id = str(item.get("candidate_id") or "")
        start, end = item.get("start"), item.get("end")
        if not candidate_id or not isinstance(start, int) or not isinstance(end, int):
            continue
        text = result.get("text", "")
        hard = []
        if not (0 <= start < end <= len(text)):
            hard.append("invalid-source-range")
        elif item.get("surface") != text[start:end]:
            hard.append("surface-range-mismatch")
        dictionary = item.get("dictionary_evidence") or {}
        out.append({
            "candidateId": candidate_id,
            "candidateSource": "existing-resolver",
            "start": start,
            "end": end,
            "surface": item.get("surface", ""),
            "proposedRole": item.get("proposed_role"),
            "candidateFamily": item.get("candidate_family"),
            "possibleLookupKeys": list(dict.fromkeys(x for x in [item.get("headword"), item.get("surface")] if x)),
            "preferredLookupKey": item.get("headword"),
            "grammarId": item.get("grammar_id"),
            "componentIds": item.get("morpheme_ids") or [],
            "evidence": item.get("evidence") or [],
            "conflictingEvidence": [],
            "features": {
                "dictionaryMatched": bool(dictionary.get("matched")),
                "dictionaryIndependentSourceCount": int(dictionary.get("independent_source_count") or 0),
                "dictionaryPosCompatible": bool(dictionary.get("pos_compatible")),
                "protected": bool(item.get("protected")),
                "sourceLayer": item.get("source_layer"),
                "utilityDimensions": list(item.get("utility_dimensions") or []),
                "utilityScore": item.get("utility_score"),
                "confidence": item.get("confidence"),
            },
            "hardRejectionReasons": hard,
            "rankingStatus": "existing-resolver-selection" if candidate_id in selected else "existing-resolver-alternative",
            "selected": candidate_id in selected,
            "selectionReason": "selected by existing analyzer resolver" if candidate_id in selected else None,
            "schemaStatus": "phase-2.2A-existing-candidate",
        })
    return out


def project_reader_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Expose existing and generated alternatives without changing readerSpans."""
    existing = _existing_candidates(result)
    generated = generate_reader_candidates(result)
    return existing + generated
