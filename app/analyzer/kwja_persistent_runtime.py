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

    This class changes execution lifecycle only. It returns the raw KNP stream
    produced by KWJA and leaves all normalization and linguistic decisions to
    the existing validated analyzer path.
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

    def analyze(self, text: str) -> WorkerResult:
        """Analyze one sentence while preventing protocol interleaving.

        Any failure invalidates the worker because delayed or partial output
        must never be consumed by a later request. Recovery/fallback policy is
        intentionally deferred to Phase 12A.3B.
        """
        with self._lock:
            worker = self._ensure_worker()
            try:
                result = worker.analyze(text, timeout_seconds=self.timeout_seconds)
            except BaseException:
                self._invalidate_locked()
                raise
            self._request_count += 1
            return result

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
