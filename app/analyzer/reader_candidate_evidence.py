from __future__ import annotations

from copy import deepcopy
from typing import Any

LEXICAL_POS = {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}
FUNCTION_POS = {"ADP", "PART", "AUX", "SCONJ"}
NOMINAL_ARGUMENT_POS = {"NOUN", "PROPN", "PRON", "NUM", "DET"}
GENERIC_STRUCTURAL_GRAMMAR = {"V_TE", "TE_IRU_CHAIN"}
TIGHT_RELATIONS = {"compound", "direct-compound", "auxiliary", "lexical-compound"}
SEQUENTIAL_RELATION_MARKERS = {"sequential", "coordinate", "subordinate", "conj", "advcl"}


def _range(item: dict[str, Any]) -> tuple[int, int] | None:
    start, end = item.get("start"), item.get("end")
    if isinstance(start, int) and isinstance(end, int) and start < end:
        return start, end
    return None


def _overlaps(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ar, br = _range(a), _range(b)
    return bool(ar and br and ar[0] < br[1] and br[0] < ar[1])


def _contained(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if start <= x.get("start", -1) and x.get("end", -1) <= end]


def _containing(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if x.get("start", -1) <= start and end <= x.get("end", -1)]


def _crosses_boundaries(items: list[dict[str, Any]], start: int, end: int) -> bool:
    # Crossing means the candidate cuts through a phrase boundary. Merely containing
    # multiple complete phrases is recorded separately and is not a hard rejection.
    for item in items:
        a, b = item.get("start"), item.get("end")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        if start < a < end < b or a < start < b < end:
            return True
    return False


def _relation_text(relation: dict[str, Any]) -> str:
    return " ".join(
        str(relation.get(key) or "").lower()
        for key in ("relation", "semantic_relation", "dependency_type", "relation_evidence")
    )


def _candidate_predicates(result: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    start, end = candidate["start"], candidate["end"]
    return _contained(list(result.get("predicates") or []), start, end)


def _predicate_relations(result: dict[str, Any], predicate_ids: set[str]) -> list[dict[str, Any]]:
    relations = result.get("predicate_relations_alpha31") or result.get("predicate_relations") or []
    return [
        relation for relation in relations
        if relation.get("from_predicate_id") in predicate_ids
        and relation.get("to_predicate_id") in predicate_ids
    ]


def _grammar_interaction(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    grammar = (
        result.get("grammar_matches_alpha321")
        or result.get("grammar_matches_alpha32")
        or result.get("grammar_matches_alpha31")
        or []
    )
    contained = _contained(grammar, start, end)
    containing = _containing(grammar, start, end)
    partial = [x for x in grammar if _overlaps(candidate, x) and x not in contained and x not in containing]
    complete = [x for x in grammar if x.get("start") == start and x.get("end") == end]
    contained_ids = sorted({x.get("grammar_id") for x in contained if x.get("grammar_id")})
    complete_ids = sorted({x.get("grammar_id") for x in complete if x.get("grammar_id")})
    learnable_complete = [gid for gid in complete_ids if gid not in GENERIC_STRUCTURAL_GRAMMAR]
    structural = [gid for gid in contained_ids if gid in GENERIC_STRUCTURAL_GRAMMAR]
    return {
        "containedGrammarIds": contained_ids,
        "completeGrammarIds": complete_ids,
        "completeLearnableGrammarIds": learnable_complete,
        "structuralGrammarIds": structural,
        "partialOverlapGrammarIds": sorted({x.get("grammar_id") for x in partial if x.get("grammar_id")}),
        "completeLearnableGrammarConflict": bool(learnable_complete) and candidate.get("proposedRole") != "learnable-grammar",
    }


def _kwja_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    basic = list(result.get("kwja_basic_phrases_alpha1") or [])
    predicates = list(result.get("kwja_predicate_phrases_alpha1") or [])
    exact_basic = [x for x in basic if x.get("start") == start and x.get("end") == end]
    containing_basic = _containing(basic, start, end)
    contained_basic = _contained(basic, start, end)
    exact_predicate = [x for x in predicates if x.get("start") == start and x.get("end") == end]
    containing_predicate = _containing(predicates, start, end)
    contained_predicate = _contained(predicates, start, end)
    return {
        "exactBasicPhrase": bool(exact_basic),
        "containingBasicPhrase": bool(containing_basic),
        "containedBasicPhraseCount": len(contained_basic),
        "crossesBasicPhraseBoundary": _crosses_boundaries(basic, start, end),
        "exactPredicatePhrase": bool(exact_predicate),
        "containingPredicatePhrase": bool(containing_predicate),
        "containedPredicatePhraseCount": len(contained_predicate),
        "crossesPredicatePhraseBoundary": _crosses_boundaries(predicates, start, end),
        "basicPhraseIds": sorted({x.get("id") for x in exact_basic + containing_basic + contained_basic if x.get("id")}),
        "predicatePhraseIds": sorted({x.get("id") for x in exact_predicate + containing_predicate + contained_predicate if x.get("id")}),
    }


def _morphology_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    morphemes = sorted(_contained(list(result.get("morphemes") or []), start, end), key=lambda x: (x["start"], x["end"]))
    contiguous = bool(morphemes) and morphemes[0].get("start") == start and morphemes[-1].get("end") == end
    cursor = start
    for morpheme in morphemes:
        if morpheme.get("start") != cursor:
            contiguous = False
            break
        cursor = morpheme.get("end")
    contiguous = contiguous and cursor == end
    lexical = [x for x in morphemes if x.get("pos") in LEXICAL_POS]
    function = [x for x in morphemes if x.get("pos") in FUNCTION_POS]
    verbal = [x for x in morphemes if x.get("pos") == "VERB"]
    auxiliaries = [x for x in morphemes if x.get("pos") == "AUX"]
    internal_particles = [x for x in morphemes if x.get("pos") in {"ADP", "PART", "SCONJ"}]
    argument_material = [x for x in morphemes[1:-1] if x.get("pos") in NOMINAL_ARGUMENT_POS]
    return {
        "sourceRangeContiguous": contiguous,
        "allComponentsCovered": contiguous,
        "morphemeCount": len(morphemes),
        "lexicalComponentCount": len(lexical),
        "functionComponentCount": len(function),
        "verbalMorphemeCount": len(verbal),
        "auxiliaryCount": len(auxiliaries),
        "internalParticleCount": len(internal_particles),
        "interveningArgumentMaterial": bool(argument_material),
        "interveningArgumentMorphemeIds": [x.get("id") for x in argument_material if x.get("id")],
        "morphemeIds": [x.get("id") for x in morphemes if x.get("id")],
    }


def _predicate_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    predicates = _candidate_predicates(result, candidate)
    predicate_ids = {x.get("id") for x in predicates if x.get("id")}
    relations = _predicate_relations(result, predicate_ids)
    relation_texts = [_relation_text(x) for x in relations]
    tight = [x for x, value in zip(relations, relation_texts) if any(marker in value for marker in TIGHT_RELATIONS)]
    sequential = [x for x, value in zip(relations, relation_texts) if any(marker in value for marker in SEQUENTIAL_RELATION_MARKERS)]
    return {
        "predicateCount": len(predicates),
        "predicateIds": sorted(predicate_ids),
        "predicateHeadwords": [x.get("headword") for x in predicates if x.get("headword")],
        "relationIds": [x.get("id") for x in relations if x.get("id")],
        "relationLabels": [x.get("semantic_relation") or x.get("relation") for x in relations],
        "singlePredicateInterpretation": len(predicates) == 1,
        "multiplePredicateInterpretation": len(predicates) > 1,
        "tightCompoundRelationSupport": bool(tight),
        "independentOrSequentialActionConflict": bool(sequential) and len(predicates) > 1,
    }


def _competition(candidates: list[dict[str, Any]], candidate: dict[str, Any]) -> dict[str, Any]:
    same = []
    contained = []
    containing = []
    overlapping = []
    different_roles = []
    start, end = candidate["start"], candidate["end"]
    for other in candidates:
        if other.get("candidateId") == candidate.get("candidateId"):
            continue
        os, oe = other.get("start"), other.get("end")
        if not isinstance(os, int) or not isinstance(oe, int):
            continue
        if os == start and oe == end:
            same.append(other)
            if other.get("proposedRole") != candidate.get("proposedRole"):
                different_roles.append(other)
        elif start <= os and oe <= end:
            contained.append(other)
        elif os <= start and end <= oe:
            containing.append(other)
        elif start < oe and os < end:
            overlapping.append(other)
    ids = lambda items: [x.get("candidateId") for x in items if x.get("candidateId")]
    return {
        "sameRangeCandidateIds": ids(same),
        "containedCandidateIds": ids(contained),
        "containingCandidateIds": ids(containing),
        "overlappingCandidateIds": ids(overlapping),
        "differentRoleCandidateIds": ids(different_roles),
        "hasSameRangeDifferentRole": bool(different_roles),
    }


def _abstention_reasons(candidate: dict[str, Any], structural: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    morphology = structural["morphology"]
    predicates = structural["predicates"]
    grammar = structural["grammar"]
    kwja = structural["kwja"]
    competition = structural["competition"]
    dictionary = candidate.get("dictionaryEvaluation") or {}

    if not morphology["sourceRangeContiguous"]:
        reasons.append("source-range-not-contiguous")
    if morphology["interveningArgumentMaterial"]:
        reasons.append("intervening-argument-material")
    if predicates["independentOrSequentialActionConflict"]:
        reasons.append("multiple-independent-or-sequential-predicates")
    if grammar["completeLearnableGrammarConflict"]:
        reasons.append("overlaps-complete-learnable-grammar")
    if kwja["crossesBasicPhraseBoundary"] or kwja["crossesPredicatePhraseBoundary"]:
        reasons.append("crosses-kwja-phrase-boundary")
    if competition["hasSameRangeDifferentRole"]:
        reasons.append("same-range-different-role-competition")
    if candidate.get("candidateFamily") == "compound-predicate" and not dictionary.get("completeCandidateMatched"):
        reasons.append("complete-lookup-key-not-corroborated")
    if dictionary.get("status") in {"dictionary-not-ready", "partial-or-error"}:
        reasons.append("dictionary-evidence-unavailable")
    return list(dict.fromkeys(reasons))


def attach_reader_candidate_structural_evidence(
    result: dict[str, Any], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Attach candidate-specific evidence without ranking or selecting.

    Existing analyzer records are treated as immutable facts. Every conclusion in
    this module is recalculated for the exact new reader-candidate range.
    """
    output: list[dict[str, Any]] = []
    for candidate in candidates:
        item = deepcopy(candidate)
        if item.get("candidateSource") != "reader-evidence-generator":
            output.append(item)
            continue
        structural = {
            "kwja": _kwja_evidence(result, item),
            "morphology": _morphology_evidence(result, item),
            "predicates": _predicate_evidence(result, item),
            "grammar": _grammar_interaction(result, item),
            "competition": {},
        }
        item["candidateStructuralEvidence"] = structural
        output.append(item)

    # Competition requires the complete candidate set, so calculate it after all
    # immutable per-range evidence has been attached.
    for item in output:
        if item.get("candidateSource") != "reader-evidence-generator":
            continue
        structural = item["candidateStructuralEvidence"]
        structural["competition"] = _competition(output, item)
        item["abstentionReasons"] = _abstention_reasons(item, structural)
        item["rankingStatus"] = "evidence-evaluated-unselected"
        item["selected"] = False
        item["selectionReason"] = None
        item["preferredLookupKey"] = None
        item["structuralEvidenceVersion"] = "1.0"
    return output
