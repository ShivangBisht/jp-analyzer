from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .kwja_alpha1 import analyze_kwja_alpha1, attach_kwja_read_only, VERSION

class TextRequest(BaseModel):
    text: str

class AttachRequest(BaseModel):
    text: str
    existing_analysis: dict

app = FastAPI(title="Phase 9 Alpha 1 KWJA Read-Only Layer", version=VERSION)

@app.get("/health")
def health():
    return {"status":"ok", "version":VERSION, "mode":"kwja-read-only"}

@app.post("/kwja-layer-alpha1")
def kwja_layer(req: TextRequest):
    return {"text":req.text, **analyze_kwja_alpha1(req.text)}

@app.post("/attach-kwja-layer-alpha1")
def attach(req: AttachRequest):
    layer = analyze_kwja_alpha1(req.text)
    return attach_kwja_read_only(req.existing_analysis, layer)
