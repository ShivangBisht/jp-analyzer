from __future__ import annotations
import json, os, subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from .health import probe
MANIFEST_SCHEMA = "JapaneseNovelMinerOwnedProcesses.v1"
@dataclass
class Identity:
    pid: int
    created: str | None
    command_line: str | None
@dataclass
class Service:
    name: str
    wrapper_pid: int
    listener_pid: int | None
    port: int
    repository: str
    identity_url: str
    kind: str
    listener_created: str | None = None

def _ps(script):
    if os.name != "nt": return None
    result = subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",script], capture_output=True, text=True, check=False, creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
    if result.returncode or not result.stdout.strip(): return None
    try: return json.loads(result.stdout)
    except json.JSONDecodeError: return None

def identity(pid):
    if not pid: return None
    value = _ps(f"$p=Get-CimInstance Win32_Process -Filter 'ProcessId = {int(pid)}' -ErrorAction SilentlyContinue;if($p){{$p|Select-Object ProcessId,CommandLine,CreationDate|ConvertTo-Json -Compress}}")
    if not isinstance(value, dict): return None
    return Identity(int(value.get("ProcessId") or pid), str(value.get("CreationDate")) if value.get("CreationDate") else None, value.get("CommandLine"))

def listener_pid(port):
    value = _ps(f"$c=Get-NetTCPConnection -LocalAddress '127.0.0.1' -LocalPort {int(port)} -State Listen -ErrorAction SilentlyContinue|Select-Object -First 1;if($c){{$c.OwningProcess|ConvertTo-Json -Compress}}")
    try: return int(value)
    except (TypeError, ValueError): return None

def service_ok(
    kind,
    url,
    *,
    timeout=10.0,
):
    result = probe(
        url,
        timeout=timeout,
    )

    if not result.ok:
        return False

    if not isinstance(result.body, dict):
        return False

    if kind == "analyzer":
        dictionary = (
            result.body.get("dictionary")
            or result.body.get("dictionaryStatus")
        )

        return isinstance(dictionary, dict)

    return (
        kind == "frontend"
        and result.body.get("application")
        == "JapaneseNovelMiner"
    )

def safe_listener(service):
    pid = listener_pid(service.port) or service.listener_pid
    current = identity(pid)
    if current is None: return None
    if service.listener_created and current.created and service.listener_created != current.created: return None
    command = (current.command_line or "").casefold()
    if service.kind == "analyzer": valid_command = "uvicorn" in command and "app.analyzer.service:app" in command
    else: valid_command = "vite" in command and service.repository.casefold() in command
    return current if valid_command and service_ok(service.kind, service.identity_url) else None

def write_manifest(path, instance_id, supervisor_pid, services):
    payload = {"schema": MANIFEST_SCHEMA, "capturedAt": datetime.now(timezone.utc).isoformat(), "launcherInstanceId": instance_id, "supervisorPid": supervisor_pid, "services": {item.name: asdict(item) for item in services}}
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp"); temp.write_text(json.dumps(payload, indent=2), encoding="utf-8"); temp.replace(path)

def load_services(path):
    try: payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError): return None
    if payload.get("schema") != MANIFEST_SCHEMA: return None
    output = []
    for item in (payload.get("services") or {}).values():
        try: output.append(Service(**item))
        except (TypeError, ValueError): pass
    return output

def stop_manifest_services(path):
    services = load_services(path); summary = {"stopped": [], "alreadyStopped": [], "refused": []}
    if services is None: summary["refused"].append("ownership manifest is missing or invalid"); return summary
    for service in services:
        current = safe_listener(service)
        if current is None:
            if listener_pid(service.port) is None: summary["alreadyStopped"].append(service.name)
            else: summary["refused"].append(f"{service.name}: ownership could not be verified")
            continue
        result = subprocess.run(["taskkill","/PID",str(current.pid),"/T","/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
        (summary["stopped"] if result.returncode == 0 else summary["refused"]).append(service.name if result.returncode == 0 else f"{service.name}: taskkill failed")
    return summary
