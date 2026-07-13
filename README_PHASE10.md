# Phase 10 Production Consolidation

## Phase 10.1: stable facade

Phase 10.1 introduces a supported production package and API while preserving
Phase 9 Alpha 2.2 behavior exactly.

### Stable Python API

```python
from app.analyzer import analyze, analyze_full
```

- `analyze_full(...)` returns the exact validated Alpha 2.2 result.
- `analyze(..., debug=True)` returns that same full result.
- `analyze(..., debug=False)` returns the stable compact consumer schema.

### Stable HTTP API

```powershell
.\.venv\Scripts\python.exe -m uvicorn `
    app.analyzer.service:app `
    --host 127.0.0.1 `
    --port 8776
```

Endpoints:

- `GET /health`
- `POST /analyze`
- `GET /dictionary-sync/status`
- dictionary sync/evidence routes inherited from the validated implementation

### Validation

```powershell
.\.venv\Scripts\python.exe .	est_phase10_facade.py
.\.venv\Scripts\python.exe .un_phase10_parity.py .andom_sentences.txt --limit 5
```

For full parity, run the 200-sentence development and unseen corpora. The parity
runner deliberately executes both entry points, so runtime is about twice the
normal corpus runtime.

### Contract

No linguistic policy, confidence, candidate, alignment, dictionary-evidence,
or resolver behavior is changed in Phase 10.1. Legacy Phase 8 and Phase 9 files
remain active until later consolidation stages achieve corpus parity.
