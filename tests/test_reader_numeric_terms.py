from __future__ import annotations

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def analysis(text: str, start: int, end: int, morphemes: list[dict], value: str, counter: str | None):
    return {
        "text": text,
        "resolved_spans_alpha2": [],
        "resolver_candidates_alpha2": [],
        "morphemes": morphemes,
        "predicates": [],
        "predicate_relations_alpha31": [],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [{
            "id": "num0", "start": start, "end": end, "surface": text[start:end],
            "value_surface": value, "counter_surface": counter,
            "morpheme_ids": [m["id"] for m in morphemes], "confidence": .96,
        }],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def main():
    cases = [
        ("二人", [{"id":"m0","start":0,"end":1,"surface":"二","lemma":"二","pos":"NUM"}, {"id":"m1","start":1,"end":2,"surface":"人","lemma":"人","pos":"NOUN"}], "二", "人"),
        ("十歳", [{"id":"m0","start":0,"end":1,"surface":"十","lemma":"十","pos":"NUM"}, {"id":"m1","start":1,"end":2,"surface":"歳","lemma":"歳","pos":"NOUN"}], "十", "歳"),
        ("二十歳", [{"id":"m0","start":0,"end":2,"surface":"二十","lemma":"二十","pos":"NUM"}, {"id":"m1","start":2,"end":3,"surface":"歳","lemma":"歳","pos":"NOUN"}], "二十", "歳"),
    ]
    for text, morphemes, value, counter in cases:
        candidates = generate_reader_candidates(analysis(text, 0, len(text), morphemes, value, counter))
        candidate = next(x for x in candidates if x["surface"] == text)
        assert candidate["candidateFamily"] == "term"
        assert candidate["proposedRole"] == "lexical"
        assert candidate["features"]["containsNumeral"] is True
        assert candidate["features"]["numericExpressionSupported"] is True
        assert candidate["features"]["numericEvidenceOnly"] is True
        assert candidate["numericEvidence"]["counterSurface"] == counter
        assert candidate["possibleLookupKeys"] == [text]
        assert candidate["preferredLookupKey"] is None
        assert candidate["selected"] is False
        assert candidate["rankingStatus"].startswith("unscored")
        assert all(x["candidateFamily"] != "numeric-lexical" for x in candidates)
        assert all(x["proposedRole"] != "numeric-lexical" for x in candidates)
        compatibility_result = {
        "text": "十歳",
        "resolver_candidates_alpha2": [
            {
                "candidate_id": "a34c0",
                "candidate_family": "numeral",
                "source_annotation_id": "num0",
                "source_layer": "numeral",
            }
        ],
        "resolved_spans_alpha2": [
            {
                "start": 0,
                "end": 2,
                "surface": "十歳",
                "role": "term",
                "headword": "十歳",
                "grammar_id": None,
                "confidence": 0.96,
                "selected_candidate_id": "a34c0",
                "source_layer": "numeral",
            }
        ],
    }

    projected = project_reader_spans(
        compatibility_result
    )

    assert projected == [
        {
            "start": 0,
            "end": 2,
            "surface": "十歳",
            "displayRole": "lexical",
            "lexicalType": "term",
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
            "knownLookupKey": "十歳",
            "frequencyLookupKey": "十歳",
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
            "headword": "十歳",
            "grammarId": None,
            "confidence": 0.96,
            "sourceSpanIds": [
                "a34c0",
                "num0",
            ],
            "sourceLayer": "numeral",
            "projectionStatus": "compatibility",
        }
    ]
    print("reader numeric term tests passed")


if __name__ == "__main__":
    main()
