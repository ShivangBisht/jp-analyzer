from __future__ import annotations
from threading import RLock
import spacy
from .config import AnalyzerConfig

_lock = RLock()
_nlp = None
_model_name = None

def get_ginza(config: AnalyzerConfig | None = None):
    global _nlp, _model_name
    cfg = config or AnalyzerConfig.from_environment()
    with _lock:
        if _nlp is not None:
            return _nlp
        errors = []
        options = {"components": {"compound_splitter": {"split_mode": cfg.ginza_split_mode}}}
        for name in cfg.ginza_models:
            try:
                _nlp = spacy.load(name, config=options)
                _model_name = name
                return _nlp
            except Exception as exc:
                errors.append(f"{name}: {exc}")
        raise RuntimeError("GiNZA load failed: " + " | ".join(errors))

def ginza_model_name():
    return _model_name

def reset_ginza_for_tests():
    global _nlp, _model_name
    with _lock:
        _nlp = None
        _model_name = None
