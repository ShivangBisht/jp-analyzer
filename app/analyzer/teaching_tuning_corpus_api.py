import json
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from .teaching_tuning_corpus import build_tuning_corpus_package, verify_tuning_corpus_package

router = APIRouter(prefix="/teaching-tuning-corpus", tags=["teaching-tuning-corpus"])

class PackageJsonRequest(BaseModel):
    packageJson: str

def _parse(text: str):
    try: value=json.loads(text)
    except json.JSONDecodeError as exc: raise HTTPException(422, {"code":"INVALID_CORPUS_JSON","message":str(exc)}) from exc
    if not isinstance(value, dict): raise HTTPException(422, {"code":"INVALID_CORPUS_JSON","message":"package must be an object"})
    return value

@router.get("/preview")
def preview(profile: str = Query("private-local")):
    package=build_tuning_corpus_package(profile)
    return {"package":package,"verification":verify_tuning_corpus_package(package),"notice":"Packaging only. No tuning or activation occurred."}

@router.get("/export")
def export(profile: str = Query("private-local")):
    package=build_tuning_corpus_package(profile)
    verification=verify_tuning_corpus_package(package)
    if not verification["ok"]: raise HTTPException(409, verification)
    return package

@router.post("/verify")
def verify(req: PackageJsonRequest):
    result=verify_tuning_corpus_package(_parse(req.packageJson))
    if not result["ok"]: raise HTTPException(422, result)
    return result
