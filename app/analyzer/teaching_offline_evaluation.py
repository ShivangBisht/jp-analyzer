from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any, Iterable

from .teaching_corpus_export import build_export_preview, verify_export_artifact

EXPERIMENT_SCHEMA = "TeachingOfflineExperiment.v1"
METRIC_NAMES = (
    "candidateGenerationRecall",
    "boundaryAccuracy",
    "classificationAccuracy",
    "identityAccuracy",
    "abstentionAccuracy",
    "partitionAccuracy",
)
DEFAULT_POLICY = {
    "minimumValidationDelta": 0.0,
    "maximumTestRegression": 0.0,
    "requireNoTestLeakage": True,
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _expected(record: dict[str, Any]) -> dict[str, Any]:
    assertions = record.get("assertions") or {}
    boundary = assertions.get("boundary") or {}
    classification = assertions.get("classification") or {}
    identity = assertions.get("identity") or {}
    return {
        "candidatePresent": True,
        "boundary": [boundary.get("start"), boundary.get("end")],
        "classification": classification.get("assertedRole"),
        "identity": identity.get("assertedIdentity") or identity.get("identityKey"),
        "abstained": False,
        "partitionCorrect": True,
    }


def _baseline(record: dict[str, Any]) -> dict[str, Any]:
    expected = _expected(record)
    correct = record.get("judgment") == "accepted-current"
    if correct:
        return expected
    failure = str(record.get("failureClassification") or "unclassified")
    prediction = dict(expected)
    if failure in {"candidate-generation-miss", "hard-gate-error"}:
        prediction["candidatePresent"] = False
        prediction["boundary"] = None
        prediction["classification"] = None
        prediction["identity"] = None
        prediction["partitionCorrect"] = False
    if failure in {"boundary-error", "partition-optimization-error"}:
        prediction["boundary"] = [None, None]
        prediction["partitionCorrect"] = False
    if failure in {"role-error", "ranking-error"}:
        prediction["classification"] = None
    if failure == "identity-error":
        prediction["identity"] = None
    if failure == "abstention-error":
        prediction["abstained"] = True
    if failure == "unclassified":
        prediction["classification"] = None
    return prediction


def _score(expected: dict[str, Any], prediction: dict[str, Any]) -> dict[str, int | None]:
    candidate_present = bool(prediction.get("candidatePresent"))
    return {
        "candidateGenerationRecall": int(candidate_present),
        "boundaryAccuracy": int(prediction.get("boundary") == expected.get("boundary")) if candidate_present else None,
        "classificationAccuracy": int(prediction.get("classification") == expected.get("classification")) if candidate_present else None,
        "identityAccuracy": int(prediction.get("identity") == expected.get("identity")) if candidate_present else None,
        "abstentionAccuracy": int(bool(prediction.get("abstained")) == bool(expected.get("abstained"))),
        "partitionAccuracy": int(candidate_present and bool(prediction.get("partitionCorrect")) == bool(expected.get("partitionCorrect"))),
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(rows)
    metrics: dict[str, float | None] = {}
    metric_counts: dict[str, int] = {}
    for name in METRIC_NAMES:
        values = [row["scores"][name] for row in rows if row["scores"][name] is not None]
        metric_counts[name] = len(values)
        metrics[name] = sum(values) / len(values) if values else None
    return {"recordCount": count, "metricCounts": metric_counts, "metrics": metrics}


def build_offline_experiment(
    *,
    corpus: dict[str, Any] | None = None,
    candidate_predictions: dict[str, dict[str, Any]] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    artifact = corpus or build_export_preview()
    verification = verify_export_artifact(artifact)
    if not verification["ok"]:
        raise ValueError("corpus export artifact is invalid: " + ", ".join(verification["problems"]))
    selected_policy = {**DEFAULT_POLICY, **(policy or {})}
    candidate_predictions = candidate_predictions or {}
    rows: list[dict[str, Any]] = []
    split_seen: dict[str, set[str]] = {"train": set(), "validation": set(), "test": set()}

    for record in artifact.get("eligibleRecords", []):
        record_id = str(record["recordId"])
        split = str(record["split"])
        split_seen.setdefault(split, set()).add(record_id)
        expected = _expected(record)
        before = _baseline(record)
        after = candidate_predictions.get(record_id, before)
        rows.append({
            "recordId": record_id,
            "split": split,
            "expected": expected,
            "beforePrediction": before,
            "afterPrediction": after,
            "beforeScores": _score(expected, before),
            "afterScores": _score(expected, after),
        })

    leakage = sorted((split_seen["train"] & split_seen["validation"]) | (split_seen["train"] & split_seen["test"]) | (split_seen["validation"] & split_seen["test"]))
    before_by_split = {}
    after_by_split = {}
    for split in ("train", "validation", "test"):
        subset = [row for row in rows if row["split"] == split]
        before_by_split[split] = _aggregate([{"scores": row["beforeScores"]} for row in subset])
        after_by_split[split] = _aggregate([{"scores": row["afterScores"]} for row in subset])

    deltas = {}
    regressions = []
    for split in ("train", "validation", "test"):
        deltas[split] = {}
        for name in METRIC_NAMES:
            before = before_by_split[split]["metrics"][name]
            after = after_by_split[split]["metrics"][name]
            if before is None and after is not None:
                delta = after
            elif before is not None and after is None:
                delta = -before
            elif before is None and after is None:
                delta = None
            else:
                delta = after - before
            deltas[split][name] = delta
            if split == "test" and delta is not None and delta < -float(selected_policy["maximumTestRegression"]):
                regressions.append({"split": split, "metric": name, "delta": delta})

    validation_deltas = [value for value in deltas["validation"].values() if value is not None]
    validation_pass = not validation_deltas or min(validation_deltas) >= float(selected_policy["minimumValidationDelta"])
    leakage_pass = not leakage if selected_policy["requireNoTestLeakage"] else True
    passed = verification["ok"] and validation_pass and leakage_pass and not regressions
    core = {
        "schema": EXPERIMENT_SCHEMA,
        "mode": "offline-evaluation",
        "liveAnalyzerMutationEnabled": False,
        "dictionaryMutationEnabled": False,
        "deploymentEnabled": False,
        "corpusDigest": artifact.get("corpusDigest"),
        "splitPolicy": artifact.get("splitPolicy"),
        "policy": selected_policy,
        "before": before_by_split,
        "after": after_by_split,
        "deltas": deltas,
        "regressions": regressions,
        "leakageRecordIds": leakage,
        "passed": passed,
        "records": rows,
    }
    digest = _digest(core)
    return {**core, "experimentId": "toe-" + digest.split(":", 1)[1][:24], "artifactDigest": digest}


def verify_offline_experiment(experiment: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if experiment.get("schema") != EXPERIMENT_SCHEMA:
        problems.append("unsupported-schema")
    if experiment.get("mode") != "offline-evaluation":
        problems.append("mode-must-be-offline-evaluation")
    for key in ("liveAnalyzerMutationEnabled", "dictionaryMutationEnabled", "deploymentEnabled"):
        if experiment.get(key) is not False:
            problems.append(key + "-must-remain-disabled")
    if experiment.get("leakageRecordIds"):
        problems.append("split-leakage-detected")
    core = {key: value for key, value in experiment.items() if key not in {"experimentId", "artifactDigest"}}
    expected = _digest(core)
    if experiment.get("artifactDigest") != expected:
        problems.append("artifact-digest-mismatch")
    if experiment.get("experimentId") != "toe-" + expected.split(":", 1)[1][:24]:
        problems.append("experiment-id-mismatch")
    return {"ok": not problems, "problems": problems, "schema": EXPERIMENT_SCHEMA}
