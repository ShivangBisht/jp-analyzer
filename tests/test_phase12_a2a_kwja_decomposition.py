from __future__ import annotations

from app.analyzer.kwja_benchmark import (
    measure_kwja_once,
    normalized_knp_fingerprint,
    summarize_rows,
)

RAW_A = "# S-ID:1 kwja:2.5.1\n* -1D\n+ -1D\n猫 ねこ 猫 名詞 6 普通名詞 1 * 0 * 0\nEOS\n"
RAW_B = "# S-ID:DIFFERENT kwja:2.5.1\n* -1D\n+ -1D\n猫 ねこ 猫 名詞 6 普通名詞 1 * 0 * 0\nEOS\n"


def test_normalized_knp_fingerprint_ignores_only_comment_headers():
    assert normalized_knp_fingerprint(RAW_A) == normalized_knp_fingerprint(RAW_B)
    changed = RAW_B.replace("猫 ねこ 猫", "犬 いぬ 犬")
    assert normalized_knp_fingerprint(RAW_A) != normalized_knp_fingerprint(changed)


def test_measurement_separates_execution_and_normalization():
    def runner(text, **kwargs):
        return RAW_A, 123.0

    def normalizer(text, raw_knp, **kwargs):
        return {
            "kwja_metadata_alpha1": {"source_alignment_complete": True},
            "kwja_alignment_diagnostics_alpha1": [],
            "kwja_morphemes_alpha1": [{"surface": text}],
        }

    row = measure_kwja_once(
        "猫",
        executable="unused",
        runner=runner,
        normalizer=normalizer,
    )
    assert row["rawExecutionReportedMs"] == 123.0
    assert row["sourceAlignmentComplete"] is True
    assert row["counts"]["morphemes"] == 1
    assert row["rawOutputBytes"] > 0


def test_summary_detects_semantic_drift():
    base = {
        "sentenceSha256": "sha256:x",
        "rawExecutionReportedMs": 10,
        "rawExecutionWallMs": 11,
        "normalizationMs": 1,
        "combinedMeasuredMs": 12,
        "rawOutputSha256": "raw",
        "normalizedKnpSha256": "knp",
        "adapterSemanticFingerprint": "semantic-a",
        "sourceAlignmentComplete": True,
        "errorDiagnosticCount": 0,
    }
    same = dict(base)
    summary = summarize_rows([base, same])
    assert summary["semanticDriftDetected"] is False
    changed = dict(base, adapterSemanticFingerprint="semantic-b")
    summary = summarize_rows([base, changed])
    assert summary["semanticDriftDetected"] is True
