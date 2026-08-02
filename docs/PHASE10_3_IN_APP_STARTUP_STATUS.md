# Phase 10.3: In-application startup status and diagnostics

Novel Audio Miner now exposes the launcher's component state in the application. A compact indicator stays unobtrusive when required services are ready and opens a detailed panel for degraded or failed components.

JP Analyzer exposes `GET /startup/status`. The response sanitizes launcher state, omits child PIDs and executable paths, reports component readiness and actionable problems, and includes only the local log-directory location in technical diagnostics. Missing, corrupt, or stale supervisor status is handled conservatively.

The supervisor writes a heartbeat and periodically rechecks optional services, so starting Anki or VOICEVOX after the application opens is reflected without restarting the application. Phase 10.3 does not synchronize the dictionary, mutate runtime data, or add process-control endpoints.
