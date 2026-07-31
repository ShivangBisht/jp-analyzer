from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .teaching_offline_evaluation import build_offline_experiment, verify_offline_experiment
from .teaching_controlled_activation import build_activation_plan, verify_activation_plan, simulate_shadow_observation

router=APIRouter(prefix="/teaching-controlled-activation",tags=["teaching-controlled-activation"])
class PlanRequest(BaseModel): experiment: dict[str,Any] | None = None
class VerifyRequest(BaseModel): plan: dict[str,Any]
class ObserveRequest(BaseModel): plan: dict[str,Any]; baseline: dict[str,Any]; candidate: dict[str,Any]

@router.get("/preview")
def preview():
    experiment=build_offline_experiment()
    if not experiment.get("passed"):
        return {"eligible":False,"reason":"offline-experiment-not-passing","experiment":experiment,"mode":"shadow","activationEnabled":False}
    return {"eligible":True,"plan":build_activation_plan(experiment),"mode":"shadow","activationEnabled":False}

@router.post("/plan")
def plan(req:PlanRequest):
    experiment=req.experiment or build_offline_experiment()
    verification=verify_offline_experiment(experiment)
    if not verification["ok"]: raise HTTPException(422,verification)
    try: value=build_activation_plan(experiment)
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    return {"plan":value,"verification":verify_activation_plan(value),"notice":"Shadow plan only. Live analyzer activation remains disabled."}

@router.post("/verify")
def verify(req:VerifyRequest):
    result=verify_activation_plan(req.plan)
    if not result["ok"]: raise HTTPException(422,result)
    return result

@router.post("/observe")
def observe(req:ObserveRequest):
    try: return simulate_shadow_observation(req.plan,baseline=req.baseline,candidate=req.candidate)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
