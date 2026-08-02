from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from app.startup import status_api


def _snapshot(captured_at: str, *, overall: str = "ready") -> dict:
    return {
        "schema": "ApplicationStartupSupervisor.v1",
        "capturedAt": captured_at,
        "overall_status": overall,
        "components": {
            "analyzer": {"required": True, "state": "ready", "detail": "Ready", "pid": 123, "url": "http://127.0.0.1:8766"},
            "dictionary": {"required": True, "state": "ready", "detail": "10 entries", "pid": None, "url": None},
            "kwja": {"required": True, "state": "ready", "detail": "C:/private/kwja.exe", "pid": None, "url": None},
            "frontend": {"required": True, "state": "ready", "detail": "Ready", "pid": 456, "url": "http://127.0.0.1:5173/"},
            "voicevox": {"required": False, "state": "degraded", "detail": "Optional service unavailable.", "pid": None, "url": "http://127.0.0.1:50021/version"},
            "ankiConnect": {"required": False, "state": "degraded", "detail": "Optional service unavailable.", "pid": None, "url": "http://127.0.0.1:8765"},
        },
        "problems": [],
        "diagnostics": {"kwjaExecutable": "C:/private/kwja.exe", "logDirectory": "C:/private/logs"},
    }


def test_status_is_sanitized_and_current(tmp_path, monkeypatch):
    monkeypatch.setattr(status_api, "_runtime_directory", lambda: tmp_path)
    (tmp_path / "startup-status.json").write_text(
        json.dumps(_snapshot(datetime.now(timezone.utc).isoformat())),
        encoding="utf-8",
    )
    value = status_api.build_startup_status()
    assert value["schema"] == "ApplicationStartupStatus.v1"
    assert value["overallStatus"] == "ready"
    assert value["stale"] is False
    assert "pid" not in value["components"]["analyzer"]
    assert "kwjaExecutable" not in value["diagnostics"]
    assert value["components"]["voicevox"]["state"] == "degraded"


def test_stale_status_is_degraded(tmp_path, monkeypatch):
    monkeypatch.setattr(status_api, "_runtime_directory", lambda: tmp_path)
    old = datetime.now(timezone.utc) - timedelta(minutes=2)
    (tmp_path / "startup-status.json").write_text(
        json.dumps(_snapshot(old.isoformat())),
        encoding="utf-8",
    )
    value = status_api.build_startup_status()
    assert value["overallStatus"] == "degraded"
    assert value["stale"] is True
    assert any(item["code"] == "SUPERVISOR_STATUS_STALE" for item in value["problems"])


def test_missing_status_uses_runtime_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(status_api, "_runtime_directory", lambda: tmp_path)
    monkeypatch.setattr(status_api, "health_report", lambda: {"dictionary": {"ready": True, "entryCount": 10, "dictionaryCount": 2, "registryConsistent": True, "recoveryRequired": False}})
    value = status_api.build_startup_status()
    assert value["source"] == "runtime-fallback"
    assert value["overallStatus"] == "degraded"
    assert value["components"]["analyzer"]["state"] == "ready"
    assert value["components"]["dictionary"]["state"] == "ready"
