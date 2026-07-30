# Phase 8 Alpha 1: Analyzer Observability Audit

**Audited commit:** `47cd14af8effc51b1a715e6ea5edc00b419af0f2`  
**Branch:** `feature/phase8-teaching-annotations`  
**Audit mode:** read-only; no analyzer behavior or runtime data changed.

## Snapshot requirements for Alpha 2

### Required identities

- snapshot ID and content digest;
- source sentence fingerprint and stable provenance;
- Git/analyzer/engine/layer versions;
- core score-policy and resolver-policy versions;
- Reader candidate and selection policy versions;
- dictionary snapshot identity and readiness;
- correction revision as context, while raw output remains correction-free.

### Required evidence

- lossless full analysis;
- core candidate set with local IDs and content fingerprints;
- utility dimensions, score and contribution explanation;
- core selected partition, total score, conflicts, decisions and tie-break trace;
- KWJA proposal status and dictionary evaluation;
- Reader-generated candidates, hypotheses, structural evidence, gates, priority and decisions;
- compatibility Reader spans before Reader-generated replacement;
- correction-free selected Reader spans;
- validation diagnostics and exact reconstruction status.

### Required status model

```text
generation: generated | deduplicated | filtered | not-generated
eligibility: eligible | blocked | evidence-only | not-applicable
ranking: selected | rejected | displaced | abstained
projection: compatibility | selected-generated-candidate
correction: none | active-exact-occurrence
```

### Replay levels

- Level 0, archival: lossless historical evidence.
- Level 1, score replay: recompute core candidate score from stored values.
- Level 2, partition replay: reproduce selected core partition and tie-break.
- Level 3, Reader replay: reproduce Reader-generated selection and policy.
- Level 4, full analyzer rerun: requires compatible models and dictionary snapshot.

The snapshot must state which levels are supported rather than claiming universal replayability.
