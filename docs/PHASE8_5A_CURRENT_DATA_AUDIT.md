# Phase 8.5A Current-Data Audit

## Confirmed available in compact analysis and current Teaching Save

- canonical sentence and exact selected start/end/surface;
- analyzer version, reader-span schema, correction revision;
- baseline/effective `readerSpans`;
- compact `readerCandidates`;
- compact `readerSelection`, including applied corrections where returned;
- Teaching action, display role, split offsets, and preview target spans.

These fields are enough for operational Preview/Save/Undo and a useful Reader-level annotation.

## Not yet guaranteed as a lossless Save-time corpus snapshot

- complete morphology and orthography arrays;
- every lexical, grammar, name, dictionary, and KWJA evidence array;
- complete central resolver candidates, conflicts, and decisions;
- dictionary snapshot identity beyond current runtime status;
- post-correction derived known/frequency lookup validation and final colour-driving presentation result;
- book/chapter/scene provenance in the backend correction request;
- confidence, note, coverage mask, annotation identity, history, dataset group, and supersession links.

## Contract decision

Phase 8.5B must add a dedicated immutable analyzer snapshot capture or content-addressed snapshot reference. The frontend must not manufacture missing linguistic layers from compact output. Save should atomically link the operational correction, raw/effective snapshot, partial annotation, and initial history event.

## Audit tool

Run `scripts/audit_teaching_annotation_data.py` against a full or compact analyzer JSON export. The report classifies the payload and lists missing required compact fields and missing full layers.
