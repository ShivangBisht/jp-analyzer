from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .layers.dictionary_api import router as dictionary_sync_router
from .layers.dictionary_evidence_api import router as dictionary_evidence_router
from .reader_corrections_api import router as reader_corrections_router
from .teaching_decision_api import router as teaching_decision_router
from .teaching_quality_api import router as teaching_quality_router
from .teaching_corpus_export_api import router as teaching_corpus_export_router
from .teaching_offline_evaluation_api import router as teaching_offline_evaluation_router
from .teaching_controlled_activation_api import router as teaching_controlled_activation_router
from .teaching_portability_api import router as teaching_portability_router

from .health import health_report
from .pipeline import analyze
from .version import ANALYZER_VERSION


class AnalyzeRequest(BaseModel):
    text: str


app = FastAPI(title="JP Analyzer", version=ANALYZER_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dictionary_sync_router)
app.include_router(dictionary_evidence_router)
app.include_router(reader_corrections_router)
app.include_router(teaching_decision_router)
app.include_router(teaching_quality_router)
app.include_router(teaching_corpus_export_router)
app.include_router(teaching_offline_evaluation_router)
app.include_router(teaching_controlled_activation_router)
app.include_router(teaching_portability_router)


@app.get("/health")
def health():
    return health_report()


@app.post("/analyze")
def analyze_endpoint(
    req: AnalyzeRequest,
    debug: bool = Query(False),
    dictionary: bool = Query(True),
):
    return analyze(req.text, debug=debug, use_dictionary=dictionary)
