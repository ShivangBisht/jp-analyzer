# Phase 8 Alpha 8 Corpus Export

Alpha 8 defines a deterministic `TeachingCorpusExport.v1` dry-run artifact.

Eligibility requires an active Teaching decision, approved corpus-quality state, valid immutable record digest, authoritative snapshot availability, and no unresolved duplicate or conflict. Every exclusion carries explicit reasons. Eligible records are sorted by record ID and assigned reproducible train, validation, or test splits by SHA-256 bucket.

The artifact has a canonical corpus digest and verifier. `exportEnabled` and `activationEnabled` are always false. Generation downloads a JSON dry-run package only. It does not train, tune, deploy, or activate the analyzer, and does not modify dictionaries or operational corrections.
