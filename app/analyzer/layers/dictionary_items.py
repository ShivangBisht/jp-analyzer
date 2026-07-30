from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from . import dictionary_store as store
from .dictionary_registry import records as registry_records

ACTIVE = {"receiving", "validating", "promoting"}


def _session(connection: sqlite3.Connection, operation_id: str):
    return connection.execute(
        "SELECT * FROM dictionary_item_sessions WHERE operation_id = ?",
        (operation_id,),
    ).fetchone()


def _staged_counts(connection: sqlite3.Connection, operation_id: str):
    row = connection.execute(
        """
        SELECT COUNT(*) AS entry_count,
               COUNT(DISTINCT dictionary_id) AS dictionary_count
        FROM staging_entries WHERE sync_id = ?
        """,
        (operation_id,),
    ).fetchone()
    return int(row["entry_count"]), int(row["dictionary_count"])


def _as_dict(connection: sqlite3.Connection, row):
    if row is None:
        return None
    staged, staged_dictionaries = _staged_counts(connection, row["operation_id"])
    expected = int(row["expected_entries"])
    received = int(row["received_entries"])
    return {
        "operationId": row["operation_id"],
        "mode": row["operation_mode"],
        "targetDictionaryId": row["target_dictionary_id"],
        "stableIdentity": row["stable_identity"],
        "displayTitle": row["display_title"],
        "dictionaryType": row["dictionary_type"],
        "priority": int(row["priority"]),
        "expectedEntries": expected,
        "receivedEntries": received,
        "stagedEntries": staged,
        "stagedDictionaryCount": staged_dictionaries,
        "status": row["status"],
        "revision": row["revision"],
        "version": row["version"],
        "contentDigest": row["content_digest"],
        "sourceUrl": row["source_url"],
        "updateManifestUrl": row["update_manifest_url"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
        "completedAt": row["completed_at"],
        "errorCode": row["error_code"],
        "errorMessage": row["error_message"],
        "progress": min(1.0, received / expected) if expected else 0.0,
    }


def start_operation(metadata: dict[str, Any]) -> dict[str, Any]:
    mode = str(metadata.get("mode") or "").strip().lower()
    if mode not in {"install", "update"}:
        raise ValueError("mode must be install or update")
    target_id = str(metadata.get("dictionaryId") or "").strip()
    stable_identity = str(metadata.get("stableIdentity") or "").strip()
    title = str(metadata.get("displayTitle") or "").strip()
    dictionary_type = str(metadata.get("dictionaryType") or "term").strip()
    expected = int(metadata.get("expectedEntries") or 0)
    if not target_id or not stable_identity or not title:
        raise ValueError("dictionaryId, stableIdentity, and displayTitle are required")
    if expected <= 0:
        raise ValueError("expectedEntries must be greater than zero")
    operation_id = str(uuid.uuid4())
    now = store._utc_now()
    with store._lock, store._db() as connection:
        active = connection.execute(
            "SELECT COUNT(*) FROM dictionary_item_sessions WHERE status IN ('receiving','validating','promoting')"
        ).fetchone()[0]
        if active:
            raise ValueError("Another dictionary operation is active")
        existing_id = connection.execute(
            "SELECT dictionary_id FROM installed_dictionaries WHERE dictionary_id = ?",
            (target_id,),
        ).fetchone()
        existing_identity = connection.execute(
            "SELECT dictionary_id FROM installed_dictionaries WHERE stable_identity = ?",
            (stable_identity,),
        ).fetchone()
        if mode == "install" and (existing_id or existing_identity):
            raise ValueError("Dictionary is already installed; use update")
        if mode == "update" and existing_id is None:
            raise ValueError("Update target is not installed")
        if mode == "update" and existing_id is not None:
            existing = connection.execute(
                "SELECT stable_identity, priority FROM installed_dictionaries WHERE dictionary_id = ?",
                (target_id,),
            ).fetchone()
            stable_identity = existing["stable_identity"]
            if int(metadata.get("priority") or 9999) == 9999:
                metadata = {**metadata, "priority": int(existing["priority"])}
        connection.execute(
            """
            INSERT INTO dictionary_item_sessions(
                operation_id, operation_mode, target_dictionary_id,
                stable_identity, display_title, dictionary_type, priority,
                expected_entries, received_entries, status, revision, version,
                content_digest, source_url, update_manifest_url,
                created_at, updated_at
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 0, 'receiving', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                operation_id, mode, target_id, stable_identity, title,
                dictionary_type, int(metadata.get("priority") or 9999), expected,
                metadata.get("revision"), metadata.get("version"),
                metadata.get("contentDigest"), metadata.get("sourceUrl"),
                metadata.get("updateManifestUrl"), now, now,
            ),
        )
        return _as_dict(connection, _session(connection, operation_id))


def add_batch(operation_id: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    with store._lock, store._db() as connection:
        session = _session(connection, operation_id)
        if session is None or session["status"] != "receiving":
            raise ValueError("Dictionary operation is not accepting batches")
        rows = []
        for entry in entries:
            term = str(entry.get("term") or "").strip()
            if not term:
                continue
            rows.append((
                operation_id, session["target_dictionary_id"],
                session["display_title"], session["dictionary_type"],
                int(session["priority"]), term, str(entry.get("reading") or ""),
                json.dumps(entry.get("tags") or [], ensure_ascii=False),
                json.dumps(entry.get("rules") or [], ensure_ascii=False),
                float(entry.get("score") or 0),
                None if entry.get("sequence") is None else str(entry.get("sequence")),
                str(entry.get("nameType") or ""),
                str(entry.get("grammarType") or ""),
                str(entry.get("expressionType") or ""),
            ))
        projected = int(session["received_entries"]) + len(rows)
        if projected > int(session["expected_entries"]):
            raise ValueError("Batch would exceed expectedEntries")
        connection.executemany(
            """
            INSERT INTO staging_entries(
                sync_id, dictionary_id, dictionary_title, dictionary_type,
                dictionary_priority, term, reading, tags_json, rules_json,
                score, sequence, name_type, grammar_type, expression_type
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.execute(
            "UPDATE dictionary_item_sessions SET received_entries = received_entries + ?, updated_at = ? WHERE operation_id = ?",
            (len(rows), store._utc_now(), operation_id),
        )
        return _as_dict(connection, _session(connection, operation_id))


def finish_operation(operation_id: str) -> dict[str, Any]:
    with store._lock, store._db() as connection:
        session = _session(connection, operation_id)
        if session is None or session["status"] != "receiving":
            raise ValueError("Dictionary operation is not ready to finish")
        staged, staged_dictionaries = _staged_counts(connection, operation_id)
        expected = int(session["expected_entries"])
        received = int(session["received_entries"])
        if received != expected or staged != received or staged_dictionaries != 1:
            message = (
                f"Validation failed: expected={expected}, received={received}, "
                f"staged={staged}, stagedDictionaries={staged_dictionaries}"
            )
            now = store._utc_now()
            connection.execute(
                "UPDATE dictionary_item_sessions SET status='failed', updated_at=?, completed_at=?, error_code='ITEM_COUNT_MISMATCH', error_message=? WHERE operation_id=?",
                (now, now, message, operation_id),
            )
            connection.commit()
            raise ValueError(message)
        connection.execute(
            "UPDATE dictionary_item_sessions SET status='promoting', updated_at=? WHERE operation_id=?",
            (store._utc_now(), operation_id),
        )
        target = session["target_dictionary_id"]
        if session["operation_mode"] == "update":
            connection.execute("DELETE FROM lexicon_entries WHERE dictionary_id = ?", (target,))
        connection.execute(
            """
            INSERT INTO lexicon_entries(
                dictionary_id, dictionary_title, dictionary_type,
                dictionary_priority, term, reading, tags_json, rules_json,
                score, sequence, name_type, grammar_type, expression_type
            )
            SELECT dictionary_id, dictionary_title, dictionary_type,
                   dictionary_priority, term, reading, tags_json, rules_json,
                   score, sequence, name_type, grammar_type, expression_type
            FROM staging_entries WHERE sync_id = ?
            """,
            (operation_id,),
        )
        promoted = connection.execute(
            "SELECT COUNT(*) FROM lexicon_entries WHERE dictionary_id = ?", (target,)
        ).fetchone()[0]
        if promoted != expected:
            raise RuntimeError("Promoted entry count mismatch")
        old = connection.execute(
            "SELECT installed_at FROM installed_dictionaries WHERE dictionary_id = ?", (target,)
        ).fetchone()
        now = store._utc_now()
        connection.execute(
            """
            INSERT INTO installed_dictionaries(
                dictionary_id, stable_identity, display_title, source_title,
                dictionary_type, priority, entry_count, content_digest,
                revision, version, source_url, update_manifest_url,
                installed_at, updated_at, enabled
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(dictionary_id) DO UPDATE SET
                stable_identity=excluded.stable_identity,
                display_title=excluded.display_title,
                source_title=excluded.source_title,
                dictionary_type=excluded.dictionary_type,
                priority=excluded.priority,
                entry_count=excluded.entry_count,
                content_digest=excluded.content_digest,
                revision=excluded.revision,
                version=excluded.version,
                source_url=excluded.source_url,
                update_manifest_url=excluded.update_manifest_url,
                updated_at=excluded.updated_at,
                enabled=1
            """,
            (
                target, session["stable_identity"], session["display_title"],
                session["display_title"], session["dictionary_type"],
                int(session["priority"]), promoted, session["content_digest"],
                session["revision"], session["version"], session["source_url"],
                session["update_manifest_url"], old["installed_at"] if old else now, now,
            ),
        )
        connection.execute("DELETE FROM staging_entries WHERE sync_id = ?", (operation_id,))
        connection.execute(
            "UPDATE dictionary_item_sessions SET status='complete', updated_at=?, completed_at=?, error_code=NULL, error_message=NULL WHERE operation_id=?",
            (now, now, operation_id),
        )
        return _as_dict(connection, _session(connection, operation_id))


def cancel_operation(operation_id: str) -> dict[str, Any]:
    with store._lock, store._db() as connection:
        session = _session(connection, operation_id)
        if session is None or session["status"] not in ACTIVE:
            raise ValueError("Only an active dictionary operation can be cancelled")
        connection.execute("DELETE FROM staging_entries WHERE sync_id = ?", (operation_id,))
        now = store._utc_now()
        connection.execute(
            "UPDATE dictionary_item_sessions SET status='cancelled', updated_at=?, completed_at=?, error_code='CANCELLED_BY_USER', error_message='Cancelled by user' WHERE operation_id=?",
            (now, now, operation_id),
        )
        return _as_dict(connection, _session(connection, operation_id))


def remove_dictionary(dictionary_id: str) -> dict[str, Any]:
    with store._lock, store._db() as connection:
        record = connection.execute(
            "SELECT * FROM installed_dictionaries WHERE dictionary_id = ?", (dictionary_id,)
        ).fetchone()
        if record is None:
            raise ValueError("Dictionary is not installed")
        removed = connection.execute(
            "SELECT COUNT(*) FROM lexicon_entries WHERE dictionary_id = ?", (dictionary_id,)
        ).fetchone()[0]
        connection.execute("DELETE FROM lexicon_entries WHERE dictionary_id = ?", (dictionary_id,))
        connection.execute("DELETE FROM installed_dictionaries WHERE dictionary_id = ?", (dictionary_id,))
        return {
            "status": "removed",
            "dictionaryId": dictionary_id,
            "stableIdentity": record["stable_identity"],
            "removedEntryCount": int(removed),
        }


def management_status() -> dict[str, Any]:
    with store._lock, store._db() as connection:
        active_row = connection.execute(
            "SELECT * FROM dictionary_item_sessions WHERE status IN ('receiving','validating','promoting') ORDER BY rowid DESC LIMIT 1"
        ).fetchone()
        problem_row = connection.execute(
            "SELECT * FROM dictionary_item_sessions WHERE status IN ('failed','cancelled') ORDER BY rowid DESC LIMIT 1"
        ).fetchone()
        dictionaries = registry_records(connection)
        return {
            "installedDictionaryCount": len(dictionaries),
            "registryEntryCount": sum(item["entryCount"] for item in dictionaries),
            "installedDictionaries": dictionaries,
            "activeOperation": _as_dict(connection, active_row),
            "lastProblemOperation": _as_dict(connection, problem_row),
        }



def update_dictionary_metadata(dictionary_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "stableIdentity": "stable_identity",
        "displayTitle": "display_title",
        "revision": "revision",
        "version": "version",
        "contentDigest": "content_digest",
        "sourceUrl": "source_url",
        "updateManifestUrl": "update_manifest_url",
        "lastUpdateCheckAt": "last_update_check_at",
        "lastUpdateStatus": "last_update_status",
    }
    assignments = []
    values = []
    for external, column in allowed.items():
        if external in metadata:
            value = metadata[external]
            if isinstance(value, str):
                value = value.strip() or None
            assignments.append(f"{column} = ?")
            values.append(value)
    if not assignments:
        raise ValueError("No supported metadata fields were supplied")
    with store._lock, store._db() as connection:
        existing = connection.execute(
            "SELECT dictionary_id FROM installed_dictionaries WHERE dictionary_id = ?",
            (dictionary_id,),
        ).fetchone()
        if existing is None:
            raise ValueError("Dictionary is not installed")
        assignments.append("updated_at = ?")
        values.append(store._utc_now())
        values.append(dictionary_id)
        connection.execute(
            f"UPDATE installed_dictionaries SET {', '.join(assignments)} WHERE dictionary_id = ?",
            values,
        )
        record = connection.execute(
            "SELECT * FROM installed_dictionaries WHERE dictionary_id = ?",
            (dictionary_id,),
        ).fetchone()
        return next(
            item for item in registry_records(connection)
            if item["dictionaryId"] == record["dictionary_id"]
        )
