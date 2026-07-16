from __future__ import annotations

from app.analyzer import pipeline
from app.analyzer.compact_output import compact_analysis
from app.analyzer.version import ANALYZER_VERSION


def main():
    sentinel = {
        "version": "9.0.0-alpha2.2-evidence-gated-decision",
        "text": "検証。",
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "検証", "role": "term"},
            {"start": 2, "end": 3, "surface": "。", "role": "punctuation"},
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {"final_projection_changed": False},
    }

    original = pipeline.analyze_layers
    try:
        pipeline.analyze_layers = lambda *args, **kwargs: sentinel
        full = pipeline.analyze_full("検証。", object())
        assert full is sentinel
        debug = pipeline.analyze("検証。", object(), debug=True)
        assert debug is sentinel
        compact = pipeline.analyze("検証。", object(), debug=False)
    finally:
        pipeline.analyze_layers = original

    assert compact == compact_analysis(sentinel, analyzer_version=ANALYZER_VERSION)
    assert compact["text"] == "検証。"
    assert compact["coverage"]["complete"] is True
    assert compact["coverage"]["unresolvedSpanCount"] == 0
    assert compact["coverage"]["kwjaAlignmentComplete"] is True
    print("stable facade tests passed")


if __name__ == "__main__":
    main()
