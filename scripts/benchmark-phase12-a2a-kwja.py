from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from app.analyzer.kwja_benchmark import measure_kwja_once, summarize_rows


def parse_args():
    parser = argparse.ArgumentParser(
        description="Phase 12A.2A direct KWJA execution decomposition benchmark."
    )
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--kwja-executable", default=os.environ.get("KWJA_EXE"))
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--model-size", default="base")
    return parser.parse_args()


def load_sentences(path: Path) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = value.get("sentences") if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("Sentence input must be a list or an object containing sentences.")
    sentences = [str(item).strip() for item in rows if str(item).strip()]
    if not sentences:
        raise ValueError("No non-empty benchmark sentences were supplied.")
    return sentences


def main() -> int:
    args = parse_args()
    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1")
    if not args.kwja_executable:
        raise SystemExit("Set KWJA_EXE or pass --kwja-executable.")
    executable = Path(args.kwja_executable)
    if not executable.is_file():
        raise SystemExit(f"KWJA executable not found: {executable}")

    sentences = load_sentences(Path(args.sentences))
    rows = []
    for sentence_index, sentence in enumerate(sentences):
        for attempt in range(1, args.repeats + 1):
            print(
                f"Sentence {sentence_index + 1}/{len(sentences)}, "
                f"attempt {attempt}/{args.repeats}",
                flush=True,
            )
            measured = measure_kwja_once(
                sentence,
                executable=str(executable),
                model_size=args.model_size,
                timeout_seconds=args.timeout_seconds,
            )
            measured.update({
                "sentenceIndex": sentence_index,
                "attempt": attempt,
            })
            rows.append(measured)

    summary = summarize_rows(rows)
    payload = {
        "schema": "Phase12A2AKwjaBenchmark.v1",
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "sentenceCount": len(sentences),
        "repeats": args.repeats,
        "requestCount": len(rows),
        "kwjaVersionCommand": [str(executable), "--version"],
        "modelSize": args.model_size,
        "timeoutSeconds": args.timeout_seconds,
        "summary": summary,
        "rows": rows,
        "safety": {
            "sentenceTextIncluded": False,
            "rawKnpIncluded": False,
            "dictionaryWrites": False,
            "teachingWrites": False,
            "correctionWrites": False,
            "productionExecutionChanged": False,
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Created: {output}")
    print(f"Requests: {len(rows)}")
    print(f"Semantic drift: {summary['semanticDriftDetected']}")
    print(f"Normalized KNP drift: {summary['normalizedKnpDriftDetected']}")
    return 1 if summary["semanticDriftDetected"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
