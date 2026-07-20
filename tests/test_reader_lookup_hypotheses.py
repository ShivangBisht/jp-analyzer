from __future__ import annotations

from app.analyzer.reader_candidate_generation import generate_reader_candidates


def fixture(surface, first_surface, first_lemma, second_surface, second_lemma, trailing_surface):
    first_start = 0
    first_end = len(first_surface)
    second_start = first_end
    second_end = second_start + len(second_surface)
    trailing_end = second_end + len(trailing_surface)
    return {
        "text": surface,
        "resolved_spans_alpha2": [],
        "resolver_candidates_alpha2": [],
        "morphemes": [
            {"id":"m0","start":first_start,"end":first_end,"surface":first_surface,"lemma":first_lemma,"pos":"VERB"},
            {"id":"m1","start":second_start,"end":second_end,"surface":second_surface,"lemma":second_lemma,"pos":"VERB"},
            {"id":"m2","start":second_end,"end":trailing_end,"surface":trailing_surface,"lemma":"た","pos":"AUX"},
        ],
        "predicates": [
            {"id":"p0","start":first_start,"end":first_end,"surface":first_surface,"headword":first_lemma,"head_morpheme_id":"m0","morpheme_ids":["m0"]},
            {"id":"p1","start":second_start,"end":second_end,"surface":second_surface,"headword":second_lemma,"head_morpheme_id":"m1","morpheme_ids":["m1"]},
        ],
        "predicate_relations_alpha31": [
            {"id":"r0","from_predicate_id":"p0","to_predicate_id":"p1","relation":"direct-compound","confidence":.82},
        ],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def complete_hypothesis(candidate):
    return next(
        item for item in candidate["lookupHypotheses"]
        if item["type"] == "complete-final-predicate-normalization"
    )


def main():
    cases = [
        ("出て行った", "出て", "出る", "行っ", "行く", "た", "出て行く"),
        ("読み終わった", "読み", "読む", "終わっ", "終わる", "た", "読み終わる"),
        ("走り出した", "走り", "走る", "出し", "出す", "た", "走り出す"),
        ("読んで寝た", "読んで", "読む", "寝", "寝る", "た", "読んで寝る"),
    ]
    forbidden = {"読みて終わる", "走りて出す", "読んて寝る"}
    for surface, first_surface, first_lemma, second_surface, second_lemma, trailing, expected in cases:
        generated = generate_reader_candidates(
            fixture(surface, first_surface, first_lemma, second_surface, second_lemma, trailing)
        )
        compound = next(x for x in generated if x["candidateFamily"] == "compound-predicate")
        hypothesis = complete_hypothesis(compound)
        assert hypothesis["text"] == expected
        assert hypothesis["status"] == "generated"
        assert hypothesis["dictionaryStatus"] == "not-evaluated"
        assert hypothesis["generationSource"] == "candidate-final-predicate"
        assert compound["preferredLookupKey"] is None
        assert compound["selected"] is False
        assert compound["features"]["completeLookupHypothesisGenerated"] is True
        assert compound["features"]["completeLookupHypothesisStatus"] == "not-evaluated"
        assert not forbidden.intersection(x["text"] for x in compound["lookupHypotheses"])

    print("reader lookup hypothesis tests passed")


if __name__ == "__main__":
    main()
