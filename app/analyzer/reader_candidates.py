from __future__ import annotations
from typing import Any

READER_CANDIDATE_SCHEMA_VERSION = "1.0"


def project_reader_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Expose existing resolver alternatives without generating or selecting new ones."""
    selected = {
        str(x.get("selected_candidate_id"))
        for x in (result.get("resolved_spans_alpha2") or [])
        if x.get("selected_candidate_id")
    }
    out: list[dict[str, Any]] = []
    for item in result.get("resolver_candidates_alpha2") or []:
        cid = str(item.get("candidate_id") or "")
        start, end = item.get("start"), item.get("end")
        if not cid or not isinstance(start, int) or not isinstance(end, int):
            continue
        hard_rejections: list[str] = []
        text = result.get("text", "")
        if not (0 <= start < end <= len(text)):
            hard_rejections.append("invalid-source-range")
        elif item.get("surface") != text[start:end]:
            hard_rejections.append("surface-range-mismatch")
        dictionary = item.get("dictionary_evidence") or {}
        out.append({
            "candidateId": cid,
            "start": start,
            "end": end,
            "surface": item.get("surface", ""),
            "proposedRole": item.get("proposed_role"),
            "candidateFamily": item.get("candidate_family"),
            "possibleLookupKeys": list(dict.fromkeys(x for x in [item.get("headword"), item.get("surface")] if x)),
            "grammarId": item.get("grammar_id"),
            "componentIds": item.get("morpheme_ids") or [],
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
            "hardRejectionReasons": hard_rejections,
            "rankingStatus": "existing-resolver-selection" if cid in selected else "existing-resolver-alternative",
            "selected": cid in selected,
            "selectionReason": "selected by existing analyzer resolver" if cid in selected else None,
            "schemaStatus": "phase-2.2A-foundation",
        })
    return out
