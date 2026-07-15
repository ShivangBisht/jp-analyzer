from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    if new in text:
        print(f"Already updated: {path.relative_to(ROOT)}")
        return
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print(f"Updated: {path.relative_to(ROOT)}")


# A model cold-start or temporary CPU contention can exceed 120 seconds.
# Raise both paths equally; this changes failure tolerance, not semantics.
for relative in (
    "app/phase9/kwja_alpha1.py",
    "app/analyzer/layers/kwja.py",
):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8-sig")
    if "timeout_seconds: int = 300" in text:
        print(f"Already updated: {relative}")
        continue
    if "timeout_seconds: int = 120" not in text:
        raise RuntimeError(f"Expected KWJA timeout declaration not found: {relative}")
    path.write_text(
        text.replace("timeout_seconds: int = 120", "timeout_seconds: int = 300", 1),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Updated: {relative}")

runner = ROOT / "run_consolidated_parity.py"
runner.write_text(
'''from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

from app.analyzer.ginza_runtime import get_ginza
from app.analyzer.layers import analyze_layers
from app.analyzer.legacy_reference import analyze_legacy
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest


def load_sentences(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def write_json(path: Path | None, value) -> None:
    if path is not None:
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def run(args) -> int:
    sentences = load_sentences(args.input_file)
    if args.limit is not None:
        sentences = sentences[: args.limit]

    references = (
        json.loads(args.reference.read_text(encoding="utf-8-sig"))
        if args.reference
        else None
    )
    if references is not None and len(references) != len(sentences):
        raise RuntimeError("Reference count mismatch")

    snapshots = []
    completed = 0
    if args.resume and args.output and args.output.exists():
        snapshots = json.loads(args.output.read_text(encoding="utf-8-sig"))
        completed = len(snapshots)
        if completed > len(sentences):
            raise RuntimeError("Checkpoint contains more snapshots than input sentences")
        print(f"Resuming after {completed} completed sentence(s).")

    nlp = get_ginza()
    mismatches = []
    timings = []
    failures = []

    for index in range(completed, len(sentences)):
        sentence_id = f"S{index + 1:04d}"
        text = sentences[index]
        started = time.perf_counter()
        last_error = None

        for attempt in range(1, args.retries + 2):
            try:
                result = (
                    analyze_legacy(text, nlp)
                    if args.create_reference
                    else analyze_layers(text, nlp)
                )
                actual = semantic_snapshot(result)
                last_error = None
                break
            except Exception as error:
                last_error = error
                print(
                    f"{sentence_id} attempt={attempt} ERROR "
                    f"{type(error).__name__}: {error}"
                )
                if attempt <= args.retries:
                    time.sleep(args.retry_delay_seconds)

        elapsed = (time.perf_counter() - started) * 1000
        timings.append(elapsed)

        if last_error is not None:
            failures.append(
                {
                    "sentenceId": sentence_id,
                    "text": text,
                    "errorType": type(last_error).__name__,
                    "error": str(last_error),
                }
            )
            write_json(
                args.report,
                {
                    "inputFile": str(args.input_file),
                    "sentences": len(sentences),
                    "completed": len(snapshots),
                    "passed": len(snapshots) - len(mismatches),
                    "failed": len(mismatches),
                    "processingFailures": failures,
                    "semanticParity": False,
                    "mismatches": mismatches,
                },
            )
            raise last_error

        snapshots.append(actual)
        write_json(args.output, snapshots)

        expected = references[index] if references is not None else actual
        passed = actual == expected
        if not passed:
            mismatches.append(
                {
                    "sentenceId": sentence_id,
                    "expectedDigest": snapshot_digest(expected),
                    "actualDigest": snapshot_digest(actual),
                    "text": text,
                }
            )

        checkpoint_report = {
            "inputFile": str(args.input_file),
            "sentences": len(sentences),
            "completed": len(snapshots),
            "passed": len(snapshots) - len(mismatches),
            "failed": len(mismatches),
            "processingFailures": failures,
            "semanticParity": not mismatches and len(snapshots) == len(sentences),
            "meanRuntimeMs": sum(timings) / len(timings) if timings else None,
            "mismatches": mismatches,
        }
        write_json(args.report, checkpoint_report)
        print(
            f"{sentence_id} {'PASS' if passed else 'FAIL'} "
            f"elapsed_ms={elapsed:.2f} checkpoint={len(snapshots)}/{len(sentences)}"
        )

    report = {
        "inputFile": str(args.input_file),
        "sentences": len(sentences),
        "completed": len(snapshots),
        "passed": len(sentences) - len(mismatches),
        "failed": len(mismatches),
        "processingFailures": failures,
        "semanticParity": not mismatches,
        "meanRuntimeMs": sum(timings) / len(timings) if timings else None,
        "mismatches": mismatches,
    }
    write_json(args.report, report)
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != "mismatches"},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not mismatches else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--create-reference", action="store_true")
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, default=Path("consolidated_parity_report.json"))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--retry-delay-seconds", type=float, default=5.0)
    args = parser.parse_args()

    if args.create_reference and args.reference:
        parser.error("choose --create-reference or --reference")
    if not args.create_reference and args.reference is None:
        parser.error("comparison mode requires --reference")
    if args.create_reference and args.output is None:
        parser.error("reference creation requires --output for checkpointing")
    if args.resume and args.output is None:
        parser.error("--resume requires --output")

    raise SystemExit(run(args))


if __name__ == "__main__":
    main()
''',
    encoding="utf-8",
    newline="\n",
)
print("Updated: run_consolidated_parity.py")
