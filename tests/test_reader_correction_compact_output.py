from __future__ import annotations

import tempfile
from pathlib import Path

import app.analyzer.reader_corrections as rc
from app.analyzer.compact_output import compact_analysis


def result_fixture():
    return {
        "text": "少年が走ってきた。",
        "version": "test-engine",
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "少年", "role": "term", "headword": "少年", "selected_candidate_id": "r0", "source_layer": "lexical"},
            {"start": 2, "end": 3, "surface": "が", "role": "particle", "selected_candidate_id": "r1", "source_layer": "morphology-fallback"},
            {"start": 3, "end": 5, "surface": "走っ", "role": "term", "headword": "走る", "selected_candidate_id": "r2", "source_layer": "lexical"},
            {"start": 5, "end": 8, "surface": "てきた", "role": "grammar", "grammar_id": "TE_KURU", "selected_candidate_id": "r3", "source_layer": "grammar"},
            {"start": 8, "end": 9, "surface": "。", "role": "punctuation", "selected_candidate_id": "r4", "source_layer": "orthography"},
        ],
        "resolver_candidates_alpha2": [
            {"candidate_id": "r0", "candidate_family": "term", "source_layer": "lexical"},
            {"candidate_id": "r1", "candidate_family": "particle", "source_layer": "morphology-fallback"},
            {"candidate_id": "r2", "candidate_family": "term", "source_layer": "lexical"},
            {"candidate_id": "r3", "candidate_family": "grammar", "source_layer": "grammar"},
            {"candidate_id": "r4", "candidate_family": "punctuation", "source_layer": "orthography"},
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {},
    }


def main():
    with tempfile.TemporaryDirectory() as directory:
        rc.DB_PATH = Path(directory) / "corrections.sqlite3"
        normal = compact_analysis(result_fixture(), analyzer_version="test")
        baseline = normal["readerSpans"]
        assert [item["surface"] for item in baseline] == ["少年", "が", "走っ", "てきた", "。"]

        rc.save(
            {
                "sentence": "少年が走ってきた。",
                "start": 3,
                "end": 8,
                "surface": "走ってきた",
                "action": "show-as-one-unit",
                "scope": "occurrence",
            },
            baseline,
            "test",
            "1.1",
        )
        corrected = compact_analysis(result_fixture(), analyzer_version="test")
        assert [item["surface"] for item in corrected["readerSpans"]] == ["少年", "が", "走ってきた", "。"]
        assert corrected["readerSpans"][2]["grammarId"] == "TE_KURU"
        assert corrected["readerSpans"][2]["hostLookupKey"] == "走る"
        assert corrected["readerSelection"]["appliedCorrectionCount"] == 1
        assert corrected["coverage"]["readerSpansComplete"] is True
        assert corrected["resolvedSpans"] == result_fixture()["resolved_spans_alpha2"]

    print("reader correction compact-output tests passed")


if __name__ == "__main__":
    main()
