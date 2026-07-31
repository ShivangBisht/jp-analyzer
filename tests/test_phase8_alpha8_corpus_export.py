from app.analyzer.teaching_corpus_export import build_export_preview, verify_export_artifact


def _record(record_id, *, lifecycle="active", quality="approved"):
    return {
        "recordId": record_id,
        "recordVersion": "TeachingDecisionRecord.v1",
        "recordDigest": "sha256:" + "a" * 64,
        "snapshotReference": {"snapshotId": "ads-" + record_id},
        "lifecycle": {"status": lifecycle},
        "judgment": "accepted-current",
        "assertions": {"boundary": {"start": 0, "end": 1, "surface": "猫"}, "classification": {"assertedRole": "lexical"}},
        "approvedTarget": None,
        "failureClassification": "accepted-current",
        "_quality": {"quality_status": quality},
    }


def test_preview_is_deterministic_and_dry_run(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_corpus_export._record_digest_valid", lambda record: True)
    first = build_export_preview(records=[_record("b"), _record("a")])
    second = build_export_preview(records=[_record("a"), _record("b")])
    assert first["corpusDigest"] == second["corpusDigest"]
    assert [x["recordId"] for x in first["eligibleRecords"]] == ["a", "b"]
    assert first["exportEnabled"] is False
    assert first["activationEnabled"] is False
    assert verify_export_artifact(first)["ok"] is True


def test_preview_excludes_nonapproved_and_inactive(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_corpus_export._record_digest_valid", lambda record: True)
    result = build_export_preview(records=[_record("captured", quality="captured"), _record("old", lifecycle="retracted")])
    assert result["eligibleCount"] == 0
    reasons = {item["recordId"]: item["reasons"] for item in result["excludedRecords"]}
    assert "quality:captured" in reasons["captured"]
    assert "lifecycle:retracted" in reasons["old"]


def test_verifier_rejects_digest_tampering(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_corpus_export._record_digest_valid", lambda record: True)
    artifact = build_export_preview(records=[_record("a")])
    artifact["eligibleRecords"][0]["judgment"] = "rejected"
    assert verify_export_artifact(artifact)["ok"] is False
