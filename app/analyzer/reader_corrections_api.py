from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from .reader_corrections import (
    correction_revision,
    deactivate,
    find_corrections,
    list_corrections,
    preview,
    save,
    preflight_correction_range,
    reactivate,
)
from .reader_projection import READER_SPAN_SCHEMA_VERSION
from .teaching_annotation_store import (
    save_snapshot, create_annotation, retract_for_correction, list_annotations,
    corpus_status, preflight_annotation_range, update_derived_outcome, integrity_report,
)
from .version import ANALYZER_VERSION

router = APIRouter(prefix="/reader-corrections", tags=["reader-corrections"])


class CorrectionRequest(BaseModel):
    sentence: str
    start: int
    end: int
    surface: str
    action: str = "show-as-one-unit"
    displayRole: str | None = None
    splitOffsets: list[int] = Field(default_factory=list)
    scope: str = "occurrence"
    baselineReaderSpans: list[dict[str, Any]] = Field(default_factory=list)
    readerCandidates: list[dict[str, Any]] = Field(default_factory=list)
    readerSelection: dict[str, Any] = Field(default_factory=dict)
    confidence: str = "preference"
    note: str | None = None
    provenance: dict[str, Any] = Field(default_factory=dict)


class TeachingResultResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    sentenceFingerprint: str
    originalReaderSpans: list[dict[str, Any]]
    previewReaderSpans: list[dict[str, Any]]
    derivedCorrection: dict[str, Any]
    saved: bool
    correctionId: str | None = None
    annotationId: str | None = None
    rawBaselineSnapshotId: str | None = None
    effectiveBaselineSnapshotId: str | None = None
    postCorrectionSnapshotId: str | None = None
    derivedOutcome: dict[str, Any] | None = None
    correctionRevisionBefore: str
    correctionRevisionAfter: str


class CorrectionRecord(BaseModel):
    model_config = ConfigDict(extra="allow")
    correction_id: str
    sentence_text: str
    sentence_fingerprint: str
    start: int
    end: int
    surface: str
    action: str
    display_role: str
    scope: str
    created_at: str
    deactivated_at: str | None = None


class CorrectionListResponse(BaseModel):
    corrections: list[CorrectionRecord]
    correctionRevision: str


class DeactivateResponse(BaseModel):
    correctionId: str
    active: bool
    deactivatedAt: str
    correctionRevisionBefore: str
    correctionRevisionAfter: str
    annotationId: str | None = None


def _data(req: CorrectionRequest):
    payload = req.model_dump()
    baseline = payload.pop("baselineReaderSpans")
    candidates = payload.pop("readerCandidates")
    selection = payload.pop("readerSelection")
    payload.pop("confidence", None)
    payload.pop("note", None)
    payload.pop("provenance", None)
    if not baseline:
        from .pipeline import analyze
        current = analyze(req.sentence)
        baseline = current.get("readerSpans") or []
        candidates = current.get("readerCandidates") or []
        selection = current.get("readerSelection") or {}
    return payload, baseline, candidates, selection


@router.post("/preview", response_model=TeachingResultResponse)
def preview_endpoint(req: CorrectionRequest):
    try:
        before = correction_revision()
        data, baseline, candidates, selection = _data(req)
        result = preview(data, baseline, reader_candidates=candidates, reader_selection=selection)
        result["correctionRevisionBefore"] = before
        result["correctionRevisionAfter"] = before
        return result
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("", response_model=TeachingResultResponse)
def save_endpoint(req: CorrectionRequest):
    replaced_corrections: list[str] = []
    new_correction_id: str | None = None
    try:
        before = correction_revision()
        data, baseline, candidates, selection = _data(req)
        correction_preflight = preflight_correction_range(req.sentence, req.start, req.end)
        preflight_annotation_range(req.sentence, req.start, req.end)

        from .pipeline import analyze, analyze_full
        from .compact_output import compact_analysis

        # Full analysis is the immutable raw evidence graph. Compacting it applies
        # the active correction set and therefore records the effective baseline.
        raw_full = analyze_full(req.sentence)
        raw_compact = compact_analysis(raw_full, analyzer_version=ANALYZER_VERSION)
        raw_for_snapshot = dict(raw_compact)
        raw_for_snapshot["readerSpans"] = baseline
        raw_snapshot_id = save_snapshot(raw_full, raw_for_snapshot, kind="raw-baseline")
        effective_snapshot_id = save_snapshot(
            raw_full, raw_compact, kind="effective-baseline",
            raw_baseline_snapshot_id=raw_snapshot_id,
        )

        # Same-range Save is explicit replacement. Temporarily deactivate prior
        # corrections; compensate by reactivating them if any later step fails.
        for correction_id in correction_preflight["sameRangeCorrectionIds"]:
            deactivate(correction_id)
            replaced_corrections.append(correction_id)

        result = save(
            data, baseline, ANALYZER_VERSION, READER_SPAN_SCHEMA_VERSION,
            reader_candidates=candidates, reader_selection=selection,
        )
        new_correction_id = result["correctionId"]
        after = correction_revision()
        annotation = create_annotation(
            correction_id=new_correction_id, sentence=req.sentence, start=req.start, end=req.end,
            surface=req.surface, action=req.action, display_role=result["derivedCorrection"].get("displayRole"),
            split_offsets=req.splitOffsets, target_spans=result["previewReaderSpans"],
            raw_snapshot_id=raw_snapshot_id, effective_snapshot_id=effective_snapshot_id,
            confidence=req.confidence, note=req.note, provenance=req.provenance,
            revision_before=before, revision_after=after,
        )

        post_compact = analyze(req.sentence)
        post_full = analyze_full(req.sentence)
        post_snapshot_id = save_snapshot(
            post_full, post_compact, kind="post-correction",
            raw_baseline_snapshot_id=raw_snapshot_id,
        )
        annotation = update_derived_outcome(
            annotation["annotation_id"], post_snapshot_id, post_compact, req.start, req.end
        )
        result.update({
            "annotationId": annotation["annotation_id"],
            "rawBaselineSnapshotId": raw_snapshot_id,
            "effectiveBaselineSnapshotId": effective_snapshot_id,
            "postCorrectionSnapshotId": post_snapshot_id,
            "derivedOutcome": annotation["derived_outcome"],
            "correctionRevisionBefore": before,
            "correctionRevisionAfter": correction_revision(),
        })
        return result
    except ValueError as exc:
        if new_correction_id:
            try: deactivate(new_correction_id)
            except ValueError: pass
        for correction_id in replaced_corrections:
            try: reactivate(correction_id)
            except ValueError: pass
        raise HTTPException(422, str(exc)) from exc
    except Exception:
        if new_correction_id:
            try: deactivate(new_correction_id)
            except ValueError: pass
        for correction_id in replaced_corrections:
            try: reactivate(correction_id)
            except ValueError: pass
        raise

@router.get("", response_model=CorrectionListResponse)
def list_endpoint(includeInactive: bool = Query(False)):
    return {
        "corrections": list_corrections(includeInactive),
        "correctionRevision": correction_revision(),
    }


@router.get("/scope", response_model=CorrectionListResponse)
def scope_endpoint(
    sentence: str,
    start: int | None = Query(None, ge=0),
    end: int | None = Query(None, ge=1),
    includeInactive: bool = Query(False),
):
    if start is not None and end is not None and start >= end:
        raise HTTPException(422, "start must be less than end")
    return {
        "corrections": find_corrections(
            sentence, start=start, end=end, include_inactive=includeInactive
        ),
        "correctionRevision": correction_revision(),
    }


@router.get("/integrity")
def integrity_endpoint():
    return integrity_report(list_corrections(include_inactive=True))


@router.delete("/{correction_id}", response_model=DeactivateResponse)
def deactivate_endpoint(correction_id: str):
    try:
        before = correction_revision()
        result = deactivate(correction_id)
        after = correction_revision()
        annotation = retract_for_correction(correction_id, revision_before=before, revision_after=after)
        result["annotationId"] = annotation.get("annotation_id") if annotation else None
        result["correctionRevisionBefore"] = before
        result["correctionRevisionAfter"] = after
        return result
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.get("/annotations")
def annotations_endpoint(includeInactive: bool = Query(False), sentence: str | None = None):
    return {"annotations": list_annotations(includeInactive, sentence=sentence), "corpus": corpus_status()}
