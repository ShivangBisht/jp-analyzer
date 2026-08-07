# Phase 12A.3B Bounded Recovery and Fresh Fallback

Phase 12A.3B hardens the opt-in persistent KWJA route without changing analyzer semantics.

## Recovery policy

1. A persistent request is attempted on the current worker.
2. Any worker or protocol exception invalidates and stops that worker.
3. The request is retried once on a clean worker generation.
4. If the clean-worker retry also fails, execution falls back once to the established fresh `kwja.exe --text` path.
5. Fresh-path failures retain the existing exception behavior and are not hidden.

There are no unbounded retries. An uncertain worker is never reused.

## Observability

The runtime tracks successful persistent requests, worker generations, restart count, fallback count, last execution mode, and last persistent error. These operational values are not included in analyzer semantic fingerprints, Reader contracts, corrections, or Teaching artifacts.

## Frozen contracts

Raw KNP from either persistent execution or fresh fallback enters the same existing `analyze_kwja_alpha1` normalization path. Morphology, structural evidence, candidates, dictionary evidence, evidence gates, resolver output, diagnostics, `readerSpans`, compact/full responses, corrections, and Teaching formats remain unchanged.

## Activation

Fresh remains the default. Recovery and fallback are used only when `KWJA_EXECUTION_MODE=persistent` is explicitly selected.
