from __future__ import annotations

from collections.abc import Callable, Iterable
from copy import deepcopy
from time import perf_counter
from typing import Any

from .kwja_equivalence import FINAL_FIELDS
from .performance import semantic_fingerprint

AnalyzeFn = Callable[[str, str], dict[str, Any]]


def authoritative_projection(result: dict[str, Any]) -> dict[str, Any]:
    """Return only the frozen final analyzer fields used by Phase 12 parity."""
    return {
        field: deepcopy(result.get(field))
        for field in FINAL_FIELDS
        if field in result
    }


def validate_reader_contract(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    text = str(result.get("text") or "")
    spans = result.get("readerSpans") or []
    reconstructed = "".join(str(item.get("surface") or "") for item in spans)
    if reconstructed != text:
        errors.append("READER_SPANS_DO_NOT_RECONSTRUCT_SOURCE")
    cursor = 0
    for index, span in enumerate(spans):
        start, end = span.get("start"), span.get("end")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"READER_SPAN_{index}_RANGE_NOT_INTEGER")
            continue
        if start != cursor or start < 0 or end < start or end > len(text):
            errors.append(f"READER_SPAN_{index}_RANGE_INVALID")
            continue
        if text[start:end] != str(span.get("surface") or ""):
            errors.append(f"READER_SPAN_{index}_SURFACE_MISMATCH")
        cursor = end
    if cursor != len(text):
        errors.append("READER_SPANS_NOT_CONTIGUOUS")
    coverage = result.get("coverage") or {}
    if coverage.get("readerSpansComplete") is False:
        errors.append("COVERAGE_REPORTS_INCOMPLETE_READER_SPANS")
    return errors


def compare_production_modes(
    sentences: Iterable[str],
    *,
    analyze_fn: AnalyzeFn,
) -> dict[str, Any]:
    """Compare fresh and persistent results through the production adapter API.

    `analyze_fn(text, mode)` must return the normal compact analyzer response.
    The helper stores fingerprints and timing only, never sentence text.
    """
    rows: list[dict[str, Any]] = []
    differences: list[dict[str, Any]] = []
    for index, text in enumerate(sentences):
        by_mode: dict[str, dict[str, Any]] = {}
        for mode in ("fresh", "persistent"):
            started = perf_counter()
            result = analyze_fn(text, mode)
            elapsed_ms = (perf_counter() - started) * 1000
            projection = authoritative_projection(result)
            field_fingerprints = {
                key: semantic_fingerprint(value)
                for key, value in projection.items()
            }
            by_mode[mode] = {
                "result": result,
                "projection": projection,
                "fingerprint": semantic_fingerprint(projection),
                "fieldFingerprints": field_fingerprints,
                "readerContractErrors": validate_reader_contract(result),
                "elapsedMs": elapsed_ms,
            }
        changed = [
            field
            for field in sorted(set(by_mode["fresh"]["fieldFingerprints"]) | set(by_mode["persistent"]["fieldFingerprints"]))
            if by_mode["fresh"]["fieldFingerprints"].get(field)
            != by_mode["persistent"]["fieldFingerprints"].get(field)
        ]
        contract_errors = {
            mode: by_mode[mode]["readerContractErrors"]
            for mode in ("fresh", "persistent")
            if by_mode[mode]["readerContractErrors"]
        }
        row = {
            "sentenceIndex": index,
            "freshFingerprint": by_mode["fresh"]["fingerprint"],
            "persistentFingerprint": by_mode["persistent"]["fingerprint"],
            "changedFinalFields": changed,
            "readerContractErrors": contract_errors,
            "freshElapsedMs": by_mode["fresh"]["elapsedMs"],
            "persistentElapsedMs": by_mode["persistent"]["elapsedMs"],
        }
        rows.append(row)
        if changed or contract_errors:
            differences.append(row)
    return {
        "schema": "Phase12A3CProductionParity.v1",
        "sentenceCount": len(rows),
        "qualified": not differences,
        "differenceCount": len(differences),
        "differences": differences,
        "rows": rows,
        "safety": {
            "sentenceTextIncluded": False,
            "rawKnpIncluded": False,
            "productionDefaultChanged": False,
            "teachingWritesRequested": False,
            "correctionWritesRequested": False,
            "dictionaryWritesRequested": False,
        },
    }
