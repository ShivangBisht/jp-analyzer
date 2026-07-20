from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def fixture():
    text = "頷いて、二人は出て行った。"
    return {
        "text": text,
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "頷い", "role": "term", "headword": "頷く", "confidence": .9, "selected_candidate_id": "c0"},
            {"start": 2, "end": 3, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .8, "selected_candidate_id": "c1"},
            {"start": 3, "end": 4, "surface": "、", "role": "punctuation", "confidence": 1, "selected_candidate_id": "c2"},
            {"start": 4, "end": 6, "surface": "二人", "role": "term", "headword": "二人", "confidence": .9, "selected_candidate_id": "c3"},
            {"start": 6, "end": 7, "surface": "は", "role": "particle", "confidence": .8, "selected_candidate_id": "c4"},
            {"start": 7, "end": 8, "surface": "出", "role": "term", "headword": "出る", "confidence": .9, "selected_candidate_id": "c5"},
            {"start": 8, "end": 9, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .8, "selected_candidate_id": "c6"},
            {"start": 9, "end": 11, "surface": "行っ", "role": "term", "headword": "行く", "confidence": .9, "selected_candidate_id": "c7"},
            {"start": 11, "end": 12, "surface": "た", "role": "particle", "confidence": .8, "selected_candidate_id": "c8"},
            {"start": 12, "end": 13, "surface": "。", "role": "punctuation", "confidence": 1, "selected_candidate_id": "c9"},
        ],
        "resolver_candidates_alpha2": [],
        "morphemes": [
            {"id": "m0", "start": 0, "end": 2, "surface": "頷い", "lemma": "頷く", "pos": "VERB"},
            {"id": "m1", "start": 2, "end": 3, "surface": "て", "lemma": "て", "pos": "SCONJ"},
            {"id": "m2", "start": 3, "end": 4, "surface": "、", "lemma": "、", "pos": "PUNCT"},
            {"id": "m3", "start": 4, "end": 5, "surface": "二", "lemma": "二", "pos": "NUM"},
            {"id": "m4", "start": 5, "end": 6, "surface": "人", "lemma": "人", "pos": "NOUN"},
            {"id": "m5", "start": 6, "end": 7, "surface": "は", "lemma": "は", "pos": "ADP"},
            {"id": "m6", "start": 7, "end": 8, "surface": "出", "lemma": "出る", "pos": "VERB"},
            {"id": "m7", "start": 8, "end": 9, "surface": "て", "lemma": "て", "pos": "SCONJ"},
            {"id": "m8", "start": 9, "end": 11, "surface": "行っ", "lemma": "行く", "pos": "VERB"},
            {"id": "m9", "start": 11, "end": 12, "surface": "た", "lemma": "た", "pos": "AUX"},
            {"id": "m10", "start": 12, "end": 13, "surface": "。", "lemma": "。", "pos": "PUNCT"},
        ],
        "predicates": [
            {"id": "p0", "start": 0, "end": 2, "surface": "頷い", "headword": "頷く"},
            {"id": "p1", "start": 7, "end": 8, "surface": "出", "headword": "出る"},
            {"id": "p2", "start": 9, "end": 11, "surface": "行っ", "headword": "行く"},
        ],
        "predicate_relations_alpha31": [
            {"id": "r0", "from_predicate_id": "p1", "to_predicate_id": "p2", "relation": "sequential-or-subordinate", "confidence": .82, "marker_range": {"start": 8, "end": 9, "surface": "て"}},
        ],
        "numeral_expressions_alpha32": [
            {"id": "n0", "start": 4, "end": 6, "surface": "二人", "morpheme_ids": ["m3", "m4"], "confidence": .96},
        ],
        "grammar_matches_alpha321": [
            {"id": "g0", "start": 2, "end": 3, "surface": "て", "grammar_id": "V_TE", "morpheme_ids": ["m1"], "confidence": .85},
        ],
        "kwja_basic_phrases_alpha1": [
            {"id": "kb0", "start": 0, "end": 3, "surface": "頷いて"},
            {"id": "kb1", "start": 7, "end": 12, "surface": "出て行った"},
        ],
        "kwja_predicate_phrases_alpha1": [
            {"id": "kp0", "start": 0, "end": 3, "surface": "頷いて"},
            {"id": "kp1", "start": 7, "end": 12, "surface": "出て行った"},
        ],
    }


def main():
    result = fixture()
    before_resolved = deepcopy(result["resolved_spans_alpha2"])
    before_reader = project_reader_spans(result)
    generated = generate_reader_candidates(result)

    assert result["resolved_spans_alpha2"] == before_resolved
    assert project_reader_spans(result) == before_reader
    assert all(x["selected"] is False for x in generated)
    assert any(x["surface"] == "頷いて" and x["candidateFamily"] == "inflected-lexical" for x in generated)
    assert any(x["surface"] == "二人" and x["candidateFamily"] == "term" and x["proposedRole"] == "lexical" for x in generated)
    assert all(x["candidateFamily"] != "numeric-lexical" and x["proposedRole"] != "numeric-lexical" for x in generated)
    compound = next(x for x in generated if x["surface"] == "出て行った" and x["candidateFamily"] == "compound-predicate")
    assert compound["conflictingEvidence"]
    assert compound["features"]["conflictingEvidenceCount"] > 0
    assert not compound["hardRejectionReasons"]
    assert all("、" not in x["surface"] and "。" not in x["surface"] for x in generated)
    print("reader candidate generation tests passed")


if __name__ == "__main__":
    main()
