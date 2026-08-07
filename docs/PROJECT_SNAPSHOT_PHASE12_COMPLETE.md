# Project Snapshot: Phase 12 Complete

**Snapshot date:** 7 August 2026, IST  
**Purpose:** Durable AI development handoff for the complete Japanese Novel Miner system  
**Authoritative continuation point:** After Phase 12A and Phase 12B completion  
**Scope:** JP Analyzer, Novel Audio Miner, one-application startup, Teaching/corpus governance, dictionary integration, Reader analysis, persistent KWJA runtime, bounded prefetch, testing, paths, and operating procedures

> **Instruction to any future AI:** Read this entire file before proposing or applying changes. Treat the current `main` branches and completion tags listed here as authoritative. Older snapshots and historical README sections may describe superseded Kuromoji-era or pre-Phase-12 behavior. Do not restart completed phases. Continue from the Phase 12-complete baseline only after verifying the live repositories.

---

## 1. Executive Summary

The system is a local Windows application for reading Japanese EPUB novels, visualizing vocabulary knowledge, reviewing analyzer output, collecting governed Teaching evidence, and mining selected vocabulary to Anki.

It is split into two repositories:

1. **JP Analyzer** is the sole linguistic authority. It owns Japanese morphology, structural evidence, candidate generation, dictionary and KWJA evidence, conservative selection, exact Reader spans, correction-aware identities, Teaching evidence contracts, and backend APIs.
2. **Novel Audio Miner** owns EPUB parsing, the React Reader, display and colorization, navigation, known-word and frequency lookup, Teaching UI, dictionary UI, debug reports, Anki mining, Nadeshiko enrichment, and VOICEVOX fallback.

Phase 12 is complete:

- **Phase 12A** optimized the backend with a persistent serialized KWJA worker, bounded recovery, production-route parity, corpus-wide equivalence qualification, startup warm-up, and runtime health metrics.
- **Phase 12B** optimized Reader-side analysis with a next-ten rolling prefetch window, priority-aware single-worker scheduling, foreground promotion, duplicate coalescing, stale-plan removal, a bounded 50-entry memory-only session cache, and sanitized operational observability.

The application remains conservative and contract-driven. JP Analyzer is authoritative. The frontend must not invent linguistic boundaries or identities. Teaching evidence does not automatically tune or mutate the analyzer. Phase 9 tuning remains deferred until corpus-governance maturity requirements are met.

---

## 2. Authoritative Repository Baseline

### 2.1 Novel Audio Miner

```text
Repository path: D:\Mining\novel-audio-miner
Remote:          https://github.com/ShivangBisht/novel-audio-miner.git
Branch:          main
HEAD:            9eb621cb27a2393265aaff468e8d258c5bf96e92
Tag on HEAD:     phase12b-complete
Merge subject:   Merge Phase 12B Reader prefetch optimization
Status:          synchronized with origin/main and clean at snapshot collection
```

Phase 12B milestone commits:

```text
882c86a  Add Phase 12B.1 rolling Reader prefetch planning
858b9a3  Add Phase 12B.2 priority-aware analyzer scheduling
543cc14  Qualify Phase 12B.3 Reader rolling-window integration
152c301  Add Phase 12B.4 bounded Reader session cache
0f6c989  Add Phase 12B.5 sanitized analyzer observability
0447f57  Complete Phase 12B end-to-end qualification
9eb621c  Merge Phase 12B Reader prefetch optimization
```

### 2.2 JP Analyzer

```text
Repository path: D:\Mining\JP analyzer
Remote:          https://github.com/ShivangBisht/jp-analyzer.git
Branch:          main
HEAD:            90f7bec2757c89a38389f593fce6421724557f1a
Tag on HEAD:     phase12a-complete
Merge subject:   Merge Phase 12A analyzer performance optimization
Status:          synchronized with origin/main and clean at snapshot collection
```

Phase 12A milestone commits:

```text
087eec6  Add Phase 12A.1 stable analyzer performance instrumentation
4b29130  Add Phase 12A.2A KWJA execution decomposition
7d5dcf8  Add Phase 12A.2B KWJA variation diagnostics
18d72c3  Add Phase 12A.2C persistent KWJA worker benchmark
5fc184b  Add Phase 12A.2D final analyzer equivalence benchmark
89afd82  Add Phase 12A.2E corpus-wide KWJA worker qualification
f8ae8c0  Add Phase 12A.3A persistent KWJA runtime foundation
0689456  Add Phase 12A.3B bounded KWJA recovery and fallback
4cdf86b  Complete Phase 12A.3C production-route parity
ae3937f  Complete Phase 12A.3D startup warm-up and activation
90f7bec  Merge Phase 12A analyzer performance optimization
```

### 2.3 Previous completion tags

```text
Novel Audio Miner: phase8-complete, phase10-complete, phase12b-complete
JP Analyzer:       phase8-complete, phase10-complete, phase12a-complete
```

---

## 3. Machine, Runtime, and Important Paths

Snapshot collection environment:

```text
Computer:       MICORPLAP106
Operating OS:   Windows 11 build line reported as Windows-10-10.0.22631-SP0
Architecture:   AMD64
Processors:     8
PowerShell:     5.1.22621.6133
Git:            2.55.0.windows.2
Node:           v24.18.0
npm:            12.0.1
Python:         3.11.8, 64-bit
UTF-8 env:      PYTHONUTF8=1, PYTHONIOENCODING=utf-8
```

### 3.1 Main directory map

```text
D:\Mining\
├── _PROJECT_WORK\               Temporary collectors, guarded installers, source bundles
├── _RECOVERY\                   Recovery material
├── JP analyzer\                 Backend repository and its Python environment
├── KWJA evaluator\              Local KWJA installation/evaluator location
└── novel-audio-miner\           Frontend repository
```

### 3.2 Python environment

The working Python interpreter is:

```text
D:\Mining\JP analyzer\.venv\Scripts\python.exe
```

The following paths did not exist when this snapshot was collected:

```text
D:\Mining\novel-audio-miner\.venv\Scripts\python.exe
D:\Mining\python\python.exe
D:\Mining\Python\python.exe
```

Use the JP Analyzer virtual environment for supported Python utilities unless a task explicitly requires another interpreter:

```powershell
$Python = "D:\Mining\JP analyzer\.venv\Scripts\python.exe"
& $Python --version
```

JP Analyzer also supports a separate KWJA-focused environment or executable configured through setup and startup configuration. Do not assume its path. Discover it from configuration and `KWJA_EXE`, or use the supported setup script.

### 3.3 Ports and service URLs

```text
Frontend Vite UI:          http://127.0.0.1:5173
JP Analyzer:               http://127.0.0.1:8766
JP Analyzer liveness:      http://127.0.0.1:8766/liveness
JP Analyzer health:        http://127.0.0.1:8766/health
JP Analyzer analysis:      POST http://127.0.0.1:8766/analyze
AnkiConnect:               http://127.0.0.1:8765
VOICEVOX:                  optional local service, startup-discovered/configured
Legacy dictionary sync:    http://127.0.0.1:8771 in Phase 8 sync client
```

For normal frontend calls, prefer the configured Vite proxy where the source already uses it. Do not hard-code a backend URL into code that intentionally routes through the proxy.

---

## 4. One-Application Startup and Shutdown

Phase 10 delivered a one-click Windows application experience. Normal users should not start frontend and backend manually.

The launchers live in the **JP Analyzer repository root**:

```text
D:\Mining\JP analyzer\Japanese Novel Miner.vbs
D:\Mining\JP analyzer\Japanese Novel Miner - Diagnostics.vbs
D:\Mining\JP analyzer\Japanese Novel Miner - Stop.vbs
```

Supporting launcher programs:

```text
D:\Mining\JP analyzer\launch_japanese_novel_miner.pyw
D:\Mining\JP analyzer\open_japanese_novel_miner_diagnostics.pyw
D:\Mining\JP analyzer\stop_japanese_novel_miner.pyw
```

### 4.1 Normal operation

- `Japanese Novel Miner.vbs` performs hidden startup.
- It starts/supervises JP Analyzer and Novel Audio Miner, opens the browser, tracks ownership, and avoids killing foreign or incompatible services.
- Duplicate launches reuse the running application.
- Optional VOICEVOX and AnkiConnect failures are nonblocking for reading and linguistic analysis.
- The frontend displays startup/component state through `ApplicationStatusIndicator.jsx` and `ApplicationStatusPanel.jsx`.
- The Reader layout reserves space for status UI so it does not overlap navigation or vertical reading content.

### 4.2 Diagnostics and shutdown

- `Japanese Novel Miner - Diagnostics.vbs` opens read-only startup diagnostics.
- `Japanese Novel Miner - Stop.vbs` performs coordinated safe shutdown.
- Launcher-owned listeners and processes are verified before termination.
- Safe orphan cleanup exists if the supervisor exits unexpectedly.

### 4.3 Startup implementation paths

```text
D:\Mining\JP analyzer\app\startup\config.py
D:\Mining\JP analyzer\app\startup\discovery.py
D:\Mining\JP analyzer\app\startup\health.py
D:\Mining\JP analyzer\app\startup\instance_lock.py
D:\Mining\JP analyzer\app\startup\models.py
D:\Mining\JP analyzer\app\startup\ownership.py
D:\Mining\JP analyzer\app\startup\process_manager.py
D:\Mining\JP analyzer\app\startup\status_api.py
D:\Mining\JP analyzer\app\startup\supervisor.py
D:\Mining\JP analyzer\app\startup\windows.py
D:\Mining\JP analyzer\config\startup.example.json
D:\Mining\JP analyzer\config\startup.local.json    # ignored machine-local override, may not exist
```

Do not commit `startup.local.json`. It is explicitly ignored and may contain machine-specific absolute paths.

---

## 5. System Architecture and Ownership Boundaries

### 5.1 Non-negotiable ownership contract

**JP Analyzer owns:**

- Japanese linguistic boundaries
- Exact source offsets
- Morphology and structure
- Candidate generation
- Dictionary and KWJA evidence
- Evidence gates and conservative abstention
- Reader-facing roles and lookup identities
- Comprehension and mining eligibility flags
- Final Reader spans
- Correction-aware analyzer identity metadata
- Analyzer diagnostics and compact/full contracts

**Novel Audio Miner owns:**

- EPUB loading and parsing
- Scene/image ordering and navigation
- React UI and rendering
- Applying classes to authoritative Reader spans
- Known-word lookup and manual-known storage
- Frequency lookup and color mapping
- Comprehension aggregation from analyzer flags
- New Words presentation
- Selection UI and Anki mining orchestration
- Nadeshiko/VOICEVOX enrichment
- Teaching and corpus administration UI
- Startup status UI and debug-report export

### 5.2 Forbidden frontend behavior

Novel Audio Miner must not:

- Merge or split analyzer spans
- Infer grammar, names, compounds, or lookup identities
- Re-tokenize Japanese for linguistic ownership
- Use surface search when authoritative exact offsets are available
- Treat dictionary misses as proof that a candidate is invalid
- Change analyzer semantic output through prefetch, caching, or observability

If analyzer output is invalid, the Reader should remain neutral rather than inventing a fallback linguistic structure.

### 5.3 Reader contract

`readerSpans` is authoritative. Valid output is contiguous, non-overlapping, offset-correct, and reconstructs the original sentence. Important frontend adapter:

```text
D:\Mining\novel-audio-miner\src\lib\analyzerReaderSpanAdapter.js
```

Important backend projection and candidate files:

```text
D:\Mining\JP analyzer\app\analyzer\reader_projection.py
D:\Mining\JP analyzer\app\analyzer\reader_candidates.py
D:\Mining\JP analyzer\app\analyzer\reader_candidate_generation.py
D:\Mining\JP analyzer\app\analyzer\reader_candidate_dictionary.py
D:\Mining\JP analyzer\app\analyzer\reader_candidate_evidence.py
D:\Mining\JP analyzer\app\analyzer\reader_candidate_selection.py
```

---

## 6. Novel Audio Miner Architecture

### 6.1 Application shell

```text
src/main.jsx                 React mounting
src/App.jsx                  Book/load/error state and upload-vs-Reader screen
src/styles.css               Application and Reader styles
src/components/FileLoader.jsx EPUB selection
```

### 6.2 Reader

Main path:

```text
D:\Mining\novel-audio-miner\src\components\Reader.jsx
```

Reader responsibilities include:

- Converting flat EPUB items into sentence and illustration scenes
- Scene, chapter, and direct numeric navigation
- Vertical/horizontal display
- Furigana on/off
- Font, spacing, and Reader height controls
- Authoritative analyzer-span rendering
- Known/unknown/frequency color mapping
- Comprehension and New Words presentation
- Selection restricted to analyzer spans
- Manual Mark Known and Undo Known
- Teaching Mode integration
- Mining to the latest Kiku note
- Debug Report v2 export
- Phase 12 rolling prefetch integration
- Cache/session cleanup on Reader unmount or book change

### 6.3 EPUB and rendering pipeline

```text
src/lib/epubParser.js
src/lib/japaneseSentenceSplitter.js
src/lib/colorSource.js
src/lib/analyzerPresentationPolicy.js
src/lib/analyzerReaderSpanAdapter.js
```

`epubParser.js` owns extraction, spine/TOC traversal, image extraction, sentence extraction, and the flat Reader stream. `japaneseSentenceSplitter.js` only splits sentences. Broad reading-unit grouping remains outside the active flow.

### 6.4 Known words and frequency

```text
src/lib/wordCache.js
src/lib/frequencyMap.js
src/lib/storage.js
public/dict/jpdb.json
public/dict/jiten.json
public/dict/cc100.json
public/dict/bccwj.json
public/dict/user_dictionary_seed.json
```

Rules:

- A word is known if present in the Anki-derived cache or manual-known storage.
- Clearing/rebuilding the Anki cache does not delete manual-known words.
- Undo Known removes only manual-known state. A word still known through Anki remains known.
- Reader progress/settings are owned separately by `storage.js`.
- Large dictionary JSON files are local and ignored by Git except the small seed/config file.

### 6.5 Mining and enrichment

```text
src/lib/ankiConnect.js
src/lib/enrichService.js
```

Mining updates the latest configured Kiku note through AnkiConnect. Nadeshiko provides enrichment when available. VOICEVOX provides fallback audio or forced TTS. These optional integrations must not change analyzer authority.

### 6.6 Teaching and administration UI

Key components:

```text
src/components/TeachingPanel.jsx
src/components/TeachingDecisionPanel.jsx
src/components/TeachingAdvancedDashboard.jsx
src/components/TeachingCorpusQualityPanel.jsx
src/components/TeachingCorpusExportPanel.jsx
src/components/TeachingCorpusGovernancePanel.jsx
src/components/TeachingOfflineEvaluationPanel.jsx
src/components/TeachingPortabilityPanel.jsx
src/components/TeachingTuningCorpusPanel.jsx
src/components/TeachingTuningHandoffPanel.jsx
src/components/TeachingControlledActivationPanel.jsx
src/components/DictionaryManagementPanel.jsx
```

Teaching clients are under `src/lib/teaching*Client.js`. Teaching captures immutable analyzer observations, supports accepted-current and corrected judgments, diagnosis, supersession, retraction, quality review, export, portability, packaging, governance, offline evaluation, and handoff contracts. Saving Teaching evidence does not automatically tune or activate the analyzer.

---

## 7. JP Analyzer Architecture

### 7.1 Entrypoints and service

```text
D:\Mining\JP analyzer\app\analyzer\__init__.py
D:\Mining\JP analyzer\app\analyzer\service.py
D:\Mining\JP analyzer\app\analyzer\services.py
D:\Mining\JP analyzer\app\analyzer\runtime.py
D:\Mining\JP analyzer\app\analyzer\health.py
D:\Mining\JP analyzer\app\analyzer\pipeline.py
D:\Mining\JP analyzer\app\analyzer\engine.py
```

The FastAPI service exposes liveness, health, analysis, corrections, Teaching, corpus/governance, and startup APIs. `liveness` is intentionally lightweight and must not initialize expensive NLP/database state.

### 7.2 Linguistic layers

Located under:

```text
D:\Mining\JP analyzer\app\analyzer\layers\
```

Major responsibilities:

```text
morphology.py             Morphological evidence
structure.py              Structural evidence
candidates.py             Core candidate generation
dictionary.py             Dictionary evidence integration
dictionary_items.py       Dictionary item normalization
dictionary_store.py       SQLite-backed dictionary storage
dictionary_registry.py    Installed dictionary metadata
dictionary_api.py         Dictionary endpoints
dictionary_update_proxy.py Controlled updates
evidence_gate.py          Conservative evidence gates
decision.py               Resolver and selection
kwja.py                   KWJA execution/normalization
protected.py              Protected ranges/invariants
invariants.py             Structural validation
stabilization.py          Stable output behavior
schema.py                 Layer contracts
```

Dictionary data is evidence, not final authority. A miss does not itself reject a candidate. Ambiguity should produce neutral or unresolved behavior rather than unsupported inference.

### 7.3 Corrections

```text
app/analyzer/reader_corrections.py
app/analyzer/reader_corrections_api.py
```

Operational Reader corrections are exact-occurrence records and remain separate from immutable Teaching evidence. The correction revision is part of analyzer cache identity. After correction mutation, the frontend clears Reader analysis state and refreshes.

### 7.4 Teaching backend

Representative modules:

```text
app/analyzer/analyzer_decision_snapshot.py
app/analyzer/teaching_decision_record.py
app/analyzer/teaching_decision_store.py
app/analyzer/teaching_decision_api.py
app/analyzer/teaching_guided_review.py
app/analyzer/teaching_review_management.py
app/analyzer/teaching_quality_store.py
app/analyzer/teaching_corpus_export.py
app/analyzer/teaching_portability.py
app/analyzer/teaching_tuning_corpus.py
app/analyzer/teaching_corpus_governance.py
app/analyzer/teaching_offline_evaluation.py
app/analyzer/teaching_tuning_handoff.py
app/analyzer/teaching_controlled_activation.py
```

Runtime databases are ignored by Git and may exist under `D:\Mining\JP analyzer\data\`. Never copy, replace, or run destructive tests against the authoritative databases without explicit isolation and before/after hash checks.

---

## 8. Phase 12A: Backend Performance Optimization

### 8.1 Goal

Reduce repeated KWJA startup cost without changing semantic output, Reader spans, cache identity, corrections, dictionaries, Teaching, or deployment safety.

### 8.2 Delivered stages

1. **A.1 instrumentation:** stable timing and semantic fingerprints.
2. **A.2A decomposition:** separated KWJA execution, normalization, and downstream analysis costs.
3. **A.2B variation:** measured raw KNP variation and normalized stability.
4. **A.2C worker benchmark:** proved a persistent interactive worker could be reused.
5. **A.2D equivalence:** fresh-process and persistent-worker outputs compared semantically.
6. **A.2E corpus qualification:** broader development/parity corpora guarded equivalence.
7. **A.3A runtime foundation:** one serialized persistent worker per executable/model.
8. **A.3B recovery/fallback:** one clean-worker retry, then unchanged fresh-process fallback.
9. **A.3C route parity:** production `/analyze` exercised the same qualified route.
10. **A.3D startup warm-up:** background warm-up after liveness, default persistent mode through application startup, clean shutdown.

### 8.3 Persistent runtime

Key paths:

```text
app/analyzer/kwja_persistent_worker.py
app/analyzer/kwja_persistent_runtime.py
app/analyzer/kwja_runtime.py
app/analyzer/kwja_warmup.py
app/analyzer/adapters/kwja_adapter.py
```

Runtime invariants:

- One serialized worker is owned by each runtime instance.
- The runtime uses a re-entrant lock.
- A failed worker is invalidated and never reused uncertainly.
- One clean persistent retry is allowed.
- A second failure may use the established fresh-process fallback.
- Counters expose generation, request count, restart count, fallback count, execution mode, and last error.
- Startup warm-up and early Reader requests share the same lock and cannot spawn duplicate workers.
- Shutdown stops shared runtimes.

Expected healthy application runtime:

```text
executionMode:       persistent
runtime.running:     true
runtime.generation:  1
runtime.restartCount: 0
runtime.fallbackCount: 0
runtime.lastError:   null/empty
```

### 8.4 Benchmark and qualification scripts

```text
scripts/benchmark-phase12-a1.py
scripts/benchmark-phase12-a2a-kwja.py
scripts/benchmark-phase12-a2b-variation.py
scripts/benchmark-phase12-a2c-persistent-worker.py
scripts/benchmark-phase12-a2d-final-equivalence.py
scripts/benchmark-phase12-a2e-corpus-qualification.py
scripts/benchmark-phase12-a3c-production-parity.py
```

Test corpora:

```text
tests/corpora/development/random_sentences.txt
tests/corpora/parity/consolidation_fresh_unseen_200.txt
tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json
```

Do not use these qualified parity corpora as future tuning or training data. They are guards, not a training corpus.

---

## 9. Phase 12B: Reader Prefetch Optimization

### 9.1 Final behavior

```text
Forward rolling window:          10 valid text scenes
Near-forward group:              first 5
Immediate previous protection:   enabled
Images/blank scenes:             skipped
Duplicate sentence text:         deduplicated in plan
Maximum analyzer concurrency:    1
Visible request priority:        0
Queued visible promotion:        enabled
Duplicate request coalescing:    enabled
Stale speculative removal:       enabled
Active request cancellation:     disabled by design
Session cache limit:             50
Persistent sentence cache:       disabled
Cross-session sentence reuse:    disabled
Sanitized observability:         enabled
Whole-book prefetch:             disabled
```

### 9.2 B.1 rolling planner

Path:

```text
src/lib/scenePrefetch.js
```

Order for current scene `N`:

```text
N+1, N+2, N+3, N+4, N+5,
immediate previous text scene,
N+6, N+7, N+8, N+9, N+10
```

Constants:

```text
DEFAULT_FORWARD_LIMIT = 10
HIGH_PRIORITY_FORWARD_COUNT = 5
```

### 9.3 B.2 priority scheduler

Path:

```text
src/lib/analyzerPriorityScheduler.js
```

Rules:

- Only one worker request is active.
- Active work is not preempted.
- A visible priority-zero request runs immediately after active work.
- Duplicate identities share one promise.
- A queued prefetch request becoming visible is promoted rather than duplicated.
- New navigation replaces stale queued speculative work outside the new plan.
- Session clear rejects queued work but permits active work to finish.
- A session generation guard prevents an old active result from repopulating a cleared/new session cache.

### 9.4 B.3 Reader integration

Paths:

```text
src/components/Reader.jsx
src/lib/useJpAnalyzerShadow.js
scripts/test-reader-prefetch-integration.mjs
```

Qualified navigation includes initial load, one-step forward replenishment, one-step backward reuse, distant jumps, chapter jumps, active-request retention, foreground promotion, duplicate coalescing, and queue cleanup.

### 9.5 B.4 bounded memory-only cache

Path:

```text
src/lib/analyzerSessionCache.js
```

Protected entries include:

- Current visible sentence
- Immediate previous text sentence
- Next ten planned sentences
- Active request
- Queued foreground request

Eviction is least-recently-used among unprotected entries. Maximum size is 50. Legacy keys beginning with `jp-analyzer-reader-cache-v3:` are purged. No new sentence analysis is written to localStorage.

Separate data remains unaffected:

- Anki known-word cache
- Manual-known words
- Frequency data
- Reader progress and settings
- Corrections
- Teaching data
- Dictionary data
- Mining state

### 9.6 B.5 sanitized observability

Path:

```text
src/lib/analyzerObservability.js
```

Operational fields include scheduler counts, active kind/priority, queue composition, promotions, coalescing, stale removal, cache size/limit/protection/evictions, visible source/timing/cache reason, and prefetch progress.

The `analyzerObservability` section excludes sentence text, hashes, identities, cache keys, analyzer results, Reader-span surfaces, raw KNP, and EPUB content. The broader manual Debug Report v2 still intentionally contains detailed troubleshooting content and novel text, so only the observability subsection is privacy-safe for operational sharing.

### 9.7 B.6 qualification

Commands:

```powershell
Set-Location "D:\Mining\novel-audio-miner"
npm.cmd run test:phase12b
npm.cmd run validate:phase12b
```

Documentation:

```text
docs/PHASE12_B1_ROLLING_PREFETCH.md
docs/PHASE12_B2_PRIORITY_SCHEDULER.md
docs/PHASE12_B3_READER_INTEGRATION.md
docs/PHASE12_B4_BOUNDED_SESSION_CACHE.md
docs/PHASE12_B5_SANITIZED_OBSERVABILITY.md
docs/PHASE12_B6_END_TO_END_QUALIFICATION.md
docs/PHASE12_B_COMPLETE.md
```

---

## 10. Earlier Phase History That Still Matters

### 10.1 Stable core and early Reader work

The stable v4.1 core established EPUB reading, sentence and image scenes, vertical/horizontal display, furigana rendering, known-word handling, frequency coloring, manual-known persistence/undo, Anki mining, Nadeshiko, and VOICEVOX fallback.

Some root documents such as `FINAL_STABLE_STATUS.md`, `PROJECT_STRUCTURE.md`, `README.md`, `STABILIZATION.md`, and `WORD_MODEL_POLICY.md` contain historical Kuromoji-era descriptions. Kuromoji/tokenizer ownership was later retired in Phase 5.2E. These documents remain valuable history but are not authoritative when they conflict with `docs/ANALYZER_INTEGRATION_CONTRACT.md`, current source, Phase 5 tests, or this snapshot.

### 10.2 Phase 7

Dictionary management and controlled online-update infrastructure were delivered. Dictionary data remains evidence. Dictionary stores and registries must be protected from test pollution.

### 10.3 Phase 8

Phase 8 established a governed Teaching system:

- Immutable correction-free analyzer snapshots
- Teaching decision records
- Persistent lifecycle and integrity checks
- Guided diagnosis and review
- Supersession and retraction
- Corpus quality states
- Deterministic export
- Read-only offline evaluation
- Controlled-activation plans without live activation
- Evidence portability
- Private and redacted corpus packaging
- Corpus governance/readiness
- Tuning-input and handoff contracts
- Repository hygiene and closeout

Phase 8 closed successfully, but the corpus was not train-fit. That did not block Phase 8 because the purpose was safe evidence and governance infrastructure, not training.

### 10.4 Phase 9

Phase 9 is deliberately deferred until the governed Teaching corpus is mature. Do not start training, candidate derivation, activation, or deployment simply because the handoff contracts exist.

### 10.5 Phase 10

Phase 10 delivered the startup supervisor, machine-local auto-discovery, diagnostics, in-app status, one-click launch, ownership-safe shutdown, and lifecycle hardening.

### 10.6 Phase 11

Kuromoji/legacy tokenizer ownership was retired early. JP Analyzer is the sole linguistic authority. Any old document saying the frontend must load Kuromoji is historical and superseded.

---

## 11. Contracts and Data Safety

### 11.1 Important contract documentation

JP Analyzer:

```text
docs/READER_PROJECTION_CONTRACT.md
docs/TEACHING_ANNOTATION_CONTRACT.md
docs/contracts/analyzer_decision_snapshot_v1.schema.json
docs/contracts/analyzer_candidate_artifact_v1.schema.json
docs/contracts/analyzer_candidate_evaluation_v1.schema.json
docs/contracts/teaching_controlled_activation_v1.schema.json
docs/contracts/teaching_corpus_export_v1.schema.json
docs/contracts/teaching_corpus_governance_v1.schema.json
docs/contracts/teaching_evidence_transfer_v1.schema.json
docs/contracts/teaching_offline_experiment_v1.schema.json
docs/contracts/teaching_tuning_corpus_v1.schema.json
docs/contracts/teaching_tuning_handoff_v1.schema.json
docs/contracts/teaching_tuning_input_v1.schema.json
```

Frontend:

```text
docs/ANALYZER_INTEGRATION_CONTRACT.md
```

### 11.2 Runtime databases

Typical local paths:

```text
D:\Mining\JP analyzer\data\phase8_analysis_lexicon.sqlite3
D:\Mining\JP analyzer\data\reader_corrections.sqlite3
D:\Mining\JP analyzer\data\teaching_annotations.sqlite3
D:\Mining\JP analyzer\data\teaching_decisions.sqlite3
```

These files are local, ignored, and potentially large. Do not commit them. Do not use them as disposable test fixtures.

A past Phase 8 closeout exposed dictionary-test contamination. The database was restored and the lifecycle tests were isolated. Therefore:

1. Use temporary databases for destructive tests.
2. Record before-and-after hashes for authoritative stores during closeout.
3. Preserve contaminated databases for forensics rather than overwriting them.
4. Do not assume older recorded hashes remain current after controlled updates.

Historical deferred item: six dictionary updates after a recovered baseline may need controlled reapplication. Verify current dictionary registry and update history before acting.

### 11.3 Teaching safety

Teaching evidence, operational occurrence corrections, dictionaries, tuning artifacts, and activation state are separate concerns. Saving evidence may optionally coordinate an occurrence correction, but it must not silently tune global analyzer behavior.

---

## 12. Setup and Installation

### 12.1 Novel Audio Miner dependencies

From `D:\Mining\novel-audio-miner`:

```powershell
npm.cmd install
npm.cmd run dev
```

Current exact top-level versions:

```text
@vitejs/plugin-react 6.0.3
jszip               3.10.1
react                19.2.7
react-dom            19.2.7
vite                 8.1.3
```

A production build:

```powershell
npm.cmd run build
```

### 12.2 JP Analyzer Python dependencies

Root files:

```text
requirements.txt
requirements-dev.txt
requirements-frozen-py311.txt
requirements-kwja-py311.txt
```

Use Python 3.11. Prefer the existing environment:

```powershell
$Python = "D:\Mining\JP analyzer\.venv\Scripts\python.exe"
& $Python -m pip --version
```

Do not casually upgrade dependency versions. Use frozen requirements and qualified setup procedures.

### 12.3 KWJA setup

Documentation and setup script:

```text
D:\Mining\JP analyzer\docs\KWJA_SETUP_WINDOWS.md
D:\Mining\JP analyzer\scripts\setup_kwja_windows.ps1
```

Typical invocation:

```powershell
Set-Location "D:\Mining\JP analyzer"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ".\scripts\setup_kwja_windows.ps1"
```

Resolve the final executable from local configuration or `KWJA_EXE`; do not embed a guessed path in source.

---

## 13. Supported Test and Build Commands

### 13.1 Novel Audio Miner

From `D:\Mining\novel-audio-miner`:

```powershell
npm.cmd run test:phase3
npm.cmd run test:phase4
npm.cmd run test:phase5
npm.cmd run test:phase12b
npm.cmd run validate:phase12b
npm.cmd run build
```

Phase 12B checks include:

```text
scripts/test-scene-prefetch.mjs
scripts/test-analyzer-priority-scheduler.mjs
scripts/test-reader-prefetch-integration.mjs
scripts/test-analyzer-session-cache.mjs
scripts/test-analyzer-observability.mjs
scripts/test-debug-report-v2.mjs
scripts/validate-phase12b-closeout.mjs
```

### 13.2 JP Analyzer

From `D:\Mining\JP analyzer`:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ".\run_tests.ps1"
```

Snapshot regression:

```powershell
$Python = "D:\Mining\JP analyzer\.venv\Scripts\python.exe"
& $Python ".\run_snapshot_regression.py"
```

Use targeted phase tests when developing, but run the supported full suite before merge/tag closeout.

### 13.3 Runtime health

```powershell
$HealthUrl = "http://127.0.0.1:8766/health"
$Health = Invoke-RestMethod $HealthUrl

[PSCustomObject]@{
    ExecutionMode    = $Health.kwja.executionMode
    WorkerRunning    = $Health.kwja.runtime.running
    WorkerGeneration = $Health.kwja.runtime.generation
    RequestCount     = $Health.kwja.runtime.requestCount
    RestartCount     = $Health.kwja.runtime.restartCount
    FallbackCount    = $Health.kwja.runtime.fallbackCount
    LastError        = $Health.kwja.runtime.lastError
}
```

### 13.4 Shutdown verification

After using the Stop launcher:

```powershell
Start-Sleep -Seconds 8

$Listeners = @(
    Get-NetTCPConnection `
      -LocalPort 8766,5173 `
      -State Listen `
      -ErrorAction SilentlyContinue
)

$RemainingKwja = @(
    Get-CimInstance Win32_Process |
    Where-Object {
        $_.CommandLine -and
        $_.CommandLine -like "*D:\Mining\KWJA evaluator*" -and
        $_.CommandLine -like "*kwja*"
    }
)

Write-Host "Application listener count: $($Listeners.Count)"
Write-Host "JP Analyzer KWJA chain count: $($RemainingKwja.Count)"
```

Expected counts are zero.

---

## 14. Debugging and Observability

### 14.1 Backend health

`/health` exposes analyzer version, schema/correction identity, dictionary readiness, KWJA mode, warm-up, and persistent runtime diagnostics. `/liveness` is only a lightweight service-alive signal.

### 14.2 Debug Report v2

Frontend paths:

```text
src/lib/debugReportV2.js
src/components/Reader.jsx
```

Debug Report v2 contains current scene, adjacent scenes, analyzer result, Reader spans, presentation, learning, selection, mining, EPUB parser information, prefetch information, and the sanitized observability subsection.

**Privacy rule:** the whole debug report is not sanitized. It may contain novel text, spans, identifiers, and parser inventory. Only `analyzerObservability` is explicitly sanitized.

### 14.3 Operational interpretation

Useful observability fields:

```text
scheduler.activeCount
scheduler.activeKind
scheduler.activePriority
scheduler.queuedCount
scheduler.queuedForegroundCount
scheduler.queuedPrefetchCount
scheduler.startedCount
scheduler.completedCount
scheduler.failedCount
scheduler.promotedCount
scheduler.coalescedCount
scheduler.staleRemovedCount
sessionCache.size
sessionCache.limit
sessionCache.protectedCount
sessionCache.evictionCount
visibleAnalysis.source
visibleAnalysis.elapsedMs
visibleAnalysis.cacheReason
prefetch.targetCount
prefetch.completedCount
prefetch.failedCount
prefetch.forwardTargetCount
prefetch.hasPreviousProtection
```

---

## 15. Git and Change-Management Workflow

Use one phase or bounded milestone per branch. Start only from a clean, synchronized baseline.

```powershell
Set-Location "D:\Mining\novel-audio-miner"   # or JP Analyzer

git status --short
git branch --show-current
git rev-parse HEAD
git pull --ff-only origin main
git switch -c feature/<bounded-name>
```

### 15.1 Guarded-installer workflow

Past development used collectors and guarded Python installers under:

```text
D:\Mining\_PROJECT_WORK
```

A good guarded installer must:

- Check the expected branch
- Check the expected HEAD
- Require a clean working tree
- Verify SHA-256 hashes or unique source anchors
- Refuse ambiguous replacements
- Refuse to overwrite existing output unexpectedly
- Write UTF-8 deterministically
- Print exactly what changed

If an installer stops on a mismatch, do not bypass the guard. Recollect exact source and update the installer.

### 15.2 Validation before commit

```powershell
git diff --check
git diff --stat
git status --short
```

Then run the relevant tests and build. Stage only intended files:

```powershell
git add -- <explicit paths>
git diff --cached --check
git diff --cached --stat
git status --short
```

After commit and push:

```powershell
git status
git rev-parse HEAD
```

The worktree must be clean.

### 15.3 Line endings

Novel Audio Miner `.gitattributes` requires LF for source/JSON/Markdown and CRLF for PowerShell/CMD/BAT. Git warnings that LF will be converted to CRLF in the working copy may be informational, but `git diff --check` must remain clean.

---

## 16. Known Deferred Work and Roadmap Boundaries

### 16.1 Phase 9 remains deferred

Do not activate global tuning until governance says the corpus is train-fit and validation/protected-test requirements are satisfied. Current contracts permit safe preparation and verification, not authorization to tune or deploy.

### 16.2 Teaching corpus maturation

Continue collecting authentic reviewed evidence. Improve balance and independent provenance. Preserve leakage controls. Reassess governance before any candidate derivation or activation.

### 16.3 Dictionary follow-up

Verify whether six updates lost during Phase 8 recovery still require controlled reapplication. Do not infer this from old hashes alone.

### 16.4 Historical stable-core deferments

Old documents mention compound merging, composite-known logic, token selection, sentence grouping, parser diagnostics, and Debug Mode as deferred. Several diagnostics and analyzer-span selection capabilities now exist. Therefore, re-evaluate each item against current source before treating it as still pending. Never reintroduce Kuromoji ownership.

### 16.5 After Phase 12

The next phase has not been formally defined in this snapshot. Begin with observation and a written bounded scope. Candidate directions include:

- Reading-driven reliability/latency measurement using sanitized observability
- Corpus-governance maturity work without tuning
- Controlled dictionary-recovery/update audit
- Further startup resilience only if measured problems exist
- Reader UX improvements that preserve analyzer authority

Do not call new work “Phase 12” unless it is a small corrective follow-up. Phase 12A and 12B are closed and tagged.

---

## 17. Conflict Resolution Between Documents

When sources disagree, use this order:

1. Current clean `main` source at the tagged Phase 12 commits
2. Current automated tests and validators
3. Versioned integration/Reader/Teaching contracts
4. This snapshot
5. Phase 12 and Phase 10 closeout documents
6. Current project snapshots
7. Historical README, stabilization, and early architecture documents

Examples of superseded statements:

- “Kuromoji must be loaded” is historical. Kuromoji linguistic ownership was retired.
- “Phase 12 is future” in the old Phase 8 snapshot is obsolete. Phase 12A/B are complete.
- “Debug report export is deferred” in stable-core documents is obsolete. Debug Report v2 exists.
- “Phase 10 pending” in older snapshots is obsolete. Phase 10 is complete.

---

## 18. AI Continuation Protocol

A future AI must follow this sequence.

### Step 1: Read and restate the baseline

Confirm understanding of:

- Two-repository architecture
- JP Analyzer authority boundary
- Current commits and completion tags
- Phase 9 deferral
- Phase 12A persistent-worker behavior
- Phase 12B bounded Reader scheduling behavior
- Runtime data safety

### Step 2: Verify live repositories

```powershell
Set-Location "D:\Mining\novel-audio-miner"
git fetch --prune
git status --short
git branch --show-current
git rev-parse HEAD
git tag --points-at HEAD

Set-Location "D:\Mining\JP analyzer"
git fetch --prune
git status --short
git branch --show-current
git rev-parse HEAD
git tag --points-at HEAD
```

If the live state differs, do not assume this snapshot is still the latest. Collect fresh exact source and explain the difference.

### Step 3: Define a bounded next milestone

State:

- Problem and evidence
- Repository ownership
- Files likely affected
- Contracts that must not change
- Automated tests
- Real runtime checks
- Rollback plan

### Step 4: Inspect exact source

Do not write blind patches from this snapshot alone. Read exact current files. For large or risky changes, create a read-only source bundle with paths, hashes, Git state, and relevant files.

### Step 5: Use guarded changes

Require branch/HEAD/clean-tree checks and unique replacements. Stop on ambiguity.

### Step 6: Preserve invariants

Never silently change:

- Analyzer linguistic ownership
- Reader span reconstruction
- Correction-aware cache identity
- Teaching evidence immutability
- Separation of Teaching and operational corrections
- Dictionary safety
- Single-worker concurrency
- Bounded session-only sentence caching
- Privacy boundary of sanitized observability

### Step 7: Validate fully

For frontend/Reader changes, at minimum consider:

```powershell
npm.cmd run test:phase5
npm.cmd run test:phase12b
npm.cmd run validate:phase12b
npm.cmd run build
```

For backend changes, run targeted tests plus `run_tests.ps1`. For startup/runtime changes, perform liveness, health, Reader navigation, and shutdown checks.

### Step 8: Document and close

Update the appropriate snapshot/phase docs, commit on a feature branch, merge only after qualification, tag only formal completion points, and record final commits.

---

## 19. Quick Resume Block

Give this file to a new AI and use the following prompt:

```text
Read PROJECT_SNAPSHOT_PHASE12_COMPLETE.md completely before responding.
Treat it as the authoritative development handoff, but verify both live Git
repositories before modifying anything. Phase 12A and Phase 12B are complete
and tagged. Do not restart them. Preserve the JP Analyzer authority boundary,
Reader-span contract, Teaching/correction separation, dictionary safety,
persistent single-worker KWJA runtime, Phase 12B bounded scheduling, 50-entry
session-only cache, and sanitized observability. First summarize the verified
baseline and propose a bounded next milestone with tests and rollback.
```

---

## 20. Final Phase 12 Completion Record

```text
JP Analyzer main:              90f7bec2757c89a38389f593fce6421724557f1a
JP Analyzer tag:               phase12a-complete
Novel Audio Miner main:        9eb621cb27a2393265aaff468e8d258c5bf96e92
Novel Audio Miner tag:         phase12b-complete
Phase 10 one-app startup:      complete
Phase 11 tokenizer retirement: complete
Phase 12A backend optimization: complete
Phase 12B Reader optimization:  complete
Phase 9 tuning:                 deferred
Analyzer concurrency:           1
Reader forward prefetch:        10 text scenes
Session analysis cache:         memory-only, maximum 50
Persistent sentence storage:    disabled
Sanitized observability:        enabled
Release tests/build/validation: passed before completion tags
```

This is the authoritative Phase 12-complete handoff. Future development should proceed from this baseline, not recreate it.
