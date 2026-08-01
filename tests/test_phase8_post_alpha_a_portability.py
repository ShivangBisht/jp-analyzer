import copy
import hashlib
import json
import sqlite3

import pytest

from app.analyzer.analyzer_decision_snapshot import _digest
from app.analyzer.teaching_decision_record import build_teaching_decision_record
from app.analyzer.teaching_decision_store import persist_record, supersede_record, integrity_report
from app.analyzer.teaching_quality_store import set_quality
from app.analyzer.teaching_portability import (
    apply_teaching_evidence_import,
    export_teaching_evidence,
    preview_teaching_evidence_import,
    verify_teaching_evidence,
)

SENTENCE = "\u4e8c\u4eba\u306f\u512a\u3057\u3044\u4eba\u9054\u3060\u3063\u305f\u3002"
START = SENTENCE.index("\u3060\u3063\u305f")
BOUNDARY = {"start": START, "end": START + 3, "surface": "\u3060\u3063\u305f"}


def snapshot():
    content = {
        "schemaVersion": "1.0",
        "source": {"sentence": SENTENCE, "sentenceSha256": hashlib.sha256(SENTENCE.encode()).hexdigest(), "textLength": len(SENTENCE)},
        "analyzerIdentity": {}, "dictionaryIdentity": {}, "fullAnalysis": {},
        "coreDecision": {"candidates": [], "decisions": [], "conflicts": [], "resolvedSpans": [], "selectedPartition": {}},
        "readerDecision": {"compatibilitySpans": [], "candidates": [], "selection": {}, "selectedSpans": [{"start": 0, "end": len(SENTENCE), "surface": SENTENCE, "displayRole": "unresolved"}]},
        "generationObservability": {}, "correctionContext": {"operationalCorrectionApplication": "disabled-for-snapshot"}, "replayability": {},
    }
    digest = "sha256:" + _digest(content)
    return {"snapshotId": "ads-" + digest.split(":")[1][:24], "capturedAt": "2026-08-01T00:00:00+00:00", "contentDigest": digest, **content}


def record(snap, failure, note):
    return build_teaching_decision_record(snap, boundary=BOUNDARY, judgment="corrected", classification={"assertedRole": "function"}, approved_target={"targetSpans": [{**BOUNDARY, "displayRole": "function"}]}, failure_classification=failure, note=note)


def source_store(path):
    snap = snapshot()
    old = record(snap, "boundary-error", "old")
    current = record(snap, "candidate-generation-miss", "current")
    persist_record(old, snapshot=snap, db_path=path)
    supersede_record(old["recordId"], current, note="refined diagnosis", db_path=path)
    set_quality(current["recordId"], "approved", reviewer="tester", quality_note="verified", db_path=path)
    return old, current


def test_round_trip_idempotency_and_history(tmp_path):
    source = tmp_path / "source.sqlite3"
    target = tmp_path / "target.sqlite3"
    old, current = source_store(source)
    package = export_teaching_evidence(db_path=source)
    assert verify_teaching_evidence(package)["ok"]

    preview = preview_teaching_evidence_import(package, db_path=target)
    assert preview["canApply"] and preview["counts"]["insert"] > 0
    applied = apply_teaching_evidence_import(package, confirm_package_digest=package["packageDigest"], db_path=target)
    assert applied["applied"] and not applied["idempotent"]
    assert integrity_report(target)["ok"]

    second = apply_teaching_evidence_import(package, confirm_package_digest=package["packageDigest"], db_path=target)
    assert second["idempotent"]
    assert second["postImportPreview"]["counts"]["alreadyPresent"] > 0
    assert second["postImportPreview"]["counts"]["conflict"] == 0

    exported_again = export_teaching_evidence(db_path=target)
    assert exported_again["sourceStoreIdentity"] == package["sourceStoreIdentity"]
    assert exported_again["counts"] == package["counts"]


def test_digest_tamper_is_blocked_without_writes(tmp_path):
    source = tmp_path / "source.sqlite3"
    target = tmp_path / "target.sqlite3"
    source_store(source)
    package = export_teaching_evidence(db_path=source)
    tampered = copy.deepcopy(package)
    tampered["records"][0]["payload"]["note"] = "tampered"
    preview = preview_teaching_evidence_import(tampered, db_path=target)
    assert not preview["canApply"]
    assert "package-digest-mismatch" in preview["actions"]["blocked"]
    with pytest.raises(ValueError):
        apply_teaching_evidence_import(tampered, confirm_package_digest=tampered["packageDigest"], db_path=target)
    assert not target.exists()


def test_same_id_different_content_is_reported_as_conflict(tmp_path):
    source = tmp_path / "source.sqlite3"
    target = tmp_path / "target.sqlite3"
    source_store(source)
    package = export_teaching_evidence(db_path=source)
    apply_teaching_evidence_import(package, confirm_package_digest=package["packageDigest"], db_path=target)
    with sqlite3.connect(target) as con:
        con.execute("UPDATE teaching_quality_state SET reviewer='other' WHERE record_id=?", (package["qualityStates"][0]["record_id"],))
        con.commit()
    preview = preview_teaching_evidence_import(package, db_path=target)
    assert not preview["canApply"]
    assert any(x["entity"] == "qualityStates" for x in preview["actions"]["conflict"])


def test_operational_corrections_dictionary_and_activation_are_excluded(tmp_path):
    source = tmp_path / "source.sqlite3"
    source_store(source)
    package = export_teaching_evidence(db_path=source)
    assert package["includesOperationalCorrections"] is False
    assert package["includesDictionary"] is False
    assert package["tuningEnabled"] is False
    assert package["activationEnabled"] is False
    encoded = json.dumps(package)
    assert "reader_corrections" not in encoded
    assert "phase8_analysis_lexicon" not in encoded


