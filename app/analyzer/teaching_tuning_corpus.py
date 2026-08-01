from __future__ import annotations


PRIVATE_REDACTION_KEYS = {
    "sourceSentence",
    "note",
    "bookTitle",
    "bookId",
    "database",
    "databasePath",
    "lastSyncId",
    "chapterTitle",
    "sceneTitle",
    "leftContext",
    "rightContext",
    "reviewer",
    "qualityNote",
    "quality_note",
    "localPath",
    "databasePath",
    "sourceStorePath",
    "readerLibraryId",
}


def _redact_private_fields(value):
    """Recursively remove private metadata from a shareable package."""
    if isinstance(value, dict):
        return {
            key: _redact_private_fields(item)
            for key, item in value.items()
            if key not in PRIVATE_REDACTION_KEYS
        }

    if isinstance(value, list):
        return [
            _redact_private_fields(item)
            for item in value
        ]

    return value
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from .layers.dictionary_store import status as dictionary_status
from .teaching_corpus_export import build_export_preview
from .teaching_decision_store import get_record, get_snapshot
from .teaching_quality_store import get_quality

SCHEMA = "TeachingTuningCorpus.v1"
PROFILES = {"private-local", "redacted-shareable"}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _dictionary_identity() -> dict[str, Any]:
    s = dictionary_status()
    installed = [
        {
            "stableIdentity": x.get("stableIdentity"),
            "dictionaryType": x.get("dictionaryType"),
            "priority": x.get("priority"),
            "entryCount": x.get("entryCount"),
            "contentDigest": x.get("contentDigest"),
            "revision": x.get("revision"),
            "enabled": x.get("enabled"),
        }
        for x in (s.get("installedDictionaries") or [])
    ]
    identity = {
        "ready": bool(s.get("ready")),
        "entryCount": int(s.get("entryCount") or 0),
        "dictionaryCount": int(s.get("dictionaryCount") or 0),
        "typeCounts": dict(s.get("typeCounts") or {}),
        "registryConsistent": bool(s.get("registryConsistent")),
        "installedDictionaries": installed,
    }
    identity["identityDigest"] = _digest(identity)
    return identity


def _baseline(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshotId": snapshot.get("snapshotId"),
        "snapshotDigest": snapshot.get("contentDigest"),
        "schemaVersion": snapshot.get("schemaVersion"),
        "source": deepcopy(snapshot.get("source") or {}),
        "analyzerIdentity": deepcopy(snapshot.get("analyzerIdentity") or {}),
        "dictionaryIdentity": deepcopy(snapshot.get("dictionaryIdentity") or {}),
        "readerDecision": deepcopy(snapshot.get("readerDecision") or {}),
        "coreDecision": deepcopy(snapshot.get("coreDecision") or {}),
        "generationObservability": deepcopy(snapshot.get("generationObservability") or {}),
        "correctionContext": deepcopy(snapshot.get("correctionContext") or {}),
    }


def _private_example(item: dict[str, Any], *, db_path=None) -> dict[str, Any]:
    rid = str(item["recordId"])
    record = get_record(rid, db_path=db_path)
    snapshot = get_snapshot(str(item["snapshotId"]), db_path=db_path)
    quality = get_quality(rid, db_path=db_path)
    return {
        "recordId": rid,
        "recordDigest": record.get("contentDigest"),
        "split": item.get("split"),
        "sourceSentence": record.get("sourceSentence"),
        "reviewCoverage": deepcopy(record.get("reviewCoverage") or []),
        "judgment": record.get("judgment"),
        "assertions": deepcopy(record.get("assertions") or {}),
        "approvedTarget": deepcopy(record.get("approvedTarget")),
        "failureClassification": record.get("failureClassification"),
        "confidence": record.get("confidence"),
        "qualityApproval": {
            "status": quality.get("quality_status"),
            "reviewer": quality.get("reviewer"),
            "qualityNote": quality.get("quality_note"),
            "updatedAt": quality.get("updated_at"),
        },
        "baseline": _baseline(snapshot),
    }


def _redact_example(example: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(example)
    sentence = str(out.pop("sourceSentence", ""))
    out["sourceIdentity"] = {
        "sentenceSha256": hashlib.sha256(sentence.encode("utf-8")).hexdigest(),
        "textLength": len(sentence),
    }
    out["reviewCoverage"] = [
        {"range": {"start": x.get("range", {}).get("start"), "end": x.get("range", {}).get("end")}, "state": x.get("state")}
        for x in out.get("reviewCoverage", [])
    ]
    assertions = out.get("assertions") or {}
    if assertions.get("boundary"):
        assertions["boundary"].pop("surface", None)
    target = out.get("approvedTarget") or {}
    for span in target.get("targetSpans") or []:
        span.pop("surface", None)
    baseline = out.get("baseline") or {}
    source = baseline.get("source") or {}
    source.pop("sentence", None)
    baseline["readerDecision"] = {
        "selectedSpans": [
            {k: v for k, v in span.items() if k not in {"surface", "preferredLookupKey", "headword"}}
            for span in ((baseline.get("readerDecision") or {}).get("selectedSpans") or [])
        ],
        "candidateCount": len((baseline.get("readerDecision") or {}).get("candidates") or []),
    }
    baseline["coreDecision"] = {
        "candidateCount": len((baseline.get("coreDecision") or {}).get("candidates") or []),
        "resolvedSpanCount": len((baseline.get("coreDecision") or {}).get("resolvedSpans") or []),
    }
    out["qualityApproval"].pop("reviewer", None)
    out["qualityApproval"].pop("qualityNote", None)
    return out


def build_tuning_corpus_package(profile: str = "private-local", *, db_path=None) -> dict[str, Any]:
    if profile not in PROFILES:
        raise ValueError("unsupported corpus package profile")
    preview = build_export_preview(db_path=db_path)
    examples = [_private_example(item, db_path=db_path) for item in preview.get("eligibleRecords") or []]
    if profile == "redacted-shareable":
        examples = [_redact_example(x) for x in examples]
    examples.sort(key=lambda x: x["recordId"])
    core = {
        "schema": SCHEMA,
        "profile": profile,
        "mode": "corpus-packaging-only",
        "tuningEnabled": False,
        "activationEnabled": False,
        "deploymentEnabled": False,
        "includesSqliteBytes": False,
        "includesOperationalCorrections": False,
        "corpusDigest": preview.get("corpusDigest"),
        "splitPolicy": deepcopy(preview.get("splitPolicy") or {}),
        "splitCounts": deepcopy(preview.get("splitCounts") or {}),
        "dictionaryIdentity": _dictionary_identity(),
        "examples": examples,
        "counts": {"examples": len(examples)},
    }
    if profile == "redacted-shareable":
        core = _redact_private_fields(core)

    core["packageDigest"] = _digest(core)
    return core


def verify_tuning_corpus_package(package: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if package.get("schema") != SCHEMA:
        problems.append("unsupported-schema")
    if package.get("profile") not in PROFILES:
        problems.append("unsupported-profile")
    for key in ("tuningEnabled", "activationEnabled", "deploymentEnabled", "includesSqliteBytes", "includesOperationalCorrections"):
        if package.get(key) is not False:
            problems.append(f"{key}-must-be-false")
    core = {k: v for k, v in package.items() if k != "packageDigest"}
    if package.get("packageDigest") != _digest(core):
        problems.append("package-digest-mismatch")
    examples = package.get("examples") or []
    ids = [x.get("recordId") for x in examples]
    if ids != sorted(ids) or None in ids or len(ids) != len(set(ids)):
        problems.append("example-order-or-identity-invalid")
    if (package.get("counts") or {}).get("examples") != len(examples):
        problems.append("example-count-mismatch")
    if package.get("profile") == "private-local":
        for x in examples:
            if not isinstance(x.get("sourceSentence"), str): problems.append(f"private-source-missing:{x.get('recordId')}")
            if not (x.get("baseline") or {}).get("readerDecision"): problems.append(f"baseline-missing:{x.get('recordId')}")
    if package.get("profile") == "redacted-shareable":
        encoded = json.dumps(package, ensure_ascii=False)
        forbidden = ["sourceSentence", "qualityNote", "reviewer", "database", "bookTitle", "bookId", "chapterTitle", "sceneTitle", "leftContext", "rightContext", "lastSyncId", "D:\\"]
        for term in forbidden:
            if term in encoded: problems.append(f"redaction-failed:{term}")
    return {"ok": not problems, "problems": problems, "schema": SCHEMA, "profile": package.get("profile"), "packageDigest": package.get("packageDigest")}




