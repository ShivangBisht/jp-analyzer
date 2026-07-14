from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnalyzeOptions:
    debug: bool = False
    use_dictionary: bool = True
    raw_knp: str | None = None
    kwja_executable: str | None = None


def linguistic_projection(result: dict[str, Any]) -> list[tuple[Any, ...]]:
    """Return the stable reader-visible projection contract."""
    return [
        (
            item.get("start"),
            item.get("end"),
            item.get("surface"),
            item.get("role"),
            item.get("headword"),
            item.get("grammar_id"),
            item.get("confidence"),
            item.get("source_layer"),
        )
        for item in (result.get("resolved_spans_alpha2") or [])
    ]
