# Phase 8 Alpha 2: AnalyzerDecisionSnapshot v1

## Purpose

Capture an immutable, content-addressed, correction-free observation of the existing analyzer without changing candidate generation, scoring, selection, Reader output, or operational correction behavior.

## Captured sections

- exact sentence and SHA-256 identity;
- analyzer, engine, schema, scoring, resolver, Reader selection and projection versions;
- dictionary snapshot identity and digest;
- lossless full analysis;
- core candidates with content fingerprints and score explanations;
- core decisions, conflicts, resolved spans, selected partition score and historical tie-policy limitation;
- Reader compatibility spans, candidates, priorities, decisions and correction-free selected spans;
- correction revision as context, with application disabled;
- explicit generation-observability and replayability capability declarations.

## Non-behavioral contract

The default `compact_analysis(..., apply_corrections=True)` path remains byte-for-byte equivalent to the previous default call. Snapshot capture uses `apply_corrections=False` and does not mutate the supplied full analysis.

## Replay levels

- Level 0 archival: supported.
- Level 1 core score replay: supported from stored candidates and policy identity.
- Level 2 core partition replay: supported for the selected partition and total score; historical per-comparison tie events and runner-up partition remain unavailable.
- Level 3 Reader selector replay: supported from candidate evidence, gate output, priority and selection.
- Level 4 full analyzer rerun: not guaranteed because compatible model binaries and dictionary content are external dependencies.

## Deferred gaps

Alpha 2 does not alter generation code to emit filtered-proposal events and does not calculate a runner-up partition. The snapshot declares these limitations explicitly. Those gaps can be instrumented later without changing the v1 meaning.
