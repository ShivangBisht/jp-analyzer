from __future__ import annotations
from app.phase9.enrichment_alpha2 import VERSION as LEGACY_RUNTIME_VERSION, analyze_integrated_alpha2
from .compact_output import compact_analysis
from .ginza_runtime import get_ginza
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION

def analyze_full(text, nlp=None, *, use_dictionary=True, raw_knp=None, kwja_executable=None):
    if LEGACY_RUNTIME_VERSION != LEGACY_ENGINE_VERSION:
        raise RuntimeError(f"Expected legacy engine {LEGACY_ENGINE_VERSION!r}, found {LEGACY_RUNTIME_VERSION!r}.")
    return analyze_integrated_alpha2(text, nlp if nlp is not None else get_ginza(), use_dictionary=use_dictionary, raw_knp=raw_knp, kwja_executable=kwja_executable)

def analyze(text, nlp=None, *, debug=False, use_dictionary=True, raw_knp=None, kwja_executable=None):
    full = analyze_full(text, nlp, use_dictionary=use_dictionary, raw_knp=raw_knp, kwja_executable=kwja_executable)
    return full if debug else compact_analysis(full, analyzer_version=ANALYZER_VERSION)
