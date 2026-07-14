from __future__ import annotations

from app.phase9.enrichment_alpha2 import (
    VERSION as LEGACY_RUNTIME_VERSION,
    analyze_integrated_alpha2,
)

from .compact_output import compact_analysis
from .contracts import AnalyzeOptions
from .engine import AnalyzerEngine
from .runtime import get_runtime
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION


def _engine() -> AnalyzerEngine:
    # Pass the module-level alias deliberately. Existing façade tests can replace
    # it with a sentinel, while production still routes through AnalyzerEngine.
    return AnalyzerEngine(
        runtime=get_runtime(),
        legacy_engine=analyze_integrated_alpha2,
    )


def analyze_full(
    text,
    nlp=None,
    *,
    use_dictionary=True,
    raw_knp=None,
    kwja_executable=None,
):
    if LEGACY_RUNTIME_VERSION != LEGACY_ENGINE_VERSION:
        raise RuntimeError(
            f"Expected legacy engine {LEGACY_ENGINE_VERSION!r}, "
            f"found {LEGACY_RUNTIME_VERSION!r}."
        )
    options = AnalyzeOptions(
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )
    return _engine().analyze_full(text, nlp, options=options)


def analyze(
    text,
    nlp=None,
    *,
    debug=False,
    use_dictionary=True,
    raw_knp=None,
    kwja_executable=None,
):
    full = analyze_full(
        text,
        nlp,
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )
    return full if debug else compact_analysis(
        full,
        analyzer_version=ANALYZER_VERSION,
    )
