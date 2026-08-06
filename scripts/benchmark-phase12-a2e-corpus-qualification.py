from __future__ import annotations

import argparse
import json
import os
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.analyzer.kwja_persistent_worker import InteractiveKwjaWorker
from app.analyzer.kwja_qualification import compare_to_baseline, file_sha256, protected_file_hashes, result_summary
from app.analyzer.layers.kwja import run_kwja
from app.analyzer.pipeline import analyze


def load_sentences(path: Path) -> list[str]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    rows = value.get("sentences") if isinstance(value, dict) else value
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected benchmark sentences.")
    return [str(item).strip() for item in rows]


def db_guard(path: Path) -> dict:
    if not path.is_file():
        return {"path": str(path), "exists": False}
    con = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        counts = {}
        for table in tables:
            safe = table.replace('"', '""')
            counts[table] = con.execute(f'SELECT COUNT(*) FROM "{safe}"').fetchone()[0]
    finally:
        con.close()
    return {"path": str(path), "exists": True, "sha256": file_sha256(path), "bytes": path.stat().st_size, "rowCounts": counts}


def final(text: str, raw: str) -> dict:
    return analyze(text, raw_knp=raw, performance_diagnostics=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentences", required=True)
    parser.add_argument("--kwja-executable", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=12025)
    args = parser.parse_args()

    sentences = load_sentences(Path(args.sentences))
    indexes = list(range(len(sentences)))
    shuffled = indexes.copy()
    random.Random(args.seed).shuffle(shuffled)
    sequences = {"forward": indexes, "reverse": list(reversed(indexes)), "shuffled": shuffled}

    teaching_db = ROOT / "data/teaching_decisions.sqlite3"
    corrections_db = ROOT / "data/reader_corrections.sqlite3"
    dictionary_db = ROOT / "data/phase8_analysis_lexicon.sqlite3"
    before = {
        "protectedFiles": protected_file_hashes(ROOT),
        "teaching": db_guard(teaching_db),
        "corrections": db_guard(corrections_db),
        "dictionary": db_guard(dictionary_db),
    }

    baseline = {}
    for index, text in enumerate(sentences):
        print(f"Baseline {index + 1}/{len(sentences)}", flush=True)
        raw, elapsed = run_kwja(text, executable=args.kwja_executable)
        result = final(text, raw)
        summary = result_summary(index, "fresh-baseline", 1, result, elapsed, -1)
        baseline[index] = {"finalAnalyzerFingerprint": summary["finalAnalyzerFingerprint"], "fieldFingerprints": summary["fieldFingerprints"], "elapsedMs": elapsed}

    rows = []
    lifecycle = []
    for name, sequence in sequences.items():
        print(f"Sequence {name}: {sequence}", flush=True)
        worker = InteractiveKwjaWorker(args.kwja_executable)
        start_ms = worker.start()
        pid = worker.process.pid
        try:
            for ordinal, index in enumerate(sequence, start=1):
                wr = worker.analyze(sentences[index])
                rows.append(result_summary(index, name, ordinal, final(sentences[index], wr.output), wr.elapsed_ms, wr.process_id))
            running_before_stop = worker.diagnostics()["running"]
        finally:
            worker.stop()
        lifecycle.append({"sequence": name, "processStartMs": start_ms, "processId": pid, "runningBeforeStop": running_before_stop, "stopped": worker.process is None})

    # Forced termination and restart qualification, never routed to production.
    test_index = 0
    worker = InteractiveKwjaWorker(args.kwja_executable)
    worker.start()
    first_pid = worker.process.pid
    worker.process.kill()
    worker.process.wait(timeout=10)
    killed_detected = worker.process.poll() is not None
    worker.stop()
    restart_ms = worker.start()
    restarted_pid = worker.process.pid
    try:
        recovered = worker.analyze(sentences[test_index])
        recovered_row = result_summary(test_index, "restart-recovery", 1, final(sentences[test_index], recovered.output), recovered.elapsed_ms, recovered.process_id)
    finally:
        worker.stop()
    rows.append(recovered_row)
    lifecycle.append({"sequence": "forced-restart", "firstPid": first_pid, "killedDetected": killed_detected, "restartMs": restart_ms, "restartedPid": restarted_pid, "pidChanged": first_pid != restarted_pid, "stopped": worker.process is None})

    comparison = compare_to_baseline(baseline, rows)
    after = {
        "protectedFiles": protected_file_hashes(ROOT),
        "teaching": db_guard(teaching_db),
        "corrections": db_guard(corrections_db),
        "dictionary": db_guard(dictionary_db),
    }
    guards = {
        "protectedFilesUnchanged": before["protectedFiles"] == after["protectedFiles"],
        "teachingUnchanged": before["teaching"] == after["teaching"],
        "correctionsUnchanged": before["corrections"] == after["corrections"],
        "dictionaryUnchanged": before["dictionary"] == after["dictionary"],
    }
    passed = comparison["qualified"] and all(guards.values()) and all(item.get("stopped") for item in lifecycle)
    payload = {
        "schema": "Phase12A2ECorpusQualification.v1",
        "productionActivated": False,
        "sentenceCount": len(sentences),
        "sequenceCount": len(sequences),
        "requestCount": len(rows),
        "seed": args.seed,
        "baseline": baseline,
        "rows": rows,
        "comparison": comparison,
        "lifecycle": lifecycle,
        "guards": guards,
        "passed": passed,
        "safety": {"sentenceTextIncluded": False, "rawKnpIncluded": False, "teachingWritesRequested": False, "correctionWritesRequested": False, "dictionaryWritesRequested": False, "productionExecutionChanged": False},
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print("Created:", args.output)
    print("Passed:", passed)
    print("Final differences:", comparison["differenceCount"])
    print("Guards:", guards)
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
