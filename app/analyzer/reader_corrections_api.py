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
)
from .reader_projection import READER_SPAN_SCHEMA_VERSION
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


class TeachingResultResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    sentenceFingerprint: str
    originalReaderSpans: list[dict[str, Any]]
    previewReaderSpans: list[dict[str, Any]]
    derivedCorrection: dict[str, Any]
    saved: bool
    correctionId: str | None = None
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


def _data(req: CorrectionRequest):
    payload = req.model_dump()
    baseline = payload.pop("baselineReaderSpans")
    candidates = payload.pop("readerCandidates")
    selection = payload.pop("readerSelection")
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
    try:
        before = correction_revision()
        data, baseline, candidates, selection = _data(req)
        result = save(
            data, baseline, ANALYZER_VERSION, READER_SPAN_SCHEMA_VERSION,
            reader_candidates=candidates, reader_selection=selection,
        )
        result["correctionRevisionBefore"] = before
        result["correctionRevisionAfter"] = correction_revision()
        return result
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


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


@router.delete("/{correction_id}", response_model=DeactivateResponse)
def deactivate_endpoint(correction_id: str):
    try:
        before = correction_revision()
        result = deactivate(correction_id)
        result["correctionRevisionBefore"] = before
        result["correctionRevisionAfter"] = correction_revision()
        return result
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
