from __future__ import annotations

from .runtime import AnalyzerRuntime, get_runtime
from .version import ANALYZER_VERSION, LEGACY_ENGINE_VERSION, SCHEMA_VERSION


def health_report(runtime: AnalyzerRuntime | None = None) -> dict:
    active = runtime or get_runtime()
    status = active.status()
    return {
        "status": "ok",
        "version": ANALYZER_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "engineVersion": LEGACY_ENGINE_VERSION,
        "mode": "production-consolidation-runtime-routing",
        "ginzaModel": status.ginza_model,
        "kwja": status.kwja,
        "dictionary": status.dictionary,
    }
