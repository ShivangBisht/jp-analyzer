from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .teaching_tuning_handoff import (
    build_handoff_preview,
    verify_tuning_input_contract,
    verify_candidate_artifact,
    verify_candidate_evaluation,
    verify_handoff_manifest,
)

router=APIRouter(prefix="/teaching-tuning-handoff",tags=["teaching-tuning-handoff"])

class VerifyRequest(BaseModel):
    artifactType: str
    artifact: dict[str,Any]

@router.get("/preview")
def preview():
    return build_handoff_preview()

@router.post("/verify")
def verify(req:VerifyRequest):
    verifiers={
        "tuning-input": verify_tuning_input_contract,
        "candidate-artifact": verify_candidate_artifact,
        "candidate-evaluation": verify_candidate_evaluation,
        "handoff-manifest": verify_handoff_manifest,
    }
    fn=verifiers.get(req.artifactType)
    if fn is None: raise HTTPException(422,"unsupported artifact type")
    result=fn(req.artifact)
    if not result["ok"]: raise HTTPException(422,result)
    return result
