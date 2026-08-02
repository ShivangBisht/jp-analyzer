# Phase 10.2: Auto-discovery and diagnostics

The launcher discovers the JP Analyzer virtual environment, sibling Novel Audio Miner repository, sibling KWJA evaluator environment, npm, environment overrides, and PATH tools. Explicit local configuration remains authoritative.

When no local configuration exists, the supervisor writes an ignored `config/startup.local.json` with resolved machine paths. Existing user configuration is never overwritten. Diagnostics record resolution sources, checked candidates, service URLs, runtime paths, logs, and suggested fixes.

Existing services are reused only when they expose the expected JP Analyzer health contract or Novel Audio Miner identity document. Occupied foreign ports are reported and never terminated. Discovery does not synchronize the dictionary, mutate runtime databases, or require a permanent dictionary file hash.
