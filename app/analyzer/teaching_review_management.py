from __future__ import annotations
from collections import Counter
from typing import Any
from .teaching_decision_store import integrity_report, list_records


def review_summary() -> dict[str, Any]:
    records = list_records(lifecycle_status=None)
    judgment = Counter(str(x.get("judgment") or "unknown") for x in records)
    lifecycle = Counter(str((x.get("lifecycle") or {}).get("status") or "unknown") for x in records)
    failures = Counter(str(x.get("failureClassification") or "unclassified") for x in records)
    reviewed = sum(1 for x in records if (x.get("qualityState") or {}).get("reviewStatus") == "reviewed")
    linked = sum(1 for x in records if x.get("operationalCorrectionLink"))
    sentences = {str((x.get("snapshotReference") or {}).get("snapshotId") or "") for x in records}
    integrity = integrity_report()
    return {
        "recordCount": len(records),
        "sentenceSnapshotCount": len({x for x in sentences if x}),
        "byJudgment": dict(sorted(judgment.items())),
        "byLifecycle": dict(sorted(lifecycle.items())),
        "byFailureClassification": dict(sorted(failures.items())),
        "reviewedCount": reviewed,
        "operationalCorrectionLinkCount": linked,
        "integrity": {"ok": integrity["ok"], "issueCount": integrity["issueCount"]},
        "exportEnabled": False,
        "operationalActivationEnabled": False,
    }


def diagnose_record(record: dict[str, Any]) -> dict[str, Any]:
    comparison = record.get("decisionComparison") or {}
    observed = comparison.get("observedReaderSpan")
    target = record.get("approvedTarget") or {}
    snapshot_ref = record.get("snapshotReference") or {}
    return {
        "recordId": record.get("recordId"),
        "snapshotId": snapshot_ref.get("snapshotId"),
        "candidatePresent": observed is not None,
        "boundaryMatches": bool(comparison.get("boundaryMatches")),
        "classificationMatches": bool(comparison.get("classificationMatches")),
        "identityCompared": bool(comparison.get("identityCompared")),
        "observedReaderSpan": observed,
        "approvedTarget": target or None,
        "failureClassification": record.get("failureClassification"),
        "operationalCorrectionLinked": bool(record.get("operationalCorrectionLink")),
        "exportStatus": (record.get("qualityState") or {}).get("exportStatus"),
    }
