from __future__ import annotations
import json
import os
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "JapaneseNovelMinerStartup.v1"

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
    open_browser: bool = True
    analyzer_timeout_seconds: float = 120.0
    frontend_timeout_seconds: float = 60.0
    @property
    def analyzer_url(self) -> str:
        return f"http://{self.analyzer_host}:{self.analyzer_port}"
    @property
    def frontend_url(self) -> str:
        # Vite serves the application at the root path. Preserve the trailing
        # slash because Vite may return 404 for the slashless origin.
        return f"http://{self.frontend_host}:{self.frontend_port}/"

def _resolve(base: Path, value: str | None, fallback: Path) -> Path:
    if not value or value == "auto":
        return fallback.resolve()
    path = Path(os.path.expandvars(os.path.expanduser(value)))
    return (base / path).resolve() if not path.is_absolute() else path.resolve()

def load_config(analyzer_repo: Path, local_path: Path | None = None) -> StartupConfig:
    analyzer_repo = analyzer_repo.resolve()
    root = analyzer_repo.parent
    path = local_path or analyzer_repo / "config" / "startup.local.json"
    raw = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    if raw and raw.get("schema") != SCHEMA:
        raise ValueError(f"Expected startup config schema {SCHEMA!r}.")
    analyzer = raw.get("analyzer", {})
    frontend = raw.get("frontend", {})
    kwja = raw.get("kwja", {})
    startup = raw.get("startup", {})
    analyzer_path = _resolve(root, analyzer.get("repository"), analyzer_repo)
    python_path = _resolve(analyzer_path, analyzer.get("python"), analyzer_path / ".venv" / "Scripts" / "python.exe")
    frontend_path = _resolve(root, frontend.get("repository"), root / "novel-audio-miner")
    kwja_value = kwja.get("executable") or os.environ.get("KWJA_EXE")
    kwja_path = None if not kwja_value or kwja_value == "auto" else _resolve(root, kwja_value, Path(kwja_value))
    command = tuple(frontend.get("command") or ["npm.cmd", "run", "dev", "--", "--host", "127.0.0.1"])
    return StartupConfig(analyzer_path, python_path, frontend_path, command,
        analyzer.get("host", "127.0.0.1"), int(analyzer.get("port", 8766)),
        frontend.get("host", "127.0.0.1"), int(frontend.get("port", 5173)), kwja_path,
        bool(startup.get("openBrowser", True)), float(startup.get("analyzerTimeoutSeconds", 120)),
        float(startup.get("frontendTimeoutSeconds", 60)))
