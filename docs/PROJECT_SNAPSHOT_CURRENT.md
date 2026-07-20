# Project Snapshot – Japanese Novel Mining App

> **Snapshot date:** 20 July 2026, 23:00 IST  
> **JP Analyzer checkpoint:** `032182a24247da4cc68274ccda2b1aca2ff4d871` (`main`) — `11.8.0-structural-teaching-backend`  
> **Novel Audio Miner checkpoint:** `116d961` on `feature/jp-analyzer-integration`  
> **Critical warning:** The Novel Audio Miner Phase 3 commits predate the new authoritative JP Analyzer `readerSpans` layer. They are reusable transport/shadow/preview infrastructure, not the final reader-facing integration.

## 1. Purpose & Goal

The project is a Japanese novel reading and mining application. The finished app should load EPUB novels, preserve Japanese text and ruby/furigana, analyse each sentence, colour coherent learner-facing units, track known/unknown vocabulary and frequency, calculate comprehension, expose New Words, play or generate audio, and support reliable Anki mining. Yomitan remains responsible for interactive dictionary lookup and the user’s dictionary/Anki workflow; Novel Audio Miner should not become a competing dictionary UI.

The long-term ownership model is:

```text
JP Analyzer
  owns linguistic boundaries, reader roles, compounds, grammar identity, lookup identities,
  candidate generation/evaluation, abstention, and structural teaching corrections.

Novel Audio Miner
  owns EPUB reading, rendering, user-known/frequency colour resolution, navigation, audio,
  comprehension display, New Words UI, teaching interaction, and mining workflow.

Yomitan
  owns dictionary lookup, reading/definition choice, and the user-facing dictionary workflow.
```

The final renderer must colour complete learner-facing units such as `頷いて`, `出て行った`, `読み終わった`, and `走り出した`, while preserving separate actions such as `読んで | 寝た`. When evidence is insufficient, JP Analyzer must abstain and emit neutral `unresolved` output rather than guess.

## 2. Where We Are Now (Current Phase)

### Exact current phase

**Phase 3 — migrate Novel Audio Miner from the old `resolvedSpans` shadow adapter to the new authoritative, correction-aware `readerSpans` contract.**

The old Novel Audio Miner integration branch was created before JP Analyzer had the reader-facing layer. It currently uses internal `resolvedSpans`, adapts them in the frontend, and can therefore display broken analytical pieces such as bare stems/auxiliaries. JP Analyzer Phase 2 is now complete and supplies authoritative `readerSpans`, `readerCandidates`, `readerSelection`, and exact structural teaching corrections. The next work is entirely on the Novel Audio Miner integration path; do not rework JP Analyzer candidate logic unless a genuine analyzer bug is demonstrated.

### Progress so far

#### JP Analyzer — completed Phase 2
- `be3994e` Add authoritative reader spans contract
- `bbc30eb` Add reader spans contract regression test
- `5076924` Add reader candidate schema and correction backend
- `7c830b5` / `8078f8b` Generate evidence-based reader candidates
- `5bc0e81` Stabilize reader candidate generation safeguards
- `ad17a33` Generate safe reader lookup hypotheses
- `1abdf43` Evaluate reader candidates against dictionary
- `9681082` Attach structural evidence to reader candidates
- `4568e1b` Treat number expressions as ordinary reader terms
- `fcb73a4` Select reader candidates with conservative evidence gates
- `032182a` Apply exact structural teaching corrections

Current JP Analyzer contracts:

```text
Analyzer version:             11.8.0-structural-teaching-backend
Compact schema:               1.2
Reader span schema:           1.1
Reader candidate schema:      2.0
Teaching contract:            1.0
Engine contract:              9.0.0-alpha2.2-evidence-gated-decision
```

#### Novel Audio Miner — older reusable integration foundation
- `f07f6bc` Add JP Analyzer Phase 1 diagnostic integration
- `2928589` Add JP Analyzer active-scene shadow mode
- `b113af2` Add JP Analyzer shadow reader comparison
- `34e8de8` Add safe JP Analyzer visual colour preview
- `116d961` Define analyzer integration ownership

These commits provide health checks, sentence requests, validation, caching, diagnostics, shadow comparison, and a safe preview. They are not the final integration because they consume `resolvedSpans` through a frontend linguistic adapter.

### Phases and remaining tasks

#### Phase 1 — ownership, consolidation, and safe baseline — complete
- Consolidated analyzer runtime and layers.
- Defined that JP Analyzer owns linguistic decisions and Novel Audio Miner consumes them.
- Preserved legacy reader behavior while integration was diagnostic-only.

#### Phase 2 — authoritative reader-facing analysis — complete
- Reader-facing span contract.
- Candidate generation and safeguards.
- Candidate-specific lookup hypotheses and dictionary evaluation.
- Morphology, predicate, grammar, KWJA, and competition evidence.
- Conservative selection with explicit abstention.
- Number words normalized as ordinary lexical terms.
- Exact occurrence structural teaching backend, preview/save/list/deactivate, provenance, and correction application.

#### Phase 3 — frontend integration — current
- **3.1:** Add a thin direct `readerSpans` validator/adapter. No linguistic reclassification.
- **3.2:** Keep the old `resolvedSpans` adapter only for diagnostics/comparison and clearly mark it legacy.
- **3.3:** Change the existing JP Analyzer visual preview to render validated `readerSpans`.
- **3.4:** Resolve known/frequency colours using analyzer-supplied `knownLookupKey` and `frequencyLookupKey` only.
- **3.5:** Add controlled colour-source modes: JP Analyzer, legacy Kuromoji, neutral.
- **3.6:** After visual validation, make JP Analyzer the default visible colour source.
- **3.7:** Cache by sentence plus analyzer/schema/correction state and prefetch current/next scenes.

#### Phase 4 — presentation refinement
- Lexical/compound units: known green or existing frequency colour.
- Function material: muted grey.
- Learnable grammar: dedicated grammar colour.
- Names: name colour.
- Punctuation and unresolved: neutral.
- Preserve ruby/furigana alignment and Yomitan text selection.

#### Phase 5 — migrate comprehension, New Words, and mining eligibility
- First calculate Kuromoji and analyzer comprehension in shadow and compare.
- Then use `countsForComprehension`, `showInNewWords`, and `eligibleForMining`.
- Keep Yomitan responsible for dictionary lookup and actual Anki card mining.
- Do not infer fallback headwords in the frontend.

#### Phase 6 — simplify Debug Mode
- Replace crowded panels with Export Debug Report and optional diagnostic ID.
- Include analyzer versions, schemas, spans, candidates, selection, corrections, cache, EPUB/ruby/image, learning, and mining information.

#### Phase 7 — dictionary management
- Make JP Analyzer dictionary sync persistent and settings-driven.
- Yomitan dictionaries remain managed by Yomitan.
- Normal reading should not require repeatedly uploading dictionaries.

#### Phase 8 — teaching frontend
- Teaching Mode: select an exact source range, inspect current partition, preview, save, and undo.
- Structural actions: Show as one unit, Split, Vocabulary, Grammar, Function, Name, Leave uncoloured, Undo.
- No “change lookup word” action; Yomitan handles lookup. Analyzer derives internal identity from evidence.

#### Phase 9 — correction data and ranker tuning
- Store accepted and rejected candidates, original/replacement partitions, evidence snapshots, analyzer version, and scope.
- Exact corrections apply immediately; global behavior changes only after offline training/validation.
- Hard invariants remain fixed: offsets, source reconstruction, no overlaps, no punctuation crossing, no fabricated identities.

#### Phase 10 — one-application startup
- One launcher starts JP Analyzer, finds KWJA, opens dictionaries, starts frontend, checks health, and shuts child processes down cleanly.

#### Phase 11 — retire Kuromoji
- Remove only after colouring, comprehension, New Words, mining, corrections, caching, fallback, and startup are stable over real reading sessions.

#### Phase 12 — reading-driven maintenance
- Classify findings as teaching correction, analyzer bug, dictionary gap, EPUB issue, or display-policy issue.

### Known issues or unfinished parts
- Novel Audio Miner still treats Kuromoji as the production linguistic source.
- The old analyzer adapter reads `resolvedSpans` and reclassifies internal roles in the frontend.
- Visible analyzer preview is based on the old internal resolver contract, not authoritative `readerSpans`.
- The frontend’s old numeric category is obsolete; JP Analyzer now treats number words as ordinary lexical terms.
- Existing surface-search fallback must never be used for analyzer spans; invalid analyzer offsets must trigger neutral rendering and diagnostics.
- The frontend teaching panel is not implemented, although the backend is ready.
- Comprehension, New Words, and mining still depend on legacy tokenization.
- The exact permanent teaching example `少年が走ってきた。 → 少年 | が | 走ってきた | 。` is stored locally in SQLite when activated; teaching data is intentionally not committed to Git.

### Next immediate action items
1. Inspect and build the clean Novel Audio Miner branch at `116d961`.
2. Create `analyzerReaderSpanAdapter` that validates and mechanically preserves `readerSpans`.
3. Add tests for source equality, integer offsets, exact surfaces, contiguity, coverage, roles, and correction metadata.
4. Point the existing Debug Mode analyzer colour preview at the new adapter.
5. Validate the representative sentences listed in Section 6, including the correction-aware `走ってきた` case.
6. Do not migrate comprehension/New Words/mining in the same patch.

## 3. Full Project File Structure

### JP Analyzer — exported working source tree

```text
├── CONSOLIDATED_ANALYZER.md
├── README.md
├── app
│   ├── __init__.py
│   └── analyzer
│       ├── __init__.py
│       ├── adapters
│       │   ├── __init__.py
│       │   ├── dictionary_adapter.py
│       │   └── kwja_adapter.py
│       ├── compact_output.py
│       ├── config.py
│       ├── contracts.py
│       ├── engine.py
│       ├── ginza_runtime.py
│       ├── health.py
│       ├── kwja_runtime.py
│       ├── layers
│       │   ├── __init__.py
│       │   ├── candidates.py
│       │   ├── decision.py
│       │   ├── dictionary.py
│       │   ├── dictionary_api.py
│       │   ├── dictionary_evidence_api.py
│       │   ├── dictionary_store.py
│       │   ├── evidence_gate.py
│       │   ├── grammar.py
│       │   ├── invariants.py
│       │   ├── kwja.py
│       │   ├── morphology.py
│       │   ├── protected.py
│       │   ├── schema.py
│       │   ├── stabilization.py
│       │   └── structure.py
│       ├── pipeline.py
│       ├── reader_projection.py
│       ├── runtime.py
│       ├── semantic_snapshot.py
│       ├── service.py
│       ├── services.py
│       ├── source_contract.py
│       └── version.py
├── docs
│   ├── KWJA_SETUP_WINDOWS.md
│   └── READER_PROJECTION_CONTRACT.md
├── evaluation
│   ├── ANNOTATION_GUIDELINES.md
│   ├── ERROR_TAXONOMY.md
│   ├── PACKAGE_MANIFEST.json
│   ├── README.md
│   ├── schemas
│   │   ├── corpus_record.schema.json
│   │   └── gold_annotation.schema.json
│   ├── scripts
│   │   ├── enrich_baseline_compact.py
│   │   ├── inspect_accuracy_baseline.py
│   │   ├── inspect_compact_keys.py
│   │   ├── make_annotation_batches.py
│   │   ├── run_baseline.py
│   │   ├── score_accuracy.py
│   │   ├── score_annotations.py
│   │   └── validate_gold.py
│   └── templates
│       └── change_record.json
├── requirements-frozen-py311.txt
├── requirements-kwja-py311.txt
├── requirements.txt
├── run_snapshot_regression.py
├── run_tests.ps1
├── scripts
│   └── setup_kwja_windows.ps1
└── tests
    ├── __init__.py
    ├── corpora
    │   ├── README.md
    │   ├── development
    │   │   └── random_sentences.txt
    │   └── parity
    │       ├── consolidation_fresh_unseen_200.txt
    │       └── consolidation_fresh_unseen_200_manifest.json
    ├── fixtures
    │   └── single_case_semantic_reference.json
    ├── test_decision.py
    ├── test_dictionary_adapter.py
    ├── test_dictionary_evidence.py
    ├── test_dictionary_path.py
    ├── test_engine_routing.py
    ├── test_evidence_routing.py
    ├── test_facade.py
    ├── test_health_contract.py
    ├── test_import_boundary.py
    ├── test_kwja_adapter.py
    ├── test_kwja_timeout.py
    ├── test_no_legacy_imports.py
    ├── test_reader_projection_contract.py
    ├── test_runtime_contracts.py
    ├── test_runtime_reuse.py
    ├── test_semantic_snapshot.py
    └── test_single_pass.py
```

### Novel Audio Miner — latest available exported source tree

> This export represents the old Phase 3 integration foundation. Git verifies the live branch checkpoint is `116d961`; regenerate the export from the live repo before patching if this snapshot’s export commit differs.

```text
├── FINAL_STABLE_STATUS.md
├── LOCAL_DATA_MANIFEST.example.json
├── PROJECT_STRUCTURE.md
├── README.md
├── RELEASE_CHECKLIST.md
├── STABILIZATION.md
├── WORD_MODEL_POLICY.md
├── index.html
├── package-lock.json
├── package.json
├── public
│   └── dict
│       └── user_dictionary_seed.json
├── src
│   ├── App.jsx
│   ├── components
│   │   ├── DictionaryDebugPanel.jsx
│   │   ├── FileLoader.jsx
│   │   ├── JpAnalyzerIntegrationPanel.jsx
│   │   ├── Phase8DictionarySyncPanel.jsx
│   │   └── Reader.jsx
│   ├── lib
│   │   ├── analyzerShadowComparison.js
│   │   ├── analyzerWordAdapter.js
│   │   ├── ankiConnect.js
│   │   ├── dictionaryDetection.js
│   │   ├── dictionaryLookup.js
│   │   ├── dictionaryStorage.js
│   │   ├── dictionaryValidationBridge.js
│   │   ├── enrichService.js
│   │   ├── epubParser.js
│   │   ├── frequencyMap.js
│   │   ├── japaneseSentenceSplitter.js
│   │   ├── jpAnalyzerClient.js
│   │   ├── phase8DictionarySync.js
│   │   ├── storage.js
│   │   ├── tokenizer.js
│   │   ├── useJpAnalyzerShadow.js
│   │   ├── wordCache.js
│   │   └── wordModel.js
│   ├── main.jsx
│   └── styles.css
└── vite.config.js
```

### File-purpose index — JP Analyzer

- `CONSOLIDATED_ANALYZER.md` — Project documentation.
- `README.md` — Repository overview and operating instructions.
- `app/__init__.py` — Python source or utility module.
- `app/analyzer/__init__.py` — Python source or utility module.
- `app/analyzer/adapters/__init__.py` — Python source or utility module.
- `app/analyzer/adapters/dictionary_adapter.py` — Dictionary import, persistence, lookup, or integration support.
- `app/analyzer/adapters/kwja_adapter.py` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/compact_output.py` — Builds the stable compact API contract, including reader output.
- `app/analyzer/config.py` — Python source or utility module.
- `app/analyzer/contracts.py` — Typed analysis options and public/internal contract definitions.
- `app/analyzer/engine.py` — Single-pass analyzer engine façade and runtime execution.
- `app/analyzer/ginza_runtime.py` — Reusable analyzer runtime and configuration management.
- `app/analyzer/health.py` — Health/readiness reporting for analyzer runtime and dictionaries.
- `app/analyzer/kwja_runtime.py` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/layers/__init__.py` — Python source or utility module.
- `app/analyzer/layers/candidates.py` — Python source or utility module.
- `app/analyzer/layers/decision.py` — Candidate normalization, scoring, conflict resolution, and explainable decisions.
- `app/analyzer/layers/dictionary.py` — Dictionary candidate evaluation and evidence scoring.
- `app/analyzer/layers/dictionary_api.py` — Dictionary synchronization HTTP API.
- `app/analyzer/layers/dictionary_evidence_api.py` — HTTP API for dictionary evidence evaluation.
- `app/analyzer/layers/dictionary_store.py` — Persistent SQLite dictionary synchronization and storage.
- `app/analyzer/layers/evidence_gate.py` — Consolidates linguistic evidence and protects immutable layer contracts.
- `app/analyzer/layers/grammar.py` — Python source or utility module.
- `app/analyzer/layers/invariants.py` — Python source or utility module.
- `app/analyzer/layers/kwja.py` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/layers/morphology.py` — Python source or utility module.
- `app/analyzer/layers/protected.py` — Python source or utility module.
- `app/analyzer/layers/schema.py` — Python source or utility module.
- `app/analyzer/layers/stabilization.py` — Python source or utility module.
- `app/analyzer/layers/structure.py` — Python source or utility module.
- `app/analyzer/pipeline.py` — Public analysis pipeline and compact/full output orchestration.
- `app/analyzer/reader_projection.py` — Projects analyzer spans into authoritative reader-facing spans and validates coverage.
- `app/analyzer/runtime.py` — Reusable analyzer runtime and configuration management.
- `app/analyzer/semantic_snapshot.py` — Python source or utility module.
- `app/analyzer/service.py` — FastAPI service entry point and HTTP routes.
- `app/analyzer/services.py` — Python source or utility module.
- `app/analyzer/source_contract.py` — Python source or utility module.
- `app/analyzer/version.py` — Declares analyzer, schema, and engine contract versions.
- `docs/KWJA_SETUP_WINDOWS.md` — KWJA integration, runtime handling, or related validation.
- `docs/READER_PROJECTION_CONTRACT.md` — Projects analyzer spans into authoritative reader-facing spans and validates coverage.
- `evaluation/ANNOTATION_GUIDELINES.md` — Project documentation.
- `evaluation/ERROR_TAXONOMY.md` — Project documentation.
- `evaluation/PACKAGE_MANIFEST.json` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/README.md` — Repository overview and operating instructions.
- `evaluation/schemas/corpus_record.schema.json` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/schemas/gold_annotation.schema.json` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/scripts/enrich_baseline_compact.py` — Python source or utility module.
- `evaluation/scripts/inspect_accuracy_baseline.py` — Python source or utility module.
- `evaluation/scripts/inspect_compact_keys.py` — Python source or utility module.
- `evaluation/scripts/make_annotation_batches.py` — Python source or utility module.
- `evaluation/scripts/run_baseline.py` — Python source or utility module.
- `evaluation/scripts/score_accuracy.py` — Python source or utility module.
- `evaluation/scripts/score_annotations.py` — Python source or utility module.
- `evaluation/scripts/validate_gold.py` — Python source or utility module.
- `evaluation/templates/change_record.json` — Data, fixture, manifest, snapshot, or configuration.
- `requirements-frozen-py311.txt` — Dependency and build/runtime configuration.
- `requirements-kwja-py311.txt` — Dependency and build/runtime configuration.
- `requirements.txt` — Dependency and build/runtime configuration.
- `run_snapshot_regression.py` — Python source or utility module.
- `run_tests.ps1` — Runs the consolidated repository test suite.
- `scripts/setup_kwja_windows.ps1` — KWJA integration, runtime handling, or related validation.
- `tests/__init__.py` — Automated regression/contract test.
- `tests/corpora/README.md` — Repository overview and operating instructions.
- `tests/corpora/development/random_sentences.txt` — Automated regression/contract test.
- `tests/corpora/parity/consolidation_fresh_unseen_200.txt` — Automated regression/contract test.
- `tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json` — Automated regression/contract test.
- `tests/fixtures/single_case_semantic_reference.json` — Automated regression/contract test.
- `tests/test_decision.py` — Candidate normalization, scoring, conflict resolution, and explainable decisions.
- `tests/test_dictionary_adapter.py` — Automated regression/contract test.
- `tests/test_dictionary_evidence.py` — Automated regression/contract test.
- `tests/test_dictionary_path.py` — Automated regression/contract test.
- `tests/test_engine_routing.py` — Single-pass analyzer engine façade and runtime execution.
- `tests/test_evidence_routing.py` — Automated regression/contract test.
- `tests/test_facade.py` — Automated regression/contract test.
- `tests/test_health_contract.py` — Health/readiness reporting for analyzer runtime and dictionaries.
- `tests/test_import_boundary.py` — Automated regression/contract test.
- `tests/test_kwja_adapter.py` — KWJA integration, runtime handling, or related validation.
- `tests/test_kwja_timeout.py` — KWJA integration, runtime handling, or related validation.
- `tests/test_no_legacy_imports.py` — Automated regression/contract test.
- `tests/test_reader_projection_contract.py` — Projects analyzer spans into authoritative reader-facing spans and validates coverage.
- `tests/test_runtime_contracts.py` — Reusable analyzer runtime and configuration management.
- `tests/test_runtime_reuse.py` — Reusable analyzer runtime and configuration management.
- `tests/test_semantic_snapshot.py` — Automated regression/contract test.
- `tests/test_single_pass.py` — Automated regression/contract test.

### File-purpose index — Novel Audio Miner

- `FINAL_STABLE_STATUS.md` — Project documentation.
- `LOCAL_DATA_MANIFEST.example.json` — Data, fixture, manifest, snapshot, or configuration.
- `PROJECT_STRUCTURE.md` — Project documentation.
- `README.md` — Repository overview and operating instructions.
- `RELEASE_CHECKLIST.md` — Project documentation.
- `STABILIZATION.md` — Project documentation.
- `WORD_MODEL_POLICY.md` — Project documentation.
- `index.html` — Project file.
- `package-lock.json` — Data, fixture, manifest, snapshot, or configuration.
- `package.json` — Dependency and build/runtime configuration.
- `public/dict/user_dictionary_seed.json` — Dictionary import, persistence, lookup, or integration support.
- `src/App.jsx` — Application source module.
- `src/components/DictionaryDebugPanel.jsx` — Dictionary import, persistence, lookup, or integration support.
- `src/components/FileLoader.jsx` — Application source module.
- `src/components/JpAnalyzerIntegrationPanel.jsx` — JP Analyzer browser client, integration UI, validation, or diagnostics.
- `src/components/Phase8DictionarySyncPanel.jsx` — Synchronizes frontend dictionaries into JP Analyzer.
- `src/components/Reader.jsx` — Primary reading interface and visible sentence rendering.
- `src/lib/analyzerShadowComparison.js` — Compares Kuromoji reader units with shadow JP Analyzer output.
- `src/lib/analyzerWordAdapter.js` — Legacy frontend adapter that reinterprets resolvedSpans; obsolete for new readerSpans path.
- `src/lib/ankiConnect.js` — AnkiConnect/mining integration.
- `src/lib/dictionaryDetection.js` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/dictionaryLookup.js` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/dictionaryStorage.js` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/dictionaryValidationBridge.js` — Bridges frontend dictionary evidence/validation into analyzer integration.
- `src/lib/enrichService.js` — Application source module.
- `src/lib/epubParser.js` — EPUB parsing, text/ruby extraction, or book navigation.
- `src/lib/frequencyMap.js` — Application source module.
- `src/lib/japaneseSentenceSplitter.js` — Application source module.
- `src/lib/jpAnalyzerClient.js` — JP Analyzer browser client, integration UI, validation, or diagnostics.
- `src/lib/phase8DictionarySync.js` — Synchronizes frontend dictionaries into JP Analyzer.
- `src/lib/storage.js` — Application source module.
- `src/lib/tokenizer.js` — Application source module.
- `src/lib/useJpAnalyzerShadow.js` — Runs/caches active-scene JP Analyzer requests in shadow mode.
- `src/lib/wordCache.js` — Application source module.
- `src/lib/wordModel.js` — Application source module.
- `src/main.jsx` — Application source module.
- `src/styles.css` — Application styling.
- `vite.config.js` — Application source module.

## 4. Complete File Contents

This section embeds the full current contents of the critical code needed to resume. Every other exported file is indexed afterward with size, SHA-256, and purpose. The attached JSON source exports remain the lossless source of truth for all exported files.

### Critical JP Analyzer files — full contents

#### `app/analyzer/version.py`

```python
ANALYZER_VERSION = "11.1.0-reader-spans-contract"
SCHEMA_VERSION = "1.1"
ENGINE_CONTRACT_VERSION = "9.0.0-alpha2.2-evidence-gated-decision"
```

#### `app/analyzer/service.py`

```python
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .layers.dictionary_api import router as dictionary_sync_router
from .layers.dictionary_evidence_api import router as dictionary_evidence_router

from .health import health_report
from .pipeline import analyze
from .version import ANALYZER_VERSION


class AnalyzeRequest(BaseModel):
    text: str


app = FastAPI(title="JP Analyzer", version=ANALYZER_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dictionary_sync_router)
app.include_router(dictionary_evidence_router)


@app.get("/health")
def health():
    return health_report()


@app.post("/analyze")
def analyze_endpoint(
    req: AnalyzeRequest,
    debug: bool = Query(False),
    dictionary: bool = Query(True),
):
    return analyze(req.text, debug=debug, use_dictionary=dictionary)
```

#### `app/analyzer/pipeline.py`

```python
from __future__ import annotations

from .layers.evidence_gate import (
    VERSION as CONSOLIDATED_ENGINE_VERSION,
    analyze_integrated_alpha2 as analyze_layers,
)

from .compact_output import compact_analysis
from .contracts import AnalyzeOptions
from .engine import AnalyzerEngine
from .runtime import get_runtime
from .version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION


def _engine() -> AnalyzerEngine:
    # Pass the module-level alias deliberately. Existing façade tests can replace
    # it with a sentinel, while production still routes through AnalyzerEngine.
    return AnalyzerEngine(
        runtime=get_runtime(),
        analyzer_fn=analyze_layers,
    )


def analyze_full(
    text,
    nlp=None,
    *,
    use_dictionary=True,
    raw_knp=None,
    kwja_executable=None,
):
    if CONSOLIDATED_ENGINE_VERSION != ENGINE_CONTRACT_VERSION:
        raise RuntimeError(
            f"Expected engine contract {ENGINE_CONTRACT_VERSION!r}, "
            f"found {CONSOLIDATED_ENGINE_VERSION!r}."
        )
    options = AnalyzeOptions(
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )
    return _engine().analyze_full(text, nlp, options=options)


def analyze(
    text,
    nlp=None,
    *,
    debug=False,
    use_dictionary=True,
    raw_knp=None,
    kwja_executable=None,
):
    full = analyze_full(
        text,
        nlp,
        use_dictionary=use_dictionary,
        raw_knp=raw_knp,
        kwja_executable=kwja_executable,
    )
    return full if debug else compact_analysis(
        full,
        analyzer_version=ANALYZER_VERSION,
    )
```

#### `app/analyzer/compact_output.py`

```python
from __future__ import annotations

from typing import Any

from .reader_projection import (
    READER_SPAN_SCHEMA_VERSION,
    project_reader_spans,
)
from .version import SCHEMA_VERSION


def compact_analysis(
    result: dict[str, Any],
    *,
    analyzer_version: str,
) -> dict[str, Any]:
    """Project the evidence graph into stable consumer schemas.

    `resolvedSpans` remains unchanged for compatibility and diagnostics.
    `readerSpans` is the versioned, authoritative reader-facing contract.
    This compatibility projection does not merge or reclassify source ranges
    beyond mapping already-selected analyzer roles to display policy fields.
    """
    resolved = result.get("resolved_spans_alpha2") or []
    reader_spans = project_reader_spans(result)
    diagnostics = result.get("diagnostics_alpha2") or []
    metadata = result.get("kwja_metadata_alpha1") or {}
    change = result.get("alpha2_change_summary") or {}
    text = result.get("text", "")

    return {
        "schemaVersion": SCHEMA_VERSION,
        "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
        "analyzerVersion": analyzer_version,
        "engineVersion": result.get("version"),
        "text": text,
        "resolvedSpans": resolved,
        "readerSpans": reader_spans,
        "structure": {
            "predicates": result.get("predicates") or [],
            "clauses": result.get("clauses") or [],
            "arguments": result.get("arguments") or [],
            "predicateRelations": result.get("predicate_relations_alpha31")
            or result.get("predicate_relations")
            or [],
            "entities": result.get("entities") or [],
            "personReferences": result.get("person_references") or [],
        },
        "coverage": {
            "complete": "".join(x.get("surface", "") for x in resolved) == text,
            "readerSpansComplete": "".join(
                x.get("surface", "") for x in reader_spans
            ) == text,
            "unresolvedSpanCount": sum(
                x.get("role") == "unresolved" for x in resolved
            ),
            "readerUnresolvedSpanCount": sum(
                x.get("displayRole") == "unresolved" for x in reader_spans
            ),
            "kwjaAlignmentComplete": bool(
                metadata.get("source_alignment_complete")
            ),
        },
        "changeSummary": change,
        "diagnostics": diagnostics,
    }
```

#### `app/analyzer/reader_projection.py`

```python
from __future__ import annotations

from typing import Any

READER_SPAN_SCHEMA_VERSION = "1.0"

FUNCTION_GRAMMAR_IDS = {
    "V_TE",
}

DISPLAY_ROLES = {
    "lexical",
    "lexical-compound",
    "numeric-lexical",
    "name",
    "learnable-grammar",
    "function",
    "punctuation",
    "unresolved",
}


def _candidate_index(result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("candidate_id")): item
        for item in (result.get("resolver_candidates_alpha2") or [])
        if item.get("candidate_id")
    }


def _source_ids(span: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    values = [
        span.get("selected_candidate_id"),
        candidate.get("source_annotation_id"),
    ]
    values.extend(candidate.get("source_annotation_ids") or [])
    return list(dict.fromkeys(str(value) for value in values if value))


def _classification(
    span: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    role = span.get("role")
    family = candidate.get("candidate_family")
    grammar_id = span.get("grammar_id")
    headword = span.get("headword")

    if role == "punctuation" or family == "punctuation":
        return {
            "displayRole": "punctuation",
            "lexicalType": None,
            "colorPolicy": "neutral",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": False,
        }

    if role == "grammar" and grammar_id and grammar_id not in FUNCTION_GRAMMAR_IDS:
        return {
            "displayRole": "learnable-grammar",
            "lexicalType": None,
            "colorPolicy": "grammar",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": True,
        }

    if role in {"particle", "grammar"} or family == "particle":
        return {
            "displayRole": "function",
            "lexicalType": None,
            "colorPolicy": "muted",
            "unknownColorPolicy": None,
            "knownLookupKey": None,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": False,
        }

    if role == "proper-name" or family == "proper-name":
        lookup = headword or span.get("surface")
        return {
            "displayRole": "name",
            "lexicalType": "proper-name",
            "colorPolicy": "name",
            "unknownColorPolicy": None,
            "knownLookupKey": lookup,
            "frequencyLookupKey": None,
            "countsForComprehension": False,
            "showInNewWords": False,
            "eligibleForMining": True,
        }

    if family == "numeral":
        lookup = headword or span.get("surface")
        return {
            "displayRole": "numeric-lexical",
            "lexicalType": "numeric",
            "colorPolicy": "known-or-numeric",
            "unknownColorPolicy": "numeric",
            "knownLookupKey": lookup,
            "frequencyLookupKey": lookup,
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
        }

    if role == "term":
        lookup = headword or span.get("surface")
        lexical_type = (
            "discourse"
            if family == "discourse"
            else "term"
        )
        return {
            "displayRole": "lexical",
            "lexicalType": lexical_type,
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
            "knownLookupKey": lookup,
            "frequencyLookupKey": lookup,
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
        }

    return {
        "displayRole": "unresolved",
        "lexicalType": None,
        "colorPolicy": "neutral",
        "unknownColorPolicy": None,
        "knownLookupKey": None,
        "frequencyLookupKey": None,
        "countsForComprehension": False,
        "showInNewWords": False,
        "eligibleForMining": False,
    }


def project_reader_spans(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Create the versioned consumer contract without changing linguistic spans."""
    candidates = _candidate_index(result)
    projected: list[dict[str, Any]] = []

    for span in result.get("resolved_spans_alpha2") or []:
        candidate = candidates.get(str(span.get("selected_candidate_id")), {})
        classification = _classification(span, candidate)
        projected.append({
            "start": span.get("start"),
            "end": span.get("end"),
            "surface": span.get("surface"),
            **classification,
            "headword": span.get("headword"),
            "grammarId": span.get("grammar_id"),
            "confidence": span.get("confidence", 0.0),
            "sourceSpanIds": _source_ids(span, candidate),
            "sourceLayer": span.get("source_layer") or candidate.get("source_layer"),
            "projectionStatus": "compatibility",
        })

    validate_reader_spans(result.get("text", ""), projected)
    return projected


def validate_reader_spans(text: str, spans: list[dict[str, Any]]) -> None:
    cursor = 0
    for index, span in enumerate(spans):
        start = span.get("start")
        end = span.get("end")
        surface = span.get("surface")
        role = span.get("displayRole")

        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"readerSpans[{index}] has non-integer offsets")
        if start != cursor:
            raise ValueError(
                f"readerSpans[{index}] expected start {cursor}, found {start}"
            )
        if not (0 <= start < end <= len(text)):
            raise ValueError(f"readerSpans[{index}] has invalid range {start}:{end}")
        if surface != text[start:end]:
            raise ValueError(f"readerSpans[{index}] surface does not match source")
        if role not in DISPLAY_ROLES:
            raise ValueError(f"readerSpans[{index}] has unknown displayRole {role!r}")
        if role in {"lexical", "lexical-compound", "numeric-lexical"}:
            if not span.get("knownLookupKey") or not span.get("frequencyLookupKey"):
                raise ValueError(
                    f"readerSpans[{index}] lexical span is missing lookup keys"
                )
        cursor = end

    if cursor != len(text):
        raise ValueError(
            f"readerSpans coverage ends at {cursor}; source length is {len(text)}"
        )
```

#### `app/analyzer/contracts.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnalyzeOptions:
    debug: bool = False
    use_dictionary: bool = True
    raw_knp: str | None = None
    kwja_executable: str | None = None


def linguistic_projection(result: dict[str, Any]) -> list[tuple[Any, ...]]:
    """Return the stable reader-visible projection contract."""
    return [
        (
            item.get("start"),
            item.get("end"),
            item.get("surface"),
            item.get("role"),
            item.get("headword"),
            item.get("grammar_id"),
            item.get("confidence"),
            item.get("source_layer"),
        )
        for item in (result.get("resolved_spans_alpha2") or [])
    ]
```

#### `app/analyzer/engine.py`

```python
from __future__ import annotations

from collections.abc import Callable
from inspect import signature
from typing import Any

from .layers import analyze_layers

from .adapters import DictionaryAdapter, KwjaAdapter
from .contracts import AnalyzeOptions
from .runtime import AnalyzerRuntime, get_runtime
from .source_contract import validate_analysis_source
from .version import ENGINE_CONTRACT_VERSION


AnalyzerFunction = Callable[..., dict[str, Any]]


class AnalyzerEngine:
    """Single production entry point over the consolidated linguistic layers."""

    def __init__(
        self,
        runtime: AnalyzerRuntime | None = None,
        analyzer_fn: AnalyzerFunction | None = None,
        kwja_adapter: KwjaAdapter | None = None,
        dictionary_adapter: DictionaryAdapter | None = None,
    ):
        self.runtime = runtime or get_runtime()
        self.analyzer_fn = analyzer_fn or analyze_layers
        services = getattr(self.runtime, "services", None)
        runtime_config = getattr(self.runtime, "config", None)

        self.kwja_adapter = kwja_adapter or (
            services.kwja
            if services is not None
            else KwjaAdapter(runtime_config)
        )
        self.dictionary_adapter = dictionary_adapter or (
            services.dictionary
            if services is not None
            else DictionaryAdapter()
        )

    def analyze_full(
        self,
        text: str,
        nlp=None,
        *,
        options: AnalyzeOptions | None = None,
    ) -> dict[str, Any]:
        opts = options or AnalyzeOptions()
        engine_kwargs = {
            "use_dictionary": opts.use_dictionary,
            "raw_knp": opts.raw_knp,
            "kwja_executable": opts.kwja_executable,
        }
        parameters = signature(self.analyzer_fn).parameters
        if "analyze_kwja_fn" in parameters:
            engine_kwargs.update({
                "analyze_kwja_fn": self.kwja_adapter.analyze,
                "evaluate_analysis_fn": self.dictionary_adapter.evaluate_analysis,
                "evaluate_candidate_fn": self.dictionary_adapter.evaluate_candidate,
            })
        result = self.analyzer_fn(
            text,
            nlp if nlp is not None else self.runtime.get_nlp(),
            **engine_kwargs,
        )
        if result.get("version") != ENGINE_CONTRACT_VERSION:
            raise RuntimeError(
                f"Expected engine contract {ENGINE_CONTRACT_VERSION!r}, "
                f"found {result.get('version')!r}."
            )
        source_diagnostics = validate_analysis_source(result)
        if source_diagnostics:
            codes = ", ".join(x.get("code", "UNKNOWN") for x in source_diagnostics)
            raise RuntimeError(f"Stable source contract failed: {codes}")
        return result
```

#### `app/analyzer/runtime.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from .config import AnalyzerConfig
from .ginza_runtime import get_ginza, ginza_model_name
from .services import AnalyzerServices


@dataclass(frozen=True)
class RuntimeStatus:
    ginza_model: str | None
    kwja: dict
    dictionary: dict


class AnalyzerRuntime:
    """Stable owner of reusable analyzer runtime dependencies."""

    def __init__(self, config: AnalyzerConfig | None = None):
        self.config = config or AnalyzerConfig.from_environment()
        self.services = AnalyzerServices.from_config(self.config)

    def get_nlp(self):
        return get_ginza(self.config)

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(
            ginza_model=ginza_model_name(),
            kwja=self.services.kwja.status(),
            dictionary=self.services.dictionary.status(),
        )


_lock = RLock()
_runtime: AnalyzerRuntime | None = None


def get_runtime(config: AnalyzerConfig | None = None) -> AnalyzerRuntime:
    global _runtime
    with _lock:
        if _runtime is None:
            _runtime = AnalyzerRuntime(config)
        elif config is not None and _runtime.config != config:
            raise RuntimeError(
                "Analyzer runtime is already initialized with a different configuration."
            )
        return _runtime


def reset_runtime_for_tests() -> None:
    global _runtime
    with _lock:
        _runtime = None
```

#### `app/analyzer/layers/evidence_gate.py`

```python
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any

from .stabilization import analyze_layered_alpha321
from .dictionary import evaluate_analysis_candidates, evaluate_candidate
from .decision import (
    _candidate_score,
    _candidate_utility,
    _dict_summary,
    analyze_layered_alpha34,
    normalize_candidates,
    resolve_candidates,
)
from .kwja import analyze_kwja_alpha1, attach_kwja_read_only

VERSION = "9.0.0-alpha2.2-evidence-gated-decision"

# Alpha 2 is deliberately allow-listed. KWJA does not generate arbitrary grammar.
PATTERNS = (
    {"suffix": "という", "grammar_id": "TO_IU_QUOTATIVE_MODIFIER", "confidence": .93},
    {"suffix": "でしまう", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "でしまった", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てしまう", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てしまった", "grammar_id": "TE_SHIMAU_INFLECTED", "confidence": .92},
    {"suffix": "てもらえる", "grammar_id": "TE_MORAU_POTENTIAL", "confidence": .93},
    {"suffix": "でもらえる", "grammar_id": "TE_MORAU_POTENTIAL", "confidence": .93},
    {"suffix": "ではあった", "grammar_id": "DEWA_ATTA", "confidence": .90},
)


def _stable_hash(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _crosses_protected(text: str, start: int, end: int, analysis: dict[str, Any]) -> bool:
    protected = list(analysis.get("orthographic_spans") or []) + list(analysis.get("person_references") or [])
    for item in protected:
        a, b = item.get("start"), item.get("end")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        overlaps = start < b and a < end
        contains_exactly = start == a and end == b
        if overlaps and not contains_exactly:
            return True
    # Never create a candidate containing punctuation, even if unavailable in layers.
    return any(ch in text[start:end] for ch in "、。！？!?「」『』（）()……─―～")


def generate_kwja_candidates(text: str, analysis: dict[str, Any], kwja: dict[str, Any]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str, str | None]] = set()
    morphemes = kwja.get("kwja_morphemes_alpha1") or []
    phrases = kwja.get("kwja_basic_phrases_alpha1") or []

    def add(start: int, end: int, family: str, *, grammar_id: str | None = None,
            headword: str | None = None, confidence: float, policy: str,
            source_ids: list[str] | None = None, lemma_status: str | None = None) -> None:
        if not (0 <= start < end <= len(text)) or _crosses_protected(text, start, end, analysis):
            return
        surface = text[start:end]
        key = (start, end, family, grammar_id or headword)
        if key in seen:
            return
        seen.add(key)
        proposals.append({
            "id": f"kwjac{len(proposals)}", "start": start, "end": end,
            "surface": surface, "candidate_family": family,
            "proposed_role": "grammar" if family == "grammar" else "term",
            "grammar_id": grammar_id, "headword": headword,
            "confidence": confidence, "source_layer": "kwja-alpha2",
            "source_annotation_ids": source_ids or [],
            "policy": policy, "lemma_status": lemma_status,
            "evidence": [{
                "source": "kwja-base-structural-evidence",
                "detail": policy, "confidence": confidence,
            }],
        })

    # Pattern proposals must occur wholly inside a KWJA basic phrase. This uses
    # KWJA structure instead of blind global substring matching.
    for phrase in phrases:
        ps, pe = phrase.get("start"), phrase.get("end")
        if not isinstance(ps, int) or not isinstance(pe, int):
            continue
        surface = text[ps:pe]
        for pattern in PATTERNS:
            suffix = pattern["suffix"]
            offset = surface.rfind(suffix)
            if offset >= 0:
                add(ps + offset, ps + offset + len(suffix), "grammar",
                    grammar_id=pattern["grammar_id"], confidence=pattern["confidence"],
                    policy=f"allow-listed KWJA phrase construction: {suffix}",
                    source_ids=[phrase.get("id")])

    # Controlled cross-basic-phrase recovery for quotative という. KWJA places
    # quotative と in the quoted-complement phrase and いう in the following
    # predicate phrase, so this construction cannot be found inside one phrase.
    phrase_by_id = {p.get("id"): p for p in phrases if p.get("id")}
    for left, right in zip(morphemes, morphemes[1:]):
        if left.get("surface") != "と" or right.get("surface") != "いう":
            continue
        if left.get("end") != right.get("start"):
            continue
        if left.get("basic_phrase_id") == right.get("basic_phrase_id"):
            continue
        if right.get("pos") != "動詞" or right.get("lemma") not in {"言う", "いう"}:
            continue
        right_phrase = phrase_by_id.get(right.get("basic_phrase_id")) or {}
        target_id = right_phrase.get("destination_basic_phrase_id")
        target_phrase = phrase_by_id.get(target_id) or {}
        target_features = target_phrase.get("features") or []
        # Require いう to modify a following nominal/basic phrase when KWJA
        # exposes that target. This blocks generic quotation predicates.
        if target_id is None or "体言" not in target_features:
            continue
        start, end = left["start"], right["end"]
        if text[start:end] == "という":
            add(start, end, "grammar", grammar_id="TO_IU_QUOTATIVE_MODIFIER",
                confidence=.94,
                policy="controlled adjacent KWJA phrases: quotative と + 言う modifying nominal",
                source_ids=[left.get("id"), right.get("id"),
                            left.get("basic_phrase_id"), right.get("basic_phrase_id")])

    # Complete lexical adjective recovery, currently limited to the validated gap.
    for m in morphemes:
        if m.get("surface") == "つまらない" and m.get("pos") == "形容詞":
            add(m["start"], m["end"], "term", headword="つまらない", confidence=.91,
                policy="KWJA preserves validated complete adjective",
                source_ids=[m.get("id")], lemma_status="corroborated-surface")

    # Unknown/coined predicate preservation: only when KWJA sees one verb-like
    # morpheme spanning 2+ characters and existing morphology fragments its range.
    existing_ms = analysis.get("morphemes") or []
    for m in morphemes:
        if m.get("pos") != "動詞" or not isinstance(m.get("start"), int):
            continue
        start, end, surface = m["start"], m["end"], m.get("surface") or ""
        covered = [x for x in existing_ms if x.get("start", -1) >= start and x.get("end", -1) <= end]
        fragmented = len(covered) >= 2
        projected = [
            x for x in (analysis.get("resolved_spans_alpha34") or [])
            if start < x.get("end", -1) and x.get("start", -1) < end
        ]
        unresolved = [
            x for x in projected
            if x.get("role") == "unresolved"
        ]
        lexical_fragments = [
            x for x in projected
            if x.get("role") == "term"
        ]
        structurally_fragmented = (
            bool(unresolved)
            or len(lexical_fragments) >= 2
        )
        suspicious_lemma = m.get("lemma") not in {surface, None, ""}
        if (
            len(surface) >= 3
            and fragmented
            and structurally_fragmented
            and suspicious_lemma
        ):
            add(start, end, "term", headword=None, confidence=.76,
                policy="KWJA preserves complete fragmented predicate; lemma withheld",
                source_ids=[m.get("id")], lemma_status="withheld-pending-corroboration")
    return proposals


def _overlapping_baseline_spans(proposal, baseline_spans):
    start, end = proposal["start"], proposal["end"]
    return [x for x in baseline_spans if start < x.get("end", -1) and x.get("start", -1) < end]


def classify_kwja_proposal(proposal, baseline_spans):
    """Evidence gate: layers propose; only genuine improvements enter resolution."""
    overlapping = _overlapping_baseline_spans(proposal, baseline_spans)
    exact = [x for x in overlapping if x.get("start") == proposal["start"] and x.get("end") == proposal["end"]]
    unresolved = [x for x in overlapping if x.get("role") == "unresolved"]
    terms = [x for x in overlapping if x.get("role") == "term"]
    complete_same_role = [x for x in exact if x.get("role") == proposal.get("proposed_role")]

    if complete_same_role:
        status, eligible = "corroborates-existing", False
        reason = "Existing licensed analysis already covers the same range and role."
    elif unresolved:
        status, eligible = "eligible-improvement", True
        reason = "Proposal replaces unresolved baseline coverage."
    elif proposal.get("candidate_family") == "term" and len(terms) >= 2:
        status, eligible = "eligible-structural-repair", True
        reason = "Proposal consolidates multiple lexical fragments."
    else:
        status, eligible = "evidence-only", False
        reason = "Evidence adds support but does not improve the final projection."

    result = dict(proposal)
    result.update({
        "decision_status": status,
        "resolver_eligible": eligible,
        "decision_reason": reason,
        "baseline_overlap": [
            {"start": x.get("start"), "end": x.get("end"), "surface": x.get("surface"),
             "role": x.get("role"), "grammar_id": x.get("grammar_id"), "headword": x.get("headword")}
            for x in overlapping
        ],
    })
    return result


def _normalized_kwja_candidate(proposal: dict[str, Any], dictionary_record: dict[str, Any] | None, index: int) -> dict[str, Any]:
    dsum = _dict_summary([dictionary_record] if dictionary_record else [])
    record = {
        "candidate_id": f"a2kwja{index}",
        "start": proposal["start"], "end": proposal["end"], "surface": proposal["surface"],
        "proposed_role": proposal["proposed_role"], "candidate_family": proposal["candidate_family"],
        "headword": proposal.get("headword"), "grammar_id": proposal.get("grammar_id"),
        "confidence": proposal["confidence"], "protected": False,
        "source_layer": "kwja-alpha2", "source_annotation_id": proposal["id"],
        "morpheme_ids": [], "dictionary_evidence": dsum,
        "evidence": deepcopy(proposal.get("evidence") or []),
        "kwja_policy": proposal.get("policy"), "lemma_status": proposal.get("lemma_status"),
    }
    record["utility_dimensions"] = _candidate_utility(record)
    record["utility_score"] = _candidate_score(record)
    return record


def analyze_integrated_alpha2(text: str, nlp, *, use_dictionary: bool = True,
                              raw_knp: str | None = None, kwja_executable: str | None = None,
                              analyze_kwja_fn=None, evaluate_analysis_fn=None,
                              evaluate_candidate_fn=None) -> dict[str, Any]:
    analyze_kwja_fn = analyze_kwja_fn or analyze_kwja_alpha1
    evaluate_analysis_fn = evaluate_analysis_fn or evaluate_analysis_candidates
    evaluate_candidate_fn = evaluate_candidate_fn or evaluate_candidate
    baseline = analyze_layered_alpha321(text, nlp)
    dictionary = evaluate_analysis_fn(baseline) if use_dictionary else None
    alpha34 = analyze_layered_alpha34(text, nlp, dictionary)
    baseline_snapshot = {
        "morphemes": _stable_hash(alpha34.get("morphemes")),
        "existing_fields": {k: _stable_hash(v) for k, v in alpha34.items()},
        "resolved_spans": _stable_hash(alpha34.get("resolved_spans_alpha34")),
        "decisions": _stable_hash(alpha34.get("resolver_decisions_alpha34")),
    }
    kwja = analyze_kwja_fn(text, raw_knp=raw_knp, executable=kwja_executable)
    attached = attach_kwja_read_only(alpha34, kwja)
    raw_proposals = generate_kwja_candidates(text, alpha34, kwja)
    baseline_spans = alpha34.get("resolved_spans_alpha34") or []
    proposals = [classify_kwja_proposal(p, baseline_spans) for p in raw_proposals]

    dictionary_records = []
    for proposal in proposals:
        dictionary_records.append(evaluate_candidate_fn(proposal) if use_dictionary else None)
    eligible_pairs = [(p, d) for p, d in zip(proposals, dictionary_records) if p.get("resolver_eligible")]
    kwja_candidates = [_normalized_kwja_candidate(p, d, i) for i, (p, d) in enumerate(eligible_pairs)]
    all_candidates = list(alpha34.get("resolver_candidates_alpha34") or []) + kwja_candidates
    selected, decisions, conflicts = resolve_candidates(text, all_candidates)
    resolved = [{
        "start": c["start"], "end": c["end"], "surface": c["surface"],
        "role": c["proposed_role"], "headword": c.get("headword"),
        "grammar_id": c.get("grammar_id"), "confidence": c.get("confidence", 0.0),
        "selected_candidate_id": c["candidate_id"], "source_layer": c.get("source_layer"),
    } for c in selected]

    def projection_signature(items):
        return [(x.get("start"), x.get("end"), x.get("surface"), x.get("role"),
                 x.get("headword"), x.get("grammar_id")) for x in items]
    changed = projection_signature(resolved) != projection_signature(alpha34.get("resolved_spans_alpha34") or [])
    diagnostics = []
    if "".join(x["surface"] for x in resolved) != text:
        diagnostics.append({"severity":"error", "code":"P9A2_PROJECTION_INCOMPLETE"})
    if _stable_hash(attached.get("morphemes")) != baseline_snapshot["morphemes"]:
        diagnostics.append({"severity":"error", "code":"P9A2_LAYER0_MUTATED"})
    if not (kwja.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete"):
        diagnostics.append({"severity":"error", "code":"P9A2_KWJA_ALIGNMENT_INCOMPLETE"})

    attached.update({
        "version": VERSION,
        "kwja_candidates_alpha2": proposals,
        "kwja_dictionary_evidence_alpha2": [x for x in dictionary_records if x is not None],
        "resolver_candidates_alpha2": all_candidates,
        "resolver_conflicts_alpha2": conflicts,
        "resolver_decisions_alpha2": decisions,
        "resolved_spans_alpha2": resolved,
        "diagnostics_alpha2": diagnostics,
        "alpha2_change_summary": {
            "final_projection_changed": changed,
            "kwja_proposal_count": len(proposals),
            "kwja_eligible_count": sum(bool(x.get("resolver_eligible")) for x in proposals),
            "kwja_corroboration_count": sum(x.get("decision_status") == "corroborates-existing" for x in proposals),
            "kwja_evidence_only_count": sum(x.get("decision_status") == "evidence-only" for x in proposals),
            "kwja_selected_count": sum(x.get("source_layer") == "kwja-alpha2" for x in resolved),
            "baseline_unresolved_count": sum(x.get("role") == "unresolved" for x in alpha34.get("resolved_spans_alpha34") or []),
            "alpha2_unresolved_count": sum(x.get("role") == "unresolved" for x in resolved),
        },
        "phase9_alpha2_contract": {
            "layer0_immutable": True, "earlier_evidence_fields_preserved": True,
            "kwja_candidates_allow_listed": True, "kwja_readings_non_authoritative": True,
            "kwja_unknown_lemmas_withheld": True, "kwja_arguments_not_resolver_candidates": True,
            "protected_boundaries_enforced": True, "dictionary_miss_is_not_rejection": True,
            "central_resolver_makes_final_decision": True,
            "evidence_improvement_required_for_selection": True,
            "same_range_existing_analysis_is_not_displaced": True,
        },
    })
    return attached
```

#### `app/analyzer/layers/decision.py`

```python
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Iterable

ROLE_ORDER = {
    "punctuation": 90,
    "proper-name": 80,
    "grammar": 70,
    "numeral": 65,
    "discourse": 63,
    "term": 60,
    "particle": 40,
    "speech-fragment": 30,
    "unresolved": 0,
}

SPECIFIC_GRAMMAR_BONUS = {
    "TE_IRU_PAST": 18,
    "DE_IRU_PAST": 18,
    "TE_IRU_NEGATIVE": 18,
    "TE_IRU_POLITE": 18,
    "TE_MORAU_POTENTIAL": 18,
    "TE_SHIMAU_INFLECTED": 16,
    "TE_KURERU_INFLECTED": 16,
    "NAKEREBA_NARANAI": 20,
    "KOTO_GA_DEKIRU": 18,
}
GENERIC_GRAMMAR_IDS = {"TE_IRU_CHAIN", "V_TE"}


def _snapshot_morphology(items: list[dict[str, Any]]) -> str:
    payload = repr([
        (x.get("id"), x.get("start"), x.get("end"), x.get("surface"),
         x.get("lemma"), x.get("normalized"), x.get("pos"), x.get("tag"),
         x.get("dependency"), x.get("head_id"))
        for x in items
    ])
    return sha256(payload.encode("utf-8")).hexdigest()


def _valid_range(text: str, item: dict[str, Any]) -> bool:
    a, b = item.get("start"), item.get("end")
    return (
        isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(text)
        and text[a:b] == item.get("surface")
    )


def _dictionary_by_range(dictionary_result: dict[str, Any] | None) -> dict[tuple[int, int], list[dict[str, Any]]]:
    out: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    if not dictionary_result:
        return out
    evidence = dictionary_result.get("evidence") or dictionary_result.get("dictionary_evidence") or []
    for item in evidence:
        a, b = item.get("start"), item.get("end")
        if isinstance(a, int) and isinstance(b, int):
            out[(a, b)].append(item)
    return out


def _dict_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    records = list(records)
    matched = [x for x in records if x.get("matched")]
    type_counts: dict[str, int] = defaultdict(int)
    sources: set[str] = set()
    headwords: set[str] = set()
    confidence = 0.0
    pos_compatible = False
    for item in matched:
        confidence = max(confidence, float(item.get("confidence") or 0.0))
        pos_compatible = pos_compatible or (item.get("pos_compatibility") or {}).get("status") == "compatible"
        for key, value in (item.get("dictionary_type_counts") or {}).items():
            type_counts[str(key)] += int(value or 0)
        sources.update(str(x) for x in (item.get("source_names") or []))
        headwords.update(str(x) for x in (item.get("matched_headwords") or []) if x)
    return {
        "matched": bool(matched),
        "evidence_records": len(records),
        "matched_records": len(matched),
        "dictionary_type_counts": dict(type_counts),
        "source_names": sorted(sources),
        "independent_source_count": len(sources),
        "matched_headwords": sorted(headwords),
        "confidence": confidence or None,
        "pos_compatible": pos_compatible,
    }


def _specificity(candidate: dict[str, Any]) -> int:
    family = candidate["candidate_family"]
    if family == "grammar":
        gid = candidate.get("grammar_id") or ""
        if gid in SPECIFIC_GRAMMAR_BONUS:
            return 95
        if gid in GENERIC_GRAMMAR_IDS:
            return 55
        return 78
    if family == "proper-name":
        return 88 if len(candidate.get("morpheme_ids") or []) > 1 else 76
    if family in {"punctuation", "numeral", "discourse"}:
        return 85
    if family == "term":
        return 70
    if family == "particle":
        return 65
    return 30


def _completeness(candidate: dict[str, Any]) -> int:
    family = candidate["candidate_family"]
    length = candidate["end"] - candidate["start"]
    if family in {"grammar", "proper-name", "numeral", "discourse", "punctuation"}:
        return min(100, 70 + length * 3)
    return min(85, 55 + length * 2)


def _candidate_utility(candidate: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    """Lexicographic evidence dimensions, not newest-rule priority.

    Dimensions: integrity, protected/context family, specificity, completeness,
    dictionary corroboration, confidence. The tuple is serialized for audit.
    """
    family = candidate["candidate_family"]
    dictionary = candidate.get("dictionary_evidence") or {}
    dictionary_support = 0
    if dictionary.get("matched"):
        type_counts = dictionary.get("dictionary_type_counts") or {}
        if family == "term":
            dictionary_support = min(80, 25 + 5 * int(type_counts.get("term", 0)) + 3 * int(type_counts.get("expression", 0)))
        elif family == "proper-name":
            dictionary_support = min(55, 15 + 5 * int(type_counts.get("name", 0)))
        elif family == "grammar":
            dictionary_support = min(45, 10 + 5 * int(type_counts.get("grammar", 0)))
        else:
            dictionary_support = 10
    protected = 100 if family == "punctuation" else (90 if family == "proper-name" else ROLE_ORDER.get(family, 0))
    confidence = int(round(float(candidate.get("confidence") or 0.0) * 100))
    return (100, protected, _specificity(candidate), _completeness(candidate), dictionary_support, confidence)


def _candidate_score(candidate: dict[str, Any]) -> int:
    # Score per covered character so splitting a range cannot manufacture extra
    # "integrity" points. Completeness/specificity then break equal-coverage ties.
    family = candidate["candidate_family"]
    if family == "unresolved":
        return 0
    u = candidate["utility_dimensions"]
    length = candidate["end"] - candidate["start"]
    per_char = u[1] * 1_000_000 + u[2] * 10_000 + u[4] * 100 + u[5]
    whole_span_bonus = u[3] * 1_000 + length
    return per_char * length + whole_span_bonus


def normalize_candidates(
    analysis: dict[str, Any],
    dictionary_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    text = analysis["text"]
    by_range = _dictionary_by_range(dictionary_result)
    out: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str, str | None, str | None]] = set()

    def add(item: dict[str, Any], family: str, role: str, *, source_layer: str,
            headword: str | None = None, grammar_id: str | None = None,
            confidence: float | None = None, protected: bool = False,
            component_ids: list[str] | None = None) -> None:
        if not _valid_range(text, item):
            return
        key = (item["start"], item["end"], role, headword, grammar_id)
        if key in seen:
            return
        seen.add(key)
        dsum = _dict_summary(by_range.get((item["start"], item["end"]), []))
        record = {
            "candidate_id": f"a34c{len(out)}",
            "start": item["start"], "end": item["end"], "surface": item["surface"],
            "proposed_role": role, "candidate_family": family,
            "headword": headword, "grammar_id": grammar_id,
            "confidence": float(confidence if confidence is not None else item.get("confidence") or 0.0),
            "protected": protected, "source_layer": source_layer,
            "source_annotation_id": item.get("id"),
            "morpheme_ids": component_ids or item.get("morpheme_ids") or [],
            "dictionary_evidence": dsum,
            "evidence": deepcopy(item.get("evidence") or []),
        }
        record["utility_dimensions"] = _candidate_utility(record)
        record["utility_score"] = _candidate_score(record)
        out.append(record)

    for item in analysis.get("orthographic_spans") or []:
        add(item, "punctuation", "punctuation", source_layer="orthography", confidence=1.0, protected=True)
    for item in analysis.get("person_references") or []:
        add(item, "proper-name", "proper-name", source_layer="person-references", headword=item.get("base_name") or item["surface"], confidence=item.get("confidence", .95), protected=True)
    for item in analysis.get("grammar_matches_alpha321") or analysis.get("grammar_matches_alpha32") or analysis.get("grammar_matches_alpha31") or []:
        add(item, "grammar", "grammar", source_layer="grammar", grammar_id=item.get("grammar_id"), confidence=item.get("confidence", .9))
    for item in analysis.get("numeral_expressions_alpha32") or []:
        add(item, "numeral", "term", source_layer="numeral", headword=item["surface"], confidence=item.get("confidence", .9))
    for item in analysis.get("discourse_connectives_alpha321") or analysis.get("discourse_connectives_alpha32") or []:
        add(item, "discourse", "term", source_layer="discourse", headword=item.get("headword") or item["surface"], confidence=item.get("confidence", .9))
    for item in analysis.get("lexical_items_alpha32") or analysis.get("lexical_items_alpha31") or []:
        family = "proper-name" if item.get("lexical_type") == "proper-name" else "term"
        add(item, family, "proper-name" if family == "proper-name" else "term", source_layer="lexical", headword=item.get("headword"), confidence=item.get("confidence", .8), protected=family == "proper-name")

    # Function/punctuation fallbacks come from immutable morphology and guarantee coverage.
    for m in analysis.get("morphemes") or []:
        if m.get("pos") in {"PUNCT", "SYM"} or str(m.get("tag") or "").startswith("補助記号"):
            add(m, "punctuation", "punctuation", source_layer="morphology-fallback", confidence=1.0, protected=True)
        elif m.get("pos") in {"ADP", "PART", "AUX", "SCONJ"}:
            add(m, "particle", "particle", source_layer="morphology-fallback", confidence=.8)

    return out


@dataclass(frozen=True)
class _Plan:
    score: int
    spans: tuple[dict[str, Any], ...]


def _better(left: _Plan, right: _Plan) -> _Plan:
    if left.score != right.score:
        return left if left.score > right.score else right
    # Stable tie-breakers: fewer fragments, then longer first span.
    if len(left.spans) != len(right.spans):
        return left if len(left.spans) < len(right.spans) else right
    left_lengths = tuple(-(x["end"] - x["start"]) for x in left.spans)
    right_lengths = tuple(-(x["end"] - x["start"]) for x in right.spans)
    return left if left_lengths <= right_lengths else right


def resolve_candidates(text: str, candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_start: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for c in candidates:
        by_start[c["start"]].append(c)

    # Explicit neutral fallback for every code point. It is never mistaken for evidence.
    for i, char in enumerate(text):
        fallback = {
            "candidate_id": f"a34fallback{i}", "start": i, "end": i + 1,
            "surface": char, "proposed_role": "unresolved", "candidate_family": "unresolved",
            "headword": None, "grammar_id": None, "confidence": 0.0, "protected": False,
            "source_layer": "coverage-fallback", "source_annotation_id": None,
            "morpheme_ids": [], "dictionary_evidence": {"matched": False}, "evidence": [],
            "utility_dimensions": (100, 0, 0, 0, 0, 0),
        }
        fallback["utility_score"] = _candidate_score(fallback)
        by_start[i].append(fallback)

    dp: list[_Plan | None] = [None] * (len(text) + 1)
    dp[len(text)] = _Plan(0, tuple())
    for pos in range(len(text) - 1, -1, -1):
        best: _Plan | None = None
        for candidate in by_start.get(pos, []):
            tail = dp[candidate["end"]]
            if tail is None:
                continue
            plan = _Plan(candidate["utility_score"] + tail.score, (candidate,) + tail.spans)
            best = plan if best is None else _better(best, plan)
        dp[pos] = best
    selected = list((dp[0] or _Plan(0, tuple())).spans)

    decisions: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for selected_candidate in selected:
        overlapping = [
            c for c in candidates
            if c["candidate_id"] != selected_candidate["candidate_id"]
            and c["start"] < selected_candidate["end"] and selected_candidate["start"] < c["end"]
        ]
        rejected = sorted({c["candidate_id"] for c in overlapping})
        policies = []
        if selected_candidate["candidate_family"] == "punctuation":
            policies.append("protected-orthography")
        if selected_candidate["candidate_family"] == "proper-name":
            policies.append("protected-person-reference")
        if selected_candidate["candidate_family"] == "grammar":
            policies.extend(["complete-contextual-construction", "grammar-specificity"])
        if (selected_candidate.get("dictionary_evidence") or {}).get("matched"):
            policies.append("dictionary-corroboration")
        if selected_candidate["candidate_family"] == "unresolved":
            policies.append("abstain-when-evidence-insufficient")
        decision = {
            "decision_id": f"a34d{len(decisions)}",
            "start": selected_candidate["start"], "end": selected_candidate["end"],
            "surface": selected_candidate["surface"],
            "selected_candidate_id": selected_candidate["candidate_id"],
            "selected_role": selected_candidate["proposed_role"],
            "selected_headword": selected_candidate.get("headword"),
            "selected_grammar_id": selected_candidate.get("grammar_id"),
            "rejected_candidate_ids": rejected,
            "decision_policies": policies,
            "utility_dimensions": selected_candidate["utility_dimensions"],
            "reason": _decision_reason(selected_candidate, overlapping),
            "confidence": selected_candidate.get("confidence", 0.0),
        }
        decisions.append(decision)
        if overlapping:
            conflicts.append({
                "conflict_id": f"a34x{len(conflicts)}",
                "start": selected_candidate["start"], "end": selected_candidate["end"],
                "surface": selected_candidate["surface"],
                "selected_candidate_id": selected_candidate["candidate_id"],
                "candidate_ids": [selected_candidate["candidate_id"]] + rejected,
                "resolved": selected_candidate["candidate_family"] != "unresolved",
                "resolution_policy": policies or ["evidence-utility"],
            })
    return selected, decisions, conflicts


def _decision_reason(selected: dict[str, Any], overlapping: list[dict[str, Any]]) -> str:
    family = selected["candidate_family"]
    if family == "punctuation":
        return "Orthographic punctuation is protected and cannot be crossed by lexical or grammar candidates."
    if family == "proper-name":
        return "A structurally supported person reference outranks component lexical proposals."
    if family == "grammar":
        return "The complete licensed contextual grammar construction outranks internal function or dictionary-valid fragments."
    if family == "term" and (selected.get("dictionary_evidence") or {}).get("matched"):
        return "Morphology and contextual lexical evidence are corroborated by independent dictionary evidence."
    if family == "term":
        return "The contextual lexical proposal is valid; dictionary absence is not treated as rejection."
    if family == "particle":
        return "Morphology identifies a contextual function element and no stronger complete construction covers the range."
    if family == "unresolved":
        return "No compatible evidence candidate was strong enough; the resolver abstains instead of guessing."
    return "Selected from compatible evidence using integrity, specificity, completeness, corroboration, and confidence."


def analyze_layered_alpha34(
    text: str,
    nlp,
    dictionary_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from .stabilization import analyze_layered_alpha321

    base = analyze_layered_alpha321(text, nlp)
    result = deepcopy(base)
    before = _snapshot_morphology(result.get("morphemes") or [])
    candidates = normalize_candidates(result, dictionary_result)
    selected, decisions, conflicts = resolve_candidates(text, candidates)
    resolved_spans = [
        {
            "start": c["start"], "end": c["end"], "surface": c["surface"],
            "role": c["proposed_role"], "headword": c.get("headword"),
            "grammar_id": c.get("grammar_id"), "confidence": c.get("confidence", 0.0),
            "selected_candidate_id": c["candidate_id"],
        }
        for c in selected
    ]
    diagnostics: list[dict[str, Any]] = []
    if before != _snapshot_morphology(result.get("morphemes") or []):
        diagnostics.append({"severity": "error", "code": "A34_MORPHOLOGY_MUTATED", "message": "Resolver changed Layer 0 morphology."})
    if "".join(x["surface"] for x in resolved_spans) != text:
        diagnostics.append({"severity": "error", "code": "A34_PROJECTION_INCOMPLETE", "message": "Resolved spans do not reconstruct source text."})
    cursor = 0
    for span in resolved_spans:
        if span["start"] != cursor or text[span["start"]:span["end"]] != span["surface"]:
            diagnostics.append({"severity": "error", "code": "A34_RANGE_INVALID", "message": f"Invalid resolved range at {cursor}."})
            break
        cursor = span["end"]

    result.update({
        "version": "8.0.0-alpha3.4-resolver",
        "dictionary_evidence_alpha34": dictionary_result or {
            "dictionary_ready": False, "evidence": [],
            "contract": {"evidence_only": True, "dictionary_miss_is_not_rejection": True},
        },
        "resolver_candidates_alpha34": candidates,
        "resolver_conflicts_alpha34": conflicts,
        "resolver_decisions_alpha34": decisions,
        "resolved_spans_alpha34": resolved_spans,
        "diagnostics_alpha34": diagnostics,
        "layer0_snapshot_alpha34": before,
        "alpha34_contract": {
            "non_destructive": True,
            "alpha321_preserved": True,
            "dictionary_is_evidence_only": True,
            "dictionary_miss_is_not_rejection": True,
            "only_resolved_spans_are_exclusive": True,
            "every_decision_is_explainable": True,
        },
    })
    return result
```

#### `app/analyzer/layers/dictionary.py`

```python
from __future__ import annotations

import json
import sqlite3
import unicodedata
from collections import Counter
from typing import Any, Iterable

from .dictionary_store import DB_PATH

# Dictionary types remain evidence dimensions. They never become final roles here.
KNOWN_TYPES = ("term", "expression", "name", "grammar", "frequency", "unknown")


def normalize_lookup_text(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value or "")).strip()


def _connect_readonly() -> sqlite3.Connection:
    # The sync step creates the DB. Opening normally also makes the evidence endpoint
    # return a clean not-ready result if the cache was cleared.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    return con


def dictionary_ready() -> bool:
    if not DB_PATH.exists():
        return False
    try:
        with _connect_readonly() as con:
            row = con.execute(
                "SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='lexicon_entries'"
            ).fetchone()
            if not row or not row["n"]:
                return False
            count = con.execute("SELECT COUNT(*) AS n FROM lexicon_entries").fetchone()["n"]
            return count > 0
    except sqlite3.Error:
        return False


def _query_form(con: sqlite3.Connection, form: str, limit: int) -> list[dict[str, Any]]:
    rows = con.execute(
        """
        SELECT id, dictionary_id, dictionary_title, dictionary_type,
               dictionary_priority, term, reading, tags_json, rules_json,
               score, sequence, name_type, grammar_type, expression_type
        FROM lexicon_entries
        WHERE term = ?
        ORDER BY dictionary_priority ASC, score DESC, id ASC
        LIMIT ?
        """,
        (form, limit),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        for key in ("tags_json", "rules_json"):
            try:
                item[key[:-5]] = json.loads(item.pop(key) or "[]")
            except (TypeError, json.JSONDecodeError):
                item[key[:-5]] = []
        out.append(item)
    return out


def _candidate_lookup_forms(candidate: dict[str, Any]) -> list[dict[str, str]]:
    raw = candidate.get("lookup_forms") or candidate.get("lookupForms") or []
    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(value: Any, kind: str) -> None:
        text = normalize_lookup_text(value)
        if text and text not in seen:
            seen.add(text)
            out.append({"text": text, "type": kind})

    # Candidate surface is always first, followed by analyzer-provided forms.
    add(candidate.get("surface"), "surface")
    for index, value in enumerate(raw):
        if isinstance(value, dict):
            add(value.get("text") or value.get("value"), str(value.get("type") or "analyzer-form"))
        else:
            add(value, "surface" if index == 0 else "analyzer-form")
    add(candidate.get("lemma"), "lemma")
    add(candidate.get("normalized"), "normalized")
    return out


def _pos_compatibility(parser_pos: str | None, entries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Conservative compatibility signal; never rejects a candidate.

    Yomitan tags/rules differ by dictionary. This method only emits positive or
    conflicting hints when recognizable markers are present. Unknown is normal.
    """
    pos = str(parser_pos or "").upper()
    markers = " ".join(
        str(value).lower()
        for entry in entries
        for value in (*entry.get("tags", []), *entry.get("rules", []), entry.get("name_type", ""), entry.get("grammar_type", ""))
        if value
    )
    families = {
        "VERB": ("verb", "v1", "v5", "vs", "vk", "vz"),
        "NOUN": ("noun", "n", "n-", "名詞"),
        "PROPN": ("name", "proper", "surname", "given", "人名"),
        "ADJ": ("adj", "形容"),
        "ADV": ("adv", "副詞"),
        "PRON": ("pron", "代名詞"),
        "NUM": ("num", "numeric", "数詞"),
    }
    expected = families.get(pos)
    if not pos or not expected or not markers:
        return {"status": "unknown", "parserPos": parser_pos, "reason": "Insufficient normalized POS metadata"}
    compatible = any(marker in markers for marker in expected)
    return {
        "status": "compatible" if compatible else "unknown",
        "parserPos": parser_pos,
        "reason": "Recognized dictionary POS/rule marker" if compatible else "No contradictory normalized marker was asserted",
    }


def evaluate_candidate(
    candidate: dict[str, Any],
    parser_pos: str | None = None,
    per_form_limit: int = 250,
) -> dict[str, Any]:
    candidate_id = str(candidate.get("id") or candidate.get("candidate_id") or candidate.get("candidateId") or "")
    forms = _candidate_lookup_forms(candidate)
    attempts: list[dict[str, Any]] = []
    all_entries: list[dict[str, Any]] = []
    selected_form: dict[str, str] | None = None

    if not dictionary_ready():
        return {
            "candidate_id": candidate_id,
            "start": candidate.get("start"),
            "end": candidate.get("end"),
            "surface": candidate.get("surface", ""),
            "matched": False,
            "dictionary_ready": False,
            "lookup_attempts": [],
            "selected_lookup_form": None,
            "match_type": "dictionary-not-ready",
            "entry_count": 0,
            "independent_source_count": 0,
            "dictionary_type_counts": {},
            "matched_headwords": [],
            "source_names": [],
            "pos_compatibility": {"status": "unknown", "parserPos": parser_pos},
            "confidence": None,
            "meaning": "Dictionary cache is unavailable; this is not a candidate rejection.",
        }

    with _connect_readonly() as con:
        for form in forms:
            entries = _query_form(con, form["text"], per_form_limit)
            attempts.append({
                "form": form["text"],
                "form_type": form["type"],
                "match_count": len(entries),
            })
            if entries and selected_form is None:
                selected_form = form
            all_entries.extend(entries)

    # Deduplicate a source entry found through more than one equivalent lookup form.
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for entry in all_entries:
        key = (
            entry.get("dictionary_id"), entry.get("term"), entry.get("reading"),
            entry.get("sequence"), entry.get("dictionary_type"), entry.get("id"),
        )
        unique[key] = entry
    entries = list(unique.values())

    type_counts = Counter(str(e.get("dictionary_type") or "unknown") for e in entries)
    sources = sorted({str(e.get("dictionary_title") or "unknown") for e in entries})
    source_ids = {str(e.get("dictionary_id") or e.get("dictionary_title") or "unknown") for e in entries}
    headwords = sorted({str(e.get("term") or "") for e in entries if e.get("term")})
    pos_signal = _pos_compatibility(parser_pos, entries)

    matched = bool(entries)
    if matched and selected_form:
        match_type = f"{selected_form['type']}-exact"
        # Confidence is evidence strength only, not final sentence confidence.
        source_strength = min(1.0, 0.65 + 0.08 * len(source_ids))
        type_bonus = 0.05 if type_counts.get("term") or type_counts.get("expression") else 0.0
        pos_bonus = 0.05 if pos_signal.get("status") == "compatible" else 0.0
        confidence = round(min(0.99, source_strength + type_bonus + pos_bonus), 3)
    else:
        match_type = "none"
        confidence = None

    # Entry details are deliberately compact; no definitions/glossary content.
    compact_entries = [
        {
            "dictionary_id": e.get("dictionary_id"),
            "dictionary_title": e.get("dictionary_title"),
            "dictionary_type": e.get("dictionary_type"),
            "dictionary_priority": e.get("dictionary_priority"),
            "term": e.get("term"),
            "reading": e.get("reading"),
            "tags": e.get("tags", []),
            "rules": e.get("rules", []),
            "score": e.get("score"),
            "sequence": e.get("sequence"),
            "name_type": e.get("name_type"),
            "grammar_type": e.get("grammar_type"),
            "expression_type": e.get("expression_type"),
        }
        for e in entries[:100]
    ]

    return {
        "candidate_id": candidate_id,
        "start": candidate.get("start"),
        "end": candidate.get("end"),
        "surface": candidate.get("surface", ""),
        "candidate_type": candidate.get("candidate_type"),
        "matched": matched,
        "dictionary_ready": True,
        "lookup_attempts": attempts,
        "selected_lookup_form": selected_form["text"] if selected_form else None,
        "selected_lookup_form_type": selected_form["type"] if selected_form else None,
        "match_type": match_type,
        "entry_count": len(entries),
        "independent_source_count": len(source_ids),
        "dictionary_type_counts": dict(type_counts),
        "matched_headwords": headwords,
        "source_names": sources,
        "pos_compatibility": pos_signal,
        "confidence": confidence,
        "entries": compact_entries,
        "meaning": "Positive dictionary evidence" if matched else "No positive dictionary evidence; this is not a candidate rejection.",
    }


def _parser_pos_for_candidate(candidate: dict[str, Any], morphemes: list[dict[str, Any]]) -> str | None:
    a, b = candidate.get("start"), candidate.get("end")
    covered = [m for m in morphemes if m.get("start", -1) >= a and m.get("end", -1) <= b]
    if len(covered) == 1:
        return covered[0].get("pos")
    lexical = [m for m in covered if m.get("pos") in {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}]
    return lexical[-1].get("pos") if lexical else None


def evaluate_analysis_candidates(analysis: dict[str, Any]) -> dict[str, Any]:
    candidates = (
        analysis.get("dictionary_candidates_alpha31")
        or analysis.get("dictionary_candidates_alpha3")
        or analysis.get("dictionary_candidates")
        or []
    )
    morphemes = analysis.get("morphemes") or []
    evidence = [
        evaluate_candidate(candidate, _parser_pos_for_candidate(candidate, morphemes))
        for candidate in candidates
    ]
    matched = [item for item in evidence if item.get("matched")]
    by_type = Counter()
    for item in matched:
        by_type.update(item.get("dictionary_type_counts") or {})
    return {
        "dictionary_ready": dictionary_ready(),
        "candidate_count": len(candidates),
        "matched_candidate_count": len(matched),
        "unmatched_candidate_count": len(candidates) - len(matched),
        "dictionary_type_evidence_counts": dict(by_type),
        "evidence": evidence,
        "contract": {
            "evidence_only": True,
            "morphology_unchanged": True,
            "grammar_unchanged": True,
            "entities_unchanged": True,
            "reader_projection_unchanged": True,
            "dictionary_miss_is_not_rejection": True,
        },
    }
```

#### `app/analyzer/layers/dictionary_store.py`

```python
from __future__ import annotations
import json, sqlite3, threading, uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[3] / "data" / "phase8_analysis_lexicon.sqlite3"
_lock = threading.RLock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_sessions(sync_id TEXT PRIMARY KEY, expected_entries INTEGER DEFAULT 0, received_entries INTEGER DEFAULT 0, dictionary_count INTEGER DEFAULT 0, status TEXT DEFAULT 'receiving');
CREATE TABLE IF NOT EXISTS staging_entries(sync_id TEXT NOT NULL, dictionary_id TEXT NOT NULL, dictionary_title TEXT NOT NULL, dictionary_type TEXT NOT NULL, dictionary_priority INTEGER NOT NULL DEFAULT 9999, term TEXT NOT NULL, reading TEXT NOT NULL DEFAULT '', tags_json TEXT NOT NULL DEFAULT '[]', rules_json TEXT NOT NULL DEFAULT '[]', score REAL NOT NULL DEFAULT 0, sequence TEXT, name_type TEXT NOT NULL DEFAULT '', grammar_type TEXT NOT NULL DEFAULT '', expression_type TEXT NOT NULL DEFAULT '');
CREATE INDEX IF NOT EXISTS idx_staging_sync ON staging_entries(sync_id);
CREATE TABLE IF NOT EXISTS lexicon_entries(id INTEGER PRIMARY KEY AUTOINCREMENT, dictionary_id TEXT NOT NULL, dictionary_title TEXT NOT NULL, dictionary_type TEXT NOT NULL, dictionary_priority INTEGER NOT NULL DEFAULT 9999, term TEXT NOT NULL, reading TEXT NOT NULL DEFAULT '', tags_json TEXT NOT NULL DEFAULT '[]', rules_json TEXT NOT NULL DEFAULT '[]', score REAL NOT NULL DEFAULT 0, sequence TEXT, name_type TEXT NOT NULL DEFAULT '', grammar_type TEXT NOT NULL DEFAULT '', expression_type TEXT NOT NULL DEFAULT '');
CREATE INDEX IF NOT EXISTS idx_lexicon_term ON lexicon_entries(term);
CREATE INDEX IF NOT EXISTS idx_lexicon_reading ON lexicon_entries(reading);
CREATE INDEX IF NOT EXISTS idx_lexicon_type ON lexicon_entries(dictionary_type);
CREATE TABLE IF NOT EXISTS lexicon_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.executescript(SCHEMA)
    return con

@contextmanager
def _db():
    """Commit/rollback and always release the SQLite file handle."""
    con = _connect()
    try:
        with con:
            yield con
    finally:
        con.close()

def start_sync(expected_entries: int = 0, dictionary_count: int = 0) -> dict[str, Any]:
    sync_id = str(uuid.uuid4())
    with _lock, _db() as con:
        con.execute("DELETE FROM staging_entries")
        con.execute("DELETE FROM sync_sessions")
        con.execute("INSERT INTO sync_sessions(sync_id,expected_entries,dictionary_count) VALUES(?,?,?)", (sync_id, expected_entries, dictionary_count))
    return {"syncId": sync_id, "status": "receiving", "database": str(DB_PATH)}

def add_batch(sync_id: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    def j(value):
        return json.dumps(value if isinstance(value, list) else ([value] if value else []), ensure_ascii=False)
    rows = []
    for entry in entries:
        term = str(entry.get("term") or "").strip()
        if not term:
            continue
        rows.append((sync_id, str(entry.get("dictionaryId") or ""), str(entry.get("dictionaryTitle") or "unknown"), str(entry.get("dictionaryType") or "term"), int(entry.get("dictionaryPriority") or 9999), term, str(entry.get("reading") or ""), j(entry.get("tags")), j(entry.get("rules")), float(entry.get("score") or 0), None if entry.get("sequence") is None else str(entry.get("sequence")), str(entry.get("nameType") or ""), str(entry.get("grammarType") or ""), str(entry.get("expressionType") or "")))
    with _lock, _db() as con:
        session = con.execute("SELECT status FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone()
        if not session or session["status"] != "receiving":
            raise ValueError("Unknown or inactive sync session")
        con.executemany("INSERT INTO staging_entries VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        con.execute("UPDATE sync_sessions SET received_entries=received_entries+? WHERE sync_id=?", (len(rows), sync_id))
        received = con.execute("SELECT received_entries FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone()[0]
    return {"syncId": sync_id, "accepted": len(rows), "received": received}

def finish_sync(sync_id: str) -> dict[str, Any]:
    with _lock, _db() as con:
        if not con.execute("SELECT 1 FROM sync_sessions WHERE sync_id=?", (sync_id,)).fetchone():
            raise ValueError("Unknown sync session")
        con.execute("DELETE FROM lexicon_entries")
        con.execute("""INSERT INTO lexicon_entries(dictionary_id,dictionary_title,dictionary_type,dictionary_priority,term,reading,tags_json,rules_json,score,sequence,name_type,grammar_type,expression_type) SELECT dictionary_id,dictionary_title,dictionary_type,dictionary_priority,term,reading,tags_json,rules_json,score,sequence,name_type,grammar_type,expression_type FROM staging_entries WHERE sync_id=?""", (sync_id,))
        count = con.execute("SELECT COUNT(*) FROM lexicon_entries").fetchone()[0]
        dictionaries = con.execute("SELECT COUNT(DISTINCT dictionary_id) FROM lexicon_entries").fetchone()[0]
        con.execute("DELETE FROM lexicon_meta")
        con.executemany("INSERT INTO lexicon_meta(key,value) VALUES(?,?)", [("last_sync_id", sync_id), ("entry_count", str(count)), ("dictionary_count", str(dictionaries))])
        con.execute("UPDATE sync_sessions SET status='complete' WHERE sync_id=?", (sync_id,))
        con.execute("DELETE FROM staging_entries WHERE sync_id=?", (sync_id,))
    return {"syncId": sync_id, "status": "complete", "entryCount": count, "dictionaryCount": dictionaries}

def status() -> dict[str, Any]:
    with _lock, _db() as con:
        count = con.execute("SELECT COUNT(*) FROM lexicon_entries").fetchone()[0]
        dictionaries = con.execute("SELECT COUNT(DISTINCT dictionary_id) FROM lexicon_entries").fetchone()[0]
        types = {r["dictionary_type"]: r["n"] for r in con.execute("SELECT dictionary_type,COUNT(*) n FROM lexicon_entries GROUP BY dictionary_type")}
        last = con.execute("SELECT value FROM lexicon_meta WHERE key='last_sync_id'").fetchone()
    return {"ready": count > 0, "entryCount": count, "dictionaryCount": dictionaries, "typeCounts": types, "lastSyncId": last[0] if last else None, "database": str(DB_PATH)}

def clear() -> dict[str, Any]:
    with _lock, _db() as con:
        for table in ("lexicon_entries", "staging_entries", "sync_sessions", "lexicon_meta"):
            con.execute(f"DELETE FROM {table}")
    return status()
```

#### `app/analyzer/layers/dictionary_api.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .dictionary_store import start_sync, add_batch, finish_sync, status, clear
router = APIRouter(prefix="/dictionary-sync", tags=["dictionary-sync"])
class StartRequest(BaseModel):
    expectedEntries: int = 0
    dictionaryCount: int = 0
class Entry(BaseModel):
    term: str
    reading: str = ""
    dictionaryId: str = ""
    dictionaryTitle: str = "unknown"
    dictionaryType: str = "term"
    dictionaryPriority: int = 9999
    tags: list[str] = Field(default_factory=list)
    rules: list[str] | str = Field(default_factory=list)
    score: float = 0
    sequence: str | int | None = None
    nameType: str = ""
    grammarType: str = ""
    expressionType: str = ""
class BatchRequest(BaseModel):
    syncId: str
    entries: list[Entry]
class FinishRequest(BaseModel):
    syncId: str
@router.post("/start")
def start(req: StartRequest): return start_sync(req.expectedEntries, req.dictionaryCount)
@router.post("/batch")
def batch(req: BatchRequest):
    try: return add_batch(req.syncId, [e.model_dump() for e in req.entries])
    except ValueError as exc: raise HTTPException(409, str(exc))
@router.post("/finish")
def finish(req: FinishRequest):
    try: return finish_sync(req.syncId)
    except ValueError as exc: raise HTTPException(409, str(exc))
@router.get("/status")
def get_status(): return status()
@router.delete("/cache")
def delete_cache(): return clear()
```

#### `app/analyzer/layers/dictionary_evidence_api.py`

```python
from __future__ import annotations

from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from .dictionary import evaluate_analysis_candidates, evaluate_candidate

router = APIRouter(prefix="/dictionary-evidence", tags=["dictionary-evidence"])


class CandidateRequest(BaseModel):
    candidate: dict[str, Any]
    parserPos: str | None = None


class AnalysisRequest(BaseModel):
    analysis: dict[str, Any]


@router.post("/candidate")
def candidate(req: CandidateRequest):
    return evaluate_candidate(req.candidate, req.parserPos)


@router.post("/analysis")
def analysis(req: AnalysisRequest):
    return evaluate_analysis_candidates(req.analysis)
```

#### `requirements.txt`

```text
fastapi==0.116.1
uvicorn[standard]==0.35.0
sudachipy>=0.6.11,<0.7
sudachidict_core>=20250129
spacy>=3.8,<3.9
ginza==5.2.0
ja_ginza==5.2.0
pydantic>=2.11,<3
```

#### `requirements-kwja-py311.txt`

```text
kwja==2.5.1
pure-cdb==4.0.0
torch==2.7.1
transformers==4.50.3
tokenizers==0.21.4
safetensors==0.8.0
sentencepiece==0.2.1
protobuf==7.35.1
```

#### `run_tests.ps1`

```powershell
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$env:PYTHONPATH = $PSScriptRoot
$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw "Python not found: $Python" }
$Tests = Get-ChildItem ".\tests\test_*.py" | Sort-Object Name
foreach ($Test in $Tests) {
    Write-Host "Running $($Test.Name)" -ForegroundColor Cyan
    & $Python $Test.FullName
    if ($LASTEXITCODE -ne 0) { throw "Test failed: $($Test.Name)" }
}
& $Python -m compileall -q ".\app\analyzer"
if ($LASTEXITCODE -ne 0) { throw "Analyzer compilation failed" }
Write-Host "All consolidated analyzer tests passed." -ForegroundColor Green
```

### Critical Novel Audio Miner integration files — full contents

#### `package.json`

```json
{
  "name": "novel-audio-miner",
  "private": true,
  "version": "4.1.0",
  "type": "module",
  "description": "Local Japanese EPUB reader and Anki mining helper.",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "6.0.3",
    "jszip": "3.10.1",
    "kuromoji": "0.1.2",
    "react": "19.2.7",
    "react-dom": "19.2.7",
    "vite": "8.1.3"
  }
}
```

#### `src/components/Reader.jsx`

```jsx
import { useEffect, useMemo, useState, useRef } from 'react';
import { getProgress, saveProgress } from '../lib/storage.js';
import { checkAnkiConnect, findLatestNote, updateNoteFields, ankiRequest } from '../lib/ankiConnect.js';
import { autoEnrichWordWithFallback, generateVoicevoxAudio } from '../lib/enrichService.js';
import { buildCache, clearCache, getCacheSize, addKnownWord, addManualKnownWord, removeManualKnownWord, isManualKnownWord, isKnownWord } from '../lib/wordCache.js';
import { getFrequency, startLoadingGlobalFrequency } from '../lib/frequencyMap.js';
import DictionaryDebugPanel from './DictionaryDebugPanel.jsx';
import JpAnalyzerIntegrationPanel from './JpAnalyzerIntegrationPanel.jsx';
import {
  clearJpAnalyzerShadowCache,
  useJpAnalyzerShadow
} from '../lib/useJpAnalyzerShadow.js';
import { adaptCompactAnalysisToReaderWords } from '../lib/analyzerWordAdapter.js';
import { compareReaderWordModels } from '../lib/analyzerShadowComparison.js';

/* ─── Constants ─── */
const DEFAULT_STYLE = { fontSize: 30, lineHeight: 2.05, height: 620, fontFamily: 'mincho' };
const DEFAULT_FIELDS = {
  expressionAudio: 'ExpressionAudio', selectionText: 'SelectionText',
  sentence: 'Sentence', sentenceFurigana: 'SentenceFurigana',
  sentenceAudio: 'SentenceAudio', picture: 'Picture', miscInfo: 'MiscInfo'
};
const FONT_STACKS = {
  mincho: '"Hiragino Mincho ProN","Yu Mincho","YuMincho","Noto Serif CJK JP","Noto Serif JP","Source Han Serif JP","IPAexMincho","Meiryo",serif',
  gothic: '"Hiragino Kaku Gothic ProN","Yu Gothic","YuGothic","Noto Sans CJK JP","Noto Sans JP","Source Han Sans JP","Meiryo",sans-serif'
};

function clamp(n, min, max) { return Math.max(min, Math.min(max, n)); }
function cleanBookTitle(title) {
  return String(title || '').replace(/[（(]\s*電撃文庫\s*[）)]/g, '').replace(/【[^】]*(電子|特典|限定|版)[^】]*】/g, '').replace(/\s+/g, ' ').trim();
}

const dashRegex = /[—―─━ー]/;
const dashSingleRegex = /[—―─━ー]/g;

function fixDashesInHtml(html) {
  try { const div = document.createElement('div'); div.innerHTML = html; wrapIndividualDashes(div); return div.innerHTML; }
  catch { return html.replace(dashSingleRegex, '<span class="vertical-dash-fix">$&</span>'); }
}
function wrapIndividualDashes(node) {
  if (node.nodeType === Node.TEXT_NODE) {
    const text = node.textContent;
    if (!dashRegex.test(text)) return;
    const frag = document.createDocumentFragment();
    let lastIdx = 0, match;
    dashSingleRegex.lastIndex = 0;
    while ((match = dashSingleRegex.exec(text)) !== null) {
      if (match.index > lastIdx) frag.appendChild(document.createTextNode(text.slice(lastIdx, match.index)));
      const span = document.createElement('span'); span.className = 'vertical-dash-fix'; span.textContent = match[0];
      frag.appendChild(span);
      lastIdx = dashSingleRegex.lastIndex;
    }
    if (lastIdx < text.length) frag.appendChild(document.createTextNode(text.slice(lastIdx)));
    node.parentNode.replaceChild(frag, node);
  } else if (node.nodeType === Node.ELEMENT_NODE && !['SCRIPT', 'STYLE'].includes(node.tagName)) {
    for (let i = node.childNodes.length - 1; i >= 0; i--) wrapIndividualDashes(node.childNodes[i]);
  }
}

/* ─── Word colour logic ─── */
function getTokenKnownKey(tokenOrWord) {
  if (typeof tokenOrWord === 'string') return tokenOrWord;
  return tokenOrWord?.dictionaryForm || tokenOrWord?.surface || '';
}

function isTokenKnownForLearning(tokenOrWord) {
  return isKnownWord(getTokenKnownKey(tokenOrWord));
}

function getWordColorClass(wordOrToken) {
  const token = typeof wordOrToken === 'object' ? wordOrToken : null;
  const word = getTokenKnownKey(wordOrToken);
  if (token?.colorRole === 'name' || token?.tokenCategory === 'proper-noun') return 'word-name';
  if (token?.colorRole === 'numeric' || token?.tokenCategory === 'numeric') return 'word-numeric';
  if (token?.colorRole === 'grammar' || token?.tokenCategory === 'grammar' || token?.tokenCategory === 'ignored') return 'word-grammar';
  if (!word) return 'word-unknown word-freq-unlisted';
  if (isKnownWord(word)) return 'word-known';
  const freq = getFrequency(word);
  if (freq && freq.category) return `word-unknown word-freq-${freq.category}`;
  return 'word-unknown word-freq-unlisted';       // grey
}


function yesNo(value) { return value ? 'yes' : 'no'; }
function truncateDebugText(text, maxLength = 80) {
  const source = String(text || '').replace(/[\n\r\t]+/g, ' ').replace(/\s+/g, ' ').trim();
  return source.length <= maxLength ? source : `${source.slice(0, maxLength)}...`;
}
function safeJson(value) { try { return JSON.stringify(value ?? null, null, 2); } catch { return String(value || ''); } }
function getDisplayItemData(displayItem) { return displayItem?.data || displayItem || null; }
function getDisplayItemType(displayItem) {
  if (!displayItem) return 'none';
  if (displayItem.type === 'illustration') return 'image';
  if (displayItem.type === 'scene') return 'sentence';
  return displayItem.type || getDisplayItemData(displayItem)?.type || 'unknown';
}
function getDisplayItemPreview(displayItem) {
  const data = getDisplayItemData(displayItem);
  if (!data) return '';
  if (getDisplayItemType(displayItem) === 'image') return data.alt || '[image]';
  return truncateDebugText(data.plainText || data.htmlText || '', 90);
}
function getDebugTokenRows(currentData) {
  if (!currentData || currentData.type === 'image') return [];
  const sourceTokens = (currentData.classifiedWords && currentData.classifiedWords.length) ? currentData.classifiedWords : (currentData.tokens || []);
  return sourceTokens.map((token, index) => {
    const key = getTokenKnownKey(token);
    const freq = key ? getFrequency(key) : null;
    return {
      index, surface: token.surface || '', dictionaryForm: token.dictionaryForm || token.surface || '',
      pos: token.pos || '', posDetail1: token.posDetail1 || '', posDetail2: token.posDetail2 || '', posDetail3: token.posDetail3 || '',
      tokenCategory: token.tokenCategory || '', colorRole: token.colorRole || '', colorClass: getWordColorClass(token),
      known: key ? isKnownWord(key) : false, manualKnown: key ? isManualKnownWord(key) : false,
      frequency: freq ? `${freq.rank} / ${freq.category}` : 'unlisted',
      countsForComprehension: Boolean(token.countsForComprehension), showInNewWords: Boolean(token.showInNewWords)
    };
  });
}
function getSceneDebugSummary({ currentData, displayItem, itemIndex, totalScenes, isText, isImage, selectedText, unknownWords, comprehension, currentChapterImages }) {
  if (!currentData) return [];
  return [
    ['scene', `${itemIndex + 1} / ${totalScenes}`], ['displayItemType', getDisplayItemType(displayItem)], ['dataType', currentData.type || (isImage ? 'image' : 'sentence')],
    ['isText', yesNo(isText)], ['isImage', yesNo(isImage)], ['chapter', currentData.chapterTitle || ''], ['chapterIndex', String(currentData.chapterIndex ?? '')],
    ['selectedText', selectedText || ''], ['unknownWords', String((unknownWords || []).length)], ['comprehension', comprehension ? `${comprehension.percent}% (${comprehension.known}/${comprehension.total})` : 'n/a'],
    ['plainTextLength', String((currentData.plainText || '').length)], ['htmlTextLength', String((currentData.htmlText || '').length)], ['tokens', String((currentData.tokens || []).length)],
    ['classifiedWords', String((currentData.classifiedWords || []).length)], ['displayWords', String((currentData.displayWords || []).length)], ['comprehensionWords', String((currentData.comprehensionWords || []).length)],
    ['miningCandidates', String((currentData.miningCandidates || []).length)], ['chapterImages', String((currentChapterImages || []).length)], ['imageAlt', isImage ? (currentData.alt || '') : ''], ['imageDataUri', isImage ? yesNo(Boolean(currentData.dataUri)) : '']
  ];
}
function getNearbySceneRows(displayItems, itemIndex) {
  const rows = [];
  for (let offset = -2; offset <= 2; offset += 1) {
    const index = itemIndex + offset;
    if (index < 0 || index >= displayItems.length) continue;
    const displayItem = displayItems[index]; const data = getDisplayItemData(displayItem);
    rows.push({ index, relative: offset === 0 ? 'current' : (offset > 0 ? `+${offset}` : String(offset)), type: getDisplayItemType(displayItem), chapterIndex: data?.chapterIndex ?? '', chapterTitle: data?.chapterTitle || '', preview: getDisplayItemPreview(displayItem), parserDebug: data?.parserDebug || null });
  }
  return rows;
}
function getMiningDebugRows(miningDebug) {
  if (!miningDebug) return [];
  return [['status', miningDebug.status || ''], ['stage', miningDebug.stage || ''], ['startedAt', miningDebug.startedAt || ''], ['updatedAt', miningDebug.updatedAt || ''], ['selectedWord', miningDebug.selectedWord || ''], ['noteType', miningDebug.noteType || ''], ['scene', miningDebug.scene || ''], ['chapter', miningDebug.chapterTitle || ''], ['latestNoteQuery', miningDebug.latestNoteQuery || ''], ['latestNoteId', miningDebug.latestNoteId ? String(miningDebug.latestNoteId) : ''], ['latestNoteCount', miningDebug.latestNoteCount != null ? String(miningDebug.latestNoteCount) : ''], ['enrichmentMethod', miningDebug.enrichmentMethod || ''], ['source', miningDebug.source || ''], ['mode', miningDebug.mode || ''], ['unknownCount', miningDebug.unknownCount != null ? String(miningDebug.unknownCount) : ''], ['hasAudioUrl', miningDebug.hasAudioUrl != null ? yesNo(miningDebug.hasAudioUrl) : ''], ['hasImageUrl', miningDebug.hasImageUrl != null ? yesNo(miningDebug.hasImageUrl) : ''], ['sentenceAudio', miningDebug.sentenceAudio || ''], ['picture', miningDebug.picture || ''], ['error', miningDebug.error || '']];
}
function getParserDebugRows(currentData, displayItem, book) {
  const data = currentData || getDisplayItemData(displayItem) || {}; const parser = data.parserDebug || {}; const bookDebug = book?.debug || {};
  return [['bookDebugAvailable', yesNo(Boolean(bookDebug && Object.keys(bookDebug).length))], ['tocCount', String(bookDebug.tocCount ?? '')], ['totalItems', String(bookDebug.totalItems ?? '')], ['sentenceCount', String(bookDebug.sentenceCount ?? '')], ['imageCount', String(bookDebug.imageCount ?? '')], ['pageHref', parser.pageHref || ''], ['pageIndex', parser.pageIndex != null ? String(parser.pageIndex) : ''], ['orderedIndex', parser.orderedIndex != null ? String(parser.orderedIndex) : ''], ['itemType', parser.itemType || getDisplayItemType(displayItem)], ['chapterIndex', parser.chapterIndex != null ? String(parser.chapterIndex) : String(data.chapterIndex ?? '')], ['chapterTitle', parser.chapterTitle || data.chapterTitle || ''], ['imageSrc', parser.imageSrc || ''], ['resolvedZipPath', parser.resolvedZipPath || ''], ['imageExists', parser.imageExists != null ? yesNo(parser.imageExists) : ''], ['dataUri', parser.hasDataUri != null ? yesNo(parser.hasDataUri) : yesNo(Boolean(data.dataUri))], ['alt', parser.alt || data.alt || ''], ['plainTextLength', parser.plainTextLength != null ? String(parser.plainTextLength) : String((data.plainText || '').length)], ['htmlTextLength', parser.htmlTextLength != null ? String(parser.htmlTextLength) : String((data.htmlText || '').length)]];
}
function getChapterDebugRows(book, chapterImageLists) {
  const chapters = book?.debug?.chapterList || [];
  return chapters.map((chapter, index) => ({ index, title: chapter.title || '', sentenceCount: chapter.sentenceCount ?? '', imageCount: chapter.imageCount ?? (chapterImageLists?.[index]?.length ?? 0), preview: chapter.preview || '' }));
}
function buildDebugReport({ book, itemIndex, totalScenes, currentData, currentDisplayItem, selectedText, comprehension, unknownWords, debugTokenRows, debugSceneRows, debugNearbyRows, parserDebugRows, chapterDebugRows, miningDebug, ankiStatus, globalFreqReady, forceTts, readerStyle, showFurigana, verticalMode }) {
  return { app: { name: 'Novel Audio Miner', debugVersion: 'v5-export-report', generatedAt: new Date().toISOString() }, book: { id: book?.id || '', fileName: book?.fileName || '', title: book?.title || '', author: book?.author || '', tocCount: book?.toc?.length || 0, chapterCount: book?.chapters?.length || 0, debug: book?.debug || null }, reader: { sceneIndex: itemIndex, sceneNumber: itemIndex + 1, totalScenes, selectedText: selectedText || '', showFurigana: Boolean(showFurigana), verticalMode: Boolean(verticalMode), readerStyle, ankiStatus, globalFreqReady: Boolean(globalFreqReady), forceTts: Boolean(forceTts) }, currentScene: { displayItemType: getDisplayItemType(currentDisplayItem), chapterIndex: currentData?.chapterIndex ?? null, chapterTitle: currentData?.chapterTitle || '', plainText: currentData?.plainText || '', htmlText: currentData?.htmlText || '', imageAlt: currentData?.alt || '', hasImageDataUri: Boolean(currentData?.dataUri), parserDebug: currentData?.parserDebug || null }, comprehension: comprehension || null, unknownWords: (unknownWords || []).map(item => ({ word: item.word || '', surface: item.surface || '', frequency: item.freq || null })), debugPanels: { sceneRows: debugSceneRows, tokenRows: debugTokenRows, nearbyRows: debugNearbyRows, parserRows: parserDebugRows, chapterRows: chapterDebugRows, mining: miningDebug || null } };
}
function downloadJsonFile(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' }); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = filename; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
}

/* ─── Stable token range colouriser ─── */
function normalizeTokenList(tokens) {
  return (tokens || [])
    .filter(token => token?.surface)
    .map(token => ({ ...token, surface: String(token.surface || ''), dictionaryForm: String(token.dictionaryForm || token.surface || '') }))
    .filter(token => token.surface.length > 0)
    .sort((a, b) => b.surface.length - a.surface.length);
}

function buildTokenRangesFromText(text, tokens) {
  const source = text || '';
  const normalized = normalizeTokenList(tokens);
  const ranges = [];
  const occupied = new Array(source.length).fill(false);
  for (const token of normalized) {
    let searchFrom = 0;
    while (searchFrom < source.length) {
      const start = source.indexOf(token.surface, searchFrom);
      if (start === -1) break;
      const end = start + token.surface.length;
      const overlaps = occupied.slice(start, end).some(Boolean);
      if (!overlaps) {
        for (let i = start; i < end; i++) occupied[i] = true;
        ranges.push({ start, end, className: getWordColorClass(token), surface: token.surface });
        break;
      }
      searchFrom = start + 1;
    }
  }
  return ranges.sort((a, b) => a.start - b.start || b.end - a.end);
}

function renderTextFragment(text, verticalMode, keyPrefix) {
  if (!verticalMode) return text;
  return renderChars(text, true, keyPrefix);
}

function renderColorizedPlainText(text, tokens, verticalMode) {
  const source = text || '';
  if (!source) return '';
  const ranges = buildTokenRangesFromText(source, tokens);
  if (!ranges.length) return renderTextFragment(source, verticalMode, 'plain-all');
  const parts = [];
  let cursor = 0;
  ranges.forEach((range, index) => {
    if (range.start > cursor) parts.push(<span key={`plain-gap-${index}`}>{renderTextFragment(source.slice(cursor, range.start), verticalMode, `plain-gap-${index}`)}</span>);
    parts.push(<span key={`plain-token-${index}`} className={range.className} data-token={range.surface}>{renderTextFragment(source.slice(range.start, range.end), verticalMode, `plain-token-${index}`)}</span>);
    cursor = range.end;
  });
  if (cursor < source.length) parts.push(<span key="plain-tail">{renderTextFragment(source.slice(cursor), verticalMode, 'plain-tail')}</span>);
  return parts;
}

function collectVisibleTextNodes(root) {
  const nodes = [];
  let text = '';
  function walk(node) {
    if (!node) return;
    if (node.nodeType === Node.TEXT_NODE) {
      const parent = node.parentElement;
      if (!parent || ['RT', 'RP', 'SCRIPT', 'STYLE'].includes(parent.tagName)) return;
      const start = text.length;
      text += node.textContent || '';
      const end = text.length;
      if (end > start) nodes.push({ node, start, end });
      return;
    }
    if (node.nodeType === Node.ELEMENT_NODE) {
      if (['RT', 'RP', 'SCRIPT', 'STYLE'].includes(node.tagName)) return;
      for (const child of [...node.childNodes]) walk(child);
    }
  }
  walk(root);
  return { text, nodes };
}

function applyRangesToVisibleTextNodes(nodes, ranges) {
  const byNodeIndex = new Map();
  for (const range of ranges) {
    for (let nodeIndex = 0; nodeIndex < nodes.length; nodeIndex++) {
      const info = nodes[nodeIndex];
      const start = Math.max(range.start, info.start);
      const end = Math.min(range.end, info.end);
      if (start < end) {
        if (!byNodeIndex.has(nodeIndex)) byNodeIndex.set(nodeIndex, []);
        byNodeIndex.get(nodeIndex).push({ localStart: start - info.start, localEnd: end - info.start, className: range.className, surface: range.surface });
      }
    }
  }
  [...byNodeIndex.entries()].sort((a, b) => b[0] - a[0]).forEach(([nodeIndex, segments]) => {
    const node = nodes[nodeIndex].node;
    if (!node.parentNode) return;
    const text = node.textContent || '';
    const ordered = segments
      .sort((a, b) => a.localStart - b.localStart || b.localEnd - a.localEnd)
      .filter((segment, index, arr) => index === 0 || segment.localStart >= arr[index - 1].localEnd);
    const frag = document.createDocumentFragment();
    let cursor = 0;
    for (const segment of ordered) {
      if (segment.localStart > cursor) frag.appendChild(document.createTextNode(text.slice(cursor, segment.localStart)));
      const matched = text.slice(segment.localStart, segment.localEnd);
      if (matched) {
        const span = document.createElement('span');
        span.className = segment.className;
        span.dataset.token = segment.surface;
        span.textContent = matched;
        frag.appendChild(span);
      }
      cursor = segment.localEnd;
    }
    if (cursor < text.length) frag.appendChild(document.createTextNode(text.slice(cursor)));
    node.parentNode.replaceChild(frag, node);
  });
}

function colorizeHtmlByVisibleTextRanges(html, tokens) {
  if (!tokens || tokens.length === 0) return html;
  try {
    const div = document.createElement('div');
    div.innerHTML = html;
    const { text, nodes } = collectVisibleTextNodes(div);
    const ranges = buildTokenRangesFromText(text, tokens);
    if (!ranges.length) return div.innerHTML;
    applyRangesToVisibleTextNodes(nodes, ranges);
    wrapIndividualDashes(div);
    return div.innerHTML;
  } catch (error) {
    console.warn('[Reader] Failed to colorize furigana HTML:', error);
    return html;
  }
}

function renderStableSentence({ htmlText, plainText, tokens, showFurigana, verticalMode }) {
  if (showFurigana) {
    const html = htmlText || plainText || '';
    return <span dangerouslySetInnerHTML={{ __html: colorizeHtmlByVisibleTextRanges(html, tokens) }} />;
  }
  return <span>{renderColorizedPlainText(plainText || '', tokens, verticalMode)}</span>;
}

/* ─── Vertical plain text ─── */
function renderChars(text, verticalMode, keyPrefix = 'c') {
  if (!verticalMode) return (text || '');
  const parts = [], str = text || '';
  let lastIdx = 0, match;
  dashSingleRegex.lastIndex = 0;
  while ((match = dashSingleRegex.exec(str)) !== null) {
    if (match.index > lastIdx) parts.push(str.slice(lastIdx, match.index));
    parts.push(<span key={`${keyPrefix}-${lastIdx}`} className="vertical-dash-fix">{match[0]}</span>);
    lastIdx = dashSingleRegex.lastIndex;
  }
  if (lastIdx < str.length) parts.push(str.slice(lastIdx));
  return parts.length ? parts : str;
}

function getSelectedWord() {
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || !sel.rangeCount) return '';
  const text = sel.toString().trim();
  if (text && !text.includes(' ') && text.length < 20) return text;
  const range = sel.getRangeAt(0);
  if (!range.startContainer || range.startContainer.nodeType !== 3) return text;
  const fullText = range.startContainer.textContent || '';
  let start = range.startOffset, end = range.endOffset;
  while (start > 0 && /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF]/.test(fullText[start - 1])) start--;
  while (end < fullText.length && /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF]/.test(fullText[end])) end++;
  return fullText.slice(start, end).trim();
}

/* ─── Component ─── */
export default function Reader({ book, flatItems, chapterImageLists, onLoadAnotherBook }) {
  const saved = getProgress(book.id) || {};
  const [itemIndex, setItemIndex] = useState(() => saved.itemIndex || 0);
  const [showFurigana, setShowFurigana] = useState(() => saved.showFurigana || false);
  const [verticalMode, setVerticalMode] = useState(() => saved.verticalMode ?? true);
  const [readerStyle, setReaderStyle] = useState(() => ({ ...DEFAULT_STYLE, ...(saved.readerStyle || {}) }));
  const [selectedText, setSelectedText] = useState('');
  const [noteType, setNoteType] = useState(() => saved.noteType || 'Kiku');
  const [fields, setFields] = useState(() => ({ ...DEFAULT_FIELDS, ...(saved.fields || {}) }));

  const [sidebarOpen, setSidebarOpen] = useState(() => saved.sidebarOpen ?? true);
  const [showStyle, setShowStyle] = useState(false);
  const [ankiStatus, setAnkiStatus] = useState({ connected: false, message: 'Not checked' });
  const [cacheVersion, setCacheVersion] = useState(0);
  const [globalFreqReady, setGlobalFreqReady] = useState(false);
  const [sessionToken, setSessionToken] = useState(() => { try { return localStorage.getItem('nadeshiko_session_token') || ''; } catch { return ''; } });
  const [forceTts, setForceTts] = useState(() => { try { return localStorage.getItem('force_tts') === 'true'; } catch { return false; } });
  const [debugMode, setDebugMode] = useState(saved.debugMode ?? false);
  const [miningDebug, setMiningDebug] = useState(null);
  const [unblurredImages, setUnblurredImages] = useState(new Set());
  const [goInput, setGoInput] = useState('');
  const [status, setStatus] = useState({ type: '', message: '' });
  const [enrichResult, setEnrichResult] = useState(null);
  const [isWorking, setIsWorking] = useState(false);

  const sentenceBoxRef = useRef(null);

  const displayItems = useMemo(() => {
    return (flatItems || []).map(item => {
      if (item.type === 'sentence') return { type: 'scene', data: item };
      if (item.type === 'image') return { type: 'illustration', data: item };
      return null;
    }).filter(Boolean);
  }, [flatItems]);

  const totalScenes = displayItems.length;
  const currentItem = displayItems[Math.min(itemIndex, Math.max(totalScenes - 1, 0))];
  const isText = currentItem?.type === 'scene';
  const isImage = currentItem?.type === 'illustration';
  const currentData = currentItem?.data;
  const cleanedTitle = cleanBookTitle(book.title);
  const jpAnalyzerShadow = useJpAnalyzerShadow(
  isText ? currentData?.plainText : '',
  {
    enabled: true
  }
);
  const jpAnalyzerAdapted = useMemo(() => {
  if (
    !isText ||
    !currentData?.plainText ||
    !jpAnalyzerShadow?.result
  ) {
    return {
      valid: false,
      errors: [],
      words: [],
      summary: null
    };
  }

  return adaptCompactAnalysisToReaderWords(
    jpAnalyzerShadow.result,
    currentData.plainText
  );
}, [
  isText,
  currentData?.plainText,
  jpAnalyzerShadow?.result
]);
  const jpAnalyzerComparison = useMemo(() => {
  if (
    !isText ||
    !jpAnalyzerAdapted.valid
  ) {
    return null;
  }

  return compareReaderWordModels({
    text: currentData?.plainText ?? '',
    kuromojiWords:
      currentData?.classifiedWords ??
      currentData?.tokens ??
      [],
    analyzerWords:
      jpAnalyzerAdapted.words
  });
}, [
  isText,
  currentData?.plainText,
  currentData?.classifiedWords,
  currentData?.tokens,
  jpAnalyzerAdapted
]);
  const comprehension = useMemo(() => {
    if (!isText) return null;
    const words = currentData?.comprehensionWords || currentData?.contentWords || [];
    if (words.length === 0) return null;
    let known = 0;
    for (const w of words) {
      if (isTokenKnownForLearning(w)) known++;
    }
    return { known, total: words.length, percent: Math.round((known / words.length) * 100) };
  }, [currentData, isText, cacheVersion]);

  const unknownWords = useMemo(() => {
    if (!isText) return [];
    const sourceWords = currentData?.miningCandidates || currentData?.contentWords || [];
    const seen = new Set();
    const result = [];
    for (const w of sourceWords) {
      const form = w.dictionaryForm || w.surface;
      if (isTokenKnownForLearning(w)) continue;
      if (seen.has(form)) continue;
      seen.add(form);
      const freq = getFrequency(form);
      result.push({ word: form, surface: w.surface, freq });
    }
    return result;
  }, [currentData, isText, cacheVersion, globalFreqReady]);

  const chapterStarts = useMemo(() => {
    const starts = new Map();
    displayItems.forEach((di, idx) => {
      const ci = di.type === 'scene' ? (di.data.chapterIndex ?? 0) : (di.data?.chapterIndex ?? 0);
      if (ci >= 0 && !starts.has(ci)) starts.set(ci, idx);
    });
    return starts;
  }, [displayItems]);

  const currentChapterIdx = isText ? (currentData?.chapterIndex ?? 0) : (isImage ? (currentData?.chapterIndex ?? 0) : 0);
  const currentChapterImages = chapterImageLists?.[currentChapterIdx] || [];

  useEffect(() => { if (itemIndex >= totalScenes) setItemIndex(Math.max(0, totalScenes - 1)); }, [totalScenes, itemIndex]);
  useEffect(() => { saveProgress(book.id, { itemIndex, showFurigana, verticalMode, readerStyle, sidebarOpen, noteType, fields, debugMode }); }, [book.id, itemIndex, showFurigana, verticalMode, readerStyle, sidebarOpen, noteType, fields, debugMode]);
  useEffect(() => {
    function key(event) {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
      if (event.key === 'ArrowRight' || event.key === ' ') { event.preventDefault(); setItemIndex(i => Math.min(totalScenes - 1, i + 1)); }
      else if (event.key === 'ArrowLeft') { event.preventDefault(); setItemIndex(i => Math.max(0, i - 1)); }
      else if (event.key.toLowerCase() === 'f') setShowFurigana(v => !v);
      else if (event.key.toLowerCase() === 'v') setVerticalMode(v => !v);
      else if (event.key.toLowerCase() === 's') setSidebarOpen(v => !v);
    }
    window.addEventListener('keydown', key);
    return () => window.removeEventListener('keydown', key);
  }, [totalScenes]);

  useEffect(() => {
    checkAnkiStatus();
    loadData();
  }, []);

  async function checkAnkiStatus() {
    try { await checkAnkiConnect(); setAnkiStatus({ connected: true, message: 'Connected' }); }
    catch { setAnkiStatus({ connected: false, message: 'Not connected' }); }
  }

  async function loadData() {
    try {
      if (getCacheSize() === 0) await buildCache(ankiRequest);
      startLoadingGlobalFrequency().then(() => setGlobalFreqReady(true));
    } catch (e) { console.error('[Reader] Data load error:', e); }
    setCacheVersion(v => v + 1);
  }

  function handleTextSelection() { setTimeout(() => { const word = getSelectedWord(); if (word) setSelectedText(word); }, 10); }

  function getKnownKeyCandidates(word) {
    const target = String(word || '').trim();
    if (!target) return [];
    const candidates = new Set();
    const tokenSources = [
      ...(currentData?.miningCandidates || []),
      ...(currentData?.displayWords || []),
      ...(currentData?.contentWords || []),
      ...(currentData?.classifiedWords || []),
      ...(currentData?.tokens || [])
    ];

    for (const token of tokenSources) {
      const surface = String(token?.surface || '').trim();
      const dictionaryForm = String(token?.dictionaryForm || surface || '').trim();
      if (surface === target || dictionaryForm === target) {
        if (dictionaryForm) candidates.add(dictionaryForm);
        if (surface) candidates.add(surface);
      }
    }

    // Fallback for selected text that does not map cleanly to a token.
    candidates.add(target);
    return [...candidates];
  }

  function getPrimaryKnownKey(word) {
    return getKnownKeyCandidates(word)[0] || String(word || '').trim();
  }

  function isManualKnownCandidate(word) {
    return getKnownKeyCandidates(word).some(candidate => isManualKnownWord(candidate));
  }

  function isKnownCandidate(word) {
    return getKnownKeyCandidates(word).some(candidate => isKnownWord(candidate));
  }

  function getSelectedLearningTokens(word) {
    const target = String(word || '').trim();
    if (!target) return [];
    const tokenSources = [
      ...(currentData?.classifiedWords || []),
      ...(currentData?.displayWords || []),
      ...(currentData?.miningCandidates || []),
      ...(currentData?.tokens || [])
    ];
    return tokenSources.filter(token => {
      const surface = String(token?.surface || '').trim();
      const dictionaryForm = String(token?.dictionaryForm || surface || '').trim();
      if (surface !== target && dictionaryForm !== target) return false;
      return token?.tokenCategory === 'learning' || token?.countsForComprehension === true || token?.showInNewWords === true;
    });
  }

  function isLearningCandidate(word) {
    return getSelectedLearningTokens(word).length > 0;
  }

  function handleMarkKnown(word) {
    const target = String(word || '').trim();
    if (!target) return;
    const primary = getPrimaryKnownKey(target);
    addManualKnownWord(primary);
    setSelectedText(primary);
    setCacheVersion(v => v + 1);
    setStatus({ type: 'ok', message: `Marked ${primary} as known.` });
  }

  function handleUndoKnown(word) {
    const target = String(word || '').trim();
    if (!target) return;
    const candidates = getKnownKeyCandidates(target);
    const removed = candidates.filter(candidate => removeManualKnownWord(candidate));
    setSelectedText(target);
    setCacheVersion(v => v + 1);
    if (removed.length > 0) {
      setStatus({ type: 'ok', message: `Removed manual-known status for ${removed.join(', ')}.` });
    } else {
      setStatus({ type: 'error', message: `${target} was not found in manual known words. It may be known from Anki.` });
    }
  }
  function updateStyle(patch) { setReaderStyle(s => ({ ...s, ...patch })); }
  function stepStyle(key, delta, min, max) { setReaderStyle(s => ({ ...s, [key]: clamp(Number(s[key]) + delta, min, max) })); }
  function resetStyle() { setReaderStyle(DEFAULT_STYLE); setVerticalMode(true); }
  function jumpToChapter(idx) { const start = chapterStarts.get(Number(idx)); if (start !== undefined) setItemIndex(start); }
  function handleSaveSessionToken(value) { setSessionToken(value); try { localStorage.setItem('nadeshiko_session_token', value); } catch {} }
  function toggleForceTts() { const next = !forceTts; setForceTts(next); try { localStorage.setItem('force_tts', String(next)); } catch {} }

  function jumpToImage(dataUri) {
    const idx = displayItems.findIndex(di => di.type === 'illustration' && di.data?.dataUri === dataUri);
    if (idx >= 0) { setItemIndex(idx); setUnblurredImages(prev => { const next = new Set(prev); next.add(dataUri); return next; }); setSidebarOpen(false); }
  }
  function toggleImageBlur(dataUri) {
    setUnblurredImages(prev => { const next = new Set(prev); if (next.has(dataUri)) next.delete(dataUri); else next.add(dataUri); return next; });
  }
  function handleGo() {
    const num = parseInt(goInput, 10);
    if (num >= 1 && num <= totalScenes) { setItemIndex(num - 1); setGoInput(''); }
  }

  function handleExportDebugReport() {
    const report = buildDebugReport({ book, itemIndex, totalScenes, currentData, currentDisplayItem, selectedText, comprehension, unknownWords, debugTokenRows, debugSceneRows, debugNearbyRows, parserDebugRows, chapterDebugRows, miningDebug, ankiStatus, globalFreqReady, forceTts, readerStyle, showFurigana, verticalMode });
    const safeTitle = cleanBookTitle(book?.title || book?.fileName || 'book').replace(/[\/:*?"<>|\s]+/g, '_').slice(0, 60) || 'book';
    downloadJsonFile(`novel-audio-miner-debug-${safeTitle}-scene-${itemIndex + 1}.json`, report);
  }

  function updateMiningDebug(patch) {
    setMiningDebug(prev => ({ ...(prev || {}), ...patch, updatedAt: new Date().toISOString() }));
  }

  async function handleMine() {
    if (!selectedText) { setMiningDebug({ status: 'blocked', stage: 'validation', selectedWord: '', error: 'Select a word first.', updatedAt: new Date().toISOString() }); setStatus({ type: 'error', message: 'Select a word first.' }); return; }
    if (!isText) { setMiningDebug({ status: 'blocked', stage: 'validation', selectedWord: selectedText, error: 'Navigate to text first.', updatedAt: new Date().toISOString() }); setStatus({ type: 'error', message: 'Navigate to text first.' }); return; }
    const novelSentence = currentData?.plainText || '';
    setMiningDebug({ status: 'running', stage: 'start', startedAt: new Date().toISOString(), updatedAt: new Date().toISOString(), selectedWord: selectedText, noteType, scene: `${itemIndex + 1} / ${totalScenes}`, chapterTitle: currentData?.chapterTitle || '', novelSentence });
    setIsWorking(true); setEnrichResult(null); setStatus({ type: 'working', message: 'Connecting to Anki...' });
    try {
      updateMiningDebug({ status: 'running', stage: 'checkAnkiConnect' }); await checkAnkiConnect();
      setStatus({ type: 'working', message: 'Finding latest note...' }); updateMiningDebug({ status: 'running', stage: 'findLatestNote' });
      const noteResult = await findLatestNote(noteType);
      updateMiningDebug({ latestNoteQuery: noteResult.query, latestNoteCount: noteResult.ids?.length ?? 0, latestNoteId: noteResult.note?.noteId || '' });
      if (!noteResult.note) { updateMiningDebug({ status: 'error', stage: 'findLatestNote', error: 'No Kiku note found.' }); setStatus({ type: 'error', message: 'No Kiku note found.' }); setIsWorking(false); return; }
      const noteId = noteResult.note.noteId;
      updateMiningDebug({ status: 'running', stage: 'enrichment' });
      const result = await autoEnrichWordWithFallback(selectedText, novelSentence, ankiRequest, noteType, msg => { updateMiningDebug({ status: 'running', stage: msg }); setStatus({ type: 'working', message: msg }); });
      setEnrichResult(result);
      updateMiningDebug({ status: 'running', stage: 'enrichmentComplete', enrichmentMethod: result.method || '', source: result.source || '', mode: result.mode || '', unknownCount: result.unknownCount ?? null, chosenSentence: result.sentence || '', sentenceFurigana: result.sentenceFurigana || '', hasAudioUrl: Boolean(result.audioUrl), hasImageUrl: Boolean(result.imageUrl), audioUrl: result.audioUrl || '', imageUrl: result.imageUrl || '' });
      setStatus({ type: 'working', message: 'Downloading media...' });
      const fieldUpdates = { [fields.sentence]: result.sentence, [fields.sentenceFurigana]: result.sentenceFurigana || result.sentence, [fields.miscInfo]: [cleanedTitle, currentData?.chapterTitle || ''].filter(Boolean).join(' · ') };
      if (result.method !== 'voicevox') fieldUpdates[fields.selectionText] = novelSentence;
      if (result.method === 'voicevox') { try { updateMiningDebug({ status: 'running', stage: 'voicevoxAudio' }); const { audioBase64, filename } = await generateVoicevoxAudio(novelSentence); await ankiRequest('storeMediaFile', { filename, data: audioBase64 }); fieldUpdates[fields.sentenceAudio] = `[sound:${filename}]`; updateMiningDebug({ sentenceAudio: `[sound:${filename}]` }); } catch (err) { updateMiningDebug({ voicevoxError: err?.message || String(err) }); } }
      else if (result.audioUrl) { try { updateMiningDebug({ status: 'running', stage: 'nadeshikoAudio' }); const filename = `nade_audio_${Date.now()}.mp3`; await ankiRequest('storeMediaFile', { filename, url: result.audioUrl }); fieldUpdates[fields.sentenceAudio] = `[sound:${filename}]`; updateMiningDebug({ sentenceAudio: `[sound:${filename}]` }); } catch (e) { updateMiningDebug({ audioError: e?.message || String(e) }); } }
      if (result.method !== 'voicevox' && result.imageUrl) { try { updateMiningDebug({ status: 'running', stage: 'nadeshikoImage' }); const filename = `nade_img_${Date.now()}.jpg`; await ankiRequest('storeMediaFile', { filename, url: result.imageUrl }); fieldUpdates[fields.picture] = `<img src="${filename}">`; updateMiningDebug({ picture: `<img src="${filename}">` }); } catch (e) { updateMiningDebug({ imageError: e?.message || String(e) }); } }
      updateMiningDebug({ status: 'running', stage: 'updateNoteFields', preparedFields: fieldUpdates }); await updateNoteFields(noteId, fieldUpdates);
      addKnownWord(selectedText); setCacheVersion(v => v + 1); try { await ankiRequest('guiBrowse', { query: `nid:${noteId}` }); } catch (e) {}
      updateMiningDebug({ status: 'completed', stage: 'done', updatedNoteId: noteId, preparedFields: fieldUpdates }); setStatus({ type: 'ok', message: `Card updated — ${result.source}${result.mode ? ` (${result.mode})` : ''}` });
    } catch (err) { updateMiningDebug({ status: 'error', stage: 'failed', error: err?.message || String(err) }); setStatus({ type: 'error', message: err?.message || String(err) }); }
    setIsWorking(false);
  }

  const boxStyle = {
    fontSize: `${readerStyle.fontSize}px`, lineHeight: readerStyle.lineHeight,
    height: verticalMode ? `${readerStyle.height}px` : undefined,
    fontFamily: FONT_STACKS[readerStyle.fontFamily] || FONT_STACKS.mincho
  };
  if (!totalScenes) return <section className="reader-card"><h2>{cleanedTitle}</h2><p>No content found.</p></section>;

  const hasDialogueColumns = Boolean(verticalMode && !showFurigana && isText && currentData?.plainText?.includes('\n'));
  const currentDisplayItem = displayItems[itemIndex] || null;
  const debugTokenRows = useMemo(() => getDebugTokenRows(currentData), [currentData, cacheVersion, globalFreqReady]);
  const debugSceneRows = useMemo(() => getSceneDebugSummary({ currentData, displayItem: currentDisplayItem, itemIndex, totalScenes, isText, isImage, selectedText, unknownWords, comprehension, currentChapterImages }), [currentData, currentDisplayItem, itemIndex, totalScenes, isText, isImage, selectedText, unknownWords, comprehension, currentChapterImages]);
  const debugNearbyRows = useMemo(() => getNearbySceneRows(displayItems, itemIndex), [displayItems, itemIndex]);
  const miningDebugRows = useMemo(() => getMiningDebugRows(miningDebug), [miningDebug]);
  const parserDebugRows = useMemo(() => getParserDebugRows(currentData, currentDisplayItem, book), [currentData, currentDisplayItem, book]);
  const chapterDebugRows = useMemo(() => getChapterDebugRows(book, chapterImageLists), [book, chapterImageLists]);
  const selectedDebugToken = useMemo(() => {
    if (!selectedText) return null;
    return debugTokenRows.find(row => row.surface === selectedText || row.dictionaryForm === selectedText) || null;
  }, [debugTokenRows, selectedText]);
  const debugTokenSummary = useMemo(() => {
    const summary = { learning: 0, knownLearning: 0, unknownLearning: 0, grammar: 0, names: 0, numeric: 0 };
    for (const row of debugTokenRows) {
      if (row.tokenCategory === 'learning') {
        summary.learning += 1;
        if (row.known) summary.knownLearning += 1;
        else summary.unknownLearning += 1;
      } else if (row.tokenCategory === 'proper-noun') summary.names += 1;
      else if (row.tokenCategory === 'numeric') summary.numeric += 1;
      else summary.grammar += 1;
    }
    return summary;
  }, [debugTokenRows]);
  const parserSummaryRows = useMemo(() => parserDebugRows.filter(([label]) => ['pageHref', 'orderedIndex', 'itemType', 'chapterIndex', 'chapterTitle', 'imageSrc', 'resolvedZipPath', 'imageExists', 'dataUri'].includes(label)), [parserDebugRows]);
  const miningSummaryRows = useMemo(() => miningDebugRows.filter(([label]) => ['status', 'stage', 'selectedWord', 'latestNoteId', 'enrichmentMethod', 'source', 'mode', 'sentenceAudio', 'picture', 'error'].includes(label)), [miningDebugRows]);

  return (
    <>
      <div className="status-bar">
        <div className="status-left">
          <span className={`status-dot ${ankiStatus.connected ? 'ok' : 'error'}`} />
          <span>Anki {ankiStatus.connected ? 'Connected' : 'Offline'}</span>
          {comprehension && (
            <>
              <span>·</span>
              <span>Comprehension: <strong>{comprehension.percent}%</strong> ({comprehension.known}/{comprehension.total})</span>
            </>
          )}
        </div>
        <div className="status-right">
          <span>{getCacheSize()} known</span>
          <span>·</span>
          <span>{!globalFreqReady ? 'Freq loading...' : forceTts ? 'VOICEVOX' : 'Nadeshiko'}</span>
          <span>·</span>
          <span>{cleanedTitle}</span>
        </div>
      </div>

      <div className="topbar">
        <div style={{ display: 'flex', alignItems: 'baseline' }}>
          <h1>{cleanedTitle}</h1>
          <span className="version">v4.1</span>
        </div>
        <button className="secondary" onClick={onLoadAnotherBook}>Load another book</button>
      </div>

      <div className="main-layout">
        <div className="sidebar-toggle" onClick={() => setSidebarOpen(v => !v)} title="Toggle sidebar (S)">{sidebarOpen ? '✕' : '☰'}</div>

        <aside className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
          <h2>{cleanedTitle}</h2>
          <p className="book-author">{book.author || 'Unknown author'}</p>
          <div style={{ display: 'flex', gap: '10px', fontSize: '12px', color: 'var(--muted)' }}>
            <span><strong>{book.chapters.length}</strong> chapters</span>
            <span><strong>{totalScenes}</strong> scenes</span>
          </div>
          <div>
            <label className="section-label">Jump to chapter</label>
            <select className="chapter-select" value={currentChapterIdx} onChange={e => jumpToChapter(e.target.value)}>
              {book.chapters.map((c, i) => <option key={c.id} value={i}>{i + 1}. {c.title || `Chapter ${i + 1}`}</option>)}
            </select>
          </div>
          {unknownWords.length > 0 && (
            <div>
              <label className="section-label">New words ({unknownWords.length})</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                {unknownWords.map((uw, idx) => {
                  const display = uw.surface || uw.word;
                  return (
                    <span key={idx} className="word-badge-pair">
                      <button
                        type="button"
                        className={`word-badge ${uw.freq?.category ? `word-freq-${uw.freq.category}` : 'word-freq-unlisted'}`}
                        title={`${uw.freq ? `Rank ${uw.freq.rank} · ${uw.freq.category}` : 'Unlisted'} · Click to select`}
                        onClick={() => setSelectedText(uw.word)}>
                        {display}
                      </button>
                      <button
                        type="button"
                        className="mark-known-mini"
                        title={`Mark ${display} as known`}
                        onClick={() => handleMarkKnown(uw.word)}>
                        ✓
                      </button>
                    </span>
                  );
                })}
              </div>
            </div>
          )}
          {currentChapterImages.length > 0 && (
            <div>
              <label className="section-label">Illustrations ({currentChapterImages.length})</label>
              <div className="image-thumbs">
                {currentChapterImages.map((img, idx) => {
                  const displayIdx = displayItems.findIndex(di => di.type === 'illustration' && di.data?.dataUri === img.dataUri);
                  return (
                    <div key={idx} className="image-thumb" onClick={() => jumpToImage(img.dataUri)} title={img.alt || ''}>
                      <img src={img.dataUri} alt={img.alt || ''} />
                      {displayIdx >= 0 && <span className="thumb-label">Scene {displayIdx + 1}</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          <div style={{ display: 'flex', gap: '6px' }}>
            <button className="secondary" onClick={() => setShowFurigana(v => !v)} style={{ flex: 1, fontSize: '12px' }}>Furigana: {showFurigana ? 'ON' : 'OFF'}</button>
            <button className="secondary" onClick={() => setVerticalMode(v => !v)} style={{ flex: 1, fontSize: '12px' }}>{verticalMode ? 'Vertical' : 'Horizontal'}</button>
          </div>
          <details open={showStyle} onToggle={e => setShowStyle(e.target.open)}>
            <summary style={{ fontSize: '12px', color: 'var(--muted)', cursor: 'pointer' }}>Reader style</summary>
            <div className="style-panel">
              <div className="style-row"><span>Font size</span><div><button onClick={() => stepStyle('fontSize', -2, 20, 46)}>−</button><b>{readerStyle.fontSize}</b><button onClick={() => stepStyle('fontSize', 2, 20, 46)}>+</button></div></div>
              <input type="range" min="20" max="46" value={readerStyle.fontSize} onChange={e => updateStyle({ fontSize: Number(e.target.value) })} />
              <div className="style-row"><span>Line spacing</span><div><button onClick={() => stepStyle('lineHeight', -0.1, 1.4, 2.8)}>−</button><b>{readerStyle.lineHeight.toFixed(2)}</b><button onClick={() => stepStyle('lineHeight', 0.1, 1.4, 2.8)}>+</button></div></div>
              <input type="range" min="1.4" max="2.8" step="0.05" value={readerStyle.lineHeight} onChange={e => updateStyle({ lineHeight: Number(e.target.value) })} />
              <div className="style-row"><span>Height</span><div><button onClick={() => stepStyle('height', -40, 420, 900)}>−</button><b>{readerStyle.height}</b><button onClick={() => stepStyle('height', 40, 420, 900)}>+</button></div></div>
              <input type="range" min="420" max="900" step="20" value={readerStyle.height} onChange={e => updateStyle({ height: Number(e.target.value) })} />
              <button className="secondary" onClick={resetStyle} style={{ marginTop: '8px', width: '100%', fontSize: '11px' }}>Reset to default</button>
            </div>
          </details>
          <details className="advanced-settings">
            <summary>Advanced</summary>
            <div style={{ display: 'grid', gap: '8px', marginTop: '8px' }}>
              <label style={{ fontSize: '11px', color: 'var(--muted)' }}>Note type: <input value={noteType} onChange={e => setNoteType(e.target.value)} /></label>
              <label style={{ fontSize: '11px', color: 'var(--muted)', display: 'grid', gap: '4px' }}>Session Token: <input value={sessionToken} onChange={e => handleSaveSessionToken(e.target.value)} placeholder="Paste __Secure-nadeshiko.session_token" /><span style={{ fontSize: '10px' }}>F12 → Application → Cookies → nadeshiko.co</span></label>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <button className="secondary" onClick={async () => { try { await buildCache(ankiRequest); setCacheVersion(v => v + 1); } catch {} }} style={{ fontSize: '10px', padding: '4px 8px' }}>Rebuild Cache</button>
                <button className="secondary" onClick={() => { clearCache(); setCacheVersion(v => v + 1); }} style={{ fontSize: '10px', padding: '4px 8px' }}>Clear Anki Cache</button>
                <button className="secondary" onClick={toggleForceTts} style={{ fontSize: '10px', padding: '4px 8px', background: forceTts ? 'var(--warning)' : undefined }}>Force TTS: {forceTts ? 'ON' : 'OFF'}</button>
                <button className="secondary" onClick={() => setDebugMode(v => !v)} style={{ fontSize: '10px', padding: '4px 8px', background: debugMode ? 'var(--accent)' : undefined }}>Debug Mode: {debugMode ? 'ON' : 'OFF'}</button>
              </div>
            </div>
          </details>

          {debugMode && (
            <div className="debug-panel">
              <div className="debug-panel-title-row">
                <div className="debug-panel-title">Debug Mode v6</div>
                <button type="button" className="debug-export-btn" onClick={handleExportDebugReport}>Export full report</button>
              </div>

              <details open>
                <summary>Current scene</summary>
                <div className="debug-summary-grid">
                  <div className="debug-mini-card"><span>Scene</span><strong>{itemIndex + 1} / {totalScenes}</strong></div>
                  <div className="debug-mini-card"><span>Type</span><strong>{isImage ? 'image' : 'sentence'}</strong></div>
                  <div className="debug-mini-card"><span>Chapter</span><strong>{currentData?.chapterTitle || '-'}</strong></div>
                  <div className="debug-mini-card"><span>Selected</span><strong>{selectedText || '-'}</strong></div>
                  <div className="debug-mini-card"><span>Comprehension</span><strong>{comprehension ? `${comprehension.percent}% (${comprehension.known}/${comprehension.total})` : 'n/a'}</strong></div>
                  <div className="debug-mini-card"><span>Unknown</span><strong>{unknownWords.length}</strong></div>
                </div>
              </details>
<JpAnalyzerIntegrationPanel
  currentData={currentData}
  shadowState={jpAnalyzerShadow}
  adaptedResult={jpAnalyzerAdapted}
  comparison={jpAnalyzerComparison}
  onClearShadowCache={
    clearJpAnalyzerShadowCache
  }
/>

<DictionaryDebugPanel
  selectedText={selectedText}
  currentData={currentData}
/>
              <details>
                <summary>Token summary</summary>
                <div className="debug-summary-grid">
                  <div className="debug-mini-card"><span>Total tokens</span><strong>{debugTokenRows.length}</strong></div>
                  <div className="debug-mini-card"><span>Learning</span><strong>{debugTokenSummary.learning}</strong></div>
                  <div className="debug-mini-card"><span>Known learning</span><strong>{debugTokenSummary.knownLearning}</strong></div>
                  <div className="debug-mini-card"><span>Unknown learning</span><strong>{debugTokenSummary.unknownLearning}</strong></div>
                  <div className="debug-mini-card"><span>Grammar/other</span><strong>{debugTokenSummary.grammar}</strong></div>
                  <div className="debug-mini-card"><span>Name/numeric</span><strong>{debugTokenSummary.names} / {debugTokenSummary.numeric}</strong></div>
                </div>
                {selectedDebugToken ? (
                  <details className="debug-nested" open>
                    <summary>selected token</summary>
                    <div className="debug-kv-list">
                      <div className="debug-kv"><span>surface</span><code>{selectedDebugToken.surface || '-'}</code></div>
                      <div className="debug-kv"><span>dictionary</span><code>{selectedDebugToken.dictionaryForm || '-'}</code></div>
                      <div className="debug-kv"><span>POS</span><code>{[selectedDebugToken.pos, selectedDebugToken.posDetail1, selectedDebugToken.posDetail2].filter(Boolean).join(' / ') || '-'}</code></div>
                      <div className="debug-kv"><span>category</span><code>{selectedDebugToken.tokenCategory || '-'}</code></div>
                      <div className="debug-kv"><span>known</span><code>{yesNo(selectedDebugToken.known)}</code></div>
                      <div className="debug-kv"><span>manual</span><code>{yesNo(selectedDebugToken.manualKnown)}</code></div>
                      <div className="debug-kv"><span>color</span><code>{selectedDebugToken.colorClass || '-'}</code></div>
                      <div className="debug-kv"><span>frequency</span><code>{selectedDebugToken.frequency || '-'}</code></div>
                    </div>
                  </details>
                ) : selectedText ? (<div className="debug-empty">Selected text was not mapped to a token. Use Export full report for raw token rows.</div>) : (<div className="debug-empty">Select a word to inspect token details.</div>)}
              </details>

              <details>
                <summary>Parser / image summary</summary>
                <div className="debug-kv-list">{parserSummaryRows.map(([label, value]) => (<div className="debug-kv" key={label}><span>{label}</span><code>{value || '-'}</code></div>))}</div>
              </details>

              <details>
                <summary>Mining summary</summary>
                {!miningDebug ? (<div className="debug-empty">No mining attempt recorded yet.</div>) : (<div className="debug-kv-list">{miningSummaryRows.map(([label, value]) => (<div className="debug-kv" key={label}><span>{label}</span><code>{value || '-'}</code></div>))}</div>)}
              </details>

              <details>
                <summary>Nearby scenes ({debugNearbyRows.length})</summary>
                <div className="debug-neighbor-list">
                  {debugNearbyRows.map(row => (<div className={`debug-neighbor-row ${row.relative === 'current' ? 'current' : ''}`} key={row.index}><div><strong>{row.relative}</strong><span>Scene {row.index + 1}</span><span>{row.type}</span></div><code>{row.preview || '-'}</code></div>))}
                </div>
              </details>

              <details>
                <summary>Raw details are in export</summary>
                <div className="debug-empty">Use Export full report for full token rows, parser rows, text/html, mining fields, dictionary diagnostics, and raw debug data.</div>
              </details>
            </div>
          )}
        </aside>

        <div className="reader-area">
          <div className="nav-header">
            <span className="chapter-info">
              {currentData?.chapterTitle || ''}
              <span style={{ color: 'var(--muted)', marginLeft: '8px' }}>Ch. {currentChapterIdx + 1}/{book.chapters.length}</span>
            </span>
            <div className="nav-controls">
              <button onClick={() => setItemIndex(i => Math.max(0, i - 1))} disabled={itemIndex === 0}>←</button>
              <input type="number" min="1" max={totalScenes} value={goInput} onChange={e => setGoInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') handleGo(); }} placeholder={`1-${totalScenes}`} />
              <button onClick={handleGo}>Go</button>
              <button onClick={() => setItemIndex(i => Math.min(totalScenes - 1, i + 1))} disabled={itemIndex === totalScenes - 1}>→</button>
            </div>
            <span className="item-counter">{isText ? '📖' : '🖼️'} Scene {itemIndex + 1}/{totalScenes}</span>
          </div>

          {isText && currentData && (
            <>
              <div ref={sentenceBoxRef}
                className={`sentence-box ${verticalMode ? 'vertical' : ''} ${hasDialogueColumns ? 'dialogue-columns' : ''}`}
                lang="ja" style={boxStyle}
                onMouseUp={handleTextSelection} onDoubleClick={handleTextSelection} onTouchEnd={handleTextSelection}>
                {renderStableSentence({
                  htmlText: currentData.htmlText,
                  plainText: currentData.plainText,
                  tokens: currentData.displayWords || currentData.contentWords,
                  showFurigana,
                  verticalMode
                })}
              </div>
              {status.message && <div className={`status-message ${status.type}`} style={{ marginTop: '8px' }}>{status.message}</div>}
            </>
          )}

          {isImage && currentData && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <div className="image-panel" onClick={() => toggleImageBlur(currentData.dataUri)}>
                <img src={currentData.dataUri} alt={currentData.alt || ''} className={!unblurredImages.has(currentData.dataUri) ? 'blurred' : ''} />
                {!unblurredImages.has(currentData.dataUri) && <div className="unblur-btn">Click to reveal</div>}
              </div>
              {currentData.alt && unblurredImages.has(currentData.dataUri) && <div className="image-caption">{currentData.alt}</div>}
              {status.message && <div className={`status-message ${status.type}`} style={{ marginTop: '8px' }}>{status.message}</div>}
            </div>
          )}

          {isText && (
            <div className="action-bar">
              <div className="selected-word">
                <span className="label">Selected:</span>
                <span className="word" title={selectedText}>{selectedText || '—'}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {isWorking && <span className="mine-status">Working...</span>}
                {enrichResult && !isWorking && <span className="mine-status" style={{ color: 'var(--success)' }}>✓ {enrichResult.source}</span>}
                {selectedText && isManualKnownCandidate(selectedText) ? (
                  <button className="secondary mark-known-btn" onClick={() => handleUndoKnown(selectedText)} disabled={isWorking}>Undo Known</button>
                ) : selectedText && isKnownCandidate(selectedText) ? (
                  <button className="secondary mark-known-btn known-from-anki-btn" disabled title="This word is already known from Anki/cache. It is not in manual-known storage.">Known from Anki</button>
                ) : selectedText && !isLearningCandidate(selectedText) ? (
                  <button className="secondary mark-known-btn non-learning-word-btn" disabled title="Particles, grammar, symbols, names, and numeric expressions are not manual-known candidates.">Not a learning word</button>
                ) : (
                  <button className="secondary mark-known-btn" onClick={() => handleMarkKnown(selectedText)} disabled={!selectedText || isWorking}>Mark as Known</button>
                )}
                <button className="mine-btn" onClick={handleMine} disabled={!selectedText || isWorking}>⚡ Mine to Anki</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
```

#### `src/lib/analyzerShadowComparison.js`

```javascript
/**
 * Compare Kuromoji-derived reader words with adapted
 * JP Analyzer words.
 *
 * This is diagnostic only and does not modify rendering.
 */

export function compareReaderWordModels({
  text,
  kuromojiWords,
  analyzerWords
}) {
  const sourceText = String(text ?? '');

  const legacyRanges = createKuromojiRanges(
    sourceText,
    kuromojiWords ?? []
  );

  const analyzerRanges = normalizeAnalyzerRanges(
    sourceText,
    analyzerWords ?? []
  );

  const legacyByRange = indexByRange(legacyRanges);
  const analyzerByRange = indexByRange(analyzerRanges);

  const exactRangeMatches = [];
  const categoryDifferences = [];
  const headwordDifferences = [];
  const kuromojiOnly = [];
  const analyzerOnly = [];

  for (const [key, legacy] of legacyByRange) {
    const analyzer = analyzerByRange.get(key);

    if (!analyzer) {
      kuromojiOnly.push(toSafeComparisonRow(legacy));
      continue;
    }

    exactRangeMatches.push(key);

    if (
      normalizeCategory(legacy) !==
      normalizeCategory(analyzer)
    ) {
      categoryDifferences.push({
        start: legacy.start,
        end: legacy.end,
        surface: legacy.surface,
        kuromojiCategory:
          normalizeCategory(legacy),
        analyzerCategory:
          normalizeCategory(analyzer),
        analyzerRole:
          analyzer.analyzerRole ?? null
      });
    }

    if (
      normalizeLookupKey(legacy) !==
      normalizeLookupKey(analyzer)
    ) {
      headwordDifferences.push({
        start: legacy.start,
        end: legacy.end,
        surface: legacy.surface,
        kuromojiKey:
          normalizeLookupKey(legacy),
        analyzerKey:
          normalizeLookupKey(analyzer)
      });
    }
  }

  for (const [key, analyzer] of analyzerByRange) {
    if (!legacyByRange.has(key)) {
      analyzerOnly.push(toSafeComparisonRow(analyzer));
    }
  }

  const kuromojiSummary =
    summarizeModel(legacyRanges);
  const analyzerSummary =
    summarizeModel(analyzerRanges);

  const exactMatchCount = exactRangeMatches.length;
  const unionRangeCount = new Set([
    ...legacyByRange.keys(),
    ...analyzerByRange.keys()
  ]).size;

  return {
    sourceTextLength: sourceText.length,

    kuromoji: kuromojiSummary,
    analyzer: analyzerSummary,

    exactRangeMatchCount: exactMatchCount,
    rangeUnionCount: unionRangeCount,
    exactRangeAgreement:
      unionRangeCount > 0
        ? exactMatchCount / unionRangeCount
        : 1,

    categoryDifferenceCount:
      categoryDifferences.length,
    headwordDifferenceCount:
      headwordDifferences.length,
    kuromojiOnlyCount: kuromojiOnly.length,
    analyzerOnlyCount: analyzerOnly.length,

    categoryDifferences,
    headwordDifferences,
    kuromojiOnly,
    analyzerOnly,

    kuromojiRangeErrors:
      legacyRanges.filter(
        (range) => range.rangeError
      ).length,

    analyzerRangeErrors:
      analyzerRanges.filter(
        (range) => range.rangeError
      ).length
  };
}

function createKuromojiRanges(text, words) {
  const ranges = [];
  const occupied = new Array(text.length).fill(false);

  for (const word of words) {
    const surface = String(word?.surface ?? '');

    if (!surface) {
      continue;
    }

    const preferredStart =
      Number.isInteger(word?.start)
        ? word.start
        : null;

    if (
      preferredStart != null &&
      text.slice(
        preferredStart,
        preferredStart + surface.length
      ) === surface &&
      !hasOccupiedRange(
        occupied,
        preferredStart,
        preferredStart + surface.length
      )
    ) {
      const end = preferredStart + surface.length;

      occupyRange(occupied, preferredStart, end);

      ranges.push({
        ...word,
        start: preferredStart,
        end,
        surface,
        analysisSource: 'kuromoji'
      });

      continue;
    }

    let searchFrom = 0;
    let matchedStart = -1;

    while (searchFrom < text.length) {
      const candidate = text.indexOf(
        surface,
        searchFrom
      );

      if (candidate < 0) {
        break;
      }

      const candidateEnd =
        candidate + surface.length;

      if (
        !hasOccupiedRange(
          occupied,
          candidate,
          candidateEnd
        )
      ) {
        matchedStart = candidate;
        break;
      }

      searchFrom = candidate + 1;
    }

    if (matchedStart < 0) {
      ranges.push({
        ...word,
        start: null,
        end: null,
        surface,
        analysisSource: 'kuromoji',
        rangeError: 'surface-not-found'
      });

      continue;
    }

    const end = matchedStart + surface.length;

    occupyRange(occupied, matchedStart, end);

    ranges.push({
      ...word,
      start: matchedStart,
      end,
      surface,
      analysisSource: 'kuromoji'
    });
  }

  return ranges.sort(compareRanges);
}

function normalizeAnalyzerRanges(text, words) {
  return words
    .map((word) => {
      const start = word?.start;
      const end = word?.end;
      const surface = String(word?.surface ?? '');

      if (
        !Number.isInteger(start) ||
        !Number.isInteger(end) ||
        start < 0 ||
        end <= start ||
        end > text.length ||
        text.slice(start, end) !== surface
      ) {
        return {
          ...word,
          rangeError: 'invalid-analyzer-range'
        };
      }

      return {
        ...word,
        analysisSource: 'jp-analyzer'
      };
    })
    .sort(compareRanges);
}

function hasOccupiedRange(occupied, start, end) {
  for (let index = start; index < end; index += 1) {
    if (occupied[index]) {
      return true;
    }
  }

  return false;
}

function occupyRange(occupied, start, end) {
  for (let index = start; index < end; index += 1) {
    occupied[index] = true;
  }
}

function indexByRange(ranges) {
  const index = new Map();

  for (const range of ranges) {
    if (
      range.rangeError ||
      !Number.isInteger(range.start) ||
      !Number.isInteger(range.end)
    ) {
      continue;
    }

    index.set(
      `${range.start}:${range.end}`,
      range
    );
  }

  return index;
}

function normalizeCategory(word) {
  if (
    word?.tokenCategory === 'proper-noun' ||
    word?.colorRole === 'name'
  ) {
    return 'name';
  }

  if (
    word?.tokenCategory === 'numeric' ||
    word?.colorRole === 'numeric'
  ) {
    return 'numeric';
  }

  if (
    word?.tokenCategory === 'grammar' ||
    word?.tokenCategory === 'ignored' ||
    word?.colorRole === 'grammar'
  ) {
    return 'grammar';
  }

  if (
    word?.tokenCategory === 'learning' ||
    word?.colorRole === 'learning'
  ) {
    return 'learning';
  }

  if (
    word?.colorRole === 'neutral'
  ) {
    return 'neutral';
  }

  return 'unresolved';
}

function normalizeLookupKey(word) {
  return String(
    word?.dictionaryForm ??
      word?.headword ??
      word?.surface ??
      ''
  ).trim();
}

function summarizeModel(ranges) {
  const summary = {
    spans: ranges.length,
    learning: 0,
    names: 0,
    grammar: 0,
    numeric: 0,
    neutral: 0,
    unresolved: 0,
    comprehension: 0,
    newWords: 0,
    rangeErrors: 0
  };

  for (const range of ranges) {
    if (range.rangeError) {
      summary.rangeErrors += 1;
    }

    const category = normalizeCategory(range);

    if (category in summary) {
      summary[category] += 1;
    }

    if (range.countsForComprehension) {
      summary.comprehension += 1;
    }

    if (range.showInNewWords) {
      summary.newWords += 1;
    }
  }

  return summary;
}

function toSafeComparisonRow(word) {
  return {
    start: word?.start ?? null,
    end: word?.end ?? null,
    surface: word?.surface ?? '',
    dictionaryForm:
      normalizeLookupKey(word),
    category: normalizeCategory(word),
    analyzerRole:
      word?.analyzerRole ?? null,
    confidence:
      word?.confidence ?? null,
    rangeError:
      word?.rangeError ?? null
  };
}

function compareRanges(left, right) {
  const leftStart =
    Number.isInteger(left?.start)
      ? left.start
      : Number.MAX_SAFE_INTEGER;

  const rightStart =
    Number.isInteger(right?.start)
      ? right.start
      : Number.MAX_SAFE_INTEGER;

  if (leftStart !== rightStart) {
    return leftStart - rightStart;
  }

  return (
    (right?.end ?? 0) -
    (left?.end ?? 0)
  );
}
```

#### `src/lib/analyzerWordAdapter.js`

```javascript
/**
 * Convert JP Analyzer compact resolved spans into the existing
 * Novel Audio Miner reader-word shape.
 *
 * Phase 3:
 * - Used only for hidden comparison.
 * - Does not replace visible Kuromoji words.
 */

const NAME_ROLES = new Set([
  'proper-name',
  'person-reference'
]);

const NUMERIC_ROLES = new Set([
  'numeral',
  'counter'
]);

const GRAMMAR_ROLES = new Set([
  'grammar',
  'particle',
  'auxiliary',
  'discourse'
]);

const NEUTRAL_ROLES = new Set([
  'punctuation',
  'symbol'
]);

const LEARNING_ROLES = new Set([
  'term',
  'predicate'
]);

export function adaptCompactAnalysisToReaderWords(
  compact,
  expectedText
) {
  const sourceText = String(expectedText ?? '');
  const errors = [];

  if (!compact || typeof compact !== 'object') {
    return {
      valid: false,
      errors: ['Compact analysis is not an object.'],
      words: []
    };
  }

  if (compact.text !== sourceText) {
    errors.push(
      'Analyzer source text differs from reader source text.'
    );
  }

  const spans = Array.isArray(compact.resolvedSpans)
    ? compact.resolvedSpans
    : [];

  if (!Array.isArray(compact.resolvedSpans)) {
    errors.push('resolvedSpans is missing.');
  }

  const words = [];
  let previousEnd = 0;

  spans.forEach((span, index) => {
    const rangeErrors = validateSpan(
      span,
      index,
      sourceText,
      previousEnd
    );

    errors.push(...rangeErrors);

    if (rangeErrors.length > 0) {
      return;
    }

    previousEnd = span.end;

    words.push(
      adaptResolvedSpan(span, sourceText)
    );
  });

  return {
    valid: errors.length === 0,
    errors,
    words,
    summary: summarizeReaderWords(words)
  };
}

function validateSpan(
  span,
  index,
  sourceText,
  previousEnd
) {
  const errors = [];
  const label = `resolvedSpans[${index}]`;

  if (!Number.isInteger(span?.start)) {
    errors.push(`${label}.start is not an integer.`);
  }

  if (!Number.isInteger(span?.end)) {
    errors.push(`${label}.end is not an integer.`);
  }

  if (errors.length > 0) {
    return errors;
  }

  if (
    span.start < 0 ||
    span.end <= span.start ||
    span.end > sourceText.length
  ) {
    errors.push(`${label} has an invalid range.`);
    return errors;
  }

  if (span.start < previousEnd) {
    errors.push(`${label} overlaps a previous span.`);
  }

  const expectedSurface = sourceText.slice(
    span.start,
    span.end
  );

  if (span.surface !== expectedSurface) {
    errors.push(
      `${label}.surface does not match source offsets.`
    );
  }

  return errors;
}

function adaptResolvedSpan(span, sourceText) {
  const role = normalizeRole(span.role);
  const classification = classifyRole(role);
  const surface = sourceText.slice(
    span.start,
    span.end
  );

  const headword =
    normalizeHeadword(span.headword) || surface;

  return {
    start: span.start,
    end: span.end,
    surface,
    dictionaryForm: headword,

    tokenCategory: classification.tokenCategory,
    colorRole: classification.colorRole,
    countsForComprehension:
      classification.countsForComprehension,
    showInNewWords:
      classification.showInNewWords,

    analyzerRole: role,
    grammarId:
      span.grammar_id ??
      span.grammarId ??
      null,
    confidence:
      typeof span.confidence === 'number'
        ? span.confidence
        : null,
    selectedCandidateId:
      span.selected_candidate_id ??
      span.selectedCandidateId ??
      null,
    sourceLayer:
      span.source_layer ??
      span.sourceLayer ??
      null,

    analysisSource: 'jp-analyzer'
  };
}

function normalizeRole(role) {
  return String(role ?? '')
    .trim()
    .toLowerCase() || 'unknown';
}

function normalizeHeadword(headword) {
  if (typeof headword !== 'string') {
    return '';
  }

  const normalized = headword.trim();

  if (
    !normalized ||
    normalized === '*' ||
    normalized === 'null'
  ) {
    return '';
  }

  return normalized;
}

function classifyRole(role) {
  if (NAME_ROLES.has(role)) {
    return {
      tokenCategory: 'proper-noun',
      colorRole: 'name',
      countsForComprehension: false,
      showInNewWords: false
    };
  }

  if (NUMERIC_ROLES.has(role)) {
    return {
      tokenCategory: 'numeric',
      colorRole: 'numeric',
      countsForComprehension: false,
      showInNewWords: false
    };
  }

  if (GRAMMAR_ROLES.has(role)) {
    return {
      tokenCategory: 'grammar',
      colorRole: 'grammar',
      countsForComprehension: false,
      showInNewWords: false
    };
  }

  if (NEUTRAL_ROLES.has(role)) {
    return {
      tokenCategory: 'ignored',
      colorRole: 'neutral',
      countsForComprehension: false,
      showInNewWords: false
    };
  }

  if (LEARNING_ROLES.has(role)) {
    return {
      tokenCategory: 'learning',
      colorRole: 'learning',
      countsForComprehension: true,
      showInNewWords: true
    };
  }

  return {
    tokenCategory: 'unresolved',
    colorRole: 'unknown',
    countsForComprehension: false,
    showInNewWords: false
  };
}

function summarizeReaderWords(words) {
  const summary = {
    total: words.length,
    learning: 0,
    names: 0,
    grammar: 0,
    numeric: 0,
    neutral: 0,
    unresolved: 0,
    comprehension: 0,
    newWords: 0
  };

  for (const word of words) {
    if (word.tokenCategory === 'learning') {
      summary.learning += 1;
    } else if (
      word.tokenCategory === 'proper-noun'
    ) {
      summary.names += 1;
    } else if (
      word.tokenCategory === 'grammar'
    ) {
      summary.grammar += 1;
    } else if (
      word.tokenCategory === 'numeric'
    ) {
      summary.numeric += 1;
    } else if (
      word.tokenCategory === 'ignored'
    ) {
      summary.neutral += 1;
    } else {
      summary.unresolved += 1;
    }

    if (word.countsForComprehension) {
      summary.comprehension += 1;
    }

    if (word.showInNewWords) {
      summary.newWords += 1;
    }
  }

  return summary;
}
```

#### `src/lib/dictionaryValidationBridge.js`

```javascript
/**
 * Phase 7B.5 browser bridge.
 *
 * `lookupExact` must be the app's existing exact-headword lookup function.
 * It may return an array directly or an object with `entries`/`matches`.
 */

const LEXICALIZED_TAG_PATTERN = /(idiom|fixed|expression|phrase|慣用|成句|連語|熟語)/iu;
const LEXICALIZED_EXACT_TAGS = new Set(["exp"]);

function normalizeEntries(result) {
  if (Array.isArray(result)) return result;
  if (Array.isArray(result?.entries)) return result.entries;
  if (Array.isArray(result?.matches)) return result.matches;
  return [];
}

function sourceName(entry) {
  return (
    entry?.sourceDictionary ||
    entry?.dictionaryTitle ||
    entry?.dictionary ||
    entry?.source ||
    "unknown"
  );
}

function entrySignals(entry) {
  const values = [
    ...(Array.isArray(entry?.tags) ? entry.tags : []),
    ...(Array.isArray(entry?.termTags) ? entry.termTags : []),
    entry?.dictionaryType,
    entry?.category,
    entry?.type,
  ].filter(Boolean).map(String);
  return values.filter((value) => {
    const normalized = value.trim().toLowerCase();
    return LEXICALIZED_EXACT_TAGS.has(normalized) || LEXICALIZED_TAG_PATTERN.test(value);
  });
}

export async function validateAnalyzerCandidates(structure, lookupExact) {
  if (typeof lookupExact !== "function") {
    throw new TypeError("lookupExact must be a function");
  }

  const candidates = structure?.candidates || [];
  const records = [];

  for (const candidate of candidates) {
    const result = await lookupExact(candidate.candidateHeadword);
    const entries = normalizeEntries(result);
    const sources = [...new Set(entries.map(sourceName))];
    const lexicalizedSignals = [...new Set(entries.flatMap(entrySignals))];

    records.push({
      candidateId: candidate.candidateId,
      candidateHeadword: candidate.candidateHeadword,
      exactMatchCount: entries.length,
      sourceCount: sources.length,
      sourceNames: sources,
      lexicalizedEvidence: lexicalizedSignals.length > 0,
      lexicalizedSignals,
      entries: entries.map((entry) => ({
        term: entry.term || entry.expression || entry.headword,
        reading: entry.reading,
        source: sourceName(entry),
        tags: entry.tags || entry.termTags || [],
        dictionaryType: entry.dictionaryType || entry.category || entry.type,
      })),
    });
  }

  return records;
}

export async function finalizeAnalyzerStructure({
  structure,
  lookupExact,
  analyzerBaseUrl = "http://127.0.0.1:8766",
}) {
  const validationRecords = await validateAnalyzerCandidates(structure, lookupExact);
  const response = await fetch(`${analyzerBaseUrl}/finalize-structure`, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ structure, validationRecords }),
  });
  if (!response.ok) {
    throw new Error(`Analyzer validation failed: ${response.status} ${response.statusText}`);
  }
  return response.json();
}
```

#### `src/lib/jpAnalyzerClient.js`

```javascript
/**
 * JP Analyzer browser client.
 *
 * Phase 1:
 * - Check service health.
 * - Analyze a sentence on demand from Debug Mode.
 * - Validate exact source text and resolved-span offsets.
 *
 * This module does not replace Kuromoji or alter reader colouring.
 */

const DEFAULT_BASE_URL = '/api/jp-analyzer';
const DEFAULT_TIMEOUT_MS = 30_000;

export class JpAnalyzerError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'JpAnalyzerError';
    this.details = details;
  }
}

function createRequestSignal(timeoutMs, externalSignal) {
  const controller = new AbortController();

  const timeoutId = window.setTimeout(() => {
    controller.abort(
      new DOMException(
        `JP Analyzer request exceeded ${timeoutMs} ms.`,
        'TimeoutError'
      )
    );
  }, timeoutMs);

  function forwardAbort() {
    controller.abort(
      externalSignal?.reason ??
        new DOMException('Request cancelled.', 'AbortError')
    );
  }

  if (externalSignal) {
    if (externalSignal.aborted) {
      forwardAbort();
    } else {
      externalSignal.addEventListener('abort', forwardAbort, {
        once: true
      });
    }
  }

  return {
    signal: controller.signal,
    dispose() {
      window.clearTimeout(timeoutId);
      externalSignal?.removeEventListener('abort', forwardAbort);
    }
  };
}

async function requestJson(
  path,
  {
    baseUrl = DEFAULT_BASE_URL,
    method = 'GET',
    body,
    timeoutMs = DEFAULT_TIMEOUT_MS,
    signal
  } = {}
) {
  const requestSignal = createRequestSignal(
    timeoutMs,
    signal
  );

  try {
    const response = await fetch(`${baseUrl}${path}`, {
      method,
      signal: requestSignal.signal,
      headers: {
        Accept: 'application/json',
        ...(body !== undefined
          ? {
              'Content-Type':
                'application/json; charset=utf-8'
            }
          : {})
      },
      body:
        body !== undefined
          ? JSON.stringify(body)
          : undefined
    });

    const responseText = await response.text();
    let payload = null;

    if (responseText) {
      try {
        payload = JSON.parse(responseText);
      } catch {
        throw new JpAnalyzerError(
          'JP Analyzer returned a non-JSON response.',
          {
            path,
            status: response.status,
            responsePreview: responseText.slice(0, 500)
          }
        );
      }
    }

    if (!response.ok) {
      throw new JpAnalyzerError(
        `JP Analyzer request failed with HTTP ${response.status}.`,
        {
          path,
          status: response.status,
          statusText: response.statusText,
          payload
        }
      );
    }

    return payload;
  } catch (error) {
    if (error instanceof JpAnalyzerError) {
      throw error;
    }

    const reason = requestSignal.signal.reason;

    if (reason?.name === 'TimeoutError') {
      throw new JpAnalyzerError(
        'JP Analyzer request timed out.',
        {
          path,
          timeoutMs,
          cause: error
        }
      );
    }

    if (error?.name === 'AbortError') {
      throw new JpAnalyzerError(
        'JP Analyzer request was cancelled.',
        {
          path,
          cause: error
        }
      );
    }

    throw new JpAnalyzerError(
      'JP Analyzer is unavailable or could not be reached.',
      {
        path,
        cause: error
      }
    );
  } finally {
    requestSignal.dispose();
  }
}

export async function getAnalyzerHealth(options = {}) {
  return requestJson('/health', options);
}

export async function getAnalyzerOpenApi(options = {}) {
  return requestJson('/openapi.json', options);
}

export async function discoverAnalyzerRoutes(options = {}) {
  const openApi = await getAnalyzerOpenApi(options);

  const routes = Object.entries(openApi?.paths ?? {})
    .map(([path, definitions]) => ({
      path,
      methods: Object.keys(definitions ?? {})
        .map((method) => method.toUpperCase())
        .sort()
    }))
    .sort((left, right) =>
      left.path.localeCompare(right.path)
    );

  return {
    title: openApi?.info?.title ?? '',
    version: openApi?.info?.version ?? '',
    routes
  };
}

export function validateCompactAnalysis(
  compact,
  expectedText
) {
  const sourceText = String(expectedText ?? '');
  const errors = [];

  if (!compact || typeof compact !== 'object') {
    return {
      valid: false,
      errors: ['Compact analysis is not an object.']
    };
  }

  if (compact.text !== sourceText) {
    errors.push(
      'Compact analysis text differs from source text.'
    );
  }

  if (!Array.isArray(compact.resolvedSpans)) {
    errors.push(
      'resolvedSpans is missing or is not an array.'
    );

    return {
      valid: false,
      errors
    };
  }

  let previousEnd = 0;

  compact.resolvedSpans.forEach((span, index) => {
    const label = `resolvedSpans[${index}]`;

    if (!Number.isInteger(span?.start)) {
      errors.push(`${label}.start is not an integer.`);
      return;
    }

    if (!Number.isInteger(span?.end)) {
      errors.push(`${label}.end is not an integer.`);
      return;
    }

    if (
      span.start < 0 ||
      span.end <= span.start ||
      span.end > sourceText.length
    ) {
      errors.push(`${label} has an invalid source range.`);
      return;
    }

    if (span.start < previousEnd) {
      errors.push(
        `${label} overlaps the previous span or is out of order.`
      );
    }

    const expectedSurface = sourceText.slice(
      span.start,
      span.end
    );

    if (span.surface !== expectedSurface) {
      errors.push(
        `${label}.surface does not match its source range.`
      );
    }

    if (
      typeof span.role !== 'string' ||
      !span.role.trim()
    ) {
      errors.push(`${label}.role is missing.`);
    }

    previousEnd = Math.max(previousEnd, span.end);
  });

  return {
    valid: errors.length === 0,
    errors
  };
}

export async function analyzeSentence(
  text,
  options = {}
) {
  const sourceText = String(text ?? '');

  if (!sourceText.trim()) {
    throw new JpAnalyzerError(
      'Cannot analyze an empty sentence.'
    );
  }

  const compact = await requestJson('/analyze', {
    ...options,
    method: 'POST',
    body: {
      text: sourceText
    }
  });

  const validation = validateCompactAnalysis(
    compact,
    sourceText
  );

  if (!validation.valid) {
    throw new JpAnalyzerError(
      'JP Analyzer returned an invalid compact analysis.',
      {
        validationErrors: validation.errors
      }
    );
  }

  return compact;
}
```

#### `src/lib/phase8DictionarySync.js`

```javascript
import { loadTermDictionaryEntriesForMeta, loadTermDictionaryMetas } from './dictionaryStorage.js';
const DEFAULT_URL='http://127.0.0.1:8771';
function compact(entry,meta){const rules=Array.isArray(entry?.rules)?entry.rules:String(entry?.rules||'').split(' ').filter(Boolean);return {term:String(entry?.term||entry?.text||'').normalize('NFKC').trim(),reading:String(entry?.reading||'').normalize('NFKC').trim(),dictionaryId:String(entry?.dictionaryId||meta.id||''),dictionaryTitle:String(entry?.sourceDictionary||meta.title||'unknown'),dictionaryType:String(entry?.dictionaryType||meta.type||'term'),dictionaryPriority:Number(entry?.dictionaryPriority??meta.priority??9999),tags:Array.isArray(entry?.tags)?entry.tags:[],rules,score:Number(entry?.score||0),sequence:entry?.sequence??null,nameType:entry?.nameType||'',grammarType:entry?.grammarType||'',expressionType:entry?.expressionType||''};}
async function request(url,path,options={}){const res=await fetch(`${url}${path}`,{headers:{'Content-Type':'application/json; charset=utf-8'},...options});if(!res.ok)throw new Error(`Dictionary sync failed: ${res.status} ${res.statusText} ${await res.text()}`);return res.json();}
export const getAnalyzerDictionaryStatus=({analyzerBaseUrl=DEFAULT_URL}={})=>request(analyzerBaseUrl,'/dictionary-sync/status');
export const clearAnalyzerDictionaryCache=({analyzerBaseUrl=DEFAULT_URL}={})=>request(analyzerBaseUrl,'/dictionary-sync/cache',{method:'DELETE'});
export async function syncIndexedDbDictionariesToAnalyzer({analyzerBaseUrl=DEFAULT_URL,batchSize=2000,onProgress,signal}={}){const metas=await loadTermDictionaryMetas();const total=metas.reduce((n,m)=>n+Number(m.entryCount||0),0);const started=await request(analyzerBaseUrl,'/dictionary-sync/start',{method:'POST',body:JSON.stringify({expectedEntries:total,dictionaryCount:metas.length}),signal});let sent=0;for(let mi=0;mi<metas.length;mi++){const meta=metas[mi],entries=await loadTermDictionaryEntriesForMeta(meta);for(let i=0;i<entries.length;i+=batchSize){if(signal?.aborted)throw new DOMException('Dictionary sync aborted','AbortError');const batch=entries.slice(i,i+batchSize).map(e=>compact(e,meta)).filter(e=>e.term);await request(analyzerBaseUrl,'/dictionary-sync/batch',{method:'POST',body:JSON.stringify({syncId:started.syncId,entries:batch}),signal});sent+=batch.length;onProgress?.({sent,total,dictionaryTitle:meta.title,dictionaryIndex:mi,dictionaryCount:metas.length});}}const final=await request(analyzerBaseUrl,'/dictionary-sync/finish',{method:'POST',body:JSON.stringify({syncId:started.syncId}),signal});return {...final,sent,expectedEntries:total};}
```

### Remaining JP Analyzer files — content manifest

- `CONSOLIDATED_ANALYZER.md` — 979 bytes — SHA-256 `2e5122570b09ed1bac9744d9237aa981b18e2b70af77381cf6253a6eef092312` — Project documentation.
- `README.md` — 1061 bytes — SHA-256 `fcf72fa570947e45689bb873f1733dc591cfee7e5d8b65d4f57465dc1d5b2d4b` — Repository overview and operating instructions.
- `app/__init__.py` — 0 bytes — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — Python source or utility module.
- `app/analyzer/__init__.py` — 805 bytes — SHA-256 `e243154c70bfe143584d15bb1b35fee66c4103fbbc0df354d72729601ecc143b` — Python source or utility module.
- `app/analyzer/adapters/__init__.py` — 140 bytes — SHA-256 `1fe610e339af091cbfa768e2ad541cd27256c4f310da0d6461a86c46ac9b6b69` — Python source or utility module.
- `app/analyzer/adapters/dictionary_adapter.py` — 748 bytes — SHA-256 `b1ec237ba2308c8fa9bb55b176f90119bef72407740caf2944be68e0af38f5b7` — Dictionary import, persistence, lookup, or integration support.
- `app/analyzer/adapters/kwja_adapter.py` — 898 bytes — SHA-256 `5ae0e0c2b8dc63eae642a8d05c6c964b3e4aa0d095f94bf827949c174bd67f73` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/config.py` — 694 bytes — SHA-256 `0572e92dc2906ae581691eb1fdcca535b018ed4977d5fc40952bd19b5399b77a` — Python source or utility module.
- `app/analyzer/ginza_runtime.py` — 1013 bytes — SHA-256 `f0d5b6805e86d0b54c33b706a2f41c87c0078c6dd9102b8e13025cc6fd1dec59` — Reusable analyzer runtime and configuration management.
- `app/analyzer/health.py` — 671 bytes — SHA-256 `1bbb5ff7b2e7503ab518772734e2e9af2c6267b2efd291fcd575bd560543ad65` — Health/readiness reporting for analyzer runtime and dictionaries.
- `app/analyzer/kwja_runtime.py` — 1035 bytes — SHA-256 `0dc0f43310f3f535c5a51369dba7b929f6e2fec12774e84e1ee69120d2230a0e` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/layers/__init__.py` — 173 bytes — SHA-256 `bab045ddb0d59383153376d73259cd7fe2323db6bb373f637979cd03e73fab87` — Python source or utility module.
- `app/analyzer/layers/candidates.py` — 14030 bytes — SHA-256 `0593de79bc20537e2a0668e673b5429c116cbf9c7594e4119074287483ec363f` — Python source or utility module.
- `app/analyzer/layers/grammar.py` — 2062 bytes — SHA-256 `cac8c93043717fd27fac9a57064588acbc6a170c812d62f3af69564694867bdc` — Python source or utility module.
- `app/analyzer/layers/invariants.py` — 5515 bytes — SHA-256 `03f9d5482d133d5888b8df3304dfa8ced196516322511dc514735df160d3cac4` — Python source or utility module.
- `app/analyzer/layers/kwja.py` — 16074 bytes — SHA-256 `efe44b02d5598926c846dcf5b2d9f719cf2d10950913cda0fcaa918f57c04054` — KWJA integration, runtime handling, or related validation.
- `app/analyzer/layers/morphology.py` — 9831 bytes — SHA-256 `56b991e10c6bb3d1232911ed1acd56b4418920ff6397f6889ce0edd27584934c` — Python source or utility module.
- `app/analyzer/layers/protected.py` — 11156 bytes — SHA-256 `43d146fa3ff6773b5e661d34c918f979aeca4a8f821e4fe1cab932294e04acf6` — Python source or utility module.
- `app/analyzer/layers/schema.py` — 3909 bytes — SHA-256 `abdcc0d625f144940a43b5bf07f878fad4a909f01d953ae04dce2c3d880fa5d0` — Python source or utility module.
- `app/analyzer/layers/stabilization.py` — 6084 bytes — SHA-256 `2fb025b8b6680ac67e961605bf208f17fc3087672d6aaa047cfdfb198ad847d7` — Python source or utility module.
- `app/analyzer/layers/structure.py` — 8720 bytes — SHA-256 `86243871cfebff2f40f6e1b286d1348f2b544f41d727814570e72569c7b905ba` — Python source or utility module.
- `app/analyzer/semantic_snapshot.py` — 1638 bytes — SHA-256 `c805d66ee21816a1e84beb220bef86b28960e89c2af3a8eeef5fa78fc55a8028` — Python source or utility module.
- `app/analyzer/services.py` — 394 bytes — SHA-256 `85ef48e63be3f8747820e04978e83dd124685d1540aa80b353df185f3b0e40a7` — Python source or utility module.
- `app/analyzer/source_contract.py` — 1445 bytes — SHA-256 `aaa8493a6adb2d8d9dc5eff7ef6f0e941b0c96d73e59a73684f2b7feddd6eeb1` — Python source or utility module.
- `docs/KWJA_SETUP_WINDOWS.md` — 1009 bytes — SHA-256 `4f1afa87db391b26bd6f5e88ba8a0a834421889831fcfdb40bcbd8bf93c1cac9` — KWJA integration, runtime handling, or related validation.
- `docs/READER_PROJECTION_CONTRACT.md` — 3166 bytes — SHA-256 `558629abe4f478c7725a53a29bbe09482c93e1ef58d9054bf8ed48352835cfb6` — Projects analyzer spans into authoritative reader-facing spans and validates coverage.
- `evaluation/ANNOTATION_GUIDELINES.md` — 2639 bytes — SHA-256 `c4a78dd5923d6e1bdd9c189bd7a8bb05fe5e8cde770edb9e7c44a5a54b739b96` — Project documentation.
- `evaluation/ERROR_TAXONOMY.md` — 1146 bytes — SHA-256 `a712073b868fceba3282925f052542e02f42d824ef0dcd6ae09b4a371cc22387` — Project documentation.
- `evaluation/PACKAGE_MANIFEST.json` — 1623 bytes — SHA-256 `7f09234de401dd942515626459731bd16c9685ed264454feb8885876d973fca5` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/README.md` — 1626 bytes — SHA-256 `7d07ccdbd3e32a6a3d2e2d8d225fd838daa7c725bdc827944066931eac5e2ce8` — Repository overview and operating instructions.
- `evaluation/schemas/corpus_record.schema.json` — 859 bytes — SHA-256 `43935de11592f28cb8fd471cccc980e9f0bd087afebab4113897eb08c842627d` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/schemas/gold_annotation.schema.json` — 2798 bytes — SHA-256 `adfdda08bfcc79d30300748fb278c4562da64e7f6c3233c5f01940dc114c3772` — Data, fixture, manifest, snapshot, or configuration.
- `evaluation/scripts/enrich_baseline_compact.py` — 2285 bytes — SHA-256 `8c6ffb6e6487c48d915ee7302d1bf8834323f31bb4926ddb509733081fbfa639` — Python source or utility module.
- `evaluation/scripts/inspect_accuracy_baseline.py` — 3657 bytes — SHA-256 `a2ecc1df910265d60c515f59f97ba498f362bb811ad917fe65a8167e2172da04` — Python source or utility module.
- `evaluation/scripts/inspect_compact_keys.py` — 1623 bytes — SHA-256 `46e6abca7cc514248e558857cc8661901a76875218d392077dcd37cb9602140e` — Python source or utility module.
- `evaluation/scripts/make_annotation_batches.py` — 1292 bytes — SHA-256 `1a20fa8e84f553f1ddfa6a2b3dd03edc209918df79ae4cc821b9118d4a4887e3` — Python source or utility module.
- `evaluation/scripts/run_baseline.py` — 3765 bytes — SHA-256 `27c333a84b83e3c87cda0e487bc50eeb3a9f70c7f08beb5e99f88992bbd63963` — Python source or utility module.
- `evaluation/scripts/score_accuracy.py` — 6130 bytes — SHA-256 `ff37b0a6c8c1752108777de568145097ca3223141bf6102b5734b71e551d100e` — Python source or utility module.
- `evaluation/scripts/score_annotations.py` — 2272 bytes — SHA-256 `c94c2d1ccfdbf4ef9067d1229dd4720a9db40c7d9e901075311db48857b73bc5` — Python source or utility module.
- `evaluation/scripts/validate_gold.py` — 1212 bytes — SHA-256 `2452dd2d75011d51b2ede122a3cb0dcabc73766ac9b506f913f45b185d694c0d` — Python source or utility module.
- `evaluation/templates/change_record.json` — 303 bytes — SHA-256 `03d7be6fa333870c019d6ca3074afad2a9f3dcf51b2c5f4b8dc8f0c822b392bf` — Data, fixture, manifest, snapshot, or configuration.
- `requirements-frozen-py311.txt` — 1023 bytes — SHA-256 `a7e463ebdcf1c92c108db2c013ee0c9beda3aeae92d0bf6c80c0b1311b2bbbb1` — Dependency and build/runtime configuration.
- `run_snapshot_regression.py` — 3332 bytes — SHA-256 `34c6b5b98f982a8b6f8702d0a3b7b33f1bf64292f035057eb36d0ba4cda78e53` — Python source or utility module.
- `scripts/setup_kwja_windows.ps1` — 511 bytes — SHA-256 `d88cc37b3440bf30c333a15b4658bd48647d52d722d0c0a8a921989ab812140e` — KWJA integration, runtime handling, or related validation.
- `tests/__init__.py` — 0 bytes — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — Automated regression/contract test.
- `tests/corpora/README.md` — 1212 bytes — SHA-256 `ce8c59c1fcd3b417d65106adc1d3ceb35cad827ca594d39ba5492e675af635f6` — Repository overview and operating instructions.
- `tests/corpora/development/random_sentences.txt` — 17647 bytes — SHA-256 `b074dc201ea445bd8d0f349c15bbe87af303281ffea814571bb1774d9b6ed3ca` — Automated regression/contract test.
- `tests/corpora/parity/consolidation_fresh_unseen_200.txt` — 22543 bytes — SHA-256 `5fec594ffe3b3c3159e53db965d959054af54bdfdcef91ec1145845772ac6955` — Automated regression/contract test.
- `tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json` — 552 bytes — SHA-256 `55816540e341f62a17205e1800a6fde67984d02303dbce44790f3c63be058e7d` — Automated regression/contract test.
- `tests/fixtures/single_case_semantic_reference.json` — 7839 bytes — SHA-256 `574121c0b509db1fcd5a8306af51689b4d415f7a0af89f605a346c4524eb5d0d` — Automated regression/contract test.
- `tests/test_decision.py` — 3205 bytes — SHA-256 `96c88170c0390d2bd006c47a50b8d3b2e18c5857f3d76df421404167e54e781d` — Candidate normalization, scoring, conflict resolution, and explainable decisions.
- `tests/test_dictionary_adapter.py` — 501 bytes — SHA-256 `ad3f15c285dd0c3a185a623a03ffbf5e003326114f1e5cd63b7a0ba76db5d867` — Automated regression/contract test.
- `tests/test_dictionary_evidence.py` — 4427 bytes — SHA-256 `82c8a811096d4ebb08c9f85ef411a80d254d963037999d584ffa05261e0ce141` — Automated regression/contract test.
- `tests/test_dictionary_path.py` — 459 bytes — SHA-256 `c01ce0a324df703fcfc9d831e54e9763fd040cfc01a0a7b9908fb1bfe74890ec` — Automated regression/contract test.
- `tests/test_engine_routing.py` — 1648 bytes — SHA-256 `46d8a3ba0856e1930d69e9e77a37532df7336dfc1cd701b9aba3bfa230a1d49b` — Single-pass analyzer engine façade and runtime execution.
- `tests/test_evidence_routing.py` — 2021 bytes — SHA-256 `c3c60f8d2f5e6ad85cc0812e70ffcfcfccc57cfb474eba7817f5f26992fb2c93` — Automated regression/contract test.
- `tests/test_facade.py` — 1531 bytes — SHA-256 `67e0e55c67cd09b2a6c2b56f02b4b0f8ad5060bc7561fa6bf25d9530a8b72e46` — Automated regression/contract test.
- `tests/test_health_contract.py` — 810 bytes — SHA-256 `4a0e13bd70ff165abd1a1b81bfe74bca51af6eab9379720e9154d5023e7bfec9` — Health/readiness reporting for analyzer runtime and dictionaries.
- `tests/test_import_boundary.py` — 665 bytes — SHA-256 `ad5693a212a9a78c18b79958686459bee1c3edcd6ea6141f533d994827e62082` — Automated regression/contract test.
- `tests/test_kwja_adapter.py` — 537 bytes — SHA-256 `e34c28992d459e0822498215f72b93fdb11697fb58efe61106cd32dac7eedd70` — KWJA integration, runtime handling, or related validation.
- `tests/test_kwja_timeout.py` — 1731 bytes — SHA-256 `27aa587eb617d79d91197042d42e61bbee8d66b4c1d66275d70df6bc1b1d59d1` — KWJA integration, runtime handling, or related validation.
- `tests/test_no_legacy_imports.py` — 705 bytes — SHA-256 `1e62f41e2a4cbdbb3d6d9aaf622f7b3fd433b73a997aeb3c9556210adeafd58d` — Automated regression/contract test.
- `tests/test_reader_projection_contract.py` — 3313 bytes — SHA-256 `63b878774ae19603ba1d024283a5d49f56ea33818a86b62bad1b0aef345a9c88` — Projects analyzer spans into authoritative reader-facing spans and validates coverage.
- `tests/test_runtime_contracts.py` — 957 bytes — SHA-256 `6c1b501f0385e95b1b7e241f5c10641bb1572fa93ee120cd910db2a375c6cdab` — Reusable analyzer runtime and configuration management.
- `tests/test_runtime_reuse.py` — 601 bytes — SHA-256 `90ae6a8ee49d3218a9d085c1a673294a4ce4125df41554d97fd6114ae99d3e0a` — Reusable analyzer runtime and configuration management.
- `tests/test_semantic_snapshot.py` — 1097 bytes — SHA-256 `eaf526c3c3998edf88128f048801230de844fbcf6f3a16fac5382a07da95d2f7` — Automated regression/contract test.
- `tests/test_single_pass.py` — 771 bytes — SHA-256 `535c46e5dd5a03b3ae6e04b3610259bbe68761fe7f9ef20c77ad1607ecd32a7f` — Automated regression/contract test.

### Remaining Novel Audio Miner files — content manifest

- `FINAL_STABLE_STATUS.md` — 2863 bytes — SHA-256 `1ac1fbfb34f027183dc60c67dad212f3957b5d0dd2c9ed855785838a5a4b4edc` — Project documentation.
- `LOCAL_DATA_MANIFEST.example.json` — 372 bytes — SHA-256 `bb564daf88208dbc94cfd3a885dbf63746788cb147ccaf6627e572d9352a439a` — Data, fixture, manifest, snapshot, or configuration.
- `PROJECT_STRUCTURE.md` — 3030 bytes — SHA-256 `f329ab81ce6a78991cf0654082d7fb55f63a4a853cc6e9da0f35b1f15b676768` — Project documentation.
- `README.md` — 3581 bytes — SHA-256 `a416acdfb86857e68bd7ac8967a61a079376dc107b111c8c3a596710e233de47` — Repository overview and operating instructions.
- `RELEASE_CHECKLIST.md` — 2807 bytes — SHA-256 `ce9264ede71ba2bb6b958b17ab0f4b20d732b57b400a45af1d57e79be8b3007f` — Project documentation.
- `STABILIZATION.md` — 6098 bytes — SHA-256 `ef777bad9beecff78e8c47c4533c2eb77e655834a88609415996988b15297ef7` — Project documentation.
- `WORD_MODEL_POLICY.md` — 2326 bytes — SHA-256 `52994df2185c936160789643f0887cbad5fc19e03e86c330872e81aa4a80bec5` — Project documentation.
- `index.html` — 507 bytes — SHA-256 `54496c2b898d8f019825f78ca0dac53170af7c670a6ba6ff25c186154c8a3243` — Project file.
- `package-lock.json` — 35159 bytes — SHA-256 `408898ba226b525d07ac575c50a0b7cf945338a34c4ae302d90f4fc4ed2fd75a` — Data, fixture, manifest, snapshot, or configuration.
- `public/dict/user_dictionary_seed.json` — 798 bytes — SHA-256 `e8c3fff4439b237ce64a83f777f609cc29a917fcfd286b1eca09696f7fb93d25` — Dictionary import, persistence, lookup, or integration support.
- `src/App.jsx` — 1160 bytes — SHA-256 `a1eead4a27bcbfb2026b94ad64e96ea661f628fb42bd8d3e41e5cdd38140e9b1` — Application source module.
- `src/components/DictionaryDebugPanel.jsx` — 42641 bytes — SHA-256 `40fa3e05908736bd7cc70f69bdbb25fb21b90ab1615a6c48fb2fb1c6c7289eed` — Dictionary import, persistence, lookup, or integration support.
- `src/components/FileLoader.jsx` — 780 bytes — SHA-256 `d04564c7aa49684a1ae63566a5f87cccd43c8aa9a6c057ad774957cfc069237c` — Application source module.
- `src/components/JpAnalyzerIntegrationPanel.jsx` — 11374 bytes — SHA-256 `937ae88fedc8d833496a917dc0c87b9c1c3528cceb26d2b5f97b2075a826d435` — JP Analyzer browser client, integration UI, validation, or diagnostics.
- `src/components/Phase8DictionarySyncPanel.jsx` — 2235 bytes — SHA-256 `9e047339d1bff0b5cd30cbf8d0226a4e7d0e3e497663b67dd10ccd3e194384b7` — Synchronizes frontend dictionaries into JP Analyzer.
- `src/lib/ankiConnect.js` — 1720 bytes — SHA-256 `a32bb91991fa25724ff32c541a4e76233224eded2744e63af41a5ef9edc5a1c0` — AnkiConnect/mining integration.
- `src/lib/dictionaryDetection.js` — 17790 bytes — SHA-256 `25ff52f8388c33bf475af42463bf68f40486d6f76bba5a23fa6c40feb725d603` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/dictionaryLookup.js` — 35341 bytes — SHA-256 `83a45364c35e0e388c98b95b8809d396facb01a0829ba64c813c4f3f741a1159` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/dictionaryStorage.js` — 6668 bytes — SHA-256 `32ed043b365e7ce6c68f813863c0521903105d1ff9fff9c5e1a16e04d5686c94` — Dictionary import, persistence, lookup, or integration support.
- `src/lib/enrichService.js` — 7990 bytes — SHA-256 `534da9370a40fad6a0f11ac68ab97dabdefc753e00de3da5a44b6070c68477f1` — Application source module.
- `src/lib/epubParser.js` — 17008 bytes — SHA-256 `b64ec65b110fa6a5ae9df37242606ce59611e3504f9fed023a78ba8b6bf9b36d` — EPUB parsing, text/ruby extraction, or book navigation.
- `src/lib/frequencyMap.js` — 5286 bytes — SHA-256 `87b5cb0bd60d33399901fe2f87a2d88ac86bae90e9dc293aa7e0059b9b720b9b` — Application source module.
- `src/lib/japaneseSentenceSplitter.js` — 2383 bytes — SHA-256 `b080d45b6dbe17a4077fbd1e07d5c9b3c0522fefc2ab296055e37c93557d3e0e` — Application source module.
- `src/lib/storage.js` — 866 bytes — SHA-256 `9d37c2cb67b10b366493c51ff7605aa34cc6030df1afce986e7a5ce9caa2ed43` — Application source module.
- `src/lib/tokenizer.js` — 2560 bytes — SHA-256 `9eb6fa15ab9a140eedbadf22a1c39078875dcf9fd6b787b8daa1e9f158eb19fc` — Application source module.
- `src/lib/useJpAnalyzerShadow.js` — 7108 bytes — SHA-256 `9bbd2cd1ded6412879d02ce2599ee7e8b4690ca46775debc0c417019dfcbb2d9` — Runs/caches active-scene JP Analyzer requests in shadow mode.
- `src/lib/wordCache.js` — 6299 bytes — SHA-256 `9736d0cf5b2bdc96c5066037430246e49c4cbbdaddf7b797d4f3db2a4ec14236` — Application source module.
- `src/lib/wordModel.js` — 5777 bytes — SHA-256 `26ebe879c3e46e67b6d37b4527eb25de19247cf0fc689be8f794fcb2a55235eb` — Application source module.
- `src/main.jsx` — 347 bytes — SHA-256 `e0184dd19789caef1e69388a6ae7ca5a2b92d4178f387a23605087edbe0bfa7f` — Application source module.
- `src/styles.css` — 15520 bytes — SHA-256 `12ac06479184d08483d1cc10006a0df6b60e0cc5cf6424e480dbf33dbbfc5af6` — Application styling.
- `vite.config.js` — 951 bytes — SHA-256 `b5e57218b58ac8d806da358443a5abfc5618444a59a3fcac593427fcb9024354` — Application source module.

## 5. Key Architecture & Design Decisions

### Layerization and boundaries

JP Analyzer uses a non-destructive layered design. Earlier layers create immutable evidence; later layers may evaluate and select but must not silently rewrite earlier facts. The broad flow is morphology → structural/predicate evidence → grammar/entities/dictionary/KWJA evidence → normalized resolver candidates → exclusive compatibility spans → reader candidate generation → candidate-specific dictionary and structural evaluation → conservative reader selection → exact corrections → compact contract.

The decider/resolver must explain every selection through utility/evidence dimensions. Dictionary evidence remains evidence-only, and a dictionary miss is not rejection. Candidate generation is separate from candidate evaluation, so evidence attached to components is never treated as proof of a newly generated compound.

### Sudachi, GiNZA, Kuromoji, and KWJA

- **Sudachi/SudachiPy:** Japanese morphological/tokenization support inside the analyzer stack and normalization pipeline where configured.
- **GiNZA / spaCy:** primary morphology, POS, dependency, predicate, and sentence-level linguistic analysis used by JP Analyzer.
- **KWJA:** read-only, cache/offline-capable structural evidence; provides phrase/predicate support and grammar/relationship evidence. KWJA does not directly overwrite morphology or force reader spans.
- **Kuromoji:** legacy frontend tokenizer. It currently remains the production reader source and explicit rollback/comparison path, but no new linguistic functionality should be added. It will be retired only after the analyzer path is complete.

### JP Analyzer consolidation

`AnalyzerEngine` runs the consolidated analyzer once per request. `pipeline.py` chooses full or compact output. The compact output exposes stable schemas and includes `resolvedSpans` for compatibility/diagnostics, `readerCandidates` for alternatives, `readerSelection` for audit, and final correction-aware `readerSpans` for consumers.

### Data flow from novel upload to colour

```text
EPUB upload
  → parse spine/chapters/scenes, preserve plain text and ruby/furigana
  → choose active sentence/scene
  → POST exact sentence text to JP Analyzer /analyze
  → validate response text and authoritative readerSpans
  → for each lexical span, resolve user-known/frequency state using analyzer keys
  → render exact source offsets without merging/splitting/search fallback
  → function/grammar/name/punctuation/unresolved use analyzer-supplied role policy
  → Yomitan remains available over selectable Japanese text
  → later: comprehension/New Words/mining use analyzer eligibility flags
```

### Special integrations

- **Yomitan:** external/user-facing dictionary lookup and Anki mining workflow; no duplicate “change lookup word” teaching action.
- **AnkiConnect:** final card creation/integration endpoint in the mining workflow.
- **VoiceVox:** local speech/audio generation where configured; fallback behavior belongs to audio integration, not the analyzer.
- **Nadeshiko:** preserve any existing enrichment/translation role in Novel Audio Miner; do not mix its behavior into linguistic span ownership.
- **Teaching:** frontend selects exact source ranges and structural actions; JP Analyzer validates, derives identities from evidence, previews, saves, applies, audits, and deactivates corrections.

## 6. Known Bugs, Limitations & Test Results

### Known limitations

- Old Novel Audio Miner preview consumes `resolvedSpans`; it may show bare stems and auxiliaries rather than complete reader units.
- The old frontend adapter performs role/category inference that is now explicitly owned by JP Analyzer.
- Teaching currently supports exact occurrence scope; automatic global generalization is deliberately disabled.
- `split` is reserved for the later frontend workflow even if the backend action vocabulary mentions it.
- JP Analyzer dictionary and KWJA readiness affect evidence quality; failure must lead to abstention or neutral output, not guessed merges.
- Local correction SQLite data is not committed and must be backed up separately if permanent personal teaching history matters.
- The current Novel Audio Miner source export should be regenerated from live commit `116d961` before creating a patch if the export metadata differs.

### Representative validated reader results

- `彼は静かに頷いて答えた。` → `彼 | は | 静かに | 頷いて | 答えた | 。`
- `二人は部屋から出て行った。` → `二人 | は | 部屋 | から | 出て行った | 。`
- `最後まで読み終わった。` → `最後 | まで | 読み終わった | 。`
- `少年は突然走り出した。` → `少年 | は | 突然 | 走り出した | 。`
- `本を読んで寝た。` → `本 | を | 読んで | 寝た | 。`
- `窓を開けて空気を入れた。` → `窓 | を | 開けて | 空気 | を | 入れた | 。`
- `二人で歩いた。` → `二人 | で | 歩いた | 。`
- `二十歳になった。` → `二十歳 | に | なった | 。`
- `十歳になった。` → `十歳 | に | なった | 。`
- Taught exact occurrence: `少年が走ってきた。` → `少年 | が | 走ってきた | 。` with internal `TE_KURU`, host `走る`, and grammar focus `てきた`.

### Test status

- JP Analyzer consolidated tests passed after candidate generation, safeguards, dictionary evaluation, structural evidence, numeric normalization, conservative selection, and structural teaching changes.
- Contract tests verify exact offsets, source reconstruction, no overlap, valid roles, lookup-key requirements for lexical spans, and schema versions.
- Teaching lifecycle validation passed: baseline → preview → save → corrected `/analyze` → other sentence unaffected → deactivate → baseline restored.
- A 200-sentence development corpus and a separate 200-sentence consolidation/parity corpus exist for regression stability. These corpora validate consistency, not full linguistic accuracy.
- A larger authentic-novel accuracy corpus and scripts for scoring/annotation are present for later tuning.

## 7. Dependencies & Environment

### Languages and runtime

- Python 3.11 is the expected JP Analyzer/KWJA Windows runtime.
- Node.js/npm are used for Novel Audio Miner; use the version declared by repository tooling/package metadata when present.
- PowerShell is used for local setup, testing, and launch commands on Windows.

### Core Python dependencies

The repository requirements include FastAPI, Uvicorn, SudachiPy/SudachiDict, spaCy, GiNZA, ja_ginza, and Pydantic. The KWJA environment uses KWJA, PyTorch, and Transformers with pinned versions in `requirements-kwja-py311.txt`. See the embedded requirement files above for the exact current pins.

### External/runtime services

- KWJA executable: `D:\Mining\KWJA evaluator\.venv\Scripts\kwja.exe`
- JP Analyzer service: FastAPI/Uvicorn on `127.0.0.1:8766`
- AnkiConnect: expected for Anki mining when enabled.
- VoiceVox: expected local audio/TTS integration when enabled.
- Yomitan: browser dictionary/mining integration.
- Kuromoji: temporary legacy frontend tokenizer until final retirement.

### JP Analyzer environment setup

```powershell
Set-Location "D:\Mining\JP analyzer"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$env:PYTHONPATH = "D:\Mining\JP analyzer"
$env:KWJA_EXE = "D:\Mining\KWJA evaluator\.venv\Scripts\kwja.exe"
$env:HF_HUB_OFFLINE = "1"
$env:TRANSFORMERS_OFFLINE = "1"
$env:HF_DATASETS_OFFLINE = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
& ".\.venv\Scripts\python.exe" -m uvicorn app.analyzer.service:app --host 127.0.0.1 --port 8766
```

Test JP Analyzer:

```powershell
Set-Location "D:\Mining\JP analyzer"
& ".un_tests.ps1"
```

### Novel Audio Miner setup

```powershell
Set-Location "D:\Mining
ovel-audio-miner"
git switch feature/jp-analyzer-integration
npm.cmd install
npm.cmd run build
npm.cmd run dev
```

Before development, verify:

```powershell
git -C "D:\Mining\JP analyzer" status --short --branch
git -C "D:\Mining
ovel-audio-miner" status --short --branch
git -C "D:\Mining\JP analyzer" rev-parse HEAD
git -C "D:\Mining
ovel-audio-miner" rev-parse HEAD
```

Expected checkpoints:

```text
JP Analyzer:       032182a24247da4cc68274ccda2b1aca2ff4d871
Novel Audio Miner: 116d961 (feature/jp-analyzer-integration)
```

## 8. Exact Resume Instructions

A new AI must treat this snapshot and the two Git repositories as the source of truth. Do not repeat Phase 2, do not add new frontend linguistic rules, and do not continue improving the old `resolvedSpans` adapter. Confirm that JP Analyzer is at commit `032182a` and Novel Audio Miner is at `116d961` on `feature/jp-analyzer-integration`. Regenerate a fresh Novel Audio Miner source export from the live repository if necessary. Then implement the smallest Phase 3 patch: introduce a thin, fully validated `readerSpans` adapter; point the existing safe visual preview to authoritative correction-aware `readerSpans`; preserve offsets and analyzer fields exactly; retain the old `resolvedSpans` adapter only for diagnostics; and leave comprehension, New Words, mining, and default production ownership unchanged until the preview is manually validated. If any current files are missing from this snapshot, ask the user to upload a fresh repository export rather than guessing.

---

## Appendix A — Canonical invariants

- JP Analyzer owns linguistic boundaries and roles.
- Novel Audio Miner never merges or splits authoritative analyzer spans.
- Every span uses exact source offsets and exact source surface.
- Reader spans are contiguous, non-overlapping, and reconstruct the sentence.
- Dictionary miss is not rejection.
- Component dictionary evidence is not proof of a complete generated compound.
- Generated candidates receive candidate-specific dictionary and structural evaluation.
- Ambiguity may produce abstention/unresolved neutral output.
- User corrections are exact occurrence data, not automatic global rules.
- Yomitan owns lookup; teaching focuses on structure.
- Analyzer failure/invalid reader contract falls back to neutral text, not guessed surface search.
- Kuromoji remains an explicit temporary legacy mode only.

## Appendix B — Source export provenance

- JP Analyzer export file used: `jp-analyzer-phase2-source.json`; embedded metadata commit: `bbc30eb45a87b8adf662cf9951ab3a8cb8319a89`; file count: `84`.
- Novel Audio Miner export file used: `novel-audio-miner-source.json`; embedded metadata commit: `b113af23a34a5932fc730161a13bcfd2ea633052`; file count: `38`.
- If the Novel Audio Miner embedded commit is not `116d961`, regenerate the export before modifying code; the Git log supplied by the user confirms `116d961` is the live branch checkpoint.
