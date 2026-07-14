from dataclasses import dataclass

from .adapters import DictionaryAdapter, KwjaAdapter
from .config import AnalyzerConfig


@dataclass(frozen=True)
class AnalyzerServices:
    kwja: KwjaAdapter
    dictionary: DictionaryAdapter

    @classmethod
    def from_config(cls, config: AnalyzerConfig) -> "AnalyzerServices":
        return cls(KwjaAdapter(config), DictionaryAdapter())
