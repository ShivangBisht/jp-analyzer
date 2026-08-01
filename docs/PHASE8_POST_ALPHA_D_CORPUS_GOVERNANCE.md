# Phase 8 Post-Alpha D: Corpus Governance and Readiness

`TeachingCorpusGovernance.v1` is a deterministic, read-only report over Teaching evidence. It reports coverage, balance, provenance grouping, split leakage, configured collection gaps, and maturity labels without tuning or activating the analyzer.

## Maturity labels

- `harness-valid`: integrity, artifact verification, duplicate/conflict policy, and provenance leakage checks pass.
- `train-fit`: the configured minimum counts and diversity gates are satisfied.
- `validation-passed`: reserved for later candidate validation; governance does not claim it.
- `test-passed`: reserved for protected final evaluation; governance does not claim it.
- `deployment-eligible`: always false in Phase 8.

The default thresholds are collection-policy defaults, not linguistic guarantees. They are versioned in the report and may be changed explicitly through the POST report endpoint.
