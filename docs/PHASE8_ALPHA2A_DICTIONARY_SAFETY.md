# Phase 8 Alpha 2A: Dictionary Safety Hardening

## Changes

- `DELETE /dictionary-sync/cache` now returns HTTP 410 with `DICTIONARY_CLEAR_DISABLED` and never calls the store clear function.
- The bulk `dictionary_store.clear()` helper requires `allow_authoritative=True`; ordinary runtime calls fail closed.
- Existing lifecycle tests use the explicit destructive flag only against test-isolated database state.
- Novel Audio Miner no longer exports the clear client or renders the misleading **Clear analyzer cache** button.
- Corpus-grade AnalyzerDecisionSnapshot capture rejects a not-ready dictionary by default.
- Diagnostic capture can opt in with `require_dictionary_ready=False`, but remains visibly dictionary-unbound.
- Dictionary identity now includes database path and a registry digest derived from installed dictionary identity, type, priority, count, content digest, revision, version, and enabled state.

## Non-goals

Alpha 2A does not change dictionary synchronization, per-dictionary install/update/remove, analyzer scoring, candidate generation, Reader selection, or operational corrections.
