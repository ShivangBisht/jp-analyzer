from __future__ import annotations

import argparse
import json
import time
from hashlib import sha256
from pathlib import Path
from typing import Any

import spacy

from app.analyzer.pipeline import analyze_full
from app.phase9.enrichment_alpha2 import analyze_integrated_alpha2


def load_ginza():
    config = {"components": {"compound_splitter": {"split_mode": "A"}}}
    errors = []
    for name in ("ja_ginza_electra", "ja_ginza"):
        try:
            return spacy.load(name, config=config), name
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    raise RuntimeError("Unable to load GiNZA. " + " | ".join(errors))


def stable_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def digest(value: Any) -> str:
    return sha256(stable_json(value).encode("utf-8")).hexdigest()


def visible_signature(result: dict[str, Any]) -> list[tuple[Any, ...]]:
    return [
        (
            item.get("start"),
            item.get("end"),
            item.get("surface"),
            item.get("role"),
            item.get("headword"),
            item.get("grammar_id"),
            item.get("confidence"),
            item.get("source_layer"),
        )
        for item in (result.get("resolved_spans_alpha2") or [])
    ]


def compare(legacy: dict[str, Any], stable: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "full_output_equal": legacy == stable,
        "full_output_hash_equal": digest(legacy) == digest(stable),
        "visible_projection_equal": visible_signature(legacy)
        == visible_signature(stable),
        "diagnostics_equal": (legacy.get("diagnostics_alpha2") or [])
        == (stable.get("diagnostics_alpha2") or []),
        "kwja_alignment_equal": (
            (legacy.get("kwja_metadata_alpha1") or {}).get(
                "source_alignment_complete"
            )
            == (stable.get("kwja_metadata_alpha1") or {}).get(
                "source_alignment_complete"
            )
        ),
    }
    return {"passed": (
                checks["visible_projection_equal"]
                and checks["diagnostics_equal"]
                and checks["kwja_alignment_equal"]
            ), "checks": checks}


def run(input_path: Path, limit: int | None) -> int:
    sentences = [
        line.strip()
        for line in input_path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if limit is not None:
        sentences = sentences[:limit]

    nlp, ginza_model = load_ginza()
    mismatches = []
    timings = []

    for index, text in enumerate(sentences, 1):
        started = time.perf_counter()
        legacy = analyze_integrated_alpha2(text, nlp)
        stable = analyze_full(text, nlp)
        elapsed = (time.perf_counter() - started) * 1000
        timings.append(elapsed)
        comparison = compare(legacy, stable)
        if not comparison["passed"]:
            mismatches.append(
                {
                    "sentenceId": f"S{index:04d}",
                    "text": text,
                    **comparison,
                    "legacyHash": digest(legacy),
                    "stableHash": digest(stable),
                    "legacyProjection": visible_signature(legacy),
                    "stableProjection": visible_signature(stable),
                }
            )
        print(
            f"S{index:04d} parity={'PASS' if comparison['passed'] else 'FAIL'} "
            f"elapsed_ms={elapsed:.2f}"
        )

    summary = {
        "phase": "10.1-stable-facade",
        "inputFile": str(input_path),
        "ginzaModel": ginza_model,
        "requestedSentences": len(sentences),
        "parityPassedSentences": len(sentences) - len(mismatches),
        "parityFailedSentences": len(mismatches),
        "exactParity": not mismatches,
        "meanCombinedRuntimeMs": (
            sum(timings) / len(timings) if timings else None
        ),
    }
    Path("phase10_parity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path("phase10_parity_mismatches.json").write_text(
        json.dumps(mismatches, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not mismatches else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    raise SystemExit(run(args.input_file, args.limit))


if __name__ == "__main__":
    main()
