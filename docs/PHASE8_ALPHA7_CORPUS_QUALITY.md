# Phase 8 Alpha 7 Corpus Quality

Alpha 7 adds a separate corpus-quality review layer. It never mutates immutable TeachingDecisionRecord payloads.

States: captured, needs-review, reviewed, approved, rejected-for-corpus.

Approval only marks a record eligible for a future export contract. Export remains disabled. The quality layer records reviewer metadata, quality notes, state-change events, duplicate groups, and conflicting judgments. Analyzer behavior, dictionaries, scores, gates, and Reader corrections remain unchanged.
