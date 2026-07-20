from __future__ import annotations

from typing import Any

READER_SPAN_SCHEMA_VERSION = "1.0"

FUNCTION_GRAMMAR_IDS = {
    "V_TE",
}

DISPLAY_ROLES = {
    "lexical",
    "lexical-compound",
    "name",
    "learnable-grammar",
    "function",
    "punctuation",
    "unresolved",
}


def _candidate_index(result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("candidate_id")): item
        for item in (result.get("resolver_candidates_alpha2") or [])
        if item.get("candidate_id")
    }


def _source_ids(span: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    values = [
        span.get("selected_candidate_id"),
        candidate.get("source_annotation_id"),
    ]
    values.extend(candidate.get("source_annotation_ids") or [])
    return list(dict.fromkeys(str(value) for value in values if value))


def _classification(
    span: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    role = span.get("role")
    family = candidate.get("candidate_family")
    grammar_id = span.get("grammar_id")
    headword = span.get("headword")

    if role == "punctuation" or family == "punctuation":
        return {
            "displayRole": "punctuation",
            "lexicalType": None,
            "colorPolicy": "neutral",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": False,
        }

    if role == "grammar" and grammar_id and grammar_id not in FUNCTION_GRAMMAR_IDS:
        return {
            "displayRole": "learnable-grammar",
            "lexicalType": None,
            "colorPolicy": "grammar",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": True,
        }

    if role in {"particle", "grammar"} or family == "particle":
        return {
            "displayRole": "function",
            "lexicalType": None,
            "colorPolicy": "muted",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": False,
        }

    if role == "proper-name" or family == "proper-name":
        lookup = headword or span.get("surface")
        return {
            "displayRole": "name",
            "lexicalType": "proper-name",
            "colorPolicy": "name",
            "unknownColorPolicy": None,
            "knownLookupKey": lookup,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": True,
        }

    if family == "numeral":
        lookup = headword or span.get("surface")
        return {
            "displayRole": "lexical",
            "lexicalType": "term",
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
            "knownLookupKey": lookup,
            "frequencyLookupKey": lookup,
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
        }

    if role == "term":
        lookup = headword or span.get("surface")
        lexical_type = (
            "discourse"
            if family == "discourse"
            else "term"
        )
        return {
            "displayRole": "lexical",
            "lexicalType": lexical_type,
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
            "knownLookupKey": lookup,
            "frequencyLookupKey": lookup,
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
        }

    return {
        "displayRole": "unresolved",
        "lexicalType": None,
        "colorPolicy": "neutral",
        "unknownColorPolicy": None,
        "knownLookupKey": None,
        "frequencyLookupKey": None,
        "countsForComprehension": False,
        "showInNewWords": False,
        "eligibleForMining": False,
    }


def project_reader_spans(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Create the versioned consumer contract without changing linguistic spans."""
    candidates = _candidate_index(result)
    projected: list[dict[str, Any]] = []

    for span in result.get("resolved_spans_alpha2") or []:
        candidate = candidates.get(str(span.get("selected_candidate_id")), {})
        classification = _classification(span, candidate)
        projected.append({
            "start": span.get("start"),
            "end": span.get("end"),
            "surface": span.get("surface"),
            **classification,
            "headword": span.get("headword"),
            "grammarId": span.get("grammar_id"),
            "confidence": span.get("confidence", 0.0),
            "sourceSpanIds": _source_ids(span, candidate),
            "sourceLayer": span.get("source_layer") or candidate.get("source_layer"),
            "projectionStatus": "compatibility",
        })

    validate_reader_spans(result.get("text", ""), projected)
    return projected


def validate_reader_spans(text: str, spans: list[dict[str, Any]]) -> None:
    cursor = 0
    for index, span in enumerate(spans):
        start = span.get("start")
        end = span.get("end")
        surface = span.get("surface")
        role = span.get("displayRole")

        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"readerSpans[{index}] has non-integer offsets")
        if start != cursor:
            raise ValueError(
                f"readerSpans[{index}] expected start {cursor}, found {start}"
            )
        if not (0 <= start < end <= len(text)):
            raise ValueError(f"readerSpans[{index}] has invalid range {start}:{end}")
        if surface != text[start:end]:
            raise ValueError(f"readerSpans[{index}] surface does not match source")
        if role not in DISPLAY_ROLES:
            raise ValueError(f"readerSpans[{index}] has unknown displayRole {role!r}")
        if role in {"lexical", "lexical-compound",}:
            if not span.get("knownLookupKey") or not span.get("frequencyLookupKey"):
                raise ValueError(
                    f"readerSpans[{index}] lexical span is missing lookup keys"
                )
        cursor = end

    if cursor != len(text):
        raise ValueError(
            f"readerSpans coverage ends at {cursor}; source length is {len(text)}"
        )
