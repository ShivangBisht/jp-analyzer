# Phase 12A.3C Production-Route Parity

Phase 12A.3C adds a read-only qualification harness that compares the real fresh and persistent production adapter routes.

## Scope

- The harness runs every supplied sentence once through fresh execution and once through persistent execution.
- Both modes continue through the same full analyzer and compact projection.
- Qualification compares only the frozen final fields: `text`, `readerSpans`, `readerCandidates`, `readerSelection`, `resolvedSpans`, `coverage`, and `diagnostics`.
- Reader spans must be contiguous, range-valid, surface-valid, and reconstruct the exact source.
- Output stores fingerprints and timings, not sentence text or raw KNP.
- Persistent workers are stopped in a `finally` block.

## Non-goals

This phase does not change the production default, add startup warm-up, modify FastAPI lifecycle handlers, change health responses, alter analyzer evidence, or change Teaching, correction, dictionary, Reader, compact, or full-response contracts.

## Command

```powershell
& ".\.venv\Scripts\python.exe" `
  ".\scripts\benchmark-phase12-a3c-production-parity.py" `
  --sentences "PATH_TO_PRIVATE_SENTENCES.json" `
  --kwja-executable $env:KWJA_EXE `
  --output "D:\Mining\_PROJECT_WORK\phase12_a3c_production_parity.json"
```

Qualification requires `qualified: true`, `differenceCount: 0`, and no Reader contract errors. Fresh remains the default after this phase.
