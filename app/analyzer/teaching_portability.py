from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analyzer_decision_snapshot import validate_analyzer_decision_snapshot
from .teaching_decision_record import validate_teaching_decision_record
from .teaching_decision_store import DB_PATH, SCHEMA as DECISION_SCHEMA
from .teaching_quality_store import SCHEMA as QUALITY_SCHEMA

TRANSFER_SCHEMA = "TeachingEvidenceTransfer.v1"
_ALLOWED_LIFECYCLE = {"active", "superseded", "retracted"}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect(db_path: Path | str | None):
    path = Path(db_path or DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(DECISION_SCHEMA)
    con.executescript(QUALITY_SCHEMA)
    return con


def _rows(con, table: str, order_by: str) -> list[dict[str, Any]]:
    return [dict(row) for row in con.execute(f"SELECT * FROM {table} ORDER BY {order_by}").fetchall()]


def _package_core(db_path=None) -> dict[str, Any]:
    con = _connect(db_path)
    try:
        snapshots = _rows(con, "decision_snapshots", "snapshot_id")
        records = _rows(con, "teaching_decision_records", "record_id")
        decision_events = _rows(con, "teaching_decision_events", "event_at,event_id")
        quality_states = _rows(con, "teaching_quality_state", "record_id")
        quality_events = _rows(con, "teaching_quality_events", "event_at,event_id")
    finally:
        con.close()

    snapshot_items = [{**row, "payload": json.loads(row.pop("payload_json"))} for row in snapshots]
    record_items = [{**row, "payload": json.loads(row.pop("payload_json"))} for row in records]
    identity = {
        "snapshotDigests": [[x["snapshot_id"], x["content_digest"]] for x in snapshot_items],
        "recordDigests": [[x["record_id"], x["content_digest"]] for x in record_items],
        "decisionEventIds": [x["event_id"] for x in decision_events],
        "qualityEventIds": [x["event_id"] for x in quality_events],
    }
    return {
        "schema": TRANSFER_SCHEMA,
        "mode": "teaching-evidence-only",
        "createdAt": _now(),
        "sourceStoreIdentity": _digest(identity),
        "includesOperationalCorrections": False,
        "includesDictionary": False,
        "tuningEnabled": False,
        "activationEnabled": False,
        "snapshots": snapshot_items,
        "records": record_items,
        "decisionEvents": decision_events,
        "qualityStates": quality_states,
        "qualityEvents": quality_events,
        "counts": {
            "snapshots": len(snapshot_items),
            "records": len(record_items),
            "decisionEvents": len(decision_events),
            "qualityStates": len(quality_states),
            "qualityEvents": len(quality_events),
        },
    }


def export_teaching_evidence(*, db_path=None) -> dict[str, Any]:
    core = _package_core(db_path)
    return {**core, "packageDigest": _digest(core)}


def verify_teaching_evidence(package: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if package.get("schema") != TRANSFER_SCHEMA:
        problems.append("unsupported-schema")
    for key in ("includesOperationalCorrections", "includesDictionary", "tuningEnabled", "activationEnabled"):
        if package.get(key) is not False:
            problems.append(f"{key}-must-be-false")
    core = {k: v for k, v in package.items() if k != "packageDigest"}
    if package.get("packageDigest") != _digest(core):
        problems.append("package-digest-mismatch")

    collections = {
        "snapshot": (package.get("snapshots") or [], "snapshot_id"),
        "record": (package.get("records") or [], "record_id"),
        "decision-event": (package.get("decisionEvents") or [], "event_id"),
        "quality-state": (package.get("qualityStates") or [], "record_id"),
        "quality-event": (package.get("qualityEvents") or [], "event_id"),
    }
    for label, (items, key) in collections.items():
        ids = [x.get(key) for x in items]
        if None in ids or len(ids) != len(set(ids)):
            problems.append(f"duplicate-or-missing-{label}-id")

    snapshot_ids = {x.get("snapshot_id") for x in package.get("snapshots") or []}
    record_ids = {x.get("record_id") for x in package.get("records") or []}
    for item in package.get("snapshots") or []:
        try:
            validate_analyzer_decision_snapshot(item.get("payload") or {})
            if item.get("payload", {}).get("snapshotId") != item.get("snapshot_id"):
                raise ValueError("snapshot row ID mismatch")
            if item.get("payload", {}).get("contentDigest") != item.get("content_digest"):
                raise ValueError("snapshot row digest mismatch")
        except (TypeError, ValueError) as exc:
            problems.append(f"invalid-snapshot:{item.get('snapshot_id')}:{exc}")
    for item in package.get("records") or []:
        try:
            validate_teaching_decision_record(item.get("payload") or {})
            payload = item.get("payload") or {}
            if payload.get("recordId") != item.get("record_id"):
                raise ValueError("record row ID mismatch")
            if payload.get("contentDigest") != item.get("content_digest"):
                raise ValueError("record row digest mismatch")
            if item.get("snapshot_id") not in snapshot_ids:
                raise ValueError("referenced snapshot missing from package")
            if item.get("lifecycle_status") not in _ALLOWED_LIFECYCLE:
                raise ValueError("unsupported lifecycle status")
        except (TypeError, ValueError) as exc:
            problems.append(f"invalid-record:{item.get('record_id')}:{exc}")
    for item in package.get("decisionEvents") or []:
        if item.get("record_id") not in record_ids:
            problems.append(f"orphan-decision-event:{item.get('event_id')}")
        related = item.get("related_record_id")
        if related and related not in record_ids:
            problems.append(f"broken-related-record:{item.get('event_id')}")
    for item in package.get("qualityStates") or []:
        if item.get("record_id") not in record_ids:
            problems.append(f"orphan-quality-state:{item.get('record_id')}")
    for item in package.get("qualityEvents") or []:
        if item.get("record_id") not in record_ids:
            problems.append(f"orphan-quality-event:{item.get('event_id')}")

    expected_counts = package.get("counts") or {}
    actual_counts = {
        "snapshots": len(package.get("snapshots") or []),
        "records": len(package.get("records") or []),
        "decisionEvents": len(package.get("decisionEvents") or []),
        "qualityStates": len(package.get("qualityStates") or []),
        "qualityEvents": len(package.get("qualityEvents") or []),
    }
    if expected_counts != actual_counts:
        problems.append("count-manifest-mismatch")
    return {"ok": not problems, "problems": problems, "schema": TRANSFER_SCHEMA, "packageDigest": package.get("packageDigest")}


def _stored_map(con, table: str, key: str) -> dict[str, dict[str, Any]]:
    return {str(row[key]): dict(row) for row in con.execute(f"SELECT * FROM {table}").fetchall()}


def _normalized_snapshot(item):
    return {**{k: v for k, v in item.items() if k != "payload"}, "payload_json": json.dumps(item["payload"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)}


def _normalized_record(item):
    return {**{k: v for k, v in item.items() if k != "payload"}, "payload_json": json.dumps(item["payload"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)}


def preview_teaching_evidence_import(package: dict[str, Any], *, db_path=None) -> dict[str, Any]:
    verification = verify_teaching_evidence(package)
    result = {
        "schema": TRANSFER_SCHEMA,
        "packageDigest": package.get("packageDigest"),
        "verification": verification,
        "canApply": False,
        "actions": {"insert": [], "alreadyPresent": [], "conflict": [], "blocked": []},
        "writesPerformed": False,
    }
    if not verification["ok"]:
        result["actions"]["blocked"].extend(verification["problems"])
        return result

    con = _connect(db_path)
    try:
        specs = [
            ("snapshots", "decision_snapshots", "snapshot_id", _normalized_snapshot),
            ("records", "teaching_decision_records", "record_id", _normalized_record),
            ("decisionEvents", "teaching_decision_events", "event_id", lambda x: x),
            ("qualityStates", "teaching_quality_state", "record_id", lambda x: x),
            ("qualityEvents", "teaching_quality_events", "event_id", lambda x: x),
        ]
        for package_key, table, key, normalize in specs:
            existing = _stored_map(con, table, key)
            for raw in package.get(package_key) or []:
                item = normalize(raw)
                item_id = str(item[key])
                action = {"entity": package_key, "id": item_id}
                if item_id not in existing:
                    result["actions"]["insert"].append(action)
                elif existing[item_id] == item:
                    result["actions"]["alreadyPresent"].append(action)
                else:
                    action["reason"] = "same-id-different-content"
                    result["actions"]["conflict"].append(action)
    finally:
        con.close()

    result["canApply"] = not result["actions"]["conflict"] and not result["actions"]["blocked"]
    result["counts"] = {key: len(value) for key, value in result["actions"].items()}
    return result


def apply_teaching_evidence_import(package: dict[str, Any], *, confirm_package_digest: str, db_path=None) -> dict[str, Any]:
    if confirm_package_digest != package.get("packageDigest"):
        raise ValueError("package digest confirmation mismatch")
    preview = preview_teaching_evidence_import(package, db_path=db_path)
    if not preview["canApply"]:
        raise ValueError("import preview contains conflicts or blocked items")

    con = _connect(db_path)
    inserted = {"snapshots": 0, "records": 0, "decisionEvents": 0, "qualityStates": 0, "qualityEvents": 0}
    try:
        con.execute("BEGIN IMMEDIATE")
        for raw in package.get("snapshots") or []:
            item = _normalized_snapshot(raw)
            cur = con.execute("INSERT OR IGNORE INTO decision_snapshots(snapshot_id,content_digest,sentence_sha256,payload_json,created_at) VALUES(:snapshot_id,:content_digest,:sentence_sha256,:payload_json,:created_at)", item)
            inserted["snapshots"] += cur.rowcount
        for raw in package.get("records") or []:
            item = _normalized_record(raw)
            cur = con.execute("INSERT OR IGNORE INTO teaching_decision_records(record_id,content_digest,snapshot_id,sentence_sha256,judgment,failure_classification,lifecycle_status,payload_json,created_at) VALUES(:record_id,:content_digest,:snapshot_id,:sentence_sha256,:judgment,:failure_classification,:lifecycle_status,:payload_json,:created_at)", item)
            inserted["records"] += cur.rowcount
        for item in package.get("decisionEvents") or []:
            cur = con.execute("INSERT OR IGNORE INTO teaching_decision_events(event_id,record_id,event_type,event_at,related_record_id,note) VALUES(:event_id,:record_id,:event_type,:event_at,:related_record_id,:note)", item)
            inserted["decisionEvents"] += cur.rowcount
        for item in package.get("qualityStates") or []:
            cur = con.execute("INSERT OR IGNORE INTO teaching_quality_state(record_id,quality_status,reviewer,quality_note,updated_at) VALUES(:record_id,:quality_status,:reviewer,:quality_note,:updated_at)", item)
            inserted["qualityStates"] += cur.rowcount
        for item in package.get("qualityEvents") or []:
            cur = con.execute("INSERT OR IGNORE INTO teaching_quality_events(event_id,record_id,previous_status,new_status,reviewer,quality_note,event_at) VALUES(:event_id,:record_id,:previous_status,:new_status,:reviewer,:quality_note,:event_at)", item)
            inserted["qualityEvents"] += cur.rowcount
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

    after = preview_teaching_evidence_import(package, db_path=db_path)
    return {
        "schema": TRANSFER_SCHEMA,
        "packageDigest": package.get("packageDigest"),
        "applied": True,
        "inserted": inserted,
        "idempotent": all(value == 0 for value in inserted.values()),
        "postImportPreview": after,
        "tuningEnabled": False,
        "activationEnabled": False,
        "dictionaryChanged": False,
        "operationalCorrectionsIncluded": False,
    }
