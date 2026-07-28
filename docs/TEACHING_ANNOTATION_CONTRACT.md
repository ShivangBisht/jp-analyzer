# Teaching Annotation Contract v1.0

## Scope

Phase 8.5A defines contracts and audits current data availability. It does not create the corpus database, alter correction behavior, or enable production tuning.

## Ownership

JP Analyzer owns immutable analyzer snapshots, annotation validation, correction links, linguistic roles, lookup identities, derived learning fields, corpus analysis, and future tuning evaluation. Novel Audio Miner supplies exact source ranges, explicit user intent, confidence, notes, and EPUB provenance.

## Two linked records

1. Operational correction: immediate exact-sentence/range override, revision-aware and undoable.
2. Teaching annotation: historical, partial supervision linked to the correction and immutable analyzer evidence.

Undo deactivates the operational correction and appends a retraction event; it does not delete the annotation snapshot.

## Partial supervision

A normal Save marks only the selected range `reviewed-corrected`. Every other source range is `unreviewed`. Unreviewed ranges are ignored by analysis and tuning metrics. Whole-sentence review is false unless explicitly recorded by a later workflow.

## Required snapshot layers

The research snapshot must preserve full analysis or a content-addressed immutable reference sufficient to reconstruct:

- morphology and source alignment;
- orthography and protected spans;
- lexical, name, grammar, dictionary, and KWJA evidence;
- resolver candidates, conflicts, and decisions;
- compact reader candidates and reader selection;
- raw and effective reader spans;
- analyzer/schema/correction/dictionary identities.

Compact `readerSpans`, `readerCandidates`, and `readerSelection` are sufficient for the current operational correction but are not automatically a lossless historical snapshot of every analyzer layer.

## Target semantics

- Show as one unit: boundary merge target only.
- Split: explicit internal boundaries.
- Vocabulary: one lexical span; analyzer derives lookup and learning identities.
- Grammar: one learnable-grammar span.
- Function: one function span.
- Name: one name span.
- Unresolved: neutral/unresolved span.

Derived outcome records whether lookup keys, comprehension, New Words, mining eligibility, presentation class, and colour source were successfully produced after correction.

## Multiple annotations

Non-overlapping active annotations may share a sentence snapshot. Same-range changes supersede prior annotations with history retained. Partial overlap and containment require explicit replacement or rejection; conflicting flat targets must never be silently active together.

## Dataset assignment

Assignment is deterministic and group-based. The first contract groups by selected surface plus action and uses 70% train, 15% development, and 15% test buckets. Phase 8.5B may refine grouping with role/candidate signatures while preserving stable assignment semantics.

## Read-only tuning

Future Phase 8 read-only tuning evaluates only reviewed ranges and cannot mutate analyzer rules, dictionaries, weights, correction rows, cache identity, or runtime configuration.
