from __future__ import annotations
import spacy
from fastapi import FastAPI, Query
from pydantic import BaseModel
from .enrichment_alpha2 import VERSION, analyze_integrated_alpha2

class Request(BaseModel):
    text: str

app = FastAPI(title="Phase 9 Alpha 2 KWJA Candidate Enrichment", version=VERSION)
_nlp = None

def nlp():
    global _nlp
    if _nlp is None:
        cfg={"components":{"compound_splitter":{"split_mode":"A"}}}
        errors=[]
        for name in ("ja_ginza_electra","ja_ginza"):
            try:
                _nlp=spacy.load(name,config=cfg); break
            except Exception as exc: errors.append(str(exc))
        if _nlp is None: raise RuntimeError("GiNZA load failed: " + " | ".join(errors))
    return _nlp

@app.get("/health")
def health(): return {"status":"ok","version":VERSION,"mode":"kwja-controlled-candidate-enrichment"}

@app.post("/analyze-layered-phase9-alpha2")
def analyze(req: Request, debug: bool=Query(False), dictionary: bool=Query(True)):
    result=analyze_integrated_alpha2(req.text,nlp(),use_dictionary=dictionary)
    if debug: return result
    return {
        "text":result["text"], "version":VERSION,
        "resolved_spans":result["resolved_spans_alpha2"],
        "change_summary":result["alpha2_change_summary"],
        "kwja_candidates":result["kwja_candidates_alpha2"],
        "diagnostics":result["diagnostics_alpha2"],
        "contract":result["phase9_alpha2_contract"],
    }
