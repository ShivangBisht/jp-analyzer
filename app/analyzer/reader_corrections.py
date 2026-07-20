from __future__ import annotations
import hashlib, json, sqlite3, threading, uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "reader_corrections.sqlite3"
_lock = threading.RLock()
_ALLOWED_ROLES = {"lexical", "lexical-compound", "name", "learnable-grammar", "function", "punctuation", "unresolved"}
_PUNCTUATION = set("、。！？!?「」『』（）()……─―～")

SCHEMA = """
CREATE TABLE IF NOT EXISTS reader_corrections(
 correction_id TEXT PRIMARY KEY, sentence_text TEXT NOT NULL, sentence_fingerprint TEXT NOT NULL,
 start INTEGER NOT NULL, end INTEGER NOT NULL, surface TEXT NOT NULL, action TEXT NOT NULL,
 display_role TEXT NOT NULL, headword TEXT, known_lookup_key TEXT, frequency_lookup_key TEXT,
 grammar_id TEXT, unknown_color_policy TEXT, scope TEXT NOT NULL,
 analyzer_version TEXT NOT NULL, reader_span_schema_version TEXT NOT NULL,
 original_spans_json TEXT NOT NULL, feature_snapshot_json TEXT NOT NULL,
 created_at TEXT NOT NULL, deactivated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_reader_corrections_occurrence
 ON reader_corrections(sentence_fingerprint,start,end,deactivated_at);
"""

def sentence_fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@contextmanager
def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con=sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    try:
        with con: yield con
    finally: con.close()

def validate_request(data: dict[str, Any]) -> dict[str, Any]:
    text=str(data.get("sentence") or "")
    start, end=data.get("start"), data.get("end")
    surface=str(data.get("surface") or "")
    role=str(data.get("displayRole") or "")
    if data.get("scope", "occurrence") != "occurrence": raise ValueError("Phase 2.2A supports occurrence scope only")
    if not isinstance(start,int) or not isinstance(end,int) or not (0 <= start < end <= len(text)): raise ValueError("Invalid correction range")
    if text[start:end] != surface: raise ValueError("Correction surface does not match sentence range")
    if any(ch in _PUNCTUATION for ch in surface): raise ValueError("Correction cannot cross or include protected punctuation")
    if role not in _ALLOWED_ROLES: raise ValueError("Unknown displayRole")
    lookup=data.get("knownLookupKey") or data.get("headword")
    frequency=data.get("frequencyLookupKey") or lookup
    if role in {"lexical","lexical-compound",} and (not lookup or not frequency): raise ValueError("Lexical corrections require lookup keys")
    if role == "learnable-grammar" and not data.get("grammarId"): raise ValueError("Grammar corrections require grammarId")
    return {**data, "sentence":text, "start":start, "end":end, "surface":surface, "displayRole":role,
            "scope":"occurrence", "knownLookupKey":lookup, "frequencyLookupKey":frequency}

def corrected_span(data: dict[str, Any], correction_id: str | None=None) -> dict[str, Any]:
    role=data["displayRole"]
    color={"lexical":"known-or-frequency","lexical-compound":"known-or-frequency","name":"name","learnable-grammar":"grammar","function":"muted","punctuation":"neutral","unresolved":"neutral"}[role]
    return {"start":data["start"],"end":data["end"],"surface":data["surface"],"displayRole":role,
      "lexicalType": data.get("lexicalType") or ("compound" if role=="lexical-compound" else "numeric" if role=="lexical-compound" else "term" if role=="lexical" else None),
      "colorPolicy":color,"unknownColorPolicy":data.get("unknownColorPolicy") or ("frequency" if role in {"lexical","lexical-compound"} else None),
      "knownLookupKey":data.get("knownLookupKey"),"frequencyLookupKey":data.get("frequencyLookupKey"),
      "headword":data.get("headword"),"grammarId":data.get("grammarId"),"confidence":1.0,
      "countsForComprehension":role in {"lexical","lexical-compound",},
      "showInNewWords":role in {"lexical","lexical-compound",},
      "eligibleForMining":role in {"lexical","lexical-compound","name","learnable-grammar"},
      "sourceSpanIds":[],"sourceLayer":"user-correction","projectionStatus":"user-corrected-preview" if not correction_id else "user-corrected",
      "correctionId":correction_id,"correctionScope":"occurrence"}

def preview(data: dict[str, Any], baseline: list[dict[str, Any]]) -> dict[str, Any]:
    data=validate_request(data); a,b=data["start"],data["end"]
    if not baseline: raise ValueError("baselineReaderSpans is required")
    left=[x for x in baseline if x["end"] <= a]; right=[x for x in baseline if x["start"] >= b]
    overlaps=[x for x in baseline if x["start"] < b and a < x["end"]]
    if not overlaps or min(x["start"] for x in overlaps) != a or max(x["end"] for x in overlaps) != b:
        raise ValueError("Correction range must align to complete existing reader spans")
    spans=left+[corrected_span(data)]+right
    from .reader_projection import validate_reader_spans
    validate_reader_spans(data["sentence"], spans)
    return {"sentenceFingerprint":sentence_fingerprint(data["sentence"]),"originalReaderSpans":baseline,"previewReaderSpans":spans,"saved":False}

def save(data: dict[str, Any], baseline: list[dict[str, Any]], analyzer_version: str, schema_version: str) -> dict[str, Any]:
    p=preview(data, baseline); data=validate_request(data); cid=str(uuid.uuid4()); now=datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        con.execute("INSERT INTO reader_corrections VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL)",(
          cid,data["sentence"],sentence_fingerprint(data["sentence"]),data["start"],data["end"],data["surface"],data.get("action","replace-reader-range"),data["displayRole"],data.get("headword"),data.get("knownLookupKey"),data.get("frequencyLookupKey"),data.get("grammarId"),data.get("unknownColorPolicy"),"occurrence",analyzer_version,schema_version,json.dumps(baseline,ensure_ascii=False),json.dumps(data.get("featureSnapshot") or {},ensure_ascii=False),now))
    p["saved"]=True; p["correctionId"]=cid; p["previewReaderSpans"]=[corrected_span(data,cid) if x.get("projectionStatus")=="user-corrected-preview" else x for x in p["previewReaderSpans"]]
    return p

def list_corrections(include_inactive: bool=False) -> list[dict[str, Any]]:
    with _lock, _db() as con:
        rows=con.execute("SELECT * FROM reader_corrections"+("" if include_inactive else " WHERE deactivated_at IS NULL")+" ORDER BY created_at").fetchall()
    return [dict(x) for x in rows]

def deactivate(correction_id: str) -> dict[str, Any]:
    now=datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        cur=con.execute("UPDATE reader_corrections SET deactivated_at=? WHERE correction_id=? AND deactivated_at IS NULL",(now,correction_id))
    if cur.rowcount != 1: raise ValueError("Active correction not found")
    return {"correctionId":correction_id,"active":False,"deactivatedAt":now}
