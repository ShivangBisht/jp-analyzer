# Phase 8 Alpha 1: Analyzer Observability Audit

**Audited commit:** `47cd14af8effc51b1a715e6ea5edc00b419af0f2`  
**Branch:** `feature/phase8-teaching-annotations`  
**Audit mode:** read-only; no analyzer behavior or runtime data changed.

## Core resolver scoring

### Utility dimensions

```text
[0] integrity = 100
[1] protected/context family
[2] specificity
[3] completeness
[4] dictionary corroboration
[5] confidence × 100
```

Protected/context values derive from role ordering, with punctuation 100 and proper name 90. Specificity varies by family and grammar specificity. Completeness grows with source length and has different caps for structural families. Dictionary support is family-specific and capped.

### Score formula

```text
if unresolved: score = 0
per_char = d1*1,000,000 + d2*10,000 + d4*100 + d5
whole_span_bonus = d3*1,000 + span_length
score = per_char*span_length + whole_span_bonus
```

### Partition resolution

The resolver adds a zero-score one-code-point fallback at every position and performs backward dynamic programming. It maximizes total score across complete sentence coverage. Ties choose fewer spans, then lexicographically longer earlier spans.

### Missing core trace

Not serialized: total selected partition score, alternative full partitions, score margins, whether a tie-break was invoked, which tie-break won, and score-policy version.

## Reader selector gates

Reader-generated candidates are not selected by core utility score. Eligibility blockers include hard rejection, non-contiguous source, intervening argument material, KWJA boundary conflicts, complete grammar conflicts, stronger same-range grammar, missing complete compound identity, multiple or absent lexical identity, and failure to align to complete compatibility spans.

Eligible candidates are ordered by:

```text
family: complete grammar > compound predicate > inflected lexical > term
then longer range
then greater matched dictionary source count
```

Overlap with an already chosen Reader-generated candidate causes abstention. The selector does not serialize its computed priority tuple.

## Generator and evidence gates

Candidate creation can be suppressed by invalid range, punctuation crossing, protected boundaries, missing structural patterns, deduplication, KWJA allow lists, baseline-improvement requirements, or same-range corroboration. Several suppressions emit no event. This is the highest-priority observability gap for diagnosing candidate-generation misses.
