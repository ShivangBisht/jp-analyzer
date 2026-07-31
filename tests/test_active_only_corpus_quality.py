from app.analyzer import teaching_quality_store as quality_store


def _record(record_id, lifecycle, judgment="corrected", role="function"):
    return {
        "recordId": record_id,
        "sourceSentence": "äº¡ããªã£ãŸäºŒäººã¯â”€â”€ã¨ã¦ã‚‚å„ªã—ã„äººé”ã ã£ãŸã€‚",
        "lifecycle": {"status": lifecycle},
        "judgment": judgment,
        "assertions": {
            "boundary": {"start": 18, "end": 21, "surface": "ã ã£ãŸ"},
            "classification": {"assertedRole": role},
        },
    }


def test_superseded_history_does_not_create_duplicate_or_conflict(monkeypatch):
    records = [
        _record("tdr-old", "superseded"),
        _record("tdr-current", "active"),
    ]
    monkeypatch.setattr(quality_store, "list_records", lambda **kwargs: records)
    monkeypatch.setattr(
        quality_store,
        "get_quality",
        lambda record_id, **kwargs: {
            "record_id": record_id,
            "quality_status": "reviewed",
        },
    )
    summary = quality_store.corpus_quality_summary()
    assert summary["recordCount"] == 2
    assert summary["activeRecordCount"] == 1
    assert summary["duplicateGroupCount"] == 0
    assert summary["conflictCount"] == 0
    assert summary["exportEligibleCount"] == 0


def test_two_active_records_still_create_duplicate_group(monkeypatch):
    records = [_record("tdr-a", "active"), _record("tdr-b", "active")]
    monkeypatch.setattr(quality_store, "list_records", lambda **kwargs: records)
    monkeypatch.setattr(
        quality_store,
        "get_quality",
        lambda record_id, **kwargs: {
            "record_id": record_id,
            "quality_status": "approved",
        },
    )
    summary = quality_store.corpus_quality_summary()
    assert summary["activeRecordCount"] == 2
    assert summary["duplicateGroupCount"] == 1
    assert summary["duplicateGroups"][0]["count"] == 2
    assert summary["exportEligibleCount"] == 2
