from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from .reader_corrections import deactivate, list_corrections, preview, save
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
    scope: str = "occurrence"
    baselineReaderSpans: list[dict[str, Any]] = Field(default_factory=list)
    readerCandidates: list[dict[str, Any]] = Field(default_factory=list)
    readerSelection: dict[str, Any] = Field(default_factory=dict)


def _data(req: CorrectionRequest):
    payload = req.model_dump()
    baseline = payload.pop("baselineReaderSpans")
    candidates = payload.pop("readerCandidates")
    selection = payload.pop("readerSelection")
    if not baseline:
        # The future frontend may omit debug evidence; derive the current analyzer
        # output server-side while keeping all linguistic logic in JP Analyzer.
        from .pipeline import analyze
        current = analyze(req.sentence)
        baseline = current.get("readerSpans") or []
        candidates = current.get("readerCandidates") or []
        selection = current.get("readerSelection") or {}
    return payload, baseline, candidates, selection


@router.post("/preview")
def preview_endpoint(req: CorrectionRequest):
    try:
        data, baseline, candidates, selection = _data(req)
        return preview(
            data,
            baseline,
            reader_candidates=candidates,
            reader_selection=selection,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.post("")
def save_endpoint(req: CorrectionRequest):
    try:
        data, baseline, candidates, selection = _data(req)
        return save(
            data,
            baseline,
            ANALYZER_VERSION,
            READER_SPAN_SCHEMA_VERSION,
            reader_candidates=candidates,
            reader_selection=selection,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.get("")
def list_endpoint(includeInactive: bool = Query(False)):
    return {"corrections": list_corrections(includeInactive)}


@router.delete("/{correction_id}")
def deactivate_endpoint(correction_id: str):
    try:
        return deactivate(correction_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc))
