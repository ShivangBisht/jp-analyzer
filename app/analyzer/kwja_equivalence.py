from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from .performance import semantic_fingerprint

FINAL_FIELDS = (
    "text",
    "readerSpans",
    "readerCandidates",
    "readerSelection",
    "resolvedSpans",
    "coverage",
    "diagnostics",
)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def final_projection(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(result.get(key))
        for key in FINAL_FIELDS
        if key in result
    }


def final_fingerprint(result: dict[str, Any]) -> str:
    return semantic_fingerprint(final_projection(result))


def compare_final_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    fingerprints = [final_fingerprint(item) for item in results]
    baseline = final_projection(results[0]) if results else {}
    differences = []
    for index, result in enumerate(results[1:], start=2):
        projected = final_projection(result)
        changed = [
            key for key in sorted(set(baseline) | set(projected))
            if semantic_fingerprint(baseline.get(key))
            != semantic_fingerprint(projected.get(key))
        ]
        differences.append({
            "attempt": index,
            "fingerprint": fingerprints[index - 1],
            "changedFinalFields": changed,
        })
    return {
        "attemptCount": len(results),
        "distinctFinalFingerprints": len(set(fingerprints)),
        "finalFingerprints": fingerprints,
        "differencesFromFirst": differences,
    }


def request_summary(
    *,
    sentence_index: int,
    request_ordinal: int,
    raw_knp: str,
    normalized_knp_fingerprint: str,
    adapter_fingerprint: str,
    final_result: dict[str, Any],
    elapsed_ms: float,
    process_id: int,
) -> dict[str, Any]:
    return {
        "sentenceIndex": sentence_index,
        "requestOrdinal": request_ordinal,
        "rawKnpSha256": sha256_text(raw_knp),
        "normalizedKnpSha256": normalized_knp_fingerprint,
        "adapterSemanticFingerprint": adapter_fingerprint,
        "finalAnalyzerFingerprint": final_fingerprint(final_result),
        "finalFieldFingerprints": {
            key: semantic_fingerprint(value)
            for key, value in final_projection(final_result).items()
        },
        "elapsedMs": elapsed_ms,
        "processId": process_id,
    }
