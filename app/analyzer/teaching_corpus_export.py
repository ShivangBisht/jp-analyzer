from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any, Iterable

from .teaching_decision_record import validate_teaching_decision_record
from .teaching_decision_store import get_snapshot, list_records
from .teaching_quality_store import corpus_quality_summary, get_quality

EXPORT_SCHEMA = "TeachingCorpusExport.v1"
SPLIT_POLICY = {"train": 80, "validation": 10, "test": 10}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _split(record_id: str) -> str:
    bucket = int(hashlib.sha256(record_id.encode("utf-8")).hexdigest()[:8], 16) % 100
    if bucket < 80:
        return "train"
    if bucket < 90:
        return "validation"
    return "test"


def _record_digest_valid(record: dict[str, Any]) -> bool:
    try:
        validate_teaching_decision_record(record)
        return True
    except (TypeError, ValueError):
        return False


def build_export_preview(*, records: Iterable[dict[str, Any]] | None = None, db_path=None) -> dict[str, Any]:
    source = list(records) if records is not None else list_records(lifecycle_status=None, db_path=db_path)
    quality_summary = corpus_quality_summary(db_path=db_path)
    conflicting_ids = {record_id for group in quality_summary["conflicts"] for record_id in group["recordIds"]}
    duplicate_ids = {record_id for group in quality_summary["duplicateGroups"] for record_id in group["recordIds"]}
    eligible: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for record in source:
        record_id = str(record.get("recordId") or "")
        reasons: list[str] = []
        lifecycle = str((record.get("lifecycle") or {}).get("status") or "unknown")
        quality = get_quality(record_id, db_path=db_path) if records is None else record.get("_quality", {"quality_status": "captured"})
        quality_status = str(quality.get("quality_status") or "captured")
        if lifecycle != "active":
            reasons.append(f"lifecycle:{lifecycle}")
        if quality_status != "approved":
            reasons.append(f"quality:{quality_status}")
        if record_id in conflicting_ids:
            reasons.append("unresolved-conflict")
        if record_id in duplicate_ids:
            reasons.append("duplicate-group")
        if not _record_digest_valid(record):
            reasons.append("invalid-record-digest")
        snapshot_id = str((record.get("snapshotReference") or {}).get("snapshotId") or "")
        if not snapshot_id:
            reasons.append("missing-snapshot-reference")
        elif records is None:
            try:
                get_snapshot(snapshot_id, db_path=db_path)
            except ValueError:
                reasons.append("missing-authoritative-snapshot")

        if reasons:
            excluded.append({"recordId": record_id, "reasons": sorted(set(reasons))})
            continue

        eligible.append({
            "recordId": record_id,
            "recordDigest": record.get("recordDigest") or record.get("contentDigest"),
            "snapshotId": snapshot_id,
            "judgment": record.get("judgment"),
            "assertions": record.get("assertions"),
            "approvedTarget": record.get("approvedTarget"),
            "failureClassification": record.get("failureClassification"),
            "split": _split(record_id),
        })

    eligible.sort(key=lambda item: item["recordId"])
    excluded.sort(key=lambda item: item["recordId"])
    split_counts = dict(Counter(item["split"] for item in eligible))
    for name in SPLIT_POLICY:
        split_counts.setdefault(name, 0)

    manifest_core = {
        "schema": EXPORT_SCHEMA,
        "mode": "dry-run",
        "exportEnabled": False,
        "activationEnabled": False,
        "splitPolicy": SPLIT_POLICY,
        "eligibleRecords": eligible,
        "excludedRecords": excluded,
    }
    return {
        **manifest_core,
        "eligibleCount": len(eligible),
        "excludedCount": len(excluded),
        "splitCounts": split_counts,
        "corpusDigest": _sha256(manifest_core),
    }


def verify_export_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if artifact.get("schema") != EXPORT_SCHEMA:
        problems.append("unsupported-schema")
    if artifact.get("mode") != "dry-run":
        problems.append("mode-must-be-dry-run")
    if artifact.get("exportEnabled") is not False:
        problems.append("export-must-remain-disabled")
    if artifact.get("activationEnabled") is not False:
        problems.append("activation-must-remain-disabled")
    record_ids = [item.get("recordId") for item in artifact.get("eligibleRecords", [])]
    if record_ids != sorted(record_ids):
        problems.append("eligible-record-order-not-deterministic")
    core = {key: artifact.get(key) for key in ["schema", "mode", "exportEnabled", "activationEnabled", "splitPolicy", "eligibleRecords", "excludedRecords"]}
    if artifact.get("corpusDigest") != _sha256(core):
        problems.append("corpus-digest-mismatch")
    return {"ok": not problems, "problems": problems, "schema": EXPORT_SCHEMA}
