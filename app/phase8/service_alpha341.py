from __future__ import annotations
import spacy
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .alpha321 import analyze_layered_alpha321
from .compact_output_alpha341 import compact_alpha34
from .dictionary_api import router as dictionary_sync_router
from .dictionary_evidence import evaluate_analysis_candidates
from .dictionary_evidence_api import router as dictionary_evidence_router
from .resolver_alpha34 import analyze_layered_alpha34

class Request(BaseModel):
    text: str

app = FastAPI(title="Phase 8 Alpha 3.4.1 Compact Resolver", version="8.0.0-alpha3.4.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dictionary_sync_router)
app.include_router(dictionary_evidence_router)
_nlp = None


def nlp():
    global _nlp
    if _nlp is None:
        cfg = {"components": {"compound_splitter": {"split_mode": "A"}}}
        errors = []
        for name in ("ja_ginza_electra", "ja_ginza"):
            try:
                _nlp = spacy.load(name, config=cfg)
                break
            except Exception as exc:
                errors.append(str(exc))
        if _nlp is None:
            raise RuntimeError("GiNZA load failed: " + " | ".join(errors))
    return _nlp


@app.get("/health")
def health():
    return {"status": "ok", "version": "8.0.0-alpha3.4.1"}


@app.post("/analyze-layered-alpha341")
def analyze(req: Request, debug: bool = Query(False)):
    base = analyze_layered_alpha321(req.text, nlp())
    dictionary_result = evaluate_analysis_candidates(base)
    full = analyze_layered_alpha34(req.text, nlp(), dictionary_result)
    return compact_alpha34(full, debug=debug)


@app.post("/analyze-layered-alpha341-without-dictionary")
def analyze_without_dictionary(req: Request, debug: bool = Query(False)):
    full = analyze_layered_alpha34(req.text, nlp(), None)
    return compact_alpha34(full, debug=debug)
