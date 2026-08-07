# Phase 12A.3A Persistent KWJA Runtime Foundation

Phase 12A.3A introduces an opt-in production runtime boundary for the already-qualified interactive KWJA process.

## Scope

- Fresh subprocess execution remains the default.
- `KWJA_EXECUTION_MODE=persistent` selects one process per resolved KWJA executable and model size.
- Requests are serialized so interactive protocol output cannot interleave.
- Startup is lazy and shutdown is registered through `atexit`.
- Any timeout or worker/protocol failure invalidates and stops the worker.
- Phase 12A.3B will define bounded retry and fresh-process fallback policy.

## Frozen contracts

This phase does not change morphology, KWJA normalization, structure, candidate generation, dictionary evidence, evidence gates, resolution, diagnostics, compact/full response fields, Reader spans, corrections, or Teaching artifacts. Persistent execution supplies raw KNP to the same `analyze_kwja_alpha1` normalization path used by injected benchmark KNP.

## Activation

Default:

```text
KWJA_EXECUTION_MODE=fresh
```

Opt-in validation:

```text
KWJA_EXECUTION_MODE=persistent
```

Persistent mode must remain opt-in until the home synthetic corpus and the original handpicked novel corpus both pass final analyzer equivalence and data-integrity guards.
