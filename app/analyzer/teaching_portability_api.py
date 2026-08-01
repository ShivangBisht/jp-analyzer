from typing import Any
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .teaching_portability import (
    apply_teaching_evidence_import,
    export_teaching_evidence,
    preview_teaching_evidence_import,
    verify_teaching_evidence,
)

router = APIRouter(prefix="/teaching-portability", tags=["teaching-portability"])

class PackageRequest(BaseModel):
    package: dict[str, Any]

class PackageJsonRequest(BaseModel):
    packageJson: str

class ApplyJsonRequest(PackageJsonRequest):
    confirmPackageDigest: str

def _package_from_json(package_json: str) -> dict[str, Any]:
    try:
        value = json.loads(package_json)
    except json.JSONDecodeError as exc:
        raise HTTPException(422, {'code': 'INVALID_TRANSFER_JSON', 'message': str(exc)}) from exc
    if not isinstance(value, dict):
        raise HTTPException(422, {'code': 'INVALID_TRANSFER_JSON', 'message': 'package JSON must contain an object'})
    return value

@router.get("/export")
def export():
    return export_teaching_evidence()

@router.post("/verify")
def verify(req: PackageJsonRequest):
    result = verify_teaching_evidence(_package_from_json(req.packageJson))
    if not result["ok"]:
        raise HTTPException(422, result)
    return result

@router.post("/import/preview")
def import_preview(req: PackageJsonRequest):
    return preview_teaching_evidence_import(_package_from_json(req.packageJson))

@router.post("/import/apply")
def import_apply(req: ApplyJsonRequest):
    try:
        return apply_teaching_evidence_import(_package_from_json(req.packageJson), confirm_package_digest=req.confirmPackageDigest)
    except ValueError as exc:
        raise HTTPException(409, {"code": "TEACHING_IMPORT_BLOCKED", "message": str(exc)}) from exc
