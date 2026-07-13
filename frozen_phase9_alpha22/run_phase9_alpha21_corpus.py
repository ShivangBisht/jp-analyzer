from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import Counter
from pathlib import Path

import spacy

from app.phase9.enrichment_alpha2 import VERSION, analyze_integrated_alpha2


def load_ginza():
    cfg = {"components": {"compound_splitter": {"split_mode": "A"}}}
    errors = []
    for name in ("ja_ginza_electra", "ja_ginza"):
        try:
            return spacy.load(name, config=cfg), name
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    raise RuntimeError("Unable to load GiNZA. " + " | ".join(errors))


def signature(spans):
    return [
        (x.get("start"), x.get("end"), x.get("surface"), x.get("role"),
         x.get("headword"), x.get("grammar_id"))
        for x in spans
    ]


def run(path: Path, limit: int | None):
    sentences = [x.strip() for x in path.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    if limit is not None:
        sentences = sentences[:limit]

    nlp, ginza_model = load_ginza()
    rows, failures, changed_rows, flagged, timings = [], [], [], [], []
    proposal_types, selected_types = Counter(), Counter()
    baseline_unresolved_total = 0
    alpha2_unresolved_total = 0

    results_path = Path("phase9_alpha21_sentence_results.jsonl")
    with results_path.open("w", encoding="utf-8") as stream:
        for index, text in enumerate(sentences, 1):
            sid = f"S{index:04d}"
            started = time.perf_counter()
            try:
                result = analyze_integrated_alpha2(text, nlp)
                elapsed = (time.perf_counter() - started) * 1000
                timings.append(elapsed)

                baseline = result.get("resolved_spans_alpha34") or []
                alpha2 = result.get("resolved_spans_alpha2") or []
                proposals = result.get("kwja_candidates_alpha2") or []
                selected_kwja = [x for x in alpha2 if x.get("source_layer") == "kwja-alpha2"]
                diagnostics = result.get("diagnostics_alpha2") or []
                kwmeta = result.get("kwja_metadata_alpha1") or {}

                baseline_unresolved = sum(x.get("role") == "unresolved" for x in baseline)
                alpha2_unresolved = sum(x.get("role") == "unresolved" for x in alpha2)
                baseline_unresolved_total += baseline_unresolved
                alpha2_unresolved_total += alpha2_unresolved

                for p in proposals:
                    proposal_types.update([p.get("grammar_id") or p.get("headword") or p.get("policy") or "unknown"])
                for s in selected_kwja:
                    selected_types.update([s.get("grammar_id") or s.get("headword") or "unknown-term"])

                changed = signature(baseline) != signature(alpha2)
                row = {
                    "sentence_id": sid,
                    "text": text,
                    "elapsed_ms": round(elapsed, 2),
                    "coverage_complete": "".join(x.get("surface") or "" for x in alpha2) == text,
                    "kwja_alignment_complete": bool(kwmeta.get("source_alignment_complete")),
                    "baseline_unresolved_count": baseline_unresolved,
                    "alpha2_unresolved_count": alpha2_unresolved,
                    "unresolved_reduction": baseline_unresolved - alpha2_unresolved,
                    "final_projection_changed": changed,
                    "kwja_proposal_count": len(proposals),
                    "kwja_selected_count": len(selected_kwja),
                    "kwja_proposals": proposals,
                    "selected_kwja_spans": selected_kwja,
                    "baseline_spans": baseline if changed else [],
                    "alpha2_spans": alpha2 if changed else [],
                    "diagnostics": diagnostics,
                    "layer0_immutable": bool((result.get("phase9_alpha2_contract") or {}).get("layer0_immutable")),
                }
                rows.append(row)
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")

                if changed:
                    changed_rows.append(row)
                reasons = []
                if not row["coverage_complete"]: reasons.append("incomplete-coverage")
                if not row["kwja_alignment_complete"]: reasons.append("kwja-alignment")
                if diagnostics: reasons.append("diagnostics")
                if alpha2_unresolved: reasons.append("unresolved-remains")
                if len(selected_kwja) and alpha2_unresolved > baseline_unresolved: reasons.append("unresolved-increased")
                if reasons:
                    row["flag_reasons"] = reasons
                    flagged.append(row)
            except Exception as exc:
                failures.append({"sentence_id": sid, "text": text, "error": repr(exc)})

            if index % 10 == 0 or index == len(sentences):
                print(f"Processed {index}/{len(sentences)}")

    summary = {
        "benchmark_version": VERSION,
        "input_file": str(path),
        "ginza_model": ginza_model,
        "kwja_model": "base",
        "requested_sentences": len(sentences),
        "processed_successfully": len(rows),
        "processing_failures": len(failures),
        "complete_projection_sentences": sum(x["coverage_complete"] for x in rows),
        "kwja_alignment_complete_sentences": sum(x["kwja_alignment_complete"] for x in rows),
        "sentences_with_kwja_proposals": sum(bool(x["kwja_proposal_count"]) for x in rows),
        "sentences_with_selected_kwja_candidates": sum(bool(x["kwja_selected_count"]) for x in rows),
        "sentences_with_changed_projection": len(changed_rows),
        "baseline_unresolved_span_total": baseline_unresolved_total,
        "alpha2_unresolved_span_total": alpha2_unresolved_total,
        "unresolved_span_reduction": baseline_unresolved_total - alpha2_unresolved_total,
        "sentences_with_remaining_unresolved": sum(bool(x["alpha2_unresolved_count"]) for x in rows),
        "sentences_with_diagnostics": sum(bool(x["diagnostics"]) for x in rows),
        "proposal_type_distribution": dict(proposal_types.most_common()),
        "selected_type_distribution": dict(selected_types.most_common()),
        "timing_ms": {
            "mean": round(statistics.mean(timings), 2) if timings else None,
            "median": round(statistics.median(timings), 2) if timings else None,
            "max": round(max(timings), 2) if timings else None,
        },
        "flagged_sentence_count": len(flagged),
        "failures": failures,
    }

    Path("phase9_alpha21_corpus_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path("phase9_alpha21_changed_sentences.json").write_text(
        json.dumps(changed_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path("phase9_alpha21_flagged_sentences.json").write_text(
        json.dumps(flagged, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = [
        "PHASE 9 ALPHA 2.1 FROZEN 200-SENTENCE BENCHMARK",
        "=" * 54,
        json.dumps(summary, ensure_ascii=False, indent=2),
        "",
        "CHANGED SENTENCES",
    ]
    for row in changed_rows:
        report.extend([
            f"{row['sentence_id']} | proposals={row['kwja_proposal_count']} | selected={row['kwja_selected_count']} | unresolved {row['baseline_unresolved_count']} -> {row['alpha2_unresolved_count']}",
            row["text"],
            "Selected KWJA: " + " | ".join(
                f"{x.get('surface')}:{x.get('grammar_id') or x.get('headword') or 'term'}"
                for x in row["selected_kwja_spans"]
            ),
            "",
        ])
    Path("phase9_alpha21_review_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("Benchmark complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="random_sentences.txt")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    run(Path(args.input), args.limit)
