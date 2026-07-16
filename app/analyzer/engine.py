from __future__ import annotations

from collections.abc import Callable
from inspect import signature
from typing import Any

from .layers import analyze_layers

from .adapters import DictionaryAdapter, KwjaAdapter
from .contracts import AnalyzeOptions
from .runtime import AnalyzerRuntime, get_runtime
from .source_contract import validate_analysis_source
from .version import ENGINE_CONTRACT_VERSION


AnalyzerFunction = Callable[..., dict[str, Any]]


class AnalyzerEngine:
    """Single production entry point over the consolidated linguistic layers."""

    def __init__(
        self,
        runtime: AnalyzerRuntime | None = None,
        analyzer_fn: AnalyzerFunction | None = None,
        kwja_adapter: KwjaAdapter | None = None,
        dictionary_adapter: DictionaryAdapter | None = None,
    ):
        self.runtime = runtime or get_runtime()
        self.analyzer_fn = analyzer_fn or analyze_layers
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
        parameters = signature(self.analyzer_fn).parameters
        if "analyze_kwja_fn" in parameters:
            engine_kwargs.update({
                "analyze_kwja_fn": self.kwja_adapter.analyze,
                "evaluate_analysis_fn": self.dictionary_adapter.evaluate_analysis,
                "evaluate_candidate_fn": self.dictionary_adapter.evaluate_candidate,
            })
        result = self.analyzer_fn(
            text,
            nlp if nlp is not None else self.runtime.get_nlp(),
            **engine_kwargs,
        )
        if result.get("version") != ENGINE_CONTRACT_VERSION:
            raise RuntimeError(
                f"Expected engine contract {ENGINE_CONTRACT_VERSION!r}, "
                f"found {result.get('version')!r}."
            )
        source_diagnostics = validate_analysis_source(result)
        if source_diagnostics:
            codes = ", ".join(x.get("code", "UNKNOWN") for x in source_diagnostics)
            raise RuntimeError(f"Stable source contract failed: {codes}")
        return result
