from pathlib import Path
import json
from app.startup.config import SCHEMA, initialize_local_config, load_config
from app.startup.discovery import discover_frontend, discover_kwja, discover_python
from app.startup.models import StartupSnapshot
from app.startup.supervisor import _compatible_analyzer, _compatible_frontend

def make_analyzer(tmp_path):
    repo=tmp_path/"JP analyzer"; python=repo/".venv/Scripts/python.exe"; python.parent.mkdir(parents=True); python.write_text(""); return repo

def test_sibling_discovery(tmp_path, monkeypatch):
    analyzer=make_analyzer(tmp_path); frontend=tmp_path/"novel-audio-miner"; frontend.mkdir(); (frontend/"package.json").write_text("{}")
    kwja=tmp_path/"KWJA evaluator/.venv/Scripts/kwja.exe"; kwja.parent.mkdir(parents=True); kwja.write_text("")
    monkeypatch.delenv("KWJA_EXE", raising=False); monkeypatch.setattr("app.startup.discovery.shutil.which", lambda _: None)
    assert discover_frontend(analyzer,"auto").source=="sibling"; assert discover_kwja(analyzer,"auto").source=="sibling-venv"; assert discover_python(analyzer,"auto").source=="analyzer-venv"

def test_local_config_is_created_once(tmp_path, monkeypatch):
    analyzer=make_analyzer(tmp_path); frontend=tmp_path/"novel-audio-miner"; frontend.mkdir(); (frontend/"package.json").write_text("{}")
    kwja=tmp_path/"KWJA evaluator/.venv/Scripts/kwja.exe"; kwja.parent.mkdir(parents=True); kwja.write_text(""); npm=tmp_path/"npm.cmd"; npm.write_text("")
    monkeypatch.setattr("app.startup.discovery.shutil.which", lambda _: str(npm))
    config=load_config(analyzer); created=initialize_local_config(config); assert created; original=created.read_text(); assert initialize_local_config(config) is None; assert created.read_text()==original; assert json.loads(original)["schema"]==SCHEMA

def test_service_identity_and_diagnostics():
    assert _compatible_analyzer({"dictionary":{"ready":True}}); assert not _compatible_analyzer({"status":"ok"})
    assert _compatible_frontend({"application":"JapaneseNovelMiner"}); assert not _compatible_frontend({"application":"Other"})
    assert StartupSnapshot(diagnostics={"logDirectory":"logs"}).to_dict()["diagnostics"]["logDirectory"]=="logs"
