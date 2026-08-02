from __future__ import annotations
import os
import signal
import sys
import time
import uuid
from pathlib import Path
from .config import load_config
from .diagnostics import write_snapshot
from .health import probe, wait_for
from .instance_lock import InstanceLock
from .models import ComponentStatus, Problem, StartupSnapshot
from .process_manager import ProcessManager
from .windows import local_app_data_dir, open_application

class ApplicationSupervisor:
    def __init__(self, analyzer_repo: Path, config_path: Path | None = None):
        self.config = load_config(analyzer_repo, config_path)
        self.instance_id = str(uuid.uuid4()); self.runtime_dir = local_app_data_dir()
        self.status_path = self.runtime_dir / "startup-status.json"
        self.lock = InstanceLock(self.runtime_dir / "launcher.lock", self.instance_id)
        self.processes = ProcessManager(self.runtime_dir / "logs")
        self.snapshot = StartupSnapshot(launcher_instance_id=self.instance_id)
        for name, required in (("analyzer", True), ("dictionary", True), ("kwja", True), ("frontend", True), ("voicevox", False), ("ankiConnect", False)):
            self.snapshot.components[name] = ComponentStatus(name, required)
        self.stopping = False
    def save(self) -> None:
        required = [x for x in self.snapshot.components.values() if x.required]
        self.snapshot.overall_status = "failed" if any(x.state == "failed" for x in required) else ("ready" if all(x.state == "ready" for x in required) else "starting")
        write_snapshot(self.status_path, self.snapshot.to_dict())
    def fail(self, code: str, message: str, component: str, detail: str | None = None) -> bool:
        self.snapshot.problems.append(Problem(code, message, component, True, detail)); item = self.snapshot.components[component]
        item.state, item.detail = "failed", message; self.save(); return False
    def validate(self) -> bool:
        valid = True
        for passed, code, message, component in (
            (self.config.analyzer_repo.is_dir(), "ANALYZER_REPO_MISSING", "JP Analyzer repository was not found.", "analyzer"),
            (self.config.analyzer_python.is_file(), "ANALYZER_PYTHON_MISSING", "JP Analyzer Python executable was not found.", "analyzer"),
            (self.config.frontend_repo.is_dir(), "FRONTEND_REPO_MISSING", "Novel Audio Miner repository was not found.", "frontend")):
            if not passed: self.fail(code, message, component); valid = False
        if not self.config.kwja_executable or not self.config.kwja_executable.is_file():
            self.fail("KWJA_NOT_CONFIGURED", "KWJA executable was not found.", "kwja"); valid = False
        else:
            self.snapshot.components["kwja"].state = "ready"; self.snapshot.components["kwja"].detail = str(self.config.kwja_executable)
        self.save(); return valid
    def apply_health(self, health: dict) -> None:
        data = health.get("dictionary") or health.get("dictionaryStatus") or {}
        item = self.snapshot.components["dictionary"]
        if data.get("ready") and data.get("registryConsistent", True) and not data.get("recoveryRequired", False):
            item.state = "ready"; item.detail = f"{data.get('entryCount', 0)} entries; {data.get('installedDictionaryCount', data.get('dictionaryCount', 0))} dictionaries."
        else:
            item.state = "failed"; item.detail = "Dictionary is not ready or requires recovery."
            self.snapshot.problems.append(Problem("DICTIONARY_NOT_READY", item.detail, "dictionary", True))
    def ensure_analyzer(self) -> bool:
        item = self.snapshot.components["analyzer"]; item.url = self.config.analyzer_url
        result = probe(self.config.analyzer_url + "/health")
        if result.ok and isinstance(result.body, dict):
            item.state, item.detail = "ready", "Reused running analyzer."; self.apply_health(result.body); self.save(); return True
        item.state = "starting"; self.save(); env = dict(os.environ); env["KWJA_EXE"] = str(self.config.kwja_executable)
        command = [str(self.config.analyzer_python), "-m", "uvicorn", "app.analyzer.service:app", "--host", self.config.analyzer_host, "--port", str(self.config.analyzer_port)]
        owned = self.processes.start("jp-analyzer", command, self.config.analyzer_repo, env); item.pid = owned.process.pid
        result = wait_for(self.config.analyzer_url + "/health", self.config.analyzer_timeout_seconds, owned.process)
        if not result.ok or not isinstance(result.body, dict): return self.fail("ANALYZER_START_FAILED", "JP Analyzer did not become ready.", "analyzer", result.error)
        item.state, item.detail = "ready", "Started by launcher."; self.apply_health(result.body); self.save(); return True
    def ensure_frontend(self) -> bool:
        item = self.snapshot.components["frontend"]; item.url = self.config.frontend_url
        if probe(self.config.frontend_url, accept="text/html,*/*;q=0.8").ok: item.state, item.detail = "ready", "Reused running frontend."; self.save(); return True
        item.state = "starting"; self.save(); owned = self.processes.start("novel-audio-miner", list(self.config.frontend_command), self.config.frontend_repo, dict(os.environ)); item.pid = owned.process.pid
        result = wait_for(self.config.frontend_url, self.config.frontend_timeout_seconds, owned.process, accept="text/html,*/*;q=0.8")
        if not result.ok: return self.fail("FRONTEND_START_FAILED", "Novel Audio Miner did not become ready.", "frontend", result.error)
        item.state, item.detail = "ready", "Started by launcher."; self.save(); return True
    def probe_optional(self) -> None:
        for name, url in (("voicevox", "http://127.0.0.1:50021/version"), ("ankiConnect", "http://127.0.0.1:8765")):
            result = probe(url); item = self.snapshot.components[name]; item.url = url; item.state = "ready" if result.ok else "degraded"; item.detail = "Available." if result.ok else "Optional service unavailable."
        self.save()
    def run(self) -> int:
        self.lock.acquire()
        try:
            signal.signal(signal.SIGINT, lambda *_: setattr(self, "stopping", True)); signal.signal(signal.SIGTERM, lambda *_: setattr(self, "stopping", True)); self.save()
            if not self.validate() or not self.ensure_analyzer() or not self.ensure_frontend(): return 1
            self.probe_optional()
            if self.config.open_browser: open_application(self.config.frontend_url)
            while not self.stopping:
                time.sleep(1)
                for item in self.processes.owned:
                    if item.process.poll() is not None: return self.fail("CHILD_EXITED", f"{item.name} exited unexpectedly.", "analyzer" if item.name == "jp-analyzer" else "frontend", str(item.process.returncode))
            return 0
        finally:
            self.processes.stop_all(); self.lock.release(); self.save()

def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    config = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    return ApplicationSupervisor(repo, config).run()
if __name__ == "__main__": raise SystemExit(main())
