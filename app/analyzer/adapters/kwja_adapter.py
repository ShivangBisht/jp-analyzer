from __future__ import annotations

from typing import Any

from ..config import AnalyzerConfig
from ..kwja_runtime import analyze_kwja, kwja_status, resolve_kwja_executable


class KwjaAdapter:
    """Stable adapter preserving the validated Phase 9 KWJA evidence schema."""

    def __init__(self, config: AnalyzerConfig | None = None):
        self.config = config or AnalyzerConfig.from_environment()

    def status(self) -> dict[str, Any]:
        return kwja_status(self.config)

    def analyze(
        self,
        text: str,
        *,
        raw_knp: str | None = None,
        executable: str | None = None,
    ) -> dict[str, Any]:
        selected = executable
        if raw_knp is None and selected is None:
            selected = str(resolve_kwja_executable(config=self.config))
        return analyze_kwja(text, raw_knp=raw_knp, executable=selected)
