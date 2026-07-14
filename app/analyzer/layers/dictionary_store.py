from __future__ import annotations
import json, sqlite3, threading, uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "phase8_analysis_lexicon.sqlite3"
_lock = threading.RLock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_sessions(sync_id TEXT PRIMARY KEY, expected_entries INTEGER DEFAULT 0, received_entries INTEGER DEFAULT 0, dictionary_count INTEGER DEFAULT 0, status TEXT DEFAULT 'receiving');
CREATE TABLE IF NOT EXISTS staging_entries(sync_id TEXT NOT NULL, dictionary_id TEXT NOT NULL, dictionary_title TEXT NOT NULL, dictionary_type TEXT NOT NULL, dictionary_priority INTEGER NOT NULL DEFAULT 9999, term TEXT NOT NULL, reading TEXT NOT NULL DEFAULT '', tags_json TEXT NOT NULL DEFAULT '[]', rules_json TEXT NOT NULL DEFAULT '[]', score REAL NOT NULL DEFAULT 0, sequence TEXT, name_type TEXT NOT NULL DEFAULT '', grammar_type TEXT NOT NULL DEFAULT '', expression_type TEXT NOT NULL DEFAULT '');
CREATE INDEX IF NOT EXISTS idx_staging_sync ON staging_entries(sync_id);
CREATE TABLE IF NOT EXISTS lexicon_entries(id INTEGER PRIMARY KEY AUTOINCREMENT, dictionary_id TEXT NOT NULL, dictionary_title TEXT NOT NULL, dictionary_type TEXT NOT NULL, dictionary_priority INTEGER NOT NULL DEFAULT 9999, term TEXT NOT NULL, reading TEXT NOT NULL DEFAULT '', tags_json TEXT NOT NULL DEFAULT '[]', rules_json TEXT NOT NULL DEFAULT '[]', score REAL NOT NULL DEFAULT 0, sequence TEXT, name_type TEXT NOT NULL DEFAULT '', grammar_type TEXT NOT NULL DEFAULT '', expression_type TEXT NOT NULL DEFAULT '');
CREATE INDEX IF NOT EXISTS idx_lexicon_term ON lexicon_entries(term);
CREATE INDEX IF NOT EXISTS idx_lexicon_reading ON lexicon_entries(reading);
CREATE INDEX IF NOT EXISTS idx_lexicon_type ON lexicon_entries(dictionary_type);
CREATE TABLE IF NOT EXISTS lexicon_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.executescript(SCHEMA)
    return con

@contextmanager
def _db():
    """Commit/rollback and always release the SQLite file handle."""
    con = _connect()
    try:
        with con:
            yield con
    finally:
        con.close()

def start_sync(expected_entries: int = 0, dictionary_count: int = 0) -> dict[str, Any]:
    sync_id = str(uuid.uuid4())
    with _lock, _db() as con:
        con.execute("DELETE FROM staging_entries")
        con.execute("DELETE FROM sync_sessions")
        con.execute("INSERT INTO sync_sessions(sync_id,expected_entries,dictionary_count) VALUES(?,?,?)", (sync_id, expected_entries, dictionary_count))
    return {"syncId": sync_id, "status": "receiving", "database": str(DB_PATH)}

def add_batch(sync_id: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    def j(value):
        return json.dumps(value if isinstance(value, list) else ([value] if value else []), ensure_ascii=False)
    rows = []
    for entry in entries:
        term = str(entry.get("term") or "").strip()
        if not term:
            continue
        rows.append((sync_id, str(entry.get("dictionaryId") or ""), str(entry.get("dictionaryTitle") or "unknown"), str(entry.get("dictionaryType") or "term"), int(entry.get("dictionaryPriority") or 9999), term, str(entry.get("reading") or ""), j(entry.get("tags")), j(entry.get("rules")), float(entry.get("score") or 0), None if entry.get("sequence") is None else str(entry.get("sequence")), str(entry.get("nameType") or ""), str(entry.get("grammarType") or ""), str(entry.get("expressionType") or "")))
    with _lock, _db() as con:
        session = con.execute("SELECT status FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone()
        if not session or session["status"] != "receiving":
            raise ValueError("Unknown or inactive sync session")
        con.executemany("INSERT INTO staging_entries VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        con.execute("UPDATE sync_sessions SET received_entries=received_entries+? WHERE sync_id=?", (len(rows), sync_id))
        received = con.execute("SELECT received_entries FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone()[0]
    return {"syncId": sync_id, "accepted": len(rows), "received": received}

def finish_sync(sync_id: str) -> dict[str, Any]:
    with _lock, _db() as con:
        if not con.execute("SELECT 1 FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone():
            raise ValueError("Unknown sync session")
        con.execute("DELETE FROM lexicon_entries")
        con.execute("""INSERT INTO lexicon_entries(dictionary_id,dictionary_title,dictionary_type,dictionary_priority,term,reading,tags_json,rules_json,score,sequence,name_type,grammar_type,expression_type) SELECT dictionary_id,dictionary_title,dictionary_type,dictionary_priority,term,reading,tags_json,rules_json,score,sequence,name_type,grammar_type,expression_type FROM staging_entries WHERE sync_id=?""", (sync_id,))
        count = con.execute("SELECT COUNT(*) FROM lexicon_entries").fetchone()[0]
        dictionaries = con.execute("SELECT COUNT(DISTINCT dictionary_id) FROM lexicon_entries").fetchone()[0]
        con.execute("DELETE FROM lexicon_meta")
        con.executemany("INSERT INTO lexicon_meta(key,value) VALUES(?,?)", [("last_sync_id", sync_id), ("entry_count", str(count)), ("dictionary_count", str(dictionaries))])
        con.execute("UPDATE sync_sessions SET status='complete' WHERE sync_id=?", (sync_id,))
        con.execute("DELETE FROM staging_entries WHERE sync_id=?", (sync_id,))
    return {"syncId": sync_id, "status": "complete", "entryCount": count, "dictionaryCount": dictionaries}

def status() -> dict[str, Any]:
    with _lock, _db() as con:
        count = con.execute("SELECT COUNT(*) FROM lexicon_entries").fetchone()[0]
        dictionaries = con.execute("SELECT COUNT(DISTINCT dictionary_id) FROM lexicon_entries").fetchone()[0]
        types = {r["dictionary_type"]: r["n"] for r in con.execute("SELECT dictionary_type,COUNT(*) n FROM lexicon_entries GROUP BY dictionary_type")}
        last = con.execute("SELECT value FROM lexicon_meta WHERE key='last_sync_id'").fetchone()
    return {"ready": count > 0, "entryCount": count, "dictionaryCount": dictionaries, "typeCounts": types, "lastSyncId": last[0] if last else None, "database": str(DB_PATH)}

def clear() -> dict[str, Any]:
    with _lock, _db() as con:
        for table in ("lexicon_entries", "staging_entries", "sync_sessions", "lexicon_meta"):
            con.execute(f"DELETE FROM {table}")
    return status()
