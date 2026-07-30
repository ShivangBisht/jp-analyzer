from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from .teaching_decision_record import build_teaching_decision_record
from .teaching_decision_store import persist_record, get_record, list_records, retract_record, supersede_record, integrity_report

router=APIRouter(prefix="/teaching-decisions", tags=["teaching-decisions"])
class CreateRequest(BaseModel):
    snapshot: dict[str,Any]
    boundary: dict[str,Any]
    judgment: str
    classification: dict[str,Any]
    identity: dict[str,Any]|None=None
    approvedTarget: dict[str,Any]|None=None
    failureClassification: str="unclassified"
    confidence: str="preference"
    note: str|None=None
    operationalCorrectionLink: dict[str,Any]|None=None
class SupersedeRequest(CreateRequest): pass
class RetractRequest(BaseModel): note: str|None=None

def _build(req):
    return build_teaching_decision_record(req.snapshot,boundary=req.boundary,judgment=req.judgment,classification=req.classification,identity=req.identity,approved_target=req.approvedTarget,failure_classification=req.failureClassification,confidence=req.confidence,note=req.note,operational_correction_link=req.operationalCorrectionLink)
@router.post("")
def create(req:CreateRequest):
    try: return persist_record(_build(req),snapshot=req.snapshot)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
@router.get("/integrity")
def integrity(): return integrity_report()
@router.get("")
def listing(judgment:str|None=None,failureClassification:str|None=None,lifecycleStatus:str|None=Query("active"),sentenceSha256:str|None=None):
    return {"records":list_records(judgment=judgment,failure_classification=failureClassification,lifecycle_status=lifecycleStatus,sentence_sha256=sentenceSha256),"exportEnabled":False}
@router.get("/{record_id}")
def get(record_id:str):
    try:return get_record(record_id)
    except ValueError as exc:raise HTTPException(404,str(exc)) from exc
@router.post("/{record_id}/supersede")
def supersede(record_id:str,req:SupersedeRequest):
    try:return supersede_record(record_id,_build(req),snapshot=req.snapshot,note=req.note)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
@router.post("/{record_id}/retract")
def retract(record_id:str,req:RetractRequest):
    try:return retract_record(record_id,note=req.note)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
