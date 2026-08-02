from types import SimpleNamespace
from app.startup.ownership import Service, load_services, safe_listener

def test_manifest_service_parsing(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text('{"schema":"JapaneseNovelMinerOwnedProcesses.v1","services":{"frontend":{"name":"frontend","wrapper_pid":1,"listener_pid":2,"port":5173,"repository":"C:/repo","identity_url":"http://x","kind":"frontend"}}}')
    assert load_services(path)[0].listener_pid == 2

def test_safe_fallback_refuses_foreign_command(monkeypatch):
    service = Service("frontend",1,2,5173,"C:/repo","http://x","frontend")
    monkeypatch.setattr("app.startup.ownership.listener_pid", lambda port: 2)
    monkeypatch.setattr("app.startup.ownership.identity", lambda pid: SimpleNamespace(pid=2, created=None, command_line="python unrelated.py"))
    monkeypatch.setattr("app.startup.ownership.service_ok", lambda kind,url: True)
    assert safe_listener(service) is None
