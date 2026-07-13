from __future__ import annotations

import spacy
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.phase8.dictionary_api import router as dictionary_sync_router
from app.phase8.dictionary_evidence_api import router as dictionary_evidence_router

from .pipeline import analyze
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION, SCHEMA_VERSION


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

_nlp = None
_nlp_name = None


def nlp():
    global _nlp, _nlp_name
    if _nlp is None:
        config = {"components": {"compound_splitter": {"split_mode": "A"}}}
        errors = []
        for name in ("ja_ginza_electra", "ja_ginza"):
            try:
                _nlp = spacy.load(name, config=config)
                _nlp_name = name
                break
            except Exception as exc:
                errors.append(f"{name}: {exc}")
        if _nlp is None:
            raise RuntimeError("GiNZA load failed: " + " | ".join(errors))
    return _nlp


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": ANALYZER_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "engineVersion": LEGACY_ENGINE_VERSION,
        "mode": "production-consolidation-facade",
        "ginzaModel": _nlp_name,
    }


@app.post("/analyze")
def analyze_endpoint(
    req: AnalyzeRequest,
    debug: bool = Query(False),
    dictionary: bool = Query(True),
):
    return analyze(
        req.text,
        nlp(),
        debug=debug,
        use_dictionary=dictionary,
    )
