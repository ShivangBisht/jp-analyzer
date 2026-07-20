from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from .layers.dictionary import evaluate_candidate

DictionaryEvaluator = Callable[[dict[str, Any], str | None], dict[str, Any]]
LEXICAL_ROLES = {"lexical", "lexical-compound", "numeric-lexical", "name"}
COMPLETE_HYPOTHESIS_TYPES = {"complete-final-predicate-normalization"}
COMPONENT_HYPOTHESIS_TYPES = {"component-or-lexical-headword"}


def _parser_pos(result: dict[str, Any], candidate: dict[str, Any]) -> str | None:
    start, end = candidate.get("start"), candidate.get("end")
    covered = [
        item for item in (result.get("morphemes") or [])
        if isinstance(start, int) and isinstance(end, int)
        and start <= item.get("start", -1) and item.get("end", -1) <= end
    ]
    lexical = [
        item for item in covered
        if item.get("pos") in {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}
    ]
    return lexical[-1].get("pos") if lexical else None


def _status_from_result(result: dict[str, Any]) -> str:
    if not result.get("dictionary_ready"):
        return "dictionary-not-ready"
    return "matched" if result.get("matched") else "evaluated-no-match"


def _compact_result(result: dict[str, Any]) -> dict[str, Any]:
    """Retain evidence metadata but never expose dictionary definitions."""
    return {
        "matched": bool(result.get("matched")),
        "dictionaryReady": bool(result.get("dictionary_ready")),
        "matchType": result.get("match_type"),
        "selectedLookupForm": result.get("selected_lookup_form"),
        "selectedLookupFormType": result.get("selected_lookup_form_type"),
        "entryCount": int(result.get("entry_count") or 0),
        "independentSourceCount": int(result.get("independent_source_count") or 0),
        "dictionaryTypeCounts": dict(result.get("dictionary_type_counts") or {}),
        "matchedHeadwords": list(result.get("matched_headwords") or []),
        "sourceNames": list(result.get("source_names") or []),
        "posCompatibility": dict(result.get("pos_compatibility") or {}),
        "confidence": result.get("confidence"),
        "lookupAttempts": list(result.get("lookup_attempts") or []),
    }


def evaluate_reader_candidate_dictionary(
    result: dict[str, Any],
    candidate: dict[str, Any],
    evaluator: DictionaryEvaluator = evaluate_candidate,
) -> dict[str, Any]:
    """Evaluate every new lookup hypothesis as its own dictionary question.

    A component match never proves a complete candidate. A miss never hard-rejects
    a candidate. This function only attaches candidate-specific evidence.
    """
    output = deepcopy(candidate)
    hypotheses = list(output.get("lookupHypotheses") or [])
    parser_pos = _parser_pos(result, output)
    evaluated: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for hypothesis in hypotheses:
        item = deepcopy(hypothesis)
        text = str(item.get("text") or "").strip()
        if not text:
            item["dictionaryStatus"] = "not-generated"
            evaluated.append(item)
            continue
        request = {
            "id": f"{output.get('candidateId', 'reader-candidate')}::{item.get('type')}::{text}",
            "start": output.get("start"),
            "end": output.get("end"),
            # Surface intentionally equals the exact hypothesis. The dictionary
            # evaluator therefore cannot report a match from the inflected source
            # surface while attributing it to another hypothesis.
            "surface": text,
            "lookup_forms": [{"text": text, "type": item.get("type") or "reader-hypothesis"}],
            "lemma": None,
            "normalized": None,
            "candidate_type": output.get("candidateFamily"),
        }
        try:
            evidence = evaluator(request, parser_pos)
            item["dictionaryStatus"] = _status_from_result(evidence)
            item["dictionaryEvidence"] = _compact_result(evidence)
        except Exception as exc:  # Analysis must abstain rather than fail closed.
            item["dictionaryStatus"] = "evaluation-error"
            item["dictionaryErrorCode"] = type(exc).__name__
            errors.append({
                "hypothesisText": text,
                "hypothesisType": item.get("type"),
                "errorCode": type(exc).__name__,
            })
        evaluated.append(item)

    complete = [x for x in evaluated if x.get("type") in COMPLETE_HYPOTHESIS_TYPES]
    components = [x for x in evaluated if x.get("type") in COMPONENT_HYPOTHESIS_TYPES]
    complete_matches = [x["text"] for x in complete if x.get("dictionaryStatus") == "matched"]
    component_matches = [x["text"] for x in components if x.get("dictionaryStatus") == "matched"]
    statuses = {x.get("dictionaryStatus") for x in evaluated}

    if not evaluated:
        status = "not-generated"
    elif "evaluation-error" in statuses:
        status = "partial-or-error"
    elif statuses == {"dictionary-not-ready"}:
        status = "dictionary-not-ready"
    else:
        status = "evaluated"

    output["lookupHypotheses"] = evaluated
    output["dictionaryEvaluation"] = {
        "status": status,
        "evaluatedHypothesisCount": sum(
            x.get("dictionaryStatus") in {"matched", "evaluated-no-match"}
            for x in evaluated
        ),
        "matchedHypothesisCount": sum(x.get("dictionaryStatus") == "matched" for x in evaluated),
        "completeCandidateMatched": bool(complete_matches),
        "componentOnlyMatched": bool(component_matches) and not bool(complete_matches),
        "matchedCompleteLookupKeys": complete_matches,
        "matchedComponentKeys": component_matches,
        "dictionaryMissIsNotRejection": True,
        "errors": errors,
    }
    output.setdefault("features", {})["completeLookupKeyCorroborated"] = bool(complete_matches)
    output["features"]["candidateSpecificDictionaryEvaluated"] = bool(evaluated)
    # D.2 records evidence only. Selection and preferred identity remain unset.
    output["preferredLookupKey"] = None
    output["selected"] = False
    output["selectionReason"] = None
    return output


def evaluate_generated_reader_candidates(
    result: dict[str, Any],
    candidates: list[dict[str, Any]],
    evaluator: DictionaryEvaluator = evaluate_candidate,
) -> list[dict[str, Any]]:
    out = []
    for candidate in candidates:
        if candidate.get("candidateSource") != "reader-evidence-generator":
            out.append(candidate)
            continue
        if candidate.get("proposedRole") not in LEXICAL_ROLES:
            item = deepcopy(candidate)
            item["dictionaryEvaluation"] = {
                "status": "not-applicable",
                "evaluatedHypothesisCount": 0,
                "matchedHypothesisCount": 0,
                "completeCandidateMatched": False,
                "componentOnlyMatched": False,
                "matchedCompleteLookupKeys": [],
                "matchedComponentKeys": [],
                "dictionaryMissIsNotRejection": True,
                "errors": [],
            }
            out.append(item)
            continue
        out.append(evaluate_reader_candidate_dictionary(result, candidate, evaluator))
    return out
