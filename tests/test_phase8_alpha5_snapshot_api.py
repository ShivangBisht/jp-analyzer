from fastapi.testclient import TestClient
from app.analyzer.service import app
import app.analyzer.teaching_decision_api as api


def test_snapshot_is_stored_during_capture(
    monkeypatch,
    tmp_path,
):
    from app.analyzer import teaching_decision_api as api

    captured = {
        "snapshotId": "ads-test",
        "contentDigest": "sha256:" + "a" * 64,
        "source": {
            "sentence": "猫。",
            "sentenceSha256": "test",
        },
    }

    saved = []

    monkeypatch.setattr(
        api,
        "analyze_decision_snapshot",
        lambda text: captured,
    )
    monkeypatch.setattr(
        api,
        "save_snapshot",
        lambda snapshot: saved.append(snapshot),
    )

    result = api.snapshot(
        api.SnapshotRequest(sentence="猫。")
    )

    assert result is captured
    assert saved == [captured]


def test_snapshot_route_rejects_empty_sentence():
    response = TestClient(app).post("/teaching-decisions/snapshot", json={"sentence": ""})
    assert response.status_code == 422
