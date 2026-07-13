from __future__ import annotations

import tempfile
from pathlib import Path

from app.phase8 import dictionary_store
from app.phase8.dictionary_evidence import evaluate_candidate, evaluate_analysis_candidates


def main():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        dictionary_store.DB_PATH = Path(tmp) / "lexicon.sqlite3"
        # dictionary_evidence imports the Path object at module import; update it too.
        import app.phase8.dictionary_evidence as evidence_module
        evidence_module.DB_PATH = dictionary_store.DB_PATH

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

        candidate = {"id": "adc0", "start": 3, "end": 5, "surface": "終え", "lookup_forms": ["終え", "終える"], "candidate_type": "alpha3-lexical-proposal"}
        result = evaluate_candidate(candidate, "VERB")
        assert result["matched"] is True
        assert result["selected_lookup_form"] == "終える"
        assert result["entry_count"] == 3
        assert result["independent_source_count"] == 3
        assert result["dictionary_type_counts"] == {"term": 2, "expression": 1}
        assert result["pos_compatibility"]["status"] == "compatible"

        missing = evaluate_candidate({"id": "adc1", "start": 0, "end": 2, "surface": "架空語", "lookup_forms": ["架空語"]}, "NOUN")
        assert missing["matched"] is False
        assert "not a candidate rejection" in missing["meaning"]

        analysis = {
            "morphemes": [{"id": "m0", "start": 3, "end": 5, "surface": "終え", "lemma": "終える", "pos": "VERB"}],
            "dictionary_candidates_alpha31": [candidate],
            "color_spans_alpha321": [{"start": 3, "end": 5, "surface": "終え", "role": "term", "headword": "終える"}],
        }
        before = repr(analysis)
        aggregate = evaluate_analysis_candidates(analysis)
        assert aggregate["matched_candidate_count"] == 1
        assert repr(analysis) == before, "Evidence evaluation mutated the analysis"
        assert aggregate["contract"]["reader_projection_unchanged"] is True
        print("Dictionary evidence test passed")


if __name__ == "__main__":
    main()
