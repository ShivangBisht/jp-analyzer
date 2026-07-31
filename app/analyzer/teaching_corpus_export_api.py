from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .teaching_corpus_export import build_export_preview, verify_export_artifact

router = APIRouter(prefix="/teaching-corpus-export", tags=["teaching-corpus-export"])

class VerifyRequest(BaseModel):
    artifact: dict[str, Any]

@router.get("/preview")
def preview():
    return build_export_preview()

@router.post("/generate")
def generate():
    artifact = build_export_preview()
    verification = verify_export_artifact(artifact)
    if not verification["ok"]:
        raise HTTPException(409, {"code": "CORPUS_EXPORT_INVALID", "problems": verification["problems"]})
    return {"artifact": artifact, "verification": verification, "notice": "Dry-run only. No training or analyzer activation occurred."}

@router.post("/verify")
def verify(req: VerifyRequest):
    result = verify_export_artifact(req.artifact)
    if not result["ok"]:
        raise HTTPException(422, result)
    return result
