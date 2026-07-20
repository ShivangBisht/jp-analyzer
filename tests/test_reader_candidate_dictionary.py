from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_dictionary import evaluate_reader_candidate_dictionary


def candidate():
    return {
        "candidateId": "reader-generated-test",
        "candidateSource": "reader-evidence-generator",
        "candidateFamily": "compound-predicate",
        "start": 0,
        "end": 5,
        "surface": "出て行った",
        "proposedRole": "lexical-compound",
        "possibleLookupKeys": ["出る", "行く"],
        "lookupHypotheses": [
            {"text":"出て行く","type":"complete-final-predicate-normalization","status":"generated","dictionaryStatus":"not-evaluated"},
            {"text":"出る","type":"component-or-lexical-headword","status":"generated","dictionaryStatus":"not-evaluated"},
            {"text":"行く","type":"component-or-lexical-headword","status":"generated","dictionaryStatus":"not-evaluated"},
        ],
        "preferredLookupKey": None,
        "features": {},
        "hardRejectionReasons": [],
        "selected": False,
        "selectionReason": None,
    }


def fake(request, parser_pos):
    form = request["surface"]
    matched = form in {"出て行く", "出る", "行く"}
    return {
        "matched": matched,
        "dictionary_ready": True,
        "match_type": "surface-exact" if matched else "none",
        "selected_lookup_form": form if matched else None,
        "selected_lookup_form_type": request["lookup_forms"][0]["type"] if matched else None,
        "entry_count": 1 if matched else 0,
        "independent_source_count": 1 if matched else 0,
        "dictionary_type_counts": {"term": 1} if matched else {},
        "matched_headwords": [form] if matched else [],
        "source_names": ["test"] if matched else [],
        "pos_compatibility": {"status":"compatible","parserPos":parser_pos},
        "confidence": .83 if matched else None,
        "lookup_attempts": [{"form":form,"form_type":"test","match_count":1 if matched else 0}],
        "entries": [{"definition":"must not leak"}],
    }


def main():
    analysis = {"morphemes":[{"start":0,"end":1,"pos":"VERB"},{"start":2,"end":4,"pos":"VERB"}]}
    original = candidate()
    evaluated = evaluate_reader_candidate_dictionary(analysis, original, fake)
    assert original["lookupHypotheses"][0]["dictionaryStatus"] == "not-evaluated"
    assert evaluated["dictionaryEvaluation"]["status"] == "evaluated"
    assert evaluated["dictionaryEvaluation"]["completeCandidateMatched"] is True
    assert evaluated["dictionaryEvaluation"]["componentOnlyMatched"] is False
    assert evaluated["dictionaryEvaluation"]["matchedCompleteLookupKeys"] == ["出て行く"]
    assert evaluated["dictionaryEvaluation"]["matchedComponentKeys"] == ["出る", "行く"]
    assert all(x["dictionaryStatus"] == "matched" for x in evaluated["lookupHypotheses"])
    assert "entries" not in evaluated["lookupHypotheses"][0]["dictionaryEvidence"]
    assert evaluated["preferredLookupKey"] is None and evaluated["selected"] is False

    component_only = candidate()
    def components(request, parser_pos):
        result = fake(request, parser_pos)
        if request["surface"] == "出て行く":
            result.update({"matched":False,"match_type":"none","selected_lookup_form":None,
                           "selected_lookup_form_type":None,"entry_count":0,
                           "independent_source_count":0,"dictionary_type_counts":{},
                           "matched_headwords":[],"source_names":[],"confidence":None})
        return result
    evaluated = evaluate_reader_candidate_dictionary(analysis, component_only, components)
    assert evaluated["dictionaryEvaluation"]["completeCandidateMatched"] is False
    assert evaluated["dictionaryEvaluation"]["componentOnlyMatched"] is True
    assert evaluated["lookupHypotheses"][0]["dictionaryStatus"] == "evaluated-no-match"
    assert evaluated["hardRejectionReasons"] == []

    def unavailable(request, parser_pos):
        return {"matched":False,"dictionary_ready":False,"match_type":"dictionary-not-ready",
                "entry_count":0,"independent_source_count":0,"dictionary_type_counts":{},
                "matched_headwords":[],"source_names":[],"pos_compatibility":{"status":"unknown"},
                "confidence":None,"lookup_attempts":[]}
    evaluated = evaluate_reader_candidate_dictionary(analysis, candidate(), unavailable)
    assert evaluated["dictionaryEvaluation"]["status"] == "dictionary-not-ready"
    assert all(x["dictionaryStatus"] == "dictionary-not-ready" for x in evaluated["lookupHypotheses"])

    print("reader candidate dictionary tests passed")


if __name__ == "__main__":
    main()
