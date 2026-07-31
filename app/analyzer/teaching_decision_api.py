from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from .pipeline import analyze_decision_snapshot
from .teaching_decision_record import build_teaching_decision_record
from .teaching_decision_store import (
    get_record,
    get_snapshot,
    integrity_report,
    list_records,
    persist_record,
    retract_record,
    save_snapshot,
    supersede_record,
)
from .teaching_review_management import diagnose_record, review_summary

router = APIRouter(prefix="/teaching-decisions", tags=["teaching-decisions"])

class SnapshotRequest(BaseModel):
    sentence: str = Field(min_length=1)

class CreateRequest(BaseModel):
    snapshot: dict[str, Any]
    boundary: dict[str, Any]
    judgment: str
    classification: dict[str, Any]
    identity: dict[str, Any] | None = None
    approvedTarget: dict[str, Any] | None = None
    failureClassification: str = "unclassified"
    confidence: str = "preference"
    note: str | None = None
    operationalCorrectionLink: dict[str, Any] | None = None

class SupersedeRequest(CreateRequest):
    pass

class RetractRequest(BaseModel):
    note: str | None = None

def _authoritative_snapshot(
    submitted_snapshot: dict[str, Any],
) -> dict[str, Any]:
    snapshot_id = submitted_snapshot.get("snapshotId")
    submitted_digest = submitted_snapshot.get("contentDigest")

    if not snapshot_id:
        raise ValueError("snapshotId is required")

    stored_snapshot = get_snapshot(str(snapshot_id))

    if stored_snapshot.get("contentDigest") != submitted_digest:
        raise ValueError(
            "submitted snapshot reference does not match "
            "the authoritative stored snapshot"
        )

    return stored_snapshot

def _build(req: CreateRequest):
    snapshot = _authoritative_snapshot(req.snapshot)

    return build_teaching_decision_record(
        snapshot,
        boundary=req.boundary,
        judgment=req.judgment,
        classification=req.classification,
        identity=req.identity,
        approved_target=req.approvedTarget,
        failure_classification=req.failureClassification,
        confidence=req.confidence,
        note=req.note,
        operational_correction_link=req.operationalCorrectionLink,
    )

@router.post("/snapshot")
def snapshot(req: SnapshotRequest):
    try:
        captured = analyze_decision_snapshot(req.sentence)
        save_snapshot(captured)

        return captured
    except RuntimeError as exc:
        raise HTTPException(
            503,
            {
                "code": "ANALYZER_SNAPSHOT_UNAVAILABLE",
                "message": str(exc),
            },
        ) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.post("")
def create(req: CreateRequest):
    try:
        record = _build(req)
        return persist_record(record, snapshot=None,)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.get("/integrity")
def integrity():
    return integrity_report()

@router.get("")
def listing(
    judgment: str | None = None,
    failureClassification: str | None = None,
    lifecycleStatus: str | None = Query("active"),
    sentenceSha256: str | None = None,
):
    return {
        "records": list_records(
            judgment=judgment,
            failure_classification=failureClassification,
            lifecycle_status=lifecycleStatus,
            sentence_sha256=sentenceSha256,
        ),
        "exportEnabled": False,
    }


@router.get("/summary")
def summary():
    return review_summary()

@router.get("/{record_id}/diagnosis")
def diagnosis(record_id: str):
    try:
        return diagnose_record(get_record(record_id))
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc

@router.get("/{record_id}")
def get(record_id: str):
    try:
        return get_record(record_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc

@router.post("/{record_id}/supersede")
def supersede(record_id: str, req: SupersedeRequest):
    try:
        record = _build(req)
        return supersede_record(record_id, record, snapshot=None, note=req.note,)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.post("/{record_id}/retract")
def retract(record_id: str, req: RetractRequest):
    try:
        return retract_record(record_id, note=req.note)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
