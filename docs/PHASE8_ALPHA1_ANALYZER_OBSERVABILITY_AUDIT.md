# Phase 8 Alpha 1: Analyzer Observability Audit

**Audited commit:** `47cd14af8effc51b1a715e6ea5edc00b419af0f2`  
**Branch:** `feature/phase8-teaching-annotations`  
**Audit mode:** read-only; no analyzer behavior or runtime data changed.

## Executive conclusion

The analyzer already exposes substantial supervision evidence, but it has **two decision systems** that must both be captured:

1. the core Alpha 2 resolver, which creates an optimal full-sentence partition using integer utility scores;
2. the later Reader candidate selector, which can replace complete compatibility spans using conservative Boolean gates and a separate priority tuple.

The compact response exposes the second system and a projection of the first, but omits enough core state that the current Teaching snapshots are not reliably replayable. In particular, core resolver decisions/conflicts, complete dictionary evidence, total partition score, tie-break outcome, candidate-generation rejection events, dictionary revision, and correction-free raw compact output are not first-class compact fields.

## Production call graph

```text
AnalyzerEngine.analyze_full
  -> analyze_integrated_alpha2
     -> analyze_layered_alpha321
     -> evaluate_analysis_candidates
     -> analyze_layered_alpha34
        -> normalize_candidates
        -> resolve_candidates (core DP resolver)
     -> KWJA analysis and read-only attachment
     -> generate_kwja_candidates
     -> classify_kwja_proposal
     -> candidate-specific dictionary evaluation
     -> resolve_candidates again (final core DP resolver)
  -> compact_analysis
     -> project_reader_candidates
        -> existing resolver candidate projection
        -> generate_reader_candidates
        -> evaluate_generated_reader_candidates
        -> attach_reader_candidate_structural_evidence
     -> select_reader_output (Reader selector)
        -> project_reader_spans (compatibility baseline)
        -> conservative gates and priority selection
     -> apply_active_corrections (post-selection exact-occurrence override)
```

## Primary findings

### A1-01: Two authoritative-looking selection systems exist

The core resolver uses dynamic programming over `utility_score`. The Reader selector does not reuse that score for generated candidates. It uses explicit eligibility gates and sorts eligible proposals by `(family_order, span_length, dictionary_source_count)`. Therefore a future snapshot must preserve both decisions rather than treating `readerSelection` as the complete analyzer decision trace.

### A1-02: Corrections are applied after both analyzers have selected output

`compact_analysis` first builds candidates and selects Reader output, then calls `apply_active_corrections`. A corrected merged span is therefore not necessarily a generated candidate, scored target, or resolver decision. This directly explains why operational Teaching can create a structural span without analyzer-native lexical identity.

### A1-03: The core score is observable but not fully decomposed

Core candidates serialize `utility_dimensions` and `utility_score`. The dimensions are integrity, protected/context family, specificity, completeness, dictionary support, and confidence. However dictionary support is a compressed number. The exact component calculation is recoverable from source and raw evidence, but the contribution breakdown and scoring-policy version are not serialized per snapshot.

### A1-04: The final partition score is computed but discarded

The DP `_Plan.score` determines the winning full-sentence partition. Neither `resolve_candidates` nor compact output returns the final total score, runner-up partition, score margin, or tie-break reason. Future ranking replay can reconstruct some of this from candidates, but cannot prove which tie-break path occurred without explicit trace data.

### A1-05: Candidate absence is not observable as an event

Range validation, deduplication, protected-boundary filtering, KWJA allow-list logic, and generation-specific conditions often return or continue without emitting a rejection record. The final snapshot can show that a target candidate is absent, but not always why it was never created. Alpha 2 needs generation-event observability, not merely final candidate inventory.

### A1-06: Candidate IDs have mixed stability

Generated Reader candidate IDs are content-derived from family, offsets, role, and lookup keys. Core IDs such as `a34cN`, `a2kwjaN`, and fallback IDs depend on generation order. They are valid within one snapshot but unsuitable as cross-version identities. Content fingerprints are required.

### A1-07: Dictionary identity is insufficient for replay and freshness

Dictionary evidence is rich at candidate level, but analyzer output does not expose a stable dictionary revision bound to the decision. Entry count and last sync metadata are not enough to prove identical lookup state. A content/snapshot identity must be captured.

### A1-08: Reader policy fields are consequences, not score features

`knownLookupKey`, `frequencyLookupKey`, comprehension, New Words, mining, and colour are created after selection by Reader projection or the Reader selector. They must be recorded as derived policy outputs, not incorrectly included as original scoring inputs.

### A1-09: Existing-resolver and generated Reader candidates are semantically different

Existing core candidates preserve utility score in the nested `features` object. Reader-generated candidates carry lookup hypotheses, candidate-specific dictionary evaluation, structural evidence, abstention reasons, and Boolean eligibility. The schema currently places both in one `readerCandidates` array without an explicit decision-system discriminator beyond `candidateSource`.

### A1-10: Raw Teaching snapshots can be contaminated by active corrections

Normal compact analysis always applies active corrections. A raw analyzer observation must be captured before correction application via an explicit correction-free entry point, not by replacing `readerSpans` after compact analysis.

## Alpha 2 implications

`AnalyzerDecisionSnapshot v1` must contain:

- lossless full analysis before the new Teaching action;
- final core candidate set and candidate fingerprints;
- core utility dimensions, score, score-policy version, selected partition score, and tie-break trace;
- KWJA proposal generation and eligibility records;
- complete Reader-generated candidate evidence, gates, priority, and selection;
- compatibility baseline Reader spans before generated-candidate replacement;
- correction-free final Reader spans;
- active correction revision recorded separately as context;
- dictionary snapshot identity;
- generation events for generated, deduplicated, filtered, gated, and rejected targets.

## Phase result

Alpha 1 is complete as an observability and gap audit. No scoring or Teaching behavior was modified. Alpha 2 may now formalize the immutable snapshot while preserving both decision systems.
