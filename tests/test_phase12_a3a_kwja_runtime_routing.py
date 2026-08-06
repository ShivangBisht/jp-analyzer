from __future__ import annotations

from pathlib import Path

from app.analyzer.config import AnalyzerConfig
from app.analyzer import kwja_runtime


def test_fresh_mode_preserves_existing_execution_path(monkeypatch, tmp_path):
    executable = tmp_path / "kwja.exe"
    executable.write_text("", encoding="utf-8")
    captured = {}

    def fake_analyze(text, *, raw_knp, executable):
        captured.update(text=text, raw_knp=raw_knp, executable=executable)
        return {"mode": "fresh"}

    monkeypatch.setattr(kwja_runtime, "analyze_kwja_alpha1", fake_analyze)
    config = AnalyzerConfig(kwja_executable=executable, kwja_execution_mode="fresh")
    assert kwja_runtime.analyze_kwja("文", config=config) == {"mode": "fresh"}
    assert captured == {"text": "文", "raw_knp": None, "executable": str(executable)}


def test_persistent_mode_only_replaces_raw_kwja_transport(monkeypatch, tmp_path):
    executable = tmp_path / "kwja.exe"
    executable.write_text("", encoding="utf-8")
    captured = {}

    class Runtime:
        def analyze(self, text):
            captured["workerText"] = text
            return type("Result", (), {"output": "RAW KNP\nEOS\n"})()

    def fake_analyze(text, *, raw_knp, executable):
        captured.update(text=text, raw_knp=raw_knp, executable=executable)
        return {"mode": "persistent"}

    monkeypatch.setattr(kwja_runtime, "get_persistent_kwja_runtime", lambda _: Runtime())
    monkeypatch.setattr(kwja_runtime, "analyze_kwja_alpha1", fake_analyze)
    config = AnalyzerConfig(kwja_executable=executable, kwja_execution_mode="persistent")
    assert kwja_runtime.analyze_kwja("文", config=config) == {"mode": "persistent"}
    assert captured == {
        "workerText": "文",
        "text": "文",
        "raw_knp": "RAW KNP\nEOS\n",
        "executable": None,
    }


def test_injected_raw_knp_bypasses_both_execution_modes(monkeypatch):
    captured = {}

    def fake_analyze(text, *, raw_knp, executable):
        captured.update(text=text, raw_knp=raw_knp, executable=executable)
        return {"ok": True}

    monkeypatch.setattr(kwja_runtime, "analyze_kwja_alpha1", fake_analyze)
    config = AnalyzerConfig(kwja_execution_mode="persistent")
    assert kwja_runtime.analyze_kwja("文", raw_knp="KNP\nEOS\n", config=config) == {"ok": True}
    assert captured == {"text": "文", "raw_knp": "KNP\nEOS\n", "executable": None}
