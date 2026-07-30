# Phase 8 Alpha 1: Analyzer Observability Audit

**Audited commit:** `47cd14af8effc51b1a715e6ea5edc00b419af0f2`  
**Branch:** `feature/phase8-teaching-annotations`  
**Audit mode:** read-only; no analyzer behavior or runtime data changed.

## Serialization gaps

### Critical

1. No correction-free compact analyzer output entry point.
2. No core selected partition score or tie-break trace.
3. No candidate-generation event ledger for filtered or never-created candidates.
4. No stable dictionary revision/content identity in analysis output.
5. Core resolver decisions/conflicts omitted from compact output and current Teaching snapshot projection.
6. Operational corrections are post-selection replacements, not analyzer-native candidates.

### High

7. No content fingerprint for order-derived core candidate IDs.
8. No explicit version for the core score formula/constants.
9. Dictionary-support dimension does not serialize its contribution breakdown.
10. Reader selector priority tuple is computed but not stored.
11. No complete competing partition inventory or runner-up margin.
12. Existing and Reader-generated candidates share one array despite different scoring semantics.
13. Generation, eligibility, ranking, projection and correction statuses are not one normalized lifecycle.

### Medium

14. Some source-layer constants and grammar priorities are versioned only by source commit.
15. Dictionary compact evidence excludes entry definitions appropriately, but snapshot identity and truncation metadata are absent.
16. Evidence evaluation exceptions abstain safely but do not include full error context.
17. Final Reader policy reasons are implicit in role/family branches rather than serialized reason codes.
18. Raw/effective/post-correction semantics are not enforced at analyzer entry-point level.

## Required disposition

Alpha 2 should add observability without changing selection behavior. Each gap is either `capture-existing`, `add-trace`, `add-version`, or `defer-to-later-behavior-change`. No weights or gates should change during snapshot formalization.
