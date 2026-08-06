# Phase 12A.2C: Benchmark-only persistent KWJA worker

This phase evaluates KWJA's documented interactive CLI mode as a long-lived worker. It compares current fresh executable calls, repeated requests in one worker, and requests across fresh workers. Production `/analyze` is unchanged and the existing executable adapter remains authoritative.

The benchmark stores only hashes, timings, process IDs, alignment status, and structural fingerprints. It does not store sentence text or raw KNP output.
