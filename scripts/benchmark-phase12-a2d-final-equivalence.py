from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.analyzer.kwja_benchmark import normalized_knp_fingerprint
from app.analyzer.kwja_equivalence import compare_final_results, request_summary
from app.analyzer.kwja_persistent_worker import InteractiveKwjaWorker
from app.analyzer.layers.kwja import normalize_kwja
from app.analyzer.performance import semantic_fingerprint
from app.analyzer.pipeline import analyze


def load_sentences(path: Path) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = value.get("sentences") if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("Expected a JSON array or an object containing sentences.")
    return [str(item).strip() for item in rows if str(item).strip()]


def analyze_raw(text: str, raw_knp: str) -> dict:
    return analyze(
        text,
        raw_knp=raw_knp,
        performance_diagnostics=False,
    )


def execute_sequence(worker, sentences, sequence):
    rows = []
    final_results = []
    for ordinal, sentence_index in enumerate(sequence, start=1):
        text = sentences[sentence_index]
        worker_result = worker.analyze(text)
        normalized = normalize_kwja(text, worker_result.output, elapsed_ms=None)
        final = analyze_raw(text, worker_result.output)
        rows.append(request_summary(
            sentence_index=sentence_index,
            request_ordinal=ordinal,
            raw_knp=worker_result.output,
            normalized_knp_fingerprint=normalized_knp_fingerprint(worker_result.output),
            adapter_fingerprint=semantic_fingerprint(normalized),
            final_result=final,
            elapsed_ms=worker_result.elapsed_ms,
            process_id=worker_result.process_id,
        ))
        final_results.append(final)
    return rows, final_results


def parse_sequence(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--kwja-executable", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--target-index", type=int, default=2)
    parser.add_argument("--other-index", type=int, default=1)
    parser.add_argument("--repeat-count", type=int, default=6)
    args = parser.parse_args()

    sentences = load_sentences(Path(args.sentences))
    target = args.target_index
    other = args.other_index
    sequences = {
        "targetOnly": [target] * args.repeat_count,
        "alternating": [target if index % 2 == 0 else other for index in range(args.repeat_count * 2)],
        "otherThenTarget": [other] * args.repeat_count + [target],
        "targetFresh": [target],
    }

    experiments = []
    for name, sequence in sequences.items():
        print(f"Experiment {name}: {sequence}", flush=True)
        worker = InteractiveKwjaWorker(args.kwja_executable)
        process_start_ms = worker.start()
        try:
            rows, final_results = execute_sequence(worker, sentences, sequence)
            diagnostics = worker.diagnostics()
        finally:
            worker.stop()
        target_rows = [row for row in rows if row["sentenceIndex"] == target]
        target_results = [
            result for result, sentence_index in zip(final_results, sequence)
            if sentence_index == target
        ]
        experiments.append({
            "name": name,
            "sequence": sequence,
            "processStartMs": process_start_ms,
            "rows": rows,
            "targetRows": target_rows,
            "targetFinalComparison": compare_final_results(target_results),
            "diagnostics": diagnostics,
        })

    target_first_fingerprints = {
        experiment["name"]: experiment["targetRows"][0]["finalAnalyzerFingerprint"]
        for experiment in experiments
        if experiment["targetRows"]
    }
    payload = {
        "schema": "Phase12A2DFinalEquivalence.v1",
        "productionActivated": False,
        "targetIndex": target,
        "otherIndex": other,
        "experiments": experiments,
        "crossWorkerFirstTargetFingerprints": target_first_fingerprints,
        "crossWorkerFirstTargetDistinct": len(set(target_first_fingerprints.values())),
        "safety": {
            "sentenceTextIncluded": False,
            "rawKnpIncluded": False,
            "databaseWritesRequested": False,
            "productionExecutionChanged": False,
        },
    }
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print("Created:", args.output)
    print("Cross-worker first-target variants:", payload["crossWorkerFirstTargetDistinct"])


if __name__ == "__main__":
    main()
