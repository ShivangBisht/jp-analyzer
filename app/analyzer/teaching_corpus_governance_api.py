from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .teaching_corpus_governance import build_corpus_governance_report, verify_corpus_governance_report

router = APIRouter(prefix="/teaching-corpus-governance", tags=["teaching-corpus-governance"])

class ReportRequest(BaseModel):
    policy: dict[str, Any] = Field(default_factory=dict)

class VerifyRequest(BaseModel):
    report: dict[str, Any]

@router.get("/report")
def report():
    value = build_corpus_governance_report()
    verification = verify_corpus_governance_report(value)
    if not verification["ok"]:
        raise HTTPException(409, verification)
    return {"report": value, "verification": verification, "notice": "Read-only governance. No tuning, activation, or deployment occurred."}

@router.post("/report")
def report_with_policy(req: ReportRequest):
    value = build_corpus_governance_report(policy=req.policy)
    verification = verify_corpus_governance_report(value)
    if not verification["ok"]:
        raise HTTPException(409, verification)
    return {"report": value, "verification": verification, "notice": "Read-only governance. No tuning, activation, or deployment occurred."}

@router.post("/verify")
def verify(req: VerifyRequest):
    result = verify_corpus_governance_report(req.report)
    if not result["ok"]:
        raise HTTPException(422, result)
    return result
