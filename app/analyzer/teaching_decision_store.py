from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analyzer_decision_snapshot import validate_analyzer_decision_snapshot
from .teaching_decision_record import validate_teaching_decision_record

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "teaching_decisions.sqlite3"
_lock = threading.RLock()
SCHEMA = """
CREATE TABLE IF NOT EXISTS decision_snapshots(
 snapshot_id TEXT PRIMARY KEY, content_digest TEXT NOT NULL UNIQUE, sentence_sha256 TEXT NOT NULL,
 payload_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teaching_decision_records(
 record_id TEXT PRIMARY KEY, content_digest TEXT NOT NULL UNIQUE, snapshot_id TEXT NOT NULL,
 sentence_sha256 TEXT NOT NULL, judgment TEXT NOT NULL, failure_classification TEXT NOT NULL,
 lifecycle_status TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL,
 FOREIGN KEY(snapshot_id) REFERENCES decision_snapshots(snapshot_id)
);
CREATE INDEX IF NOT EXISTS idx_tdr_query ON teaching_decision_records(judgment,failure_classification,lifecycle_status,created_at);
CREATE INDEX IF NOT EXISTS idx_tdr_sentence ON teaching_decision_records(sentence_sha256,created_at);
CREATE TABLE IF NOT EXISTS teaching_decision_events(
 event_id TEXT PRIMARY KEY, record_id TEXT NOT NULL, event_type TEXT NOT NULL, event_at TEXT NOT NULL,
 related_record_id TEXT, note TEXT, FOREIGN KEY(record_id) REFERENCES teaching_decision_records(record_id)
);
"""


def _now(): return datetime.now(timezone.utc).isoformat()
def _json(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)

@contextmanager
def _db(path: Path | None = None):
    p = Path(path or DB_PATH); p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(p, timeout=30); con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL"); con.execute("PRAGMA foreign_keys=ON"); con.executescript(SCHEMA)
    try:
        with con: yield con
    finally: con.close()


def save_snapshot(snapshot: dict[str, Any], db_path=None) -> dict[str, Any]:
    validate_analyzer_decision_snapshot(snapshot)
    sid, digest = snapshot["snapshotId"], snapshot["contentDigest"]
    sentence_sha = snapshot["source"]["sentenceSha256"]
    with _lock, _db(db_path) as con:
        row = con.execute("SELECT content_digest,payload_json FROM decision_snapshots WHERE snapshot_id=?", (sid,)).fetchone()
        if row and row["content_digest"] != digest:
            raise ValueError("snapshot ID already exists with different digest")
        con.execute("INSERT OR IGNORE INTO decision_snapshots VALUES(?,?,?,?,?)", (sid, digest, sentence_sha, _json(snapshot), _now()))
    return {"snapshotId": sid, "contentDigest": digest, "inserted": row is None}


def persist_record(record: dict[str, Any], *, snapshot: dict[str, Any] | None = None, db_path=None) -> dict[str, Any]:
    validate_teaching_decision_record(record)
    if record["qualityState"]["exportStatus"] != "excluded":
        raise ValueError("Alpha 4 only accepts export-excluded records")
    sid = record["snapshotReference"]["snapshotId"]
    expected_digest = record["snapshotReference"]["contentDigest"]
    with _lock, _db(db_path) as con:
        snap = con.execute("SELECT content_digest,sentence_sha256 FROM decision_snapshots WHERE snapshot_id=?", (sid,)).fetchone()
    if snap is None:
        if snapshot is None: raise ValueError("referenced AnalyzerDecisionSnapshot is not stored")
        save_snapshot(snapshot, db_path=db_path)
        with _lock, _db(db_path) as con:
            snap = con.execute("SELECT content_digest,sentence_sha256 FROM decision_snapshots WHERE snapshot_id=?", (sid,)).fetchone()
    if snap["content_digest"] != expected_digest:
        raise ValueError("record snapshot digest does not match stored snapshot")
    if snap["sentence_sha256"] != __import__("hashlib").sha256(record["sourceSentence"].encode("utf-8")).hexdigest():
        raise ValueError("record sentence does not match referenced snapshot")
    rid = record["recordId"]
    status = record["lifecycle"]["status"]
    with _lock, _db(db_path) as con:
        existing = con.execute("SELECT content_digest FROM teaching_decision_records WHERE record_id=?", (rid,)).fetchone()
        if existing and existing["content_digest"] != record["contentDigest"]:
            raise ValueError("record ID already exists with different digest")
        con.execute("INSERT OR IGNORE INTO teaching_decision_records VALUES(?,?,?,?,?,?,?,?,?)", (
            rid, record["contentDigest"], sid, snap["sentence_sha256"], record["judgment"], record["failureClassification"],
            status, _json(record), record["createdAt"],
        ))
        if existing is None:
            con.execute("INSERT INTO teaching_decision_events VALUES(?,?,?,?,?,?)", ("evt-"+str(uuid.uuid4()), rid, "created", _now(), None, None))
    return get_record(rid, db_path=db_path)


def get_record(record_id: str, db_path=None) -> dict[str, Any]:
    with _lock, _db(db_path) as con:
        row = con.execute("SELECT payload_json,lifecycle_status FROM teaching_decision_records WHERE record_id=?", (record_id,)).fetchone()
        if not row: raise ValueError("TeachingDecisionRecord not found")
        events = con.execute("SELECT * FROM teaching_decision_events WHERE record_id=? ORDER BY event_at,event_id", (record_id,)).fetchall()
    result = json.loads(row["payload_json"]); result["lifecycle"]["status"] = row["lifecycle_status"]
    result["storeEvents"] = [dict(x) for x in events]
    return result


def list_records(*, judgment=None, failure_classification=None, lifecycle_status="active", sentence_sha256=None, db_path=None):
    clauses=[]; values=[]
    for column, value in (("judgment", judgment), ("failure_classification", failure_classification), ("lifecycle_status", lifecycle_status), ("sentence_sha256", sentence_sha256)):
        if value is not None: clauses.append(column+"=?"); values.append(value)
    sql="SELECT record_id FROM teaching_decision_records"+(" WHERE "+" AND ".join(clauses) if clauses else "")+" ORDER BY created_at,record_id"
    with _lock, _db(db_path) as con: rows=con.execute(sql, values).fetchall()
    return [get_record(x["record_id"], db_path=db_path) for x in rows]


def _transition(record_id: str, new_status: str, *, related_record_id=None, note=None, db_path=None):
    with _lock, _db(db_path) as con:
        row=con.execute("SELECT lifecycle_status FROM teaching_decision_records WHERE record_id=?", (record_id,)).fetchone()
        if not row: raise ValueError("TeachingDecisionRecord not found")
        if row["lifecycle_status"] != "active": raise ValueError("only active records can transition")
        con.execute("UPDATE teaching_decision_records SET lifecycle_status=? WHERE record_id=?", (new_status, record_id))
        con.execute("INSERT INTO teaching_decision_events VALUES(?,?,?,?,?,?)", ("evt-"+str(uuid.uuid4()), record_id, new_status, _now(), related_record_id, note))
    return get_record(record_id, db_path=db_path)


def retract_record(record_id: str, *, note=None, db_path=None): return _transition(record_id, "retracted", note=note, db_path=db_path)
def supersede_record(record_id: str, replacement_record: dict[str, Any], *, snapshot=None, note=None, db_path=None):
    replacement = persist_record(replacement_record, snapshot=snapshot, db_path=db_path)
    old = _transition(record_id, "superseded", related_record_id=replacement["recordId"], note=note, db_path=db_path)
    return {"superseded": old, "replacement": replacement}


def integrity_report(db_path=None):
    issues=[]
    with _lock, _db(db_path) as con:
        rows=con.execute("SELECT record_id,snapshot_id,payload_json,content_digest FROM teaching_decision_records").fetchall()
        snapshots=con.execute("SELECT COUNT(*) FROM decision_snapshots").fetchone()[0]
    for row in rows:
        try:
            payload=json.loads(row["payload_json"]); validate_teaching_decision_record(payload)
            if payload["contentDigest"] != row["content_digest"]: raise ValueError("stored digest mismatch")
        except Exception as exc: issues.append({"recordId":row["record_id"],"error":str(exc)})
    return {"ok":not issues,"issueCount":len(issues),"issues":issues,"snapshotCount":snapshots,"recordCount":len(rows),"database":str(db_path or DB_PATH),"exportEnabled":False}
