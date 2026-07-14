# Consolidated Analyzer Checkpoint

## Purpose

This checkpoint creates one production analyzer under `app/analyzer` with explicit linguistic layers. It intentionally preserves the current Phase 10.4 semantics. No linguistic rule, confidence, dictionary policy, KWJA gate, or resolver score is changed.

## Layer order

1. `morphology.py` — GiNZA/Sudachi source-aligned morphology and native structure
2. `protected.py` — orthography, person references and protected boundaries
3. `structure.py` — dependency-aware structural refinements
4. `candidates.py` — grammar, lexical, numeral and discourse candidates
5. `stabilization.py` — final candidate-specificity stabilization
6. `dictionary.py` — advisory exact dictionary evidence
7. `kwja.py` — internal KWJA execution, KNP parsing, alignment and normalization
8. `evidence_gate.py` — controlled KWJA proposals and improvement gate
9. `decision.py` — one global final resolver

## Public route

`app.analyzer.analyze()` -> `AnalyzerEngine` -> consolidated layer engine -> source validation -> compact/full output.

## Temporary compatibility rule

`app/phase8` and `app/phase9` remain only as the legacy parity reference until both corpora pass:

- work computer: `random_sentences.txt` — 200/200
- home computer: `unseen_novel_sentences.txt` — 200/200

Only after 400/400 parity may the legacy packages and phase-specific services be deleted.

## Git checkpoints

1. Apply and run fast tests.
2. Commit the layer consolidation.
3. Create the development reference once with the legacy path.
4. Compare the consolidated path once per sentence.
5. Push and pull at home.
6. Run unseen reference/comparison.
7. Remove the legacy packages only after both reports show zero mismatches.

## Development parity commands

```powershell
& ".\.venv\Scripts\python.exe" ".\run_consolidated_parity.py" ".\random_sentences.txt" --create-reference --output ".\consolidation_dev_reference.json" --report ".\consolidation_dev_reference_report.json"
& ".\.venv\Scripts\python.exe" ".\run_consolidated_parity.py" ".\random_sentences.txt" --reference ".\consolidation_dev_reference.json" --report ".\consolidation_dev_parity_report.json"
```

## Unseen parity commands (home computer)

```powershell
& ".\.venv\Scripts\python.exe" ".\run_consolidated_parity.py" ".\unseen_novel_sentences.txt" --create-reference --output ".\consolidation_unseen_reference.json" --report ".\consolidation_unseen_reference_report.json"
& ".\.venv\Scripts\python.exe" ".\run_consolidated_parity.py" ".\unseen_novel_sentences.txt" --reference ".\consolidation_unseen_reference.json" --report ".\consolidation_unseen_parity_report.json"
```

These commands execute only one analyzer path per sentence. Reference creation uses the legacy path once; comparison uses the consolidated path once.
