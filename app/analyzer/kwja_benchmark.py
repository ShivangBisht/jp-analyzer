from __future__ import annotations

import hashlib
import json
from time import perf_counter
from typing import Any, Callable

from .layers.kwja import normalize_kwja, run_kwja
from .performance import semantic_fingerprint

SCHEMA = "Phase12A2AKwjaMeasurement.v1"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_knp_fingerprint(raw_knp: str) -> str:
    """Fingerprint KNP content while excluding volatile comment headers."""
    stable_lines = [
        line.rstrip()
        for line in raw_knp.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if not line.startswith("#") and line.rstrip()
    ]
    return sha256_text("\n".join(stable_lines) + "\n")


def measure_kwja_once(
    text: str,
    *,
    executable: str,
    model_size: str = "base",
    timeout_seconds: int = 300,
    runner: Callable[..., tuple[str, float]] = run_kwja,
    normalizer: Callable[..., dict[str, Any]] = normalize_kwja,
) -> dict[str, Any]:
    execution_started = perf_counter()
    raw_knp, reported_ms = runner(
        text,
        executable=executable,
        model_size=model_size,
        timeout_seconds=timeout_seconds,
    )
    execution_wall_ms = (perf_counter() - execution_started) * 1000

    normalization_started = perf_counter()
    normalized = normalizer(
        text,
        raw_knp,
        model_size=model_size,
        elapsed_ms=None,
    )
    normalization_ms = (perf_counter() - normalization_started) * 1000

    metadata = normalized.get("kwja_metadata_alpha1") or {}
    diagnostics = normalized.get("kwja_alignment_diagnostics_alpha1") or []
    return {
        "schema": SCHEMA,
        "sentenceSha256": sha256_text(text),
        "sourceLength": len(text),
        "rawExecutionReportedMs": reported_ms,
        "rawExecutionWallMs": execution_wall_ms,
        "normalizationMs": normalization_ms,
        "combinedMeasuredMs": execution_wall_ms + normalization_ms,
        "rawOutputBytes": len(raw_knp.encode("utf-8")),
        "rawOutputSha256": sha256_text(raw_knp),
        "normalizedKnpSha256": normalized_knp_fingerprint(raw_knp),
        "adapterSemanticFingerprint": semantic_fingerprint(normalized),
        "sourceAlignmentComplete": bool(metadata.get("source_alignment_complete")),
        "diagnosticCount": len(diagnostics),
        "errorDiagnosticCount": sum(
            item.get("severity") == "error" for item in diagnostics
        ),
        "counts": {
            "morphemes": len(normalized.get("kwja_morphemes_alpha1") or []),
            "bunsetsu": len(normalized.get("kwja_bunsetsu_alpha1") or []),
            "basicPhrases": len(normalized.get("kwja_basic_phrases_alpha1") or []),
            "dependencies": len(normalized.get("kwja_dependencies_alpha1") or []),
            "predicates": len(normalized.get("kwja_predicate_phrases_alpha1") or []),
            "arguments": len(normalized.get("kwja_argument_evidence_alpha1") or []),
        },
    }


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def stats(field: str) -> dict[str, float | None]:
        values = sorted(float(row[field]) for row in rows if row.get(field) is not None)
        if not values:
            return {"minimum": None, "median": None, "mean": None, "maximum": None}
        middle = len(values) // 2
        median = (
            values[middle]
            if len(values) % 2
            else (values[middle - 1] + values[middle]) / 2
        )
        return {
            "minimum": values[0],
            "median": median,
            "mean": sum(values) / len(values),
            "maximum": values[-1],
        }

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["sentenceSha256"], []).append(row)

    equivalence = []
    for sentence_hash, items in grouped.items():
        equivalence.append({
            "sentenceSha256": sentence_hash,
            "attempts": len(items),
            "distinctRawOutputs": len({item["rawOutputSha256"] for item in items}),
            "distinctNormalizedKnp": len({item["normalizedKnpSha256"] for item in items}),
            "distinctAdapterSemantics": len({item["adapterSemanticFingerprint"] for item in items}),
            "allAligned": all(item["sourceAlignmentComplete"] for item in items),
            "errorDiagnostics": sum(item["errorDiagnosticCount"] for item in items),
        })

    return {
        "requestCount": len(rows),
        "rawExecutionReportedMs": stats("rawExecutionReportedMs"),
        "rawExecutionWallMs": stats("rawExecutionWallMs"),
        "normalizationMs": stats("normalizationMs"),
        "combinedMeasuredMs": stats("combinedMeasuredMs"),
        "equivalence": equivalence,
        "semanticDriftDetected": any(
            item["distinctAdapterSemantics"] != 1 for item in equivalence
        ),
        "normalizedKnpDriftDetected": any(
            item["distinctNormalizedKnp"] != 1 for item in equivalence
        ),
    }
