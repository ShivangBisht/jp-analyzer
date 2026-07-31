from __future__ import annotations
import json, sqlite3, threading, uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .teaching_decision_store import DB_PATH as DECISION_DB_PATH, get_record, list_records

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "teaching_decisions.sqlite3"
_lock = threading.RLock()
QUALITY_STATES = {"captured", "needs-review", "reviewed", "approved", "rejected-for-corpus"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS teaching_quality_state(
 record_id TEXT PRIMARY KEY, quality_status TEXT NOT NULL, reviewer TEXT,
 quality_note TEXT, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teaching_quality_events(
 event_id TEXT PRIMARY KEY, record_id TEXT NOT NULL, previous_status TEXT,
 new_status TEXT NOT NULL, reviewer TEXT, quality_note TEXT, event_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_quality_status ON teaching_quality_state(quality_status,updated_at);
"""

def _now(): return datetime.now(timezone.utc).isoformat()
@contextmanager
def _db(path: Path | None = None):
    p=Path(path or DB_PATH);p.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(p,timeout=30);con.row_factory=sqlite3.Row;con.executescript(SCHEMA)
    try:
        with con: yield con
    finally: con.close()

def get_quality(record_id: str, db_path=None) -> dict[str, Any]:
    get_record(record_id, db_path=db_path)
    with _lock,_db(db_path) as con:
        row=con.execute("SELECT * FROM teaching_quality_state WHERE record_id=?",(record_id,)).fetchone()
        events=con.execute("SELECT * FROM teaching_quality_events WHERE record_id=? ORDER BY event_at,event_id",(record_id,)).fetchall()
    state=dict(row) if row else {"record_id":record_id,"quality_status":"captured","reviewer":None,"quality_note":None,"updated_at":None}
    state["events"]=[dict(x) for x in events]
    state["exportEligible"]=state["quality_status"]=="approved"
    state["exportEnabled"]=False
    return state

def set_quality(record_id: str, quality_status: str, *, reviewer=None, quality_note=None, db_path=None):
    if quality_status not in QUALITY_STATES: raise ValueError("unsupported quality status")
    record=get_record(record_id,db_path=db_path)
    if (record.get("lifecycle") or {}).get("status") != "active" and quality_status == "approved":
        raise ValueError("only active records can be approved")
    with _lock,_db(db_path) as con:
        old=con.execute("SELECT quality_status FROM teaching_quality_state WHERE record_id=?",(record_id,)).fetchone()
        previous=old["quality_status"] if old else "captured"
        now=_now()
        con.execute("INSERT INTO teaching_quality_state VALUES(?,?,?,?,?) ON CONFLICT(record_id) DO UPDATE SET quality_status=excluded.quality_status,reviewer=excluded.reviewer,quality_note=excluded.quality_note,updated_at=excluded.updated_at",(record_id,quality_status,reviewer,quality_note,now))
        con.execute("INSERT INTO teaching_quality_events VALUES(?,?,?,?,?,?,?)",("qevt-"+str(uuid.uuid4()),record_id,previous,quality_status,reviewer,quality_note,now))
    return get_quality(record_id,db_path=db_path)

def corpus_quality_summary(db_path=None):
    records=list_records(lifecycle_status=None,db_path=db_path)
    states=[]
    for record in records:
        quality=get_quality(record["recordId"],db_path=db_path)
        states.append({"record":record,"quality":quality})
    counts={state:0 for state in sorted(QUALITY_STATES)}
    duplicates={}; conflicts=[]
    active_states=[]
    for item in states:
        counts[item["quality"]["quality_status"]]+=1
        record=item["record"]
        if (record.get("lifecycle") or {}).get("status") != "active":
            continue
        active_states.append(item)
        key=(record.get("sourceSentence"),json.dumps((record.get("assertions") or {}).get("boundary"),sort_keys=True,ensure_ascii=False))
        duplicates.setdefault(key,[]).append(record)
    duplicate_groups=[{"recordIds":[x["recordId"] for x in group],"count":len(group)} for group in duplicates.values() if len(group)>1]
    for group in duplicates.values():
        judgments={x.get("judgment") for x in group}; classifications={json.dumps((x.get("assertions") or {}).get("classification"),sort_keys=True,ensure_ascii=False) for x in group}
        if len(judgments)>1 or len(classifications)>1: conflicts.append({"recordIds":[x["recordId"] for x in group],"judgments":sorted(judgments)})
    active_approved_count=sum(item["quality"]["quality_status"]=="approved" for item in active_states)
    return {"recordCount":len(records),"activeRecordCount":len(active_states),"byQualityStatus":counts,"approvedCount":counts["approved"],"needsReviewCount":counts["needs-review"],"duplicateGroupCount":len(duplicate_groups),"duplicateGroups":duplicate_groups,"conflictCount":len(conflicts),"conflicts":conflicts,"exportEligibleCount":active_approved_count,"exportEnabled":False}
