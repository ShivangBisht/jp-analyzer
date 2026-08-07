from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from app.analyzer.layers import dictionary_store

ORIGINAL_DB_PATH = dictionary_store.DB_PATH


def add_entry(connection, dictionary_id, title, dictionary_type, priority, term):
    connection.execute(
        """
        INSERT INTO lexicon_entries(
            dictionary_id, dictionary_title, dictionary_type,
            dictionary_priority, term, reading
        ) VALUES(?, ?, ?, ?, ?, '')
        """,
        (dictionary_id, title, dictionary_type, priority, term),
    )


def run():
    with tempfile.TemporaryDirectory(
        prefix="jp-analyzer-dictionary-registry-",
        ignore_cleanup_errors=True,
    ) as directory:
        temporary_db_path = Path(directory) / "registry.sqlite3"
        assert temporary_db_path.resolve() != ORIGINAL_DB_PATH.resolve()
        dictionary_store.DB_PATH = temporary_db_path
        try:
            with dictionary_store._db() as connection:
                add_entry(connection, "研究社_新和英大辞典_第5版-1783925776608", "研究社　新和英大辞典　第５版", "term", 3, "研究")
                add_entry(connection, "JMdict_2025_11_01-1783925759170", "JMdict [2025-11-01]", "term", 1, "辞書")
            first = dictionary_store.status()
            second = dictionary_store.status()
            assert first["installedDictionaryCount"] == 2
            assert first["registryEntryCount"] == 2
            assert first["registryConsistent"] is True
            assert second["installedDictionaryCount"] == 2
            items = {item["dictionaryId"]: item for item in second["installedDictionaries"]}
            japanese = items["研究社_新和英大辞典_第5版-1783925776608"]
            assert japanese["displayTitle"] == "研究社　新和英大辞典　第５版"
            assert japanese["stableIdentity"] == "研究社_新和英大辞典_第5版"
            jmdict = items["JMdict_2025_11_01-1783925759170"]
            assert jmdict["stableIdentity"] == "JMdict_2025_11_01"
            assert jmdict["revision"] == "2025-11-01"
            with sqlite3.connect(dictionary_store.DB_PATH) as connection:
                assert connection.execute("SELECT COUNT(*) FROM installed_dictionaries").fetchone()[0] == 2
                assert connection.execute("SELECT COUNT(*) FROM lexicon_entries").fetchone()[0] == 2
            assert dictionary_store.DB_PATH.resolve() != ORIGINAL_DB_PATH.resolve()
            cleared = dictionary_store.clear(allow_authoritative=True)
            assert cleared["installedDictionaryCount"] == 0
            assert cleared["registryEntryCount"] == 0
            assert cleared["registryConsistent"] is True
        finally:
            dictionary_store.DB_PATH = ORIGINAL_DB_PATH
    print("dictionary registry tests passed")


if __name__ == "__main__":
    run()
