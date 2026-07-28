from __future__ import annotations

import hashlib, json, sqlite3, threading, uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .teaching_annotation_contract import SourceRange, build_partial_coverage, stable_dataset_assignment

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "teaching_annotations.sqlite3"
_lock = threading.RLock()
SCHEMA = """
CREATE TABLE IF NOT EXISTS analyzer_snapshots(
 snapshot_id TEXT PRIMARY KEY, content_digest TEXT NOT NULL UNIQUE, snapshot_kind TEXT NOT NULL,
 sentence_text TEXT NOT NULL, sentence_fingerprint TEXT NOT NULL, analyzer_version TEXT NOT NULL,
 engine_version TEXT, compact_schema_version TEXT, reader_span_schema_version TEXT NOT NULL,
 reader_candidate_schema_version TEXT, correction_revision TEXT NOT NULL, dictionary_identity_json TEXT,
 full_analysis_json TEXT NOT NULL, compact_analysis_json TEXT NOT NULL, raw_baseline_snapshot_id TEXT,
 created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_annotation_snapshots_sentence ON analyzer_snapshots(sentence_fingerprint,created_at);
CREATE TABLE IF NOT EXISTS teaching_annotations(
 annotation_id TEXT PRIMARY KEY, correction_id TEXT NOT NULL, status TEXT NOT NULL,
 sentence_text TEXT NOT NULL, sentence_fingerprint TEXT NOT NULL, start INTEGER NOT NULL, end INTEGER NOT NULL,
 surface TEXT NOT NULL, action TEXT NOT NULL, display_role TEXT, split_offsets_json TEXT NOT NULL,
 target_spans_json TEXT NOT NULL, raw_baseline_snapshot_id TEXT NOT NULL, effective_baseline_snapshot_id TEXT NOT NULL,
 confidence TEXT NOT NULL, note TEXT, coverage_json TEXT NOT NULL, provenance_json TEXT NOT NULL,
 derived_outcome_json TEXT NOT NULL, dataset_group_id TEXT NOT NULL, dataset_partition TEXT NOT NULL,
 supersedes_annotation_id TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(raw_baseline_snapshot_id) REFERENCES analyzer_snapshots(snapshot_id),
 FOREIGN KEY(effective_baseline_snapshot_id) REFERENCES analyzer_snapshots(snapshot_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_annotations_active_correction ON teaching_annotations(correction_id) WHERE status='active';
CREATE INDEX IF NOT EXISTS idx_annotations_sentence ON teaching_annotations(sentence_fingerprint,start,end,status);
CREATE TABLE IF NOT EXISTS annotation_history(
 event_id TEXT PRIMARY KEY, annotation_id TEXT NOT NULL, event_type TEXT NOT NULL, event_at TEXT NOT NULL,
 correction_revision_before TEXT, correction_revision_after TEXT, related_annotation_id TEXT, note TEXT,
 FOREIGN KEY(annotation_id) REFERENCES teaching_annotations(annotation_id)
);
"""

def _now(): return datetime.now(timezone.utc).isoformat()
def _canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str)
def _fingerprint(text): return hashlib.sha256(text.encode('utf-8')).hexdigest()
@contextmanager
def _db(path: Path | None=None):
 p=path or DB_PATH; p.parent.mkdir(parents=True,exist_ok=True); con=sqlite3.connect(p,timeout=30); con.row_factory=sqlite3.Row
 con.execute('PRAGMA journal_mode=WAL'); con.execute('PRAGMA foreign_keys=ON'); con.executescript(SCHEMA)
 try:
  with con: yield con
 finally: con.close()

def _snapshot_payload(full:dict[str,Any],compact:dict[str,Any],kind:str,raw_id:str|None):
 text=str(compact.get('text') or full.get('text') or '')
 return {'snapshotSchemaVersion':'1.0','snapshotKind':kind,'sentence':text,'identity':{
  'analyzerVersion':compact.get('analyzerVersion') or 'unknown','engineVersion':compact.get('engineVersion'),
  'compactSchemaVersion':compact.get('schemaVersion'),'readerSpanSchemaVersion':compact.get('readerSpanSchemaVersion') or 'unknown',
  'readerCandidateSchemaVersion':compact.get('readerCandidateSchemaVersion'),'correctionRevision':compact.get('correctionRevision') or 'unknown',
  'dictionaryIdentity':full.get('dictionary_identity') or full.get('dictionaryIdentity')},
  'fullAnalysis':full,'compactAnalysis':compact,'rawBaselineSnapshotId':raw_id}

def save_snapshot(full_analysis,compact_analysis,kind='effective-baseline',raw_baseline_snapshot_id=None,db_path=None):
 payload=_snapshot_payload(full_analysis,compact_analysis,kind,raw_baseline_snapshot_id); digest=hashlib.sha256(_canonical(payload).encode()).hexdigest(); sid='snap-'+digest
 text=payload['sentence']; ident=payload['identity']; now=_now()
 with _lock,_db(db_path) as con:
  con.execute("""INSERT OR IGNORE INTO analyzer_snapshots VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
   sid,digest,kind,text,_fingerprint(text),ident['analyzerVersion'],ident.get('engineVersion'),ident.get('compactSchemaVersion'),ident['readerSpanSchemaVersion'],ident.get('readerCandidateSchemaVersion'),ident['correctionRevision'],_canonical(ident.get('dictionaryIdentity')), _canonical(full_analysis),_canonical(compact_analysis),raw_baseline_snapshot_id,now))
 return sid

def _overlap(a,b,c,d): return a<d and c<b

def create_annotation(*,correction_id,sentence,start,end,surface,action,display_role,split_offsets,target_spans,raw_snapshot_id,effective_snapshot_id,confidence='preference',note=None,provenance=None,revision_before=None,revision_after=None,db_path=None):
 selected=SourceRange(start=start,end=end,surface=surface); selected.validate_against(sentence)
 coverage=build_partial_coverage(sentence,selected).model_dump(mode='json'); assignment=stable_dataset_assignment(sentence,selected,action)
 now=_now(); ann='ann-'+str(uuid.uuid4()); supersedes=None
 with _lock,_db(db_path) as con:
  active=con.execute("SELECT * FROM teaching_annotations WHERE sentence_fingerprint=? AND status='active' ORDER BY created_at",(_fingerprint(sentence),)).fetchall()
  for row in active:
   if row['start']==start and row['end']==end:
    supersedes=row['annotation_id']
   elif _overlap(start,end,row['start'],row['end']):
    raise ValueError(f"Annotation range overlaps active annotation {row['annotation_id']}; retract or replace it first")
  if supersedes:
   con.execute("UPDATE teaching_annotations SET status='superseded',updated_at=? WHERE annotation_id=?",(now,supersedes))
   con.execute("INSERT INTO annotation_history VALUES(?,?,?,?,?,?,?,?)",('evt-'+str(uuid.uuid4()),supersedes,'superseded',now,revision_before,revision_after,ann,'same-range replacement'))
  con.execute("""INSERT INTO teaching_annotations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
   ann,correction_id,'active',sentence,_fingerprint(sentence),start,end,surface,action,display_role,_canonical(split_offsets),_canonical(target_spans),raw_snapshot_id,effective_snapshot_id,confidence,note,_canonical(coverage),_canonical(provenance or {}),_canonical({'derivationStatus':'pending'}),assignment.groupId,assignment.partition,supersedes,now,now))
  con.execute("INSERT INTO annotation_history VALUES(?,?,?,?,?,?,?,?)",('evt-'+str(uuid.uuid4()),ann,'saved',now,revision_before,revision_after,supersedes,note))
 return get_annotation(ann,db_path=db_path)

def get_annotation(annotation_id,db_path=None):
 with _lock,_db(db_path) as con:
  row=con.execute('SELECT * FROM teaching_annotations WHERE annotation_id=?',(annotation_id,)).fetchone()
  if not row: raise ValueError('Annotation not found')
  history=con.execute('SELECT * FROM annotation_history WHERE annotation_id=? ORDER BY event_at,event_id',(annotation_id,)).fetchall()
 result=dict(row)
 for key in ('split_offsets_json','target_spans_json','coverage_json','provenance_json','derived_outcome_json'): result[key[:-5]]=json.loads(result.pop(key))
 result['history']=[dict(x) for x in history]; return result

def find_annotation_by_correction(correction_id,include_inactive=True,db_path=None):
 with _lock,_db(db_path) as con:
  sql='SELECT annotation_id FROM teaching_annotations WHERE correction_id=?'+('' if include_inactive else " AND status='active'")+' ORDER BY created_at DESC LIMIT 1'
  row=con.execute(sql,(correction_id,)).fetchone()
 return get_annotation(row['annotation_id'],db_path=db_path) if row else None

def retract_for_correction(correction_id,revision_before=None,revision_after=None,db_path=None):
 now=_now()
 with _lock,_db(db_path) as con:
  row=con.execute("SELECT annotation_id FROM teaching_annotations WHERE correction_id=? AND status='active'",(correction_id,)).fetchone()
  if not row: return None
  ann=row['annotation_id']; con.execute("UPDATE teaching_annotations SET status='retracted',updated_at=? WHERE annotation_id=?",(now,ann))
  con.execute("INSERT INTO annotation_history VALUES(?,?,?,?,?,?,?,?)",('evt-'+str(uuid.uuid4()),ann,'retracted',now,revision_before,revision_after,None,'operational correction deactivated'))
 return get_annotation(ann,db_path=db_path)

def list_annotations(include_inactive=False,sentence=None,db_path=None):
 clauses=[]; values=[]
 if not include_inactive: clauses.append("status='active'")
 if sentence is not None: clauses.append('sentence_fingerprint=?'); values.append(_fingerprint(sentence))
 sql='SELECT annotation_id FROM teaching_annotations'+((' WHERE '+' AND '.join(clauses)) if clauses else '')+' ORDER BY created_at'
 with _lock,_db(db_path) as con: rows=con.execute(sql,values).fetchall()
 return [get_annotation(x['annotation_id'],db_path=db_path) for x in rows]

def corpus_status(db_path=None):
 with _lock,_db(db_path) as con:
  snaps=con.execute('SELECT COUNT(*) FROM analyzer_snapshots').fetchone()[0]
  counts={r['status']:r['n'] for r in con.execute('SELECT status,COUNT(*) n FROM teaching_annotations GROUP BY status')}
 return {'database':str(db_path or DB_PATH),'snapshotCount':snaps,'annotationCounts':counts,'activeAnnotationCount':counts.get('active',0)}



def preflight_annotation_range(sentence: str, start: int, end: int, db_path=None) -> dict[str, Any]:
    same = []
    conflicts = []
    with _lock, _db(db_path) as con:
        rows = con.execute(
            "SELECT annotation_id,start,end,surface FROM teaching_annotations "
            "WHERE sentence_fingerprint=? AND status='active' ORDER BY created_at",
            (_fingerprint(sentence),),
        ).fetchall()
    for row in rows:
        if row["start"] == start and row["end"] == end:
            same.append(row["annotation_id"])
        elif _overlap(start, end, row["start"], row["end"]):
            conflicts.append(dict(row))
    if conflicts:
        item = conflicts[0]
        raise ValueError(
            f"Selected range overlaps active annotation {item['annotation_id']} "
            f"at {item['start']}..{item['end']}; retract it before saving"
        )
    return {"sameRangeAnnotationIds": same, "conflicts": []}


def update_derived_outcome(annotation_id: str, post_snapshot_id: str, compact: dict[str, Any], start: int, end: int, db_path=None):
    selected = next((x for x in compact.get("readerSpans", []) if x.get("start") == start and x.get("end") == end), None)
    errors = [] if selected else ["corrected selected range not found as one post-correction Reader span"]
    outcome = {
        "postCorrectionSnapshotId": post_snapshot_id,
        "effectiveReaderSpans": compact.get("readerSpans") or [],
        "selectedSpan": selected,
        "knownLookupKey": selected.get("knownLookupKey") if selected else None,
        "frequencyLookupKey": selected.get("frequencyLookupKey") if selected else None,
        "countsForComprehension": selected.get("countsForComprehension") if selected else None,
        "showInNewWords": selected.get("showInNewWords") if selected else None,
        "eligibleForMining": selected.get("eligibleForMining") if selected else None,
        "presentationClass": selected.get("displayRole") if selected else None,
        "colourSource": selected.get("colorPolicy") if selected else None,
        "unknownColorPolicy": selected.get("unknownColorPolicy") if selected else None,
        "derivationStatus": "complete" if selected else "partial",
        "derivationErrors": errors,
    }
    now = _now()
    with _lock, _db(db_path) as con:
        cursor = con.execute(
            "UPDATE teaching_annotations SET derived_outcome_json=?,updated_at=? WHERE annotation_id=?",
            (_canonical(outcome), now, annotation_id),
        )
    if cursor.rowcount != 1:
        raise ValueError("Annotation not found")
    return get_annotation(annotation_id, db_path=db_path)


def integrity_report(corrections: list[dict[str, Any]], db_path=None) -> dict[str, Any]:
    annotations = list_annotations(include_inactive=True, db_path=db_path)
    correction_by_id = {x.get("correction_id"): x for x in corrections}
    active_annotations = [x for x in annotations if x["status"] == "active"]
    issues = []
    for ann in active_annotations:
        correction = correction_by_id.get(ann["correction_id"])
        if correction is None:
            issues.append({"code": "ACTIVE_ANNOTATION_MISSING_CORRECTION", "annotationId": ann["annotation_id"]})
        elif correction.get("deactivated_at") is not None:
            issues.append({"code": "ACTIVE_ANNOTATION_INACTIVE_CORRECTION", "annotationId": ann["annotation_id"], "correctionId": ann["correction_id"]})
    active_correction_ids = {x.get("correction_id") for x in corrections if x.get("deactivated_at") is None}
    active_annotation_correction_ids = {x["correction_id"] for x in active_annotations}
    for correction_id in sorted(active_correction_ids - active_annotation_correction_ids):
        issues.append({"code": "ACTIVE_CORRECTION_MISSING_ANNOTATION", "correctionId": correction_id})
    with _lock, _db(db_path) as con:
        missing_snapshots = con.execute(
            "SELECT annotation_id FROM teaching_annotations WHERE "
            "raw_baseline_snapshot_id NOT IN (SELECT snapshot_id FROM analyzer_snapshots) OR "
            "effective_baseline_snapshot_id NOT IN (SELECT snapshot_id FROM analyzer_snapshots)"
        ).fetchall()
    for row in missing_snapshots:
        issues.append({"code": "ANNOTATION_MISSING_SNAPSHOT", "annotationId": row["annotation_id"]})
    return {"ok": not issues, "issueCount": len(issues), "issues": issues, "corpus": corpus_status(db_path)}
