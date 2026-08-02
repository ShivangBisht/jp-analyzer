from __future__ import annotations
import json, os, time
from datetime import datetime, timezone
from pathlib import Path
from app.startup.discovery import tcp_port_open
from app.startup.ownership import stop_manifest_services
runtime = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "JapaneseNovelMiner"
runtime.mkdir(parents=True, exist_ok=True)
request = runtime / "shutdown.request"; temp = request.with_suffix(".tmp")
temp.write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8"); temp.replace(request)
deadline = time.monotonic() + 8
while time.monotonic() < deadline:
    if not tcp_port_open("127.0.0.1", 8766) and not tcp_port_open("127.0.0.1", 5173): break
    time.sleep(.5)
normal = not tcp_port_open("127.0.0.1", 8766) and not tcp_port_open("127.0.0.1", 5173)
summary = {"normalShutdown": normal, "fallback": None}
if not normal:
    summary["fallback"] = stop_manifest_services(runtime / "owned-processes.json")
    time.sleep(1)
(runtime / "shutdown-result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
