from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FULL_LAYER_KEYS = (
    "morphemes", "orthographic_spans", "person_references",
    "grammar_matches_alpha321", "grammar_matches_alpha32",
    "lexical_items_alpha32", "dictionary_evidence_alpha34",
    "kwja_morphemes_alpha1", "kwja_basic_phrases_alpha1",
    "kwja_dependencies_alpha1", "kwja_entities_alpha1",
    "kwja_candidates_alpha2", "kwja_dictionary_evidence_alpha2",
    "resolver_candidates_alpha2", "resolver_conflicts_alpha2",
    "resolver_decisions_alpha2", "resolved_spans_alpha2",
)
COMPACT_KEYS = (
    "schemaVersion", "readerSpanSchemaVersion", "readerCandidateSchemaVersion",
    "analyzerVersion", "correctionRevision", "engineVersion", "text",
    "readerSpans", "readerCandidates", "readerSelection", "structure",
    "coverage", "changeSummary", "diagnostics",
)


def presence(payload: dict[str, Any], keys: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    return {
        key: {
            "present": key in payload,
            "kind": type(payload.get(key)).__name__ if key in payload else None,
            "count": len(payload[key]) if isinstance(payload.get(key), (list, dict)) else None,
        }
        for key in keys
    }


def audit(payload: dict[str, Any]) -> dict[str, Any]:
    compact = presence(payload, COMPACT_KEYS)
    layers = presence(payload, FULL_LAYER_KEYS)
    required_compact = ("text", "readerSpans", "readerCandidates", "readerSelection", "analyzerVersion", "readerSpanSchemaVersion", "correctionRevision")
    missing_required = [key for key in required_compact if not compact[key]["present"]]
    available_layers = [key for key, value in layers.items() if value["present"]]
    missing_layers = [key for key, value in layers.items() if not value["present"]]
    return {
        "auditSchemaVersion": "1.0",
        "inputClassification": "full-analysis" if available_layers else "compact-analysis",
        "compactContract": compact,
        "fullLayerInventory": layers,
        "saveTimeAssessment": {
            "minimumCompactContractComplete": not missing_required,
            "missingRequiredCompactFields": missing_required,
            "historicalLayerSnapshotComplete": not missing_layers,
            "availableFullLayers": available_layers,
            "missingFullLayers": missing_layers,
            "requiresDedicatedFullSnapshotCapture": bool(missing_layers),
        },
        "contractDecision": {
            "operationalCorrectionPayloadIsEnough": not missing_required,
            "researchGradeAnnotationIsEnough": not missing_required and not missing_layers,
            "reason": "Compact output supports operational correction, but research-grade annotation requires a lossless full-analysis snapshot or immutable snapshot reference." if missing_layers else "Payload contains compact contract and audited full layers.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8-sig"))
    report = audit(payload)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
