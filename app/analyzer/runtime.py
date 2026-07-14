from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from .config import AnalyzerConfig
from .ginza_runtime import get_ginza, ginza_model_name
from .services import AnalyzerServices


@dataclass(frozen=True)
class RuntimeStatus:
    ginza_model: str | None
    kwja: dict
    dictionary: dict


class AnalyzerRuntime:
    """Stable owner of reusable analyzer runtime dependencies."""

    def __init__(self, config: AnalyzerConfig | None = None):
        self.config = config or AnalyzerConfig.from_environment()
        self.services = AnalyzerServices.from_config(self.config)

    def get_nlp(self):
        return get_ginza(self.config)

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(
            ginza_model=ginza_model_name(),
            kwja=self.services.kwja.status(),
            dictionary=self.services.dictionary.status(),
        )


_lock = RLock()
_runtime: AnalyzerRuntime | None = None


def get_runtime(config: AnalyzerConfig | None = None) -> AnalyzerRuntime:
    global _runtime
    with _lock:
        if _runtime is None:
            _runtime = AnalyzerRuntime(config)
        elif config is not None and _runtime.config != config:
            raise RuntimeError(
                "Analyzer runtime is already initialized with a different configuration."
            )
        return _runtime


def reset_runtime_for_tests() -> None:
    global _runtime
    with _lock:
        _runtime = None
