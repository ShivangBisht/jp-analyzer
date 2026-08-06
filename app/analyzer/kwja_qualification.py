from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .kwja_equivalence import final_fingerprint, final_projection
from .performance import semantic_fingerprint

TEACHING_PROTECTED_FILES = (
    "app/analyzer/reader_corrections.py",
    "app/analyzer/reader_corrections_api.py",
    "app/analyzer/teaching_annotation_contract.py",
    "app/analyzer/teaching_annotation_store.py",
    "app/analyzer/teaching_decision_record.py",
    "app/analyzer/teaching_decision_store.py",
    "app/analyzer/teaching_portability.py",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_file_hashes(root: Path) -> dict[str, str | None]:
    return {
        relative: file_sha256(root / relative) if (root / relative).is_file() else None
        for relative in TEACHING_PROTECTED_FILES
    }


def compare_to_baseline(
    baseline: dict[int, dict[str, Any]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    differences = []
    for row in rows:
        index = int(row["sentenceIndex"])
        expected = baseline[index]
        changed = [
            key
            for key in sorted(set(expected["fieldFingerprints"]) | set(row["fieldFingerprints"]))
            if expected["fieldFingerprints"].get(key) != row["fieldFingerprints"].get(key)
        ]
        if row["finalAnalyzerFingerprint"] != expected["finalAnalyzerFingerprint"]:
            differences.append({
                "sentenceIndex": index,
                "sequence": row["sequence"],
                "requestOrdinal": row["requestOrdinal"],
                "changedFinalFields": changed,
                "baselineFingerprint": expected["finalAnalyzerFingerprint"],
                "actualFingerprint": row["finalAnalyzerFingerprint"],
            })
    return {
        "qualified": not differences,
        "differenceCount": len(differences),
        "differences": differences,
    }


def result_summary(index: int, sequence: str, ordinal: int, result: dict[str, Any], elapsed_ms: float, process_id: int) -> dict[str, Any]:
    projection = final_projection(result)
    return {
        "sentenceIndex": index,
        "sequence": sequence,
        "requestOrdinal": ordinal,
        "finalAnalyzerFingerprint": final_fingerprint(result),
        "fieldFingerprints": {key: semantic_fingerprint(value) for key, value in projection.items()},
        "elapsedMs": elapsed_ms,
        "workerPid": process_id,
    }
