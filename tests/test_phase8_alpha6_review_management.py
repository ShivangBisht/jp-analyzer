from app.analyzer.teaching_review_management import diagnose_record


def test_diagnosis_reports_candidate_presence_and_safety_state():
    record = {
        "recordId": "tdr-test",
        "snapshotReference": {"snapshotId": "ads-test"},
        "decisionComparison": {
            "observedReaderSpan": {"start": 0, "end": 1, "surface": "猫"},
            "boundaryMatches": True,
            "classificationMatches": False,
            "identityCompared": True,
        },
        "approvedTarget": {"targetSpans": []},
        "failureClassification": "role-error",
        "qualityState": {"exportStatus": "excluded"},
        "operationalCorrectionLink": None,
    }
    result = diagnose_record(record)
    assert result["candidatePresent"] is True
    assert result["classificationMatches"] is False
    assert result["exportStatus"] == "excluded"
    assert result["operationalCorrectionLinked"] is False
