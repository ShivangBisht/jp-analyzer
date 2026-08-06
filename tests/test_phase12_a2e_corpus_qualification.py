from app.analyzer.kwja_qualification import compare_to_baseline, result_summary


def test_compare_to_baseline_passes_identical_output():
    result = {"text": "x", "readerSpans": []}
    row = result_summary(0, "forward", 1, result, 1.0, 1)
    baseline = {0: {"finalAnalyzerFingerprint": row["finalAnalyzerFingerprint"], "fieldFingerprints": row["fieldFingerprints"]}}
    assert compare_to_baseline(baseline, [row])["qualified"] is True


def test_compare_to_baseline_reports_authoritative_change():
    first = result_summary(0, "fresh", 1, {"text": "x", "readerSpans": []}, 1.0, 1)
    second = result_summary(0, "forward", 1, {"text": "x", "readerSpans": [{"surface": "x"}]}, 1.0, 2)
    baseline = {0: {"finalAnalyzerFingerprint": first["finalAnalyzerFingerprint"], "fieldFingerprints": first["fieldFingerprints"]}}
    summary = compare_to_baseline(baseline, [second])
    assert summary["qualified"] is False
    assert summary["differences"][0]["changedFinalFields"] == ["readerSpans"]
