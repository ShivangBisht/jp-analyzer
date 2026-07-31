# Phase 8 Alpha 9: Offline Evaluation

Alpha 9 introduces `TeachingOfflineExperiment.v1`, a deterministic evaluation artifact over the Alpha 8 dry-run corpus. It compares frozen baseline predictions with explicitly supplied candidate predictions, reports metrics by split, blocks split leakage, verifies artifact digests, and keeps live analyzer mutation, dictionary mutation, and deployment disabled.
