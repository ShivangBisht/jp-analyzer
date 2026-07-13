from app.phase8.resolver_alpha34 import normalize_candidates, resolve_candidates


def base_analysis(text):
    return {
        "text": text,
        "morphemes": [],
        "orthographic_spans": [],
        "person_references": [],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [],
        "discourse_connectives_alpha321": [],
        "lexical_items_alpha32": [],
    }


def main():
    # Specific complete grammar must outrank internal dictionary-valid term.
    a = base_analysis("ならない")
    a["grammar_matches_alpha321"] = [{"id":"g1","start":0,"end":4,"surface":"ならない","grammar_id":"NAKEREBA_NARANAI","confidence":.98,"morpheme_ids":[]}]
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"なら","headword":"なる","lexical_type":"term","confidence":.9,"morpheme_ids":[]}]
    c = normalize_candidates(a, None)
    spans, decisions, conflicts = resolve_candidates(a["text"], c)
    assert spans[0]["surface"] == "ならない" and spans[0]["candidate_family"] == "grammar"

    # Complete person reference must outrank component term.
    a = base_analysis("綾子さん")
    a["person_references"] = [{"id":"p1","start":0,"end":4,"surface":"綾子さん","base_name":"綾子","confidence":.96,"morpheme_ids":["m0","m1"]}]
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"綾子","headword":"綾子","lexical_type":"term","confidence":.9,"morpheme_ids":["m0"]}]
    spans, _, _ = resolve_candidates(a["text"], normalize_candidates(a, None))
    assert spans[0]["surface"] == "綾子さん" and spans[0]["candidate_family"] == "proper-name"

    # Dictionary miss must not remove a morphology-backed term.
    a = base_analysis("未知語")
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":3,"surface":"未知語","headword":"未知語","lexical_type":"term","confidence":.84,"morpheme_ids":[]}]
    dictionary = {"evidence":[{"start":0,"end":3,"surface":"未知語","matched":False,"dictionary_type_counts":{},"source_names":[]}]}
    spans, decisions, _ = resolve_candidates(a["text"], normalize_candidates(a, dictionary))
    assert spans[0]["candidate_family"] == "term"
    assert "dictionary-corroboration" not in decisions[0]["decision_policies"]

    # Dictionary support strengthens but does not create a range.
    a = base_analysis("終え")
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"終え","headword":"終える","lexical_type":"term","confidence":.84,"morpheme_ids":[]}]
    dictionary = {"evidence":[{"start":0,"end":2,"surface":"終え","matched":True,"confidence":.98,"dictionary_type_counts":{"term":4},"source_names":["A","B"],"matched_headwords":["終える"]}]}
    candidates = normalize_candidates(a, dictionary)
    term = next(x for x in candidates if x["candidate_family"] == "term")
    assert term["dictionary_evidence"]["matched"] is True
    spans, decisions, _ = resolve_candidates(a["text"], candidates)
    assert "dictionary-corroboration" in decisions[0]["decision_policies"]

    print("Alpha 3.4 resolver tests passed")


if __name__ == "__main__":
    main()
