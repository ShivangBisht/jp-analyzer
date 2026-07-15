from pathlib import Path
from app.analyzer.config import AnalyzerConfig
from app.analyzer.layers.dictionary_store import DB_PATH


def main():
    expected = Path(__file__).resolve().parent / "data" / "phase8_analysis_lexicon.sqlite3"
    assert DB_PATH == expected, (DB_PATH, expected)
    assert AnalyzerConfig().dictionary_database == expected
    print("Consolidated dictionary path test passed")


if __name__ == "__main__":
    main()
