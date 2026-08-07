from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from .discovery import Resolution, discover_command, discover_frontend, discover_kwja, discover_python
SCHEMA = "JapaneseNovelMinerStartup.v1"
VALID_KWJA_EXECUTION_MODES = {"fresh", "persistent"}
@dataclass(frozen=True)
class StartupConfig:
    analyzer_repo: Path
    analyzer_python: Path
    frontend_repo: Path
    frontend_command: tuple[str, ...]
    analyzer_host: str = "127.0.0.1"
    analyzer_port: int = 8766
    frontend_host: str = "127.0.0.1"
    frontend_port: int = 5173
    kwja_executable: Path | None = None
    kwja_execution_mode: str = "persistent"
    open_browser: bool = True
    analyzer_timeout_seconds: float = 120.0
    frontend_timeout_seconds: float = 60.0
    config_path: Path | None = None
    resolutions: dict[str, dict] = field(default_factory=dict)
    @property
    def analyzer_url(self): return f"http://{self.analyzer_host}:{self.analyzer_port}"
    @property
    def frontend_url(self): return f"http://{self.frontend_host}:{self.frontend_port}/"
    @property
    def frontend_identity_url(self): return self.frontend_url + "japanese-novel-miner-identity.json"
    def diagnostics(self):
        return {"configPath": str(self.config_path) if self.config_path else None, "analyzerRepository": str(self.analyzer_repo), "analyzerPython": str(self.analyzer_python), "frontendRepository": str(self.frontend_repo), "frontendCommand": list(self.frontend_command), "kwjaExecutable": str(self.kwja_executable) if self.kwja_executable else None, "kwjaExecutionMode": self.kwja_execution_mode, "analyzerUrl": self.analyzer_url, "frontendUrl": self.frontend_url, "resolutions": self.resolutions}
def _required(result, label):
    if result.value is None: raise ValueError(f"{label} could not be resolved. Checked: {', '.join(result.candidates) or 'none'}")
    return result.value
def _execution_mode(value):
    mode = str(value or "persistent").strip().lower()
    if mode not in VALID_KWJA_EXECUTION_MODES:
        raise ValueError(f"kwja.executionMode must be one of: {', '.join(sorted(VALID_KWJA_EXECUTION_MODES))}")
    return mode
def initialize_local_config(config):
    path = config.analyzer_repo / "config/startup.local.json"
    if path.exists(): return None
    payload = {"schema": SCHEMA, "analyzer": {"repository": str(config.analyzer_repo), "python": str(config.analyzer_python), "host": config.analyzer_host, "port": config.analyzer_port}, "frontend": {"repository": str(config.frontend_repo), "host": config.frontend_host, "port": config.frontend_port, "command": list(config.frontend_command)}, "kwja": {"executable": str(config.kwja_executable) if config.kwja_executable else "auto", "executionMode": config.kwja_execution_mode}, "startup": {"openBrowser": config.open_browser, "analyzerTimeoutSeconds": config.analyzer_timeout_seconds, "frontendTimeoutSeconds": config.frontend_timeout_seconds}}
    path.parent.mkdir(parents=True, exist_ok=True); temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n"); temporary.replace(path); return path
def load_config(analyzer_repo: Path, local_path: Path | None = None):
    analyzer_repo = analyzer_repo.resolve(); path = local_path or analyzer_repo / "config/startup.local.json"
    raw = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    if raw and raw.get("schema") != SCHEMA: raise ValueError(f"Expected startup config schema {SCHEMA!r}.")
    analyzer, frontend, kwja, startup = raw.get("analyzer", {}), raw.get("frontend", {}), raw.get("kwja", {}), raw.get("startup", {})
    py = discover_python(analyzer_repo, analyzer.get("python")); fe = discover_frontend(analyzer_repo, frontend.get("repository")); kw = discover_kwja(analyzer_repo, kwja.get("executable"))
    command = tuple(frontend.get("command") or ["npm.cmd", "run", "dev", "--", "--host", "127.0.0.1"]); npm = discover_command(command[0])
    resolutions = {"analyzerRepository": Resolution(analyzer_repo, "launcher-location", (str(analyzer_repo),)).to_dict(), "analyzerPython": py.to_dict(), "frontendRepository": fe.to_dict(), "kwjaExecutable": kw.to_dict(), "frontendCommand": npm.to_dict()}
    return StartupConfig(analyzer_repo, _required(py, "JP Analyzer Python"), _required(fe, "Novel Audio Miner repository"), command, analyzer.get("host", "127.0.0.1"), int(analyzer.get("port", 8766)), frontend.get("host", "127.0.0.1"), int(frontend.get("port", 5173)), kw.value, _execution_mode(kwja.get("executionMode")), bool(startup.get("openBrowser", True)), float(startup.get("analyzerTimeoutSeconds", 120)), float(startup.get("frontendTimeoutSeconds", 60)), path if path.exists() else None, resolutions)
