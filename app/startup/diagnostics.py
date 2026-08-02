from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

def write_snapshot(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"capturedAt": datetime.now(timezone.utc).isoformat(), **value}
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)
