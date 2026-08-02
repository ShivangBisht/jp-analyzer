from __future__ import annotations
import os
import shutil
import socket
import sys
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Resolution:
    value: Path | None
    source: str
    candidates: tuple[str, ...]
    def to_dict(self) -> dict:
        return {"value": str(self.value) if self.value else None, "source": self.source, "candidates": list(self.candidates)}

def _expanded(value: str | None, base: Path) -> Path | None:
    if not value or value == "auto": return None
    path = Path(os.path.expandvars(os.path.expanduser(value)))
    return (base / path).resolve() if not path.is_absolute() else path.resolve()

def _first_file(items):
    seen = []
    for source, candidate in items:
        if candidate is None: continue
        candidate = candidate.resolve(); seen.append(str(candidate))
        if candidate.is_file(): return Resolution(candidate, source, tuple(seen))
    return Resolution(None, "unresolved", tuple(seen))

def _first_directory(items, marker):
    seen = []
    for source, candidate in items:
        if candidate is None: continue
        candidate = candidate.resolve(); seen.append(str(candidate))
        if candidate.is_dir() and (candidate / marker).is_file(): return Resolution(candidate, source, tuple(seen))
    return Resolution(None, "unresolved", tuple(seen))

def discover_frontend(analyzer_repo: Path, configured: str | None) -> Resolution:
    workspace = analyzer_repo.resolve().parent
    return _first_directory([("configured", _expanded(configured, workspace)), ("sibling", workspace / "novel-audio-miner")], "package.json")

def discover_python(analyzer_repo: Path, configured: str | None) -> Resolution:
    repo = analyzer_repo.resolve(); venv = repo / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return _first_file([("configured", _expanded(configured, repo)), ("analyzer-venv", venv), ("current-interpreter", Path(sys.executable))])

def discover_kwja(analyzer_repo: Path, configured: str | None) -> Resolution:
    workspace = analyzer_repo.resolve().parent; hit = shutil.which("kwja.exe") or shutil.which("kwja")
    items = [("configured", _expanded(configured, workspace)), ("environment", _expanded(os.environ.get("KWJA_EXE"), workspace))]
    if os.name == "nt":
        items += [("sibling-venv", workspace / "KWJA evaluator/.venv/Scripts/kwja.exe"), ("sibling-kwja-venv", workspace / "KWJA evaluator/.kwja-venv/Scripts/kwja.exe")]
    else:
        items += [("sibling-venv", workspace / "KWJA evaluator/.venv/bin/kwja")]
    items += [("path", Path(hit) if hit else None)]
    return _first_file(items)

def discover_command(command: str) -> Resolution:
    hit = shutil.which(command)
    return _first_file([("path", Path(hit) if hit else None)])

def tcp_port_open(host: str, port: int, timeout: float = 0.25) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout): return True
    except OSError: return False
