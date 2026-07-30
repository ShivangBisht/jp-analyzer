# Phase 8 Alpha 4: Teaching Decision Store

Alpha 4 persists validated `TeachingDecisionRecord v1` payloads and their referenced `AnalyzerDecisionSnapshot v1` payloads in a dedicated SQLite database.

## Capabilities

- content-addressed snapshot and record deduplication
- snapshot foreign-key and digest verification
- create, get, list, retract, and supersede operations
- append-only lifecycle event ledger
- filters for judgment, failure classification, lifecycle, and sentence digest
- integrity report
- API routes under `/teaching-decisions`

## Safety policy

All Alpha 4 records remain `exportStatus=excluded`; export is disabled. Tests use only pytest temporary databases. The installer compares the authoritative lexicon hash and counts before and after validation.
