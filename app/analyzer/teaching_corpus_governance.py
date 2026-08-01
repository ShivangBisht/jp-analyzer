from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from typing import Any

from .teaching_corpus_export import build_export_preview, verify_export_artifact
from .teaching_decision_store import integrity_report, list_records
from .teaching_quality_store import corpus_quality_summary, get_quality

SCHEMA = "TeachingCorpusGovernance.v1"
DEFAULT_POLICY = {
    "minimumTrainExamples": 8,
    "minimumCorrectedTrainExamples": 4,
    "minimumPreservationTrainExamples": 4,
    "minimumValidationExamples": 2,
    "minimumTestExamples": 2,
    "minimumFailureClasses": 2,
    "minimumAssertedRoles": 2,
    "minimumProvenanceGroups": 3,
    "requireNoDuplicateGroups": True,
    "requireNoConflicts": True,
    "requireNoProvenanceLeakage": True,
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _count(values):
    return dict(sorted(Counter(str(x or "unknown") for x in values).items()))


def _sentence_digest(record: dict[str, Any]) -> str:
    sentence = str(record.get("sourceSentence") or "")
    return hashlib.sha256(sentence.encode("utf-8")).hexdigest()


def _provenance(record: dict[str, Any]) -> dict[str, Any]:
    target = record.get("approvedTarget") or {}
    provenance = target.get("provenance") or {}
    book = provenance.get("bookId") or provenance.get("bookTitle")
    chapter = provenance.get("chapterIndex") if provenance.get("chapterIndex") is not None else provenance.get("chapterTitle")
    scene = provenance.get("sceneIndex") if provenance.get("sceneIndex") is not None else provenance.get("sceneTitle")
    sentence_sha = _sentence_digest(record)
    if book is not None:
        level = "book-chapter-scene"
        raw = {"book": str(book), "chapter": chapter, "scene": scene}
    else:
        level = "sentence"
        raw = {"sentenceSha256": sentence_sha}
    return {
        "groupId": "pvg-" + hashlib.sha256(_canonical(raw)).hexdigest()[:24],
        "level": level,
        "sentenceSha256": sentence_sha,
    }


def _maturity(level: str, passed: bool, status: str, reasons: list[str]) -> dict[str, Any]:
    return {"level": level, "passed": passed, "status": status, "reasons": reasons}


def build_corpus_governance_report(*, db_path=None, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    selected_policy = {**DEFAULT_POLICY, **(policy or {})}
    records = list_records(lifecycle_status=None, db_path=db_path)
    integrity = integrity_report(db_path)
    quality_summary = corpus_quality_summary(db_path=db_path)
    export = build_export_preview(db_path=db_path)
    export_verification = verify_export_artifact(export)
    split_by_id = {str(x["recordId"]): str(x["split"]) for x in export.get("eligibleRecords") or []}

    enriched = []
    for record in records:
        rid = str(record.get("recordId") or "")
        quality = get_quality(rid, db_path=db_path)
        provenance = _provenance(record)
        enriched.append({
            "recordId": rid,
            "lifecycle": str((record.get("lifecycle") or {}).get("status") or "unknown"),
            "judgment": str(record.get("judgment") or "unknown"),
            "failureClassification": str(record.get("failureClassification") or "unknown"),
            "assertedRole": str(((record.get("assertions") or {}).get("classification") or {}).get("assertedRole") or "unknown"),
            "qualityStatus": str(quality.get("quality_status") or "captured"),
            "reviewerPresent": bool(quality.get("reviewer")),
            "split": split_by_id.get(rid),
            "eligible": rid in split_by_id,
            "provenance": provenance,
        })

    active = [x for x in enriched if x["lifecycle"] == "active"]
    eligible = [x for x in enriched if x["eligible"]]
    historical = [x for x in enriched if x["lifecycle"] != "active"]

    provenance_splits: dict[str, set[str]] = defaultdict(set)
    provenance_records: dict[str, list[str]] = defaultdict(list)
    sentence_splits: dict[str, set[str]] = defaultdict(set)
    for item in eligible:
        group = item["provenance"]["groupId"]
        split = str(item["split"])
        provenance_splits[group].add(split)
        provenance_records[group].append(item["recordId"])
        sentence_splits[item["provenance"]["sentenceSha256"]].add(split)

    leakage = []
    for group, splits in sorted(provenance_splits.items()):
        if len(splits) > 1:
            leakage.append({"type": "provenance-group", "groupId": group, "splits": sorted(splits), "recordIds": sorted(provenance_records[group])})
    for sentence_sha, splits in sorted(sentence_splits.items()):
        if len(splits) > 1:
            leakage.append({"type": "sentence", "sentenceSha256": sentence_sha, "splits": sorted(splits)})

    split_counts = {name: int((export.get("splitCounts") or {}).get(name) or 0) for name in ("train", "validation", "test")}
    train = [x for x in eligible if x["split"] == "train"]
    failure_classes = sorted({x["failureClassification"] for x in eligible})
    roles = sorted({x["assertedRole"] for x in eligible})
    provenance_groups = sorted({x["provenance"]["groupId"] for x in eligible})
    corrected_train = sum(x["judgment"] == "corrected" for x in train)
    preservation_train = sum(x["judgment"] == "accepted-current" for x in train)

    harness_reasons = []
    if not integrity.get("ok"): harness_reasons.append("Teaching-store integrity has issues.")
    if not export_verification.get("ok"): harness_reasons.append("Corpus artifact verification failed.")
    if selected_policy["requireNoDuplicateGroups"] and quality_summary.get("duplicateGroupCount"): harness_reasons.append("Active duplicate groups remain.")
    if selected_policy["requireNoConflicts"] and quality_summary.get("conflictCount"): harness_reasons.append("Active conflicts remain.")
    if selected_policy["requireNoProvenanceLeakage"] and leakage: harness_reasons.append("Provenance leakage crosses corpus splits.")
    harness_ok = not harness_reasons

    gaps = []
    def require(actual, minimum, code, message):
        if actual < int(minimum): gaps.append({"code": code, "actual": actual, "required": int(minimum), "message": message})
    require(split_counts["train"], selected_policy["minimumTrainExamples"], "train-examples", "Collect more approved train examples.")
    require(corrected_train, selected_policy["minimumCorrectedTrainExamples"], "corrected-train", "Collect more corrected train examples.")
    require(preservation_train, selected_policy["minimumPreservationTrainExamples"], "preservation-train", "Collect more accepted-current preservation examples in train.")
    require(split_counts["validation"], selected_policy["minimumValidationExamples"], "validation-examples", "Collect approved validation evidence before candidate selection.")
    require(split_counts["test"], selected_policy["minimumTestExamples"], "test-examples", "Collect protected test evidence before final evaluation.")
    require(len(failure_classes), selected_policy["minimumFailureClasses"], "failure-classes", "Collect evidence across more failure classes.")
    require(len(roles), selected_policy["minimumAssertedRoles"], "asserted-roles", "Collect evidence across more Reader roles.")
    require(len(provenance_groups), selected_policy["minimumProvenanceGroups"], "provenance-groups", "Collect evidence from more independent provenance groups.")
    train_fit = harness_ok and not gaps

    maturity = {
        "harnessValid": _maturity("harness-valid", harness_ok, "passed" if harness_ok else "blocked", harness_reasons),
        "trainFit": _maturity("train-fit", train_fit, "passed" if train_fit else "insufficient", [x["message"] for x in gaps]),
        "validationPassed": _maturity("validation-passed", False, "not-evaluated" if split_counts["validation"] else "unavailable", ["Candidate validation has not been performed." if split_counts["validation"] else "Validation split is empty."]),
        "testPassed": _maturity("test-passed", False, "not-claimed", ["Protected test success is not claimed during corpus governance."]),
        "deploymentEligible": _maturity("deployment-eligible", False, "not-eligible", ["Deployment remains disabled in Phase 8."]),
    }

    recommendations = [x["message"] for x in gaps]
    if not recommendations and not train_fit:
        recommendations.append("Resolve governance blockers before tuning.")
    if train_fit:
        recommendations.append("Corpus meets the configured collection gate; define the later tuning handoff before deriving candidates.")

    core = {
        "schema": SCHEMA,
        "mode": "governance-read-only",
        "tuningEnabled": False,
        "activationEnabled": False,
        "deploymentEnabled": False,
        "policy": selected_policy,
        "corpusDigest": export.get("corpusDigest"),
        "counts": {
            "records": len(enriched),
            "active": len(active),
            "historical": len(historical),
            "approved": int(quality_summary.get("approvedCount") or 0),
            "eligible": len(eligible),
            "excluded": int(export.get("excludedCount") or 0),
            "duplicateGroups": int(quality_summary.get("duplicateGroupCount") or 0),
            "conflicts": int(quality_summary.get("conflictCount") or 0),
            "provenanceGroups": len(provenance_groups),
            "leakageFindings": len(leakage),
        },
        "coverage": {
            "byJudgment": _count(x["judgment"] for x in active),
            "byFailureClassification": _count(x["failureClassification"] for x in active),
            "byAssertedRole": _count(x["assertedRole"] for x in active),
            "byLifecycle": _count(x["lifecycle"] for x in enriched),
            "byQualityStatus": _count(x["qualityStatus"] for x in enriched),
            "byReviewerPresence": {"present": sum(x["reviewerPresent"] for x in enriched), "missing": sum(not x["reviewerPresent"] for x in enriched)},
            "bySplit": split_counts,
            "correctedTrain": corrected_train,
            "preservationTrain": preservation_train,
        },
        "provenance": {
            "groupCount": len(provenance_groups),
            "groups": [{"groupId": group, "recordCount": len(provenance_records[group]), "splits": sorted(provenance_splits[group])} for group in provenance_groups],
            "leakage": leakage,
        },
        "quality": {
            "integrity": deepcopy(integrity),
            "duplicateGroups": deepcopy(quality_summary.get("duplicateGroups") or []),
            "conflicts": deepcopy(quality_summary.get("conflicts") or []),
            "exportVerification": deepcopy(export_verification),
        },
        "maturity": maturity,
        "gaps": gaps,
        "recommendations": recommendations,
    }
    core["reportDigest"] = _digest(core)
    return core


def verify_corpus_governance_report(report: dict[str, Any]) -> dict[str, Any]:
    problems = []
    if report.get("schema") != SCHEMA: problems.append("unsupported-schema")
    if report.get("mode") != "governance-read-only": problems.append("mode-must-be-governance-read-only")
    for key in ("tuningEnabled", "activationEnabled", "deploymentEnabled"):
        if report.get(key) is not False: problems.append(key + "-must-be-false")
    core = {k: v for k, v in report.items() if k != "reportDigest"}
    if report.get("reportDigest") != _digest(core): problems.append("report-digest-mismatch")
    return {"ok": not problems, "problems": problems, "schema": SCHEMA, "reportDigest": report.get("reportDigest")}
