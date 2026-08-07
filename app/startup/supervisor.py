from __future__ import annotations
import os
import signal
import sys
import time
import uuid
from pathlib import Path
from .config import initialize_local_config, load_config
from .diagnostics import write_snapshot
from .discovery import tcp_port_open
from .health import probe, wait_for
from .instance_lock import InstanceLock
from .models import ComponentStatus, Problem, StartupSnapshot
from .ownership import Service, identity, listener_pid, service_ok, write_manifest
from .process_manager import ProcessManager
from .windows import local_app_data_dir, open_application

FRONTEND_IDENTITY = "JapaneseNovelMiner"

def shutdown_requested(path: Path) -> bool:
    return path.is_file()

def _compatible_analyzer(body):
    return isinstance(body, dict) and isinstance(body.get("dictionary") or body.get("dictionaryStatus"), dict)

def _compatible_analyzer_liveness(body):
    return (
        isinstance(body, dict)
        and body.get("status") == "alive"
        and body.get("service") == "jp-analyzer"
    )

def _compatible_frontend(body):
    return isinstance(body, dict) and body.get("application") == FRONTEND_IDENTITY

class ApplicationSupervisor:
    def __init__(self, analyzer_repo: Path, config_path: Path | None = None):
        self.config = load_config(analyzer_repo, config_path)
        if config_path is None and self.config.config_path is None:
            created = initialize_local_config(self.config)
            if created: self.config = load_config(analyzer_repo, created)
        self.instance_id = str(uuid.uuid4()); self.runtime_dir = local_app_data_dir()
        self.status_path = self.runtime_dir / "startup-status.json"
        self.manifest_path = self.runtime_dir / "owned-processes.json"
        self.shutdown_request_path = self.runtime_dir / "shutdown.request"
        self.shutdown_request_path.unlink(missing_ok=True)
        self.lock = InstanceLock(self.runtime_dir / "launcher.lock", self.instance_id)
        self.processes = ProcessManager(self.runtime_dir / "logs")
        self.services = {}
        self.snapshot = StartupSnapshot(launcher_instance_id=self.instance_id, diagnostics={**self.config.diagnostics(), "runtimeDirectory": str(self.runtime_dir), "statusFile": str(self.status_path), "logDirectory": str(self.runtime_dir / "logs")})
        for name, required in (("analyzer", True), ("dictionary", True), ("kwja", True), ("frontend", True), ("voicevox", False), ("ankiConnect", False)):
            self.snapshot.components[name] = ComponentStatus(name, required)
        self.stopping = False
    def save(self) -> None:
        required = [
            item
            for item in self.snapshot.components.values()
            if item.required
        ]
        shutdown_reason = self.snapshot.diagnostics.get("shutdownReason")
        if shutdown_reason:
            self.snapshot.overall_status = "stopped"
        elif any(item.state == "failed" for item in required):
            self.snapshot.overall_status = "failed"
        elif all(item.state == "ready" for item in required):
            self.snapshot.overall_status = "ready"
        else:
            self.snapshot.overall_status = "starting"
        write_snapshot(self.status_path, self.snapshot.to_dict())

    def finalize_shutdown_status(self, reason: str) -> None:
        for item in self.snapshot.components.values():
            item.state = "stopped"
            item.pid = None
        self.snapshot.diagnostics["shutdownReason"] = reason
        self.save()
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
            self.snapshot.components["kwja"].state = "starting"; self.snapshot.components["kwja"].detail = "KWJA is configured; background warm-up has not completed."
        self.save(); return valid
    def apply_health(self, health: dict) -> None:
        data = health.get("dictionary") or health.get("dictionaryStatus") or {}
        item = self.snapshot.components["dictionary"]
        if data.get("ready") and data.get("registryConsistent", True) and not data.get("recoveryRequired", False):
            item.state = "ready"; item.detail = f"{data.get('entryCount', 0)} entries; {data.get('installedDictionaryCount', data.get('dictionaryCount', 0))} dictionaries."
        else:
            item.state = "failed"; item.detail = "Dictionary is not ready or requires recovery."
            self.snapshot.problems.append(Problem("DICTIONARY_NOT_READY", item.detail, "dictionary", True))
        kwja = health.get("kwja") or {}
        warmup = kwja.get("warmup") or {}
        runtime = kwja.get("runtime") or {}
        kwja_item = self.snapshot.components["kwja"]
        if kwja.get("executionMode") == "fresh":
            kwja_item.state = "ready"; kwja_item.detail = "KWJA fresh-process mode is active."
        elif warmup.get("state") == "ready" and runtime.get("running"):
            kwja_item.state = "ready"; kwja_item.detail = "Persistent KWJA is warm and ready."
        elif warmup.get("state") == "failed":
            kwja_item.state = "degraded"; kwja_item.detail = "Persistent warm-up failed; bounded recovery and fresh fallback remain available."
        else:
            kwja_item.state = "starting"; kwja_item.detail = "Persistent KWJA is warming in the background."
    def _record_service(self, name, owned, port, repo, url, kind):
        pid = listener_pid(port); current = identity(pid) if pid else None
        self.services[name] = Service(name, owned.process.pid, pid, port, str(repo.resolve()), url, kind, current.created if current else None)
        write_manifest(self.manifest_path, self.instance_id, os.getpid(), list(self.services.values()))
    def required_service_health(self):
        return {
            "analyzer": service_ok(
                "analyzer-liveness",
                self.config.analyzer_url + "/liveness",
                timeout=10.0,
            ),
            "frontend": service_ok(
                "frontend",
                self.config.frontend_identity_url,
                timeout=10.0,
            ),
        }

    def update_required_service_health(
        self,
        failure_counts,
    ):
        health = self.required_service_health()
        failed_component = None

        for name, healthy in health.items():
            item = self.snapshot.components[name]

            if healthy:
                failure_counts[name] = 0
                if name == "analyzer" and hasattr(self, "config"):
                    current = probe(self.config.analyzer_url + "/health", timeout=10.0)
                    if current.ok and isinstance(current.body, dict):
                        self.apply_health(current.body)
                if item.state == "checking":
                    item.state = "ready"
                    item.detail = (
                        "Service recovered after a "
                        "temporary health-check failure."
                    )

                continue

            failure_counts[name] += 1

            if failure_counts[name] < 3:
                item.state = "checking"
                item.detail = (
                    "Health check temporarily unavailable. "
                    f"Retrying ({failure_counts[name]}/3)."
                )
            else:
                failed_component = name
                break

        self.save()

        return failed_component
    def ensure_analyzer(self) -> bool:
        item = self.snapshot.components["analyzer"]; item.url = self.config.analyzer_url
        result = probe(self.config.analyzer_url + "/health")
        if result.ok and _compatible_analyzer(result.body):
            item.state, item.detail = "ready", "Reused running analyzer."; self.apply_health(result.body); self.save(); return True
        if tcp_port_open(self.config.analyzer_host, self.config.analyzer_port): return self.fail("ANALYZER_PORT_CONFLICT", f"Port {self.config.analyzer_port} is occupied by an incompatible service.", "analyzer", result.error)
        item.state = "starting"; self.save(); env = dict(os.environ); env["KWJA_EXE"] = str(self.config.kwja_executable); env["KWJA_EXECUTION_MODE"] = self.config.kwja_execution_mode
        command = [str(self.config.analyzer_python), "-m", "uvicorn", "app.analyzer.service:app", "--host", self.config.analyzer_host, "--port", str(self.config.analyzer_port)]
        owned = self.processes.start("jp-analyzer", command, self.config.analyzer_repo, env); item.pid = owned.process.pid
        result = wait_for(self.config.analyzer_url + "/liveness", self.config.analyzer_timeout_seconds, owned.process)
        if not result.ok or not _compatible_analyzer_liveness(result.body): return self.fail("ANALYZER_START_FAILED", "JP Analyzer did not become live.", "analyzer", result.error)
        item.state, item.detail = "ready", "Started by launcher."; self._record_service("analyzer", owned, self.config.analyzer_port, self.config.analyzer_repo, self.config.analyzer_url + "/health", "analyzer"); self.save(); return True
    def ensure_frontend(self) -> bool:
        item = self.snapshot.components["frontend"]; item.url = self.config.frontend_url
        identity = probe(self.config.frontend_identity_url)
        if identity.ok and _compatible_frontend(identity.body): item.state, item.detail = "ready", "Reused compatible running frontend."; self.save(); return True
        if tcp_port_open(self.config.frontend_host, self.config.frontend_port): return self.fail("FRONTEND_PORT_CONFLICT", f"Port {self.config.frontend_port} is occupied by an incompatible service.", "frontend", identity.error)
        item.state = "starting"; self.save(); owned = self.processes.start("novel-audio-miner", list(self.config.frontend_command), self.config.frontend_repo, dict(os.environ)); item.pid = owned.process.pid
        result = wait_for(self.config.frontend_identity_url, self.config.frontend_timeout_seconds, owned.process)
        if not result.ok or not _compatible_frontend(result.body): return self.fail("FRONTEND_START_FAILED", "Novel Audio Miner did not become ready.", "frontend", result.error)
        item.state, item.detail = "ready", "Started by launcher."; self._record_service("frontend", owned, self.config.frontend_port, self.config.frontend_repo, self.config.frontend_identity_url, "frontend"); self.save(); return True
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
            heartbeat_at = 0.0
            optional_probe_at = 0.0
            service_probe_at = 0.0

            required_failure_counts = {
                "analyzer": 0,
                "frontend": 0,
            }
            while not self.stopping:
                time.sleep(1)
                if shutdown_requested(self.shutdown_request_path):
                    self.shutdown_request_path.unlink(missing_ok=True)
                    self.stopping = True
                    continue
                now = time.monotonic()
                if now >= heartbeat_at:
                    self.save()
                    heartbeat_at = now + 5
                if now >= optional_probe_at:
                    self.probe_optional()
                    optional_probe_at = now + 10
                if now >= service_probe_at:
                    failed_component = (
                        self.update_required_service_health(
                            required_failure_counts,
                        )
                    )

                    if failed_component is not None:
                        return self.fail(
                            "REQUIRED_SERVICE_LOST",
                            (
                                "A required application service "
                                "stopped responding after three "
                                "consecutive health checks."
                            ),
                            failed_component,
                        )

                    service_probe_at = now + 5
            return 0
        finally:
            self.processes.stop_all()
            self.lock.release()
            self.manifest_path.unlink(missing_ok=True)
            if self.stopping:
                self.finalize_shutdown_status("user-requested")
            else:
                self.save()

def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    config = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    supervisor = ApplicationSupervisor(repo, config)
    try:
        return supervisor.run()
    except Exception as error:
        from .instance_lock import InstanceLockError
        if isinstance(error, InstanceLockError):
            open_application(supervisor.config.frontend_url)
            return 0
        raise
if __name__ == "__main__": raise SystemExit(main())
