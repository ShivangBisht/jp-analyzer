from __future__ import annotations

from copy import deepcopy
from typing import Any

SCHEMA = "TeachingGuidedReviewDiagnosis.v1"
SUPPORTED_INTENTS = {"accepted-current", "show-as-one-unit", "change-role", "unresolved"}


def _range(item: dict[str, Any]) -> tuple[int | None, int | None]:
    return item.get("start"), item.get("end")


def _role(item: dict[str, Any] | None) -> str | None:
    if not item:
        return None
    return item.get("displayRole") or item.get("proposedRole") or item.get("role")


def diagnose_guided_review(
    snapshot: dict[str, Any],
    *,
    boundary: dict[str, Any],
    asserted_role: str | None,
    intent: str,
) -> dict[str, Any]:
    """Derive technical diagnosis from a frozen snapshot and human target.

    The reviewer supplies the intended range and role. This function never
    mutates the snapshot, creates a Teaching record, or applies a correction.
    """
    if intent not in SUPPORTED_INTENTS:
        raise ValueError("unsupported guided Teaching intent")

    source = snapshot.get("source") or {}
    sentence = source.get("sentence")
    if not isinstance(sentence, str):
        raise ValueError("snapshot source sentence is missing")

    start = boundary.get("start")
    end = boundary.get("end")
    surface = boundary.get("surface")
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or start >= end or end > len(sentence):
        raise ValueError("review boundary is outside the sentence")
    if sentence[start:end] != surface:
        raise ValueError("review surface does not match the sentence")

    reader = snapshot.get("readerDecision") or {}
    selected = list(reader.get("selectedSpans") or [])
    candidates = list(reader.get("candidates") or [])
    exact_selected = next((deepcopy(x) for x in selected if _range(x) == (start, end)), None)
    exact_candidates = [deepcopy(x) for x in candidates if _range(x) == (start, end)]
    overlapping_selected = [deepcopy(x) for x in selected if int(x.get("end") or 0) > start and int(x.get("start") or 0) < end]
    overlapping_candidates = [deepcopy(x) for x in candidates if int(x.get("end") or 0) > start and int(x.get("start") or 0) < end]

    observed_role = _role(exact_selected)
    exact_candidate_role_match = any(_role(x) == asserted_role for x in exact_candidates)
    boundary_matches = exact_selected is not None
    classification_matches = bool(exact_selected and asserted_role and observed_role == asserted_role)

    if intent == "unresolved":
        judgment = "rejected"
        failure = "unclassified"
        confidence = "needs-review"
        reason = "The reviewer marked the result as uncertain. It will remain excluded until reviewed."
    elif intent == "accepted-current":
        if not exact_selected:
            raise ValueError("accepted-current requires one exact selected Reader span")
        judgment = "accepted-current"
        failure = "accepted-current"
        confidence = "preference"
        reason = "The selected Reader span already exists and is being preserved."
    elif not exact_candidates:
        judgment = "corrected"
        failure = "candidate-generation-miss"
        confidence = "preference"
        reason = "No analyzer candidate covers the complete intended range."
    elif not exact_selected and exact_candidate_role_match:
        judgment = "corrected"
        failure = "ranking-error"
        confidence = "preference"
        reason = "A matching candidate exists, but the Reader selected another partition."
    elif exact_selected and asserted_role and observed_role != asserted_role:
        judgment = "corrected"
        failure = "role-error"
        confidence = "preference"
        reason = "The boundary matches, but the Reader role differs from the approved role."
    elif not exact_selected:
        judgment = "corrected"
        failure = "boundary-error"
        confidence = "preference"
        reason = "Candidates overlap the intended text, but the selected Reader boundary differs."
    else:
        judgment = "accepted-current"
        failure = "accepted-current"
        confidence = "preference"
        reason = "The current boundary and role already match the intended result."

    return {
        "schema": SCHEMA,
        "judgment": judgment,
        "failureClassification": failure,
        "recommendedConfidence": confidence,
        "reason": reason,
        "candidatePresent": bool(exact_candidates),
        "candidateCount": len(exact_candidates),
        "boundaryMatches": boundary_matches,
        "classificationMatches": classification_matches,
        "observedReaderSpan": exact_selected,
        "overlappingReaderSpans": overlapping_selected,
        "overlappingCandidateCount": len(overlapping_candidates),
        "assertedBoundary": deepcopy(boundary),
        "assertedRole": asserted_role,
        "technicalDetailsAvailable": True,
        "tuningPerformed": False,
        "activationEnabled": False,
    }
