from __future__ import annotations

import tempfile
from pathlib import Path

from app.analyzer.layers import dictionary as evidence_module
from app.analyzer.layers import dictionary_store
from app.analyzer.layers.dictionary import (
    evaluate_analysis_candidates,
    evaluate_candidate,
)


def main():
    original_store_path = dictionary_store.DB_PATH
    original_evidence_path = evidence_module.DB_PATH
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            test_path = Path(tmp) / "lexicon.sqlite3"
            dictionary_store.DB_PATH = test_path
            # dictionary.py imports DB_PATH at module import, so update its test seam too.
            evidence_module.DB_PATH = test_path

            session = dictionary_store.start_sync(5, 4)
            entries = [
                {"term": "終える", "reading": "おえる", "dictionaryId": "d1", "dictionaryTitle": "Term A", "dictionaryType": "term", "dictionaryPriority": 10, "tags": ["v1", "vt"], "rules": ["v1"]},
                {"term": "終える", "reading": "おえる", "dictionaryId": "d2", "dictionaryTitle": "Term B", "dictionaryType": "term", "dictionaryPriority": 20, "tags": ["verb"]},
                {"term": "終える", "reading": "おえる", "dictionaryId": "d3", "dictionaryTitle": "Expression C", "dictionaryType": "expression", "dictionaryPriority": 30, "tags": ["exp"]},
                {"term": "らしい", "reading": "らしい", "dictionaryId": "g1", "dictionaryTitle": "Grammar", "dictionaryType": "grammar", "dictionaryPriority": 5, "grammarType": "evidential"},
                {"term": "美羽", "reading": "みう", "dictionaryId": "n1", "dictionaryTitle": "Names", "dictionaryType": "name", "dictionaryPriority": 5, "nameType": "given"},
            ]
            dictionary_store.add_batch(session["syncId"], entries)
            dictionary_store.finish_sync(session["syncId"])

            candidate = {
                "id": "adc0",
                "start": 3,
                "end": 5,
                "surface": "終え",
                "lookup_forms": ["終え", "終える"],
                "candidate_type": "lexical-proposal",
            }
            result = evaluate_candidate(candidate, "VERB")
            assert result["matched"] is True
            assert result["selected_lookup_form"] == "終える"
            assert result["entry_count"] == 3
            assert result["independent_source_count"] == 3
            assert result["dictionary_type_counts"] == {"term": 2, "expression": 1}
            assert result["pos_compatibility"]["status"] == "compatible"

            missing = evaluate_candidate(
                {
                    "id": "adc1",
                    "start": 0,
                    "end": 3,
                    "surface": "架空語",
                    "lookup_forms": ["架空語"],
                },
                "NOUN",
            )
            assert missing["matched"] is False
            assert "not a candidate rejection" in missing["meaning"]

            analysis = {
                "morphemes": [
                    {
                        "id": "m0",
                        "start": 3,
                        "end": 5,
                        "surface": "終え",
                        "lemma": "終える",
                        "pos": "VERB",
                    }
                ],
                "dictionary_candidates_alpha31": [candidate],
                "color_spans_alpha321": [
                    {
                        "start": 3,
                        "end": 5,
                        "surface": "終え",
                        "role": "term",
                        "headword": "終える",
                    }
                ],
            }
            before = repr(analysis)
            aggregate = evaluate_analysis_candidates(analysis)
            assert aggregate["matched_candidate_count"] == 1
            assert repr(analysis) == before, "Evidence evaluation mutated analysis"
            assert aggregate["contract"]["reader_projection_unchanged"] is True
    finally:
        dictionary_store.DB_PATH = original_store_path
        evidence_module.DB_PATH = original_evidence_path

    print("Dictionary evidence test passed")


if __name__ == "__main__":
    main()
