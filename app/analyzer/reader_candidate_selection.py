from __future__ import annotations

from copy import deepcopy
from typing import Any

from .reader_projection import project_reader_spans, validate_reader_spans

POLICY_VERSION = "1.0"


def _dictionary(candidate: dict[str, Any]) -> dict[str, Any]:
    return candidate.get("dictionaryEvaluation") or {}


def _structural(candidate: dict[str, Any], key: str) -> dict[str, Any]:
    return (candidate.get("candidateStructuralEvidence") or {}).get(key) or {}


def _kwja_conflict(candidate: dict[str, Any]) -> bool:
    kwja = _structural(candidate, "kwja")
    return bool(kwja.get("crossesBasicPhraseBoundary") or kwja.get("crossesPredicatePhraseBoundary"))


def _same_range_grammar(candidate: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> bool:
    competition = _structural(candidate, "competition")
    for candidate_id in competition.get("sameRangeCandidateIds") or []:
        other = by_id.get(candidate_id) or {}
        if other.get("candidateFamily") == "complete-grammar":
            grammar = _structural(other, "grammar")
            if other.get("grammarId") in (grammar.get("completeLearnableGrammarIds") or []):
                return True
    return False


def _unique_matched_key(candidate: dict[str, Any], *, complete: bool = False) -> str | None:
    dictionary = _dictionary(candidate)
    values = (
        dictionary.get("matchedCompleteLookupKeys")
        if complete
        else dictionary.get("matchedComponentKeys")
    ) or []
    values = list(dict.fromkeys(str(x) for x in values if x))
    return values[0] if len(values) == 1 else None


def _eligible(candidate: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> tuple[bool, str | None, list[str]]:
    family = candidate.get("candidateFamily")
    morphology = _structural(candidate, "morphology")
    predicates = _structural(candidate, "predicates")
    grammar = _structural(candidate, "grammar")
    dictionary = _dictionary(candidate)
    blockers: list[str] = []

    if candidate.get("hardRejectionReasons"):
        blockers.append("hard-rejection")
    if not morphology.get("sourceRangeContiguous"):
        blockers.append("source-range-not-contiguous")
    if morphology.get("interveningArgumentMaterial"):
        blockers.append("intervening-argument-material")
    if _kwja_conflict(candidate):
        blockers.append("kwja-boundary-conflict")
    if grammar.get("completeLearnableGrammarConflict"):
        blockers.append("complete-grammar-conflict")

    if family == "complete-grammar":
        gid = candidate.get("grammarId")
        if not gid or gid not in (grammar.get("completeLearnableGrammarIds") or []):
            blockers.append("grammar-not-exactly-corroborated")
        return not blockers, None, blockers

    if _same_range_grammar(candidate, by_id):
        blockers.append("stronger-same-range-grammar")

    if family == "compound-predicate":
        key = _unique_matched_key(candidate, complete=True)
        if not dictionary.get("completeCandidateMatched") or not key:
            blockers.append("complete-compound-identity-not-corroborated")
        # A generic sequential relation is retained as conflict evidence, but does
        # not veto a complete dictionary identity when morphology and KWJA agree.
        return not blockers, key, blockers

    if family == "inflected-lexical":
        key = _unique_matched_key(candidate)
        if not predicates.get("singlePredicateInterpretation"):
            blockers.append("not-single-predicate")
        if not key:
            blockers.append("unique-lexical-identity-not-corroborated")
        return not blockers, key, blockers

    if family == "term":
        matched = [
            item.get("text") for item in (candidate.get("lookupHypotheses") or [])
            if item.get("dictionaryStatus") == "matched"
            and item.get("text") in (candidate.get("possibleLookupKeys") or [])
        ]
        matched = list(dict.fromkeys(x for x in matched if x))
        key = matched[0] if len(matched) == 1 else None
        if not key:
            blockers.append("unique-complete-term-identity-not-corroborated")
        return not blockers, key, blockers

    return False, None, ["candidate-family-not-selectable-in-policy-v1"]


def _priority(candidate: dict[str, Any]) -> tuple[int, int, int]:
    family_order = {
        "complete-grammar": 40,
        "compound-predicate": 30,
        "inflected-lexical": 20,
        "term": 10,
    }
    length = int(candidate.get("end") or 0) - int(candidate.get("start") or 0)
    dictionary = _dictionary(candidate)
    sources = 0
    for hypothesis in candidate.get("lookupHypotheses") or []:
        if hypothesis.get("dictionaryStatus") == "matched":
            sources = max(sources, int((hypothesis.get("dictionaryEvidence") or {}).get("independentSourceCount") or 0))
    return family_order.get(candidate.get("candidateFamily"), 0), length, sources


def _aligns_to_complete_spans(candidate: dict[str, Any], spans: list[dict[str, Any]]) -> bool:
    start, end = candidate.get("start"), candidate.get("end")
    overlapping = [x for x in spans if x.get("start", -1) < end and start < x.get("end", -1)]
    return bool(overlapping) and min(x["start"] for x in overlapping) == start and max(x["end"] for x in overlapping) == end


def _reader_span(candidate: dict[str, Any], lookup: str | None) -> dict[str, Any]:
    family = candidate.get("candidateFamily")
    if family == "complete-grammar":
        return {
            "start": candidate["start"], "end": candidate["end"], "surface": candidate["surface"],
            "displayRole": "learnable-grammar", "lexicalType": None,
            "colorPolicy": "grammar", "unknownColorPolicy": None,
            "knownLookupKey": None, "frequencyLookupKey": None,
            "countsForComprehension": False, "showInNewWords": False, "eligibleForMining": True,
            "headword": None, "grammarId": candidate.get("grammarId"), "confidence": 1.0,
            "sourceSpanIds": [candidate["candidateId"]], "sourceLayer": "reader-candidate-selector",
            "projectionStatus": "selected-generated-candidate",
        }
    lexical_type = "compound" if family == "compound-predicate" else "term"
    display_role = "lexical-compound" if family == "compound-predicate" else "lexical"
    return {
        "start": candidate["start"], "end": candidate["end"], "surface": candidate["surface"],
        "displayRole": display_role, "lexicalType": lexical_type,
        "colorPolicy": "known-or-frequency", "unknownColorPolicy": "frequency",
        "knownLookupKey": lookup, "frequencyLookupKey": lookup,
        "countsForComprehension": True, "showInNewWords": True, "eligibleForMining": True,
        "headword": lookup, "grammarId": None, "confidence": 1.0,
        "sourceSpanIds": [candidate["candidateId"]], "sourceLayer": "reader-candidate-selector",
        "projectionStatus": "selected-generated-candidate",
    }


def select_reader_output(result: dict[str, Any], candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Select only candidates satisfying explicit evidence gates; otherwise abstain.

    The compatibility partition is always a valid fallback. Generated candidates
    replace only complete compatibility spans, and selected ranges never overlap.
    """
    baseline = project_reader_spans(result)
    output_candidates = deepcopy(candidates)
    by_id = {x.get("candidateId"): x for x in output_candidates if x.get("candidateId")}
    proposals = []
    decisions = []

    for candidate in output_candidates:
        if candidate.get("candidateSource") != "reader-evidence-generator":
            continue
        eligible, lookup, blockers = _eligible(candidate, by_id)
        if eligible and not _aligns_to_complete_spans(candidate, baseline):
            eligible = False
            blockers.append("does-not-align-to-complete-reader-spans")
        proposals.append((candidate, lookup, eligible, blockers))

    chosen: list[tuple[dict[str, Any], str | None]] = []
    for candidate, lookup, eligible, blockers in sorted(proposals, key=lambda x: _priority(x[0]), reverse=True):
        if not eligible:
            decisions.append({
                "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
                "decision": "abstain", "reasons": blockers or list(candidate.get("abstentionReasons") or []),
            })
            continue
        if any(candidate["start"] < other["end"] and other["start"] < candidate["end"] for other, _ in chosen):
            decisions.append({
                "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
                "decision": "abstain", "reasons": ["overlaps-higher-priority-selected-candidate"],
            })
            continue
        chosen.append((candidate, lookup))
        decisions.append({
            "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
            "decision": "select-generated-candidate", "preferredLookupKey": lookup,
            "reasons": ["all-conservative-evidence-gates-satisfied"],
        })

    chosen_ids = {candidate["candidateId"] for candidate, _ in chosen}
    chosen_ranges = [(candidate["start"], candidate["end"]) for candidate, _ in chosen]
    for candidate in output_candidates:
        cid = candidate.get("candidateId")
        if cid in chosen_ids:
            lookup = next(value for item, value in chosen if item["candidateId"] == cid)
            candidate["selected"] = True
            candidate["preferredLookupKey"] = lookup
            candidate["rankingStatus"] = "selected-conservative-v1"
            candidate["selectionReason"] = "all conservative evidence gates satisfied"
        elif candidate.get("candidateSource") == "reader-evidence-generator":
            candidate["selected"] = False
            candidate["preferredLookupKey"] = None
            candidate["rankingStatus"] = "abstained-conservative-v1"
            candidate["selectionReason"] = None
        elif candidate.get("selected") and any(candidate["start"] < b and a < candidate["end"] for a, b in chosen_ranges):
            candidate["selected"] = False
            candidate["rankingStatus"] = "displaced-by-selected-reader-candidate"
            candidate["selectionReason"] = None

    selected_spans = {candidate["start"]: _reader_span(candidate, lookup) for candidate, lookup in chosen}
    final = []
    index = 0
    while index < len(baseline):
        span = baseline[index]
        replacement = selected_spans.get(span["start"])
        if replacement:
            final.append(replacement)
            end = replacement["end"]
            while index < len(baseline) and baseline[index]["end"] <= end:
                index += 1
            continue
        final.append(span)
        index += 1

    validate_reader_spans(result.get("text", ""), final)
    selection = {
        "policyVersion": POLICY_VERSION,
        "mode": "conservative-evidence-gates-with-abstention",
        "compatibilityFallbackAvailable": True,
        "selectedGeneratedCandidateIds": sorted(chosen_ids),
        "selectedGeneratedCandidateCount": len(chosen_ids),
        "decisions": decisions,
    }
    return final, output_candidates, selection
