from __future__ import annotations

import threading
from datetime import datetime, timezone
from time import perf_counter
from typing import Any

from .config import AnalyzerConfig
from .kwja_persistent_runtime import (
    get_persistent_kwja_runtime,
    stop_persistent_kwja_runtimes,
)

WARMUP_TEXT = "検証。"
_lock = threading.RLock()
_thread: threading.Thread | None = None
_state: dict[str, Any] = {
    "state": "not-started",
    "startedAt": None,
    "completedAt": None,
    "elapsedMs": None,
    "error": None,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(config: AnalyzerConfig) -> None:
    started = perf_counter()
    with _lock:
        _state.update(state="running", startedAt=_now(), completedAt=None, elapsedMs=None, error=None)
    try:
        runtime = get_persistent_kwja_runtime(str(config.kwja_executable))
        runtime.analyze_with_retry(WARMUP_TEXT)
    except Exception as error:
        with _lock:
            _state.update(
                state="failed",
                completedAt=_now(),
                elapsedMs=(perf_counter() - started) * 1000,
                error=f"{type(error).__name__}: {error}",
            )
        return
    with _lock:
        _state.update(
            state="ready",
            completedAt=_now(),
            elapsedMs=(perf_counter() - started) * 1000,
            error=None,
        )


def start_kwja_warmup(config: AnalyzerConfig | None = None) -> bool:
    """Start one non-blocking warm-up only for configured persistent mode."""
    global _thread
    cfg = config or AnalyzerConfig.from_environment()
    with _lock:
        if cfg.kwja_execution_mode != "persistent":
            _state.update(state="disabled", startedAt=None, completedAt=None, elapsedMs=None, error=None)
            return False
        if not cfg.kwja_available():
            _state.update(state="failed", startedAt=None, completedAt=_now(), elapsedMs=None, error="KWJA executable is unavailable.")
            return False
        if _thread is not None and _thread.is_alive():
            return False
        if _state["state"] == "ready":
            return False
        _thread = threading.Thread(target=_run, args=(cfg,), name="kwja-background-warmup", daemon=True)
        _thread.start()
        return True


def kwja_warmup_status() -> dict[str, Any]:
    with _lock:
        return dict(_state)


def shutdown_kwja_runtime() -> None:
    """Stop the shared runtime. The runtime lock safely coordinates warm-up/request completion."""
    stop_persistent_kwja_runtimes()


def reset_kwja_warmup_for_tests() -> None:
    global _thread
    shutdown_kwja_runtime()
    with _lock:
        _thread = None
        _state.update(state="not-started", startedAt=None, completedAt=None, elapsedMs=None, error=None)
