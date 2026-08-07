from __future__ import annotations

from copy import deepcopy

from app.analyzer.kwja_production_parity import (
    compare_production_modes,
    validate_reader_contract,
)


def result(text="文"):
    return {
        "text": text,
        "readerSpans": [{"start": 0, "end": len(text), "surface": text}],
        "readerCandidates": [],
        "readerSelection": {},
        "resolvedSpans": [{"start": 0, "end": len(text), "surface": text}],
        "coverage": {"readerSpansComplete": True},
        "diagnostics": [],
    }


def test_reader_contract_accepts_exact_partition():
    assert validate_reader_contract(result()) == []


def test_reader_contract_rejects_surface_and_range_drift():
    value = result()
    value["readerSpans"] = [{"start": 1, "end": 2, "surface": "違"}]
    errors = validate_reader_contract(value)
    assert "READER_SPANS_DO_NOT_RECONSTRUCT_SOURCE" in errors
    assert "READER_SPAN_0_RANGE_INVALID" in errors


def test_production_parity_accepts_identical_authoritative_output():
    calls = []

    def analyze(text, mode):
        calls.append((text, mode))
        return result(text)

    summary = compare_production_modes(["一", "二"], analyze_fn=analyze)
    assert summary["qualified"] is True
    assert summary["differenceCount"] == 0
    assert calls == [("一", "fresh"), ("一", "persistent"), ("二", "fresh"), ("二", "persistent")]
    assert summary["safety"]["sentenceTextIncluded"] is False


def test_production_parity_reports_changed_final_field():
    def analyze(text, mode):
        value = result(text)
        if mode == "persistent":
            value = deepcopy(value)
            value["readerSelection"] = {"changed": True}
        return value

    summary = compare_production_modes(["文"], analyze_fn=analyze)
    assert summary["qualified"] is False
    assert summary["differenceCount"] == 1
    assert summary["differences"][0]["changedFinalFields"] == ["readerSelection"]


def test_non_authoritative_fields_do_not_fail_parity():
    def analyze(text, mode):
        value = result(text)
        value["runtimeDebug"] = {"mode": mode}
        return value

    assert compare_production_modes(["文"], analyze_fn=analyze)["qualified"] is True
