# Phase 10.4: One-click Windows launch and Reader-safe status layout

Phase 10.4 provides hidden Windows entry points for startup, diagnostics, and coordinated shutdown. The normal launcher uses `pythonw.exe`, so no terminal is shown. A second launch reuses the existing application and opens the Reader.

The diagnostics launcher creates a local read-only HTML report from startup status and logs. The stop launcher writes a shutdown request consumed by the supervisor, which closes only launcher-owned process trees.

When a book is open, the status control participates in layout instead of floating over Reader controls or content. The upload screen retains the compact floating presentation. No dictionary synchronization, scoring change, runtime-data mutation, permanent dictionary hash, or foreign-process termination is introduced.
