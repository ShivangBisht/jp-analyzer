# Phase 12A.2D: Persistent-worker final analyzer equivalence

This benchmark answers two production-gating questions:

1. Do varying persistent-worker KWJA results change authoritative Reader output?
2. Does the result for a target sentence depend on requests processed earlier by the worker?

The benchmark feeds each worker-produced KNP result through the existing complete analyzer using the established `raw_knp` test path. It compares final Reader spans, candidates, selection, resolved spans, coverage, and diagnostics. Production `/analyze` remains unchanged.

The benchmark is read-only regarding Teaching, corrections, and dictionaries. Result JSON excludes sentence text and raw KNP output.
