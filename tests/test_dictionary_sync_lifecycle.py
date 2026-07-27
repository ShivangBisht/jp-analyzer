from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from app.analyzer.layers import dictionary_store


ORIGINAL_DB_PATH = dictionary_store.DB_PATH


def entry(
    term: str,
    dictionary_id: str,
    dictionary_type: str = "term",
) -> dict:
    return {
        "term": term,
        "reading": "",
        "dictionaryId": dictionary_id,
        "dictionaryTitle": dictionary_id,
        "dictionaryType": dictionary_type,
        "dictionaryPriority": 1,
        "tags": [],
        "rules": [],
        "score": 0,
        "sequence": None,
        "nameType": "",
        "grammarType": "",
        "expressionType": "",
    }


def live_terms():
    with sqlite3.connect(
        dictionary_store.DB_PATH
    ) as connection:
        return [
            row[0]
            for row in connection.execute(
                """
                SELECT term
                FROM lexicon_entries
                ORDER BY term
                """
            )
        ]


def test_successful_sync_and_persistence() -> None:
    started = dictionary_store.start_sync(
        expected_entries=2,
        dictionary_count=1,
        snapshot_identity="snapshot-a",
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("一", "dictionary-a"),
            entry("二", "dictionary-a"),
        ],
    )

    finished = dictionary_store.finish_sync(
        started["syncId"]
    )

    assert finished["status"] == "complete"
    assert finished["entryCount"] == 2
    assert finished["dictionaryCount"] == 1
    assert live_terms() == ["一", "二"]

    current = dictionary_store.status()

    assert current["ready"] is True
    assert current["entryCount"] == 2
    assert current["snapshotIdentity"] == "snapshot-a"
    assert current["activeSession"] is None
    assert current["recoveryRequired"] is False

    with sqlite3.connect(
        dictionary_store.DB_PATH
    ) as connection:
        persisted = connection.execute(
            """
            SELECT value
            FROM lexicon_meta
            WHERE key = 'snapshot_identity'
            """
        ).fetchone()

    assert persisted is not None
    assert persisted[0] == "snapshot-a"


def test_expected_received_mismatch_preserves_live() -> None:
    started = dictionary_store.start_sync(
        expected_entries=2,
        dictionary_count=1,
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("三", "dictionary-b"),
        ],
    )

    try:
        dictionary_store.finish_sync(
            started["syncId"]
        )
    except ValueError as error:
        assert "Expected entries" in str(error)
    else:
        raise AssertionError(
            "Expected finish_sync to reject the count mismatch"
        )

    assert live_terms() == ["一", "二"]

    current = dictionary_store.status()
    problem = current["lastProblemSession"]

    assert problem is not None
    assert problem["status"] == "failed"
    assert (
        problem["errorCode"]
        == "EXPECTED_RECEIVED_MISMATCH"
    )

    recovery = dictionary_store.recover_interrupted_syncs()

    assert recovery["recoveredCount"] == 0
    assert recovery["cleanedTerminalCount"] == 1
    assert recovery["cleanedTerminalSyncIds"] == [
        started["syncId"]
    ]

    current = dictionary_store.status()
    assert current["stagedEntryCount"] == 0
    assert current["lastProblemSession"]["status"] == "failed"


def test_dictionary_count_mismatch_preserves_live() -> None:
    started = dictionary_store.start_sync(
        expected_entries=2,
        dictionary_count=2,
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("四", "dictionary-c"),
            entry("五", "dictionary-c"),
        ],
    )

    try:
        dictionary_store.finish_sync(
            started["syncId"]
        )
    except ValueError as error:
        assert "dictionary count" in str(error).lower()
    else:
        raise AssertionError(
            "Expected dictionary-count mismatch"
        )

    assert live_terms() == ["一", "二"]

    current = dictionary_store.status()
    problem = current["lastProblemSession"]

    assert problem is not None
    assert problem["status"] == "failed"
    assert problem["errorCode"] == "DICTIONARY_COUNT_MISMATCH"

    recovery = dictionary_store.recover_interrupted_syncs()

    assert recovery["recoveredCount"] == 0
    assert recovery["cleanedTerminalCount"] == 1
    assert recovery["cleanedTerminalSyncIds"] == [
        started["syncId"]
    ]

    current = dictionary_store.status()
    assert current["stagedEntryCount"] == 0
    assert current["lastProblemSession"]["status"] == "failed"


def test_cancel_removes_staging_and_preserves_live() -> None:
    started = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("六", "dictionary-d"),
        ],
    )

    cancelled = dictionary_store.cancel_sync(
        started["syncId"]
    )

    assert cancelled["status"] == "cancelled"
    assert cancelled["stagedEntries"] == 0
    assert live_terms() == ["一", "二"]

    current = dictionary_store.status()

    assert current["activeSession"] is None
    assert current["stagedEntryCount"] == 0


def test_retry_after_cancellation() -> None:
    started = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
        snapshot_identity="snapshot-b",
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("七", "dictionary-e"),
        ],
    )

    finished = dictionary_store.finish_sync(
        started["syncId"]
    )

    assert finished["status"] == "complete"
    assert finished["snapshotIdentity"] == "snapshot-b"
    assert live_terms() == ["七"]


def test_recovery_clears_interrupted_staging() -> None:
    started = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
    )

    dictionary_store.add_batch(
        started["syncId"],
        [
            entry("八", "dictionary-f"),
        ],
    )

    recovered = (
        dictionary_store.recover_interrupted_syncs()
    )

    assert recovered["recoveredCount"] == 1
    assert (
        started["syncId"]
        in recovered["recoveredSyncIds"]
    )
    assert live_terms() == ["七"]

    current = dictionary_store.status()

    assert current["activeSession"] is None
    assert current["stagedEntryCount"] == 0
    assert current["recoveryRequired"] is False

    problem = current["lastProblemSession"]

    assert problem is not None
    assert problem["status"] == "interrupted"


def test_new_sync_interrupts_old_session() -> None:
    first = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
    )

    dictionary_store.add_batch(
        first["syncId"],
        [
            entry("九", "dictionary-g"),
        ],
    )

    second = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
    )

    current = dictionary_store.status()

    assert current["activeSession"] is not None
    assert (
        current["activeSession"]["syncId"]
        == second["syncId"]
    )
    assert current["stagedEntryCount"] == 0

    dictionary_store.cancel_sync(
        second["syncId"]
    )

    assert live_terms() == ["七"]


def test_received_count_exceeded_preserves_live() -> None:
    started = dictionary_store.start_sync(
        expected_entries=1,
        dictionary_count=1,
    )

    try:
        dictionary_store.add_batch(
            started["syncId"],
            [
                entry("十", "dictionary-h"),
                entry("十一", "dictionary-h"),
            ],
        )
    except ValueError as error:
        assert "exceed expectedEntries" in str(error)
    else:
        raise AssertionError(
            "Expected oversized batch to be rejected"
        )

    assert live_terms() == ["七"]

    current = dictionary_store.status()
    problem = current["lastProblemSession"]

    assert problem is not None
    assert (
        problem["errorCode"]
        == "RECEIVED_COUNT_EXCEEDED"
    )

    recovery = dictionary_store.recover_interrupted_syncs()

    assert recovery["recoveredCount"] == 0
    assert recovery["cleanedTerminalCount"] == 0

    current = dictionary_store.status()
    assert current["stagedEntryCount"] == 0
    assert current["lastProblemSession"]["status"] == "failed"


def test_additive_migration_from_legacy_schema() -> None:
    migration_database = (
        dictionary_store.DB_PATH.parent
        / "legacy-schema.sqlite3"
    )

    with sqlite3.connect(migration_database) as connection:
        connection.executescript(
            """
            CREATE TABLE sync_sessions(
                sync_id TEXT PRIMARY KEY,
                expected_entries INTEGER DEFAULT 0,
                received_entries INTEGER DEFAULT 0,
                dictionary_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'receiving'
            );

            CREATE TABLE staging_entries(
                sync_id TEXT NOT NULL,
                dictionary_id TEXT NOT NULL,
                dictionary_title TEXT NOT NULL,
                dictionary_type TEXT NOT NULL,
                dictionary_priority INTEGER NOT NULL DEFAULT 9999,
                term TEXT NOT NULL,
                reading TEXT NOT NULL DEFAULT '',
                tags_json TEXT NOT NULL DEFAULT '[]',
                rules_json TEXT NOT NULL DEFAULT '[]',
                score REAL NOT NULL DEFAULT 0,
                sequence TEXT,
                name_type TEXT NOT NULL DEFAULT '',
                grammar_type TEXT NOT NULL DEFAULT '',
                expression_type TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE lexicon_entries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictionary_id TEXT NOT NULL,
                dictionary_title TEXT NOT NULL,
                dictionary_type TEXT NOT NULL,
                dictionary_priority INTEGER NOT NULL DEFAULT 9999,
                term TEXT NOT NULL,
                reading TEXT NOT NULL DEFAULT '',
                tags_json TEXT NOT NULL DEFAULT '[]',
                rules_json TEXT NOT NULL DEFAULT '[]',
                score REAL NOT NULL DEFAULT 0,
                sequence TEXT,
                name_type TEXT NOT NULL DEFAULT '',
                grammar_type TEXT NOT NULL DEFAULT '',
                expression_type TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE lexicon_meta(
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            INSERT INTO sync_sessions(
                sync_id,
                expected_entries,
                received_entries,
                dictionary_count,
                status
            )
            VALUES(
                'legacy-complete',
                1,
                1,
                1,
                'complete'
            );
            """
        )

    temporary_original = dictionary_store.DB_PATH
    dictionary_store.DB_PATH = migration_database

    try:
        migrated_status = dictionary_store.status()

        assert migrated_status["ready"] is False

        with sqlite3.connect(
            migration_database
        ) as connection:
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(sync_sessions)"
                )
            }

            legacy_session = connection.execute(
                """
                SELECT
                    created_at,
                    updated_at,
                    completed_at
                FROM sync_sessions
                WHERE sync_id = 'legacy-complete'
                """
            ).fetchone()

        expected_columns = {
            "snapshot_identity",
            "created_at",
            "updated_at",
            "completed_at",
            "error_code",
            "error_message",
        }

        assert expected_columns.issubset(columns)
        assert legacy_session is not None
        assert legacy_session[0] is not None
        assert legacy_session[1] is not None
        assert legacy_session[2] is not None
    finally:
        dictionary_store.DB_PATH = temporary_original


def test_clear_removes_live_and_session_data() -> None:
    cleared = dictionary_store.clear()

    assert cleared["ready"] is False
    assert cleared["entryCount"] == 0
    assert cleared["dictionaryCount"] == 0
    assert cleared["activeSession"] is None
    assert cleared["lastCompletedSession"] is None
    assert cleared["lastProblemSession"] is None
    assert cleared["stagedEntryCount"] == 0


def run() -> None:
    temporary_parent = Path(
        r"D:\Mining\_DELETE_AFTER_20260726\phase7"
    )
    temporary_parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tempfile.TemporaryDirectory(
        prefix="dictionary-lifecycle-",
        dir=temporary_parent,
        ignore_cleanup_errors=True,
    ) as temporary_directory:
        dictionary_store.DB_PATH = (
            Path(temporary_directory)
            / "dictionary.sqlite3"
        )

        try:
            test_successful_sync_and_persistence()
            test_expected_received_mismatch_preserves_live()
            test_dictionary_count_mismatch_preserves_live()
            test_cancel_removes_staging_and_preserves_live()
            test_retry_after_cancellation()
            test_recovery_clears_interrupted_staging()
            test_new_sync_interrupts_old_session()
            test_received_count_exceeded_preserves_live()
            test_additive_migration_from_legacy_schema()
            test_clear_removes_live_and_session_data()
        finally:
            dictionary_store.DB_PATH = ORIGINAL_DB_PATH

    print("dictionary sync lifecycle tests passed")


if __name__ == "__main__":
    run()
