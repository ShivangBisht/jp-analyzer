from __future__ import annotations
import json
from app.analyzer.config import AnalyzerConfig
from app.analyzer import kwja_warmup
from app.startup.config import SCHEMA, load_config


def test_fresh_mode_does_not_start_warmup(monkeypatch):
    kwja_warmup.reset_kwja_warmup_for_tests()
    config = AnalyzerConfig(kwja_execution_mode="fresh")
    assert kwja_warmup.start_kwja_warmup(config) is False
    assert kwja_warmup.kwja_warmup_status()["state"] == "disabled"


def test_persistent_warmup_is_non_blocking_and_reuses_runtime(monkeypatch, tmp_path):
    kwja_warmup.reset_kwja_warmup_for_tests()
    executable = tmp_path / "kwja.exe"; executable.write_text("")
    completed = __import__("threading").Event()
    class Runtime:
        def analyze_with_retry(self, text):
            assert text == kwja_warmup.WARMUP_TEXT
            completed.set()
    monkeypatch.setattr(kwja_warmup, "get_persistent_kwja_runtime", lambda _: Runtime())
    config = AnalyzerConfig(kwja_executable=executable, kwja_execution_mode="persistent")
    assert kwja_warmup.start_kwja_warmup(config) is True
    assert completed.wait(2)
    for _ in range(100):
        if kwja_warmup.kwja_warmup_status()["state"] == "ready": break
        __import__("time").sleep(.01)
    assert kwja_warmup.kwja_warmup_status()["state"] == "ready"


def test_launcher_defaults_to_persistent_and_accepts_fresh(tmp_path, monkeypatch):
    analyzer=tmp_path/"JP analyzer"; frontend=tmp_path/"novel-audio-miner"; python=analyzer/".venv/Scripts/python.exe"; kwja=tmp_path/"kwja.exe"; npm=tmp_path/"npm.cmd"
    frontend.mkdir(parents=True); (frontend/"package.json").write_text("{}")
    python.parent.mkdir(parents=True); python.write_text(""); kwja.write_text(""); npm.write_text("")
    monkeypatch.setattr("app.startup.discovery.shutil.which", lambda _: str(npm))
    path=analyzer/"startup.json"
    path.write_text(json.dumps({"schema":SCHEMA,"frontend":{"repository":str(frontend)},"kwja":{"executable":str(kwja)},"startup":{"openBrowser":False}}))
    assert load_config(analyzer,path).kwja_execution_mode == "persistent"
    payload=json.loads(path.read_text()); payload["kwja"]["executionMode"]="fresh"; path.write_text(json.dumps(payload))
    assert load_config(analyzer,path).kwja_execution_mode == "fresh"



def test_analyzer_liveness_contract_is_lightweight():
    from app.startup.supervisor import _compatible_analyzer_liveness

    assert _compatible_analyzer_liveness({
        "status": "alive",
        "service": "jp-analyzer",
    }) is True
    assert _compatible_analyzer_liveness({"status": "ok"}) is False
    assert _compatible_analyzer_liveness({
        "status": "alive",
        "service": "other",
    }) is False


def test_started_analyzer_waits_for_liveness_before_health():
    source = (
        __import__("pathlib").Path(__file__).resolve().parents[1]
        / "app"
        / "startup"
        / "supervisor.py"
    ).read_text(encoding="utf-8")
    assert 'wait_for(self.config.analyzer_url + "/liveness"' in source
    assert 'wait_for(self.config.analyzer_url + "/health"' not in source
    assert 'self.apply_health(result.body); self._record_service("analyzer"' not in source
