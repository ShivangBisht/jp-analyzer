from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Callable

from .compact_output import compact_analysis
from .layers.dictionary_store import status as dictionary_status
from .reader_candidate_selection import POLICY_VERSION as READER_SELECTION_POLICY_VERSION
from .reader_candidates import READER_CANDIDATE_SCHEMA_VERSION
from .reader_corrections import correction_revision
from .reader_projection import READER_SPAN_SCHEMA_VERSION
from .version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION, SCHEMA_VERSION

ANALYZER_DECISION_SNAPSHOT_SCHEMA_VERSION = "1.0"
CORE_FEATURE_SCHEMA_VERSION = "1.0"
CORE_SCORE_POLICY_VERSION = "1.0"
CORE_RESOLVER_POLICY_VERSION = "1.0"
READER_PRIORITY_POLICY_VERSION = "1.0"
READER_POLICY_PROJECTION_VERSION = "1.0"

DictionaryStatus = Callable[[], dict[str, Any]]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _candidate_fingerprint(text_sha256: str, candidate: dict[str, Any], *, system: str) -> str:
    payload = {
        "textSha256": text_sha256,
        "system": system,
        "start": candidate.get("start"),
        "end": candidate.get("end"),
        "surface": candidate.get("surface"),
        "family": candidate.get("candidate_family", candidate.get("candidateFamily")),
        "role": candidate.get("proposed_role", candidate.get("proposedRole")),
        "headword": candidate.get("headword", candidate.get("preferredLookupKey")),
        "grammarId": candidate.get("grammar_id", candidate.get("grammarId")),
        "sourceLayer": candidate.get("source_layer") or (candidate.get("features") or {}).get("sourceLayer"),
    }
    return "sha256:" + _digest(payload)


def _dictionary_support_explanation(candidate: dict[str, Any]) -> dict[str, Any]:
    family = candidate.get("candidate_family")
    evidence = candidate.get("dictionary_evidence") or {}
    counts = evidence.get("dictionary_type_counts") or {}
    matched = bool(evidence.get("matched"))
    base = term = expression = name = grammar = other = 0
    cap = 0
    if matched and family == "term":
        base, term, expression, cap = 25, 5 * int(counts.get("term", 0)), 3 * int(counts.get("expression", 0)), 80
    elif matched and family == "proper-name":
        base, name, cap = 15, 5 * int(counts.get("name", 0)), 55
    elif matched and family == "grammar":
        base, grammar, cap = 10, 5 * int(counts.get("grammar", 0)), 45
    elif matched:
        other, cap = 10, 10
    uncapped = base + term + expression + name + grammar + other
    result = min(cap, uncapped) if cap else 0
    return {
        "matched": matched,
        "base": base,
        "termContribution": term,
        "expressionContribution": expression,
        "nameContribution": name,
        "grammarContribution": grammar,
        "otherContribution": other,
        "uncapped": uncapped,
        "cap": cap,
        "result": result,
    }


def _core_candidates(full: dict[str, Any], text_sha256: str) -> list[dict[str, Any]]:
    out = []
    for source in full.get("resolver_candidates_alpha2") or []:
        item = deepcopy(source)
        item["candidateFingerprint"] = _candidate_fingerprint(text_sha256, source, system="core-resolver")
        dimensions = list(source.get("utility_dimensions") or [])
        item["scoreExplanation"] = {
            "policyVersion": CORE_SCORE_POLICY_VERSION,
            "featureSchemaVersion": CORE_FEATURE_SCHEMA_VERSION,
            "dimensions": {
                "integrity": dimensions[0] if len(dimensions) > 0 else None,
                "protectedOrContextFamily": dimensions[1] if len(dimensions) > 1 else None,
                "specificity": dimensions[2] if len(dimensions) > 2 else None,
                "completeness": dimensions[3] if len(dimensions) > 3 else None,
                "dictionarySupport": dimensions[4] if len(dimensions) > 4 else None,
                "confidence": dimensions[5] if len(dimensions) > 5 else None,
            },
            "dictionarySupportExplanation": _dictionary_support_explanation(source),
            "utilityScore": source.get("utility_score"),
        }
        out.append(item)
    return out


def _core_partition(full: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {str(x.get("candidate_id")): x for x in candidates if x.get("candidate_id")}
    selected_ids = [
        str(x.get("selected_candidate_id"))
        for x in (full.get("resolved_spans_alpha2") or [])
        if x.get("selected_candidate_id")
    ]
    missing = [cid for cid in selected_ids if cid not in by_id and not cid.startswith("a34fallback")]
    scores = [int((by_id.get(cid) or {}).get("utility_score") or 0) for cid in selected_ids]
    return {
        "policyVersion": CORE_RESOLVER_POLICY_VERSION,
        "selectedCandidateIds": selected_ids,
        "selectedCandidateFingerprints": [
            by_id[cid]["candidateFingerprint"] for cid in selected_ids if cid in by_id
        ],
        "totalUtilityScore": sum(scores),
        "selectedCandidateScores": scores,
        "missingSelectedCandidateIds": missing,
        "tieBreakTrace": {
            "available": False,
            "reason": "Historical resolver does not emit per-comparison tie events.",
            "policy": ["higher-total-score", "fewer-fragments", "longer-earlier-spans"],
        },
        "runnerUpPartition": None,
    }


def _reader_priority(candidate: dict[str, Any]) -> dict[str, int]:
    family_order = {"complete-grammar": 40, "compound-predicate": 30, "inflected-lexical": 20, "term": 10}
    length = int(candidate.get("end") or 0) - int(candidate.get("start") or 0)
    sources = 0
    for hypothesis in candidate.get("lookupHypotheses") or []:
        if hypothesis.get("dictionaryStatus") == "matched":
            sources = max(sources, int((hypothesis.get("dictionaryEvidence") or {}).get("independentSourceCount") or 0))
    return {"family": family_order.get(candidate.get("candidateFamily"), 0), "length": length, "dictionarySources": sources}


def _reader_candidates(compact: dict[str, Any], text_sha256: str) -> list[dict[str, Any]]:
    out = []
    for source in compact.get("readerCandidates") or []:
        item = deepcopy(source)
        item["candidateFingerprint"] = _candidate_fingerprint(text_sha256, source, system=str(source.get("candidateSource") or "reader"))
        if source.get("candidateSource") == "reader-evidence-generator":
            item["priorityExplanation"] = {
                "policyVersion": READER_PRIORITY_POLICY_VERSION,
                **_reader_priority(source),
            }
        out.append(item)
    return out


def _dictionary_identity(status: dict[str, Any]) -> dict[str, Any]:
    selected = {
        "ready": bool(status.get("ready")),
        "snapshotIdentity": status.get("snapshotIdentity"),
        "lastSyncId": status.get("lastSyncId"),
        "entryCount": int(status.get("entryCount") or 0),
        "dictionaryCount": int(status.get("dictionaryCount") or 0),
        "typeCounts": dict(status.get("typeCounts") or {}),
        "registryEntryCount": status.get("registryEntryCount"),
        "registryConsistent": status.get("registryConsistent"),
    }
    selected["identityDigest"] = "sha256:" + _digest(selected)
    return selected


def build_analyzer_decision_snapshot(
    full_analysis: dict[str, Any],
    *,
    captured_at: str | None = None,
    dictionary_status_fn: DictionaryStatus = dictionary_status,
    analyzer_version: str = ANALYZER_VERSION,
) -> dict[str, Any]:
    """Build an immutable, correction-free observation of the current analyzer.

    This function adds observability only. It does not generate candidates, change
    scores, alter selection, or apply operational corrections.
    """
    full = deepcopy(full_analysis)
    text = str(full.get("text") or "")
    text_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    observed_correction_revision = correction_revision()
    compact = compact_analysis(full, analyzer_version=analyzer_version, apply_corrections=False)
    core_candidates = _core_candidates(full, text_sha256)
    reader_candidates = _reader_candidates(compact, text_sha256)
    dictionary = _dictionary_identity(dictionary_status_fn())

    content = {
        "schemaVersion": ANALYZER_DECISION_SNAPSHOT_SCHEMA_VERSION,
        "source": {"sentence": text, "sentenceSha256": text_sha256, "textLength": len(text)},
        "analyzerIdentity": {
            "analyzerVersion": analyzer_version,
            "engineVersion": full.get("version") or ENGINE_CONTRACT_VERSION,
            "compactSchemaVersion": SCHEMA_VERSION,
            "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
            "readerCandidateSchemaVersion": READER_CANDIDATE_SCHEMA_VERSION,
            "coreFeatureSchemaVersion": CORE_FEATURE_SCHEMA_VERSION,
            "coreScorePolicyVersion": CORE_SCORE_POLICY_VERSION,
            "coreResolverPolicyVersion": CORE_RESOLVER_POLICY_VERSION,
            "readerSelectionPolicyVersion": READER_SELECTION_POLICY_VERSION,
            "readerPriorityPolicyVersion": READER_PRIORITY_POLICY_VERSION,
            "readerPolicyProjectionVersion": READER_POLICY_PROJECTION_VERSION,
            "observedCorrectionRevision": observed_correction_revision,
        },
        "dictionaryIdentity": dictionary,
        "fullAnalysis": full,
        "coreDecision": {
            "candidates": core_candidates,
            "decisions": deepcopy(full.get("resolver_decisions_alpha2") or []),
            "conflicts": deepcopy(full.get("resolver_conflicts_alpha2") or []),
            "resolvedSpans": deepcopy(full.get("resolved_spans_alpha2") or []),
            "selectedPartition": _core_partition(full, core_candidates),
        },
        "readerDecision": {
            "compatibilitySpans": deepcopy(compact.get("compatibilityReaderSpans") or []),
            "candidates": reader_candidates,
            "selection": deepcopy(compact.get("readerSelection") or {}),
            "selectedSpans": deepcopy(compact.get("readerSpans") or []),
        },
        "generationObservability": {
            "eventLedgerAvailable": False,
            "finalCandidateInventoryAvailable": True,
            "reason": "Alpha 2 captures existing output; filtered proposal events require later instrumentation.",
        },
        "correctionContext": {
            "operationalCorrectionApplication": "disabled-for-snapshot",
            "observedCorrectionRevision": observed_correction_revision,
            "appliedCorrections": [],
        },
        "replayability": {
            "level0Archival": True,
            "level1CoreScore": True,
            "level2CorePartition": True,
            "level3ReaderSelection": True,
            "level4FullAnalyzerRerun": False,
            "limitations": [
                "core tie events and runner-up partition are not emitted by the historical resolver",
                "filtered candidate-generation events are not emitted",
                "full rerun requires compatible models and dictionary content",
            ],
        },
    }
    content_digest = "sha256:" + _digest(content)
    return {
        "snapshotId": "ads-" + content_digest.split(":", 1)[1][:24],
        "capturedAt": captured_at or datetime.now(timezone.utc).isoformat(),
        "contentDigest": content_digest,
        **content,
    }


def validate_analyzer_decision_snapshot(snapshot: dict[str, Any]) -> None:
    if snapshot.get("schemaVersion") != ANALYZER_DECISION_SNAPSHOT_SCHEMA_VERSION:
        raise ValueError("unsupported AnalyzerDecisionSnapshot schema")
    source = snapshot.get("source") or {}
    sentence = source.get("sentence")
    if not isinstance(sentence, str):
        raise ValueError("snapshot source sentence is missing")
    expected = hashlib.sha256(sentence.encode("utf-8")).hexdigest()
    if source.get("sentenceSha256") != expected:
        raise ValueError("snapshot sentence digest mismatch")
    reader = snapshot.get("readerDecision") or {}
    spans = reader.get("selectedSpans") or []
    if "".join(str(x.get("surface") or "") for x in spans) != sentence:
        raise ValueError("snapshot Reader spans do not reconstruct sentence")
    payload = {k: v for k, v in snapshot.items() if k not in {"snapshotId", "capturedAt", "contentDigest"}}
    digest = "sha256:" + _digest(payload)
    if snapshot.get("contentDigest") != digest:
        raise ValueError("snapshot content digest mismatch")
    if snapshot.get("snapshotId") != "ads-" + digest.split(":", 1)[1][:24]:
        raise ValueError("snapshot ID mismatch")
