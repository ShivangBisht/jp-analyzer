from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


KWJA_EXECUTION_MODES = {"fresh", "persistent"}


@dataclass(frozen=True)
class AnalyzerConfig:
    ginza_models: tuple[str, ...] = ("ja_ginza_electra", "ja_ginza")
    ginza_split_mode: str = "A"
    kwja_executable: Path | None = None
    kwja_execution_mode: str = "fresh"
    dictionary_database: Path = Path(__file__).resolve().parents[2] / "data" / "phase8_analysis_lexicon.sqlite3"

    @classmethod
    def from_environment(cls):
        executable = os.getenv("KWJA_EXE")
        mode = str(os.getenv("KWJA_EXECUTION_MODE") or "fresh").strip().lower()
        if mode not in KWJA_EXECUTION_MODES:
            allowed = ", ".join(sorted(KWJA_EXECUTION_MODES))
            raise ValueError(f"KWJA_EXECUTION_MODE must be one of: {allowed}")
        return cls(
            kwja_executable=Path(executable) if executable else None,
            kwja_execution_mode=mode,
        )

    def kwja_available(self) -> bool:
        return bool(self.kwja_executable and self.kwja_executable.is_file())
