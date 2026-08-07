from __future__ import annotations

from dataclasses import dataclass

from app.analyzer.config import AnalyzerConfig
from app.analyzer.kwja_persistent_runtime import PersistentKwjaRuntime
from app.analyzer import kwja_runtime


@dataclass
class FakeResult:
    request_id: str = "request"
    output: str = "RAW KNP\nEOS\n"
    elapsed_ms: float = 1.0
    process_id: int = 123


class FakeWorker:
    def __init__(self, outcome):
        self.outcome = outcome
        self.running = False
        self.stop_count = 0

    def start(self):
        self.running = True
        return 0.0

    def analyze(self, text, *, timeout_seconds):
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome

    def diagnostics(self):
        return {"running": self.running, "processId": 123 if self.running else None}

    def stop(self):
        self.running = False
        self.stop_count += 1


def test_one_failure_retries_with_clean_worker():
    first = FakeWorker(TimeoutError("first failed"))
    second = FakeWorker(FakeResult())
    workers = iter([first, second])
    runtime = PersistentKwjaRuntime("kwja.exe", worker_factory=lambda _: next(workers))
    result = runtime.analyze_with_retry("回復")
    assert result.output.endswith("EOS\n")
    assert first.stop_count == 1
    status = runtime.status()
    assert status["generation"] == 2
    assert status["restartCount"] == 1
    assert status["fallbackCount"] == 0
    assert status["requestCount"] == 1


def test_second_failure_is_propagated_for_fresh_fallback():
    workers = iter([
        FakeWorker(RuntimeError("first failed")),
        FakeWorker(RuntimeError("second failed")),
    ])
    runtime = PersistentKwjaRuntime("kwja.exe", worker_factory=lambda _: next(workers))
    try:
        runtime.analyze_with_retry("失敗")
    except RuntimeError as error:
        assert str(error) == "second failed"
    else:
        raise AssertionError("second persistent failure was not propagated")
    status = runtime.status()
    assert status["generation"] == 2
    assert status["restartCount"] == 1
    assert status["running"] is False


def test_adapter_falls_back_to_unchanged_fresh_path(monkeypatch, tmp_path):
    executable = tmp_path / "kwja.exe"
    executable.write_text("", encoding="utf-8")
    calls = []

    class Runtime:
        def analyze_with_retry(self, text):
            raise RuntimeError("persistent unavailable")

        def record_fallback(self):
            calls.append("fallback-recorded")

    def fake_analyze(text, *, raw_knp, executable):
        calls.append((text, raw_knp, executable))
        return {"mode": "fresh-fallback"}

    monkeypatch.setattr(kwja_runtime, "get_persistent_kwja_runtime", lambda _: Runtime())
    monkeypatch.setattr(kwja_runtime, "analyze_kwja_alpha1", fake_analyze)
    config = AnalyzerConfig(kwja_executable=executable, kwja_execution_mode="persistent")
    result = kwja_runtime.analyze_kwja("文", config=config)
    assert result == {"mode": "fresh-fallback"}
    assert calls == [
        "fallback-recorded",
        ("文", None, str(executable)),
    ]


def test_successful_persistent_request_never_invokes_fresh(monkeypatch, tmp_path):
    executable = tmp_path / "kwja.exe"
    executable.write_text("", encoding="utf-8")
    calls = []

    class Runtime:
        def analyze_with_retry(self, text):
            return FakeResult()

        def record_fallback(self):
            raise AssertionError("fallback must not be recorded")

    def fake_analyze(text, *, raw_knp, executable):
        calls.append((raw_knp, executable))
        return {"ok": True}

    monkeypatch.setattr(kwja_runtime, "get_persistent_kwja_runtime", lambda _: Runtime())
    monkeypatch.setattr(kwja_runtime, "analyze_kwja_alpha1", fake_analyze)
    config = AnalyzerConfig(kwja_executable=executable, kwja_execution_mode="persistent")
    assert kwja_runtime.analyze_kwja("文", config=config) == {"ok": True}
    assert calls == [("RAW KNP\nEOS\n", None)]
