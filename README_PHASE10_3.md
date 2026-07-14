# Phase 10.3 — Runtime Routing Consolidation

Phase 10.3 routes the stable production façade through an `AnalyzerEngine` and
one reusable `AnalyzerRuntime`. The frozen Phase 9 Alpha 2.2 implementation
remains the linguistic engine.

## Scope

- stable analysis options and projection contracts;
- reusable GiNZA runtime ownership;
- stable engine invocation;
- production health report;
- source-contract validation after every analysis.

## Explicit non-goals

This phase does not change grammar, lexical candidates, dictionary evidence,
KWJA proposal generation, confidence, resolver scoring, or final spans.

## Required tests

```powershell
.\.venv\Scripts\python.exe .	est_phase10_engine_routing.py
.\.venv\Scripts\python.exe .	est_phase10_runtime_reuse.py
.\.venv\Scripts\python.exe .	est_phase10_health_contract.py
.\.venv\Scripts\python.exe .	est_phase10_facade.py
.\.venv\Scripts\python.exe .	est_phase10_runtime_contracts.py
.\.venv\Scripts\python.exe .	est_phase10_semantic_snapshot.py
```

Then run 5- and 20-sentence parity plus S0198. Full 400-sentence parity is not
required until a complete legacy implementation family is replaced or removed.
