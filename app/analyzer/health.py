from __future__ import annotations

from .runtime import AnalyzerRuntime, get_runtime
from .version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION, SCHEMA_VERSION
from .reader_projection import READER_SPAN_SCHEMA_VERSION
from .reader_corrections import correction_revision


def health_report(runtime: AnalyzerRuntime | None = None) -> dict:
    active = runtime or get_runtime()
    status = active.status()
    return {
        "status": "ok",
        "version": ANALYZER_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
        "correctionRevision": correction_revision(),
        "engineVersion": ENGINE_CONTRACT_VERSION,
        "mode": "production-consolidation-stable-evidence-routing",
        "ginzaModel": status.ginza_model,
        "kwja": status.kwja,
        "dictionary": status.dictionary,
    }
