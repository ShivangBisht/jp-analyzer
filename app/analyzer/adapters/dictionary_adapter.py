from __future__ import annotations
from typing import Any
from ..layers.dictionary import evaluate_analysis_candidates, evaluate_candidate
from ..layers.dictionary_store import DB_PATH, status

class DictionaryAdapter:
    """Stable dictionary evidence adapter; a miss never rejects a candidate."""
    def status(self) -> dict[str, Any]:
        result = dict(status())
        result["database"] = str(DB_PATH)
        return result
    def evaluate_analysis(self, analysis: dict[str, Any]) -> dict[str, Any]:
        return evaluate_analysis_candidates(analysis)
    def evaluate_candidate(self, candidate: dict[str, Any], parser_pos: str | None = None) -> dict[str, Any]:
        return evaluate_candidate(candidate, parser_pos)
