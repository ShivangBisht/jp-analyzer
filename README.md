# JP Analyzer

JP Analyzer is the single supported Japanese linguistic-analysis service in this repository.

## Production entry points

- Python: `app.analyzer.analyze` and `app.analyzer.analyze_full`
- FastAPI: `app.analyzer.service:app`
- Health: `GET /health`
- Analysis: `POST /analyze`

The implementation is organized under `app/analyzer/layers` and owns morphology, structure, candidate generation, dictionary evidence, KWJA evidence, evidence gating, final resolution, diagnostics, and compact/full output.

## Test suite

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\run_tests.ps1
```

Regression corpora are versioned under `tests/corpora`. Generated snapshots and reports remain local.

## KWJA runtime

Routine analysis is cache-only by default and does not contact Hugging Face. Install or refresh the isolated KWJA environment with `scripts/setup_kwja_windows.ps1` during a controlled online session, then set `KWJA_EXE` to that environment's executable. See `docs/KWJA_SETUP_WINDOWS.md`.
