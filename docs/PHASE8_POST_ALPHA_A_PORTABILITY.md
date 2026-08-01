# Phase 8 Post-Alpha A: Teaching Evidence Portability

`TeachingEvidenceTransfer.v1` moves authoritative Teaching evidence between computers without copying SQLite databases or using Git for runtime data.

Included: analyzer snapshots, immutable Teaching records, lifecycle events, quality states, quality events, reviewer metadata, supersession relationships, and package digests.

Excluded: dictionaries, operational Reader corrections, tuning artifacts, rules, activation, and deployment.

Import is always preceded by verification and a read-only preview. Same ID plus identical content is idempotent. Same ID plus different content is a blocking conflict. Apply uses one SQLite transaction and rolls back on failure.
