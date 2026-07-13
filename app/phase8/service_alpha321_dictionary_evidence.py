from __future__ import annotations

import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .alpha321 import analyze_layered_alpha321
from .dictionary_api import router as dictionary_sync_router
from .dictionary_evidence import evaluate_analysis_candidates
from .dictionary_evidence_api import router as dictionary_evidence_router


class Request(BaseModel):
    text: str


app = FastAPI(
    title="Phase 8 Alpha 3.2.1 + Dictionary Evidence",
    version="8.0.0-alpha3.2.1-dict-evidence",
)
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
    return {"status": "ok", "version": "8.0.0-alpha3.2.1-dict-evidence"}


@app.post("/analyze-layered-alpha321")
def analyze(req: Request):
    # Existing stable analysis; unchanged by dictionary evidence.
    return analyze_layered_alpha321(req.text, nlp())


@app.post("/analyze-layered-alpha321-with-dictionary-evidence")
def analyze_with_dictionary(req: Request):
    analysis = analyze_layered_alpha321(req.text, nlp())
    evidence = evaluate_analysis_candidates(analysis)
    return {
        "analysis": analysis,
        "dictionary_evidence_alpha34": evidence,
        "contract": {
            "analysis_is_identical_to_plain_endpoint": True,
            "dictionary_is_evidence_only": True,
            "final_resolver_not_run": True,
        },
    }
