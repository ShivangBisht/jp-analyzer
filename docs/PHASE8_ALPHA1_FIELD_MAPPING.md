# Phase 8 Alpha 1: Analyzer Observability Audit

**Audited commit:** `47cd14af8effc51b1a715e6ea5edc00b419af0f2`  
**Branch:** `feature/phase8-teaching-annotations`  
**Audit mode:** read-only; no analyzer behavior or runtime data changed.

## Field mapping

### Full analysis layers

- `morphemes`: GiNZA source-aligned morphology, including lemma, normalized form, reading, POS, tag, dependency, head and conjugation. Persist losslessly.
- `orthographic_spans`: protected punctuation ranges. Used in core candidate generation and protected-boundary handling.
- `person_references`: protected person/name ranges with base name, title, morpheme IDs and evidence.
- `grammar_matches_alpha321`: stabilized grammar candidates, IDs, canonical form, function, priority, confidence and evidence.
- `numeral_expressions_alpha32`: numeral/counter units.
- `discourse_connectives_alpha321`: contextual discourse terms.
- `lexical_items_alpha32`: lexical proposals with headword, normalized headword, type, morpheme IDs, confidence and evidence.
- KWJA fields: source-aligned morphemes, bunsetsu, basic phrases, dependencies, predicates, arguments, entities, clauses, modality, discourse, metadata and alignment diagnostics.

### Core resolver candidate

```json
{
  "candidate_id": "a34c0",
  "start": 0,
  "end": 1,
  "surface": "...",
  "proposed_role": "term",
  "candidate_family": "term",
  "headword": "...",
  "grammar_id": null,
  "confidence": 0.84,
  "protected": false,
  "source_layer": "lexical",
  "source_annotation_id": "...",
  "morpheme_ids": [],
  "dictionary_evidence": {},
  "evidence": [],
  "utility_dimensions": [100, 60, 70, 57, 30, 84],
  "utility_score": 0
}
```

Serialization: preserved in full analysis as `resolver_candidates_alpha2`; compact output projects it into a camelCase existing-resolver Reader candidate and retains utility values under `features`.

### Core resolver decision

Fields: decision ID, source range/surface, selected candidate, role/headword/grammar, rejected overlapping candidate IDs, policies, utility dimensions, reason, confidence. Stored in full analysis as `resolver_decisions_alpha2`; omitted from compact output except indirectly through selected flags and compatibility spans.

### Core conflict

Fields: conflict ID, selected range, selected candidate, all candidate IDs, resolved flag, resolution policy. Stored in full analysis; omitted from compact output.

### Reader-generated candidate

Fields include content-derived candidate ID, family, source range, proposed role, possible lookup keys, typed lookup hypotheses, grammar ID, component IDs, evidence, features, hard rejections, dictionary evaluation, structural evidence, abstention reasons, selected state, preferred lookup key, ranking status and selection reason. Preserved in `readerCandidates`.

### Reader selection

Fields: policy version, mode, compatibility fallback availability, selected generated candidate IDs/count, decisions. Preserved in compact output. Decisions contain candidate ID, surface, select/abstain action, reasons and preferred lookup key when selected.

### Reader span

Fields: range/surface, display role, lexical type, colour policies, lookup keys, comprehension/New Words/mining flags, headword, grammar ID, confidence, source IDs/layer and projection status. Corrections add correction metadata after ordinary selection.
