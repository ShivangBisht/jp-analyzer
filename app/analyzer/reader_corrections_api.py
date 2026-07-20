from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from .reader_corrections import preview, save, list_corrections, deactivate
from .version import ANALYZER_VERSION
from .reader_projection import READER_SPAN_SCHEMA_VERSION

router=APIRouter(prefix="/reader-corrections", tags=["reader-corrections"])
class CorrectionRequest(BaseModel):
    sentence:str; start:int; end:int; surface:str; displayRole:str
    headword:str|None=None; knownLookupKey:str|None=None; frequencyLookupKey:str|None=None
    grammarId:str|None=None; unknownColorPolicy:str|None=None; lexicalType:str|None=None
    scope:str="occurrence"; action:str="replace-reader-range"
    baselineReaderSpans:list[dict[str,Any]]=Field(default_factory=list)
    featureSnapshot:dict[str,Any]=Field(default_factory=dict)

def _data(req):
    d=req.model_dump(); baseline=d.pop("baselineReaderSpans"); return d,baseline
@router.post("/preview")
def preview_endpoint(req:CorrectionRequest):
    try: d,b=_data(req); return preview(d,b)
    except ValueError as e: raise HTTPException(422,str(e))
@router.post("")
def save_endpoint(req:CorrectionRequest):
    try: d,b=_data(req); return save(d,b,ANALYZER_VERSION,READER_SPAN_SCHEMA_VERSION)
    except ValueError as e: raise HTTPException(422,str(e))
@router.get("")
def list_endpoint(includeInactive:bool=Query(False)): return {"corrections":list_corrections(includeInactive)}
@router.delete("/{correction_id}")
def deactivate_endpoint(correction_id:str):
    try: return deactivate(correction_id)
    except ValueError as e: raise HTTPException(404,str(e))
