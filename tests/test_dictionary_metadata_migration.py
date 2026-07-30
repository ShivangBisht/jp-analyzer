from __future__ import annotations
import tempfile
from pathlib import Path
from app.analyzer.layers import dictionary_items, dictionary_store
ORIGINAL = dictionary_store.DB_PATH
TEMP = Path(r"D:\Mining\_DELETE_AFTER_20260726\phase7\tests")

def run():
    TEMP.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dictionary-metadata-", dir=TEMP, ignore_cleanup_errors=True) as directory:
        dictionary_store.DB_PATH = Path(directory) / "metadata.sqlite3"
        try:
            operation = dictionary_items.start_operation({
                "mode":"install", "dictionaryId":"jmdict-test", "stableIdentity":"jmdict",
                "displayTitle":"JMdict [2025-11-01]", "dictionaryType":"term", "expectedEntries":1,
            })
            dictionary_items.add_batch(operation["operationId"], [{"term":"辞書"}])
            dictionary_items.finish_operation(operation["operationId"])
            updated = dictionary_items.update_dictionary_metadata("jmdict-test", {
                "revision":"JMdict.2025-11-01",
                "sourceUrl":"https://github.com/themoeway/yomitan-import",
                "updateManifestUrl":"https://github.com/yomidevs/jmdict-yomitan/releases/latest/download/JMdict_english_with_examples.json",
            })
            assert updated["revision"] == "JMdict.2025-11-01"
            assert updated["updateManifestUrl"].endswith(".json")
            assert dictionary_items.management_status()["registryEntryCount"] == 1
        finally:
            dictionary_store.DB_PATH = ORIGINAL
    print("dictionary metadata migration tests passed")
if __name__ == "__main__": run()
