import spacy
from fastapi import FastAPI
from pydantic import BaseModel
from .alpha321 import analyze_layered_alpha321

class Request(BaseModel):
    text: str

app = FastAPI(title="Phase 8 Alpha 3.2.1", version="8.0.0-alpha3.2.1")
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
    return {"status": "ok", "version": "8.0.0-alpha3.2.1"}

@app.post("/analyze-layered-alpha321")
def analyze(req: Request):
    return analyze_layered_alpha321(req.text, nlp())
