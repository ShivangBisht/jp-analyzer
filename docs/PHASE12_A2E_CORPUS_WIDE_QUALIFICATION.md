# Phase 12A.2E: Corpus-wide persistent-worker qualification

This milestone qualifies the benchmark-only persistent KWJA worker against all 15 representative sentences in forward, reverse, and fixed shuffled sequences. Every worker result is compared with a fresh-executable final analyzer baseline.

The qualification guards authoritative analyzer fields and hashes protected Teaching source files. Teaching, correction, and dictionary databases are opened read-only for row-count and digest guards. No production runtime is connected to the worker.

A pass requires zero final analyzer differences, unchanged Teaching/correction/dictionary guards, successful worker shutdown, and successful forced-kill restart recovery.
