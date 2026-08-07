from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.analyzer.config import AnalyzerConfig
from app.analyzer.kwja_persistent_runtime import PersistentKwjaRuntime


@dataclass
class FakeResult:
    request_id: str
    output: str
    elapsed_ms: float
    process_id: int


class FakeWorker:
    def __init__(self, *, fail=False):
        self.fail = fail
        self.running = False
        self.start_count = 0
        self.stop_count = 0
        self.calls = []

    def start(self):
        self.running = True
        self.start_count += 1
        return 0.0

    def analyze(self, text, *, timeout_seconds):
        self.calls.append((text, timeout_seconds))
        if self.fail:
            raise TimeoutError("synthetic timeout")
        return FakeResult("request", "EOS\n", 1.0, 123)

    def diagnostics(self):
        return {"running": self.running, "processId": 123 if self.running else None}

    def stop(self):
        self.running = False
        self.stop_count += 1


def test_configuration_defaults_to_fresh(monkeypatch):
    monkeypatch.delenv("KWJA_EXECUTION_MODE", raising=False)
    assert AnalyzerConfig.from_environment().kwja_execution_mode == "fresh"


def test_configuration_accepts_persistent(monkeypatch):
    monkeypatch.setenv("KWJA_EXECUTION_MODE", "persistent")
    assert AnalyzerConfig.from_environment().kwja_execution_mode == "persistent"


def test_configuration_rejects_unknown_mode(monkeypatch):
    monkeypatch.setenv("KWJA_EXECUTION_MODE", "unsafe")
    with pytest.raises(ValueError, match="KWJA_EXECUTION_MODE"):
        AnalyzerConfig.from_environment()


def test_runtime_reuses_one_worker_and_stops_idempotently():
    worker = FakeWorker()
    runtime = PersistentKwjaRuntime("kwja.exe", worker_factory=lambda _: worker)
    assert runtime.analyze("一").output == "EOS\n"
    assert runtime.analyze("二").output == "EOS\n"
    assert worker.start_count == 1
    assert [item[0] for item in worker.calls] == ["一", "二"]
    assert runtime.status()["requestCount"] == 2
    runtime.stop()
    runtime.stop()
    assert not runtime.status()["running"]


def test_runtime_invalidates_worker_after_protocol_failure():
    first = FakeWorker(fail=True)
    second = FakeWorker()
    workers = iter([first, second])
    runtime = PersistentKwjaRuntime("kwja.exe", worker_factory=lambda _: next(workers))
    with pytest.raises(TimeoutError, match="synthetic timeout"):
        runtime.analyze("失敗")
    assert first.stop_count == 1
    assert not runtime.status()["running"]
    assert runtime.analyze("回復").output == "EOS\n"
    assert runtime.status()["generation"] == 2
