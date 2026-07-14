from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.phase8.dictionary_api import router as dictionary_sync_router
from app.phase8.dictionary_evidence_api import router as dictionary_evidence_router
from .dictionary_runtime import get_dictionary_status
from .ginza_runtime import get_ginza, ginza_model_name
from .kwja_runtime import kwja_status
from .pipeline import analyze
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION, SCHEMA_VERSION
class AnalyzeRequest(BaseModel): text: str
app = FastAPI(title="JP Analyzer", version=ANALYZER_VERSION)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])
app.include_router(dictionary_sync_router)
app.include_router(dictionary_evidence_router)
@app.get("/health")
def health():
    return {"status":"ok", "version":ANALYZER_VERSION, "schemaVersion":SCHEMA_VERSION, "engineVersion":LEGACY_ENGINE_VERSION, "mode":"production-consolidation-infrastructure", "ginzaModel":ginza_model_name(), "kwja":kwja_status(), "dictionary":get_dictionary_status()}
@app.post("/analyze")
def analyze_endpoint(req: AnalyzeRequest, debug: bool = Query(False), dictionary: bool = Query(True)):
    return analyze(req.text, get_ginza(), debug=debug, use_dictionary=dictionary)
