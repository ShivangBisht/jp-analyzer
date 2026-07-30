from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TEACHING_DECISION_RECORD_SCHEMA_VERSION = "1.0"
JudgmentType = Literal["accepted-current", "corrected", "rejected"]
CoverageState = Literal["reviewed-accepted", "reviewed-corrected", "reviewed-rejected", "unreviewed"]
FailureClass = Literal[
    "accepted-current", "candidate-generation-miss", "ranking-error", "hard-gate-error",
    "boundary-error", "role-error", "identity-error", "partition-optimization-error",
    "abstention-error", "unclassified",
]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RangeAssertion(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    surface: str = Field(min_length=1)

    def check(self, sentence: str) -> None:
        if self.start >= self.end or self.end > len(sentence):
            raise ValueError("assertion range is outside sentence")
        if sentence[self.start:self.end] != self.surface:
            raise ValueError("assertion surface does not match sentence")


class CoverageRegion(BaseModel):
    range: RangeAssertion
    state: CoverageState


class Assertions(BaseModel):
    boundary: RangeAssertion
    classification: dict[str, Any]
    identity: dict[str, Any] | None = None


class SnapshotReference(BaseModel):
    snapshotId: str = Field(pattern=r"^ads-")
    contentDigest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    schemaVersion: str = "1.0"


class QualityState(BaseModel):
    corpusMode: Literal["test"] = "test"
    reviewStatus: Literal["captured", "reviewed"] = "captured"
    exportStatus: Literal["excluded"] = "excluded"
    operationalStatus: Literal["inactive"] = "inactive"


class Lifecycle(BaseModel):
    status: Literal["active", "superseded", "retracted"] = "active"
    supersedesRecordId: str | None = None


class TeachingDecisionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recordId: str
    schemaVersion: str = TEACHING_DECISION_RECORD_SCHEMA_VERSION
    createdAt: str = Field(default_factory=_now)
    sourceSentence: str = Field(min_length=1)
    snapshotReference: SnapshotReference
    judgment: JudgmentType
    reviewCoverage: list[CoverageRegion]
    assertions: Assertions
    approvedTarget: dict[str, Any] | None = None
    decisionComparison: dict[str, Any]
    failureClassification: FailureClass
    confidence: Literal["preference", "confident", "needs-review"] = "preference"
    note: str | None = None
    qualityState: QualityState = Field(default_factory=QualityState)
    operationalCorrectionLink: dict[str, Any] | None = None
    lifecycle: Lifecycle = Field(default_factory=Lifecycle)
    history: list[dict[str, Any]] = Field(default_factory=list)
    contentDigest: str

    @model_validator(mode="after")
    def validate_record(self):
        self.assertions.boundary.check(self.sourceSentence)
        if not self.reviewCoverage:
            raise ValueError("review coverage is required")
        cursor = 0
        reviewed = []
        for region in self.reviewCoverage:
            region.range.check(self.sourceSentence)
            if region.range.start != cursor:
                raise ValueError("review coverage must be contiguous and ordered")
            cursor = region.range.end
            if region.state != "unreviewed":
                reviewed.append(region)
        if cursor != len(self.sourceSentence):
            raise ValueError("review coverage must cover the complete sentence")
        target = self.assertions.boundary
        expected_state = {
            "accepted-current": "reviewed-accepted",
            "corrected": "reviewed-corrected",
            "rejected": "reviewed-rejected",
        }[self.judgment]
        if not any(r.range.start == target.start and r.range.end == target.end and r.state == expected_state for r in reviewed):
            raise ValueError("asserted range must have coverage matching judgment")
        if self.judgment == "corrected" and self.approvedTarget is None:
            raise ValueError("corrected judgment requires approvedTarget")
        if self.judgment == "accepted-current" and self.failureClassification != "accepted-current":
            raise ValueError("accepted-current judgment requires accepted-current classification")
        if self.judgment != "accepted-current" and self.failureClassification == "accepted-current":
            raise ValueError("non-accepted judgment cannot use accepted-current classification")
        return self


def build_review_coverage(sentence: str, selected: RangeAssertion, judgment: JudgmentType) -> list[CoverageRegion]:
    selected.check(sentence)
    state = {
        "accepted-current": "reviewed-accepted",
        "corrected": "reviewed-corrected",
        "rejected": "reviewed-rejected",
    }[judgment]
    regions: list[CoverageRegion] = []
    if selected.start:
        regions.append(CoverageRegion(range=RangeAssertion(start=0, end=selected.start, surface=sentence[:selected.start]), state="unreviewed"))
    regions.append(CoverageRegion(range=selected, state=state))
    if selected.end < len(sentence):
        regions.append(CoverageRegion(range=RangeAssertion(start=selected.end, end=len(sentence), surface=sentence[selected.end:]), state="unreviewed"))
    return regions


def _comparison(snapshot: dict[str, Any], boundary: RangeAssertion, assertions: Assertions, approved_target: dict[str, Any] | None) -> dict[str, Any]:
    spans = (snapshot.get("readerDecision") or {}).get("selectedSpans") or []
    observed = next((deepcopy(x) for x in spans if x.get("start") == boundary.start and x.get("end") == boundary.end), None)
    return {
        "observedReaderSpan": observed,
        "assertedBoundary": boundary.model_dump(mode="json"),
        "assertedClassification": deepcopy(assertions.classification),
        "assertedIdentity": deepcopy(assertions.identity),
        "approvedTarget": deepcopy(approved_target),
        "boundaryMatches": observed is not None,
        "classificationMatches": bool(observed and observed.get("displayRole") == assertions.classification.get("assertedRole")),
        "identityCompared": assertions.identity is not None,
    }


def build_teaching_decision_record(
    snapshot: dict[str, Any], *, boundary: RangeAssertion | dict[str, Any], judgment: JudgmentType,
    classification: dict[str, Any], identity: dict[str, Any] | None = None,
    approved_target: dict[str, Any] | None = None, failure_classification: FailureClass = "unclassified",
    confidence: str = "preference", note: str | None = None,
    operational_correction_link: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sentence = str((snapshot.get("source") or {}).get("sentence") or "")
    selected = boundary if isinstance(boundary, RangeAssertion) else RangeAssertion.model_validate(boundary)
    assertions = Assertions(boundary=selected, classification=deepcopy(classification), identity=deepcopy(identity))
    content = {
        "schemaVersion": TEACHING_DECISION_RECORD_SCHEMA_VERSION,
        "sourceSentence": sentence,
        "snapshotReference": {
            "snapshotId": snapshot.get("snapshotId"),
            "contentDigest": snapshot.get("contentDigest"),
            "schemaVersion": snapshot.get("schemaVersion") or "1.0",
        },
        "judgment": judgment,
        "reviewCoverage": [x.model_dump(mode="json") for x in build_review_coverage(sentence, selected, judgment)],
        "assertions": assertions.model_dump(mode="json"),
        "approvedTarget": deepcopy(approved_target),
        "decisionComparison": _comparison(snapshot, selected, assertions, approved_target),
        "failureClassification": failure_classification,
        "confidence": confidence,
        "note": note,
        "qualityState": QualityState().model_dump(mode="json"),
        "operationalCorrectionLink": deepcopy(operational_correction_link),
        "lifecycle": Lifecycle().model_dump(mode="json"),
        "history": [{"event": "captured", "at": _now()}],
    }
    digest = _digest(content)
    record = {"recordId": "tdr-" + digest.split(":", 1)[1][:24], "createdAt": _now(), **content, "contentDigest": digest}
    TeachingDecisionRecord.model_validate(record)
    return record


def validate_teaching_decision_record(record: dict[str, Any]) -> None:
    parsed = TeachingDecisionRecord.model_validate(record)
    content = parsed.model_dump(mode="json", exclude={"recordId", "createdAt", "contentDigest"})
    expected = _digest(content)
    if parsed.contentDigest != expected:
        raise ValueError("TeachingDecisionRecord content digest mismatch")
    if parsed.recordId != "tdr-" + expected.split(":", 1)[1][:24]:
        raise ValueError("TeachingDecisionRecord ID mismatch")
