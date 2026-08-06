from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.analyzer.kwja_persistent_worker import InteractiveKwjaWorker
from app.analyzer.kwja_benchmark import normalized_knp_fingerprint
from app.analyzer.layers.kwja import normalize_kwja, run_kwja
from app.analyzer.performance import semantic_fingerprint


def sha(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_sentences(path: Path) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = value.get("sentences") if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("Expected a JSON array or an object containing sentences.")
    return [str(value).strip() for value in rows if str(value).strip()]


def summarize_times(values):
    ordered = sorted(values)
    return {
        "minimum": min(values),
        "median": statistics.median(values),
        "mean": statistics.mean(values),
        "maximum": max(values),
    }


def fingerprint(text: str, raw: str) -> dict:
    normalized = normalize_kwja(text, raw, elapsed_ms=None)
    return {
        "rawSha256": sha(raw),
        "normalizedKnpSha256": normalized_knp_fingerprint(raw),
        "adapterSemanticFingerprint": semantic_fingerprint(normalized),
        "aligned": bool((normalized.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete")),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--kwja-executable", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--indexes", default="1,2,6")
    parser.add_argument("--same-worker-repeats", type=int, default=10)
    parser.add_argument("--fresh-worker-repeats", type=int, default=3)
    parser.add_argument("--reference-repeats", type=int, default=3)
    args = parser.parse_args()

    sentences = load_sentences(Path(args.sentences))
    indexes = [int(value.strip()) for value in args.indexes.split(",") if value.strip()]
    results = []

    for index in indexes:
        text = sentences[index]
        reference = []
        for attempt in range(args.reference_repeats):
            print(f"Reference executable: sentence {index}, {attempt + 1}/{args.reference_repeats}", flush=True)
            raw, elapsed = run_kwja(text, executable=args.kwja_executable)
            reference.append({"elapsedMs": elapsed, **fingerprint(text, raw)})

        same_worker = []
        worker = InteractiveKwjaWorker(args.kwja_executable)
        start_ms = worker.start()
        try:
            for attempt in range(args.same_worker_repeats):
                print(f"Same worker: sentence {index}, {attempt + 1}/{args.same_worker_repeats}", flush=True)
                result = worker.analyze(text)
                same_worker.append({"elapsedMs": result.elapsed_ms, "processId": result.process_id, **fingerprint(text, result.output)})
            same_worker_diagnostics = worker.diagnostics()
        finally:
            worker.stop()

        fresh_workers = []
        for attempt in range(args.fresh_worker_repeats):
            print(f"Fresh worker: sentence {index}, {attempt + 1}/{args.fresh_worker_repeats}", flush=True)
            worker = InteractiveKwjaWorker(args.kwja_executable)
            fresh_start = worker.start()
            try:
                result = worker.analyze(text)
                fresh_workers.append({"processStartMs": fresh_start, "elapsedMs": result.elapsed_ms, "processId": result.process_id, **fingerprint(text, result.output)})
            finally:
                worker.stop()

        results.append({
            "sentenceIndex": index,
            "sentenceSha256": sha(text),
            "reference": reference,
            "sameWorker": {"processStartMs": start_ms, "rows": same_worker, "diagnostics": same_worker_diagnostics},
            "freshWorkers": fresh_workers,
        })

    def variants(rows, field):
        return len({row[field] for row in rows})

    for result in results:
        for key, rows in (("referenceSummary", result["reference"]), ("sameWorkerSummary", result["sameWorker"]["rows"]), ("freshWorkerSummary", result["freshWorkers"])):
            result[key] = {
                "timingMs": summarize_times([row["elapsedMs"] for row in rows]),
                "rawVariants": variants(rows, "rawSha256"),
                "normalizedKnpVariants": variants(rows, "normalizedKnpSha256"),
                "adapterSemanticVariants": variants(rows, "adapterSemanticFingerprint"),
                "allAligned": all(row["aligned"] for row in rows),
            }

    payload = {
        "schema": "Phase12A2CPersistentWorkerBenchmark.v1",
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "productionActivated": False,
        "protocol": "documented-interactive-cli-eod",
        "indexes": indexes,
        "results": results,
        "safety": {"sentenceTextIncluded": False, "rawKnpIncluded": False, "databaseWrites": False, "productionExecutionChanged": False},
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print("Created:", args.output)


if __name__ == "__main__":
    main()
