from __future__ import annotations

import tempfile
from pathlib import Path

from app.analyzer.layers import dictionary_items, dictionary_store

ORIGINAL = dictionary_store.DB_PATH
TEMP_PARENT = Path(r"D:\Mining\_DELETE_AFTER_20260726\phase7\tests")


def entry(term):
    return {"term": term, "reading": "", "tags": [], "rules": []}


def run():
    TEMP_PARENT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dictionary-item-", dir=TEMP_PARENT, ignore_cleanup_errors=True) as directory:
        dictionary_store.DB_PATH = Path(directory) / "items.sqlite3"
        try:
            install = dictionary_items.start_operation({
                "mode": "install", "dictionaryId": "alpha-1700000000000",
                "stableIdentity": "alpha", "displayTitle": "Alpha 辞書",
                "dictionaryType": "term", "priority": 1,
                "expectedEntries": 2, "revision": "1",
                "sourceUrl": "https://example.invalid/alpha.zip",
            })
            dictionary_items.add_batch(install["operationId"], [entry("一"), entry("二")])
            done = dictionary_items.finish_operation(install["operationId"])
            assert done["status"] == "complete"
            status = dictionary_items.management_status()
            assert status["installedDictionaryCount"] == 1
            assert status["registryEntryCount"] == 2

            update = dictionary_items.start_operation({
                "mode": "update", "dictionaryId": "alpha-1700000000000",
                "stableIdentity": "alpha", "displayTitle": "Alpha 辞書 v2",
                "dictionaryType": "term", "priority": 1,
                "expectedEntries": 1, "revision": "2",
            })
            dictionary_items.add_batch(update["operationId"], [entry("三")])
            dictionary_items.finish_operation(update["operationId"])
            status = dictionary_items.management_status()
            assert status["registryEntryCount"] == 1
            assert status["installedDictionaries"][0]["revision"] == "2"
            assert status["installedDictionaries"][0]["displayTitle"] == "Alpha 辞書 v2"

            failed = dictionary_items.start_operation({
                "mode": "update", "dictionaryId": "alpha-1700000000000",
                "stableIdentity": "alpha", "displayTitle": "Broken",
                "dictionaryType": "term", "expectedEntries": 2,
            })
            dictionary_items.add_batch(failed["operationId"], [entry("四")])
            try:
                dictionary_items.finish_operation(failed["operationId"])
            except ValueError:
                pass
            else:
                raise AssertionError("Expected count mismatch")
            status = dictionary_items.management_status()
            assert status["registryEntryCount"] == 1
            assert status["installedDictionaries"][0]["revision"] == "2"

            cancelled = dictionary_items.start_operation({
                "mode": "update", "dictionaryId": "alpha-1700000000000",
                "stableIdentity": "alpha", "displayTitle": "Cancelled",
                "dictionaryType": "term", "expectedEntries": 1,
            })
            dictionary_items.add_batch(cancelled["operationId"], [entry("五")])
            result = dictionary_items.cancel_operation(cancelled["operationId"])
            assert result["status"] == "cancelled"
            assert dictionary_items.management_status()["registryEntryCount"] == 1

            removed = dictionary_items.remove_dictionary("alpha-1700000000000")
            assert removed["removedEntryCount"] == 1
            assert dictionary_items.management_status()["installedDictionaryCount"] == 0
        finally:
            dictionary_store.DB_PATH = ORIGINAL
    print("dictionary item lifecycle tests passed")


if __name__ == "__main__":
    run()
