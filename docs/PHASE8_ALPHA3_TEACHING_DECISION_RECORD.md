# Phase 8 Alpha 3: TeachingDecisionRecord v1

Alpha 3 adds a content-addressed, correction-independent review record that references an immutable `AnalyzerDecisionSnapshot v1`.

## Supported judgments

- `accepted-current`
- `corrected`
- `rejected`

## Review coverage

Only the asserted source range is reviewed. All other sentence ranges remain `unreviewed` unless a later workflow explicitly reviews them.

## Assertions

Boundary, classification, and optional identity assertions remain separate. User-asserted identity is preserved even when analyzer identity is unavailable.

## Failure classes

`accepted-current`, `candidate-generation-miss`, `ranking-error`, `hard-gate-error`, `boundary-error`, `role-error`, `identity-error`, `partition-optimization-error`, `abstention-error`, and `unclassified`.

## Initial quality policy

All records start with `corpusMode=test`, `reviewStatus=captured`, `exportStatus=excluded`, and `operationalStatus=inactive`. Creating a record does not activate a correction or alter analyzer behavior.

## Safety

The installer runs only contract tests that do not open SQLite. It compares dictionary readiness, counts, consistency, and database hash before and after validation, and aborts on any change.
