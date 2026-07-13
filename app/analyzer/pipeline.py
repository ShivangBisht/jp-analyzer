from __future__ import annotations

from typing import Any

from app.phase9.enrichment_alpha2 import (
    VERSION as LEGACY_RUNTIME_VERSION,
    analyze_integrated_alpha2,
)

from .compact_output import compact_analysis
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION


def analyze_full(
    text: str,
    nlp,
    *,
    use_dictionary: bool = True,
    raw_knp: str | None = None,
    kwja_executable: str | None = None,
) -> dict[str, Any]:
    """Return the exact validated Phase 9 Alpha 2.2 result.

    Phase 10.1 intentionally delegates without mutating, copying, filtering,
    reordering, or relabelling the legacy result. This is the parity anchor for
    later layer-by-layer consolidation.
    """
    if LEGACY_RUNTIME_VERSION != LEGACY_ENGINE_VERSION:
        raise RuntimeError(
            "Phase 10 facade expected legacy engine "
            f"{LEGACY_ENGINE_VERSION!r}, found {LEGACY_RUNTIME_VERSION!r}."
        )
    return analyze_integrated_alpha2(
        text,
        nlp,
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )


def analyze(
    text: str,
    nlp,
    *,
    debug: bool = False,
    use_dictionary: bool = True,
    raw_knp: str | None = None,
    kwja_executable: str | None = None,
) -> dict[str, Any]:
    """Stable production entry point.

    debug=True returns the exact Phase 9 Alpha 2.2 result for strict parity.
    debug=False returns the stable compact schema intended for Novel Miner.
    """
    full = analyze_full(
        text,
        nlp,
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )
    if debug:
        return full
    return compact_analysis(full, analyzer_version=ANALYZER_VERSION)
