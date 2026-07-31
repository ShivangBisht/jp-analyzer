from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .teaching_quality_store import corpus_quality_summary, get_quality, set_quality
router=APIRouter(prefix="/teaching-quality",tags=["teaching-quality"])
class QualityRequest(BaseModel):
    qualityStatus:str
    reviewer:str|None=None
    qualityNote:str|None=None
@router.get("/summary")
def summary(): return corpus_quality_summary()
@router.get("/{record_id}")
def get(record_id:str):
    try:return get_quality(record_id)
    except ValueError as exc:raise HTTPException(404,str(exc)) from exc
@router.put("/{record_id}")
def update(record_id:str,req:QualityRequest):
    try:return set_quality(record_id,req.qualityStatus,reviewer=req.reviewer,quality_note=req.qualityNote)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
