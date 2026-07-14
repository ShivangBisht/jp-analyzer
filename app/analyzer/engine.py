from __future__ import annotations

from collections.abc import Callable
from inspect import signature
from typing import Any

from app.phase9.enrichment_alpha2 import analyze_integrated_alpha2

from .adapters import DictionaryAdapter, KwjaAdapter
from .contracts import AnalyzeOptions
from .runtime import AnalyzerRuntime, get_runtime
from .source_contract import validate_analysis_source
from .version import LEGACY_ENGINE_VERSION


LegacyEngine = Callable[..., dict[str, Any]]


class AnalyzerEngine:
    """Stable production routing over the frozen Phase 9 linguistic engine."""

    def __init__(
        self,
        runtime: AnalyzerRuntime | None = None,
        legacy_engine: LegacyEngine | None = None,
        kwja_adapter: KwjaAdapter | None = None,
        dictionary_adapter: DictionaryAdapter | None = None,
    ):
        self.runtime = runtime or get_runtime()
        self.legacy_engine = legacy_engine or analyze_integrated_alpha2
        services = getattr(self.runtime, "services", None)
        runtime_config = getattr(self.runtime, "config", None)

        self.kwja_adapter = kwja_adapter or (
            services.kwja
            if services is not None
            else KwjaAdapter(runtime_config)
        )
        self.dictionary_adapter = dictionary_adapter or (
            services.dictionary
            if services is not None
            else DictionaryAdapter()
        )

    def analyze_full(
        self,
        text: str,
        nlp=None,
        *,
        options: AnalyzeOptions | None = None,
    ) -> dict[str, Any]:
        opts = options or AnalyzeOptions()
        engine_kwargs = {
            "use_dictionary": opts.use_dictionary,
            "raw_knp": opts.raw_knp,
            "kwja_executable": opts.kwja_executable,
        }
        parameters = signature(self.legacy_engine).parameters
        if "analyze_kwja_fn" in parameters:
            engine_kwargs.update({
                "analyze_kwja_fn": self.kwja_adapter.analyze,
                "evaluate_analysis_fn": self.dictionary_adapter.evaluate_analysis,
                "evaluate_candidate_fn": self.dictionary_adapter.evaluate_candidate,
            })
        result = self.legacy_engine(
            text,
            nlp if nlp is not None else self.runtime.get_nlp(),
            **engine_kwargs,
        )
        if result.get("version") != LEGACY_ENGINE_VERSION:
            raise RuntimeError(
                f"Expected legacy engine {LEGACY_ENGINE_VERSION!r}, "
                f"found {result.get('version')!r}."
            )
        source_diagnostics = validate_analysis_source(result)
        if source_diagnostics:
            codes = ", ".join(x.get("code", "UNKNOWN") for x in source_diagnostics)
            raise RuntimeError(f"Stable source contract failed: {codes}")
        return result
