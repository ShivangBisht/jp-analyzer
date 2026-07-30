from pathlib import Path
import pytest
from fastapi import HTTPException
from app.analyzer.layers import dictionary_api, dictionary_store
from app.analyzer.analyzer_decision_snapshot import build_analyzer_decision_snapshot
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from test_analyzer_decision_snapshot import fixture


def test_delete_cache_endpoint_is_gone():
    with pytest.raises(HTTPException) as error:
        dictionary_api.delete_cache()
    assert error.value.status_code == 410
    assert error.value.detail["code"] == "DICTIONARY_CLEAR_DISABLED"


def test_clear_rejects_without_explicit_maintenance_context(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    with pytest.raises(PermissionError, match="DICTIONARY_CLEAR_DISABLED"):
        dictionary_store.clear()


def test_snapshot_rejects_not_ready_dictionary():
    empty = lambda: {"ready": False, "entryCount": 0, "dictionaryCount": 0, "installedDictionaries": []}
    with pytest.raises(RuntimeError, match="ANALYZER_SNAPSHOT_DICTIONARY_NOT_READY"):
        build_analyzer_decision_snapshot(fixture(), dictionary_status_fn=empty, analyzer_version="test")


def test_diagnostic_snapshot_can_explicitly_capture_not_ready():
    empty = lambda: {"ready": False, "entryCount": 0, "dictionaryCount": 0, "installedDictionaries": [], "database": "test.sqlite3"}
    snapshot = build_analyzer_decision_snapshot(fixture(), dictionary_status_fn=empty, analyzer_version="test", require_dictionary_ready=False)
    assert snapshot["dictionaryIdentity"]["ready"] is False
    assert snapshot["dictionaryIdentity"]["registryDigest"].startswith("sha256:")
