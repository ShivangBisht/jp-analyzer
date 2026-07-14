from __future__ import annotations

from typing import Any

from ..dictionary_runtime import (
    evaluate_analysis_candidates,
    evaluate_candidate,
    get_dictionary_status,
)


class DictionaryAdapter:
    """Stable dictionary evidence adapter; a miss never rejects a candidate."""

    def status(self) -> dict[str, Any]:
        return get_dictionary_status()

    def evaluate_analysis(self, analysis: dict[str, Any]) -> dict[str, Any]:
        return evaluate_analysis_candidates(analysis)

    def evaluate_candidate(
        self,
        candidate: dict[str, Any],
        parser_pos: str | None = None,
    ) -> dict[str, Any]:
        return evaluate_candidate(candidate, parser_pos)
