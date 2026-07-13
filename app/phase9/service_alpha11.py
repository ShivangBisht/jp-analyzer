from __future__ import annotations

import spacy
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.phase8.compact_output_alpha341 import compact_alpha34
from .integrated_alpha11 import VERSION, analyze_integrated_alpha11


class Request(BaseModel):
    text: str


app = FastAPI(title="Phase 9 Alpha 1.1 Integrated Read-Only KWJA", version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"status": "ok", "version": VERSION, "mode": "alpha34-plus-kwja-read-only"}


@app.post("/analyze-layered-phase9-alpha11")
def analyze(req: Request, debug: bool = Query(False), dictionary: bool = Query(True)):
    full = analyze_integrated_alpha11(req.text, nlp(), use_dictionary=dictionary)
    if debug:
        return full
    compact = compact_alpha34(full, debug=False)
    compact["version"] = VERSION
    compact["kwja_summary"] = {
        "available": bool((full.get("kwja_metadata_alpha1") or {}).get("available")),
        "model_size": (full.get("kwja_metadata_alpha1") or {}).get("model_size"),
        "alignment_complete": (full.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete"),
        "morpheme_count": len(full.get("kwja_morphemes_alpha1") or []),
        "basic_phrase_count": len(full.get("kwja_basic_phrases_alpha1") or []),
        "predicate_count": len(full.get("kwja_predicate_phrases_alpha1") or []),
        "argument_proposal_count": len(full.get("kwja_argument_evidence_alpha1") or []),
        "entity_count": len(full.get("kwja_entities_alpha1") or []),
        "alignment_diagnostic_count": len(full.get("kwja_alignment_diagnostics_alpha1") or []),
        "read_only": True,
    }
    compact["phase9_contract"] = full.get("phase9_alpha11_contract")
    compact["phase9_diagnostics"] = full.get("diagnostics_phase9_alpha11") or []
    return compact
