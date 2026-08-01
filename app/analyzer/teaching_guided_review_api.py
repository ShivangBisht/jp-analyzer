from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .teaching_decision_store import get_snapshot
from .teaching_guided_review import diagnose_guided_review

router = APIRouter(prefix="/teaching-guided-review", tags=["teaching-guided-review"])


class DiagnosisRequest(BaseModel):
    snapshotId: str
    snapshotDigest: str
    boundary: dict[str, Any]
    assertedRole: str | None = None
    intent: str


@router.post("/diagnose")
def diagnose(req: DiagnosisRequest):
    try:
        snapshot = get_snapshot(req.snapshotId)
        if snapshot.get("contentDigest") != req.snapshotDigest:
            raise ValueError("snapshot digest does not match authoritative snapshot")
        return diagnose_guided_review(
            snapshot,
            boundary=req.boundary,
            asserted_role=req.assertedRole,
            intent=req.intent,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
