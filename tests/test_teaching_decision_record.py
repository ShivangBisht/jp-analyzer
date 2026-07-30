from copy import deepcopy
import pytest
from app.analyzer.teaching_decision_record import build_teaching_decision_record, validate_teaching_decision_record

SENTENCE = "黒い服を着た。"
SNAPSHOT = {
    "snapshotId": "ads-1234567890abcdef12345678",
    "contentDigest": "sha256:" + "a" * 64,
    "schemaVersion": "1.0",
    "source": {"sentence": SENTENCE},
    "readerDecision": {"selectedSpans": [
        {"start": 0, "end": 2, "surface": "黒い", "displayRole": "lexical"},
        {"start": 2, "end": 3, "surface": "服", "displayRole": "lexical"},
    ]},
}
BOUNDARY = {"start": 0, "end": 2, "surface": "黒い"}


def test_accepted_current_record_is_content_addressed_and_partial():
    record = build_teaching_decision_record(SNAPSHOT, boundary=BOUNDARY, judgment="accepted-current", classification={"assertedRole": "lexical"}, failure_classification="accepted-current")
    validate_teaching_decision_record(record)
    assert record["recordId"].startswith("tdr-")
    assert [x["state"] for x in record["reviewCoverage"]] == ["reviewed-accepted", "unreviewed"]
    assert record["qualityState"]["exportStatus"] == "excluded"


def test_corrected_record_preserves_user_asserted_identity():
    identity = {"status": "user-asserted-unconfirmed", "lookupKey": "黒い"}
    record = build_teaching_decision_record(SNAPSHOT, boundary=BOUNDARY, judgment="corrected", classification={"assertedRole": "vocabulary"}, identity=identity, approved_target={"displayRole": "lexical"}, failure_classification="role-error")
    assert record["assertions"]["classification"]["assertedRole"] == "vocabulary"
    assert record["assertions"]["identity"] == identity
    assert record["reviewCoverage"][0]["state"] == "reviewed-corrected"


def test_rejected_record_uses_reviewed_rejected():
    record = build_teaching_decision_record(SNAPSHOT, boundary=BOUNDARY, judgment="rejected", classification={"assertedRole": "none"}, failure_classification="hard-gate-error")
    assert record["reviewCoverage"][0]["state"] == "reviewed-rejected"


def test_tampering_is_rejected():
    record = build_teaching_decision_record(SNAPSHOT, boundary=BOUNDARY, judgment="accepted-current", classification={"assertedRole": "lexical"}, failure_classification="accepted-current")
    changed = deepcopy(record); changed["assertions"]["classification"]["assertedRole"] = "grammar"
    with pytest.raises(ValueError, match="digest mismatch"):
        validate_teaching_decision_record(changed)


def test_corrected_requires_target():
    with pytest.raises(ValueError, match="approvedTarget"):
        build_teaching_decision_record(SNAPSHOT, boundary=BOUNDARY, judgment="corrected", classification={"assertedRole": "lexical"}, failure_classification="boundary-error")
