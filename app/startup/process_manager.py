from __future__ import annotations
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

@dataclass
class OwnedProcess:
    name: str
    process: subprocess.Popen
    stdout_path: Path
    stderr_path: Path

class ProcessManager:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir; self.log_dir.mkdir(parents=True, exist_ok=True)
        self.owned: list[OwnedProcess] = []; self.handles = []
    def start(self, name: str, command: list[str], cwd: Path, env: dict[str, str]) -> OwnedProcess:
        out_path, err_path = self.log_dir / f"{name}.stdout.log", self.log_dir / f"{name}.stderr.log"
        out, err = out_path.open("a", encoding="utf-8", buffering=1), err_path.open("a", encoding="utf-8", buffering=1)
        self.handles.extend([out, err])
        flags = (subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0
        process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err, creationflags=flags, text=True)
        owned = OwnedProcess(name, process, out_path, err_path); self.owned.append(owned); return owned
    def _stop_owned_process_tree(self, item: OwnedProcess) -> None:
        if os.name == "nt":
            # npm.cmd starts Vite as a descendant node.exe process. Terminating
            # only the wrapper leaves that descendant listening on port 5173.
            # taskkill /T is restricted to the PID created and owned here.
            subprocess.run(
                ["taskkill", "/PID", str(item.process.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            try:
                item.process.wait(timeout=5)
            except (subprocess.TimeoutExpired, OSError):
                pass
            return

        if item.process.poll() is None:
            item.process.terminate()
            try:
                item.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                item.process.kill()
                item.process.wait(timeout=5)

    def stop_all(self) -> None:
        for item in reversed(self.owned):
            self._stop_owned_process_tree(item)
        for handle in self.handles:
            handle.close()
        self.owned.clear()
        self.handles.clear()
