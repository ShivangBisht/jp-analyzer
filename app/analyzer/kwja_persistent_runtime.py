from __future__ import annotations

import atexit
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .kwja_persistent_worker import InteractiveKwjaWorker, WorkerResult

WorkerFactory = Callable[[str], InteractiveKwjaWorker]


class PersistentKwjaRuntime:
    """Own one serialized interactive KWJA worker for one executable.

    Runtime recovery is bounded to one clean-worker retry. If both persistent
    attempts fail, the caller may use the unchanged fresh-process route.
    Linguistic normalization and decisions remain outside this class.
    """

    def __init__(
        self,
        executable: str,
        *,
        model_size: str = "base",
        timeout_seconds: float = 180.0,
        worker_factory: WorkerFactory | None = None,
    ):
        self.executable = str(Path(executable))
        self.model_size = model_size
        self.timeout_seconds = timeout_seconds
        self._worker_factory = worker_factory or self._default_worker_factory
        self._lock = threading.RLock()
        self._worker: InteractiveKwjaWorker | None = None
        self._generation = 0
        self._request_count = 0
        self._restart_count = 0
        self._fallback_count = 0
        self._last_error: str | None = None
        self._last_execution_mode = "idle"

    def _default_worker_factory(self, executable: str) -> InteractiveKwjaWorker:
        return InteractiveKwjaWorker(executable, model_size=self.model_size)

    def _ensure_worker(self) -> InteractiveKwjaWorker:
        worker = self._worker
        if worker is not None and worker.diagnostics().get("running"):
            return worker
        if worker is not None:
            worker.stop()
        worker = self._worker_factory(self.executable)
        worker.start()
        self._worker = worker
        self._generation += 1
        return worker

    def _analyze_once_locked(self, text: str) -> WorkerResult:
        worker = self._ensure_worker()
        try:
            result = worker.analyze(text, timeout_seconds=self.timeout_seconds)
        except Exception as error:
            self._last_error = f"{type(error).__name__}: {error}"
            self._invalidate_locked()
            raise
        self._request_count += 1
        self._last_error = None
        self._last_execution_mode = "persistent"
        return result

    def analyze(self, text: str) -> WorkerResult:
        """Perform one persistent attempt, preserving the A.3A API."""
        with self._lock:
            return self._analyze_once_locked(text)

    def analyze_with_retry(self, text: str) -> WorkerResult:
        """Retry once with a clean worker after a persistent failure.

        The failed worker is already invalidated by the first attempt. A second
        failure is propagated so the transport adapter can use the established
        fresh-process fallback. No uncertain worker is ever reused.
        """
        with self._lock:
            try:
                return self._analyze_once_locked(text)
            except Exception:
                self._restart_count += 1
                self._last_execution_mode = "persistent-retry"
                return self._analyze_once_locked(text)

    def record_fallback(self) -> None:
        with self._lock:
            self._fallback_count += 1
            self._last_execution_mode = "fresh-fallback"

    def _invalidate_locked(self) -> None:
        worker = self._worker
        self._worker = None
        if worker is not None:
            worker.stop()

    def stop(self) -> None:
        with self._lock:
            self._invalidate_locked()

    def status(self) -> dict[str, Any]:
        with self._lock:
            diagnostics = self._worker.diagnostics() if self._worker is not None else {"running": False, "processId": None}
            return {
                "running": bool(diagnostics.get("running")),
                "processId": diagnostics.get("processId"),
                "generation": self._generation,
                "requestCount": self._request_count,
                "restartCount": self._restart_count,
                "fallbackCount": self._fallback_count,
                "lastExecutionMode": self._last_execution_mode,
                "lastError": self._last_error,
                "modelSize": self.model_size,
            }


_registry_lock = threading.RLock()
_runtimes: dict[tuple[str, str], PersistentKwjaRuntime] = {}


def get_persistent_kwja_runtime(
    executable: str,
    *,
    model_size: str = "base",
) -> PersistentKwjaRuntime:
    key = (str(Path(executable).resolve()), model_size)
    with _registry_lock:
        runtime = _runtimes.get(key)
        if runtime is None:
            runtime = PersistentKwjaRuntime(key[0], model_size=model_size)
            _runtimes[key] = runtime
        return runtime


def stop_persistent_kwja_runtimes() -> None:
    with _registry_lock:
        runtimes = list(_runtimes.values())
        _runtimes.clear()
    for runtime in runtimes:
        runtime.stop()


atexit.register(stop_persistent_kwja_runtimes)
