from __future__ import annotations

from typing import Any

from .version import SCHEMA_VERSION


def compact_analysis(
    result: dict[str, Any],
    *,
    analyzer_version: str,
) -> dict[str, Any]:
    """Project the full evidence graph into the stable consumer schema.

    This function does not make linguistic decisions. It only exposes fields
    already decided by the validated resolver.
    """
    resolved = result.get("resolved_spans_alpha2") or []
    diagnostics = result.get("diagnostics_alpha2") or []
    metadata = result.get("kwja_metadata_alpha1") or {}
    change = result.get("alpha2_change_summary") or {}

    return {
        "schemaVersion": SCHEMA_VERSION,
        "analyzerVersion": analyzer_version,
        "engineVersion": result.get("version"),
        "text": result.get("text", ""),
        "resolvedSpans": resolved,
        "structure": {
            "predicates": result.get("predicates") or [],
            "clauses": result.get("clauses") or [],
            "arguments": result.get("arguments") or [],
            "predicateRelations": result.get("predicate_relations_alpha31")
            or result.get("predicate_relations")
            or [],
            "entities": result.get("entities") or [],
            "personReferences": result.get("person_references") or [],
        },
        "coverage": {
            "complete": "".join(x.get("surface", "") for x in resolved)
            == result.get("text", ""),
            "unresolvedSpanCount": sum(
                x.get("role") == "unresolved" for x in resolved
            ),
            "kwjaAlignmentComplete": bool(
                metadata.get("source_alignment_complete")
            ),
        },
        "changeSummary": change,
        "diagnostics": diagnostics,
    }
