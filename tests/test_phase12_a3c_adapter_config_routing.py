from __future__ import annotations

from pathlib import Path

from app.analyzer.adapters.kwja_adapter import KwjaAdapter
from app.analyzer.config import AnalyzerConfig
from app.analyzer.adapters import kwja_adapter


def test_adapter_passes_its_config_to_runtime(monkeypatch, tmp_path):
    executable = tmp_path / "kwja.exe"
    executable.write_text("", encoding="utf-8")
    config = AnalyzerConfig(
        kwja_executable=executable,
        kwja_execution_mode="persistent",
    )
    captured = {}

    def fake_analyze(text, *, raw_knp, executable, config):
        captured.update(
            text=text,
            raw_knp=raw_knp,
            executable=executable,
            config=config,
        )
        return {"ok": True}

    monkeypatch.setattr(kwja_adapter, "analyze_kwja", fake_analyze)
    assert KwjaAdapter(config).analyze("文") == {"ok": True}
    assert captured["text"] == "文"
    assert captured["raw_knp"] is None
    assert captured["executable"] == str(executable)
    assert captured["config"] is config
    assert captured["config"].kwja_execution_mode == "persistent"


def test_adapter_raw_knp_still_passes_config_and_skips_resolution(monkeypatch):
    config = AnalyzerConfig(kwja_execution_mode="persistent")
    captured = {}

    def fake_analyze(text, *, raw_knp, executable, config):
        captured.update(raw_knp=raw_knp, executable=executable, config=config)
        return {"ok": True}

    monkeypatch.setattr(kwja_adapter, "analyze_kwja", fake_analyze)
    assert KwjaAdapter(config).analyze("文", raw_knp="KNP\nEOS\n") == {"ok": True}
    assert captured == {
        "raw_knp": "KNP\nEOS\n",
        "executable": None,
        "config": config,
    }
