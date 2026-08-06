from __future__ import annotations

from pathlib import Path

from .config import AnalyzerConfig
from .kwja_persistent_runtime import get_persistent_kwja_runtime
from .layers.kwja import analyze_kwja_alpha1


def resolve_kwja_executable(executable=None, config=None) -> Path:
    cfg = config or AnalyzerConfig.from_environment()
    path = Path(executable) if executable else cfg.kwja_executable
    if path is None:
        raise RuntimeError("Set KWJA_EXE to the isolated KWJA executable path.")
    if not path.is_file():
        raise FileNotFoundError(f"KWJA executable not found: {path}")
    return path


def kwja_status(config=None):
    cfg = config or AnalyzerConfig.from_environment()
    path = cfg.kwja_executable
    return {
        "available": bool(path and path.is_file()),
        "executable": str(path) if path else None,
        "modelSize": "base",
        "executionMode": cfg.kwja_execution_mode,
    }


def analyze_kwja(text, *, raw_knp=None, executable=None, config=None):
    cfg = config or AnalyzerConfig.from_environment()
    if raw_knp is not None:
        return analyze_kwja_alpha1(text, raw_knp=raw_knp, executable=None)

    path = resolve_kwja_executable(executable, cfg)
    if cfg.kwja_execution_mode == "persistent":
        worker_result = get_persistent_kwja_runtime(str(path)).analyze(text)
        return analyze_kwja_alpha1(text, raw_knp=worker_result.output, executable=None)

    return analyze_kwja_alpha1(text, raw_knp=None, executable=str(path))
