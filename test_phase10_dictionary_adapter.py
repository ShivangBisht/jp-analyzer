from app.analyzer.adapters.dictionary_adapter import DictionaryAdapter


def main():
    adapter = DictionaryAdapter()
    status = adapter.status()
    assert {"ready", "entryCount", "database"} <= set(status)
    result = adapter.evaluate_candidate({
        "id": "test", "start": 0, "end": 2, "surface": "検証"
    })
    assert result["candidate_id"] == "test"
    assert "matched" in result
    print("Phase 10.4 dictionary adapter tests passed")


if __name__ == "__main__":
    main()
