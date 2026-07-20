from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def base(text, spans, morphemes, predicates, relations, grammar=None):
    return {
        "text": text,
        "resolved_spans_alpha2": spans,
        "resolver_candidates_alpha2": [],
        "morphemes": morphemes,
        "predicates": predicates,
        "predicate_relations_alpha31": relations,
        "grammar_matches_alpha321": grammar or [],
        "numeral_expressions_alpha32": [],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def span(a, b, surface, role, headword=None, grammar_id=None, cid="x"):
    return {"start": a, "end": b, "surface": surface, "role": role, "headword": headword,
            "grammar_id": grammar_id, "confidence": .8, "selected_candidate_id": cid}


def main():
    # Valid contiguous VてV remains an unselected, component-key-only candidate.
    result = base(
        "出て行った。",
        [span(0,1,"出","term","出る",cid="c0"), span(1,2,"て","grammar",grammar_id="V_TE",cid="c1"),
         span(2,4,"行っ","term","行く",cid="c2"), span(4,5,"た","particle",cid="c3"), span(5,6,"。","punctuation",cid="c4")],
        [{"id":"m0","start":0,"end":1,"surface":"出","lemma":"出る","pos":"VERB"},
         {"id":"m1","start":1,"end":2,"surface":"て","lemma":"て","pos":"SCONJ"},
         {"id":"m2","start":2,"end":4,"surface":"行っ","lemma":"行く","pos":"VERB"},
         {"id":"m3","start":4,"end":5,"surface":"た","lemma":"た","pos":"AUX"},
         {"id":"m4","start":5,"end":6,"surface":"。","lemma":"。","pos":"PUNCT"}],
        [{"id":"p0","start":0,"end":1,"surface":"出","headword":"出る","head_morpheme_id":"m0","morpheme_ids":["m0"]},
         {"id":"p1","start":2,"end":4,"surface":"行っ","headword":"行く","head_morpheme_id":"m2","morpheme_ids":["m2"]}],
        [{"id":"r0","from_predicate_id":"p0","to_predicate_id":"p1","relation":"sequential-or-coordinate","confidence":.82,
          "marker_range":{"start":1,"end":2,"surface":"て"}}],
        [{"id":"g0","start":1,"end":2,"surface":"て","grammar_id":"V_TE","morpheme_ids":["m1"],"confidence":.85}],
    )
    before = deepcopy(project_reader_spans(result))
    candidates = generate_reader_candidates(result)
    compound = next(x for x in candidates if x["surface"] == "出て行った")
    assert compound["possibleLookupKeys"] == ["出る", "行く"]
    assert compound["preferredLookupKey"] is None
    assert compound["features"]["completeLookupKeyCorroborated"] is False
    assert compound["selected"] is False and compound["rankingEligible"] is True
    assert all(x.get("grammarId") != "V_TE" for x in candidates)
    assert project_reader_spans(result) == before

    # Intervening argument material blocks a lexical-compound proposal.
    separate = base(
        "開けて空気を入れた。",
        [],
        [{"id":"a0","start":0,"end":2,"surface":"開け","lemma":"開ける","pos":"VERB"},
         {"id":"a1","start":2,"end":3,"surface":"て","lemma":"て","pos":"SCONJ"},
         {"id":"a2","start":3,"end":5,"surface":"空気","lemma":"空気","pos":"NOUN"},
         {"id":"a3","start":5,"end":6,"surface":"を","lemma":"を","pos":"ADP"},
         {"id":"a4","start":6,"end":8,"surface":"入れ","lemma":"入れる","pos":"VERB"},
         {"id":"a5","start":8,"end":9,"surface":"た","lemma":"た","pos":"AUX"}],
        [{"id":"q0","start":0,"end":2,"surface":"開け","headword":"開ける","head_morpheme_id":"a0","morpheme_ids":["a0"]},
         {"id":"q1","start":6,"end":8,"surface":"入れ","headword":"入れる","head_morpheme_id":"a4","morpheme_ids":["a4"]}],
        [{"id":"rq","from_predicate_id":"q0","to_predicate_id":"q1","relation":"sequential-or-coordinate","confidence":.82,
          "marker_range":{"start":2,"end":3,"surface":"て"}}],
    )
    assert not any(x["candidateFamily"] == "compound-predicate" for x in generate_reader_candidates(separate))

    # Non-verbal predicate-like records and punctuation-crossing ranges are blocked.
    unsafe = base(
        "静かに、頷いた。",
        [],
        [{"id":"s0","start":0,"end":2,"surface":"静か","lemma":"静か","pos":"ADJ"},
         {"id":"s1","start":2,"end":3,"surface":"に","lemma":"だ","pos":"AUX"},
         {"id":"s2","start":3,"end":4,"surface":"、","lemma":"、","pos":"PUNCT"},
         {"id":"s3","start":4,"end":6,"surface":"頷い","lemma":"頷く","pos":"VERB"}],
        [{"id":"z0","start":0,"end":2,"surface":"静か","headword":"静か","head_morpheme_id":"s0","morpheme_ids":["s0"]},
         {"id":"z1","start":4,"end":6,"surface":"頷い","headword":"頷く","head_morpheme_id":"s3","morpheme_ids":["s3"]}],
        [{"id":"rz","from_predicate_id":"z0","to_predicate_id":"z1","relation":"direct-subordinate","confidence":.8}],
    )
    unsafe_candidates = generate_reader_candidates(unsafe)
    assert not any(x["candidateFamily"] == "compound-predicate" for x in unsafe_candidates)
    assert all(not x["hardRejectionReasons"] for x in unsafe_candidates)
    assert all("、" not in x["surface"] for x in unsafe_candidates)

    print("reader candidate safeguard tests passed")


if __name__ == "__main__":
    main()
