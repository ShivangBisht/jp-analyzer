from copy import deepcopy

from app.analyzer import teaching_corpus_export as corpus_export


def _valid_record():
    return {
        "recordId": "tdr-example",
        "contentDigest": "sha256:" + "a" * 64,
        "lifecycle": {"status": "active"},
        "snapshotReference": {"snapshotId": "ads-example"},
        "judgment": "corrected",
        "assertions": {"boundary": {"start": 0, "end": 3, "surface": "ã ã£ãŸ"}},
        "approvedTarget": None,
        "failureClassification": "candidate-generation-miss",
        "_quality": {"quality_status": "approved"},
        "storeEvents": [{"event_type": "created"}],
    }


def test_runtime_store_events_are_removed_only_for_formal_validation(monkeypatch):
    record = _valid_record()
    original = deepcopy(record)
    captured = {}

    def validate(value):
        captured.update(value)

    monkeypatch.setattr(corpus_export, "validate_teaching_decision_record", validate)
    assert corpus_export._record_digest_valid(record) is True
    assert "storeEvents" not in captured
    assert record == original
    assert record["storeEvents"] == [{"event_type": "created"}]


def test_invalid_immutable_payload_still_fails(monkeypatch):
    def reject(value):
        raise ValueError("digest mismatch")

    monkeypatch.setattr(corpus_export, "validate_teaching_decision_record", reject)
    assert corpus_export._record_digest_valid(_valid_record()) is False


def test_active_approved_hydrated_record_is_eligible(monkeypatch):
    record = _valid_record()
    monkeypatch.setattr(corpus_export, "_record_digest_valid", lambda value: True)
    monkeypatch.setattr(
        corpus_export,
        "corpus_quality_summary",
        lambda **kwargs: {"conflicts": [], "duplicateGroups": []},
    )
    result = corpus_export.build_export_preview(records=[record])
    assert result["eligibleCount"] == 1
    assert result["excludedCount"] == 0
    assert result["exportEnabled"] is False
    assert result["activationEnabled"] is False
