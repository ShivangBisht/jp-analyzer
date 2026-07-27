from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .dictionary_registry import backfill as backfill_registry
from .dictionary_registry import rebuild as rebuild_registry
from .dictionary_registry import records as registry_records


DB_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "phase8_analysis_lexicon.sqlite3"
)

_lock = threading.RLock()

TERMINAL_SESSION_STATUSES = {
    "complete",
    "failed",
    "cancelled",
    "interrupted",
}

ACTIVE_SESSION_STATUSES = {
    "receiving",
    "validating",
    "promoting",
}


SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_sessions(
    sync_id TEXT PRIMARY KEY,
    expected_entries INTEGER NOT NULL DEFAULT 0,
    received_entries INTEGER NOT NULL DEFAULT 0,
    dictionary_count INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'receiving',
    snapshot_identity TEXT,
    created_at TEXT,
    updated_at TEXT,
    completed_at TEXT,
    error_code TEXT,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS staging_entries(
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

CREATE INDEX IF NOT EXISTS idx_staging_sync
ON staging_entries(sync_id);

CREATE TABLE IF NOT EXISTS lexicon_entries(
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

CREATE INDEX IF NOT EXISTS idx_lexicon_term
ON lexicon_entries(term);

CREATE INDEX IF NOT EXISTS idx_lexicon_reading
ON lexicon_entries(reading);

CREATE INDEX IF NOT EXISTS idx_lexicon_type
ON lexicon_entries(dictionary_type);

CREATE TABLE IF NOT EXISTS dictionary_item_sessions(
    operation_id TEXT PRIMARY KEY,
    operation_mode TEXT NOT NULL,
    target_dictionary_id TEXT NOT NULL,
    stable_identity TEXT NOT NULL,
    display_title TEXT NOT NULL,
    dictionary_type TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 9999,
    expected_entries INTEGER NOT NULL,
    received_entries INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'receiving',
    revision TEXT,
    version TEXT,
    content_digest TEXT,
    source_url TEXT,
    update_manifest_url TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    error_code TEXT,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_dictionary_item_session_status
ON dictionary_item_sessions(status);

CREATE TABLE IF NOT EXISTS lexicon_meta(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS installed_dictionaries(
    dictionary_id TEXT PRIMARY KEY,
    stable_identity TEXT NOT NULL,
    display_title TEXT NOT NULL,
    source_title TEXT NOT NULL,
    dictionary_type TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 9999,
    entry_count INTEGER NOT NULL DEFAULT 0,
    content_digest TEXT,
    revision TEXT,
    version TEXT,
    source_url TEXT,
    update_manifest_url TEXT,
    installed_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_update_check_at TEXT,
    last_update_status TEXT,
    enabled INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_installed_dictionary_stable_identity
ON installed_dictionaries(stable_identity);

CREATE INDEX IF NOT EXISTS idx_installed_dictionary_type
ON installed_dictionaries(dictionary_type);
"""


SESSION_COLUMN_MIGRATIONS = {
    "snapshot_identity": "TEXT",
    "created_at": "TEXT",
    "updated_at": "TEXT",
    "completed_at": "TEXT",
    "error_code": "TEXT",
    "error_message": "TEXT",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DB_PATH,
        timeout=120,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.executescript(SCHEMA)

    _migrate_schema(connection)
    return connection


def _migrate_schema(connection: sqlite3.Connection) -> None:
    existing_columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(sync_sessions)"
        )
    }

    for column_name, declaration in SESSION_COLUMN_MIGRATIONS.items():
        if column_name not in existing_columns:
            connection.execute(
                f'ALTER TABLE sync_sessions '
                f'ADD COLUMN "{column_name}" {declaration}'
            )

    now = _utc_now()

    connection.execute(
        """
        UPDATE sync_sessions
        SET created_at = COALESCE(created_at, ?),
            updated_at = COALESCE(updated_at, ?)
        """,
        (now, now),
    )

    connection.execute(
        """
        UPDATE sync_sessions
        SET completed_at = COALESCE(completed_at, updated_at)
        WHERE status = 'complete'
        """
    )

    backfill_registry(connection, _utc_now)

@contextmanager
def _db():
    connection = _connect()

    try:
        with connection:
            yield connection
    finally:
        connection.close()


def _metadata(connection: sqlite3.Connection) -> dict[str, str]:
    return {
        row["key"]: row["value"]
        for row in connection.execute(
            """
            SELECT key, value
            FROM lexicon_meta
            ORDER BY key
            """
        )
    }


def _set_metadata(
    connection: sqlite3.Connection,
    values: dict[str, Any],
) -> None:
    rows = [
        (str(key), str(value))
        for key, value in values.items()
        if value is not None
    ]

    connection.executemany(
        """
        INSERT INTO lexicon_meta(key, value)
        VALUES(?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        rows,
    )


def _session_to_dict(
    row: sqlite3.Row | None,
    *,
    staged_entries: int = 0,
    staged_dictionaries: int = 0,
) -> dict[str, Any] | None:
    if row is None:
        return None

    expected = int(row["expected_entries"] or 0)
    received = int(row["received_entries"] or 0)

    progress = 0.0
    if expected > 0:
        progress = min(1.0, received / expected)

    return {
        "syncId": row["sync_id"],
        "status": row["status"],
        "expectedEntries": expected,
        "receivedEntries": received,
        "stagedEntries": int(staged_entries),
        "dictionaryCount": int(row["dictionary_count"] or 0),
        "stagedDictionaryCount": int(staged_dictionaries),
        "snapshotIdentity": row["snapshot_identity"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
        "completedAt": row["completed_at"],
        "errorCode": row["error_code"],
        "errorMessage": row["error_message"],
        "progress": progress,
    }


def _session_details(
    connection: sqlite3.Connection,
    sync_id: str,
) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT *
        FROM sync_sessions
        WHERE sync_id = ?
        """,
        (sync_id,),
    ).fetchone()

    if row is None:
        return None

    staged = connection.execute(
        """
        SELECT
            COUNT(*) AS entry_count,
            COUNT(DISTINCT dictionary_id) AS dictionary_count
        FROM staging_entries
        WHERE sync_id = ?
        """,
        (sync_id,),
    ).fetchone()

    return _session_to_dict(
        row,
        staged_entries=staged["entry_count"],
        staged_dictionaries=staged["dictionary_count"],
    )


def _latest_session(
    connection: sqlite3.Connection,
    statuses: tuple[str, ...] | None = None,
) -> dict[str, Any] | None:
    parameters: tuple[Any, ...] = ()
    condition = ""

    if statuses:
        placeholders = ",".join("?" for _ in statuses)
        condition = f"WHERE status IN ({placeholders})"
        parameters = statuses

    row = connection.execute(
        f"""
        SELECT *
        FROM sync_sessions
        {condition}
        ORDER BY
            COALESCE(updated_at, created_at) DESC,
            rowid DESC
        LIMIT 1
        """,
        parameters,
    ).fetchone()

    if row is None:
        return None

    return _session_details(connection, row["sync_id"])


def _mark_session_failed(
    connection: sqlite3.Connection,
    sync_id: str,
    error_code: str,
    error_message: str,
) -> None:
    now = _utc_now()

    connection.execute(
        """
        UPDATE sync_sessions
        SET status = 'failed',
            updated_at = ?,
            completed_at = ?,
            error_code = ?,
            error_message = ?
        WHERE sync_id = ?
        """,
        (
            now,
            now,
            error_code,
            error_message,
            sync_id,
        ),
    )


def _validate_positive_integer(
    value: int,
    field_name: str,
) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{field_name} must be an integer"
        ) from error

    if normalized <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero"
        )

    return normalized


def start_sync(
    expected_entries: int = 0,
    dictionary_count: int = 0,
    snapshot_identity: str | None = None,
) -> dict[str, Any]:
    expected = _validate_positive_integer(
        expected_entries,
        "expectedEntries",
    )
    expected_dictionaries = _validate_positive_integer(
        dictionary_count,
        "dictionaryCount",
    )

    sync_id = str(uuid.uuid4())
    now = _utc_now()
    normalized_identity = (
        str(snapshot_identity).strip()
        if snapshot_identity
        else None
    )

    with _lock, _db() as connection:
        active_rows = connection.execute(
            """
            SELECT sync_id
            FROM sync_sessions
            WHERE status IN ('receiving', 'validating', 'promoting')
            """
        ).fetchall()

        for active in active_rows:
            interrupted_id = active["sync_id"]

            connection.execute(
                """
                DELETE FROM staging_entries
                WHERE sync_id = ?
                """,
                (interrupted_id,),
            )

            connection.execute(
                """
                UPDATE sync_sessions
                SET status = 'interrupted',
                    updated_at = ?,
                    completed_at = ?,
                    error_code = 'REPLACED_BY_NEW_SYNC',
                    error_message =
                        'The session was interrupted by a new sync.'
                WHERE sync_id = ?
                """,
                (now, now, interrupted_id),
            )

        connection.execute(
            """
            INSERT INTO sync_sessions(
                sync_id,
                expected_entries,
                received_entries,
                dictionary_count,
                status,
                snapshot_identity,
                created_at,
                updated_at,
                completed_at,
                error_code,
                error_message
            )
            VALUES(?, ?, 0, ?, 'receiving', ?, ?, ?, NULL, NULL, NULL)
            """,
            (
                sync_id,
                expected,
                expected_dictionaries,
                normalized_identity,
                now,
                now,
            ),
        )

        details = _session_details(connection, sync_id)

    return {
        **details,
        "database": str(DB_PATH),
    }


def add_batch(
    sync_id: str,
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    def encode_list(value: Any) -> str:
        normalized = (
            value
            if isinstance(value, list)
            else ([value] if value else [])
        )
        return json.dumps(
            normalized,
            ensure_ascii=False,
        )

    rows = []

    for entry in entries:
        term = str(entry.get("term") or "").strip()

        if not term:
            continue

        rows.append(
            (
                sync_id,
                str(entry.get("dictionaryId") or ""),
                str(entry.get("dictionaryTitle") or "unknown"),
                str(entry.get("dictionaryType") or "term"),
                int(entry.get("dictionaryPriority") or 9999),
                term,
                str(entry.get("reading") or ""),
                encode_list(entry.get("tags")),
                encode_list(entry.get("rules")),
                float(entry.get("score") or 0),
                (
                    None
                    if entry.get("sequence") is None
                    else str(entry.get("sequence"))
                ),
                str(entry.get("nameType") or ""),
                str(entry.get("grammarType") or ""),
                str(entry.get("expressionType") or ""),
            )
        )

    now = _utc_now()

    with _lock, _db() as connection:
        session = connection.execute(
            """
            SELECT status, expected_entries, received_entries
            FROM sync_sessions
            WHERE sync_id = ?
            """,
            (sync_id,),
        ).fetchone()

        if session is None:
            raise ValueError("Unknown sync session")

        if session["status"] != "receiving":
            raise ValueError(
                "Sync session is not accepting batches"
            )

        projected_received = (
            int(session["received_entries"] or 0)
            + len(rows)
        )
        expected = int(session["expected_entries"] or 0)

        if projected_received > expected:
            message = (
                "Batch would exceed expectedEntries: "
                f"expected {expected}, "
                f"projected {projected_received}"
            )

            _mark_session_failed(
                connection,
                sync_id,
                "RECEIVED_COUNT_EXCEEDED",
                message,
            )

            # Preserve the terminal failure state before propagating
            # the validation error. Otherwise the context manager
            # rolls this update back with the raised exception.
            connection.commit()
            raise ValueError(message)

        connection.executemany(
            """
            INSERT INTO staging_entries(
                sync_id,
                dictionary_id,
                dictionary_title,
                dictionary_type,
                dictionary_priority,
                term,
                reading,
                tags_json,
                rules_json,
                score,
                sequence,
                name_type,
                grammar_type,
                expression_type
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        connection.execute(
            """
            UPDATE sync_sessions
            SET received_entries = received_entries + ?,
                updated_at = ?
            WHERE sync_id = ?
            """,
            (len(rows), now, sync_id),
        )

        details = _session_details(connection, sync_id)

    return {
        "syncId": sync_id,
        "accepted": len(rows),
        "received": details["receivedEntries"],
        "expected": details["expectedEntries"],
        "staged": details["stagedEntries"],
        "progress": details["progress"],
        "status": details["status"],
    }


def _validate_sync_for_promotion(
    connection: sqlite3.Connection,
    sync_id: str,
) -> dict[str, Any]:
    details = _session_details(connection, sync_id)

    if details is None:
        raise ValueError("Unknown sync session")

    problems: list[tuple[str, str]] = []

    if details["status"] != "receiving":
        problems.append(
            (
                "SESSION_NOT_RECEIVING",
                (
                    "Expected session status receiving, found "
                    f"{details['status']}"
                ),
            )
        )

    if details["expectedEntries"] <= 0:
        problems.append(
            (
                "INVALID_EXPECTED_COUNT",
                "expectedEntries must be greater than zero",
            )
        )

    if (
        details["receivedEntries"]
        != details["expectedEntries"]
    ):
        problems.append(
            (
                "EXPECTED_RECEIVED_MISMATCH",
                (
                    "Expected entries do not match received entries: "
                    f"expected {details['expectedEntries']}, "
                    f"received {details['receivedEntries']}"
                ),
            )
        )

    if (
        details["stagedEntries"]
        != details["receivedEntries"]
    ):
        problems.append(
            (
                "RECEIVED_STAGED_MISMATCH",
                (
                    "Received entries do not match staged entries: "
                    f"received {details['receivedEntries']}, "
                    f"staged {details['stagedEntries']}"
                ),
            )
        )

    if details["stagedEntries"] <= 0:
        problems.append(
            (
                "EMPTY_STAGING",
                "Staging contains no dictionary entries",
            )
        )

    if (
        details["stagedDictionaryCount"]
        != details["dictionaryCount"]
    ):
        problems.append(
            (
                "DICTIONARY_COUNT_MISMATCH",
                (
                    "Expected dictionary count does not match staging: "
                    f"expected {details['dictionaryCount']}, "
                    f"staged {details['stagedDictionaryCount']}"
                ),
            )
        )

    if problems:
        error_code = problems[0][0]
        error_message = "; ".join(
            message
            for _, message in problems
        )

        _mark_session_failed(
            connection,
            sync_id,
            error_code,
            error_message,
        )

        # Validation failure is an intentional terminal state, not a
        # database-operation failure. Commit its diagnostics before
        # raising so the live lexicon remains unchanged while status
        # retains the actionable failure details.
        connection.commit()
        raise ValueError(error_message)

    return details


def finish_sync(sync_id: str) -> dict[str, Any]:
    now = _utc_now()

    with _lock, _db() as connection:
        connection.execute(
            """
            UPDATE sync_sessions
            SET status = 'validating',
                updated_at = ?
            WHERE sync_id = ? AND status = 'receiving'
            """,
            (now, sync_id),
        )

        connection.execute(
            """
            UPDATE sync_sessions
            SET status = 'receiving'
            WHERE sync_id = ? AND status = 'validating'
            """,
            (sync_id,),
        )

        details = _validate_sync_for_promotion(
            connection,
            sync_id,
        )

        connection.execute(
            """
            UPDATE sync_sessions
            SET status = 'promoting',
                updated_at = ?
            WHERE sync_id = ?
            """,
            (now, sync_id),
        )

        connection.execute(
            "DELETE FROM lexicon_entries"
        )

        connection.execute(
            """
            INSERT INTO lexicon_entries(
                dictionary_id,
                dictionary_title,
                dictionary_type,
                dictionary_priority,
                term,
                reading,
                tags_json,
                rules_json,
                score,
                sequence,
                name_type,
                grammar_type,
                expression_type
            )
            SELECT
                dictionary_id,
                dictionary_title,
                dictionary_type,
                dictionary_priority,
                term,
                reading,
                tags_json,
                rules_json,
                score,
                sequence,
                name_type,
                grammar_type,
                expression_type
            FROM staging_entries
            WHERE sync_id = ?
            """,
            (sync_id,),
        )

        promoted_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM lexicon_entries
            """
        ).fetchone()[0]

        promoted_dictionaries = connection.execute(
            """
            SELECT COUNT(DISTINCT dictionary_id)
            FROM lexicon_entries
            """
        ).fetchone()[0]

        if promoted_count != details["stagedEntries"]:
            raise RuntimeError(
                "Promoted entry count does not match staging"
            )

        if (
            promoted_dictionaries
            != details["stagedDictionaryCount"]
        ):
            raise RuntimeError(
                "Promoted dictionary count does not match staging"
            )

        type_counts = {
            row["dictionary_type"]: row["entry_count"]
            for row in connection.execute(
                """
                SELECT
                    dictionary_type,
                    COUNT(*) AS entry_count
                FROM lexicon_entries
                GROUP BY dictionary_type
                ORDER BY dictionary_type
                """
            )
        }

        rebuild_registry(connection, _utc_now)

        completed_at = _utc_now()

        _set_metadata(
            connection,
            {
                "last_sync_id": sync_id,
                "entry_count": promoted_count,
                "dictionary_count": promoted_dictionaries,
                "snapshot_identity": details[
                    "snapshotIdentity"
                ],
                "last_sync_completed_at": completed_at,
                "type_counts_json": json.dumps(
                    type_counts,
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            },
        )

        connection.execute(
            """
            UPDATE sync_sessions
            SET status = 'complete',
                updated_at = ?,
                completed_at = ?,
                error_code = NULL,
                error_message = NULL
            WHERE sync_id = ?
            """,
            (completed_at, completed_at, sync_id),
        )

        connection.execute(
            """
            DELETE FROM staging_entries
            WHERE sync_id = ?
            """,
            (sync_id,),
        )

    return {
        "syncId": sync_id,
        "status": "complete",
        "entryCount": promoted_count,
        "dictionaryCount": promoted_dictionaries,
        "typeCounts": type_counts,
        "snapshotIdentity": details["snapshotIdentity"],
        "completedAt": completed_at,
    }


def cancel_sync(sync_id: str) -> dict[str, Any]:
    now = _utc_now()

    with _lock, _db() as connection:
        session = connection.execute(
            """
            SELECT status
            FROM sync_sessions
            WHERE sync_id = ?
            """,
            (sync_id,),
        ).fetchone()

        if session is None:
            raise ValueError("Unknown sync session")

        if session["status"] not in ACTIVE_SESSION_STATUSES:
            raise ValueError(
                "Only an active sync session can be cancelled"
            )

        connection.execute(
            """
            DELETE FROM staging_entries
            WHERE sync_id = ?
            """,
            (sync_id,),
        )

        connection.execute(
            """
            UPDATE sync_sessions
            SET status = 'cancelled',
                updated_at = ?,
                completed_at = ?,
                error_code = 'CANCELLED_BY_USER',
                error_message =
                    'The synchronization was cancelled by the user.'
            WHERE sync_id = ?
            """,
            (now, now, sync_id),
        )

        details = _session_details(connection, sync_id)

    return details


def recover_interrupted_syncs() -> dict[str, Any]:
    recovered: list[str] = []
    cleaned_terminal_sessions: list[str] = []
    now = _utc_now()

    with _lock, _db() as connection:
        rows = connection.execute(
            """
            SELECT
                session.sync_id,
                session.status,
                COUNT(staging.sync_id) AS staged_entries
            FROM sync_sessions AS session
            LEFT JOIN staging_entries AS staging
                ON staging.sync_id = session.sync_id
            WHERE session.status IN (
                'receiving',
                'validating',
                'promoting',
                'failed',
                'cancelled',
                'interrupted'
            )
            GROUP BY session.sync_id, session.status
            ORDER BY session.rowid
            """
        ).fetchall()

        for row in rows:
            sync_id = row["sync_id"]
            session_status = row["status"]
            staged_entries = int(row["staged_entries"] or 0)

            if staged_entries > 0:
                connection.execute(
                    """
                    DELETE FROM staging_entries
                    WHERE sync_id = ?
                    """,
                    (sync_id,),
                )

            if session_status in ACTIVE_SESSION_STATUSES:
                connection.execute(
                    """
                    UPDATE sync_sessions
                    SET status = 'interrupted',
                        updated_at = ?,
                        completed_at = ?,
                        error_code = 'RECOVERED_INTERRUPTED_SYNC',
                        error_message =
                            'Interrupted staging was cleared during recovery.'
                    WHERE sync_id = ?
                    """,
                    (now, now, sync_id),
                )

                recovered.append(sync_id)
                continue

            if staged_entries > 0:
                cleaned_terminal_sessions.append(sync_id)

    return {
        "status": "recovered",
        "recoveredCount": len(recovered),
        "recoveredSyncIds": recovered,
        "cleanedTerminalCount": len(cleaned_terminal_sessions),
        "cleanedTerminalSyncIds": cleaned_terminal_sessions,
        "database": str(DB_PATH),
    }


def status() -> dict[str, Any]:
    with _lock, _db() as connection:
        entry_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM lexicon_entries
            """
        ).fetchone()[0]

        dictionary_count = connection.execute(
            """
            SELECT COUNT(DISTINCT dictionary_id)
            FROM lexicon_entries
            """
        ).fetchone()[0]

        type_counts = {
            row["dictionary_type"]: row["entry_count"]
            for row in connection.execute(
                """
                SELECT
                    dictionary_type,
                    COUNT(*) AS entry_count
                FROM lexicon_entries
                GROUP BY dictionary_type
                ORDER BY dictionary_type
                """
            )
        }

        metadata = _metadata(connection)

        active_session = _latest_session(
            connection,
            tuple(ACTIVE_SESSION_STATUSES),
        )

        last_completed = _latest_session(
            connection,
            ("complete",),
        )

        last_problem = _latest_session(
            connection,
            ("failed", "cancelled", "interrupted"),
        )

        staged_total = connection.execute(
            """
            SELECT COUNT(*)
            FROM staging_entries
            """
        ).fetchone()[0]

        installed_dictionaries = registry_records(connection)
        installed_dictionary_count = len(installed_dictionaries)
        registry_entry_count = sum(
            item["entryCount"]
            for item in installed_dictionaries
        )

    registry_consistent = (
        installed_dictionary_count == dictionary_count
        and registry_entry_count == entry_count
    )

    recovery_required = (
        active_session is not None
        or staged_total > 0
    )

    return {
        "ready": entry_count > 0,
        "entryCount": entry_count,
        "dictionaryCount": dictionary_count,
        "typeCounts": type_counts,
        "lastSyncId": metadata.get("last_sync_id"),
        "snapshotIdentity": metadata.get(
            "snapshot_identity"
        ),
        "lastSyncCompletedAt": metadata.get(
            "last_sync_completed_at"
        ),
        "database": str(DB_PATH),
        "activeSession": active_session,
        "lastCompletedSession": last_completed,
        "lastProblemSession": last_problem,
        "stagedEntryCount": staged_total,
        "recoveryRequired": recovery_required,
        "installedDictionaryCount": installed_dictionary_count,
        "registryEntryCount": registry_entry_count,
        "registryConsistent": registry_consistent,
        "installedDictionaries": installed_dictionaries,
    }


def clear() -> dict[str, Any]:
    with _lock, _db() as connection:
        for table in (
            "lexicon_entries",
            "staging_entries",
            "sync_sessions",
            "lexicon_meta",
            "installed_dictionaries",
            "dictionary_item_sessions",
        ):
            connection.execute(
                f'DELETE FROM "{table}"'
            )

    return status()
