from __future__ import annotations
import json
import os
from pathlib import Path

class InstanceLockError(RuntimeError): pass

class InstanceLock:
    def __init__(self, path: Path, instance_id: str):
        self.path, self.instance_id, self._owned = path, instance_id, False
    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                pid = int(json.loads(self.path.read_text(encoding="utf-8")).get("pid", 0))
                if pid and _pid_exists(pid):
                    raise InstanceLockError(f"Japanese Novel Miner is already running (PID {pid}).")
            except (ValueError, OSError, json.JSONDecodeError): pass
            self.path.unlink(missing_ok=True)
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump({"pid": os.getpid(), "instanceId": self.instance_id}, handle)
        self._owned = True
    def release(self) -> None:
        if self._owned: self.path.unlink(missing_ok=True); self._owned = False

def _pid_exists(pid: int) -> bool:
    try: os.kill(pid, 0); return True
    except OSError: return False
