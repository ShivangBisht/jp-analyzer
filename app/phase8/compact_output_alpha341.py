from __future__ import annotations
from collections import Counter
from typing import Any


def _compact_predicate(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "start": item.get("start"),
        "end": item.get("end"),
        "surface": item.get("surface"),
        "headword": item.get("headword") or item.get("lemma"),
        "confidence": item.get("confidence"),
    }


def _compact_clause(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "type": item.get("type") or item.get("clause_type"),
        "start": item.get("start"),
        "end": item.get("end"),
        "surface": item.get("surface"),
        "predicate_id": item.get("predicate_id"),
        "modified_target": item.get("modified_target") or item.get("modifies"),
        "confidence": item.get("confidence"),
    }


def _compact_relation(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "from_predicate_id": item.get("from_predicate_id"),
        "to_predicate_id": item.get("to_predicate_id"),
        "semantic_relation": item.get("semantic_relation") or item.get("relation"),
        "marker_range": item.get("marker_range"),
        "construction_surface": item.get("construction_surface"),
        "confidence": item.get("confidence"),
    }


def compact_alpha34(result: dict[str, Any], *, debug: bool = False) -> dict[str, Any]:
    if debug:
        return result

    spans = result.get("resolved_spans_alpha34") or []
    decisions = result.get("resolver_decisions_alpha34") or []
    conflicts = result.get("resolver_conflicts_alpha34") or []
    diagnostics = result.get("diagnostics_alpha34") or []
    dictionary = result.get("dictionary_evidence_alpha34") or {}
    evidence = dictionary.get("evidence") or dictionary.get("dictionary_evidence") or []

    decision_by_candidate = {
        d.get("selected_candidate_id"): d for d in decisions if d.get("selected_candidate_id")
    }
    resolved = []
    for span in spans:
        decision = decision_by_candidate.get(span.get("selected_candidate_id"), {})
        resolved.append({
            "start": span.get("start"),
            "end": span.get("end"),
            "surface": span.get("surface"),
            "role": span.get("role"),
            "headword": span.get("headword"),
            "grammar_id": span.get("grammar_id"),
            "confidence": span.get("confidence"),
            "decision_policies": decision.get("decision_policies") or [],
            "reason": decision.get("reason"),
        })

    projected_grammar = Counter(
        str(x.get("grammar_id")) for x in resolved if x.get("role") == "grammar" and x.get("grammar_id")
    )
    roles = Counter(str(x.get("role") or "unknown") for x in resolved)
    unresolved = [x for x in resolved if x.get("role") == "unresolved"]
    unresolved_conflicts = [x for x in conflicts if not x.get("resolved")]
    confidences = [float(x.get("confidence")) for x in resolved if x.get("confidence") is not None]

    predicates = result.get("predicates") or []
    clauses = result.get("clauses") or []
    relations = (
        result.get("predicate_relations_alpha31")
        or result.get("predicate_relations_alpha3")
        or result.get("predicate_relations")
        or []
    )

    matched = [x for x in evidence if x.get("matched")]
    return {
        "text": result.get("text"),
        "version": "8.0.0-alpha3.4.1",
        "resolved_spans": resolved,
        "structure_summary": {
            "predicates": [_compact_predicate(x) for x in predicates],
            "clauses": [_compact_clause(x) for x in clauses],
            "predicate_relations": [_compact_relation(x) for x in relations],
        },
        "dictionary_summary": {
            "ready": bool(dictionary.get("dictionary_ready")),
            "candidate_count": dictionary.get("candidate_count", len(evidence)),
            "matched_count": dictionary.get("matched_candidate_count", len(matched)),
            "unmatched_count": dictionary.get("unmatched_candidate_count", len(evidence) - len(matched)),
            "dictionary_type_evidence_counts": dictionary.get("dictionary_type_evidence_counts") or {},
        },
        "resolver_summary": {
            "candidate_count": len(result.get("resolver_candidates_alpha34") or []),
            "decision_count": len(decisions),
            "conflict_count": len(conflicts),
            "unresolved_conflict_count": len(unresolved_conflicts),
            "unresolved_span_count": len(unresolved),
            "minimum_confidence": min(confidences) if confidences else None,
            "role_counts": dict(roles),
            "projected_grammar_distribution": dict(projected_grammar),
        },
        "coverage": {
            "complete": "".join(str(x.get("surface") or "") for x in resolved) == str(result.get("text") or ""),
            "span_count": len(resolved),
        },
        "diagnostics": diagnostics,
        "contract": {
            "compact_response_only": True,
            "full_evidence_available_in_debug_mode": True,
            "dictionary_is_evidence_only": True,
            "earlier_layers_preserved_in_debug_mode": True,
        },
    }
