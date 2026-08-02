from pathlib import Path
import json
import pytest
from app.startup.config import SCHEMA, load_config
from app.startup.instance_lock import InstanceLock, InstanceLockError
from app.startup.models import ComponentStatus, StartupSnapshot

def test_snapshot_contract():
    value = StartupSnapshot(components={"analyzer": ComponentStatus("analyzer", True, "ready")}).to_dict()
    assert value["schema"] == "ApplicationStartupSupervisor.v1"
    assert value["components"]["analyzer"]["state"] == "ready"

def test_machine_local_config(tmp_path: Path):
    analyzer, frontend, kwja = tmp_path / "JP analyzer", tmp_path / "novel-audio-miner", tmp_path / "kwja.exe"
    python = analyzer / ".venv" / "Scripts" / "python.exe"
    frontend.mkdir(); python.parent.mkdir(parents=True); python.write_text(""); kwja.write_text("")
    config = analyzer / "startup.json"; config.write_text(json.dumps({"schema": SCHEMA, "frontend": {"repository": str(frontend)}, "kwja": {"executable": str(kwja)}, "startup": {"openBrowser": False}}))
    loaded = load_config(analyzer, config)
    assert loaded.frontend_repo == frontend.resolve() and loaded.kwja_executable == kwja.resolve() and not loaded.open_browser

def test_lock_rejects_live_owner(tmp_path: Path, monkeypatch):
    first = InstanceLock(tmp_path / "lock", "one"); first.acquire(); monkeypatch.setattr("app.startup.instance_lock._pid_exists", lambda _: True)
    with pytest.raises(InstanceLockError): InstanceLock(tmp_path / "lock", "two").acquire()
    first.release()


def test_frontend_url_keeps_root_slash(tmp_path: Path):
    analyzer = tmp_path / "JP analyzer"
    frontend = tmp_path / "novel-audio-miner"
    python = analyzer / ".venv" / "Scripts" / "python.exe"
    frontend.mkdir(parents=True)
    python.parent.mkdir(parents=True)
    python.write_text("")
    config = analyzer / "startup.json"
    config.write_text(json.dumps({
        "schema": SCHEMA,
        "frontend": {"repository": str(frontend)},
        "startup": {"openBrowser": False},
    }))
    loaded = load_config(analyzer, config)
    assert loaded.frontend_url == "http://127.0.0.1:5173/"


def test_windows_cleanup_targets_owned_process_tree(tmp_path: Path, monkeypatch):
    from types import SimpleNamespace
    from app.startup.process_manager import OwnedProcess, ProcessManager

    class FakeProcess:
        pid = 43210
        returncode = None

        def poll(self):
            return None

        def wait(self, timeout=None):
            self.returncode = 1
            return 1

    calls = []
    monkeypatch.setattr("app.startup.process_manager.os.name", "nt")
    monkeypatch.setattr(
        "app.startup.process_manager.subprocess.run",
        lambda command, **kwargs: calls.append((command, kwargs))
        or SimpleNamespace(returncode=0),
    )

    manager = ProcessManager(tmp_path / "logs")
    manager.owned.append(OwnedProcess(
        "novel-audio-miner",
        FakeProcess(),
        tmp_path / "out.log",
        tmp_path / "err.log",
    ))
    manager.stop_all()

    assert calls
    assert calls[0][0] == ["taskkill", "/PID", "43210", "/T", "/F"]
    assert manager.owned == []

def test_html_probe_uses_browser_accept_header(monkeypatch):
    from app.startup.health import probe

    captured = {}

    class Response:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return b"<html>ready</html>"

    def fake_urlopen(request, timeout):
        captured["accept"] = request.get_header("Accept")
        return Response()

    monkeypatch.setattr("app.startup.health.urlopen", fake_urlopen)
    result = probe("http://127.0.0.1:5173/", accept="text/html,*/*;q=0.8")
    assert result.ok is True
    assert result.status == 200
    assert captured["accept"] == "text/html,*/*;q=0.8"
    assert "ready" in result.body

