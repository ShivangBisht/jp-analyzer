from __future__ import annotations

from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from .dictionary_evidence import evaluate_analysis_candidates, evaluate_candidate

router = APIRouter(prefix="/dictionary-evidence", tags=["dictionary-evidence"])


class CandidateRequest(BaseModel):
    candidate: dict[str, Any]
    parserPos: str | None = None


class AnalysisRequest(BaseModel):
    analysis: dict[str, Any]


@router.post("/candidate")
def candidate(req: CandidateRequest):
    return evaluate_candidate(req.candidate, req.parserPos)


@router.post("/analysis")
def analysis(req: AnalysisRequest):
    return evaluate_analysis_candidates(req.analysis)
