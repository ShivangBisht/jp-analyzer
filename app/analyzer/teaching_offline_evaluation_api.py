from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .teaching_corpus_export import build_export_preview
from .teaching_offline_evaluation import build_offline_experiment, verify_offline_experiment

router = APIRouter(prefix="/teaching-offline-evaluation", tags=["teaching-offline-evaluation"])

class RunRequest(BaseModel):
    candidatePredictions: dict[str, dict[str, Any]] = Field(default_factory=dict)
    policy: dict[str, Any] = Field(default_factory=dict)

class VerifyRequest(BaseModel):
    experiment: dict[str, Any]

@router.get("/preview")
def preview():
    return build_offline_experiment(corpus=build_export_preview())

@router.post("/run")
def run(req: RunRequest):
    experiment = build_offline_experiment(corpus=build_export_preview(), candidate_predictions=req.candidatePredictions, policy=req.policy)
    verification = verify_offline_experiment(experiment)
    if not verification["ok"]:
        raise HTTPException(409, {"code": "OFFLINE_EXPERIMENT_INVALID", "problems": verification["problems"]})
    return {"experiment": experiment, "verification": verification, "notice": "Offline evaluation only. The live analyzer, dictionary, and deployment state were not changed."}

@router.post("/verify")
def verify(req: VerifyRequest):
    result = verify_offline_experiment(req.experiment)
    if not result["ok"]:
        raise HTTPException(422, result)
    return result
