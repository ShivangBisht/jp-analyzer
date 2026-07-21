from __future__ import annotations

from typing import Any

from .reader_projection import (
    READER_SPAN_SCHEMA_VERSION,
    project_reader_spans,
)
from .version import SCHEMA_VERSION
from .reader_candidates import READER_CANDIDATE_SCHEMA_VERSION, project_reader_candidates
from .reader_candidate_selection import select_reader_output
from .reader_corrections import apply_active_corrections, correction_revision


def compact_analysis(
    result: dict[str, Any],
    *,
    analyzer_version: str,
) -> dict[str, Any]:
    """Project the evidence graph into stable consumer schemas.

    `resolvedSpans` remains unchanged for compatibility and diagnostics.
    `readerSpans` is the versioned, authoritative reader-facing contract.
    This compatibility projection does not merge or reclassify source ranges
    beyond mapping already-selected analyzer roles to display policy fields.
    """
    resolved = result.get("resolved_spans_alpha2") or []
    evaluated_reader_candidates = project_reader_candidates(result)
    reader_spans, reader_candidates, reader_selection = select_reader_output(
        result, evaluated_reader_candidates
    )
    reader_spans, applied_corrections = apply_active_corrections(
        result.get("text", ""), reader_spans
    )
    reader_selection = dict(reader_selection)
    reader_selection["appliedCorrections"] = applied_corrections
    reader_selection["appliedCorrectionCount"] = len(applied_corrections)
    diagnostics = result.get("diagnostics_alpha2") or []
    metadata = result.get("kwja_metadata_alpha1") or {}
    change = result.get("alpha2_change_summary") or {}
    text = result.get("text", "")

    return {
        "schemaVersion": SCHEMA_VERSION,
        "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
        "readerCandidateSchemaVersion": READER_CANDIDATE_SCHEMA_VERSION,
        "analyzerVersion": analyzer_version,
        "correctionRevision": correction_revision(),
        "engineVersion": result.get("version"),
        "text": text,
        "resolvedSpans": resolved,
        "readerSpans": reader_spans,
        "readerCandidates": reader_candidates,
        "readerSelection": reader_selection,
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
            "complete": "".join(x.get("surface", "") for x in resolved) == text,
            "readerSpansComplete": "".join(
                x.get("surface", "") for x in reader_spans
            ) == text,
            "unresolvedSpanCount": sum(
                x.get("role") == "unresolved" for x in resolved
            ),
            "readerUnresolvedSpanCount": sum(
                x.get("displayRole") == "unresolved" for x in reader_spans
            ),
            "kwjaAlignmentComplete": bool(
                metadata.get("source_alignment_complete")
            ),
        },
        "changeSummary": change,
        "diagnostics": diagnostics,
    }
