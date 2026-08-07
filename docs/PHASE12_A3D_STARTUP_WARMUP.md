# Phase 12A.3D Controlled Application Activation and Startup Warm-up

The one-click launcher now supplies `KWJA_EXECUTION_MODE=persistent` by default through startup configuration. The general analyzer environment default remains `fresh`, so direct and rollback operation remain conservative.

FastAPI lifespan starts a daemon warm-up thread after service startup. `/liveness` remains immediately available. Warm-up uses the same persistent runtime registry and lock as real requests, so an early Reader request waits safely rather than creating a second worker. Shutdown stops the shared worker runtime.

Warm-up uses the internal synthetic text `検証。` only to initialize KWJA. It does not pass through the full analyzer, Reader cache, corrections, dictionary writes, or Teaching stores.

`/health` exposes operational execution mode, warm-up state, worker state, generation, request count, restart count, fallback count, and last error inside the existing `kwja` object. These values are operational only and do not enter analyzer responses or semantic fingerprints.

Machine-local rollback is available by setting `kwja.executionMode` to `fresh` in ignored `config/startup.local.json`.


## Liveness-first application startup

The supervisor waits only for the lightweight `/liveness` contract before it records analyzer ownership, starts the frontend, and opens the browser. It does not block the application interface on `/health`, GiNZA initialization, dictionary inspection, or KWJA warm-up.

The existing periodic supervisor cycle then reads `/health` and updates dictionary and KWJA component readiness. A user may therefore see the interface while KWJA reports `starting`; once background warm-up completes, the existing status panel reports that persistent KWJA is ready.

An analysis request that arrives during warm-up safely shares the persistent runtime lock. It does not create a second worker.
