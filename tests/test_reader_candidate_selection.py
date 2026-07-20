from __future__ import annotations

from app.analyzer.reader_candidate_selection import select_reader_output


def baseline(text="頷いて読んで寝た"):
    return {
        "text": text,
        "resolver_candidates_alpha2": [],
        "resolved_spans_alpha2": [
            {"start":0,"end":2,"surface":"頷い","role":"term","headword":"頷く","confidence":.9,"selected_candidate_id":"e0"},
            {"start":2,"end":3,"surface":"て","role":"particle","confidence":.8,"selected_candidate_id":"e1"},
            {"start":3,"end":5,"surface":"読ん","role":"term","headword":"読む","confidence":.9,"selected_candidate_id":"e2"},
            {"start":5,"end":6,"surface":"で","role":"particle","confidence":.8,"selected_candidate_id":"e3"},
            {"start":6,"end":7,"surface":"寝","role":"term","headword":"寝る","confidence":.9,"selected_candidate_id":"e4"},
            {"start":7,"end":8,"surface":"た","role":"particle","confidence":.8,"selected_candidate_id":"e5"},
        ],
    }


def structural(single=True, boundary=False, grammar=False, sequential=False):
    return {
        "morphology":{"sourceRangeContiguous":True,"interveningArgumentMaterial":False},
        "kwja":{"crossesBasicPhraseBoundary":boundary,"crossesPredicatePhraseBoundary":False},
        "predicates":{"singlePredicateInterpretation":single,"independentOrSequentialActionConflict":sequential},
        "grammar":{"completeLearnableGrammarConflict":grammar,"completeLearnableGrammarIds":[]},
        "competition":{"sameRangeCandidateIds":[]},
    }


def candidate(cid, start, end, surface, family, keys, dictionary, evidence):
    return {
        "candidateId":cid,"candidateSource":"reader-evidence-generator","start":start,"end":end,
        "surface":surface,"candidateFamily":family,"proposedRole":"lexical","possibleLookupKeys":keys,
        "preferredLookupKey":None,"selected":False,"hardRejectionReasons":[],
        "candidateStructuralEvidence":evidence,"dictionaryEvaluation":dictionary,"lookupHypotheses":[],
    }


def main():
    inflected = candidate("g0",0,3,"頷いて","inflected-lexical",["頷く"],{
        "status":"evaluated","matchedComponentKeys":["頷く"],"completeCandidateMatched":False
    }, structural())
    broad = candidate("g1",3,8,"読んで寝た","compound-predicate",["読む","寝る"],{
        "status":"evaluated","matchedCompleteLookupKeys":[],"matchedComponentKeys":["読む","寝る"],
        "completeCandidateMatched":False,"componentOnlyMatched":True
    }, structural(single=False,boundary=True,sequential=True))
    spans, candidates, selection = select_reader_output(baseline(), [inflected,broad])
    assert [x["surface"] for x in spans] == ["頷いて","読ん","で","寝","た"]
    assert spans[0]["knownLookupKey"] == "頷く"
    assert next(x for x in candidates if x["candidateId"]=="g0")["selected"] is True
    assert next(x for x in candidates if x["candidateId"]=="g1")["selected"] is False
    assert selection["selectedGeneratedCandidateCount"] == 1

    compound = candidate("g2",0,5,"出て行った","compound-predicate",["出る","行く"],{
        "status":"evaluated","matchedCompleteLookupKeys":["出て行く"],"matchedComponentKeys":["出る","行く"],
        "completeCandidateMatched":True,"componentOnlyMatched":False
    }, structural(single=False,sequential=True))
    source = baseline("出て行った")
    source["resolved_spans_alpha2"] = [
        {"start":0,"end":1,"surface":"出","role":"term","headword":"出る","confidence":.9,"selected_candidate_id":"a"},
        {"start":1,"end":2,"surface":"て","role":"particle","confidence":.8,"selected_candidate_id":"b"},
        {"start":2,"end":4,"surface":"行っ","role":"term","headword":"行く","confidence":.9,"selected_candidate_id":"c"},
        {"start":4,"end":5,"surface":"た","role":"particle","confidence":.8,"selected_candidate_id":"d"},
    ]
    spans, candidates, selection = select_reader_output(source,[compound])
    assert len(spans)==1 and spans[0]["surface"]=="出て行った"
    assert spans[0]["displayRole"]=="lexical-compound"
    assert spans[0]["knownLookupKey"]=="出て行く"
    assert selection["selectedGeneratedCandidateCount"]==1
    print("reader conservative selection tests passed")


if __name__ == "__main__":
    main()
