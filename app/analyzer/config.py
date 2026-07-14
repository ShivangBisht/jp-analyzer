from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AnalyzerConfig:
    ginza_models: tuple[str, ...] = ("ja_ginza_electra", "ja_ginza")
    ginza_split_mode: str = "A"
    kwja_executable: Path | None = None
    dictionary_database: Path = Path(__file__).resolve().parents[2] / "data" / "phase8_analysis_lexicon.sqlite3"

    @classmethod
    def from_environment(cls):
        value = os.getenv("KWJA_EXE")
        return cls(kwja_executable=Path(value) if value else None)

    def kwja_available(self) -> bool:
        return bool(self.kwja_executable and self.kwja_executable.is_file())
