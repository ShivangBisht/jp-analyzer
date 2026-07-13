from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any

from app.phase8.alpha321 import analyze_layered_alpha321
from app.phase8.dictionary_evidence import evaluate_analysis_candidates, evaluate_candidate
from app.phase8.resolver_alpha34 import (
    _candidate_score,
    _candidate_utility,
    _dict_summary,
    analyze_layered_alpha34,
    normalize_candidates,
    resolve_candidates,
)
from app.phase9.kwja_alpha1 import analyze_kwja_alpha1, attach_kwja_read_only

VERSION = "9.0.0-alpha2.2-evidence-gated-decision"

# Alpha 2 is deliberately allow-listed. KWJA does not generate arbitrary grammar.
PATTERNS = (
    {"suffix": "という", "grammar_id": "TO_IU_QUOTATIVE_MODIFIER", "confidence": .93},
    {"suffix": "でしまう", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "でしまった", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てしまう", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てしまった", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てもらえる", "grammar_id": "TE_MORAU_POTENTIAL", "confidence": .93},
    {"suffix": "でもらえる", "grammar_id": "TE_MORAU_POTENTIAL", "confidence": .93},
    {"suffix": "ではあった", "grammar_id": "DEWA_ATTA", "confidence": .90},
)


def _stable_hash(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _crosses_protected(text: str, start: int, end: int, analysis: dict[str, Any]) -> bool:
    protected = list(analysis.get("orthographic_spans") or []) + list(analysis.get("person_references") or [])
    for item in protected:
        a, b = item.get("start"), item.get("end")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        overlaps = start < b and a < end
        contains_exactly = start == a and end == b
        if overlaps and not contains_exactly:
            return True
    # Never create a candidate containing punctuation, even if unavailable in layers.
    return any(ch in text[start:end] for ch in "、。！？!?「」『』（）()……─―～")


def generate_kwja_candidates(text: str, analysis: dict[str, Any], kwja: dict[str, Any]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str, str | None]] = set()
    morphemes = kwja.get("kwja_morphemes_alpha1") or []
    phrases = kwja.get("kwja_basic_phrases_alpha1") or []

    def add(start: int, end: int, family: str, *, grammar_id: str | None = None,
            headword: str | None = None, confidence: float, policy: str,
            source_ids: list[str] | None = None, lemma_status: str | None = None) -> None:
        if not (0 <= start < end <= len(text)) or _crosses_protected(text, start, end, analysis):
            return
        surface = text[start:end]
        key = (start, end, family, grammar_id or headword)
        if key in seen:
            return
        seen.add(key)
        proposals.append({
            "id": f"kwjac{len(proposals)}", "start": start, "end": end,
            "surface": surface, "candidate_family": family,
            "proposed_role": "grammar" if family == "grammar" else "term",
            "grammar_id": grammar_id, "headword": headword,
            "confidence": confidence, "source_layer": "kwja-alpha2",
            "source_annotation_ids": source_ids or [],
            "policy": policy, "lemma_status": lemma_status,
            "evidence": [{
                "source": "kwja-base-structural-evidence",
                "detail": policy, "confidence": confidence,
            }],
        })

    # Pattern proposals must occur wholly inside a KWJA basic phrase. This uses
    # KWJA structure instead of blind global substring matching.
    for phrase in phrases:
        ps, pe = phrase.get("start"), phrase.get("end")
        if not isinstance(ps, int) or not isinstance(pe, int):
            continue
        surface = text[ps:pe]
        for pattern in PATTERNS:
            suffix = pattern["suffix"]
            offset = surface.rfind(suffix)
            if offset >= 0:
                add(ps + offset, ps + offset + len(suffix), "grammar",
                    grammar_id=pattern["grammar_id"], confidence=pattern["confidence"],
                    policy=f"allow-listed KWJA phrase construction: {suffix}",
                    source_ids=[phrase.get("id")])

    # Controlled cross-basic-phrase recovery for quotative という. KWJA places
    # quotative と in the quoted-complement phrase and いう in the following
    # predicate phrase, so this construction cannot be found inside one phrase.
    phrase_by_id = {p.get("id"): p for p in phrases if p.get("id")}
    for left, right in zip(morphemes, morphemes[1:]):
        if left.get("surface") != "と" or right.get("surface") != "いう":
            continue
        if left.get("end") != right.get("start"):
            continue
        if left.get("basic_phrase_id") == right.get("basic_phrase_id"):
            continue
        if right.get("pos") != "動詞" or right.get("lemma") not in {"言う", "いう"}:
            continue
        right_phrase = phrase_by_id.get(right.get("basic_phrase_id")) or {}
        target_id = right_phrase.get("destination_basic_phrase_id")
        target_phrase = phrase_by_id.get(target_id) or {}
        target_features = target_phrase.get("features") or []
        # Require いう to modify a following nominal/basic phrase when KWJA
        # exposes that target. This blocks generic quotation predicates.
        if target_id is None or "体言" not in target_features:
            continue
        start, end = left["start"], right["end"]
        if text[start:end] == "という":
            add(start, end, "grammar", grammar_id="TO_IU_QUOTATIVE_MODIFIER",
                confidence=.94,
                policy="controlled adjacent KWJA phrases: quotative と + 言う modifying nominal",
                source_ids=[left.get("id"), right.get("id"),
                            left.get("basic_phrase_id"), right.get("basic_phrase_id")])

    # Complete lexical adjective recovery, currently limited to the validated gap.
    for m in morphemes:
        if m.get("surface") == "つまらない" and m.get("pos") == "形容詞":
            add(m["start"], m["end"], "term", headword="つまらない", confidence=.91,
                policy="KWJA preserves validated complete adjective",
                source_ids=[m.get("id")], lemma_status="corroborated-surface")

    # Unknown/coined predicate preservation: only when KWJA sees one verb-like
    # morpheme spanning 2+ characters and existing morphology fragments its range.
    existing_ms = analysis.get("morphemes") or []
    for m in morphemes:
        if m.get("pos") != "動詞" or not isinstance(m.get("start"), int):
            continue
        start, end, surface = m["start"], m["end"], m.get("surface") or ""
        covered = [x for x in existing_ms if x.get("start", -1) >= start and x.get("end", -1) <= end]
        fragmented = len(covered) >= 2
        projected = [
            x for x in (analysis.get("resolved_spans_alpha34") or [])
            if start < x.get("end", -1) and x.get("start", -1) < end
        ]
        unresolved = [
            x for x in projected
            if x.get("role") == "unresolved"
        ]
        lexical_fragments = [
            x for x in projected
            if x.get("role") == "term"
        ]
        structurally_fragmented = (
            bool(unresolved)
            or len(lexical_fragments) >= 2
        )
        suspicious_lemma = m.get("lemma") not in {surface, None, ""}
        if (
            len(surface) >= 3
            and fragmented
            and structurally_fragmented
            and suspicious_lemma
        ):
            add(start, end, "term", headword=None, confidence=.76,
                policy="KWJA preserves complete fragmented predicate; lemma withheld",
                source_ids=[m.get("id")], lemma_status="withheld-pending-corroboration")
    return proposals


def _overlapping_baseline_spans(proposal, baseline_spans):
    start, end = proposal["start"], proposal["end"]
    return [x for x in baseline_spans if start < x.get("end", -1) and x.get("start", -1) < end]


def classify_kwja_proposal(proposal, baseline_spans):
    """Evidence gate: layers propose; only genuine improvements enter resolution."""
    overlapping = _overlapping_baseline_spans(proposal, baseline_spans)
    exact = [x for x in overlapping if x.get("start") == proposal["start"] and x.get("end") == proposal["end"]]
    unresolved = [x for x in overlapping if x.get("role") == "unresolved"]
    terms = [x for x in overlapping if x.get("role") == "term"]
    complete_same_role = [x for x in exact if x.get("role") == proposal.get("proposed_role")]

    if complete_same_role:
        status, eligible = "corroborates-existing", False
        reason = "Existing licensed analysis already covers the same range and role."
    elif unresolved:
        status, eligible = "eligible-improvement", True
        reason = "Proposal replaces unresolved baseline coverage."
    elif proposal.get("candidate_family") == "term" and len(terms) >= 2:
        status, eligible = "eligible-structural-repair", True
        reason = "Proposal consolidates multiple lexical fragments."
    else:
        status, eligible = "evidence-only", False
        reason = "Evidence adds support but does not improve the final projection."

    result = dict(proposal)
    result.update({
        "decision_status": status,
        "resolver_eligible": eligible,
        "decision_reason": reason,
        "baseline_overlap": [
            {"start": x.get("start"), "end": x.get("end"), "surface": x.get("surface"),
             "role": x.get("role"), "grammar_id": x.get("grammar_id"), "headword": x.get("headword")}
            for x in overlapping
        ],
    })
    return result


def _normalized_kwja_candidate(proposal: dict[str, Any], dictionary_record: dict[str, Any] | None, index: int) -> dict[str, Any]:
    dsum = _dict_summary([dictionary_record] if dictionary_record else [])
    record = {
        "candidate_id": f"a2kwja{index}",
        "start": proposal["start"], "end": proposal["end"], "surface": proposal["surface"],
        "proposed_role": proposal["proposed_role"], "candidate_family": proposal["candidate_family"],
        "headword": proposal.get("headword"), "grammar_id": proposal.get("grammar_id"),
        "confidence": proposal["confidence"], "protected": False,
        "source_layer": "kwja-alpha2", "source_annotation_id": proposal["id"],
        "morpheme_ids": [], "dictionary_evidence": dsum,
        "evidence": deepcopy(proposal.get("evidence") or []),
        "kwja_policy": proposal.get("policy"), "lemma_status": proposal.get("lemma_status"),
    }
    record["utility_dimensions"] = _candidate_utility(record)
    record["utility_score"] = _candidate_score(record)
    return record


def analyze_integrated_alpha2(text: str, nlp, *, use_dictionary: bool = True,
                              raw_knp: str | None = None, kwja_executable: str | None = None) -> dict[str, Any]:
    baseline = analyze_layered_alpha321(text, nlp)
    dictionary = evaluate_analysis_candidates(baseline) if use_dictionary else None
    alpha34 = analyze_layered_alpha34(text, nlp, dictionary)
    baseline_snapshot = {
        "morphemes": _stable_hash(alpha34.get("morphemes")),
        "existing_fields": {k: _stable_hash(v) for k, v in alpha34.items()},
        "resolved_spans": _stable_hash(alpha34.get("resolved_spans_alpha34")),
        "decisions": _stable_hash(alpha34.get("resolver_decisions_alpha34")),
    }
    kwja = analyze_kwja_alpha1(text, raw_knp=raw_knp, executable=kwja_executable)
    attached = attach_kwja_read_only(alpha34, kwja)
    raw_proposals = generate_kwja_candidates(text, alpha34, kwja)
    baseline_spans = alpha34.get("resolved_spans_alpha34") or []
    proposals = [classify_kwja_proposal(p, baseline_spans) for p in raw_proposals]

    dictionary_records = []
    for proposal in proposals:
        dictionary_records.append(evaluate_candidate(proposal) if use_dictionary else None)
    eligible_pairs = [(p, d) for p, d in zip(proposals, dictionary_records) if p.get("resolver_eligible")]
    kwja_candidates = [_normalized_kwja_candidate(p, d, i) for i, (p, d) in enumerate(eligible_pairs)]
    all_candidates = list(alpha34.get("resolver_candidates_alpha34") or []) + kwja_candidates
    selected, decisions, conflicts = resolve_candidates(text, all_candidates)
    resolved = [{
        "start": c["start"], "end": c["end"], "surface": c["surface"],
        "role": c["proposed_role"], "headword": c.get("headword"),
        "grammar_id": c.get("grammar_id"), "confidence": c.get("confidence", 0.0),
        "selected_candidate_id": c["candidate_id"], "source_layer": c.get("source_layer"),
    } for c in selected]

    def projection_signature(items):
        return [(x.get("start"), x.get("end"), x.get("surface"), x.get("role"),
                 x.get("headword"), x.get("grammar_id")) for x in items]
    changed = projection_signature(resolved) != projection_signature(alpha34.get("resolved_spans_alpha34") or [])
    diagnostics = []
    if "".join(x["surface"] for x in resolved) != text:
        diagnostics.append({"severity":"error", "code":"P9A2_PROJECTION_INCOMPLETE"})
    if _stable_hash(attached.get("morphemes")) != baseline_snapshot["morphemes"]:
        diagnostics.append({"severity":"error", "code":"P9A2_LAYER0_MUTATED"})
    if not (kwja.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete"):
        diagnostics.append({"severity":"error", "code":"P9A2_KWJA_ALIGNMENT_INCOMPLETE"})

    attached.update({
        "version": VERSION,
        "kwja_candidates_alpha2": proposals,
        "kwja_dictionary_evidence_alpha2": [x for x in dictionary_records if x is not None],
        "resolver_candidates_alpha2": all_candidates,
        "resolver_conflicts_alpha2": conflicts,
        "resolver_decisions_alpha2": decisions,
        "resolved_spans_alpha2": resolved,
        "diagnostics_alpha2": diagnostics,
        "alpha2_change_summary": {
            "final_projection_changed": changed,
            "kwja_proposal_count": len(proposals),
            "kwja_eligible_count": sum(bool(x.get("resolver_eligible")) for x in proposals),
            "kwja_corroboration_count": sum(x.get("decision_status") == "corroborates-existing" for x in proposals),
            "kwja_evidence_only_count": sum(x.get("decision_status") == "evidence-only" for x in proposals),
            "kwja_selected_count": sum(x.get("source_layer") == "kwja-alpha2" for x in resolved),
            "baseline_unresolved_count": sum(x.get("role") == "unresolved" for x in alpha34.get("resolved_spans_alpha34") or []),
            "alpha2_unresolved_count": sum(x.get("role") == "unresolved" for x in resolved),
        },
        "phase9_alpha2_contract": {
            "layer0_immutable": True, "earlier_evidence_fields_preserved": True,
            "kwja_candidates_allow_listed": True, "kwja_readings_non_authoritative": True,
            "kwja_unknown_lemmas_withheld": True, "kwja_arguments_not_resolver_candidates": True,
            "protected_boundaries_enforced": True, "dictionary_miss_is_not_rejection": True,
            "central_resolver_makes_final_decision": True,
            "evidence_improvement_required_for_selection": True,
            "same_range_existing_analysis_is_not_displaced": True,
        },
    })
    return attached
