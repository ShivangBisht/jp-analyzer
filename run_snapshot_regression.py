from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from app.analyzer.pipeline import analyze_full
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest


def read_sentences(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path | None, value) -> None:
    if path is not None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, default=Path("snapshot_regression_report.json"))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()

    sentences = read_sentences(args.input_file)
    references = json.loads(args.reference.read_text(encoding="utf-8-sig"))
    if len(references) != len(sentences):
        raise RuntimeError("Reference count mismatch")

    actuals = []
    if args.resume and args.output and args.output.exists():
        actuals = json.loads(args.output.read_text(encoding="utf-8-sig"))
        print(f"Resuming after {len(actuals)} sentence(s).")

    mismatches = []
    timings = []
    for index in range(len(actuals), len(sentences)):
        sentence_id = f"S{index + 1:04d}"
        started = time.perf_counter()
        last_error = None
        for attempt in range(args.retries + 1):
            try:
                actual = semantic_snapshot(analyze_full(sentences[index]))
                last_error = None
                break
            except Exception as error:
                last_error = error
                print(f"{sentence_id} attempt={attempt + 1} ERROR {type(error).__name__}: {error}")
        if last_error is not None:
            raise last_error
        elapsed = (time.perf_counter() - started) * 1000
        timings.append(elapsed)
        actuals.append(actual)
        write_json(args.output, actuals)
        expected = references[index]
        passed = actual == expected
        if not passed:
            mismatches.append({
                "sentenceId": sentence_id,
                "expectedDigest": snapshot_digest(expected),
                "actualDigest": snapshot_digest(actual),
                "text": sentences[index],
            })
        report = {
            "sentences": len(sentences),
            "completed": len(actuals),
            "passed": len(actuals) - len(mismatches),
            "failed": len(mismatches),
            "semanticParity": len(actuals) == len(sentences) and not mismatches,
            "meanRuntimeMs": sum(timings) / len(timings) if timings else None,
            "mismatches": mismatches,
        }
        write_json(args.report, report)
        print(f"{sentence_id} {'PASS' if passed else 'FAIL'} elapsed_ms={elapsed:.2f} checkpoint={len(actuals)}/{len(sentences)}")

    raise SystemExit(0 if not mismatches else 1)


if __name__ == "__main__":
    main()
