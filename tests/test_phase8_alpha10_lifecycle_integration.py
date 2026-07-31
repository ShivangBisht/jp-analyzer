import hashlib

from app.analyzer.analyzer_decision_snapshot import _digest
from app.analyzer.teaching_corpus_export import build_export_preview, verify_export_artifact
from app.analyzer.teaching_decision_record import build_teaching_decision_record
from app.analyzer.teaching_decision_store import (
    get_record,
    integrity_report,
    persist_record,
    supersede_record,
)
from app.analyzer.teaching_quality_store import corpus_quality_summary, set_quality

SENTENCE = "\u4ea1\u304f\u306a\u3063\u305f\u4e8c\u4eba\u306f\u3068\u3066\u3082\u512a\u3057\u3044\u4eba\u9054\u3060\u3063\u305f\u3002"
BOUNDARY = {"start": len(SENTENCE) - 4, "end": len(SENTENCE) - 1, "surface": "\u3060\u3063\u305f"}


def snapshot():
    content = {
        "schemaVersion": "1.0",
        "source": {
            "sentence": SENTENCE,
            "sentenceSha256": hashlib.sha256(SENTENCE.encode("utf-8")).hexdigest(),
            "textLength": len(SENTENCE),
        },
        "analyzerIdentity": {},
        "dictionaryIdentity": {},
        "fullAnalysis": {},
        "coreDecision": {
            "candidates": [],
            "decisions": [],
            "conflicts": [],
            "resolvedSpans": [],
            "selectedPartition": {},
        },
        "readerDecision": {
            "compatibilitySpans": [],
            "candidates": [],
            "selection": {},
            "selectedSpans": [
                {"start": 0, "end": BOUNDARY["start"], "surface": SENTENCE[:BOUNDARY["start"]], "displayRole": "lexical"},
                {"start": BOUNDARY["start"], "end": BOUNDARY["start"] + 2, "surface": "\u3060\u3063", "displayRole": "function"},
                {"start": BOUNDARY["start"] + 2, "end": BOUNDARY["end"], "surface": "\u305f", "displayRole": "function"},
                {"start": BOUNDARY["end"], "end": len(SENTENCE), "surface": "\u3002", "displayRole": "punctuation"},
            ],
        },
        "generationObservability": {},
        "correctionContext": {"operationalCorrectionApplication": "disabled-for-snapshot"},
        "replayability": {},
    }
    digest = "sha256:" + _digest(content)
    return {
        "snapshotId": "ads-" + digest.split(":", 1)[1][:24],
        "capturedAt": "2026-07-31T00:00:00+00:00",
        "contentDigest": digest,
        **content,
    }


def decision(snap, *, failure, note):
    return build_teaching_decision_record(
        snap,
        boundary=BOUNDARY,
        judgment="corrected",
        classification={"assertedRole": "function"},
        approved_target={"targetSpans": [{**BOUNDARY, "displayRole": "function"}]},
        failure_classification=failure,
        confidence="preference",
        note=note,
    )


def test_superseded_history_is_retained_while_only_active_replacement_exports(tmp_path):
    db = tmp_path / "lifecycle.sqlite3"
    snap = snapshot()
    original = decision(snap, failure="boundary-error", note="Original visible symptom")
    replacement = decision(snap, failure="candidate-generation-miss", note="Replacement root diagnosis")

    persist_record(original, snapshot=snap, db_path=db)
    result = supersede_record(
        original["recordId"],
        replacement,
        note="Replace symptom diagnosis with root diagnosis",
        db_path=db,
    )

    set_quality(
        replacement["recordId"],
        "approved",
        reviewer="Lifecycle regression",
        quality_note="Active replacement approved",
        db_path=db,
    )

    old = get_record(original["recordId"], db_path=db)
    current = get_record(replacement["recordId"], db_path=db)
    summary = corpus_quality_summary(db_path=db)
    preview = build_export_preview(db_path=db)
    verification = verify_export_artifact(preview)

    assert result["superseded"]["lifecycle"]["status"] == "superseded"
    assert result["replacement"]["lifecycle"]["status"] == "active"
    assert old["lifecycle"]["status"] == "superseded"
    assert current["lifecycle"]["status"] == "active"
    assert any(
        event["event_type"] == "superseded"
        and event["related_record_id"] == replacement["recordId"]
        for event in old["storeEvents"]
    )

    assert summary["recordCount"] == 2
    assert summary["activeRecordCount"] == 1
    assert summary["duplicateGroupCount"] == 0
    assert summary["conflictCount"] == 0
    assert summary["exportEligibleCount"] == 1
    assert summary["exportEnabled"] is False

    assert preview["eligibleCount"] == 1
    assert preview["eligibleRecords"][0]["recordId"] == replacement["recordId"]
    assert preview["eligibleRecords"][0]["failureClassification"] == "candidate-generation-miss"
    assert original["recordId"] not in {item["recordId"] for item in preview["eligibleRecords"]}
    assert preview["exportEnabled"] is False
    assert preview["activationEnabled"] is False
    assert verification == {"ok": True, "problems": [], "schema": "TeachingCorpusExport.v1"}

    report = integrity_report(db)
    assert report["ok"] is True
    assert report["recordCount"] == 2
    assert report["snapshotCount"] == 1
    assert report["exportEnabled"] is False
