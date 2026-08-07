from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.analyzer.adapters.kwja_adapter import KwjaAdapter
from app.analyzer.compact_output import compact_analysis
from app.analyzer.config import AnalyzerConfig
from app.analyzer.engine import AnalyzerEngine
from app.analyzer.kwja_persistent_runtime import stop_persistent_kwja_runtimes
from app.analyzer.kwja_production_parity import compare_production_modes
from app.analyzer.version import ANALYZER_VERSION


def load_sentences(path: Path) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(value, dict):
        value = value.get("sentences")
    if not isinstance(value, list):
        raise ValueError(
            'sentences file must contain a JSON array or an object with a "sentences" array'
        )
    sentences = [str(item).strip() for item in value if str(item).strip()]
    if not sentences:
        raise ValueError("sentences file contains no non-empty sentences")
    return sentences


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare fresh and persistent production adapter routes."
    )
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--kwja-executable", required=True)
    parser.add_argument("--output", required=True)
    arguments = parser.parse_args()

    sentences = load_sentences(Path(arguments.sentences))
    executable = Path(arguments.kwja_executable)
    if not executable.is_file():
        raise FileNotFoundError(f"KWJA executable not found: {executable}")

    engines: dict[str, AnalyzerEngine] = {}

    def analyze(text: str, mode: str):
        engine = engines.get(mode)
        if engine is None:
            config = AnalyzerConfig(
                kwja_executable=executable,
                kwja_execution_mode=mode,
            )
            engine = AnalyzerEngine(kwja_adapter=KwjaAdapter(config))
            engines[mode] = engine
        full = engine.analyze_full(text)
        return compact_analysis(full, analyzer_version=ANALYZER_VERSION)

    try:
        result = compare_production_modes(sentences, analyze_fn=analyze)
    finally:
        stop_persistent_kwja_runtimes()

    output = Path(arguments.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Created: {output}")
    print(f"Qualified: {result['qualified']}")
    print(f"Final differences: {result['differenceCount']}")
    if not result["qualified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
