from app.analyzer.kwja_equivalence import compare_final_results, final_fingerprint, final_projection


def test_final_projection_excludes_non_authoritative_debug_fields():
    result = {"text": "x", "readerSpans": [], "internal": {"changing": 1}}
    projected = final_projection(result)
    assert "internal" not in projected
    assert projected["text"] == "x"


def test_final_comparison_detects_reader_change():
    first = {"text": "x", "readerSpans": [{"surface": "x"}]}
    second = {"text": "x", "readerSpans": [{"surface": "y"}]}
    summary = compare_final_results([first, second])
    assert summary["distinctFinalFingerprints"] == 2
    assert summary["differencesFromFirst"][0]["changedFinalFields"] == ["readerSpans"]


def test_final_comparison_accepts_identical_output():
    value = {"text": "x", "readerSpans": []}
    assert compare_final_results([value, value])["distinctFinalFingerprints"] == 1
