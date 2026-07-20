from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_evidence import attach_reader_candidate_structural_evidence


def candidate(surface="出て行った", complete=True):
    return {
        "candidateId":"rc-compound", "candidateSource":"reader-evidence-generator",
        "candidateFamily":"compound-predicate", "start":0, "end":len(surface),
        "surface":surface, "proposedRole":"lexical-compound", "possibleLookupKeys":["出る","行く"],
        "preferredLookupKey":None, "selected":False, "selectionReason":None,
        "dictionaryEvaluation":{
            "status":"evaluated", "completeCandidateMatched":complete,
            "componentOnlyMatched":not complete,
            "matchedCompleteLookupKeys":["出て行く"] if complete else [],
            "matchedComponentKeys":["出る","行く"],
        },
        "features":{}, "hardRejectionReasons":[],
    }


def analysis(surface="出て行った", relation="sequential-or-coordinate"):
    return {
        "text":surface,
        "morphemes":[
            {"id":"m0","start":0,"end":1,"surface":"出","pos":"VERB"},
            {"id":"m1","start":1,"end":2,"surface":"て","pos":"SCONJ"},
            {"id":"m2","start":2,"end":4,"surface":"行っ","pos":"VERB"},
            {"id":"m3","start":4,"end":5,"surface":"た","pos":"AUX"},
        ],
        "predicates":[
            {"id":"p0","start":0,"end":1,"surface":"出","headword":"出る"},
            {"id":"p1","start":2,"end":4,"surface":"行っ","headword":"行く"},
        ],
        "predicate_relations_alpha31":[
            {"id":"pr0","from_predicate_id":"p0","to_predicate_id":"p1","relation":relation}
        ],
        "grammar_matches_alpha321":[
            {"id":"g0","start":1,"end":2,"surface":"て","grammar_id":"V_TE"}
        ],
        "kwja_basic_phrases_alpha1":[
            {"id":"kb0","start":0,"end":5,"surface":surface}
        ],
        "kwja_predicate_phrases_alpha1":[
            {"id":"kp0","start":0,"end":5,"surface":surface}
        ],
    }


def main():
    original = candidate()
    evaluated = attach_reader_candidate_structural_evidence(analysis(), [original])
    item = evaluated[0]
    assert original.get("candidateStructuralEvidence") is None
    assert item["structuralEvidenceVersion"] == "1.0"
    assert item["candidateStructuralEvidence"]["morphology"]["sourceRangeContiguous"] is True
    assert item["candidateStructuralEvidence"]["morphology"]["interveningArgumentMaterial"] is False
    assert item["candidateStructuralEvidence"]["kwja"]["exactBasicPhrase"] is True
    assert item["candidateStructuralEvidence"]["kwja"]["exactPredicatePhrase"] is True
    assert item["candidateStructuralEvidence"]["predicates"]["predicateCount"] == 2
    assert item["candidateStructuralEvidence"]["predicates"]["independentOrSequentialActionConflict"] is True
    assert item["candidateStructuralEvidence"]["grammar"]["structuralGrammarIds"] == ["V_TE"]
    assert "multiple-independent-or-sequential-predicates" in item["abstentionReasons"]
    assert "complete-lookup-key-not-corroborated" not in item["abstentionReasons"]
    assert item["rankingStatus"] == "evidence-evaluated-unselected"
    assert item["selected"] is False and item["preferredLookupKey"] is None

    no_complete = attach_reader_candidate_structural_evidence(analysis(), [candidate(complete=False)])[0]
    assert "complete-lookup-key-not-corroborated" in no_complete["abstentionReasons"]
    assert no_complete["hardRejectionReasons"] == []

    with_argument = analysis("開けて空気を入れた")
    with_argument["morphemes"] = [
        {"id":"m0","start":0,"end":2,"surface":"開け","pos":"VERB"},
        {"id":"m1","start":2,"end":3,"surface":"て","pos":"SCONJ"},
        {"id":"m2","start":3,"end":5,"surface":"空気","pos":"NOUN"},
        {"id":"m3","start":5,"end":6,"surface":"を","pos":"ADP"},
        {"id":"m4","start":6,"end":8,"surface":"入れ","pos":"VERB"},
        {"id":"m5","start":8,"end":9,"surface":"た","pos":"AUX"},
    ]
    wide = candidate("開けて空気を入れた", complete=False)
    wide["end"] = 9
    wide["candidateId"] = "rc-wide"
    evidence = attach_reader_candidate_structural_evidence(with_argument, [wide])[0]
    assert evidence["candidateStructuralEvidence"]["morphology"]["interveningArgumentMaterial"] is True
    assert "intervening-argument-material" in evidence["abstentionReasons"]

    print("reader candidate structural evidence tests passed")


if __name__ == "__main__":
    main()
