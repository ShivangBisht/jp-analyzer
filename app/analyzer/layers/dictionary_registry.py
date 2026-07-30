from __future__ import annotations

import re
import sqlite3
from typing import Any, Callable

_IMPORT_TIMESTAMP_PATTERN = re.compile(r"-(?P<timestamp>[0-9]{13})$")
_ISO_DATE_PATTERN = re.compile(r"(?P<revision>[0-9]{4}[-_][0-9]{2}[-_][0-9]{2})")


def stable_dictionary_identity(dictionary_id: str) -> str:
    normalized = str(dictionary_id or "").strip()
    match = _IMPORT_TIMESTAMP_PATTERN.search(normalized)
    return normalized[:match.start()] if match else normalized


def extract_dictionary_revision(title: str, dictionary_id: str) -> str | None:
    for value in (title, dictionary_id):
        match = _ISO_DATE_PATTERN.search(str(value or ""))
        if match:
            return match.group("revision").replace("_", "-")
    return None


def registry_rows_from_lexicon(connection: sqlite3.Connection):
    return connection.execute(
        """
        SELECT dictionary_id,
               MIN(dictionary_title) AS dictionary_title,
               MIN(dictionary_type) AS dictionary_type,
               MIN(dictionary_priority) AS dictionary_priority,
               COUNT(*) AS entry_count
        FROM lexicon_entries
        GROUP BY dictionary_id
        ORDER BY MIN(dictionary_priority), dictionary_id
        """
    ).fetchall()


def _record(row: sqlite3.Row, now: str) -> tuple[Any, ...]:
    dictionary_id = str(row["dictionary_id"])
    title = str(row["dictionary_title"])
    return (
        dictionary_id, stable_dictionary_identity(dictionary_id), title, title,
        str(row["dictionary_type"]), int(row["dictionary_priority"]),
        int(row["entry_count"]), None,
        extract_dictionary_revision(title, dictionary_id), None, None, None,
        now, now, None, None, 1,
    )


def _insert(connection: sqlite3.Connection, rows, now: str) -> None:
    connection.executemany(
        """
        INSERT INTO installed_dictionaries(
            dictionary_id, stable_identity, display_title, source_title,
            dictionary_type, priority, entry_count, content_digest,
            revision, version, source_url, update_manifest_url,
            installed_at, updated_at, last_update_check_at,
            last_update_status, enabled
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [_record(row, now) for row in rows],
    )


def backfill(connection: sqlite3.Connection, now_fn: Callable[[], str]) -> None:
    count = connection.execute(
        "SELECT COUNT(*) FROM installed_dictionaries"
    ).fetchone()[0]
    if count:
        return
    rows = registry_rows_from_lexicon(connection)
    if rows:
        _insert(connection, rows, now_fn())


def rebuild(connection: sqlite3.Connection, now_fn: Callable[[], str]) -> None:
    previous = {
        row["dictionary_id"]: dict(row)
        for row in connection.execute("SELECT * FROM installed_dictionaries")
    }
    connection.execute("DELETE FROM installed_dictionaries")
    rows = registry_rows_from_lexicon(connection)
    if rows:
        _insert(connection, rows, now_fn())
    for dictionary_id, metadata in previous.items():
        connection.execute(
            """
            UPDATE installed_dictionaries
            SET stable_identity = ?, content_digest = ?,
                revision = COALESCE(?, revision), version = ?, source_url = ?,
                update_manifest_url = ?, installed_at = ?,
                last_update_check_at = ?, last_update_status = ?, enabled = ?
            WHERE dictionary_id = ?
            """,
            (
                metadata["stable_identity"], metadata["content_digest"],
                metadata["revision"], metadata["version"],
                metadata["source_url"], metadata["update_manifest_url"],
                metadata["installed_at"], metadata["last_update_check_at"],
                metadata["last_update_status"], metadata["enabled"],
                dictionary_id,
            ),
        )


def records(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    return [
        {
            "dictionaryId": row["dictionary_id"],
            "stableIdentity": row["stable_identity"],
            "displayTitle": row["display_title"],
            "sourceTitle": row["source_title"],
            "dictionaryType": row["dictionary_type"],
            "priority": int(row["priority"]),
            "entryCount": int(row["entry_count"]),
            "contentDigest": row["content_digest"],
            "revision": row["revision"],
            "version": row["version"],
            "sourceUrl": row["source_url"],
            "updateManifestUrl": row["update_manifest_url"],
            "installedAt": row["installed_at"],
            "updatedAt": row["updated_at"],
            "lastUpdateCheckAt": row["last_update_check_at"],
            "lastUpdateStatus": row["last_update_status"],
            "enabled": bool(row["enabled"]),
        }
        for row in connection.execute(
            "SELECT * FROM installed_dictionaries ORDER BY priority, display_title, dictionary_id"
        )
    ]
