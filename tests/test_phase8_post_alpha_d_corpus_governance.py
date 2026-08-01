from app.analyzer.teaching_corpus_governance import build_corpus_governance_report, verify_corpus_governance_report


def _record(rid, *, judgment="corrected", failure="boundary-error", role="lexical", lifecycle="active", quality="approved", sentence="sentence", provenance=None):
    return {
        "recordId": rid,
        "sourceSentence": sentence,
        "judgment": judgment,
        "failureClassification": failure,
        "assertions": {"classification": {"assertedRole": role}},
        "approvedTarget": {"provenance": provenance or {}},
        "lifecycle": {"status": lifecycle},
        "_quality": {"quality_status": quality},
    }


def _install(monkeypatch, records, eligible):
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.list_records", lambda **kwargs: records)
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.integrity_report", lambda path=None: {"ok": True, "issueCount": 0})
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.corpus_quality_summary", lambda **kwargs: {"approvedCount": len(eligible), "duplicateGroupCount": 0, "duplicateGroups": [], "conflictCount": 0, "conflicts": []})
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.get_quality", lambda rid, **kwargs: next(x["_quality"] for x in records if x["recordId"] == rid))
    artifact = {"schema":"TeachingCorpusExport.v1","mode":"dry-run","exportEnabled":False,"activationEnabled":False,"splitPolicy":{"train":80,"validation":10,"test":10},"eligibleRecords":eligible,"excludedRecords":[],"excludedCount":0,"splitCounts":{s:sum(x["split"]==s for x in eligible) for s in ("train","validation","test")},"corpusDigest":"sha256:"+"a"*64}
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.build_export_preview", lambda **kwargs: artifact)
    monkeypatch.setattr("app.analyzer.teaching_corpus_governance.verify_export_artifact", lambda value: {"ok": True, "problems": [], "schema":"TeachingCorpusExport.v1"})


def test_small_corpus_is_harness_valid_but_not_train_fit(monkeypatch):
    records=[_record("a",sentence="independent train sentence",provenance={"bookId":"book-a","chapterIndex":1,"sceneIndex":1}),_record("b",judgment="accepted-current",failure="accepted-current",sentence="independent test sentence",provenance={"bookId":"book-b","chapterIndex":1,"sceneIndex":1})]
    eligible=[{"recordId":"a","split":"train"},{"recordId":"b","split":"test"}]
    _install(monkeypatch,records,eligible)
    report=build_corpus_governance_report()
    assert report["maturity"]["harnessValid"]["passed"] is True
    assert report["maturity"]["trainFit"]["passed"] is False
    assert report["maturity"]["validationPassed"]["status"] == "unavailable"
    assert report["maturity"]["testPassed"]["status"] == "not-claimed"
    assert report["maturity"]["deploymentEligible"]["passed"] is False
    assert verify_corpus_governance_report(report)["ok"] is True


def test_provenance_leakage_blocks_harness(monkeypatch):
    provenance={"bookId":"book","chapterIndex":1,"sceneIndex":1}
    records=[_record("a",provenance=provenance),_record("b",provenance=provenance)]
    eligible=[{"recordId":"a","split":"train"},{"recordId":"b","split":"test"}]
    _install(monkeypatch,records,eligible)
    report=build_corpus_governance_report()
    assert report["counts"]["leakageFindings"] > 0
    assert report["maturity"]["harnessValid"]["passed"] is False


def test_report_is_deterministic_and_read_only(monkeypatch):
    records=[_record("a")]
    eligible=[{"recordId":"a","split":"train"}]
    _install(monkeypatch,records,eligible)
    first=build_corpus_governance_report(); second=build_corpus_governance_report()
    assert first["reportDigest"] == second["reportDigest"]
    assert first["tuningEnabled"] is False
    assert first["activationEnabled"] is False
    assert first["deploymentEnabled"] is False
    first["deploymentEnabled"] = True
    assert verify_corpus_governance_report(first)["ok"] is False

