# Phase 12A.2A: Direct KWJA Execution Decomposition

## Purpose

Measure the dominant KWJA cost without changing production analysis behavior.

## Added diagnostics

- Raw `kwja.exe` wall-clock and internally reported duration.
- Raw output byte size and exact SHA-256.
- Header-insensitive normalized KNP fingerprint.
- Existing adapter normalization and alignment duration.
- Semantic adapter fingerprint and per-layer counts.
- Per-sentence equivalence summary across repeated executions.

## Safety

The benchmark is read-only. It does not write Teaching evidence, occurrence
corrections, dictionary data, or activate an alternative KWJA execution path.
The normal JP Analyzer pipeline continues to use the existing subprocess
adapter.

## Decision boundary

A persistent worker is considered only after this benchmark establishes:

1. stable normalized KNP output;
2. stable adapter semantics;
3. the proportion of time spent in executable/model execution versus parsing;
4. exact fallback and restart requirements.
