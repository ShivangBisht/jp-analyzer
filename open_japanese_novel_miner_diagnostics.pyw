from __future__ import annotations
import html, json, os, webbrowser
from datetime import datetime, timezone
from pathlib import Path
runtime = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "JapaneseNovelMiner"
status_path = runtime / "startup-status.json"
report_path = runtime / "diagnostics.html"
try:
    status = json.loads(status_path.read_text(encoding="utf-8-sig"))
except FileNotFoundError:
    status = {"overall_status":"unavailable","components":{},"problems":[{"code":"NO_STATUS","message":"No launcher status has been recorded."}]}
except (OSError, json.JSONDecodeError) as error:
    status = {"overall_status":"unavailable","components":{},"problems":[{"code":"STATUS_READ_FAILED","message":str(error)}]}
components = status.get("components") if isinstance(status.get("components"), dict) else {}
problems = status.get("problems") if isinstance(status.get("problems"), list) else []
rows = "".join("<tr><th>%s</th><td>%s</td><td>%s</td></tr>" % (html.escape(str(name)), html.escape(str((value or {}).get("state","unknown"))), html.escape(str((value or {}).get("detail") or ""))) for name,value in components.items())
issues = "".join("<li><code>%s</code> %s</li>" % (html.escape(str(item.get("code","UNKNOWN"))), html.escape(str(item.get("message","")))) for item in problems if isinstance(item,dict)) or "<li>No reported problems.</li>"
log_dir = runtime / "logs"
logs = "".join("<li>%s (%s bytes)</li>" % (html.escape(path.name), path.stat().st_size) for path in sorted(log_dir.glob("*.log"))) if log_dir.exists() else "<li>No logs found.</li>"
page = """<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="10"><title>Japanese Novel Miner Diagnostics</title><style>body{font-family:Segoe UI,sans-serif;background:#0d1117;color:#c9d1d9;max-width:980px;margin:32px auto;padding:0 20px}section{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;margin:14px 0}table{width:100%%;border-collapse:collapse}th,td{text-align:left;padding:9px;border-bottom:1px solid #30363d}code{color:#79c0ff}</style><h1>Japanese Novel Miner Diagnostics</h1><p>Refreshes every 10 seconds. Generated %s.</p><section><h2>Application: %s</h2><p>Status: <code>%s</code></p><p>Logs: <code>%s</code></p></section><section><h2>Components</h2><table>%s</table></section><section><h2>Problems</h2><ul>%s</ul></section><section><h2>Log files</h2><ul>%s</ul></section>""" % (datetime.now(timezone.utc).isoformat(), html.escape(str(status.get("overall_status","unknown"))), html.escape(str(status_path)), html.escape(str(log_dir)), rows or "<tr><td>No component status available.</td></tr>", issues, logs)
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(page, encoding="utf-8")
webbrowser.open(report_path.as_uri(), new=1, autoraise=True)
