from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ANNOTATION_SCHEMA_VERSION = "1.0"
SNAPSHOT_SCHEMA_VERSION = "1.0"

AnnotationConfidence = Literal["preference", "confident", "needs-review"]
AnnotationStatus = Literal["active", "retracted", "superseded"]
CoverageState = Literal["reviewed-corrected", "reviewed-accepted", "unreviewed", "retracted"]
DatasetPartition = Literal["train", "development", "test"]
TeachingAction = Literal[
    "show-as-one-unit", "split", "mark-vocabulary", "mark-grammar",
    "mark-function", "mark-name", "mark-unresolved",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_digest(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


class SourceRange(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    surface: str = Field(min_length=1)

    def validate_against(self, sentence: str) -> None:
        if self.start >= self.end or self.end > len(sentence):
            raise ValueError("range is outside sentence")
        if sentence[self.start:self.end] != self.surface:
            raise ValueError("range surface does not match sentence")


class SourceProvenance(BaseModel):
    bookId: str | None = None
    bookTitle: str | None = None
    chapterIndex: int | None = Field(default=None, ge=0)
    chapterTitle: str | None = None
    sceneIndex: int | None = Field(default=None, ge=0)
    sentence: str = Field(min_length=1)
    sentenceFingerprint: str
    leftContext: str | None = None
    rightContext: str | None = None


class AnalyzerIdentity(BaseModel):
    analyzerVersion: str
    engineVersion: str | None = None
    compactSchemaVersion: str | None = None
    readerSpanSchemaVersion: str
    readerCandidateSchemaVersion: str | None = None
    correctionRevision: str
    dictionaryIdentity: dict[str, Any] | None = None


class AnalyzerSnapshot(BaseModel):
    snapshotId: str
    snapshotSchemaVersion: str = SNAPSHOT_SCHEMA_VERSION
    capturedAt: str = Field(default_factory=utc_now)
    identity: AnalyzerIdentity
    sentence: str
    snapshotKind: Literal["raw-baseline", "effective-baseline", "post-correction"]
    rawBaselineSnapshotId: str | None = None
    fullAnalysis: dict[str, Any] | None = None
    fullAnalysisDigest: str | None = None
    readerSpans: list[dict[str, Any]]
    readerCandidates: list[dict[str, Any]]
    readerSelection: dict[str, Any]
    appliedCorrections: list[dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_reader_partition(self):
        cursor = 0
        for span in self.readerSpans:
            start, end = span.get("start"), span.get("end")
            surface = span.get("surface")
            if not isinstance(start, int) or not isinstance(end, int) or start != cursor:
                raise ValueError("readerSpans must be an ordered contiguous partition")
            if self.sentence[start:end] != surface:
                raise ValueError("readerSpans surface mismatch")
            cursor = end
        if cursor != len(self.sentence):
            raise ValueError("readerSpans do not cover sentence")
        return self


class CoverageRegion(BaseModel):
    range: SourceRange
    state: CoverageState


class CoverageMask(BaseModel):
    wholeSentenceReviewed: bool = False
    regions: list[CoverageRegion]

    @model_validator(mode="after")
    def validate_partition(self):
        if not self.regions:
            raise ValueError("coverage regions are required")
        ordered = sorted(self.regions, key=lambda item: item.range.start)
        cursor = 0
        for region in ordered:
            if region.range.start != cursor:
                raise ValueError("coverage regions must be contiguous and non-overlapping")
            cursor = region.range.end
        return self


class TeachingTarget(BaseModel):
    selectedRange: SourceRange
    action: TeachingAction
    displayRole: str | None = None
    splitOffsets: list[int] = Field(default_factory=list)
    targetReaderSpans: list[dict[str, Any]]
    assertions: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_action(self):
        if self.action == "split":
            if not self.splitOffsets:
                raise ValueError("split requires at least one split offset")
            if any(value <= self.selectedRange.start or value >= self.selectedRange.end for value in self.splitOffsets):
                raise ValueError("split offset outside selected range")
        elif self.splitOffsets:
            raise ValueError("splitOffsets are only valid for split")
        expected_roles = {
            "mark-vocabulary": "lexical",
            "mark-grammar": "learnable-grammar",
            "mark-function": "function",
            "mark-name": "name",
            "mark-unresolved": "unresolved",
        }
        expected = expected_roles.get(self.action)
        if expected and self.displayRole != expected:
            raise ValueError(f"{self.action} requires displayRole {expected}")
        return self


class DerivedOutcome(BaseModel):
    postCorrectionSnapshotId: str | None = None
    effectiveReaderSpans: list[dict[str, Any]] = Field(default_factory=list)
    selectedSpan: dict[str, Any] | None = None
    knownLookupKey: str | None = None
    frequencyLookupKey: str | None = None
    countsForComprehension: bool | None = None
    showInNewWords: bool | None = None
    eligibleForMining: bool | None = None
    presentationClass: str | None = None
    colourSource: str | None = None
    derivationStatus: Literal["pending", "complete", "partial", "failed"] = "pending"
    derivationErrors: list[str] = Field(default_factory=list)


class AnnotationHistoryEvent(BaseModel):
    eventId: str
    event: Literal["saved", "retracted", "superseded", "reviewed", "note-updated"]
    at: str = Field(default_factory=utc_now)
    correctionRevisionBefore: str | None = None
    correctionRevisionAfter: str | None = None
    relatedAnnotationId: str | None = None
    note: str | None = None


class DatasetAssignment(BaseModel):
    groupId: str
    partition: DatasetPartition
    assignmentMethod: str = "stable-group-hash-v1"


class TeachingAnnotation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    annotationId: str
    annotationSchemaVersion: str = ANNOTATION_SCHEMA_VERSION
    status: AnnotationStatus = "active"
    createdAt: str = Field(default_factory=utc_now)
    correctionId: str
    source: SourceProvenance
    rawBaselineSnapshotId: str
    effectiveBaselineSnapshotId: str
    target: TeachingTarget
    coverage: CoverageMask
    confidence: AnnotationConfidence = "preference"
    note: str | None = None
    derivedOutcome: DerivedOutcome = Field(default_factory=DerivedOutcome)
    history: list[AnnotationHistoryEvent]
    dataset: DatasetAssignment

    @model_validator(mode="after")
    def validate_annotation(self):
        self.target.selectedRange.validate_against(self.source.sentence)
        for region in self.coverage.regions:
            region.range.validate_against(self.source.sentence)
        if self.coverage.regions[-1].range.end != len(self.source.sentence):
            raise ValueError("coverage mask must cover the complete sentence")
        reviewed = [
            region for region in self.coverage.regions
            if region.state == "reviewed-corrected"
            and region.range.start == self.target.selectedRange.start
            and region.range.end == self.target.selectedRange.end
        ]
        if not reviewed:
            raise ValueError("selected range must be reviewed-corrected")
        return self


def build_partial_coverage(sentence: str, selected: SourceRange) -> CoverageMask:
    selected.validate_against(sentence)
    regions: list[CoverageRegion] = []
    if selected.start:
        regions.append(CoverageRegion(
            range=SourceRange(start=0, end=selected.start, surface=sentence[:selected.start]),
            state="unreviewed",
        ))
    regions.append(CoverageRegion(range=selected, state="reviewed-corrected"))
    if selected.end < len(sentence):
        regions.append(CoverageRegion(
            range=SourceRange(start=selected.end, end=len(sentence), surface=sentence[selected.end:]),
            state="unreviewed",
        ))
    return CoverageMask(wholeSentenceReviewed=False, regions=regions)


def stable_dataset_assignment(sentence: str, selected: SourceRange, action: str) -> DatasetAssignment:
    group_id = stable_digest(f"{selected.surface}\0{action}")
    bucket = int(group_id[:8], 16) % 100
    partition: DatasetPartition = "train" if bucket < 70 else "development" if bucket < 85 else "test"
    return DatasetAssignment(groupId=group_id, partition=partition)
