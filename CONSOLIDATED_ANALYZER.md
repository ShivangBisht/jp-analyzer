# Consolidated JP Analyzer

The supported production implementation is `app.analyzer.analyze`. The analyzer owns morphology, protected ranges, structure, candidates, dictionary evidence, KWJA evidence, evidence gating, the final decision, diagnostics, and compact/full output.

Historical Phase 8, Phase 9, and Phase 10 wrapper implementations were removed after exact semantic parity on 200 development and 200 fresh unseen sentences. Existing phase-named debug fields remain temporarily for response-schema compatibility; they are not separate runtime implementations.

## Run tests

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\run_tests.ps1
```

## Run frozen snapshot regression

```powershell
& .\.venv\Scripts\python.exe .\run_snapshot_regression.py .\random_sentences.txt --reference .\consolidation_dev_reference_200.json --output .\post_cleanup_dev_actual.json --report .\post_cleanup_dev_report.json
```
