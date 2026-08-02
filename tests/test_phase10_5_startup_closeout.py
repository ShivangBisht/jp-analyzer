from __future__ import annotations
from pathlib import Path

import json
from datetime import datetime, timedelta, timezone

from app.startup.models import ComponentStatus, StartupSnapshot
from app.startup.supervisor import ApplicationSupervisor
from app.startup import status_api


def _supervisor(tmp_path):
    value = object.__new__(ApplicationSupervisor)
    value.status_path = tmp_path / "startup-status.json"
    value.snapshot = StartupSnapshot(
        overall_status="ready",
        components={
            "analyzer": ComponentStatus("analyzer", True, "ready", pid=101),
            "dictionary": ComponentStatus("dictionary", True, "ready"),
            "kwja": ComponentStatus("kwja", True, "ready"),
            "frontend": ComponentStatus("frontend", True, "ready", pid=202),
            "voicevox": ComponentStatus("voicevox", False, "degraded"),
            "ankiConnect": ComponentStatus("ankiConnect", False, "degraded"),
        },
        diagnostics={},
    )
    return value


def test_finalize_requested_shutdown_records_stopped(tmp_path):
    supervisor = _supervisor(tmp_path)
    supervisor.finalize_shutdown_status("user-requested")
    payload = json.loads(supervisor.status_path.read_text(encoding="utf-8"))
    assert payload["overall_status"] == "stopped"
    assert payload["diagnostics"]["shutdownReason"] == "user-requested"
    assert all(
        component["state"] == "stopped"
        for component in payload["components"].values()
    )
    assert payload["components"]["analyzer"]["pid"] is None
    assert payload["components"]["frontend"]["pid"] is None


def test_stopped_status_is_not_reclassified_as_stale(tmp_path, monkeypatch):
    monkeypatch.setattr(status_api, "_runtime_directory", lambda: tmp_path)
    captured = datetime.now(timezone.utc) - timedelta(minutes=5)
    payload = {
        "schema": "ApplicationStartupSupervisor.v1",
        "capturedAt": captured.isoformat(),
        "overall_status": "stopped",
        "components": {
            name: {
                "required": name in {"analyzer", "dictionary", "kwja", "frontend"},
                "state": "stopped",
                "detail": None,
                "pid": None,
                "url": None,
            }
            for name in (
                "analyzer", "dictionary", "kwja", "frontend",
                "voicevox", "ankiConnect",
            )
        },
        "problems": [],
        "diagnostics": {"shutdownReason": "user-requested"},
    }
    (tmp_path / "startup-status.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    result = status_api.build_startup_status()
    assert result["overallStatus"] == "stopped"
    assert result["stale"] is True
    assert not any(
        problem["code"] == "SUPERVISOR_STATUS_STALE"
        for problem in result["problems"]
    )


def test_phase10_startup_source_has_no_fixed_dictionary_hash():
    root = Path(__file__).resolve().parents[1] / "app/startup"
    source = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in root.glob("*.py")
    )
    assert "C085D5ED805B287509AC5DC0AE26D0766AABA93C077F736D75EA19AD902C63CD" not in source
    assert "D2D926647AC7035C43971D57D46A270A7112FA21472CDD720879ABABA8E55D85" not in source
