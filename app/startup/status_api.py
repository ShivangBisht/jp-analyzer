from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from app.analyzer.health import health_report

router = APIRouter(prefix="/startup", tags=["startup"])
STATUS_SCHEMA = "ApplicationStartupStatus.v1"
SUPERVISOR_SCHEMA = "ApplicationStartupSupervisor.v1"
HEARTBEAT_STALE_SECONDS = 30


def _runtime_directory() -> Path:
    return Path(os.environ.get("LOCALAPPDATA", Path.home())) / "JapaneseNovelMiner"


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _age_seconds(value: Any) -> float | None:
    captured = _parse_time(value)
    if captured is None:
        return None
    if captured.tzinfo is None:
        captured = captured.replace(tzinfo=timezone.utc)
    return max(0.0, (datetime.now(timezone.utc) - captured).total_seconds())


def _component(value: Any, *, required: bool) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    state = str(source.get("state") or "pending")
    if state not in {"pending", "starting", "ready", "degraded", "failed", "stopped"}:
        state = "pending"
    return {
        "required": bool(source.get("required", required)),
        "state": state,
        "detail": source.get("detail") if isinstance(source.get("detail"), str) else None,
        "url": source.get("url") if isinstance(source.get("url"), str) else None,
    }


def _problem(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    code = value.get("code")
    message = value.get("message")
    component = value.get("component")
    if not all(isinstance(item, str) and item for item in (code, message, component)):
        return None
    return {
        "code": code,
        "message": message,
        "component": component,
        "fatal": bool(value.get("fatal", False)),
        "detail": value.get("detail") if isinstance(value.get("detail"), str) else None,
        "suggestedAction": value.get("suggested_action") if isinstance(value.get("suggested_action"), str) else None,
    }


def _fallback_status(reason: str) -> dict[str, Any]:
    health = health_report()
    dictionary = health.get("dictionary") or health.get("dictionaryStatus") or {}
    dictionary_ready = bool(
        dictionary.get("ready")
        and dictionary.get("registryConsistent", True)
        and not dictionary.get("recoveryRequired", False)
    )
    return {
        "schema": STATUS_SCHEMA,
        "overallStatus": "degraded",
        "source": "runtime-fallback",
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "stale": True,
        "ageSeconds": None,
        "components": {
            "analyzer": {"required": True, "state": "ready", "detail": "JP Analyzer is responding.", "url": None},
            "dictionary": {
                "required": True,
                "state": "ready" if dictionary_ready else "failed",
                "detail": (
                    f"{dictionary.get('entryCount', 0)} entries; "
                    f"{dictionary.get('installedDictionaryCount', dictionary.get('dictionaryCount', 0))} dictionaries."
                    if dictionary_ready else "Dictionary is not ready or requires recovery."
                ),
                "url": None,
            },
            "kwja": {"required": True, "state": "degraded", "detail": "Supervisor status is unavailable.", "url": None},
            "frontend": {"required": True, "state": "ready", "detail": "The application interface is open.", "url": None},
            "voicevox": {"required": False, "state": "pending", "detail": "Not checked.", "url": None},
            "ankiConnect": {"required": False, "state": "pending", "detail": "Not checked.", "url": None},
        },
        "problems": [{
            "code": "SUPERVISOR_STATUS_UNAVAILABLE",
            "message": reason,
            "component": "application",
            "fatal": False,
            "detail": None,
            "suggestedAction": "Start the application with the Japanese Novel Miner launcher.",
        }],
        "diagnostics": {"logDirectory": str(_runtime_directory() / "logs")},
    }


def build_startup_status() -> dict[str, Any]:
    runtime = _runtime_directory()
    path = runtime / "startup-status.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return _fallback_status("No launcher status has been recorded.")
    except (OSError, json.JSONDecodeError):
        return _fallback_status("Launcher status could not be read.")
    if raw.get("schema") != SUPERVISOR_SCHEMA:
        return _fallback_status("Launcher status uses an unsupported schema.")

    source_components = raw.get("components") if isinstance(raw.get("components"), dict) else {}
    required = {"analyzer", "dictionary", "kwja", "frontend"}
    names = ["analyzer", "dictionary", "kwja", "frontend", "voicevox", "ankiConnect"]
    components = {
        name: _component(source_components.get(name), required=name in required)
        for name in names
    }
    problems = [item for item in (_problem(value) for value in raw.get("problems", [])) if item]
    age = _age_seconds(raw.get("capturedAt"))
    stale = age is None or age > HEARTBEAT_STALE_SECONDS
    overall = str(raw.get("overall_status") or "starting")
    if overall not in {"starting", "ready", "degraded", "failed", "stopped"}:
        overall = "starting"
    if stale and overall == "ready":
        overall = "degraded"
        problems.append({
            "code": "SUPERVISOR_STATUS_STALE",
            "message": "The launcher has stopped reporting current status.",
            "component": "application",
            "fatal": False,
            "detail": None,
            "suggestedAction": "Open diagnostics or restart with the Japanese Novel Miner launcher.",
        })

    return {
        "schema": STATUS_SCHEMA,
        "overallStatus": overall,
        "source": "supervisor",
        "capturedAt": raw.get("capturedAt"),
        "stale": stale,
        "ageSeconds": round(age, 1) if age is not None else None,
        "components": components,
        "problems": problems,
        "diagnostics": {"logDirectory": str(runtime / "logs")},
    }


@router.get("/status")
def startup_status():
    return build_startup_status()
