import pytest

from app.analyzer.teaching_guided_review import diagnose_guided_review

SENTENCE = "二人は優しい人達だった。"
START = SENTENCE.index("だった")
BOUNDARY = {"start": START, "end": START + 3, "surface": "だった"}


def snapshot(selected, candidates):
    return {
        "source": {"sentence": SENTENCE},
        "readerDecision": {
            "selectedSpans": selected,
            "candidates": candidates,
        },
    }


def span(start, end, surface, role):
    return {"start": start, "end": end, "surface": surface, "displayRole": role}


def test_missing_exact_candidate_is_diagnosed_automatically():
    selected = [span(START, START + 2, "だっ", "function"), span(START + 2, START + 3, "た", "function")]
    result = diagnose_guided_review(snapshot(selected, selected), boundary=BOUNDARY, asserted_role="function", intent="show-as-one-unit")
    assert result["judgment"] == "corrected"
    assert result["failureClassification"] == "candidate-generation-miss"
    assert result["candidatePresent"] is False
    assert result["tuningPerformed"] is False


def test_matching_current_span_is_accepted():
    current = span(START, START + 3, "だった", "function")
    result = diagnose_guided_review(snapshot([current], [current]), boundary=BOUNDARY, asserted_role="function", intent="accepted-current")
    assert result["judgment"] == "accepted-current"
    assert result["failureClassification"] == "accepted-current"
    assert result["boundaryMatches"] is True


def test_matching_candidate_not_selected_is_ranking_error():
    current = span(START, START + 3, "だった", "function")
    selected = [span(START, START + 2, "だっ", "function"), span(START + 2, START + 3, "た", "function")]
    result = diagnose_guided_review(snapshot(selected, [current]), boundary=BOUNDARY, asserted_role="function", intent="show-as-one-unit")
    assert result["failureClassification"] == "ranking-error"


def test_role_only_change_is_diagnosed():
    current = span(START, START + 3, "だった", "lexical")
    result = diagnose_guided_review(snapshot([current], [current]), boundary=BOUNDARY, asserted_role="function", intent="change-role")
    assert result["failureClassification"] == "role-error"


def test_uncertain_path_is_not_export_ready_claim():
    result = diagnose_guided_review(snapshot([], []), boundary=BOUNDARY, asserted_role=None, intent="unresolved")
    assert result["judgment"] == "rejected"
    assert result["failureClassification"] == "unclassified"
    assert result["recommendedConfidence"] == "needs-review"


def test_invalid_surface_is_rejected():
    bad = {**BOUNDARY, "surface": "different"}
    with pytest.raises(ValueError, match="surface"):
        diagnose_guided_review(snapshot([], []), boundary=bad, asserted_role="function", intent="show-as-one-unit")
