from __future__ import annotations

from app.analyzer.compact_output import compact_analysis
from app.analyzer.reader_projection import validate_reader_spans
from app.analyzer.version import ANALYZER_VERSION


def _candidate(candidate_id, family, source_layer="test"):
    return {
        "candidate_id": candidate_id,
        "candidate_family": family,
        "source_layer": source_layer,
    }


def main():
    text = "二人はとばかりに頷いて。"
    result = {
        "version": "9.0.0-alpha2.2-evidence-gated-decision",
        "text": text,
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "二人", "role": "term", "headword": "二人", "confidence": .9, "selected_candidate_id": "num"},
            {"start": 2, "end": 3, "surface": "は", "role": "particle", "headword": None, "confidence": .8, "selected_candidate_id": "particle"},
            {"start": 3, "end": 8, "surface": "とばかりに", "role": "grammar", "grammar_id": "TO_BAKARI_NI", "confidence": .96, "selected_candidate_id": "grammar"},
            {"start": 8, "end": 10, "surface": "頷い", "role": "term", "headword": "頷く", "confidence": .9, "selected_candidate_id": "term"},
            {"start": 10, "end": 11, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .85, "selected_candidate_id": "te"},
            {"start": 11, "end": 12, "surface": "。", "role": "punctuation", "confidence": 1.0, "selected_candidate_id": "punct"},
        ],
        "resolver_candidates_alpha2": [
            _candidate("num", "numeral"),
            _candidate("particle", "particle"),
            _candidate("grammar", "grammar"),
            _candidate("term", "term"),
            _candidate("te", "grammar"),
            _candidate("punct", "punctuation"),
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {},
    }

    compact = compact_analysis(result, analyzer_version=ANALYZER_VERSION)
    spans = compact["readerSpans"]
    validate_reader_spans(text, spans)

    assert compact["schemaVersion"] == "1.2"
    assert compact["readerSpanSchemaVersion"] == "1.0"

    assert compact["readerCandidateSchemaVersion"] == "1.5"
    assert isinstance(compact["readerCandidates"], list)
    assert compact["resolvedSpans"] is result["resolved_spans_alpha2"]
    assert compact["coverage"]["readerSpansComplete"] is True

    numeric, function, grammar, lexical, te_function, punctuation = spans
    assert numeric["displayRole"] == "lexical"
    assert numeric["lexicalType"] == "term"
    assert numeric["colorPolicy"] == "known-or-frequency"
    assert numeric["unknownColorPolicy"] == "frequency"
    assert function["displayRole"] == "function"
    assert function["colorPolicy"] == "muted"
    assert grammar["displayRole"] == "learnable-grammar"
    assert grammar["grammarId"] == "TO_BAKARI_NI"
    assert lexical["displayRole"] == "lexical"
    assert lexical["knownLookupKey"] == "頷く"
    assert te_function["displayRole"] == "function"
    assert punctuation["displayRole"] == "punctuation"

    broken = [dict(item) for item in spans]
    broken[1]["start"] = 1
    try:
        validate_reader_spans(text, broken)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid reader span partition was accepted")

    print("readerSpans contract tests passed")


if __name__ == "__main__":
    main()
