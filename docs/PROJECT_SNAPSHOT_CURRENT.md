# Project Snapshot – Japanese Novel Mining App

**Snapshot date:** 24 July 2026, IST  
**JP Analyzer:** `main` at `0b00fbd5ae1bdb1106a5c16199f3c9b862315fdf`  
**Novel Audio Miner:** `feature/jp-analyzer-integration` at `2d2569771cb44ba28f794a82e4e047adfc7051ac`  
**Canonical location:** `D:\Mining\JP analyzer\docs\PROJECT_SNAPSHOT_CURRENT.md`  
**Status:** This snapshot supersedes all earlier project snapshots. It was generated from the complete current tracked source exports, current Git metadata, live analyzer health/OpenAPI output, dictionary status, and current test/build results.

> **Working-tree note:** Novel Audio Miner was clean. JP Analyzer had one untracked local utility, `direct_analyzer_timing.py`; it is embedded below for completeness but is not part of commit `0b00fbd`. Runtime SQLite contents are intentionally not embedded.

## 1. Purpose & Goal

The project is a local Japanese EPUB reading and mining application. Its finished form should load Japanese novels, preserve spine order, chapters, illustrations, original sentence text and ruby/furigana, analyze each sentence into coherent learner-facing units, colour those units from known-word and frequency state, calculate comprehension, expose New Words, preserve Yomitan lookup, and support reliable Anki mining with existing Nadeshiko and VoiceVox enrichment paths.

The intended ownership model is:

- **JP Analyzer** owns linguistic boundaries, reader roles, compounds, grammar identity, names, lookup identities, candidate generation/evaluation, conservative abstention, and structural teaching corrections.
- **Novel Audio Miner** owns EPUB parsing, exact-offset rendering, known/frequency resolution, navigation, illustrations, audio, comprehension/New Words presentation, selection, diagnostics, dictionary synchronization UI, and mining workflow.
- **Yomitan** owns interactive dictionary lookup, reading/definition choice, and the user-facing dictionary/Anki workflow.

The frontend must consume authoritative `readerSpans` mechanically. It must not merge or split them, infer linguistic roles, invent lookup identities, or use surface-search fallback when exact analyzer offsets exist. Invalid analyzer output must render neutrally and produce diagnostics rather than guesses.

## 2. Where We Are Now (Current Phase)

### Exact current phase

**Phase 7 — Dictionary management.** Persistent analyzer dictionary storage is already operational; current work should refine and verify the settings-driven synchronization and management lifecycle rather than reimplement persistence.

### Consolidation and roadmap progress

- **Phase 1 — Ownership, consolidation, and safe baseline: complete.**
- **Phase 2 — Authoritative reader-facing analysis: complete.** `readerSpans`, reader candidates, conservative selection, lookup hypotheses, structural evidence, exact corrections, and correction revision are active.
- **Phase 3 — Frontend integration: complete.** The current branch renders validated authoritative reader spans, uses analyzer-supplied lookup identities, supports colour-source ownership, maintains correction-aware cache identity, metadata leases, and adjacent-scene prefetch.
- **Phase 4 — Presentation refinement: complete.** Analyzer roles drive lexical, function, grammar, name, punctuation, unresolved, known, and frequency presentation.
- **Phase 5 — Comprehension, New Words, and mining eligibility: complete.** JP Analyzer is the active learning and mining-eligibility source; offset-aware selection/mining is active.
- **Phase 6 — Simplified Debug Mode: complete.** Debug report schema v2, diagnostic IDs, analyzer/cache/prefetch/learning/mining/EPUB sections, and optional full EPUB parser inventory are implemented.
- **Original Phase 11 — Retire Kuromoji: completed early in Phase 5.2E.** Kuromoji and the legacy tokenizer model are removed from production and from dependencies; Plain Text remains a presentation mode using JP Analyzer structure.

### Current verified runtime

- Analyzer version: `11.9.0-correction-aware-cache-contract`
- Compact schema: `1.2`
- Reader span schema: `1.1`
- Engine contract: `9.0.0-alpha2.2-evidence-gated-decision`
- Correction revision: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- GiNZA model: `ja_ginza`
- KWJA: available, base model, executable `D:\Mining\KWJA evaluator\.venv\Scripts\kwja.exe`
- Dictionary: ready, 4,223,665 entries across 24 dictionaries
- Dictionary types: {'expression': 55377, 'grammar': 5411, 'name': 667480, 'term': 3495397}
- Persistent database: `D:\Mining\JP analyzer\data\phase8_analysis_lexicon.sqlite3`
- User confirmation: the analyzer dictionary remains available in the current persistent database.
- User clarification: the earlier tick referred to **Include all EPUB parser data**. The exported reports correctly recorded `fullParserInventoryIncluded: true`; this is resolved and is not a bug.

### Remaining Phase 7 tasks

1. Rename historical `Phase8DictionarySyncPanel` / `phase8DictionarySync` identifiers to phase-neutral dictionary-management names without changing behavior.
2. Make dictionary lifecycle clearly settings-driven: status, initial sync, manual resync, progress, cancellation, clear, and recovery.
3. Avoid unnecessary full resynchronization during ordinary reading; compare frontend dictionary snapshot identity with analyzer status before syncing.
4. Surface entry count, dictionary count, type counts, last sync ID, database path, and error state in settings and debug report.
5. Strengthen atomic sync behavior for interrupted uploads, stale staging data, validation of expected versus received entries, and preservation of the last valid live lexicon on failure.
6. Add dedicated automated coverage for dictionary persistence/restart, synchronization identity, cancellation, retry, cache clear, and mismatch recovery.
7. Keep Yomitan dictionary management independent and avoid introducing a competing dictionary UI.

### Remaining original roadmap

- **Phase 8 — Teaching frontend:** exact range selection, inspect partition, preview/save/deactivate corrections, and actions for one unit, split, vocabulary, grammar, function, name, neutral, and undo.
- **Phase 9 — Correction data and ranker tuning:** collect accepted/rejected candidates and evidence snapshots; exact corrections apply immediately, global changes only after offline validation.
- **Phase 10 — One-application startup:** one launcher starts analyzer, locates KWJA, opens dictionaries, starts frontend, checks health, and shuts down children cleanly.
- **Phase 12 — Reading-driven maintenance:** classify findings as teaching correction, analyzer bug, dictionary gap, EPUB issue, or display-policy issue.
- **Phase 11 is no longer pending:** Kuromoji retirement has already been completed.

### Known issues and unfinished items

- JP Analyzer contains untracked `direct_analyzer_timing.py`; decide whether to commit it as an intentional performance utility or remove it before treating the analyzer working tree as clean.
- Two dictionary database files exist: the active large database under `data/` and a small `app/data/phase8_analysis_lexicon.sqlite3`. The active health result points to the root `data/` database; the small duplicate should be audited and removed or documented to avoid path confusion.
- The snapshot-regression runner was invoked without required `input_file` and `--reference` arguments. This is a collector invocation error, not a regression failure.
- Novel Audio Miner has dedicated phase test scripts but no generic `npm test` script. The production build passed, but the collector did not execute the dedicated phase suites.
- Current OpenAPI response schemas for several endpoints are `{}`. Typed response models would improve API documentation and consumer validation.
- Teaching backend exists, but the complete teaching frontend remains Phase 8 work.

### Next immediate action items

1. Replace `D:\Mining\JP analyzer\docs\PROJECT_SNAPSHOT_CURRENT.md` with this file and commit it on JP Analyzer `main`.
2. Audit Phase 7 dictionary UI and synchronization against the remaining tasks above.
3. Run all dedicated Novel Audio Miner test scripts (`npm run test:phase5` covers the integrated Phase 3–6 chain) and record the result before Phase 7 code changes.
4. Run snapshot regression with its required corpus and reference arguments; do not call it with no arguments.
5. Resolve the duplicate small analyzer database and the untracked timing utility.
6. Implement Phase 7 in small, independently tested commits.

## 3. Full Project File Structure

Every source file captured from the current working trees is listed below. Runtime databases are listed separately because their contents are local and intentionally excluded.

### JP Analyzer

```text
JP Analyzer
  .gitignore
  app/__init__.py
  app/analyzer/__init__.py
  app/analyzer/adapters/__init__.py
  app/analyzer/adapters/dictionary_adapter.py
  app/analyzer/adapters/kwja_adapter.py
  app/analyzer/compact_output.py
  app/analyzer/config.py
  app/analyzer/contracts.py
  app/analyzer/engine.py
  app/analyzer/ginza_runtime.py
  app/analyzer/health.py
  app/analyzer/kwja_runtime.py
  app/analyzer/layers/__init__.py
  app/analyzer/layers/candidates.py
  app/analyzer/layers/decision.py
  app/analyzer/layers/dictionary.py
  app/analyzer/layers/dictionary_api.py
  app/analyzer/layers/dictionary_evidence_api.py
  app/analyzer/layers/dictionary_store.py
  app/analyzer/layers/evidence_gate.py
  app/analyzer/layers/grammar.py
  app/analyzer/layers/invariants.py
  app/analyzer/layers/kwja.py
  app/analyzer/layers/morphology.py
  app/analyzer/layers/protected.py
  app/analyzer/layers/schema.py
  app/analyzer/layers/stabilization.py
  app/analyzer/layers/structure.py
  app/analyzer/pipeline.py
  app/analyzer/reader_candidate_dictionary.py
  app/analyzer/reader_candidate_evidence.py
  app/analyzer/reader_candidate_generation.py
  app/analyzer/reader_candidate_selection.py
  app/analyzer/reader_candidates.py
  app/analyzer/reader_corrections.py
  app/analyzer/reader_corrections_api.py
  app/analyzer/reader_projection.py
  app/analyzer/runtime.py
  app/analyzer/semantic_snapshot.py
  app/analyzer/service.py
  app/analyzer/services.py
  app/analyzer/source_contract.py
  app/analyzer/version.py
  CONSOLIDATED_ANALYZER.md
  direct_analyzer_timing.py
  docs/KWJA_SETUP_WINDOWS.md
  docs/PROJECT_SNAPSHOT_CURRENT.md
  docs/READER_PROJECTION_CONTRACT.md
  README.md
  requirements-frozen-py311.txt
  requirements-kwja-py311.txt
  requirements.txt
  run_snapshot_regression.py
  run_tests.ps1
  scripts/setup_kwja_windows.ps1
  tests/__init__.py
  tests/corpora/development/random_sentences.txt
  tests/corpora/parity/consolidation_fresh_unseen_200.txt
  tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json
  tests/corpora/README.md
  tests/fixtures/single_case_semantic_reference.json
  tests/test_correction_revision.py
  tests/test_decision.py
  tests/test_dictionary_adapter.py
  tests/test_dictionary_evidence.py
  tests/test_dictionary_path.py
  tests/test_engine_routing.py
  tests/test_evidence_routing.py
  tests/test_facade.py
  tests/test_health_contract.py
  tests/test_import_boundary.py
  tests/test_kwja_adapter.py
  tests/test_kwja_timeout.py
  tests/test_no_legacy_imports.py
  tests/test_reader_candidate_dictionary.py
  tests/test_reader_candidate_evidence.py
  tests/test_reader_candidate_generation.py
  tests/test_reader_candidate_safeguards.py
  tests/test_reader_candidate_selection.py
  tests/test_reader_correction_compact_output.py
  tests/test_reader_corrections_backend.py
  tests/test_reader_lookup_hypotheses.py
  tests/test_reader_numeric_terms.py
  tests/test_reader_projection_contract.py
  tests/test_runtime_contracts.py
  tests/test_runtime_reuse.py
  tests/test_semantic_snapshot.py
  tests/test_single_pass.py
```

#### JP Analyzer file purposes

- `.gitignore` — Project source or support file. SHA-256 `dd78ab120d88f316a8caf0a2b7a7d27eed5b727094eecbedc72da5f0d90ac47f`.
- `app/__init__.py` — Python source. SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `app/analyzer/__init__.py` — Python source. SHA-256 `e243154c70bfe143584d15bb1b35fee66c4103fbbc0df354d72729601ecc143b`.
- `app/analyzer/adapters/__init__.py` — Python source. SHA-256 `1fe610e339af091cbfa768e2ad541cd27256c4f310da0d6461a86c46ac9b6b69`.
- `app/analyzer/adapters/dictionary_adapter.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `b1ec237ba2308c8fa9bb55b176f90119bef72407740caf2944be68e0af38f5b7`.
- `app/analyzer/adapters/kwja_adapter.py` — KWJA runtime, evidence, or tests. SHA-256 `5ae0e0c2b8dc63eae642a8d05c6c964b3e4aa0d095f94bf827949c174bd67f73`.
- `app/analyzer/compact_output.py` — Python source. SHA-256 `c3c857da1afa7035edf6879606df25711c756ff82098ad328da301a58aa0608e`.
- `app/analyzer/config.py` — Python source. SHA-256 `0572e92dc2906ae581691eb1fdcca535b018ed4977d5fc40952bd19b5399b77a`.
- `app/analyzer/contracts.py` — Python source. SHA-256 `e42182bb18de775c9063fb1c2b3c9b00d86ba730748b5fd7ad78b8afc0234cf4`.
- `app/analyzer/engine.py` — Python source. SHA-256 `5272712888cc23118cc1d602c2d5863fb671a9574b1a5fdac62443ba02c549fc`.
- `app/analyzer/ginza_runtime.py` — Python source. SHA-256 `f0d5b6805e86d0b54c33b706a2f41c87c0078c6dd9102b8e13025cc6fd1dec59`.
- `app/analyzer/health.py` — Python source. SHA-256 `22acc926eade6b8f4810ef03fcbac7efaf718689852093824d85466b39a4532d`.
- `app/analyzer/kwja_runtime.py` — KWJA runtime, evidence, or tests. SHA-256 `0dc0f43310f3f535c5a51369dba7b929f6e2fec12774e84e1ee69120d2230a0e`.
- `app/analyzer/layers/__init__.py` — Python source. SHA-256 `bab045ddb0d59383153376d73259cd7fe2323db6bb373f637979cd03e73fab87`.
- `app/analyzer/layers/candidates.py` — Python source. SHA-256 `0593de79bc20537e2a0668e673b5429c116cbf9c7594e4119074287483ec363f`.
- `app/analyzer/layers/decision.py` — Python source. SHA-256 `2101e09eca13a5b3fa4bb8e614c82958c6e999898665ec962b1559271640a2c8`.
- `app/analyzer/layers/dictionary.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `91636e767134430cc58f6eef7c0bcc5771ca8884357ba636672f574488a92349`.
- `app/analyzer/layers/dictionary_api.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `a9946dea6c6a38d694abd6827a82dbee93defbd2ddbb74c27a1a790ded573eb5`.
- `app/analyzer/layers/dictionary_evidence_api.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `c6d4a8dfc34e6ff50987f9bcc011b5c4d656272ae3a779a60c8956d319432cb2`.
- `app/analyzer/layers/dictionary_store.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `17fe42a1b5329380a04a8d52fde8842f3adcec4e8b9bb2faa9797de60f66e4a7`.
- `app/analyzer/layers/evidence_gate.py` — Python source. SHA-256 `c341fcf2a30bcb7ac4105784a10be1c7549c94e69cc2c46e3033c1a1ea6ef85b`.
- `app/analyzer/layers/grammar.py` — Python source. SHA-256 `cac8c93043717fd27fac9a57064588acbc6a170c812d62f3af69564694867bdc`.
- `app/analyzer/layers/invariants.py` — Python source. SHA-256 `03f9d5482d133d5888b8df3304dfa8ced196516322511dc514735df160d3cac4`.
- `app/analyzer/layers/kwja.py` — KWJA runtime, evidence, or tests. SHA-256 `efe44b02d5598926c846dcf5b2d9f719cf2d10950913cda0fcaa918f57c04054`.
- `app/analyzer/layers/morphology.py` — Python source. SHA-256 `56b991e10c6bb3d1232911ed1acd56b4418920ff6397f6889ce0edd27584934c`.
- `app/analyzer/layers/protected.py` — Python source. SHA-256 `43d146fa3ff6773b5e661d34c918f979aeca4a8f821e4fe1cab932294e04acf6`.
- `app/analyzer/layers/schema.py` — Python source. SHA-256 `abdcc0d625f144940a43b5bf07f878fad4a909f01d953ae04dce2c3d880fa5d0`.
- `app/analyzer/layers/stabilization.py` — Python source. SHA-256 `2fb025b8b6680ac67e961605bf208f17fc3087672d6aaa047cfdfb198ad847d7`.
- `app/analyzer/layers/structure.py` — Python source. SHA-256 `86243871cfebff2f40f6e1b286d1348f2b544f41d727814570e72569c7b905ba`.
- `app/analyzer/pipeline.py` — Python source. SHA-256 `3ccf1bfb7b4112251ec3de50fe7fa89a3ffcff9e365758aed44594324dd31712`.
- `app/analyzer/reader_candidate_dictionary.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `d519c953d3d4a49701cd7fae49176bf813f81ef891d0c03428d7f912111cf7b0`.
- `app/analyzer/reader_candidate_evidence.py` — Reader contract, rendering, or UI. SHA-256 `44cd8a33c3cd50ceed01fe4dea6e31fe18dd7cfecdb80dea9a310684df43f958`.
- `app/analyzer/reader_candidate_generation.py` — Reader contract, rendering, or UI. SHA-256 `6630b45916b92ff67dcd8bf92d9bb2400740a261c1807565978a07dbca183482`.
- `app/analyzer/reader_candidate_selection.py` — Reader contract, rendering, or UI. SHA-256 `98483a0910552cf392bcf288104afdc957b909155fc2cf9b587f46007fb92158`.
- `app/analyzer/reader_candidates.py` — Reader contract, rendering, or UI. SHA-256 `7fe41090a7a20b2039347a8e78293a5c20b0659eee45cc98801f81c1c279b8c1`.
- `app/analyzer/reader_corrections.py` — Reader contract, rendering, or UI. SHA-256 `15fc3b76bba63c6af232b0bbb956aa3ee5703dcc4c312af5ddb6abc2dc50b406`.
- `app/analyzer/reader_corrections_api.py` — Reader contract, rendering, or UI. SHA-256 `035395754bd62e79e3ecddb8a1c1018a479e9441399483b83764e52f635b3383`.
- `app/analyzer/reader_projection.py` — Reader contract, rendering, or UI. SHA-256 `89983e8a64df9e10599036e05178ab3652798766cbaef0b7ff7dbbeaf2a663ba`.
- `app/analyzer/runtime.py` — Python source. SHA-256 `3244da7fb42e4b421f759d2d273ebc3c9aa35d7e1ba264bd6478416e45217f12`.
- `app/analyzer/semantic_snapshot.py` — Python source. SHA-256 `c805d66ee21816a1e84beb220bef86b28960e89c2af3a8eeef5fa78fc55a8028`.
- `app/analyzer/service.py` — Python source. SHA-256 `163f92a16fca98727046da6f843ad81552c1339bf524bfa6273dd120fa12cb4a`.
- `app/analyzer/services.py` — Python source. SHA-256 `85ef48e63be3f8747820e04978e83dd124685d1540aa80b353df185f3b0e40a7`.
- `app/analyzer/source_contract.py` — Python source. SHA-256 `aaa8493a6adb2d8d9dc5eff7ef6f0e941b0c96d73e59a73684f2b7feddd6eeb1`.
- `app/analyzer/version.py` — Python source. SHA-256 `2ace8b20208561b754ad9b242a47c76a8108428e7da9f626ccd2dce8ee95f445`.
- `CONSOLIDATED_ANALYZER.md` — Documentation. SHA-256 `2e5122570b09ed1bac9744d9237aa981b18e2b70af77381cf6253a6eef092312`.
- `direct_analyzer_timing.py` — Python source. SHA-256 `149fcb9290d5175cbd4c76ac4468caf1bca4ebd705557e0a80f7eae9965aa75c`.
- `docs/KWJA_SETUP_WINDOWS.md` — KWJA runtime, evidence, or tests. SHA-256 `4f1afa87db391b26bd6f5e88ba8a0a834421889831fcfdb40bcbd8bf93c1cac9`.
- `docs/PROJECT_SNAPSHOT_CURRENT.md` — Documentation. SHA-256 `5d26af018006aed383c32dec3d7ed10c4a4479f5db9280d3a719a6d004bc2ffd`.
- `docs/READER_PROJECTION_CONTRACT.md` — Reader contract, rendering, or UI. SHA-256 `558629abe4f478c7725a53a29bbe09482c93e1ef58d9054bf8ed48352835cfb6`.
- `README.md` — Documentation. SHA-256 `fcf72fa570947e45689bb873f1733dc591cfee7e5d8b65d4f57465dc1d5b2d4b`.
- `requirements-frozen-py311.txt` — Python dependency configuration. SHA-256 `a7e463ebdcf1c92c108db2c013ee0c9beda3aeae92d0bf6c80c0b1311b2bbbb1`.
- `requirements-kwja-py311.txt` — Python dependency configuration. SHA-256 `bb2685f638dc7d1b4d108c2dfdbafef186bd15482a9a9349b319b3f3e60462c6`.
- `requirements.txt` — Python dependency configuration. SHA-256 `504419d8379e69ad3e687bcfd288eb964771836c83415fed2faf359708426722`.
- `run_snapshot_regression.py` — Python source. SHA-256 `34c6b5b98f982a8b6f8702d0a3b7b33f1bf64292f035057eb36d0ba4cda78e53`.
- `run_tests.ps1` — Project source or support file. SHA-256 `4e56bcad3c84d3c11db1fbe9fd04c2f48824fdc3282c671eb0ce688c263fa2a6`.
- `scripts/setup_kwja_windows.ps1` — KWJA runtime, evidence, or tests. SHA-256 `d88cc37b3440bf30c333a15b4658bd48647d52d722d0c0a8a921989ab812140e`.
- `tests/__init__.py` — Automated test or fixture. SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `tests/corpora/development/random_sentences.txt` — Automated test or fixture. SHA-256 `b074dc201ea445bd8d0f349c15bbe87af303281ffea814571bb1774d9b6ed3ca`.
- `tests/corpora/parity/consolidation_fresh_unseen_200.txt` — Automated test or fixture. SHA-256 `5fec594ffe3b3c3159e53db965d959054af54bdfdcef91ec1145845772ac6955`.
- `tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json` — Automated test or fixture. SHA-256 `55816540e341f62a17205e1800a6fde67984d02303dbce44790f3c63be058e7d`.
- `tests/corpora/README.md` — Automated test or fixture. SHA-256 `ce8c59c1fcd3b417d65106adc1d3ceb35cad827ca594d39ba5492e675af635f6`.
- `tests/fixtures/single_case_semantic_reference.json` — Automated test or fixture. SHA-256 `574121c0b509db1fcd5a8306af51689b4d415f7a0af89f605a346c4524eb5d0d`.
- `tests/test_correction_revision.py` — Teaching correction workflow. SHA-256 `9ded1b0095391a49a5d5737d198e6680789d992ef8cea2122e3eda19a8ca241d`.
- `tests/test_decision.py` — Automated test or fixture. SHA-256 `96c88170c0390d2bd006c47a50b8d3b2e18c5857f3d76df421404167e54e781d`.
- `tests/test_dictionary_adapter.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `ad3f15c285dd0c3a185a623a03ffbf5e003326114f1e5cd63b7a0ba76db5d867`.
- `tests/test_dictionary_evidence.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `82c8a811096d4ebb08c9f85ef411a80d254d963037999d584ffa05261e0ce141`.
- `tests/test_dictionary_path.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `c01ce0a324df703fcfc9d831e54e9763fd040cfc01a0a7b9908fb1bfe74890ec`.
- `tests/test_engine_routing.py` — Automated test or fixture. SHA-256 `46d8a3ba0856e1930d69e9e77a37532df7336dfc1cd701b9aba3bfa230a1d49b`.
- `tests/test_evidence_routing.py` — Automated test or fixture. SHA-256 `c3c60f8d2f5e6ad85cc0812e70ffcfcfccc57cfb474eba7817f5f26992fb2c93`.
- `tests/test_facade.py` — Automated test or fixture. SHA-256 `67e0e55c67cd09b2a6c2b56f02b4b0f8ad5060bc7561fa6bf25d9530a8b72e46`.
- `tests/test_health_contract.py` — Automated test or fixture. SHA-256 `4a0e13bd70ff165abd1a1b81bfe74bca51af6eab9379720e9154d5023e7bfec9`.
- `tests/test_import_boundary.py` — Automated test or fixture. SHA-256 `ad5693a212a9a78c18b79958686459bee1c3edcd6ea6141f533d994827e62082`.
- `tests/test_kwja_adapter.py` — KWJA runtime, evidence, or tests. SHA-256 `e34c28992d459e0822498215f72b93fdb11697fb58efe61106cd32dac7eedd70`.
- `tests/test_kwja_timeout.py` — KWJA runtime, evidence, or tests. SHA-256 `27aa587eb617d79d91197042d42e61bbee8d66b4c1d66275d70df6bc1b1d59d1`.
- `tests/test_no_legacy_imports.py` — Automated test or fixture. SHA-256 `1e62f41e2a4cbdbb3d6d9aaf622f7b3fd433b73a997aeb3c9556210adeafd58d`.
- `tests/test_reader_candidate_dictionary.py` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `b4a11d9454e5d7816ae634637aed8ed9d4bf1eb627dce5a3347d2b4e96a6cb46`.
- `tests/test_reader_candidate_evidence.py` — Reader contract, rendering, or UI. SHA-256 `a306e0c75892a500de0f608481a65092f19e05744a56bc5b6a25de4f7a75c271`.
- `tests/test_reader_candidate_generation.py` — Reader contract, rendering, or UI. SHA-256 `704cff08ec89b8701beeea9e81f7690a2f80d127c044db50265f556ceffa26d9`.
- `tests/test_reader_candidate_safeguards.py` — Reader contract, rendering, or UI. SHA-256 `e225623c8a99082e2325f8a2ded199ddb49206a087dd14fe9f82913f805ee866`.
- `tests/test_reader_candidate_selection.py` — Reader contract, rendering, or UI. SHA-256 `06e2ec5c9ec30e936cc03c25e4e6307074c8fec0529c4e1cb21574030a3c5edd`.
- `tests/test_reader_correction_compact_output.py` — Reader contract, rendering, or UI. SHA-256 `a8146448ec96515f4dd7c8a568eed663524e5407755e71ec9b377ea6f2409b32`.
- `tests/test_reader_corrections_backend.py` — Reader contract, rendering, or UI. SHA-256 `686814e765c41cde1a54908fd380cfdce77f2f80ce393a551f57ce9f34b539f1`.
- `tests/test_reader_lookup_hypotheses.py` — Reader contract, rendering, or UI. SHA-256 `21421bc2497fe1b77d9f0757925eda8bf7c258e9a0ed78280c6b62144915ad68`.
- `tests/test_reader_numeric_terms.py` — Reader contract, rendering, or UI. SHA-256 `ef905e2733a2f55f2b84428ffa9d0dc20e33c478257fecd4237ca56c0f8e6dcd`.
- `tests/test_reader_projection_contract.py` — Reader contract, rendering, or UI. SHA-256 `fff5baa30b9f05d074c1387346972b2b71125745be8f92b65aae51d3dbe58d23`.
- `tests/test_runtime_contracts.py` — Automated test or fixture. SHA-256 `6c1b501f0385e95b1b7e241f5c10641bb1572fa93ee120cd910db2a375c6cdab`.
- `tests/test_runtime_reuse.py` — Automated test or fixture. SHA-256 `90ae6a8ee49d3218a9d085c1a673294a4ce4125df41554d97fd6114ae99d3e0a`.
- `tests/test_semantic_snapshot.py` — Automated test or fixture. SHA-256 `eaf526c3c3998edf88128f048801230de844fbcf6f3a16fac5382a07da95d2f7`.
- `tests/test_single_pass.py` — Automated test or fixture. SHA-256 `535c46e5dd5a03b3ae6e04b3610259bbe68761fe7f9ef20c77ad1607ecd32a7f`.

### Novel Audio Miner

```text
Novel Audio Miner
  .gitattributes
  .gitignore
  docs/ANALYZER_INTEGRATION_CONTRACT.md
  FINAL_STABLE_STATUS.md
  index.html
  LOCAL_DATA_MANIFEST.example.json
  package-lock.json
  package.json
  PROJECT_STRUCTURE.md
  public/dict/user_dictionary_seed.json
  README.md
  RELEASE_CHECKLIST.md
  scripts/test-analyzer-cache.mjs
  scripts/test-analyzer-learning-activation.mjs
  scripts/test-analyzer-learning-model.mjs
  scripts/test-analyzer-metadata-lease.mjs
  scripts/test-analyzer-mining-selection.mjs
  scripts/test-analyzer-presentation.mjs
  scripts/test-analyzer-reader-spans.mjs
  scripts/test-analyzer-selection-ownership.mjs
  scripts/test-color-sources.mjs
  scripts/test-debug-report-v2.mjs
  scripts/test-scene-prefetch.mjs
  scripts/test-tokenizer-retirement.mjs
  src/App.jsx
  src/components/FileLoader.jsx
  src/components/Phase8DictionarySyncPanel.jsx
  src/components/Reader.jsx
  src/lib/analyzerCacheIdentity.js
  src/lib/analyzerLearningModel.js
  src/lib/analyzerMetadataLease.js
  src/lib/analyzerMiningSelection.js
  src/lib/analyzerPresentationPolicy.js
  src/lib/analyzerReaderSpanAdapter.js
  src/lib/ankiConnect.js
  src/lib/colorSource.js
  src/lib/debugReportV2.js
  src/lib/dictionaryDetection.js
  src/lib/dictionaryLookup.js
  src/lib/dictionaryStorage.js
  src/lib/dictionaryValidationBridge.js
  src/lib/enrichService.js
  src/lib/epubParser.js
  src/lib/frequencyMap.js
  src/lib/japaneseSentenceSplitter.js
  src/lib/jpAnalyzerClient.js
  src/lib/phase8DictionarySync.js
  src/lib/scenePrefetch.js
  src/lib/storage.js
  src/lib/useJpAnalyzerShadow.js
  src/lib/wordCache.js
  src/main.jsx
  src/styles.css
  STABILIZATION.md
  vite.config.js
  WORD_MODEL_POLICY.md
```

#### Novel Audio Miner file purposes

- `.gitattributes` — Project source or support file. SHA-256 `39c7511572246661bf73790ae3658d61e73e77623a5e08cd463ad402e466b0f8`.
- `.gitignore` — Project source or support file. SHA-256 `2523690971b97378a0438892b75233178330006644d668bf4e272de8386c79e3`.
- `docs/ANALYZER_INTEGRATION_CONTRACT.md` — Documentation. SHA-256 `31ea9b689bb25a99b47e209fda178f5d5afd521ac068a68a29843a65894bbdbc`.
- `FINAL_STABLE_STATUS.md` — Documentation. SHA-256 `1ac1fbfb34f027183dc60c67dad212f3957b5d0dd2c9ed855785838a5a4b4edc`.
- `index.html` — Project source or support file. SHA-256 `755b0049db5826b6b77e22bcf3c129f5ffe1ab0c2a55ff8411d99999d18bdabd`.
- `LOCAL_DATA_MANIFEST.example.json` — Project source or support file. SHA-256 `6857a0d0f03ddb6470cbf91ec80b422afab795503c6579585ffde310745b8e6c`.
- `package-lock.json` — Node dependency and script configuration. SHA-256 `a08886d11b538d77d6e14a16e230a90bea29e70ebfe4257d8830fb12e0313915`.
- `package.json` — Node dependency and script configuration. SHA-256 `02fc98336ec170b23937ff560dff7e26748fa031cb641d74be7c03d56307b8bb`.
- `PROJECT_STRUCTURE.md` — Documentation. SHA-256 `f329ab81ce6a78991cf0654082d7fb55f63a4a853cc6e9da0f35b1f15b676768`.
- `public/dict/user_dictionary_seed.json` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `e8c3fff4439b237ce64a83f777f609cc29a917fcfd286b1eca09696f7fb93d25`.
- `README.md` — Documentation. SHA-256 `a416acdfb86857e68bd7ac8967a61a079376dc107b111c8c3a596710e233de47`.
- `RELEASE_CHECKLIST.md` — Documentation. SHA-256 `ce9264ede71ba2bb6b958b17ab0f4b20d732b57b400a45af1d57e79be8b3007f`.
- `scripts/test-analyzer-cache.mjs` — Automated test or fixture. SHA-256 `6303f3706222905b74d7053873f54e3ca3257a05b0ab0e73b37cd7e6fa916fe1`.
- `scripts/test-analyzer-learning-activation.mjs` — Automated test or fixture. SHA-256 `eb67aa3c05e3194e79431101c3780534eb36247d26f32cd31ac94f98750b269a`.
- `scripts/test-analyzer-learning-model.mjs` — Automated test or fixture. SHA-256 `f661aa1f08a1208ba49cbda0381ab3ef87ba0ed03d7ea75c423f622bf2bde850`.
- `scripts/test-analyzer-metadata-lease.mjs` — Automated test or fixture. SHA-256 `acf2b1710aa409fae1e6e7492a8291f384cd0596790d9c4f6b12342a118e8897`.
- `scripts/test-analyzer-mining-selection.mjs` — Automated test or fixture. SHA-256 `8ddb97c473af861c104bb182b4a3339e452c8df06660c481089c80ea3fdaccef`.
- `scripts/test-analyzer-presentation.mjs` — Automated test or fixture. SHA-256 `1f1e2d884d3b4b923b14a3d64335f385912263c7bbe76cd9cce28db09e3c5ab3`.
- `scripts/test-analyzer-reader-spans.mjs` — Reader contract, rendering, or UI. SHA-256 `0dbd4de79ae6ca903ec67a8125933953033876205a732b47c5ff36a29fa947b4`.
- `scripts/test-analyzer-selection-ownership.mjs` — Automated test or fixture. SHA-256 `00987e4b6044d66e7208b5745f30102cfa05ed02b5f7a83bd1883545aa26ab65`.
- `scripts/test-color-sources.mjs` — Automated test or fixture. SHA-256 `e069018b53661672b54ae1ca5a53c71b30282af4ab84fd0f3253ad0be3e800a6`.
- `scripts/test-debug-report-v2.mjs` — Automated test or fixture. SHA-256 `7882df3c8b01510e809ae3aa8c27d0cdedde9add48f64b33587f126df60b03b1`.
- `scripts/test-scene-prefetch.mjs` — Automated test or fixture. SHA-256 `d513454fefd883860526bc6d8807f057b913d1e8a32b7b3b280b442b2f075399`.
- `scripts/test-tokenizer-retirement.mjs` — Automated test or fixture. SHA-256 `a90b59f6407324f7060bb7ba3bc9bc0a4d0bbaca628f0c6dc388db5906265528`.
- `src/App.jsx` — JavaScript/React source. SHA-256 `a1eead4a27bcbfb2026b94ad64e96ea661f628fb42bd8d3e41e5cdd38140e9b1`.
- `src/components/FileLoader.jsx` — JavaScript/React source. SHA-256 `d04564c7aa49684a1ae63566a5f87cccd43c8aa9a6c057ad774957cfc069237c`.
- `src/components/Phase8DictionarySyncPanel.jsx` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `9e047339d1bff0b5cd30cbf8d0226a4e7d0e3e497663b67dd10ccd3e194384b7`.
- `src/components/Reader.jsx` — Reader contract, rendering, or UI. SHA-256 `01dee1b69d454fe7df9a5bbb61c7f52295ef5f67738cf33006943befd8174cee`.
- `src/lib/analyzerCacheIdentity.js` — JavaScript/React source. SHA-256 `b68c876cc2160d45cf3d3bb873f042dda4d98506996dc026472915034370c5dc`.
- `src/lib/analyzerLearningModel.js` — JavaScript/React source. SHA-256 `324bf646b36f9c4c46fe680f6411b64dd9aaf99e9e4eaa388a1fc7888ad0c25e`.
- `src/lib/analyzerMetadataLease.js` — JavaScript/React source. SHA-256 `a95d758702a22cc7ea9cca9585eb355044b9f8b1c84d1a261c0020f9c2ebbd8c`.
- `src/lib/analyzerMiningSelection.js` — JavaScript/React source. SHA-256 `216a9ddcd722163ec091a74a0f0a64ca7bc894143839fdfb010f805d8523aba7`.
- `src/lib/analyzerPresentationPolicy.js` — JavaScript/React source. SHA-256 `beb654d4a6cd8552c2e7be25225a69dd13a713a7531c9b3fb796084537182a2c`.
- `src/lib/analyzerReaderSpanAdapter.js` — Reader contract, rendering, or UI. SHA-256 `5d3903b2306d88474973a5e59b7394afe6932846978952d4379e4ab8d7a0d6cb`.
- `src/lib/ankiConnect.js` — Anki integration. SHA-256 `a32bb91991fa25724ff32c541a4e76233224eded2744e63af41a5ef9edc5a1c0`.
- `src/lib/colorSource.js` — JavaScript/React source. SHA-256 `539b933deb2418ad079fbd44f38f36caae2d2059e1ee149631d7bd66510b1066`.
- `src/lib/debugReportV2.js` — JavaScript/React source. SHA-256 `c337caac8823febe71ded5822013f37738d20ccd3cc57888688d3be261edc949`.
- `src/lib/dictionaryDetection.js` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `25ff52f8388c33bf475af42463bf68f40486d6f76bba5a23fa6c40feb725d603`.
- `src/lib/dictionaryLookup.js` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `83a45364c35e0e388c98b95b8809d396facb01a0829ba64c813c4f3f741a1159`.
- `src/lib/dictionaryStorage.js` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `32ed043b365e7ce6c68f813863c0521903105d1ff9fff9c5e1a16e04d5686c94`.
- `src/lib/dictionaryValidationBridge.js` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `c85bb539b3b39fb9314be3c3693f235c914f561f92ce642bb4ff78d2913902ac`.
- `src/lib/enrichService.js` — JavaScript/React source. SHA-256 `534da9370a40fad6a0f11ac68ab97dabdefc753e00de3da5a44b6070c68477f1`.
- `src/lib/epubParser.js` — EPUB parsing or diagnostics. SHA-256 `2016a1b37f63015ebab4f944b97d56b10ff17af38d2603ab5b856a2a850839ad`.
- `src/lib/frequencyMap.js` — JavaScript/React source. SHA-256 `87b5cb0bd60d33399901fe2f87a2d88ac86bae90e9dc293aa7e0059b9b720b9b`.
- `src/lib/japaneseSentenceSplitter.js` — JavaScript/React source. SHA-256 `b080d45b6dbe17a4077fbd1e07d5c9b3c0522fefc2ab296055e37c93557d3e0e`.
- `src/lib/jpAnalyzerClient.js` — JavaScript/React source. SHA-256 `57ba68a64303333ec908334b239ef9d7113be4dfb0fa9c1c6c253e8d32ee5e75`.
- `src/lib/phase8DictionarySync.js` — Dictionary storage, sync, lookup, evidence, or UI. SHA-256 `361fffb3677c99801dd21ce554e67a111d8cee5fc3b2c76bd5ea049d4c09cc48`.
- `src/lib/scenePrefetch.js` — JavaScript/React source. SHA-256 `fed68e1677d41eb82d731f3e35cbb7f5ad0da125e610cd09715d2f84231b68de`.
- `src/lib/storage.js` — JavaScript/React source. SHA-256 `9d37c2cb67b10b366493c51ff7605aa34cc6030df1afce986e7a5ce9caa2ed43`.
- `src/lib/useJpAnalyzerShadow.js` — JavaScript/React source. SHA-256 `dda710873a39f1bc93137c3e129954bab6f1ba6d299825ef52b57213b1f3fe83`.
- `src/lib/wordCache.js` — JavaScript/React source. SHA-256 `9736d0cf5b2bdc96c5066037430246e49c4cbbdaddf7b797d4f3db2a4ec14236`.
- `src/main.jsx` — JavaScript/React source. SHA-256 `e0184dd19789caef1e69388a6ae7ca5a2b92d4178f387a23605087edbe0bfa7f`.
- `src/styles.css` — Project source or support file. SHA-256 `90f88426d3495668945e0d68ba41e276c3b65ecdc83ed50dd12fd3d034b5489b`.
- `STABILIZATION.md` — Documentation. SHA-256 `ef777bad9beecff78e8c47c4533c2eb77e655834a88609415996988b15297ef7`.
- `vite.config.js` — JavaScript/React source. SHA-256 `b5e57218b58ac8d806da358443a5abfc5618444a59a3fcac593427fcb9024354`.
- `WORD_MODEL_POLICY.md` — Documentation. SHA-256 `52994df2185c936160789643f0887cbad5fc19e03e86c330872e81aa4a80bec5`.

### Runtime/local data files (contents excluded)

- **jpAnalyzer:** `D:\Mining\JP analyzer\app\data\phase8_analysis_lexicon.sqlite3` — 49,152 bytes; SHA-256 `7b453dbdd160387102b09dda5af944cbdc0c667fa848664f8b489bf7cba60cf3`.
- **jpAnalyzer:** `D:\Mining\JP analyzer\data\phase8_analysis_lexicon.sqlite3` — 1,815,511,040 bytes; SHA-256 `2c0b9bc2dfc1c3b2bb8d0fd35cf7d519997ea9a4ad72fc6b75f3308400f81e12`.
- **jpAnalyzer:** `D:\Mining\JP analyzer\data\reader_corrections.sqlite3` — 16,384 bytes; SHA-256 `ee1782e1132f953a52611c1d2aa070e338522bf10fdc4459489e07dbada99e89`.

## 4. Complete File Contents

The following blocks contain the complete text content of every captured relevant file in both current working trees. Binary/generated/runtime data remains excluded by design. The embedded content is the source of truth corresponding to the Git states stated at the top of this snapshot.

### Repository A — JP Analyzer

### `JP analyzer/.gitignore`

- Purpose: Project source or support file.
- Size: 2707 bytes
- SHA-256: `dd78ab120d88f316a8caf0a2b7a7d27eed5b727094eecbedc72da5f0d90ac47f`

````text
# Local Python environments
.venv/
.venv*/
venv/
env/

# Python-generated data
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Analyzer runtime databases
data/
*.sqlite
*.sqlite3
*.sqlite3-*
*.db
*.db-*

# Generated analysis results
phase8_*.json
phase8_*.jsonl
phase9_*.json
phase9_*.jsonl
work_pc_*.json

# Generated reports
*_result.json
*_results.json
*_results.jsonl
*_summary.json
*_review_report.txt
*_changed_sentences.json
*_flagged_sentences.json
*_changed_and_flagged.json
*_alignment_failures.json
*_readonly_regressions.json

# Frozen benchmark outputs remain local
frozen_phase9_alpha22/benchmark_200/

# Temporary inventories and source bundles
*_inventory.txt
*_current_source.txt
*_source_bundle.txt
*_debug.json
staged_files_check.txt

# Backups and temporary files
*.bak
*.backup
*.tmp
*.temp

# Cleanup and one-time migration scripts
cleanup_*.ps1
restore_*.ps1
delete_*.ps1
apply_*.py
patch_*.py

# Archives and quarantine
_archive*/
_backup*/
_cleanup*/
*.zip
*.7z
*.rar

# Editor and OS files
.vscode/
.idea/
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/

# Local unseen-novel evaluation corpus and outputs
all_sentences_original.txt
unseen_sample_indices.txt
unseen_sample_manifest.json
unseen_novel_sentences.txt
unseen_novel_sentences_hash.json
phase9_alpha22_unseen_*

# Local unseen-corpus preparation utility
create_unseen_corpus.py

# Phase 10 local parity outputs
phase10_parity_*.json
phase10_*_check.json
apply_phase10_1_facade.py

# Local Phase 10 source-review bundles
phase10_2_current_source.txt

# Phase 10.2 local infrastructure artifacts
apply_phase10_2_infrastructure.py
phase10_2_current_source.txt
phase10_semantic_snapshots.json
phase10_reference_*.json
phase10_snapshot_*.json
*.phase10.1.bak

# Local Phase 10.3 source review bundle
phase10_3_current_source.txt

# Local Phase 10.3 source review bundle
phase10_3_current_source.txt

# Phase 10.3 local artifacts
apply_phase10_3_routing.py
phase10_3_current_source.txt
phase10_3_api_check.json
*.phase10.2.bak

# Machine-specific runtime configuration
configure_local_runtime.ps1

# Local Phase 10.4 source review bundle
phase10_4_current_source.txt
.kwja-venv/
consolidation_*_reference*.json
consolidation_*_actual*.json
consolidation_*_report*.json
fresh_unseen_*.json
post_cleanup_*.json

# Local analyzer regression outputs
post_cleanup_*.json
consolidation_*_reference*.json
consolidation_*_actual*.json
consolidation_*_report*.json
fresh_unseen_*.json
s*.knp
s*_actual.json
*_raw.knp
streamlined_*.json
data/reader_corrections.sqlite3*
````

### `JP analyzer/app/__init__.py`

- Purpose: Python source.
- Size: 0 bytes
- SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

````python

````

### `JP analyzer/app/analyzer/__init__.py`

- Purpose: Python source.
- Size: 805 bytes
- SHA-256: `e243154c70bfe143584d15bb1b35fee66c4103fbbc0df354d72729601ecc143b`

````python
from .adapters import DictionaryAdapter, KwjaAdapter
from .config import AnalyzerConfig
from .contracts import AnalyzeOptions, linguistic_projection
from .engine import AnalyzerEngine
from .health import health_report
from .pipeline import analyze, analyze_full
from .runtime import AnalyzerRuntime, get_runtime
from .semantic_snapshot import semantic_snapshot, snapshot_digest
from .version import ANALYZER_VERSION, SCHEMA_VERSION

__all__ = [
    "ANALYZER_VERSION",
    "SCHEMA_VERSION",
    "AnalyzerConfig",
    "DictionaryAdapter",
    "KwjaAdapter",
    "AnalyzeOptions",
    "AnalyzerEngine",
    "AnalyzerRuntime",
    "get_runtime",
    "health_report",
    "linguistic_projection",
    "analyze",
    "analyze_full",
    "semantic_snapshot",
    "snapshot_digest",
]
````

### `JP analyzer/app/analyzer/adapters/__init__.py`

- Purpose: Python source.
- Size: 140 bytes
- SHA-256: `1fe610e339af091cbfa768e2ad541cd27256c4f310da0d6461a86c46ac9b6b69`

````python
from .dictionary_adapter import DictionaryAdapter
from .kwja_adapter import KwjaAdapter

__all__ = ["DictionaryAdapter", "KwjaAdapter"]
````

### `JP analyzer/app/analyzer/adapters/dictionary_adapter.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 748 bytes
- SHA-256: `b1ec237ba2308c8fa9bb55b176f90119bef72407740caf2944be68e0af38f5b7`

````python
from __future__ import annotations
from typing import Any
from ..layers.dictionary import evaluate_analysis_candidates, evaluate_candidate
from ..layers.dictionary_store import DB_PATH, status

class DictionaryAdapter:
    """Stable dictionary evidence adapter; a miss never rejects a candidate."""
    def status(self) -> dict[str, Any]:
        result = dict(status())
        result["database"] = str(DB_PATH)
        return result
    def evaluate_analysis(self, analysis: dict[str, Any]) -> dict[str, Any]:
        return evaluate_analysis_candidates(analysis)
    def evaluate_candidate(self, candidate: dict[str, Any], parser_pos: str | None = None) -> dict[str, Any]:
        return evaluate_candidate(candidate, parser_pos)
````

### `JP analyzer/app/analyzer/adapters/kwja_adapter.py`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 898 bytes
- SHA-256: `5ae0e0c2b8dc63eae642a8d05c6c964b3e4aa0d095f94bf827949c174bd67f73`

````python
from __future__ import annotations

from typing import Any

from ..config import AnalyzerConfig
from ..kwja_runtime import analyze_kwja, kwja_status, resolve_kwja_executable


class KwjaAdapter:
    """Stable adapter preserving the validated Phase 9 KWJA evidence schema."""

    def __init__(self, config: AnalyzerConfig | None = None):
        self.config = config or AnalyzerConfig.from_environment()

    def status(self) -> dict[str, Any]:
        return kwja_status(self.config)

    def analyze(
        self,
        text: str,
        *,
        raw_knp: str | None = None,
        executable: str | None = None,
    ) -> dict[str, Any]:
        selected = executable
        if raw_knp is None and selected is None:
            selected = str(resolve_kwja_executable(config=self.config))
        return analyze_kwja(text, raw_knp=raw_knp, executable=selected)
````

### `JP analyzer/app/analyzer/compact_output.py`

- Purpose: Python source.
- Size: 3416 bytes
- SHA-256: `c3c857da1afa7035edf6879606df25711c756ff82098ad328da301a58aa0608e`

````python
from __future__ import annotations

from typing import Any

from .reader_projection import (
    READER_SPAN_SCHEMA_VERSION,
    project_reader_spans,
)
from .version import SCHEMA_VERSION
from .reader_candidates import READER_CANDIDATE_SCHEMA_VERSION, project_reader_candidates
from .reader_candidate_selection import select_reader_output
from .reader_corrections import apply_active_corrections, correction_revision


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
    evaluated_reader_candidates = project_reader_candidates(result)
    reader_spans, reader_candidates, reader_selection = select_reader_output(
        result, evaluated_reader_candidates
    )
    reader_spans, applied_corrections = apply_active_corrections(
        result.get("text", ""), reader_spans
    )
    reader_selection = dict(reader_selection)
    reader_selection["appliedCorrections"] = applied_corrections
    reader_selection["appliedCorrectionCount"] = len(applied_corrections)
    diagnostics = result.get("diagnostics_alpha2") or []
    metadata = result.get("kwja_metadata_alpha1") or {}
    change = result.get("alpha2_change_summary") or {}
    text = result.get("text", "")

    return {
        "schemaVersion": SCHEMA_VERSION,
        "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
        "readerCandidateSchemaVersion": READER_CANDIDATE_SCHEMA_VERSION,
        "analyzerVersion": analyzer_version,
        "correctionRevision": correction_revision(),
        "engineVersion": result.get("version"),
        "text": text,
        "resolvedSpans": resolved,
        "readerSpans": reader_spans,
        "readerCandidates": reader_candidates,
        "readerSelection": reader_selection,
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
````

### `JP analyzer/app/analyzer/config.py`

- Purpose: Python source.
- Size: 694 bytes
- SHA-256: `0572e92dc2906ae581691eb1fdcca535b018ed4977d5fc40952bd19b5399b77a`

````python
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AnalyzerConfig:
    ginza_models: tuple[str, ...] = ("ja_ginza_electra", "ja_ginza")
    ginza_split_mode: str = "A"
    kwja_executable: Path | None = None
    dictionary_database: Path = Path(__file__).resolve().parents[2] / "data" / "phase8_analysis_lexicon.sqlite3"

    @classmethod
    def from_environment(cls):
        value = os.getenv("KWJA_EXE")
        return cls(kwja_executable=Path(value) if value else None)

    def kwja_available(self) -> bool:
        return bool(self.kwja_executable and self.kwja_executable.is_file())
````

### `JP analyzer/app/analyzer/contracts.py`

- Purpose: Python source.
- Size: 808 bytes
- SHA-256: `e42182bb18de775c9063fb1c2b3c9b00d86ba730748b5fd7ad78b8afc0234cf4`

````python
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
````

### `JP analyzer/app/analyzer/engine.py`

- Purpose: Python source.
- Size: 2876 bytes
- SHA-256: `5272712888cc23118cc1d602c2d5863fb671a9574b1a5fdac62443ba02c549fc`

````python
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
````

### `JP analyzer/app/analyzer/ginza_runtime.py`

- Purpose: Python source.
- Size: 1013 bytes
- SHA-256: `f0d5b6805e86d0b54c33b706a2f41c87c0078c6dd9102b8e13025cc6fd1dec59`

````python
from __future__ import annotations
from threading import RLock
import spacy
from .config import AnalyzerConfig

_lock = RLock()
_nlp = None
_model_name = None

def get_ginza(config: AnalyzerConfig | None = None):
    global _nlp, _model_name
    cfg = config or AnalyzerConfig.from_environment()
    with _lock:
        if _nlp is not None:
            return _nlp
        errors = []
        options = {"components": {"compound_splitter": {"split_mode": cfg.ginza_split_mode}}}
        for name in cfg.ginza_models:
            try:
                _nlp = spacy.load(name, config=options)
                _model_name = name
                return _nlp
            except Exception as exc:
                errors.append(f"{name}: {exc}")
        raise RuntimeError("GiNZA load failed: " + " | ".join(errors))

def ginza_model_name():
    return _model_name

def reset_ginza_for_tests():
    global _nlp, _model_name
    with _lock:
        _nlp = None
        _model_name = None
````

### `JP analyzer/app/analyzer/health.py`

- Purpose: Python source.
- Size: 901 bytes
- SHA-256: `22acc926eade6b8f4810ef03fcbac7efaf718689852093824d85466b39a4532d`

````python
from __future__ import annotations

from .runtime import AnalyzerRuntime, get_runtime
from .version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION, SCHEMA_VERSION
from .reader_projection import READER_SPAN_SCHEMA_VERSION
from .reader_corrections import correction_revision


def health_report(runtime: AnalyzerRuntime | None = None) -> dict:
    active = runtime or get_runtime()
    status = active.status()
    return {
        "status": "ok",
        "version": ANALYZER_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "readerSpanSchemaVersion": READER_SPAN_SCHEMA_VERSION,
        "correctionRevision": correction_revision(),
        "engineVersion": ENGINE_CONTRACT_VERSION,
        "mode": "production-consolidation-stable-evidence-routing",
        "ginzaModel": status.ginza_model,
        "kwja": status.kwja,
        "dictionary": status.dictionary,
    }
````

### `JP analyzer/app/analyzer/kwja_runtime.py`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 1035 bytes
- SHA-256: `0dc0f43310f3f535c5a51369dba7b929f6e2fec12774e84e1ee69120d2230a0e`

````python
from __future__ import annotations
from pathlib import Path
from .layers.kwja import analyze_kwja_alpha1
from .config import AnalyzerConfig

def resolve_kwja_executable(executable=None, config=None) -> Path:
    cfg = config or AnalyzerConfig.from_environment()
    path = Path(executable) if executable else cfg.kwja_executable
    if path is None:
        raise RuntimeError("Set KWJA_EXE to the isolated KWJA executable path.")
    if not path.is_file():
        raise FileNotFoundError(f"KWJA executable not found: {path}")
    return path

def kwja_status(config=None):
    cfg = config or AnalyzerConfig.from_environment()
    path = cfg.kwja_executable
    return {"available": bool(path and path.is_file()), "executable": str(path) if path else None, "modelSize": "base"}

def analyze_kwja(text, *, raw_knp=None, executable=None):
    path = None if raw_knp is not None else resolve_kwja_executable(executable)
    return analyze_kwja_alpha1(text, raw_knp=raw_knp, executable=str(path) if path else None)
````

### `JP analyzer/app/analyzer/layers/__init__.py`

- Purpose: Python source.
- Size: 173 bytes
- SHA-256: `bab045ddb0d59383153376d73259cd7fe2323db6bb373f637979cd03e73fab87`

````python
"""Consolidated linguistic layers for the production analyzer."""

from .evidence_gate import analyze_integrated_alpha2 as analyze_layers

__all__ = ["analyze_layers"]
````

### `JP analyzer/app/analyzer/layers/candidates.py`

- Purpose: Python source.
- Size: 14030 bytes
- SHA-256: `0593de79bc20537e2a0668e673b5429c116cbf9c7594e4119074287483ec363f`

````python
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
import unicodedata
from .structure import analyze_layered_alpha31

LEXICAL_EXTRA_POS = {"DET", "CCONJ", "NUM"}
DISCOURSE_FORMS = {"そして", "しかし", "また", "それでも", "でも", "だから", "ところで", "それに"}
COUNTER_TAG_HINTS = ("助数詞", "名詞-普通名詞-助数詞可能")
COUNTER_SURFACES = {
    "歳", "才", "年", "月", "日", "回", "階", "週間", "週", "人", "個", "本", "枚", "匹", "台", "冊", "度", "時", "分", "秒", "円", "対"
}
AUX_HEADS = {"いる", "ある", "おく", "いく", "くる", "もらう"}


def _snapshot(items: list[dict[str, Any]]) -> str:
    payload = repr([(x.get("id"), x.get("start"), x.get("end"), x.get("surface"), x.get("lemma"), x.get("pos"), x.get("tag")) for x in items])
    return sha256(payload.encode("utf-8")).hexdigest()


def _add_grammar(out, seen, text, ms, start_i, end_i, gid, canonical, function, confidence, priority, evidence_detail):
    a, b = ms[start_i]["start"], ms[end_i - 1]["end"]
    key = (a, b, gid)
    if key in seen:
        return
    out.append({
        "id": f"a32g{len(out)}",
        "start": a,
        "end": b,
        "surface": text[a:b],
        "grammar_id": gid,
        "canonical_form": canonical,
        "function": function,
        "host_predicate_id": None,
        "morpheme_ids": [m["id"] for m in ms[start_i:end_i]],
        "confidence": confidence,
        "priority": priority,
        "evidence": [{"source": "alpha3.2-compositional-grammar", "detail": evidence_detail, "confidence": confidence}],
    })
    seen.add(key)


def _expand_grammar(text, morphemes, existing):
    """Add grammar families without changing Alpha 3.1 records."""
    out = deepcopy(existing)
    seen = {(g["start"], g["end"], g["grammar_id"]) for g in out}
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    n = len(ms)

    for i in range(n):
        # Vて/で + dependent auxiliary (+ inflection chain)
        if ms[i].get("surface") not in {"て", "で"}:
            continue
        if i + 1 >= n:
            continue
        aux = ms[i + 1]
        lemma = aux.get("lemma")
        if lemma not in AUX_HEADS:
            continue
        end = i + 2
        while end < n and ms[end].get("pos") == "AUX" and ms[end]["start"] == ms[end - 1]["end"]:
            end += 1
        gid_map = {
            "いる": "TE_IRU_CHAIN",
            "ある": "TE_ARU",
            "おく": "TE_OKU",
            "いく": "TE_IKU",
            "くる": "TE_KURU",
            "もらう": "TE_MORAU",
        }
        fun_map = {
            "いる": "progressive-resultative",
            "ある": "resultant-state",
            "おく": "preparatory-action",
            "いく": "directional-or-continuative-away",
            "くる": "directional-or-continuative-toward",
            "もらう": "benefactive-reception",
        }
        _add_grammar(out, seen, text, ms, i, end, gid_map[lemma], f"V{ms[i]['surface']} + {lemma}", fun_map[lemma], .95, 116, f"conjunctive + dependent {lemma} chain")

    # Surface families whose pedagogical boundary is larger than one morpheme.
    surface_patterns = [
        ("かもしれない", "KAMOSHIRENAI", "かもしれない", "possibility", .98, 130),
        ("にとって", "NI_TOTTE", "にとって", "perspective-or-relevance", .97, 120),
        ("という間に", "TO_IU_AIDA_NI", "という間に", "during-the-brief-time", .96, 118),
        ("とばかりに", "TO_BAKARI_NI", "とばかりに", "as-if-to-say", .96, 118),
        ("たばかり", "TA_BAKARI", "Vたばかり", "recent-completion", .96, 116),
        ("というか", "TO_IU_KA", "というか", "rephrasing-or-qualification", .94, 108),
        ("ではなかった", "NEGATIVE_COPULA_PAST", "ではなかった", "past-negative-copula", .98, 125),
        ("ではない", "NEGATIVE_COPULA", "ではない", "negative-copula", .98, 122),
        ("ようだった", "YOU_DA_PAST", "ようだった", "appearance-or-similarity-past", .95, 112),
        ("ようだ", "YOU_DA", "ようだ", "appearance-or-similarity", .95, 110),
        ("んです", "NO_DA_POLITE", "のです", "explanatory-polite", .94, 105),
        ("のだ", "NO_DA", "のだ", "explanatory", .93, 102),
    ]
    for surf, gid, canonical, function, conf, pri in surface_patterns:
        p = 0
        while True:
            p = text.find(surf, p)
            if p < 0:
                break
            e = p + len(surf)
            inside = [k for k, m in enumerate(ms) if p <= m["start"] and m["end"] <= e]
            if inside:
                _add_grammar(out, seen, text, ms, min(inside), max(inside) + 1, gid, canonical, function, conf, pri, f"licensed surface family {surf}")
            p = e
    return out


def _numeral_expressions(text, morphemes):
    out = []
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    i = 0
    while i < len(ms):
        m = ms[i]
        if m.get("pos") != "NUM" and "数詞" not in m.get("tag", ""):
            i += 1
            continue
        end_i = i + 1
        # Allow counter/unit chains and numeral ratios such as 一対一.
        while end_i < len(ms) and ms[end_i]["start"] == ms[end_i - 1]["end"]:
            x = ms[end_i]
            if x.get("pos") == "NUM" or any(h in x.get("tag", "") for h in COUNTER_TAG_HINTS) or x.get("surface") in COUNTER_SURFACES:
                end_i += 1
                continue
            break
        # Keep a bare numeral as a useful numeral annotation too.
        a, b = m["start"], ms[end_i - 1]["end"]
        counter = text[m["end"]:b] or None
        out.append({
            "id": f"num{len(out)}", "start": a, "end": b, "surface": text[a:b],
            "role": "numeral-expression", "value_surface": m["surface"], "counter_surface": counter,
            "morpheme_ids": [x["id"] for x in ms[i:end_i]], "confidence": .96 if counter else .9,
            "evidence": [{"source": "alpha3.2-numeral-composition", "detail": "NUM plus contiguous counter/unit"}],
        })
        i = end_i
    return out


def _discourse_connectives(text, morphemes):
    out = []
    for m in morphemes:
        if m["surface"] in DISCOURSE_FORMS or m.get("pos") == "CCONJ":
            out.append({
                "id": f"disc{len(out)}", "start": m["start"], "end": m["end"], "surface": m["surface"],
                "role": "discourse-connective", "headword": m.get("lemma") or m["surface"], "morpheme_ids": [m["id"]],
                "confidence": .94, "evidence": [{"source": "alpha3.2-discourse-policy", "detail": f"{m.get('pos')}/{m.get('tag')}"}],
            })
    return out


def _lexical_items(text, morphemes, base_lexical, grammar, numerals, discourse, persons, orthography):
    """Create Alpha 3.2 lexical proposals; earlier lexical arrays remain untouched."""
    out = deepcopy(base_lexical)
    covered = {(x["start"], x["end"], x.get("lexical_type"), x.get("headword")) for x in out}
    grammar_ranges = [(g["start"], g["end"]) for g in grammar]
    person_ranges = [(p["start"], p["end"]) for p in persons]
    punct_ranges = [(o["start"], o["end"]) for o in orthography]
    numeral_ranges = {(n["start"], n["end"]) for n in numerals}
    discourse_ranges = {(d["start"], d["end"]) for d in discourse}

    # Remove earlier terms fully swallowed by newer grammar; preserve the earlier array separately.
    out = [x for x in out if not any(a <= x["start"] and x["end"] <= b for a, b in grammar_ranges)]

    for m in morphemes:
        a, b = m["start"], m["end"]
        if any(x <= a and b <= y for x, y in person_ranges + punct_ranges + grammar_ranges):
            continue
        if (a, b) in numeral_ranges or (a, b) in discourse_ranges:
            continue
        if m.get("pos") not in LEXICAL_EXTRA_POS:
            continue
        key = (a, b, "term", m.get("lemma") or m["surface"])
        if key in covered:
            continue
        out.append({
            "id": f"a32l{len(out)}", "start": a, "end": b, "surface": m["surface"],
            "headword": m.get("lemma") or m["surface"], "normalized_headword": m.get("normalized") or m["surface"],
            "lexical_type": "term", "morpheme_ids": [m["id"]], "confidence": .88,
            "evidence": [{"source": "alpha3.2-lexical-class", "detail": f"supported POS {m.get('pos')}"}],
        })
        covered.add(key)
    return out


def _name_diagnostics(text, morphemes, persons):
    out = []
    # Roman/katakana yes/no discourse should not become a person just because the parser says PROPN.
    for p in persons:
        if p["surface"] in {"イエス", "ノー"} or p["surface"].startswith("イエスとも"):
            out.append({"severity": "warning", "code": "SUSPICIOUS_PROPER_NAME", "message": p["surface"], "start": p["start"], "end": p["end"]})
    # Adjacent proper-name-like tokens are review candidates for full-name composition.
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    for i in range(len(ms) - 1):
        a, b = ms[i], ms[i + 1]
        if a["end"] != b["start"]:
            continue
        if ("固有名詞" in a.get("tag", "") or a.get("pos") == "PROPN") and ("人名" in b.get("tag", "") or b.get("pos") == "PROPN"):
            out.append({"severity": "info", "code": "POSSIBLE_MULTI_TOKEN_NAME", "message": text[a["start"]:b["end"]], "start": a["start"], "end": b["end"]})
    return out


def _project(text, morphemes, orthography, persons, grammar, lexical, numerals, discourse):
    claims = [None] * len(text)
    decisions = []
    def put(a, b, role, priority, source, head=None, gid=None, confidence=1.0):
        for i in range(a, b):
            c = {"priority": priority, "role": role, "headword": head, "grammar_id": gid, "confidence": confidence, "source": source}
            if claims[i] is None or priority > claims[i]["priority"]:
                claims[i] = c
    for m in morphemes:
        if m.get("pos") in {"ADP", "PART", "AUX", "SCONJ"}:
            put(m["start"], m["end"], "particle", 30, "morphology")
    for l in lexical:
        put(l["start"], l["end"], "proper-name" if l.get("lexical_type") == "proper-name" else "term", 80 if l.get("lexical_type") == "proper-name" else 60, l["id"], l.get("headword"), None, l.get("confidence", .8))
    for d in discourse:
        put(d["start"], d["end"], "term", 90, d["id"], d["headword"], None, d["confidence"])
    for n in numerals:
        put(n["start"], n["end"], "term", 92, n["id"], n["surface"], None, n["confidence"])
    for g in sorted(grammar, key=lambda x: (x.get("priority", 0), x["end"] - x["start"])):
        put(g["start"], g["end"], "grammar", 150 + g.get("priority", 0), g["id"], None, g["grammar_id"], g.get("confidence", .9))
    for o in orthography:
        put(o["start"], o["end"], "punctuation", 300, o["id"], None, None, 1.0)
    for i in range(len(text)):
        if claims[i] is None:
            claims[i] = {"priority": 0, "role": "unresolved", "headword": None, "grammar_id": None, "confidence": 0.0, "source": "none"}
    spans = []; a = 0
    def same(x, y):
        return all(x[k] == y[k] for k in ("role", "headword", "grammar_id", "confidence", "source"))
    for i in range(1, len(text) + 1):
        if i == len(text) or not same(claims[a], claims[i]):
            c = claims[a]; rid = f"a32rd{len(decisions)}"
            decisions.append({"id": rid, "start": a, "end": i, "surface": text[a:i], "selected_role": c["role"], "selected_source": c["source"], "reason": "Alpha 3.2 projection priority; all earlier annotations preserved", "confidence": c["confidence"]})
            spans.append({"start": a, "end": i, "surface": text[a:i], "role": c["role"], "headword": c["headword"], "grammar_id": c["grammar_id"], "confidence": c["confidence"], "evidence_ids": [c["source"], rid]})
            a = i
    return spans, decisions


def analyze_layered_alpha32(text, nlp, dictionary_evidence=None):
    base = analyze_layered_alpha31(text, nlp, dictionary_evidence)
    result = deepcopy(base)
    ms = deepcopy(result["morphemes"])
    before = _snapshot(ms)

    grammar = _expand_grammar(text, ms, result["grammar_matches_alpha31"])
    numerals = _numeral_expressions(text, ms)
    discourse = _discourse_connectives(text, ms)
    lexical = _lexical_items(text, ms, result["lexical_items_alpha31"], grammar, numerals, discourse, result["person_references"], result["orthographic_spans"])
    colors, decisions = _project(text, ms, result["orthographic_spans"], result["person_references"], grammar, lexical, numerals, discourse)
    name_diags = _name_diagnostics(text, ms, result["person_references"])

    diagnostics = []
    if before != _snapshot(ms):
        diagnostics.append({"severity": "error", "code": "MORPHOLOGY_MUTATED", "message": "Alpha 3.2 changed Layer 0 morphology."})
    if "".join(s["surface"] for s in colors) != text:
        diagnostics.append({"severity": "error", "code": "A32_COLOR_INCOMPLETE", "message": "Alpha 3.2 projection does not reconstruct source text."})

    result.update({
        "version": "8.0.0-alpha3.2",
        "grammar_matches_alpha32": grammar,
        "numeral_expressions_alpha32": numerals,
        "discourse_connectives_alpha32": discourse,
        "lexical_items_alpha32": lexical,
        "reader_decisions_alpha32": decisions,
        "color_spans_alpha32": colors,
        "name_diagnostics_alpha32": name_diags,
        "diagnostics_alpha32": diagnostics,
        "layer0_snapshot_alpha32": before,
        "alpha32_contract": {"non_destructive": True, "alpha31_preserved": True, "only_reader_projection_is_exclusive": True},
    })
    return result

````

### `JP analyzer/app/analyzer/layers/decision.py`

- Purpose: Python source.
- Size: 18697 bytes
- SHA-256: `2101e09eca13a5b3fa4bb8e614c82958c6e999898665ec962b1559271640a2c8`

````python
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

````

### `JP analyzer/app/analyzer/layers/dictionary.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 11550 bytes
- SHA-256: `91636e767134430cc58f6eef7c0bcc5771ca8884357ba636672f574488a92349`

````python
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
````

### `JP analyzer/app/analyzer/layers/dictionary_api.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 1506 bytes
- SHA-256: `a9946dea6c6a38d694abd6827a82dbee93defbd2ddbb74c27a1a790ded573eb5`

````python
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
````

### `JP analyzer/app/analyzer/layers/dictionary_evidence_api.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 720 bytes
- SHA-256: `c6d4a8dfc34e6ff50987f9bcc011b5c4d656272ae3a779a60c8956d319432cb2`

````python
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
````

### `JP analyzer/app/analyzer/layers/dictionary_store.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 6793 bytes
- SHA-256: `17fe42a1b5329380a04a8d52fde8842f3adcec4e8b9bb2faa9797de60f66e4a7`

````python
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
````

### `JP analyzer/app/analyzer/layers/evidence_gate.py`

- Purpose: Python source.
- Size: 16317 bytes
- SHA-256: `c341fcf2a30bcb7ac4105784a10be1c7549c94e69cc2c46e3033c1a1ea6ef85b`

````python
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

````

### `JP analyzer/app/analyzer/layers/grammar.py`

- Purpose: Python source.
- Size: 2062 bytes
- SHA-256: `cac8c93043717fd27fac9a57064588acbc6a170c812d62f3af69564694867bdc`

````python
from .schema import GrammarMatch,Evidence
PATTERNS=[('V_TA_RASHII','Vた + らしい','evidential-inference',('た','らしい'),80),('TE_KURERU','Vて + くれる','benefactive',('て','くれる'),85),('TE_SHIMAU','Vて + しまう','completion-or-regret',('て','しまう'),85),('KOTO_GA_DEKIRU','Vことができる','ability',('こと','が','できる'),95)]
def detect(text,ms,preds):
 out=[]
 def host(start):
  p=[x for x in preds if x.end<=start]; return max(p,key=lambda x:x.end).id if p else None
 for gid,can,fun,seq,pri in PATTERNS:
  for i in range(len(ms)-len(seq)+1):
   w=ms[i:i+len(seq)]
   if tuple(x.lemma for x in w)!=seq: continue
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id=gid,canonical_form=can,function=fun,host_predicate_id=host(w[0].start),morpheme_ids=[x.id for x in w],start=w[0].start,end=w[-1].end,surface=text[w[0].start:w[-1].end],confidence=.94,priority=pri,evidence=[Evidence(source='grammar-pattern',detail='lemma window',confidence=.94)]))
 for m in ms:
  if m.surface in {'て','で'} and m.pos in {'SCONJ','PART'} and not any(g.start<=m.start and m.end<=g.end for g in out):
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id='V_TE',canonical_form='Vて',function='conjunctive',host_predicate_id=host(m.start),morpheme_ids=[m.id],start=m.start,end=m.end,surface=m.surface,confidence=.85,priority=40,evidence=[Evidence(source='morphology',detail='conjunctive marker',confidence=.85)]))
 # surface family because analyzers differ on negative morphology
 for surface in ('なければならない','なくてはならない'):
  p=text.find(surface)
  if p>=0:
   mids=[m.id for m in ms if p<=m.start and m.end<=p+len(surface)]
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id='NAKEREBA_NARANAI',canonical_form='なければならない',function='obligation',host_predicate_id=None,morpheme_ids=mids,start=p,end=p+len(surface),surface=surface,confidence=.98,priority=100,evidence=[Evidence(source='grammar-pattern',detail='licensed full surface',confidence=.98)]))
 return out
````

### `JP analyzer/app/analyzer/layers/invariants.py`

- Purpose: Python source.
- Size: 5515 bytes
- SHA-256: `03f9d5482d133d5888b8df3304dfa8ced196516322511dc514735df160d3cac4`

````python
from .schema import Diagnostic, LayeredAnalysis

FUNCTION_POS = {"ADP", "AUX", "SCONJ", "PART", "PUNCT", "SYM"}


def validate(a: LayeredAnalysis):
    out = []
    cursor = 0

    # Reader projection must form an exact, non-overlapping partition.
    for span in sorted(a.color_spans, key=lambda x: (x.start, x.end)):
        if span.start != cursor:
            out.append(
                Diagnostic(
                    severity="error",
                    code="COLOR_GAP_OR_OVERLAP",
                    message=f"Expected {cursor}, found {span.start}",
                    start=cursor,
                    end=span.start,
                )
            )
        if span.surface != a.text[span.start:span.end] or span.end <= span.start:
            out.append(
                Diagnostic(
                    severity="error",
                    code="COLOR_RANGE_INVALID",
                    message="Color range mismatch",
                    start=span.start,
                    end=span.end,
                )
            )
        cursor = span.end

    if cursor != len(a.text):
        out.append(
            Diagnostic(
                severity="error",
                code="COLOR_INCOMPLETE",
                message="Color partition incomplete",
                start=cursor,
                end=len(a.text),
            )
        )

    morphemes = {m.id: m for m in a.morphemes}
    entities = {e.id: e for e in a.entities}
    predicates = {p.id: p for p in a.predicates}

    for m in a.morphemes:
        if m.surface != a.text[m.start:m.end]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="MORPHEME_RANGE_INVALID",
                    message=m.id,
                    start=m.start,
                    end=m.end,
                )
            )

    # Bunsetsu heads must be content heads, never punctuation/function tokens.
    for phrase in a.basic_phrases:
        head = morphemes.get(phrase.head_id or "")
        if head and head.pos in {"PUNCT", "SYM"}:
            out.append(
                Diagnostic(
                    severity="error",
                    code="BUNSETSU_HEAD_IS_PUNCTUATION",
                    message=f"{phrase.id} points to punctuation head {head.id}",
                    start=phrase.start,
                    end=phrase.end,
                )
            )

    # General dictionary lookup must never target protected person/name spans.
    protected_names = [
        e for e in a.entities if e.protected and e.entity_class == "proper-name"
    ]
    for candidate in a.dictionary_candidates:
        for entity in protected_names:
            if entity.start <= candidate.start and candidate.end <= entity.end:
                out.append(
                    Diagnostic(
                        severity="error",
                        code="DICTIONARY_CANDIDATE_INSIDE_PROTECTED_NAME",
                        message=f"{candidate.id} is inside protected name {entity.surface}",
                        start=candidate.start,
                        end=candidate.end,
                    )
                )

    # Predicate relations should retain their visible connective when available.
    for relation in a.predicate_relations:
        if relation.from_predicate_id not in predicates or relation.to_predicate_id not in predicates:
            out.append(
                Diagnostic(
                    severity="error",
                    code="PREDICATE_RELATION_TARGET_MISSING",
                    message=relation.id,
                )
            )
        if relation.marker_range is None:
            out.append(
                Diagnostic(
                    severity="warning",
                    code="PREDICATE_RELATION_MARKER_MISSING",
                    message=f"{relation.id} has no connective marker",
                )
            )
        elif relation.marker_range.surface != a.text[
            relation.marker_range.start : relation.marker_range.end
        ]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="PREDICATE_RELATION_MARKER_INVALID",
                    message=relation.id,
                    start=relation.marker_range.start,
                    end=relation.marker_range.end,
                )
            )

    # Japanese prenominal relative clauses should finish before the modified noun.
    for clause in a.clauses:
        if clause.clause_type != "relative-clause" or clause.modifies_range is None:
            continue
        if clause.end > clause.modifies_range.start:
            out.append(
                Diagnostic(
                    severity="error",
                    code="RELATIVE_CLAUSE_CROSSES_MODIFIED_NOUN",
                    message=f"{clause.id} extends into {clause.modifies_range.surface}",
                    start=clause.start,
                    end=clause.end,
                )
            )
        if clause.surface != a.text[clause.start:clause.end]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="RELATIVE_CLAUSE_RANGE_INVALID",
                    message=clause.id,
                    start=clause.start,
                    end=clause.end,
                )
            )

    return out
````

### `JP analyzer/app/analyzer/layers/kwja.py`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 16074 bytes
- SHA-256: `efe44b02d5598926c846dcf5b2d9f719cf2d10950913cda0fcaa918f57c04054`

````python
from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

VERSION = "9.0.0-alpha1-readonly"
_FEATURE_RE = re.compile(r"<([^<>]+)>")
_REL_RE = re.compile(r'^rel type="([^"]+)" target="([^"]*)"(?: sid="([^"]*)")?(?: id="([^"]*)")?/?$')
_HEADER_RE = re.compile(r"^([*+])\s+(-?\d+)([A-Z])?(?:\s+(.*))?$")

# KWJA may normalize source punctuation in the morpheme surface column.
_SURFACE_ALIASES = {
    "~": ("～", "~"),
    "......": ("……", "...", "......"),
    "?": ("？", "?"),
    "!": ("！", "!"),
    ".": ("．", "."),
    "-": ("−", "-"),
}


@dataclass
class _Morpheme:
    surface: str
    reading: str
    lemma: str
    pos: str
    pos_id: str
    subpos: str
    subpos_id: str
    conjugation_type: str
    conjugation_type_id: str
    conjugation_form: str
    conjugation_form_id: str
    semantic: str = ""
    features: list[str] = field(default_factory=list)
    start: int | None = None
    end: int | None = None
    aligned_surface: str | None = None


@dataclass
class _BasicPhrase:
    index: int
    destination: int
    dependency_type: str
    features: list[str]
    morphemes: list[_Morpheme] = field(default_factory=list)


@dataclass
class _Bunsetsu:
    index: int
    destination: int
    dependency_type: str
    features: list[str]
    basic_phrases: list[_BasicPhrase] = field(default_factory=list)


def _extract_features(text: str) -> list[str]:
    return _FEATURE_RE.findall(text or "")


def _parse_morpheme(line: str) -> _Morpheme | None:
    # KNP guarantees 12 fixed whitespace-separated fields; semantic/features follow.
    fields = line.split(maxsplit=11)
    if len(fields) < 11:
        return None
    semantic = fields[11] if len(fields) > 11 else ""
    return _Morpheme(
        surface=fields[0], reading=fields[1], lemma=fields[2], pos=fields[3],
        pos_id=fields[4], subpos=fields[5], subpos_id=fields[6],
        conjugation_type=fields[7], conjugation_type_id=fields[8],
        conjugation_form=fields[9], conjugation_form_id=fields[10],
        semantic=semantic, features=_extract_features(semantic),
    )


def parse_knp(text: str) -> dict[str, Any]:
    bunsetsu: list[_Bunsetsu] = []
    current_b: _Bunsetsu | None = None
    current_bp: _BasicPhrase | None = None
    metadata: dict[str, Any] = {}
    diagnostics: list[dict[str, Any]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "EOS":
            continue
        if line.startswith("#"):
            metadata["header"] = line
            m = re.search(r"kwja:([^\s]+)", line)
            if m:
                metadata["kwja_version"] = m.group(1)
            continue
        hm = _HEADER_RE.match(line)
        if hm:
            kind, destination, dep_type, remainder = hm.groups()
            features = _extract_features(remainder or "")
            if kind == "*":
                current_b = _Bunsetsu(len(bunsetsu), int(destination), dep_type or "D", features)
                bunsetsu.append(current_b)
                current_bp = None
            else:
                if current_b is None:
                    diagnostics.append({"severity":"error","code":"KWJA_BASIC_PHRASE_WITHOUT_BUNSETSU","line":line})
                    continue
                current_bp = _BasicPhrase(sum(len(x.basic_phrases) for x in bunsetsu), int(destination), dep_type or "D", features)
                current_b.basic_phrases.append(current_bp)
            continue
        if current_bp is None:
            diagnostics.append({"severity":"warning","code":"KWJA_MORPHEME_WITHOUT_BASIC_PHRASE","line":line})
            continue
        morpheme = _parse_morpheme(line)
        if morpheme is None:
            diagnostics.append({"severity":"warning","code":"KWJA_UNPARSED_LINE","line":line})
        else:
            current_bp.morphemes.append(morpheme)
    return {"metadata": metadata, "bunsetsu": bunsetsu, "diagnostics": diagnostics}


def _candidate_surfaces(surface: str) -> tuple[str, ...]:
    return _SURFACE_ALIASES.get(surface, (surface,))


def align_to_source(source: str, bunsetsu: list[_Bunsetsu]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    cursor = 0
    for b in bunsetsu:
        for bp in b.basic_phrases:
            for m in bp.morphemes:
                candidates = _candidate_surfaces(m.surface)
                matched = None
                for candidate in sorted(candidates, key=len, reverse=True):
                    if source.startswith(candidate, cursor):
                        matched = candidate
                        break
                if matched is None:
                    # Strict monotonic recovery: search only a short forward window and
                    # report skipped source; never align backward or silently guess.
                    hits = [(source.find(x, cursor, min(len(source), cursor + 12)), x) for x in candidates]
                    hits = [(i, x) for i, x in hits if i >= 0]
                    if hits:
                        start, matched = min(hits, key=lambda z: z[0])
                        if start > cursor:
                            diagnostics.append({
                                "severity":"warning", "code":"KWJA_ALIGNMENT_SOURCE_GAP",
                                "start":cursor, "end":start, "surface":source[cursor:start],
                                "kwja_surface":m.surface,
                            })
                        cursor = start
                    else:
                        diagnostics.append({
                            "severity":"error", "code":"KWJA_ALIGNMENT_FAILED",
                            "source_cursor":cursor, "kwja_surface":m.surface,
                        })
                        continue
                m.start = cursor
                m.end = cursor + len(matched)
                m.aligned_surface = source[m.start:m.end]
                cursor = m.end
    if cursor != len(source):
        diagnostics.append({
            "severity":"error", "code":"KWJA_ALIGNMENT_TRAILING_SOURCE",
            "start":cursor, "end":len(source), "surface":source[cursor:],
        })
    return diagnostics


def _span(morphemes: list[_Morpheme], source: str) -> dict[str, Any] | None:
    aligned = [m for m in morphemes if m.start is not None and m.end is not None]
    if not aligned:
        return None
    start, end = min(m.start for m in aligned), max(m.end for m in aligned)
    return {"start":start, "end":end, "surface":source[start:end]}


def _feature_values(features: list[str], prefix: str) -> list[str]:
    return [x.split(":", 1)[1] for x in features if x.startswith(prefix + ":")]


def normalize_kwja(source: str, raw_knp: str, *, model_size: str = "base", elapsed_ms: float | None = None) -> dict[str, Any]:
    parsed = parse_knp(raw_knp)
    bunsetsu: list[_Bunsetsu] = parsed["bunsetsu"]
    alignment_diagnostics = align_to_source(source, bunsetsu)
    morphemes: list[dict[str, Any]] = []
    basic_phrases: list[dict[str, Any]] = []
    bunsetsu_rows: list[dict[str, Any]] = []
    dependencies: list[dict[str, Any]] = []
    predicates: list[dict[str, Any]] = []
    arguments: list[dict[str, Any]] = []
    entities: list[dict[str, Any]] = []
    clauses: list[dict[str, Any]] = []
    modalities: list[dict[str, Any]] = []
    discourse: list[dict[str, Any]] = []

    bp_index = 0
    for b in bunsetsu:
        b_morphs = [m for bp in b.basic_phrases for m in bp.morphemes]
        bspan = _span(b_morphs, source)
        if bspan:
            bunsetsu_rows.append({
                "id":f"kwb{b.index}", **bspan,
                "destination_bunsetsu_id": None if b.destination < 0 else f"kwb{b.destination}",
                "dependency_type":b.dependency_type, "features":b.features,
            })
        for bp in b.basic_phrases:
            span = _span(bp.morphemes, source)
            if not span:
                bp_index += 1
                continue
            bp_id = f"kwbp{bp_index}"
            all_features = list(dict.fromkeys(bp.features + b.features))
            basic_phrases.append({
                "id":bp_id, **span, "bunsetsu_id":f"kwb{b.index}",
                "destination_basic_phrase_id":None if bp.destination < 0 else f"kwbp{bp.destination}",
                "dependency_type":bp.dependency_type, "features":all_features,
            })
            if bp.destination >= 0:
                dependencies.append({
                    "id":f"kwdep{len(dependencies)}", "from_basic_phrase_id":bp_id,
                    "to_basic_phrase_id":f"kwbp{bp.destination}", "dependency_type":bp.dependency_type,
                    **span,
                })
            for m in bp.morphemes:
                if m.start is None:
                    continue
                mid = f"kwm{len(morphemes)}"
                morphemes.append({
                    "id":mid, "start":m.start, "end":m.end, "surface":m.aligned_surface,
                    "kwja_surface":m.surface, "reading":m.reading, "lemma":m.lemma,
                    "pos":m.pos, "pos_id":m.pos_id, "subpos":m.subpos,
                    "subpos_id":m.subpos_id, "conjugation_type":m.conjugation_type,
                    "conjugation_form":m.conjugation_form, "features":m.features,
                    "basic_phrase_id":bp_id,
                    "authority":{"range":True,"reading":False,"lemma_requires_corroboration":True},
                })
            predicate_types = _feature_values(all_features, "用言")
            if predicate_types:
                predicates.append({
                    "id":f"kwp{len(predicates)}", **span, "basic_phrase_id":bp_id,
                    "predicate_types":predicate_types,
                    "state":"state" if "状態述語" in all_features else ("dynamic" if "動態述語" in all_features else None),
                    "tense":_feature_values(all_features,"時制"),
                    "negative":"否定表現" in all_features,
                    "potential":"可能表現" in all_features,
                    "politeness":[x for x in all_features if x.startswith("敬語:")],
                    "evidence_only":True,
                })
            for feature in all_features:
                rm = _REL_RE.match(feature)
                if rm:
                    rel_type, target, sid, target_id = rm.groups()
                    arguments.append({
                        "id":f"kwa{len(arguments)}", **span, "predicate_basic_phrase_id":bp_id,
                        "relation_type":rel_type, "target_surface":target,
                        "target_sentence_id":sid, "target_kwja_id":target_id,
                        "status":"proposal", "requires_corroboration":True,
                    })
                if feature.startswith("NE:"):
                    parts = feature.split(":", 2)
                    named_surface = parts[2] if len(parts) == 3 else span["surface"]
                    loc = source.find(named_surface, span["start"], span["end"])
                    if loc >= 0:
                        entities.append({
                            "id":f"kwe{len(entities)}", "start":loc, "end":loc+len(named_surface),
                            "surface":named_surface, "entity_type":parts[1],
                            "source_basic_phrase_id":bp_id, "evidence_only":True,
                        })
                if feature.startswith("節-"):
                    clauses.append({
                        "id":f"kwc{len(clauses)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
                if feature.startswith("モダリティ-"):
                    modalities.append({
                        "id":f"kwmod{len(modalities)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
                if feature.startswith("談話関係:"):
                    discourse.append({
                        "id":f"kwdis{len(discourse)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
            bp_index += 1

    diagnostics = parsed["diagnostics"] + alignment_diagnostics
    complete = not any(x.get("severity") == "error" for x in diagnostics)
    return {
        "kwja_metadata_alpha1": {
            "available":True, "layer_version":VERSION, "kwja_version":parsed["metadata"].get("kwja_version"),
            "model_size":model_size, "elapsed_ms":elapsed_ms, "source_alignment_complete":complete,
            "read_only":True,
        },
        "kwja_morphemes_alpha1":morphemes,
        "kwja_bunsetsu_alpha1":bunsetsu_rows,
        "kwja_basic_phrases_alpha1":basic_phrases,
        "kwja_dependencies_alpha1":dependencies,
        "kwja_predicate_phrases_alpha1":predicates,
        "kwja_argument_evidence_alpha1":arguments,
        "kwja_entities_alpha1":entities,
        "kwja_clause_features_alpha1":clauses,
        "kwja_modality_features_alpha1":modalities,
        "kwja_discourse_relations_alpha1":discourse,
        "kwja_alignment_diagnostics_alpha1":diagnostics,
        "kwja_contract_alpha1": {
            "evidence_only":True, "source_text_immutable":True, "ginza_layers_immutable":True,
            "existing_resolver_immutable":True, "readings_non_authoritative":True,
            "lemmas_require_corroboration":True, "arguments_require_corroboration":True,
            "orthography_controls_punctuation":True,
        },
    }


def run_kwja(text: str, *, executable: str | None = None, model_size: str = "base", timeout_seconds: int = 300) -> tuple[str, float]:
    exe = executable or os.getenv("KWJA_EXE")
    if not exe:
        raise RuntimeError("Set KWJA_EXE to the isolated KWJA executable path.")
    path = Path(exe)
    if not path.exists():
        raise FileNotFoundError(f"KWJA executable not found: {path}")
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    # Analysis is cache-only by default. Set any variable to "0" explicitly
    # when installing or refreshing models in a controlled online session.
    env.setdefault("HF_HUB_OFFLINE", "1")
    env.setdefault("TRANSFORMERS_OFFLINE", "1")
    env.setdefault("HF_DATASETS_OFFLINE", "1")
    started = time.perf_counter()
    result = subprocess.run(
        [str(path), "--model-size", model_size, "--text", text],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        timeout=timeout_seconds, env=env,
    )
    elapsed = (time.perf_counter() - started) * 1000
    return result.stdout.decode("utf-8", errors="strict"), elapsed


def analyze_kwja_alpha1(text: str, *, raw_knp: str | None = None, executable: str | None = None) -> dict[str, Any]:
    if raw_knp is None:
        raw_knp, elapsed = run_kwja(text, executable=executable)
    else:
        elapsed = None
    return normalize_kwja(text, raw_knp, model_size="base", elapsed_ms=elapsed)


def attach_kwja_read_only(existing_analysis: dict[str, Any], kwja_layer: dict[str, Any]) -> dict[str, Any]:
    """Return a new object and prove that pre-existing fields are retained unchanged."""
    result = dict(existing_analysis)
    collision = set(result).intersection(kwja_layer)
    if collision:
        raise ValueError(f"KWJA layer would overwrite existing fields: {sorted(collision)}")
    result.update(kwja_layer)
    result["phase9_alpha1_contract"] = {
        "read_only":True, "existing_field_count":len(existing_analysis),
        "kwja_field_count":len(kwja_layer), "overwritten_fields":[],
    }
    return result

````

### `JP analyzer/app/analyzer/layers/morphology.py`

- Purpose: Python source.
- Size: 9831 bytes
- SHA-256: `56b991e10c6bb3d1232911ed1acd56b4418920ff6397f6889ce0edd27584934c`

````python
from __future__ import annotations
from .schema import *
from .grammar import detect
from .invariants import validate
PUNCT={'PUNCT','SYM'}; NOMINAL={'NOUN','PROPN','PRON','NUM'}
PROPER_NER={'Person','PERSON','Character','Company','Organization','ORG','Country','City','Facility','GPE','LOC','Product','Book'}
TEMP_NER_PREFIX=('Date','Time','Period','Duration','Age')

def morphemes(doc):
 out=[]
 for i,t in enumerate(doc):
  try: inf=list(t.morph.get('Inflection')); reading=(list(t.morph.get('Reading')) or [None])[0]
  except Exception: inf=[]; reading=None
  out.append(Morpheme(id=f'm{i}',surface=t.text,start=t.idx,end=t.idx+len(t.text),lemma=t.lemma_,normalized=t.norm_,reading=reading,pos=t.pos_,tag=t.tag_,dependency=t.dep_,head_id=f'm{t.head.i}',conjugation=inf))
 return out

def entities(doc,ms):
 out=[]; occupied=set()
 for m in ms:
  if '固有名詞-人名' in m.tag:
   out.append(EntitySpan(id=f'e{len(out)}',start=m.start,end=m.end,surface=m.surface,entity_type='Person',entity_class='proper-name',protected=True,morpheme_ids=[m.id],evidence=[Evidence(source='morphology',detail=m.tag,confidence=.95)])); occupied.update(range(m.start,m.end))
 for e in doc.ents:
  mids=[m.id for m in ms if e.start_char<=m.start and m.end<=e.end_char]
  cls='proper-name' if e.label_ in PROPER_NER else ('temporal' if e.label_.startswith(TEMP_NER_PREFIX) else 'semantic-category')
  protected=cls in {'proper-name','temporal'}
  if cls=='proper-name' and all(i in occupied for i in range(e.start_char,e.end_char)): continue
  out.append(EntitySpan(id=f'e{len(out)}',start=e.start_char,end=e.end_char,surface=e.text,entity_type=e.label_,entity_class=cls,protected=protected,morpheme_ids=mids,evidence=[Evidence(source='ginza-ner',detail=e.label_,confidence=.75)]))
 return out

def particle_phrases(text,ms):
 out=[]
 for i,m in enumerate(ms):
  if m.pos not in {'ADP','PART'} or '接続助詞' in m.tag or i==0: continue
  head=ms[i-1]
  if head.pos not in NOMINAL: continue
  out.append(ParticlePhrase(id=f'pp{len(out)}',start=head.start,end=m.end,surface=text[head.start:m.end],nominal_morpheme_ids=[head.id],particle_morpheme_ids=[m.id],nominal_head_id=head.id,particle_surface=m.surface,particle_type=m.tag,evidence=[Evidence(source='morphology',detail='nominal case/topic/focus phrase',confidence=.9)]))
 return out

def basic_phrases(text,doc,ms):
 out=[]
 try:
  import ginza
  spans=list(ginza.bunsetu_spans(doc))
  for s in spans:
   mids=[m.id for m in ms if s.start_char<=m.start and m.end<=s.end_char]
   head=next((m.id for m in reversed(ms) if m.id in mids and m.pos not in {'ADP','AUX','SCONJ','PART','PUNCT','SYM'}),None)
   out.append(BasicPhrase(id=f'bp{len(out)}',start=s.start_char,end=s.end_char,surface=s.text,morpheme_ids=mids,head_id=head,evidence=[Evidence(source='ginza-bunsetu',detail='native bunsetsu span',confidence=.85)]))
 except Exception as ex:
  # one morpheme per safe phrase is preferable to inventing large punctuation chunks
  for m in ms:
   if m.pos not in PUNCT: out.append(BasicPhrase(id=f'bp{len(out)}',start=m.start,end=m.end,surface=m.surface,morpheme_ids=[m.id],head_id=m.id,evidence=[Evidence(source='safe-fallback',detail='single morpheme phrase',confidence=.3)]))
 return out

def predicates(ms):
 return [Predicate(id=f'p{j}',start=m.start,end=m.end,surface=m.surface,head_morpheme_id=m.id,headword=m.lemma,morpheme_ids=[m.id],evidence=[Evidence(source='dependency',detail=f'{m.pos}/{m.dependency}',confidence=.8)]) for j,m in enumerate([x for x in ms if x.pos in {'VERB','ADJ'} and x.dependency not in {'aux','cop','fixed'}])]

def structure(text,ms,pps,preds):
 by={m.id:m for m in ms}; pb={p.head_morpheme_id:p for p in preds}; args=[]; rel=[]; clauses=[]
 for pp in pps:
  n=by[pp.nominal_head_id]; target=pb.get(n.head_id or '')
  if not target: continue
  role={'obj':'object','nsubj':'subject','obl':'oblique'}.get(n.dependency,'dependent')
  if role=='oblique': role={'に':'destination-or-target','で':'manner-or-location','から':'source','へ':'destination'}.get(pp.particle_surface,'oblique')
  args.append(Argument(id=f'a{len(args)}',predicate_id=target.id,phrase_id=pp.id,source_range=Range(start=pp.start,end=pp.end,surface=pp.surface),role=role,marker=pp.particle_surface,confidence=.78,evidence=[Evidence(source='ud-dependency',detail=n.dependency or '',confidence=.78)]))
 for p in preds:
  m=by[p.head_morpheme_id]; target=pb.get(m.head_id or '')
  if target and m.dependency in {'advcl','conj'}:
   marker=next((x for x in ms if x.head_id==m.id and x.pos in {'SCONJ','PART'}),None)
   rel.append(PredicateRelation(id=f'pr{len(rel)}',from_predicate_id=p.id,to_predicate_id=target.id,marker_range=Range(start=marker.start,end=marker.end,surface=marker.surface) if marker else None,relation='sequential-or-subordinate',confidence=.82,evidence=[Evidence(source='ud-dependency',detail=m.dependency,confidence=.82)]))
  if m.dependency=='acl':
   modified=by.get(m.head_id or '')
   if modified:
    start=min([x.start for x in ms if x.head_id==m.id]+[m.start]); end=max([x.end for x in ms if x.head_id==m.id]+[m.end])
    clauses.append(Clause(id=f'c{len(clauses)}',start=start,end=end,surface=text[start:end],clause_type='relative-clause',predicate_ids=[p.id],modifies_range=Range(start=modified.start,end=modified.end,surface=modified.surface),evidence=[Evidence(source='ud-acl',detail='predicate modifies nominal',confidence=.88)]))
 # conservative subject propagation from governing predicate to subordinate predicate
 subjects={a.predicate_id:a for a in args if a.role=='subject'}
 for r in rel:
  if r.from_predicate_id not in subjects and r.to_predicate_id in subjects:
   s=subjects[r.to_predicate_id]
   args.append(Argument(id=f'a{len(args)}',predicate_id=r.from_predicate_id,phrase_id=s.phrase_id,source_range=s.source_range,role='subject',marker=s.marker,inherited=True,confidence=.72,evidence=[Evidence(source='subject-propagation',detail='shared subject through predicate relation',confidence=.72)]))
 return args,rel,clauses

def dictionary_candidates(text,ms,ents,grammar):
 blocked=[(e.start,e.end) for e in ents if e.protected]+[(g.start,g.end) for g in grammar]
 out=[]
 for m in ms:
  if m.pos not in {'NOUN','VERB','ADJ','ADV','INTJ','PROPN'}: continue
  if any(e.entity_class=='proper-name' and e.protected and e.start<=m.start and m.end<=e.end for e in ents): continue
  if any(a<m.start<b or a<m.end<b for a,b in blocked): continue
  forms=[]
  for f in (m.surface,m.lemma,m.normalized):
   if f and f not in forms: forms.append(f)
  out.append(DictionaryCandidate(id=f'dc{len(out)}',start=m.start,end=m.end,surface=m.surface,lookup_forms=forms,candidate_type='morphological-lexeme',evidence=[Evidence(source='morphology',detail=m.tag,confidence=.85)]))
 return out

def resolve_lexical(text,ms,ents,grammar,cands,evidence):
 bycand={e.candidate_id:e for e in evidence}; out=[]
 for e in ents:
  if e.entity_class=='proper-name': out.append(LexicalItem(id=f'l{len(out)}',start=e.start,end=e.end,surface=e.surface,headword=e.surface,normalized_headword=e.surface,lexical_type='proper-name',morpheme_ids=e.morpheme_ids,confidence=.95,evidence=e.evidence))
 for c in cands:
  if any(x.start<=c.start and c.end<=x.end and x.entity_class=='proper-name' for x in ents): continue
  m=next(x for x in ms if x.start==c.start and x.end==c.end); ev=bycand.get(c.id)
  head=ev.matched_headword if ev and ev.matched_headword else m.lemma
  conf=max(.82,ev.confidence) if ev else .82
  out.append(LexicalItem(id=f'l{len(out)}',start=c.start,end=c.end,surface=c.surface,headword=head,normalized_headword=m.normalized,lexical_type='term',morpheme_ids=[m.id],confidence=conf,evidence=[Evidence(source='dictionary' if ev else 'morphology',detail=ev.match_type if ev else m.tag,confidence=conf)]))
 return out

def colors(text,ms,ents,grammar,lex):
 claims=[None]*len(text)
 def put(a,b,role,pri,head=None,gid=None,conf=1,eids=None):
  for i in range(a,b):
   if claims[i] is None or pri>claims[i][0]: claims[i]=(pri,role,head,gid,conf,eids or [])
 for m in ms:
  if m.pos in PUNCT: put(m.start,m.end,'punctuation',100)
  elif m.pos in {'ADP','PART','AUX','SCONJ'}: put(m.start,m.end,'particle',40)
 for l in lex: put(l.start,l.end,'proper-name' if l.lexical_type=='proper-name' else 'term',80 if l.lexical_type=='proper-name' else 60,l.headword,None,l.confidence,[l.id])
 for g in grammar: put(g.start,g.end,'grammar',200+g.priority,None,g.grammar_id,g.confidence,[g.id])
 for i in range(len(text)):
  if claims[i] is None: claims[i]=(0,'unresolved',None,None,0,[])
 out=[]; a=0
 def key(c): return c[1:]
 for i in range(1,len(text)+1):
  if i==len(text) or key(claims[i])!=key(claims[a]):
   _,role,head,gid,conf,eids=claims[a]; out.append(ColorSpan(start=a,end=i,surface=text[a:i],role=role,headword=head,grammar_id=gid,confidence=conf,evidence_ids=eids)); a=i
 return out

def analyze_layered(text,nlp,dictionary_evidence=None):
 doc=nlp(text); ms=morphemes(doc); es=entities(doc,ms); pps=particle_phrases(text,ms); bps=basic_phrases(text,doc,ms); ps=predicates(ms); args,rels,cls=structure(text,ms,pps,ps); gs=detect(text,ms,ps); dcs=dictionary_candidates(text,ms,es,gs); des=dictionary_evidence or []; ls=resolve_lexical(text,ms,es,gs,dcs,des); cs=colors(text,ms,es,gs,ls)
 r=LayeredAnalysis(text=text,morphemes=ms,particle_phrases=pps,basic_phrases=bps,entities=es,predicates=ps,arguments=args,predicate_relations=rels,clauses=cls,grammar_matches=gs,dictionary_candidates=dcs,dictionary_evidence=des,lexical_items=ls,color_spans=cs,diagnostics=[],parser_metadata={'parser':'GiNZA','split_mode':'A','architecture':'immutable-layers','dictionary_policy':'evidence-only'})
 r.diagnostics.extend(validate(r)); return r

````

### `JP analyzer/app/analyzer/layers/protected.py`

- Purpose: Python source.
- Size: 11156 bytes
- SHA-256: `43d146fa3ff6773b5e661d34c918f979aeca4a8f821e4fe1cab932294e04acf6`

````python
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
import unicodedata

from .morphology import analyze_layered as analyze_alpha21

HONORIFICS={"さん","くん","君","ちゃん","様","さま","氏","先生","先輩","殿","ちゃん"}
CONTENT_POS={"NOUN","VERB","ADJ","ADV","INTJ","PROPN","PRON"}
FUNCTION_DEPS={"fixed","aux","cop"}


def _snapshot(items:list[dict[str,Any]])->str:
    payload=repr([(x.get('id'),x.get('start'),x.get('end'),x.get('surface'),x.get('lemma'),x.get('pos'),x.get('tag')) for x in items])
    return sha256(payload.encode('utf-8')).hexdigest()


def _is_punct(m:dict[str,Any])->bool:
    surface=m['surface']; tag=m.get('tag','')
    return tag.startswith('補助記号') or m.get('pos') in {'PUNCT','SYM'} or (surface and all(unicodedata.category(c).startswith('P') or c in '─—―…⋯〜～' for c in surface))


def orthography(text,ms):
    out=[]; i=0
    while i<len(ms):
        if not _is_punct(ms[i]): i+=1; continue
        start=ms[i]['start']; end=ms[i]['end']; ids=[ms[i]['id']]; j=i+1
        while j<len(ms) and _is_punct(ms[j]) and ms[j]['start']==end:
            # group identical/repeated dash or ellipsis classes; quotes remain independent
            a=text[start:end]; b=ms[j]['surface']
            repeatable=all(c in '─—―…⋯' for c in a+b)
            if not repeatable: break
            end=ms[j]['end']; ids.append(ms[j]['id']); j+=1
        out.append({'id':f'o{len(out)}','start':start,'end':end,'surface':text[start:end],'role':'punctuation','morpheme_ids':ids,'confidence':1.0,'evidence':[{'source':'orthographic-tag','detail':'補助記号/Unicode punctuation'}]})
        i=j
    return out


def person_references(text,ms,base_entities):
    out=[]; consumed=set()
    for i,m in enumerate(ms):
        if '固有名詞-人名' not in m.get('tag',''): continue
        start=m['start']; end=m['end']; ids=[m['id']]; title=None
        if i+1<len(ms) and ms[i+1]['start']==end and (ms[i+1]['surface'] in HONORIFICS or ms[i+1].get('tag','').startswith('接尾辞-名詞的')):
            title=ms[i+1]['surface']; end=ms[i+1]['end']; ids.append(ms[i+1]['id'])
        out.append({'id':f'person{len(out)}','start':start,'end':end,'surface':text[start:end],'base_name':m['surface'],'title':title,'morpheme_ids':ids,'protected':True,'confidence':.96,'evidence':[{'source':'morphology','detail':m['tag']},{'source':'entity-composition','detail':'adjacent honorific' if title else 'person-name tag'}]})
        consumed.update(ids)
    return out


def alpha3_grammar(text,ms,predicates,existing):
    out=deepcopy(existing)
    covered={(g['start'],g['end'],g['grammar_id']) for g in out}
    def add(a,b,gid,canonical,function,conf,priority,ids):
        key=(a,b,gid)
        if key in covered:return
        out.append({'id':f'ag{len(out)}','start':a,'end':b,'surface':text[a:b],'grammar_id':gid,'canonical_form':canonical,'function':function,'host_predicate_id':None,'morpheme_ids':ids,'confidence':conf,'priority':priority,'evidence':[{'source':'alpha3-grammar-pattern','detail':canonical,'confidence':conf}]});covered.add(key)
    # longest licensed surface families first
    surfaces=[
      ('じゃありません','NEGATIVE_COPULA_POLITE','ではありません','polite-negative-copula',.98,120),
      ('ではありません','NEGATIVE_COPULA_POLITE','ではありません','polite-negative-copula',.98,120),
      ('じゃなかった','NEGATIVE_COPULA_PAST','ではなかった','past-negative-copula',.97,115),
      ('ていた','TE_IRU_PAST','Vていた','progressive-resultative-past',.96,110),
      ('でいた','DE_IRU_PAST','Vでいた','progressive-resultative-past',.96,110),
      ('ている','TE_IRU','Vている','progressive-resultative',.96,105),
      ('でいる','DE_IRU','Vでいる','progressive-resultative',.96,105),
      ('ように','YOU_NI','Vように','manner-similarity-purpose',.91,90),
      ('けれど','KEREDO','けれど','concessive-connective',.95,90),
    ]
    for surf,gid,can,fun,conf,pri in surfaces:
        p=0
        while True:
            p=text.find(surf,p)
            if p<0:break
            e=p+len(surf); ids=[m['id'] for m in ms if p<=m['start'] and m['end']<=e]
            add(p,e,gid,can,fun,conf,pri,ids);p=e
    # Remove no evidence: keep old matches, but projection will select longest/highest.
    return out


def predicate_relations(ms,preds,base_relations,grammar):
    out=deepcopy(base_relations); bym={m['id']:m for m in ms}; byp={p['head_morpheme_id']:p for p in preds}
    for r in out:
        frm=next((p for p in preds if p['id']==r['from_predicate_id']),None)
        if not frm:continue
        m=bym[frm['head_morpheme_id']]
        # Taxonomy is annotation only; the original UD evidence remains.
        if m.get('pos')=='ADJ' and next((p for p in preds if p['id']==r['to_predicate_id'] and p['headword']=='なる'),None):
            r['semantic_relation']='result-state'
        else:
            marker = r.get('marker_range') or {}
            if marker.get('surface') == 'けれど':
                r['semantic_relation'] = 'concessive'
            elif marker.get('surface') in {'て', 'で'}:
                r['semantic_relation'] = 'sequential-or-coordinate'
            else:
                g = next((g for g in grammar if g['start'] == m['end'] and g['grammar_id'] == 'YOU_NI'), None)
                r['semantic_relation'] = 'manner-similarity' if g else 'direct-subordinate'
            r['relation_evidence'] = 'alpha3-taxonomy'
            continue
        r['relation_evidence']='alpha3-taxonomy'
    return out


def lexical_proposals(text,ms,persons,grammar,orth):
    blocked_person=[(x['start'],x['end']) for x in persons]
    blocked_punct=[(x['start'],x['end']) for x in orth]
    grammar_ranges=[(g['start'],g['end']) for g in grammar]
    title_ids={mid for p in persons for mid in p['morpheme_ids'][1:]}
    out=[]
    for p in persons:
        out.append({'id':f'al{len(out)}','start':p['start'],'end':p['end'],'surface':p['surface'],'headword':p['base_name'],'lexical_type':'proper-name','morpheme_ids':p['morpheme_ids'],'confidence':p['confidence'],'evidence':[{'source':'person-reference','detail':p['id']}]})
    for m in ms:
        a,b=m['start'],m['end']
        if m['id'] in title_ids or _is_punct(m):continue
        if any(x<=a and b<=y for x,y in blocked_person):continue
        if m.get('pos') not in CONTENT_POS:continue
        if m.get('dependency') in FUNCTION_DEPS:continue
        if any(x<=a and b<=y for x,y in grammar_ranges):continue
        out.append({'id':f'al{len(out)}','start':a,'end':b,'surface':m['surface'],'headword':m['lemma'],'normalized_headword':m['normalized'],'lexical_type':'term','morpheme_ids':[m['id']],'confidence':.84,'evidence':[{'source':'alpha3-lexical-policy','detail':f"{m['pos']}/{m['dependency']}"}]})
    return out


def dictionary_candidates(ms,lexical):
    byid={m['id']:m for m in ms};out=[]
    for l in lexical:
        if l['lexical_type']!='term':continue
        m=byid[l['morpheme_ids'][0]];forms=[]
        for f in (m['surface'],m['lemma'],m['normalized']):
            if f and f not in forms:forms.append(f)
        out.append({'id':f'adc{len(out)}','start':l['start'],'end':l['end'],'surface':l['surface'],'lookup_forms':forms,'candidate_type':'alpha3-lexical-proposal','protected_boundary_safe':True,'evidence':[{'source':'alpha3-lexical-policy','detail':'content lexeme outside grammar/name/punctuation'}]})
    return out


def project(text,ms,orth,persons,grammar,lexical):
    claims=[None]*len(text);decisions=[]
    def put(a,b,role,pri,source,head=None,gid=None,conf=1):
        for i in range(a,b):
            claim={'priority':pri,'role':role,'headword':head,'grammar_id':gid,'confidence':conf,'source':source}
            if claims[i] is None or pri>claims[i]['priority']:claims[i]=claim
    for m in ms:
        if m.get('pos') in {'ADP','PART','AUX','SCONJ'}:put(m['start'],m['end'],'particle',30,'morphology')
    for l in lexical:put(l['start'],l['end'],'proper-name' if l['lexical_type']=='proper-name' else 'term',80 if l['lexical_type']=='proper-name' else 60,l['id'],l['headword'],None,l['confidence'])
    # grammar overlaps are resolved longest/highest, not by deleting other matches
    for g in sorted(grammar,key=lambda x:(x['priority'],x['end']-x['start'])):put(g['start'],g['end'],'grammar',150+g['priority'],g['id'],None,g['grammar_id'],g['confidence'])
    for o in orth:put(o['start'],o['end'],'punctuation',300,o['id'],None,None,1)
    for i in range(len(text)):
        if claims[i] is None:claims[i]={'priority':0,'role':'unresolved','headword':None,'grammar_id':None,'confidence':0,'source':'none'}
    out=[];a=0
    def same(x,y):return all(x[k]==y[k] for k in ('role','headword','grammar_id','confidence','source'))
    for i in range(1,len(text)+1):
        if i==len(text) or not same(claims[a],claims[i]):
            c=claims[a];cid=f'rd{len(decisions)}';decisions.append({'id':cid,'start':a,'end':i,'surface':text[a:i],'selected_role':c['role'],'selected_source':c['source'],'reason':'highest applicable projection priority; source annotations preserved','confidence':c['confidence']})
            out.append({'start':a,'end':i,'surface':text[a:i],'role':c['role'],'headword':c['headword'],'grammar_id':c['grammar_id'],'confidence':c['confidence'],'evidence_ids':[c['source'],cid]});a=i
    return out,decisions


def analyze_layered_alpha3(text,nlp,dictionary_evidence=None):
    base=analyze_alpha21(text,nlp,dictionary_evidence)
    result=deepcopy(base.model_dump())
    ms=deepcopy(result['morphemes']); before=_snapshot(ms)
    orth=orthography(text,ms); persons=person_references(text,ms,result['entities']); grammar=alpha3_grammar(text,ms,result['predicates'],result['grammar_matches'])
    relations=predicate_relations(ms,result['predicates'],result['predicate_relations'],grammar)
    lexical=lexical_proposals(text,ms,persons,grammar,orth); dc=dictionary_candidates(ms,lexical); colors,decisions=project(text,ms,orth,persons,grammar,lexical)
    after=_snapshot(ms)
    diagnostics=[]
    if before!=after: diagnostics.append({'severity':'error','code':'MORPHOLOGY_MUTATED','message':'A later layer changed Layer 0 morphology.'})
    if ''.join(x['surface'] for x in colors)!=text:diagnostics.append({'severity':'error','code':'ALPHA3_COLOR_INCOMPLETE','message':'Alpha 3 projection does not reconstruct text.'})
    result.update({'version':'8.0.0-alpha3','orthographic_spans':orth,'person_references':persons,'grammar_matches_alpha3':grammar,'predicate_relations_alpha3':relations,'dictionary_candidates_alpha3':dc,'lexical_items_alpha3':lexical,'reader_decisions':decisions,'color_spans_alpha3':colors,'diagnostics_alpha3':diagnostics,'layer0_snapshot':before,'alpha3_contract':{'non_destructive':True,'earlier_layers_preserved':True,'only_reader_projection_is_exclusive':True}})
    return result

````

### `JP analyzer/app/analyzer/layers/schema.py`

- Purpose: Python source.
- Size: 3909 bytes
- SHA-256: `abdcc0d625f144940a43b5bf07f878fad4a909f01d953ae04dce2c3d880fa5d0`

````python
from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    source:str; detail:str; confidence:float=1.0
class Range(BaseModel):
    start:int; end:int; surface:str
class Morpheme(Range):
    id:str; lemma:str; normalized:str; reading:str|None=None; pos:str; tag:str
    dependency:str|None=None; head_id:str|None=None; conjugation:list[str]=Field(default_factory=list)
class ParticlePhrase(Range):
    id:str; nominal_morpheme_ids:list[str]; particle_morpheme_ids:list[str]; nominal_head_id:str
    particle_surface:str; particle_type:str; evidence:list[Evidence]=Field(default_factory=list)
class BasicPhrase(Range):
    id:str; morpheme_ids:list[str]; head_id:str|None=None; phrase_type:str='basic-phrase'
    evidence:list[Evidence]=Field(default_factory=list)
class EntitySpan(Range):
    id:str; entity_type:str; entity_class:Literal['proper-name','semantic-category','temporal','other']='other'
    protected:bool=False; morpheme_ids:list[str]=Field(default_factory=list); evidence:list[Evidence]=Field(default_factory=list)
class Predicate(Range):
    id:str; head_morpheme_id:str; headword:str; morpheme_ids:list[str]; predicate_type:str='lexical'
    evidence:list[Evidence]=Field(default_factory=list)
class Argument(BaseModel):
    id:str; predicate_id:str; phrase_id:str|None=None; source_range:Range; role:str; marker:str|None=None
    inherited:bool=False; confidence:float=.7; evidence:list[Evidence]=Field(default_factory=list)
class PredicateRelation(BaseModel):
    id:str; from_predicate_id:str; to_predicate_id:str; marker_range:Range|None=None; relation:str
    confidence:float=.7; evidence:list[Evidence]=Field(default_factory=list)
class Clause(Range):
    id:str; clause_type:str; predicate_ids:list[str]; modifies_range:Range|None=None
    evidence:list[Evidence]=Field(default_factory=list)
class GrammarMatch(Range):
    id:str; grammar_id:str; canonical_form:str; function:str; host_predicate_id:str|None=None
    morpheme_ids:list[str]; confidence:float; priority:int=50; evidence:list[Evidence]=Field(default_factory=list)
class DictionaryCandidate(Range):
    id:str; lookup_forms:list[str]; candidate_type:str; protected_boundary_safe:bool=True
    evidence:list[Evidence]=Field(default_factory=list)
class DictionaryEvidence(Range):
    candidate_id:str; lookup_form:str; matched_headword:str|None=None
    match_type:Literal['exact','lemma','normalized','none']='none'; source_count:int=0; source_names:list[str]=Field(default_factory=list)
    confidence:float=0.0
class LexicalItem(Range):
    id:str; headword:str; normalized_headword:str; lexical_type:Literal['term','proper-name','expression','unknown']='term'
    morpheme_ids:list[str]; confidence:float; evidence:list[Evidence]=Field(default_factory=list)
class ColorSpan(Range):
    role:Literal['term','grammar','particle','proper-name','punctuation','unresolved']; headword:str|None=None
    grammar_id:str|None=None; confidence:float=1.0; evidence_ids:list[str]=Field(default_factory=list)
class Diagnostic(BaseModel):
    severity:Literal['info','warning','error']; code:str; message:str; start:int|None=None; end:int|None=None
class LayeredAnalysis(BaseModel):
    text:str; version:str='8.0.0-alpha2.1'; morphemes:list[Morpheme]; particle_phrases:list[ParticlePhrase]
    basic_phrases:list[BasicPhrase]; entities:list[EntitySpan]; predicates:list[Predicate]; arguments:list[Argument]
    predicate_relations:list[PredicateRelation]; clauses:list[Clause]; grammar_matches:list[GrammarMatch]
    dictionary_candidates:list[DictionaryCandidate]; dictionary_evidence:list[DictionaryEvidence]=Field(default_factory=list)
    lexical_items:list[LexicalItem]; color_spans:list[ColorSpan]; diagnostics:list[Diagnostic]
    parser_metadata:dict[str,Any]=Field(default_factory=dict)
````

### `JP analyzer/app/analyzer/layers/stabilization.py`

- Purpose: Python source.
- Size: 6084 bytes
- SHA-256: `2fb025b8b6680ac67e961605bf208f17fc3087672d6aaa047cfdfb198ad847d7`

````python
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

from .candidates import analyze_layered_alpha32, _project

# Generic families must never displace a more specific, already licensed grammar
# covering the same source range.
GENERIC_GRAMMAR_IDS = {
    "TE_IRU_CHAIN",
}
SPECIFICITY = {
    "TE_IRU_PAST": 50,
    "TE_IRU_NEGATIVE": 50,
    "TE_IRU_POLITE": 50,
    "DE_IRU_PAST": 50,
    "TE_IRU_CHAIN": 10,
}

DISCOURSE_WINDOWS = {
    ("で", "も"): ("でも", "でも"),
}
BOUNDARY_PUNCT = {"。", "！", "？", "!", "?", "、", "，", ",", "…", "……", "─", "──", "―", "――", "「", "『", "（", "("}


def _snapshot(items: list[dict[str, Any]]) -> str:
    payload = repr([
        (x.get("id"), x.get("start"), x.get("end"), x.get("surface"), x.get("lemma"), x.get("pos"), x.get("tag"))
        for x in items
    ])
    return sha256(payload.encode("utf-8")).hexdigest()


def _stabilize_grammar(grammar: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retain every annotation but make specificity explicit for projection.

    Alpha 3.2 annotations remain present and unchanged in grammar_matches_alpha32.
    This function works on a copy for the Alpha 3.2.1 projection only.
    """
    out = deepcopy(grammar)
    by_range: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for g in out:
        by_range.setdefault((g["start"], g["end"]), []).append(g)

    for same_range in by_range.values():
        best_specificity = max((SPECIFICITY.get(g.get("grammar_id"), 25) for g in same_range), default=25)
        for g in same_range:
            gid = g.get("grammar_id")
            current_specificity = SPECIFICITY.get(gid, 25)
            g["projection_specificity_alpha321"] = current_specificity
            if gid in GENERIC_GRAMMAR_IDS and current_specificity < best_specificity:
                # Lower only the copied projection priority. The original record is preserved.
                g["priority"] = min(int(g.get("priority", 0)), 70)
                g.setdefault("evidence", []).append({
                    "source": "alpha3.2.1-specificity-policy",
                    "detail": "generic grammar retained but projection yields to a more specific annotation on the same range",
                    "confidence": 1.0,
                })
    return out


def _is_clause_boundary(text: str, start: int) -> bool:
    if start == 0:
        return True
    prefix = text[:start].rstrip()
    if not prefix:
        return True
    return prefix[-1] in BOUNDARY_PUNCT


def _discourse_windows(text: str, morphemes: list[dict[str, Any]], existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add contextual multi-morpheme discourse connectives without mutating Alpha 3.2 records."""
    out = deepcopy(existing)
    seen = {(d["start"], d["end"], d["surface"]) for d in out}
    ms = sorted(morphemes, key=lambda x: (x["start"], x["end"]))

    for i in range(len(ms) - 1):
        first, second = ms[i], ms[i + 1]
        if first["end"] != second["start"]:
            continue
        key = (first["surface"], second["surface"])
        if key not in DISCOURSE_WINDOWS:
            continue
        if not _is_clause_boundary(text, first["start"]):
            continue
        surface, headword = DISCOURSE_WINDOWS[key]
        if text[first["start"]:second["end"]] != surface:
            continue
        identity = (first["start"], second["end"], surface)
        if identity in seen:
            continue
        out.append({
            "id": f"a321disc{len(out)}",
            "start": first["start"],
            "end": second["end"],
            "surface": surface,
            "role": "discourse-connective",
            "headword": headword,
            "morpheme_ids": [first["id"], second["id"]],
            "confidence": 0.96,
            "evidence": [{
                "source": "alpha3.2.1-contextual-discourse-window",
                "detail": "adjacent morphemes at sentence/clause boundary",
                "confidence": 0.96,
            }],
        })
        seen.add(identity)
    return out


def analyze_layered_alpha321(text, nlp, dictionary_evidence=None):
    base = analyze_layered_alpha32(text, nlp, dictionary_evidence)
    result = deepcopy(base)
    morphemes = deepcopy(result["morphemes"])
    before = _snapshot(morphemes)

    grammar = _stabilize_grammar(result["grammar_matches_alpha32"])
    discourse = _discourse_windows(text, morphemes, result["discourse_connectives_alpha32"])

    colors, decisions = _project(
        text,
        morphemes,
        result["orthographic_spans"],
        result["person_references"],
        grammar,
        result["lexical_items_alpha32"],
        result["numeral_expressions_alpha32"],
        discourse,
    )

    diagnostics = []
    if before != _snapshot(morphemes):
        diagnostics.append({
            "severity": "error",
            "code": "MORPHOLOGY_MUTATED",
            "message": "Alpha 3.2.1 changed Layer 0 morphology.",
        })
    if "".join(span["surface"] for span in colors) != text:
        diagnostics.append({
            "severity": "error",
            "code": "A321_COLOR_INCOMPLETE",
            "message": "Alpha 3.2.1 projection does not reconstruct source text.",
        })

    result.update({
        "version": "8.0.0-alpha3.2.1",
        "grammar_matches_alpha321": grammar,
        "discourse_connectives_alpha321": discourse,
        "reader_decisions_alpha321": decisions,
        "color_spans_alpha321": colors,
        "diagnostics_alpha321": diagnostics,
        "layer0_snapshot_alpha321": before,
        "alpha321_contract": {
            "non_destructive": True,
            "alpha32_preserved": True,
            "only_reader_projection_is_exclusive": True,
            "specific_grammar_outranks_generic_same_range": True,
        },
    })
    return result

````

### `JP analyzer/app/analyzer/layers/structure.py`

- Purpose: Python source.
- Size: 8720 bytes
- SHA-256: `86243871cfebff2f40f6e1b286d1348f2b544f41d727814570e72569c7b905ba`

````python
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

from .protected import analyze_layered_alpha3, lexical_proposals, dictionary_candidates, project

MOTION_HEADS={"行く","来る","帰る","向かう","戻る"}
LICENSED_TRAILING={"た","ない","なかっ","ます","まし","ません","ぬ"}


def _morph_snapshot(items:list[dict[str,Any]])->str:
    payload=repr([(x.get('id'),x.get('start'),x.get('end'),x.get('surface'),x.get('lemma'),x.get('pos'),x.get('tag')) for x in items])
    return sha256(payload.encode('utf-8')).hexdigest()


def _expand_inflected_grammar(text, morphemes, grammar):
    """Add larger licensed grammar ranges. Existing grammar records remain untouched."""
    out=deepcopy(grammar); seen={(g['start'],g['end'],g['grammar_id']) for g in out}
    ms=sorted(morphemes,key=lambda x:(x['start'],x['end']))
    by_start={m['start']:i for i,m in enumerate(ms)}
    for g in list(grammar):
        idx=by_start.get(g['end'])
        if idx is None: continue
        m=ms[idx]
        if m['start']!=g['end']: continue
        # Extend only grammar families that license inflectional auxiliaries.
        if g['grammar_id'] not in {'TE_SHIMAU','TE_KURERU','TE_IRU','DE_IRU'}: continue
        if m.get('lemma') not in LICENSED_TRAILING and m.get('surface') not in LICENSED_TRAILING: continue
        end=m['end']; suffix=m['surface']; gid=g['grammar_id']+'_INFLECTED'
        key=(g['start'],end,gid)
        if key in seen: continue
        out.append({
          'id':f'a31g{len(out)}','start':g['start'],'end':end,'surface':text[g['start']:end],
          'grammar_id':gid,'canonical_form':g.get('canonical_form',g['surface'])+' + '+m.get('lemma',suffix),
          'function':g.get('function','grammar')+'-inflected','host_predicate_id':g.get('host_predicate_id'),
          'morpheme_ids':list(g.get('morpheme_ids',[]))+[m['id']], 'confidence':min(0.99,g.get('confidence',0.9)+0.02),
          'priority':g.get('priority',80)+8,
          'evidence':list(g.get('evidence',[]))+[{'source':'alpha3.1-inflection-extension','detail':f'licensed trailing auxiliary {suffix}','confidence':0.96}]
        });seen.add(key)
    return out


def _dependency_aware_basic_phrase_heads(morphemes, basic_phrases):
    byid={m['id']:m for m in morphemes}; out=[]
    for bp in basic_phrases:
        x=deepcopy(bp); mids=x.get('morpheme_ids',[]); midset=set(mids)
        candidates=[byid[i] for i in mids if i in byid]
        # Prefer ROOT or token whose syntactic head exits the phrase, then non-dependent content.
        head=next((m for m in candidates if m.get('dependency')=='ROOT'),None)
        if head is None:
            head=next((m for m in candidates if m.get('head_morpheme_id') and m.get('head_morpheme_id') not in midset and m.get('pos') not in {'ADP','AUX','PART','SCONJ','PUNCT','SYM'}),None)
        if head is None:
            head=next((m for m in candidates if m.get('dependency') not in {'fixed','aux','cop'} and m.get('pos') not in {'ADP','AUX','PART','SCONJ','PUNCT','SYM'}),None)
        x['projected_head_id']=head['id'] if head else x.get('head_id')
        x['head_projection_source']='alpha3.1-dependency-aware'
        out.append(x)
    return out


def _person_aware_projections(text, person_refs, particle_phrases, clauses, arguments):
    """Add expanded semantic ranges; never alter parser-native records."""
    pps=[]; cps=[]; aps=[]
    for p in person_refs:
        for ph in particle_phrases:
            # Native phrase may start inside composed person reference and end after it.
            if p['start'] <= ph['start'] < p['end'] and ph['end']>p['end']:
                pps.append({'id':f'a31pp{len(pps)}','start':p['start'],'end':ph['end'],'surface':text[p['start']:ph['end']],
                    'nominal_head_surface':p['surface'],'person_reference_id':p['id'],'source_particle_phrase_id':ph['id'],
                    'particle':ph.get('particle_surface'),'confidence':min(p['confidence'],ph.get('confidence',0.9)),
                    'evidence':[{'source':'alpha3.1-person-range-projection','detail':'expanded native nominal range to composed person reference'}]})
        for c in clauses:
            mr=c.get('modifies_range') or {}
            if mr and p['start']<=mr.get('start',-1)<p['end']:
                y=deepcopy(c);y['id']=f'a31cl{len(cps)}';y['projected_modifies_range']={'start':p['start'],'end':p['end'],'surface':p['surface'],'person_reference_id':p['id']};y['projection_source']='alpha3.1-person-range-projection';cps.append(y)
        for a in arguments:
            ar=a.get('source_range') or {}
            if ar and p['start']<=ar.get('start',-1)<p['end']:
                y=deepcopy(a);y['id']=f'a31arg{len(aps)}';y['projected_argument_range']={'start':p['start'],'end':max(p['end'],ar.get('end',p['end'])),'surface':text[p['start']:max(p['end'],ar.get('end',p['end']))],'person_reference_id':p['id']};y['projection_source']='alpha3.1-person-range-projection';aps.append(y)
    return pps,cps,aps


def _purpose_motion_relations(text,morphemes,predicates,relations,particle_phrases):
    out=deepcopy(relations); eyebypid={p['id']:p for p in predicates}; bymid={m['id']:m for m in morphemes}
    # Correct accidental variable name support without mutation.
    bypid=eyebypid
    for r in out:
        frm=bypid.get(r.get('from_predicate_id')); to=bypid.get(r.get('to_predicate_id'))
        if not frm or not to or to.get('headword') not in MOTION_HEADS: continue
        fm=bymid.get(frm.get('head_morpheme_id'))
        if not fm: continue
        # V continuative + に + motion predicate.
        between=text[frm['end']:to['start']]
        if fm.get('pos')=='VERB' and between=='に':
            r['semantic_relation']='purpose-motion'
            r['relation_evidence']='alpha3.1-purpose-motion'
            r['construction_surface']=text[frm['start']:to['end']]
            r['purpose_predicate_head']=frm.get('headword')
            r['motion_predicate_head']=to.get('headword')
    return out


def _validate_projection(text, spans):
    issues=[]
    if ''.join(s['surface'] for s in spans)!=text: issues.append({'severity':'error','code':'A31_COLOR_INCOMPLETE','message':'Alpha 3.1 color projection does not reconstruct source text.'})
    cursor=0
    for s in spans:
        if s['start']!=cursor or text[s['start']:s['end']]!=s['surface']:
            issues.append({'severity':'error','code':'A31_COLOR_RANGE','message':f"Invalid color span {s.get('surface')!r} at {s.get('start')}:{s.get('end')}"});break
        cursor=s['end']
    if cursor!=len(text):issues.append({'severity':'error','code':'A31_COLOR_END','message':'Alpha 3.1 projection does not end at source length.'})
    return issues


def analyze_layered_alpha31(text,nlp,dictionary_evidence=None):
    base=analyze_layered_alpha3(text,nlp,dictionary_evidence)
    result=deepcopy(base)
    ms=deepcopy(result['morphemes']); before=_morph_snapshot(ms)
    grammar=_expand_inflected_grammar(text,ms,result['grammar_matches_alpha3'])
    bpheads=_dependency_aware_basic_phrase_heads(ms,result['basic_phrases'])
    pp_proj,cl_proj,arg_proj=_person_aware_projections(text,result['person_references'],result['particle_phrases'],result['clauses'],result['arguments'])
    rels=_purpose_motion_relations(text,ms,result['predicates'],result['predicate_relations_alpha3'],result['particle_phrases'])
    lexical=lexical_proposals(text,ms,result['person_references'],grammar,result['orthographic_spans'])
    dc=dictionary_candidates(ms,lexical)
    colors,decisions=project(text,ms,result['orthographic_spans'],result['person_references'],grammar,lexical)
    after=_morph_snapshot(ms)
    diagnostics=[]
    if before!=after:diagnostics.append({'severity':'error','code':'MORPHOLOGY_MUTATED','message':'A later Alpha 3.1 layer changed Layer 0 morphology.'})
    diagnostics.extend(_validate_projection(text,colors))
    result.update({
      'version':'8.0.0-alpha3.1','grammar_matches_alpha31':grammar,'basic_phrase_head_projections':bpheads,
      'particle_phrase_projections':pp_proj,'clause_target_projections':cl_proj,'argument_range_projections':arg_proj,
      'predicate_relations_alpha31':rels,'lexical_items_alpha31':lexical,'dictionary_candidates_alpha31':dc,
      'reader_decisions_alpha31':decisions,'color_spans_alpha31':colors,'diagnostics_alpha31':diagnostics,
      'layer0_snapshot_alpha31':before,'alpha31_contract':{'non_destructive':True,'alpha3_preserved':True,'only_reader_projection_is_exclusive':True}
    })
    return result

````

### `JP analyzer/app/analyzer/pipeline.py`

- Purpose: Python source.
- Size: 1704 bytes
- SHA-256: `3ccf1bfb7b4112251ec3de50fe7fa89a3ffcff9e365758aed44594324dd31712`

````python
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
````

### `JP analyzer/app/analyzer/reader_candidate_dictionary.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 7437 bytes
- SHA-256: `d519c953d3d4a49701cd7fae49176bf813f81ef891d0c03428d7f912111cf7b0`

````python
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from .layers.dictionary import evaluate_candidate

DictionaryEvaluator = Callable[[dict[str, Any], str | None], dict[str, Any]]
LEXICAL_ROLES = {"lexical", "lexical-compound", "name"}
COMPLETE_HYPOTHESIS_TYPES = {"complete-final-predicate-normalization"}
COMPONENT_HYPOTHESIS_TYPES = {"component-or-lexical-headword"}


def _parser_pos(result: dict[str, Any], candidate: dict[str, Any]) -> str | None:
    start, end = candidate.get("start"), candidate.get("end")
    covered = [
        item for item in (result.get("morphemes") or [])
        if isinstance(start, int) and isinstance(end, int)
        and start <= item.get("start", -1) and item.get("end", -1) <= end
    ]
    lexical = [
        item for item in covered
        if item.get("pos") in {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}
    ]
    return lexical[-1].get("pos") if lexical else None


def _status_from_result(result: dict[str, Any]) -> str:
    if not result.get("dictionary_ready"):
        return "dictionary-not-ready"
    return "matched" if result.get("matched") else "evaluated-no-match"


def _compact_result(result: dict[str, Any]) -> dict[str, Any]:
    """Retain evidence metadata but never expose dictionary definitions."""
    return {
        "matched": bool(result.get("matched")),
        "dictionaryReady": bool(result.get("dictionary_ready")),
        "matchType": result.get("match_type"),
        "selectedLookupForm": result.get("selected_lookup_form"),
        "selectedLookupFormType": result.get("selected_lookup_form_type"),
        "entryCount": int(result.get("entry_count") or 0),
        "independentSourceCount": int(result.get("independent_source_count") or 0),
        "dictionaryTypeCounts": dict(result.get("dictionary_type_counts") or {}),
        "matchedHeadwords": list(result.get("matched_headwords") or []),
        "sourceNames": list(result.get("source_names") or []),
        "posCompatibility": dict(result.get("pos_compatibility") or {}),
        "confidence": result.get("confidence"),
        "lookupAttempts": list(result.get("lookup_attempts") or []),
    }


def evaluate_reader_candidate_dictionary(
    result: dict[str, Any],
    candidate: dict[str, Any],
    evaluator: DictionaryEvaluator = evaluate_candidate,
) -> dict[str, Any]:
    """Evaluate every new lookup hypothesis as its own dictionary question.

    A component match never proves a complete candidate. A miss never hard-rejects
    a candidate. This function only attaches candidate-specific evidence.
    """
    output = deepcopy(candidate)
    hypotheses = list(output.get("lookupHypotheses") or [])
    parser_pos = _parser_pos(result, output)
    evaluated: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for hypothesis in hypotheses:
        item = deepcopy(hypothesis)
        text = str(item.get("text") or "").strip()
        if not text:
            item["dictionaryStatus"] = "not-generated"
            evaluated.append(item)
            continue
        request = {
            "id": f"{output.get('candidateId', 'reader-candidate')}::{item.get('type')}::{text}",
            "start": output.get("start"),
            "end": output.get("end"),
            # Surface intentionally equals the exact hypothesis. The dictionary
            # evaluator therefore cannot report a match from the inflected source
            # surface while attributing it to another hypothesis.
            "surface": text,
            "lookup_forms": [{"text": text, "type": item.get("type") or "reader-hypothesis"}],
            "lemma": None,
            "normalized": None,
            "candidate_type": output.get("candidateFamily"),
        }
        try:
            evidence = evaluator(request, parser_pos)
            item["dictionaryStatus"] = _status_from_result(evidence)
            item["dictionaryEvidence"] = _compact_result(evidence)
        except Exception as exc:  # Analysis must abstain rather than fail closed.
            item["dictionaryStatus"] = "evaluation-error"
            item["dictionaryErrorCode"] = type(exc).__name__
            errors.append({
                "hypothesisText": text,
                "hypothesisType": item.get("type"),
                "errorCode": type(exc).__name__,
            })
        evaluated.append(item)

    complete = [x for x in evaluated if x.get("type") in COMPLETE_HYPOTHESIS_TYPES]
    components = [x for x in evaluated if x.get("type") in COMPONENT_HYPOTHESIS_TYPES]
    complete_matches = [x["text"] for x in complete if x.get("dictionaryStatus") == "matched"]
    component_matches = [x["text"] for x in components if x.get("dictionaryStatus") == "matched"]
    statuses = {x.get("dictionaryStatus") for x in evaluated}

    if not evaluated:
        status = "not-generated"
    elif "evaluation-error" in statuses:
        status = "partial-or-error"
    elif statuses == {"dictionary-not-ready"}:
        status = "dictionary-not-ready"
    else:
        status = "evaluated"

    output["lookupHypotheses"] = evaluated
    output["dictionaryEvaluation"] = {
        "status": status,
        "evaluatedHypothesisCount": sum(
            x.get("dictionaryStatus") in {"matched", "evaluated-no-match"}
            for x in evaluated
        ),
        "matchedHypothesisCount": sum(x.get("dictionaryStatus") == "matched" for x in evaluated),
        "completeCandidateMatched": bool(complete_matches),
        "componentOnlyMatched": bool(component_matches) and not bool(complete_matches),
        "matchedCompleteLookupKeys": complete_matches,
        "matchedComponentKeys": component_matches,
        "dictionaryMissIsNotRejection": True,
        "errors": errors,
    }
    output.setdefault("features", {})["completeLookupKeyCorroborated"] = bool(complete_matches)
    output["features"]["candidateSpecificDictionaryEvaluated"] = bool(evaluated)
    # D.2 records evidence only. Selection and preferred identity remain unset.
    output["preferredLookupKey"] = None
    output["selected"] = False
    output["selectionReason"] = None
    return output


def evaluate_generated_reader_candidates(
    result: dict[str, Any],
    candidates: list[dict[str, Any]],
    evaluator: DictionaryEvaluator = evaluate_candidate,
) -> list[dict[str, Any]]:
    out = []
    for candidate in candidates:
        if candidate.get("candidateSource") != "reader-evidence-generator":
            out.append(candidate)
            continue
        if candidate.get("proposedRole") not in LEXICAL_ROLES:
            item = deepcopy(candidate)
            item["dictionaryEvaluation"] = {
                "status": "not-applicable",
                "evaluatedHypothesisCount": 0,
                "matchedHypothesisCount": 0,
                "completeCandidateMatched": False,
                "componentOnlyMatched": False,
                "matchedCompleteLookupKeys": [],
                "matchedComponentKeys": [],
                "dictionaryMissIsNotRejection": True,
                "errors": [],
            }
            out.append(item)
            continue
        out.append(evaluate_reader_candidate_dictionary(result, candidate, evaluator))
    return out
````

### `JP analyzer/app/analyzer/reader_candidate_evidence.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 13197 bytes
- SHA-256: `44cd8a33c3cd50ceed01fe4dea6e31fe18dd7cfecdb80dea9a310684df43f958`

````python
from __future__ import annotations

from copy import deepcopy
from typing import Any

LEXICAL_POS = {"VERB", "NOUN", "PROPN", "ADJ", "ADV", "PRON", "NUM", "INTJ", "DET", "CCONJ"}
FUNCTION_POS = {"ADP", "PART", "AUX", "SCONJ"}
NOMINAL_ARGUMENT_POS = {"NOUN", "PROPN", "PRON", "NUM", "DET"}
GENERIC_STRUCTURAL_GRAMMAR = {"V_TE", "TE_IRU_CHAIN"}
TIGHT_RELATIONS = {"compound", "direct-compound", "auxiliary", "lexical-compound"}
SEQUENTIAL_RELATION_MARKERS = {"sequential", "coordinate", "subordinate", "conj", "advcl"}


def _range(item: dict[str, Any]) -> tuple[int, int] | None:
    start, end = item.get("start"), item.get("end")
    if isinstance(start, int) and isinstance(end, int) and start < end:
        return start, end
    return None


def _overlaps(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ar, br = _range(a), _range(b)
    return bool(ar and br and ar[0] < br[1] and br[0] < ar[1])


def _contained(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if start <= x.get("start", -1) and x.get("end", -1) <= end]


def _containing(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if x.get("start", -1) <= start and end <= x.get("end", -1)]


def _crosses_boundaries(items: list[dict[str, Any]], start: int, end: int) -> bool:
    # Crossing means the candidate cuts through a phrase boundary. Merely containing
    # multiple complete phrases is recorded separately and is not a hard rejection.
    for item in items:
        a, b = item.get("start"), item.get("end")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        if start < a < end < b or a < start < b < end:
            return True
    return False


def _relation_text(relation: dict[str, Any]) -> str:
    return " ".join(
        str(relation.get(key) or "").lower()
        for key in ("relation", "semantic_relation", "dependency_type", "relation_evidence")
    )


def _candidate_predicates(result: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    start, end = candidate["start"], candidate["end"]
    return _contained(list(result.get("predicates") or []), start, end)


def _predicate_relations(result: dict[str, Any], predicate_ids: set[str]) -> list[dict[str, Any]]:
    relations = result.get("predicate_relations_alpha31") or result.get("predicate_relations") or []
    return [
        relation for relation in relations
        if relation.get("from_predicate_id") in predicate_ids
        and relation.get("to_predicate_id") in predicate_ids
    ]


def _grammar_interaction(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    grammar = (
        result.get("grammar_matches_alpha321")
        or result.get("grammar_matches_alpha32")
        or result.get("grammar_matches_alpha31")
        or []
    )
    contained = _contained(grammar, start, end)
    containing = _containing(grammar, start, end)
    partial = [x for x in grammar if _overlaps(candidate, x) and x not in contained and x not in containing]
    complete = [x for x in grammar if x.get("start") == start and x.get("end") == end]
    contained_ids = sorted({x.get("grammar_id") for x in contained if x.get("grammar_id")})
    complete_ids = sorted({x.get("grammar_id") for x in complete if x.get("grammar_id")})
    learnable_complete = [gid for gid in complete_ids if gid not in GENERIC_STRUCTURAL_GRAMMAR]
    structural = [gid for gid in contained_ids if gid in GENERIC_STRUCTURAL_GRAMMAR]
    return {
        "containedGrammarIds": contained_ids,
        "completeGrammarIds": complete_ids,
        "completeLearnableGrammarIds": learnable_complete,
        "structuralGrammarIds": structural,
        "partialOverlapGrammarIds": sorted({x.get("grammar_id") for x in partial if x.get("grammar_id")}),
        "completeLearnableGrammarConflict": bool(learnable_complete) and candidate.get("proposedRole") != "learnable-grammar",
    }


def _kwja_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    basic = list(result.get("kwja_basic_phrases_alpha1") or [])
    predicates = list(result.get("kwja_predicate_phrases_alpha1") or [])
    exact_basic = [x for x in basic if x.get("start") == start and x.get("end") == end]
    containing_basic = _containing(basic, start, end)
    contained_basic = _contained(basic, start, end)
    exact_predicate = [x for x in predicates if x.get("start") == start and x.get("end") == end]
    containing_predicate = _containing(predicates, start, end)
    contained_predicate = _contained(predicates, start, end)
    return {
        "exactBasicPhrase": bool(exact_basic),
        "containingBasicPhrase": bool(containing_basic),
        "containedBasicPhraseCount": len(contained_basic),
        "crossesBasicPhraseBoundary": _crosses_boundaries(basic, start, end),
        "exactPredicatePhrase": bool(exact_predicate),
        "containingPredicatePhrase": bool(containing_predicate),
        "containedPredicatePhraseCount": len(contained_predicate),
        "crossesPredicatePhraseBoundary": _crosses_boundaries(predicates, start, end),
        "basicPhraseIds": sorted({x.get("id") for x in exact_basic + containing_basic + contained_basic if x.get("id")}),
        "predicatePhraseIds": sorted({x.get("id") for x in exact_predicate + containing_predicate + contained_predicate if x.get("id")}),
    }


def _morphology_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    start, end = candidate["start"], candidate["end"]
    morphemes = sorted(_contained(list(result.get("morphemes") or []), start, end), key=lambda x: (x["start"], x["end"]))
    contiguous = bool(morphemes) and morphemes[0].get("start") == start and morphemes[-1].get("end") == end
    cursor = start
    for morpheme in morphemes:
        if morpheme.get("start") != cursor:
            contiguous = False
            break
        cursor = morpheme.get("end")
    contiguous = contiguous and cursor == end
    lexical = [x for x in morphemes if x.get("pos") in LEXICAL_POS]
    function = [x for x in morphemes if x.get("pos") in FUNCTION_POS]
    verbal = [x for x in morphemes if x.get("pos") == "VERB"]
    auxiliaries = [x for x in morphemes if x.get("pos") == "AUX"]
    internal_particles = [x for x in morphemes if x.get("pos") in {"ADP", "PART", "SCONJ"}]
    argument_material = [x for x in morphemes[1:-1] if x.get("pos") in NOMINAL_ARGUMENT_POS]
    return {
        "sourceRangeContiguous": contiguous,
        "allComponentsCovered": contiguous,
        "morphemeCount": len(morphemes),
        "lexicalComponentCount": len(lexical),
        "functionComponentCount": len(function),
        "verbalMorphemeCount": len(verbal),
        "auxiliaryCount": len(auxiliaries),
        "internalParticleCount": len(internal_particles),
        "interveningArgumentMaterial": bool(argument_material),
        "interveningArgumentMorphemeIds": [x.get("id") for x in argument_material if x.get("id")],
        "morphemeIds": [x.get("id") for x in morphemes if x.get("id")],
    }


def _predicate_evidence(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    predicates = _candidate_predicates(result, candidate)
    predicate_ids = {x.get("id") for x in predicates if x.get("id")}
    relations = _predicate_relations(result, predicate_ids)
    relation_texts = [_relation_text(x) for x in relations]
    tight = [x for x, value in zip(relations, relation_texts) if any(marker in value for marker in TIGHT_RELATIONS)]
    sequential = [x for x, value in zip(relations, relation_texts) if any(marker in value for marker in SEQUENTIAL_RELATION_MARKERS)]
    return {
        "predicateCount": len(predicates),
        "predicateIds": sorted(predicate_ids),
        "predicateHeadwords": [x.get("headword") for x in predicates if x.get("headword")],
        "relationIds": [x.get("id") for x in relations if x.get("id")],
        "relationLabels": [x.get("semantic_relation") or x.get("relation") for x in relations],
        "singlePredicateInterpretation": len(predicates) == 1,
        "multiplePredicateInterpretation": len(predicates) > 1,
        "tightCompoundRelationSupport": bool(tight),
        "independentOrSequentialActionConflict": bool(sequential) and len(predicates) > 1,
    }


def _competition(candidates: list[dict[str, Any]], candidate: dict[str, Any]) -> dict[str, Any]:
    same = []
    contained = []
    containing = []
    overlapping = []
    different_roles = []
    start, end = candidate["start"], candidate["end"]
    for other in candidates:
        if other.get("candidateId") == candidate.get("candidateId"):
            continue
        os, oe = other.get("start"), other.get("end")
        if not isinstance(os, int) or not isinstance(oe, int):
            continue
        if os == start and oe == end:
            same.append(other)
            if other.get("proposedRole") != candidate.get("proposedRole"):
                different_roles.append(other)
        elif start <= os and oe <= end:
            contained.append(other)
        elif os <= start and end <= oe:
            containing.append(other)
        elif start < oe and os < end:
            overlapping.append(other)
    ids = lambda items: [x.get("candidateId") for x in items if x.get("candidateId")]
    return {
        "sameRangeCandidateIds": ids(same),
        "containedCandidateIds": ids(contained),
        "containingCandidateIds": ids(containing),
        "overlappingCandidateIds": ids(overlapping),
        "differentRoleCandidateIds": ids(different_roles),
        "hasSameRangeDifferentRole": bool(different_roles),
    }


def _abstention_reasons(candidate: dict[str, Any], structural: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    morphology = structural["morphology"]
    predicates = structural["predicates"]
    grammar = structural["grammar"]
    kwja = structural["kwja"]
    competition = structural["competition"]
    dictionary = candidate.get("dictionaryEvaluation") or {}

    if not morphology["sourceRangeContiguous"]:
        reasons.append("source-range-not-contiguous")
    if morphology["interveningArgumentMaterial"]:
        reasons.append("intervening-argument-material")
    if predicates["independentOrSequentialActionConflict"]:
        reasons.append("multiple-independent-or-sequential-predicates")
    if grammar["completeLearnableGrammarConflict"]:
        reasons.append("overlaps-complete-learnable-grammar")
    if kwja["crossesBasicPhraseBoundary"] or kwja["crossesPredicatePhraseBoundary"]:
        reasons.append("crosses-kwja-phrase-boundary")
    if competition["hasSameRangeDifferentRole"]:
        reasons.append("same-range-different-role-competition")
    if candidate.get("candidateFamily") == "compound-predicate" and not dictionary.get("completeCandidateMatched"):
        reasons.append("complete-lookup-key-not-corroborated")
    if dictionary.get("status") in {"dictionary-not-ready", "partial-or-error"}:
        reasons.append("dictionary-evidence-unavailable")
    return list(dict.fromkeys(reasons))


def attach_reader_candidate_structural_evidence(
    result: dict[str, Any], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Attach candidate-specific evidence without ranking or selecting.

    Existing analyzer records are treated as immutable facts. Every conclusion in
    this module is recalculated for the exact new reader-candidate range.
    """
    output: list[dict[str, Any]] = []
    for candidate in candidates:
        item = deepcopy(candidate)
        if item.get("candidateSource") != "reader-evidence-generator":
            output.append(item)
            continue
        structural = {
            "kwja": _kwja_evidence(result, item),
            "morphology": _morphology_evidence(result, item),
            "predicates": _predicate_evidence(result, item),
            "grammar": _grammar_interaction(result, item),
            "competition": {},
        }
        item["candidateStructuralEvidence"] = structural
        output.append(item)

    # Competition requires the complete candidate set, so calculate it after all
    # immutable per-range evidence has been attached.
    for item in output:
        if item.get("candidateSource") != "reader-evidence-generator":
            continue
        structural = item["candidateStructuralEvidence"]
        structural["competition"] = _competition(output, item)
        item["abstentionReasons"] = _abstention_reasons(item, structural)
        item["rankingStatus"] = "evidence-evaluated-unselected"
        item["selected"] = False
        item["selectionReason"] = None
        item["preferredLookupKey"] = None
        item["structuralEvidenceVersion"] = "1.0"
    return output
````

### `JP analyzer/app/analyzer/reader_candidate_generation.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 18903 bytes
- SHA-256: `6630b45916b92ff67dcd8bf92d9bb2400740a261c1807565978a07dbca183482`

````python
from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

PUNCTUATION = set("、。！？!?「」『』（）()……─―～")
LEXICAL_ROLES = {"term"}
FUNCTION_ROLES = {"particle", "grammar"}
INFLECTION_GRAMMAR_IDS = {"V_TE"}
TRAILING_AUX_LEMMAS = {
    "れる", "られる", "せる", "させる", "ない", "ぬ", "た", "ます", "です",
}


def _candidate_id(family: str, start: int, end: int, role: str, keys: list[str]) -> str:
    raw = f"{family}|{start}|{end}|{role}|{'|'.join(keys)}"
    return "reader-generated-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _range_valid(text: str, start: Any, end: Any) -> bool:
    return isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text)


def _crosses_punctuation(text: str, start: int, end: int) -> bool:
    return any(char in PUNCTUATION for char in text[start:end])


def _contained(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if start <= x.get("start", -1) and x.get("end", -1) <= end]


def _lookup_hypothesis(
    text: str,
    hypothesis_type: str,
    *,
    source: str,
    source_predicate_id: str | None = None,
    source_surface: str | None = None,
    source_lemma: str | None = None,
) -> dict[str, Any] | None:
    value = str(text or "").strip()
    if not value or any(char in PUNCTUATION for char in value):
        return None
    return {
        "text": value,
        "type": hypothesis_type,
        "status": "generated",
        "dictionaryStatus": "not-evaluated",
        "generationSource": source,
        "sourcePredicateId": source_predicate_id,
        "sourceSurface": source_surface,
        "sourceLemma": source_lemma,
    }


def _dedupe_lookup_hypotheses(items: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        if not item:
            continue
        key = (item["text"], item["type"])
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _final_predicate_lookup_hypothesis(
    source_text: str,
    candidate_start: int,
    final_predicate: dict[str, Any],
) -> dict[str, Any] | None:
    pred_start = final_predicate.get("start")
    pred_end = final_predicate.get("end")
    lemma = str(final_predicate.get("headword") or "").strip()
    if not (
        isinstance(candidate_start, int)
        and isinstance(pred_start, int)
        and isinstance(pred_end, int)
        and 0 <= candidate_start <= pred_start < pred_end <= len(source_text)
        and lemma
    ):
        return None
    # Preserve the actual source prefix exactly and normalize only the final
    # predicate. No connective is inserted, no component is reordered, and no
    # earlier source character is rewritten.
    prefix = source_text[candidate_start:pred_start]
    hypothesis = prefix + lemma
    return _lookup_hypothesis(
        hypothesis,
        "complete-final-predicate-normalization",
        source="candidate-final-predicate",
        source_predicate_id=final_predicate.get("id"),
        source_surface=source_text[pred_start:pred_end],
        source_lemma=lemma,
    )


def _kwja_support(result: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    phrases = result.get("kwja_basic_phrases_alpha1") or []
    predicates = result.get("kwja_predicate_phrases_alpha1") or []
    exact_phrase_ids = [x.get("id") for x in phrases if x.get("start") == start and x.get("end") == end]
    containing_phrase_ids = [x.get("id") for x in phrases if x.get("start", 10**9) <= start and end <= x.get("end", -1)]
    exact_predicate_ids = [x.get("id") for x in predicates if x.get("start") == start and x.get("end") == end]
    containing_predicate_ids = [x.get("id") for x in predicates if x.get("start", 10**9) <= start and end <= x.get("end", -1)]
    return {
        "kwjaExactBasicPhrase": bool(exact_phrase_ids),
        "kwjaContainingBasicPhrase": bool(containing_phrase_ids),
        "kwjaExactPredicatePhrase": bool(exact_predicate_ids),
        "kwjaContainingPredicatePhrase": bool(containing_predicate_ids),
        "kwjaBasicPhraseIds": list(dict.fromkeys(x for x in exact_phrase_ids + containing_phrase_ids if x)),
        "kwjaPredicatePhraseIds": list(dict.fromkeys(x for x in exact_predicate_ids + containing_predicate_ids if x)),
    }


def _dictionary_support(result: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    candidates = result.get("resolver_candidates_alpha2") or []
    exact = [x for x in candidates if x.get("start") == start and x.get("end") == end]
    records = [x.get("dictionary_evidence") or {} for x in exact]
    return {
        "dictionaryMatched": any(x.get("matched") for x in records),
        "dictionaryIndependentSourceCount": max([int(x.get("independent_source_count") or 0) for x in records] or [0]),
        "dictionaryPosCompatible": any(x.get("pos_compatible") for x in records),
        "dictionaryEvidenceStatus": "existing-exact-range" if records else "not-evaluated-for-generated-candidate",
    }


def _record(
    result: dict[str, Any], family: str, start: int, end: int, role: str,
    lookup_keys: list[str], component_ids: list[str], evidence: list[dict[str, Any]],
    conflicts: list[dict[str, Any]], grammar_id: str | None = None,
    lookup_hypotheses: list[dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    text = result.get("text", "")
    hard: list[str] = []
    if not _range_valid(text, start, end):
        hard.append("invalid-source-range")
        surface = ""
    else:
        surface = text[start:end]
        if _crosses_punctuation(text, start, end):
            hard.append("crosses-protected-punctuation")
    features = {
        **_kwja_support(result, start, end),
        **_dictionary_support(result, start, end),
        "componentCount": len(component_ids),
        "positiveEvidenceCount": len(evidence),
        "conflictingEvidenceCount": len(conflicts),
        "hasLookupKey": bool(lookup_keys),
        "crossesPunctuation": "crosses-protected-punctuation" in hard,
    }
    return {
        "candidateId": _candidate_id(family, start, end, role, lookup_keys),
        "candidateSource": "reader-evidence-generator",
        "candidateFamily": family,
        "start": start,
        "end": end,
        "surface": surface,
        "proposedRole": role,
        "possibleLookupKeys": list(dict.fromkeys(x for x in lookup_keys if x)),
        "lookupHypotheses": _dedupe_lookup_hypotheses(
            list(lookup_hypotheses or [])
            + [
                _lookup_hypothesis(
                    key,
                    "component-or-lexical-headword",
                    source="candidate-component-headword",
                )
                for key in lookup_keys
                if key
            ]
        ),
        "preferredLookupKey": None,
        "grammarId": grammar_id,
        "componentIds": list(dict.fromkeys(x for x in component_ids if x)),
        "evidence": evidence,
        "conflictingEvidence": conflicts,
        "features": features,
        "hardRejectionReasons": hard,
        "rankingStatus": "unscored-generated-alternative",
        "selected": False,
        "selectionReason": None,
        "schemaStatus": "phase-2.2B-generated-candidate",
    }


def _from_complete_grammar(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    grammar = (
        result.get("grammar_matches_alpha321")
        or result.get("grammar_matches_alpha32")
        or result.get("grammar_matches_alpha31")
        or []
    )
    for item in grammar:
        start, end = item.get("start"), item.get("end")
        gid = item.get("grammar_id")
        if not _range_valid(result.get("text", ""), start, end) or not gid:
            continue
        if gid in INFLECTION_GRAMMAR_IDS:
            continue
        out.append(_record(
            result, "complete-grammar", start, end, "learnable-grammar", [],
            item.get("morpheme_ids") or [item.get("id")],
            [{"source": "known-grammar-id", "detail": gid, "confidence": item.get("confidence")}],
            [], grammar_id=gid,
        ))
    return out


def _from_numerals(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for item in result.get("numeral_expressions_alpha32") or []:
        start, end = item.get("start"), item.get("end")
        if not _range_valid(result.get("text", ""), start, end):
            continue
        surface = result["text"][start:end]
        candidate = _record(
            result, "term", start, end, "lexical", [surface],
            item.get("morpheme_ids") or [item.get("id")],
            [{"source": "numeral-expression", "detail": "existing numeric/counter composition; numeric structure is evidence only", "confidence": item.get("confidence")}],
            [],
        )
        candidate["features"].update({
            "containsNumeral": True,
            "numericExpressionSupported": True,
            "numericEvidenceOnly": True,
        })
        candidate["numericEvidence"] = {
            "sourceNumeralExpressionId": item.get("id"),
            "valueSurface": item.get("value_surface"),
            "counterSurface": item.get("counter_surface"),
            "morphemeIds": list(item.get("morpheme_ids") or []),
            "confidence": item.get("confidence"),
        }
        out.append(candidate)
    return out


def _from_inflected_predicates(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    text = result.get("text", "")
    resolved = result.get("resolved_spans_alpha2") or []
    morphemes = result.get("morphemes") or []
    predicates = result.get("predicates") or []
    predicate_by_range = {(x.get("start"), x.get("end")): x for x in predicates}

    for index, span in enumerate(resolved):
        if span.get("role") not in LEXICAL_ROLES or not span.get("headword"):
            continue
        start, end = span.get("start"), span.get("end")
        components = [span.get("selected_candidate_id")]
        evidence = [{"source": "lexical-headword", "detail": span.get("headword"), "confidence": span.get("confidence")}]
        conflicts = []
        cursor = end
        consumed = 0
        for following in resolved[index + 1:index + 4]:
            if following.get("start") != cursor or following.get("role") not in FUNCTION_ROLES:
                break
            covered = _contained(morphemes, following["start"], following["end"])
            grammar_id = following.get("grammar_id")
            auxiliary = any(
                x.get("pos") == "AUX" or x.get("lemma") in TRAILING_AUX_LEMMAS
                for x in covered
            )
            conjunctive = grammar_id in INFLECTION_GRAMMAR_IDS
            if not (auxiliary or conjunctive):
                break
            cursor = following["end"]
            consumed += 1
            components.append(following.get("selected_candidate_id"))
            evidence.append({
                "source": "attached-function-material",
                "detail": grammar_id or ",".join(str(x.get("lemma") or x.get("surface")) for x in covered),
                "confidence": following.get("confidence"),
            })
        if consumed:
            predicate = predicate_by_range.get((start, end))
            if predicate:
                evidence.append({"source": "predicate-record", "detail": predicate.get("id"), "confidence": 1.0})
            out.append(_record(
                result, "inflected-lexical", start, cursor, "lexical", [span.get("headword")],
                components, evidence, conflicts,
            ))
    return out


def _from_predicate_relations(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate only contiguous verbal compound alternatives.

    This function does not claim that a candidate is a word. It only preserves a
    structurally viable alternative for later evidence ranking. Ambiguous VてV
    sequences retain conflict evidence and remain unselected.
    """
    out = []
    text = result.get("text", "")
    predicates = result.get("predicates") or []
    by_id = {x.get("id"): x for x in predicates if x.get("id")}
    relations = result.get("predicate_relations_alpha31") or result.get("predicate_relations") or []
    morphemes = sorted(result.get("morphemes") or [], key=lambda x: (x.get("start", 0), x.get("end", 0)))

    def predicate_is_verbal(predicate: dict[str, Any]) -> bool:
        ids = set(predicate.get("morpheme_ids") or [])
        heads = [
            item for item in morphemes
            if item.get("id") == predicate.get("head_morpheme_id")
            or item.get("id") in ids
            or (item.get("start") == predicate.get("start") and item.get("end") == predicate.get("end"))
        ]
        return any(item.get("pos") == "VERB" for item in heads)

    for relation in relations:
        left = by_id.get(relation.get("from_predicate_id"))
        right = by_id.get(relation.get("to_predicate_id"))
        if not left or not right or not predicate_is_verbal(left) or not predicate_is_verbal(right):
            continue

        ordered = sorted([left, right], key=lambda x: (x.get("start", 0), x.get("end", 0)))
        first, second = ordered
        start, second_end = first.get("start"), second.get("end")
        if not _range_valid(text, start, second_end):
            continue

        between = [
            item for item in morphemes
            if first.get("end", -1) <= item.get("start", -1)
            and item.get("end", -1) <= second.get("start", -1)
        ]
        gap_surface = text[first.get("end", 0):second.get("start", 0)]
        marker = relation.get("marker_range") or {}
        marker_surface = marker.get("surface")

        # Contiguous lexical compounds may have no gap (読み終わる), or only a
        # visible conjunctive marker (出て行く). Arguments and modifiers block
        # a lexical-compound proposal.
        direct_compound = first.get("end") == second.get("start")
        conjunctive_compound = gap_surface in {"て", "で"} and marker_surface in {"て", "で"}
        if not (direct_compound or conjunctive_compound):
            continue
        if any(item.get("pos") in {"NOUN", "PROPN", "PRON", "NUM", "DET"} for item in between):
            continue
        if _crosses_punctuation(text, start, second_end):
            continue

        end = second_end
        trailing = [item for item in morphemes if item.get("start") == end]
        while trailing and trailing[0].get("pos") == "AUX":
            end = trailing[0]["end"]
            trailing = [item for item in morphemes if item.get("start") == end]
        if _crosses_punctuation(text, start, end):
            continue

        component_keys = list(dict.fromkeys(
            value for value in [first.get("headword"), second.get("headword")] if value
        ))
        conflicts = [{
            "source": "predicate-relation",
            "detail": relation.get("semantic_relation") or relation.get("relation") or "compound-vs-independent-predicates",
            "confidence": relation.get("confidence"),
        }]
        evidence = [{
            "source": "predicate-link",
            "detail": relation.get("id"),
            "confidence": relation.get("confidence"),
        }]
        if marker_surface:
            evidence.append({
                "source": "visible-connective",
                "detail": marker_surface,
                "confidence": relation.get("confidence"),
            })
        if direct_compound:
            evidence.append({
                "source": "contiguous-verbal-predicates",
                "detail": "no intervening source material",
                "confidence": relation.get("confidence"),
            })

        complete_hypothesis = _final_predicate_lookup_hypothesis(text, start, second)
        candidate = _record(
            result,
            "compound-predicate",
            start,
            end,
            "lexical-compound",
            component_keys,
            [first.get("id"), second.get("id"), relation.get("id")],
            evidence,
            conflicts,
            lookup_hypotheses=[complete_hypothesis],
        )
        candidate["features"]["completeLookupHypothesisGenerated"] = bool(complete_hypothesis)
        candidate["features"]["completeLookupHypothesisStatus"] = (
            "not-evaluated" if complete_hypothesis else "not-generated"
        )
        candidate["features"]["completeLookupKeyCorroborated"] = False
        candidate["features"]["containsInterveningArgumentMaterial"] = False
        candidate["features"]["verbalPredicatePair"] = True
        out.append(candidate)
    return out


def generate_reader_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    generated = []
    generated.extend(_from_complete_grammar(result))
    generated.extend(_from_numerals(result))
    generated.extend(_from_inflected_predicates(result))
    generated.extend(_from_predicate_relations(result))

    deduped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in generated:
        key = (
            item.get("start"), item.get("end"), item.get("proposedRole"),
            tuple(item.get("possibleLookupKeys") or []), item.get("grammarId"),
        )
        if key not in deduped:
            deduped[key] = item
            continue
        existing = deduped[key]
        existing["evidence"] = existing.get("evidence", []) + item.get("evidence", [])
        existing["conflictingEvidence"] = existing.get("conflictingEvidence", []) + item.get("conflictingEvidence", [])
        existing["componentIds"] = list(dict.fromkeys(existing.get("componentIds", []) + item.get("componentIds", [])))
        existing["features"]["positiveEvidenceCount"] = len(existing["evidence"])
        existing["features"]["conflictingEvidenceCount"] = len(existing["conflictingEvidence"])
    public = []
    for item in deduped.values():
        if item.get("hardRejectionReasons"):
            continue
        item["rankingEligible"] = True
        item["abstentionEligible"] = True
        item["selectionPolicy"] = "evidence-ranking-with-abstention"
        public.append(item)
    return sorted(public, key=lambda x: (x.get("start", 0), x.get("end", 0), x.get("candidateFamily", "")))
````

### `JP analyzer/app/analyzer/reader_candidate_selection.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 11580 bytes
- SHA-256: `98483a0910552cf392bcf288104afdc957b909155fc2cf9b587f46007fb92158`

````python
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .reader_projection import project_reader_spans, validate_reader_spans

POLICY_VERSION = "1.0"


def _dictionary(candidate: dict[str, Any]) -> dict[str, Any]:
    return candidate.get("dictionaryEvaluation") or {}


def _structural(candidate: dict[str, Any], key: str) -> dict[str, Any]:
    return (candidate.get("candidateStructuralEvidence") or {}).get(key) or {}


def _kwja_conflict(candidate: dict[str, Any]) -> bool:
    kwja = _structural(candidate, "kwja")
    return bool(kwja.get("crossesBasicPhraseBoundary") or kwja.get("crossesPredicatePhraseBoundary"))


def _same_range_grammar(candidate: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> bool:
    competition = _structural(candidate, "competition")
    for candidate_id in competition.get("sameRangeCandidateIds") or []:
        other = by_id.get(candidate_id) or {}
        if other.get("candidateFamily") == "complete-grammar":
            grammar = _structural(other, "grammar")
            if other.get("grammarId") in (grammar.get("completeLearnableGrammarIds") or []):
                return True
    return False


def _unique_matched_key(candidate: dict[str, Any], *, complete: bool = False) -> str | None:
    dictionary = _dictionary(candidate)
    values = (
        dictionary.get("matchedCompleteLookupKeys")
        if complete
        else dictionary.get("matchedComponentKeys")
    ) or []
    values = list(dict.fromkeys(str(x) for x in values if x))
    return values[0] if len(values) == 1 else None


def _eligible(candidate: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> tuple[bool, str | None, list[str]]:
    family = candidate.get("candidateFamily")
    morphology = _structural(candidate, "morphology")
    predicates = _structural(candidate, "predicates")
    grammar = _structural(candidate, "grammar")
    dictionary = _dictionary(candidate)
    blockers: list[str] = []

    if candidate.get("hardRejectionReasons"):
        blockers.append("hard-rejection")
    if not morphology.get("sourceRangeContiguous"):
        blockers.append("source-range-not-contiguous")
    if morphology.get("interveningArgumentMaterial"):
        blockers.append("intervening-argument-material")
    if _kwja_conflict(candidate):
        blockers.append("kwja-boundary-conflict")
    if grammar.get("completeLearnableGrammarConflict"):
        blockers.append("complete-grammar-conflict")

    if family == "complete-grammar":
        gid = candidate.get("grammarId")
        if not gid or gid not in (grammar.get("completeLearnableGrammarIds") or []):
            blockers.append("grammar-not-exactly-corroborated")
        return not blockers, None, blockers

    if _same_range_grammar(candidate, by_id):
        blockers.append("stronger-same-range-grammar")

    if family == "compound-predicate":
        key = _unique_matched_key(candidate, complete=True)
        if not dictionary.get("completeCandidateMatched") or not key:
            blockers.append("complete-compound-identity-not-corroborated")
        # A generic sequential relation is retained as conflict evidence, but does
        # not veto a complete dictionary identity when morphology and KWJA agree.
        return not blockers, key, blockers

    if family == "inflected-lexical":
        key = _unique_matched_key(candidate)
        if not predicates.get("singlePredicateInterpretation"):
            blockers.append("not-single-predicate")
        if not key:
            blockers.append("unique-lexical-identity-not-corroborated")
        return not blockers, key, blockers

    if family == "term":
        matched = [
            item.get("text") for item in (candidate.get("lookupHypotheses") or [])
            if item.get("dictionaryStatus") == "matched"
            and item.get("text") in (candidate.get("possibleLookupKeys") or [])
        ]
        matched = list(dict.fromkeys(x for x in matched if x))
        key = matched[0] if len(matched) == 1 else None
        if not key:
            blockers.append("unique-complete-term-identity-not-corroborated")
        return not blockers, key, blockers

    return False, None, ["candidate-family-not-selectable-in-policy-v1"]


def _priority(candidate: dict[str, Any]) -> tuple[int, int, int]:
    family_order = {
        "complete-grammar": 40,
        "compound-predicate": 30,
        "inflected-lexical": 20,
        "term": 10,
    }
    length = int(candidate.get("end") or 0) - int(candidate.get("start") or 0)
    dictionary = _dictionary(candidate)
    sources = 0
    for hypothesis in candidate.get("lookupHypotheses") or []:
        if hypothesis.get("dictionaryStatus") == "matched":
            sources = max(sources, int((hypothesis.get("dictionaryEvidence") or {}).get("independentSourceCount") or 0))
    return family_order.get(candidate.get("candidateFamily"), 0), length, sources


def _aligns_to_complete_spans(candidate: dict[str, Any], spans: list[dict[str, Any]]) -> bool:
    start, end = candidate.get("start"), candidate.get("end")
    overlapping = [x for x in spans if x.get("start", -1) < end and start < x.get("end", -1)]
    return bool(overlapping) and min(x["start"] for x in overlapping) == start and max(x["end"] for x in overlapping) == end


def _reader_span(candidate: dict[str, Any], lookup: str | None) -> dict[str, Any]:
    family = candidate.get("candidateFamily")
    if family == "complete-grammar":
        return {
            "start": candidate["start"], "end": candidate["end"], "surface": candidate["surface"],
            "displayRole": "learnable-grammar", "lexicalType": None,
            "colorPolicy": "grammar", "unknownColorPolicy": None,
            "knownLookupKey": None, "frequencyLookupKey": None,
            "countsForComprehension": False, "showInNewWords": False, "eligibleForMining": True,
            "headword": None, "grammarId": candidate.get("grammarId"), "confidence": 1.0,
            "sourceSpanIds": [candidate["candidateId"]], "sourceLayer": "reader-candidate-selector",
            "projectionStatus": "selected-generated-candidate",
        }
    lexical_type = "compound" if family == "compound-predicate" else "term"
    display_role = "lexical-compound" if family == "compound-predicate" else "lexical"
    return {
        "start": candidate["start"], "end": candidate["end"], "surface": candidate["surface"],
        "displayRole": display_role, "lexicalType": lexical_type,
        "colorPolicy": "known-or-frequency", "unknownColorPolicy": "frequency",
        "knownLookupKey": lookup, "frequencyLookupKey": lookup,
        "countsForComprehension": True, "showInNewWords": True, "eligibleForMining": True,
        "headword": lookup, "grammarId": None, "confidence": 1.0,
        "sourceSpanIds": [candidate["candidateId"]], "sourceLayer": "reader-candidate-selector",
        "projectionStatus": "selected-generated-candidate",
    }


def select_reader_output(result: dict[str, Any], candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Select only candidates satisfying explicit evidence gates; otherwise abstain.

    The compatibility partition is always a valid fallback. Generated candidates
    replace only complete compatibility spans, and selected ranges never overlap.
    """
    baseline = project_reader_spans(result)
    output_candidates = deepcopy(candidates)
    by_id = {x.get("candidateId"): x for x in output_candidates if x.get("candidateId")}
    proposals = []
    decisions = []

    for candidate in output_candidates:
        if candidate.get("candidateSource") != "reader-evidence-generator":
            continue
        eligible, lookup, blockers = _eligible(candidate, by_id)
        if eligible and not _aligns_to_complete_spans(candidate, baseline):
            eligible = False
            blockers.append("does-not-align-to-complete-reader-spans")
        proposals.append((candidate, lookup, eligible, blockers))

    chosen: list[tuple[dict[str, Any], str | None]] = []
    for candidate, lookup, eligible, blockers in sorted(proposals, key=lambda x: _priority(x[0]), reverse=True):
        if not eligible:
            decisions.append({
                "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
                "decision": "abstain", "reasons": blockers or list(candidate.get("abstentionReasons") or []),
            })
            continue
        if any(candidate["start"] < other["end"] and other["start"] < candidate["end"] for other, _ in chosen):
            decisions.append({
                "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
                "decision": "abstain", "reasons": ["overlaps-higher-priority-selected-candidate"],
            })
            continue
        chosen.append((candidate, lookup))
        decisions.append({
            "candidateId": candidate.get("candidateId"), "surface": candidate.get("surface"),
            "decision": "select-generated-candidate", "preferredLookupKey": lookup,
            "reasons": ["all-conservative-evidence-gates-satisfied"],
        })

    chosen_ids = {candidate["candidateId"] for candidate, _ in chosen}
    chosen_ranges = [(candidate["start"], candidate["end"]) for candidate, _ in chosen]
    for candidate in output_candidates:
        cid = candidate.get("candidateId")
        if cid in chosen_ids:
            lookup = next(value for item, value in chosen if item["candidateId"] == cid)
            candidate["selected"] = True
            candidate["preferredLookupKey"] = lookup
            candidate["rankingStatus"] = "selected-conservative-v1"
            candidate["selectionReason"] = "all conservative evidence gates satisfied"
        elif candidate.get("candidateSource") == "reader-evidence-generator":
            candidate["selected"] = False
            candidate["preferredLookupKey"] = None
            candidate["rankingStatus"] = "abstained-conservative-v1"
            candidate["selectionReason"] = None
        elif candidate.get("selected") and any(candidate["start"] < b and a < candidate["end"] for a, b in chosen_ranges):
            candidate["selected"] = False
            candidate["rankingStatus"] = "displaced-by-selected-reader-candidate"
            candidate["selectionReason"] = None

    selected_spans = {candidate["start"]: _reader_span(candidate, lookup) for candidate, lookup in chosen}
    final = []
    index = 0
    while index < len(baseline):
        span = baseline[index]
        replacement = selected_spans.get(span["start"])
        if replacement:
            final.append(replacement)
            end = replacement["end"]
            while index < len(baseline) and baseline[index]["end"] <= end:
                index += 1
            continue
        final.append(span)
        index += 1

    validate_reader_spans(result.get("text", ""), final)
    selection = {
        "policyVersion": POLICY_VERSION,
        "mode": "conservative-evidence-gates-with-abstention",
        "compatibilityFallbackAvailable": True,
        "selectedGeneratedCandidateIds": sorted(chosen_ids),
        "selectedGeneratedCandidateCount": len(chosen_ids),
        "decisions": decisions,
    }
    return final, output_candidates, selection
````

### `JP analyzer/app/analyzer/reader_candidates.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 3455 bytes
- SHA-256: `7fe41090a7a20b2039347a8e78293a5c20b0659eee45cc98801f81c1c279b8c1`

````python
from __future__ import annotations
from typing import Any

from .reader_candidate_generation import generate_reader_candidates
from .reader_candidate_dictionary import evaluate_generated_reader_candidates
from .reader_candidate_evidence import attach_reader_candidate_structural_evidence

READER_CANDIDATE_SCHEMA_VERSION = "2.0"


def _existing_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    selected = {
        str(item.get("selected_candidate_id"))
        for item in (result.get("resolved_spans_alpha2") or [])
        if item.get("selected_candidate_id")
    }
    out: list[dict[str, Any]] = []
    for item in result.get("resolver_candidates_alpha2") or []:
        candidate_id = str(item.get("candidate_id") or "")
        start, end = item.get("start"), item.get("end")
        if not candidate_id or not isinstance(start, int) or not isinstance(end, int):
            continue
        text = result.get("text", "")
        hard = []
        if not (0 <= start < end <= len(text)):
            hard.append("invalid-source-range")
        elif item.get("surface") != text[start:end]:
            hard.append("surface-range-mismatch")
        dictionary = item.get("dictionary_evidence") or {}
        out.append({
            "candidateId": candidate_id,
            "candidateSource": "existing-resolver",
            "start": start,
            "end": end,
            "surface": item.get("surface", ""),
            "proposedRole": item.get("proposed_role"),
            "candidateFamily": item.get("candidate_family"),
            "possibleLookupKeys": list(dict.fromkeys(x for x in [item.get("headword"), item.get("surface")] if x)),
            "preferredLookupKey": item.get("headword"),
            "grammarId": item.get("grammar_id"),
            "componentIds": item.get("morpheme_ids") or [],
            "evidence": item.get("evidence") or [],
            "conflictingEvidence": [],
            "features": {
                "dictionaryMatched": bool(dictionary.get("matched")),
                "dictionaryIndependentSourceCount": int(dictionary.get("independent_source_count") or 0),
                "dictionaryPosCompatible": bool(dictionary.get("pos_compatible")),
                "protected": bool(item.get("protected")),
                "sourceLayer": item.get("source_layer"),
                "utilityDimensions": list(item.get("utility_dimensions") or []),
                "utilityScore": item.get("utility_score"),
                "confidence": item.get("confidence"),
            },
            "hardRejectionReasons": hard,
            "rankingStatus": "existing-resolver-selection" if candidate_id in selected else "existing-resolver-alternative",
            "selected": candidate_id in selected,
            "selectionReason": "selected by existing analyzer resolver" if candidate_id in selected else None,
            "schemaStatus": "phase-2.2A-existing-candidate",
        })
    return out


def project_reader_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Expose existing and generated alternatives without changing readerSpans."""
    existing = _existing_candidates(result)
    generated = generate_reader_candidates(result)
    evaluated = evaluate_generated_reader_candidates(result, generated)
    combined = existing + evaluated
    return attach_reader_candidate_structural_evidence(result, combined)
````

### `JP analyzer/app/analyzer/reader_corrections.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 18190 bytes
- SHA-256: `15fc3b76bba63c6af232b0bbb956aa3ee5703dcc4c312af5ddb6abc2dc50b406`

````python
from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "reader_corrections.sqlite3"
_lock = threading.RLock()
_ALLOWED_ROLES = {
    "lexical",
    "lexical-compound",
    "name",
    "learnable-grammar",
    "function",
    "punctuation",
    "unresolved",
}
_ALLOWED_ACTIONS = {
    "show-as-one-unit",
    "mark-unresolved",
    # Reserved structural actions for the later frontend.
    "split",
    "mark-vocabulary",
    "mark-grammar",
    "mark-function",
    "mark-name",
}
_PUNCTUATION = set("、。！？!?「」『』（）()……─―～")

SCHEMA = """
CREATE TABLE IF NOT EXISTS reader_corrections(
 correction_id TEXT PRIMARY KEY, sentence_text TEXT NOT NULL, sentence_fingerprint TEXT NOT NULL,
 start INTEGER NOT NULL, end INTEGER NOT NULL, surface TEXT NOT NULL, action TEXT NOT NULL,
 display_role TEXT NOT NULL, headword TEXT, known_lookup_key TEXT, frequency_lookup_key TEXT,
 grammar_id TEXT, unknown_color_policy TEXT, scope TEXT NOT NULL,
 analyzer_version TEXT NOT NULL, reader_span_schema_version TEXT NOT NULL,
 original_spans_json TEXT NOT NULL, feature_snapshot_json TEXT NOT NULL,
 created_at TEXT NOT NULL, deactivated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_reader_corrections_occurrence
 ON reader_corrections(sentence_fingerprint,start,end,deactivated_at);
"""


def sentence_fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@contextmanager
def _db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    try:
        with con:
            yield con
    finally:
        con.close()


def _aligned_overlaps(
    text: str,
    start: int,
    end: int,
    baseline: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not baseline:
        raise ValueError("baselineReaderSpans is required")
    overlaps = [
        item for item in baseline
        if item.get("start", -1) < end and start < item.get("end", -1)
    ]
    if (
        not overlaps
        or min(item["start"] for item in overlaps) != start
        or max(item["end"] for item in overlaps) != end
    ):
        raise ValueError("Correction range must align to complete existing reader spans")
    if "".join(item.get("surface", "") for item in overlaps) != text[start:end]:
        raise ValueError("Correction range does not reconstruct selected source")
    return overlaps


def _unique(values: list[Any]) -> list[str]:
    return list(dict.fromkeys(str(value) for value in values if value))


def _candidate_snapshot(
    start: int,
    end: int,
    reader_candidates: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    candidates = []
    for candidate in reader_candidates or []:
        if candidate.get("start", -1) < end and start < candidate.get("end", -1):
            candidates.append({
                "candidateId": candidate.get("candidateId"),
                "start": candidate.get("start"),
                "end": candidate.get("end"),
                "surface": candidate.get("surface"),
                "candidateFamily": candidate.get("candidateFamily"),
                "proposedRole": candidate.get("proposedRole"),
                "grammarId": candidate.get("grammarId"),
                "possibleLookupKeys": candidate.get("possibleLookupKeys") or [],
                "selected": candidate.get("selected"),
                "rankingStatus": candidate.get("rankingStatus"),
                "selectionReason": candidate.get("selectionReason"),
                "abstentionReasons": candidate.get("abstentionReasons") or [],
                "dictionaryEvaluation": candidate.get("dictionaryEvaluation") or {},
                "candidateStructuralEvidence": candidate.get("candidateStructuralEvidence") or {},
            })
    return {"overlappingReaderCandidates": candidates}


def derive_structural_correction(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate user structural intent and derive identities from analyzer output.

    The user supplies boundaries/action and may supply a broad role. Dictionary keys,
    headwords, grammar IDs, and grammar-focus ranges are analyzer-derived only.
    """
    text = str(data.get("sentence") or "")
    start, end = data.get("start"), data.get("end")
    surface = str(data.get("surface") or "")
    scope = str(data.get("scope") or "occurrence")
    action = str(data.get("action") or "show-as-one-unit")
    requested_role = data.get("displayRole")

    if scope != "occurrence":
        raise ValueError("Structural teaching currently supports occurrence scope only")
    if action not in _ALLOWED_ACTIONS:
        raise ValueError("Unknown structural correction action")
    if action == "split":
        raise ValueError("Split teaching is reserved for the frontend phase")
    if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= len(text)):
        raise ValueError("Invalid correction range")
    if text[start:end] != surface:
        raise ValueError("Correction surface does not match sentence range")
    if any(ch in _PUNCTUATION for ch in surface):
        raise ValueError("Correction cannot cross or include protected punctuation")

    overlaps = _aligned_overlaps(text, start, end, baseline)
    grammar_ids = _unique([item.get("grammarId") for item in overlaps])
    lexical_keys = _unique([
        item.get("knownLookupKey") or item.get("headword")
        for item in overlaps
        if item.get("displayRole") in {"lexical", "lexical-compound"}
    ])
    grammar_focus_ranges = [
        {
            "start": item["start"],
            "end": item["end"],
            "surface": item.get("surface", ""),
            "grammarId": item.get("grammarId"),
        }
        for item in overlaps
        if item.get("displayRole") == "learnable-grammar"
    ]

    if action == "mark-unresolved":
        role = "unresolved"
    elif requested_role:
        role = str(requested_role)
    elif grammar_ids:
        role = "learnable-grammar"
    elif any(item.get("displayRole") == "lexical-compound" for item in overlaps):
        role = "lexical-compound"
    elif lexical_keys:
        role = "lexical"
    else:
        role = "unresolved"

    if role not in _ALLOWED_ROLES:
        raise ValueError("Unknown displayRole")

    grammar_id = grammar_ids[0] if len(grammar_ids) == 1 else None
    host_lookup_key = lexical_keys[0] if len(lexical_keys) == 1 else None
    lookup = host_lookup_key if role in {"lexical", "lexical-compound"} else None

    # A taught lexical unit without a defensible analyzer identity remains neutral.
    if role in {"lexical", "lexical-compound"} and not lookup:
        role = "unresolved"
    # A grammar correction may be structurally taught without a known catalog ID,
    # but when the analyzer has one, it is preserved as evidence.

    snapshot = dict(data.get("featureSnapshot") or {})
    snapshot.update({
        "teachingContractVersion": "1.0",
        "userSuppliedLookupKeys": False,
        "originalPartition": [
            {
                "start": item.get("start"),
                "end": item.get("end"),
                "surface": item.get("surface"),
                "displayRole": item.get("displayRole"),
                "grammarId": item.get("grammarId"),
                "knownLookupKey": item.get("knownLookupKey"),
                "projectionStatus": item.get("projectionStatus"),
            }
            for item in overlaps
        ],
        "derivedEvidence": {
            "grammarIds": grammar_ids,
            "hostLookupKeys": lexical_keys,
            "grammarFocusRanges": grammar_focus_ranges,
        },
        "readerSelection": reader_selection or {},
        **_candidate_snapshot(start, end, reader_candidates),
    })

    return {
        "sentence": text,
        "start": start,
        "end": end,
        "surface": surface,
        "scope": "occurrence",
        "action": action,
        "displayRole": role,
        "headword": lookup,
        "knownLookupKey": lookup,
        "frequencyLookupKey": lookup,
        "grammarId": grammar_id,
        "hostLookupKey": host_lookup_key,
        "grammarFocusRanges": grammar_focus_ranges,
        "unknownColorPolicy": "frequency" if role in {"lexical", "lexical-compound"} else None,
        "featureSnapshot": snapshot,
    }


def corrected_span(data: dict[str, Any], correction_id: str | None = None) -> dict[str, Any]:
    role = data["displayRole"]
    color = {
        "lexical": "known-or-frequency",
        "lexical-compound": "known-or-frequency",
        "name": "name",
        "learnable-grammar": "grammar",
        "function": "muted",
        "punctuation": "neutral",
        "unresolved": "neutral",
    }[role]
    return {
        "start": data["start"],
        "end": data["end"],
        "surface": data["surface"],
        "displayRole": role,
        "lexicalType": "compound" if role == "lexical-compound" else "term" if role == "lexical" else None,
        "colorPolicy": color,
        "unknownColorPolicy": data.get("unknownColorPolicy"),
        "knownLookupKey": data.get("knownLookupKey"),
        "frequencyLookupKey": data.get("frequencyLookupKey"),
        "headword": data.get("headword"),
        "grammarId": data.get("grammarId"),
        "hostLookupKey": data.get("hostLookupKey"),
        "grammarFocusRanges": data.get("grammarFocusRanges") or [],
        "confidence": 1.0,
        "countsForComprehension": role in {"lexical", "lexical-compound"},
        "showInNewWords": role in {"lexical", "lexical-compound"},
        "eligibleForMining": role in {"lexical", "lexical-compound", "name", "learnable-grammar"},
        "sourceSpanIds": [],
        "sourceLayer": "user-correction",
        "projectionStatus": "user-corrected-preview" if not correction_id else "user-corrected",
        "correctionId": correction_id,
        "correctionScope": "occurrence",
        "correctionAction": data.get("action"),
    }


def _replace_range(
    text: str,
    baseline: list[dict[str, Any]],
    data: dict[str, Any],
    correction_id: str | None,
) -> list[dict[str, Any]]:
    start, end = data["start"], data["end"]
    _aligned_overlaps(text, start, end, baseline)
    left = [item for item in baseline if item["end"] <= start]
    right = [item for item in baseline if item["start"] >= end]
    spans = left + [corrected_span(data, correction_id)] + right
    from .reader_projection import validate_reader_spans
    validate_reader_spans(text, spans)
    return spans


def preview(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    derived = derive_structural_correction(
        data,
        baseline,
        reader_candidates=reader_candidates,
        reader_selection=reader_selection,
    )
    spans = _replace_range(derived["sentence"], baseline, derived, None)
    return {
        "sentenceFingerprint": sentence_fingerprint(derived["sentence"]),
        "originalReaderSpans": baseline,
        "previewReaderSpans": spans,
        "derivedCorrection": derived,
        "saved": False,
    }


def save(
    data: dict[str, Any],
    baseline: list[dict[str, Any]],
    analyzer_version: str,
    schema_version: str,
    *,
    reader_candidates: list[dict[str, Any]] | None = None,
    reader_selection: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = preview(
        data,
        baseline,
        reader_candidates=reader_candidates,
        reader_selection=reader_selection,
    )
    derived = result["derivedCorrection"]
    correction_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        con.execute(
            "INSERT INTO reader_corrections VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL)",
            (
                correction_id,
                derived["sentence"],
                sentence_fingerprint(derived["sentence"]),
                derived["start"],
                derived["end"],
                derived["surface"],
                derived["action"],
                derived["displayRole"],
                derived.get("headword"),
                derived.get("knownLookupKey"),
                derived.get("frequencyLookupKey"),
                derived.get("grammarId"),
                derived.get("unknownColorPolicy"),
                "occurrence",
                analyzer_version,
                schema_version,
                json.dumps(baseline, ensure_ascii=False),
                json.dumps(derived.get("featureSnapshot") or {}, ensure_ascii=False),
                now,
            ),
        )
    result["saved"] = True
    result["correctionId"] = correction_id
    result["previewReaderSpans"] = _replace_range(
        derived["sentence"], baseline, derived, correction_id
    )
    return result


def list_corrections(include_inactive: bool = False) -> list[dict[str, Any]]:
    with _lock, _db() as con:
        rows = con.execute(
            "SELECT * FROM reader_corrections"
            + ("" if include_inactive else " WHERE deactivated_at IS NULL")
            + " ORDER BY created_at"
        ).fetchall()
    return [dict(item) for item in rows]


def _row_to_derived(row: dict[str, Any]) -> dict[str, Any]:
    snapshot = json.loads(row.get("feature_snapshot_json") or "{}")
    evidence = snapshot.get("derivedEvidence") or {}
    host_keys = evidence.get("hostLookupKeys") or []
    return {
        "sentence": row["sentence_text"],
        "start": row["start"],
        "end": row["end"],
        "surface": row["surface"],
        "scope": row["scope"],
        "action": row["action"],
        "displayRole": row["display_role"],
        "headword": row.get("headword"),
        "knownLookupKey": row.get("known_lookup_key"),
        "frequencyLookupKey": row.get("frequency_lookup_key"),
        "grammarId": row.get("grammar_id"),
        "hostLookupKey": host_keys[0] if len(host_keys) == 1 else None,
        "grammarFocusRanges": evidence.get("grammarFocusRanges") or [],
        "unknownColorPolicy": row.get("unknown_color_policy"),
        "featureSnapshot": snapshot,
    }



def correction_revision() -> str:
    """Return a deterministic revision for the active correction set.

    The revision changes when an active correction is added, replaced, or
    deactivated. It is independent of SQLite row order and database timestamps
    that do not affect reader output.
    """
    import hashlib
    import json

    active = []
    for record in list_corrections(include_inactive=False):
        active.append({
            "correctionId": record.get("correctionId"),
            "sentenceFingerprint": record.get("sentenceFingerprint"),
            "start": record.get("start"),
            "end": record.get("end"),
            "surface": record.get("surface"),
            "action": record.get("action"),
            "displayRole": record.get("displayRole"),
            "scope": record.get("scope"),
            "replacementReaderSpans": record.get("replacementReaderSpans") or [],
        })
    active.sort(key=lambda item: str(item.get("correctionId") or ""))
    payload = json.dumps(active, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def apply_active_corrections(
    text: str,
    baseline: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply active exact-occurrence corrections after normal reader selection."""
    fingerprint = sentence_fingerprint(text)
    with _lock, _db() as con:
        rows = con.execute(
            "SELECT * FROM reader_corrections "
            "WHERE sentence_fingerprint=? AND deactivated_at IS NULL "
            "ORDER BY created_at",
            (fingerprint,),
        ).fetchall()
    spans = list(baseline)
    applied: list[dict[str, Any]] = []
    for sqlite_row in rows:
        row = dict(sqlite_row)
        if row["sentence_text"] != text:
            continue
        derived = _row_to_derived(row)
        try:
            spans = _replace_range(text, spans, derived, row["correction_id"])
        except ValueError:
            # Stale corrections never corrupt output; they remain in audit history.
            continue
        applied.append({
            "correctionId": row["correction_id"],
            "action": row["action"],
            "start": row["start"],
            "end": row["end"],
            "surface": row["surface"],
            "displayRole": row["display_role"],
            "scope": row["scope"],
        })
    return spans, applied


def deactivate(correction_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _db() as con:
        cursor = con.execute(
            "UPDATE reader_corrections SET deactivated_at=? "
            "WHERE correction_id=? AND deactivated_at IS NULL",
            (now, correction_id),
        )
    if cursor.rowcount != 1:
        raise ValueError("Active correction not found")
    return {"correctionId": correction_id, "active": False, "deactivatedAt": now}
````

### `JP analyzer/app/analyzer/reader_corrections_api.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 2738 bytes
- SHA-256: `035395754bd62e79e3ecddb8a1c1018a479e9441399483b83764e52f635b3383`

````python
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from .reader_corrections import deactivate, list_corrections, preview, save
from .reader_projection import READER_SPAN_SCHEMA_VERSION
from .version import ANALYZER_VERSION

router = APIRouter(prefix="/reader-corrections", tags=["reader-corrections"])


class CorrectionRequest(BaseModel):
    sentence: str
    start: int
    end: int
    surface: str
    action: str = "show-as-one-unit"
    displayRole: str | None = None
    scope: str = "occurrence"
    baselineReaderSpans: list[dict[str, Any]] = Field(default_factory=list)
    readerCandidates: list[dict[str, Any]] = Field(default_factory=list)
    readerSelection: dict[str, Any] = Field(default_factory=dict)


def _data(req: CorrectionRequest):
    payload = req.model_dump()
    baseline = payload.pop("baselineReaderSpans")
    candidates = payload.pop("readerCandidates")
    selection = payload.pop("readerSelection")
    if not baseline:
        # The future frontend may omit debug evidence; derive the current analyzer
        # output server-side while keeping all linguistic logic in JP Analyzer.
        from .pipeline import analyze
        current = analyze(req.sentence)
        baseline = current.get("readerSpans") or []
        candidates = current.get("readerCandidates") or []
        selection = current.get("readerSelection") or {}
    return payload, baseline, candidates, selection


@router.post("/preview")
def preview_endpoint(req: CorrectionRequest):
    try:
        data, baseline, candidates, selection = _data(req)
        return preview(
            data,
            baseline,
            reader_candidates=candidates,
            reader_selection=selection,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.post("")
def save_endpoint(req: CorrectionRequest):
    try:
        data, baseline, candidates, selection = _data(req)
        return save(
            data,
            baseline,
            ANALYZER_VERSION,
            READER_SPAN_SCHEMA_VERSION,
            reader_candidates=candidates,
            reader_selection=selection,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc))


@router.get("")
def list_endpoint(includeInactive: bool = Query(False)):
    return {"corrections": list_corrections(includeInactive)}


@router.delete("/{correction_id}")
def deactivate_endpoint(correction_id: str):
    try:
        return deactivate(correction_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc))
````

### `JP analyzer/app/analyzer/reader_projection.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 6987 bytes
- SHA-256: `89983e8a64df9e10599036e05178ab3652798766cbaef0b7ff7dbbeaf2a663ba`

````python
from __future__ import annotations

from typing import Any

READER_SPAN_SCHEMA_VERSION = "1.1"

FUNCTION_GRAMMAR_IDS = {
    "V_TE",
}

DISPLAY_ROLES = {
    "lexical",
    "lexical-compound",
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
            "displayRole": "lexical",
            "lexicalType": "term",
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
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
        if role in {"lexical", "lexical-compound",}:
            if not span.get("knownLookupKey") or not span.get("frequencyLookupKey"):
                raise ValueError(
                    f"readerSpans[{index}] lexical span is missing lookup keys"
                )
        cursor = end

    if cursor != len(text):
        raise ValueError(
            f"readerSpans coverage ends at {cursor}; source length is {len(text)}"
        )
````

### `JP analyzer/app/analyzer/runtime.py`

- Purpose: Python source.
- Size: 1540 bytes
- SHA-256: `3244da7fb42e4b421f759d2d273ebc3c9aa35d7e1ba264bd6478416e45217f12`

````python
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
````

### `JP analyzer/app/analyzer/semantic_snapshot.py`

- Purpose: Python source.
- Size: 1638 bytes
- SHA-256: `c805d66ee21816a1e84beb220bef86b28960e89c2af3a8eeef5fa78fc55a8028`

````python
from __future__ import annotations
import hashlib, json

def _span(item):
    return {"start":item.get("start"), "end":item.get("end"), "surface":item.get("surface"), "role":item.get("role"), "headword":item.get("headword"), "grammarId":item.get("grammar_id"), "confidence":item.get("confidence"), "sourceLayer":item.get("source_layer")}

def semantic_snapshot(result):
    text = result.get("text", "")
    resolved = result.get("resolved_spans_alpha2") or []
    dictionary = result.get("dictionary_evidence_alpha34") or {}
    metadata = result.get("kwja_metadata_alpha1") or {}
    diagnostics = result.get("diagnostics_alpha2") or []
    return {"contractVersion":"1.0", "textSha256":hashlib.sha256(text.encode("utf-8")).hexdigest(), "textLength":len(text), "resolvedSpans":[_span(x) for x in resolved], "unresolvedSpans":[_span(x) for x in resolved if x.get("role") == "unresolved"], "diagnostics":[{"severity":x.get("severity"), "code":x.get("code"), "start":x.get("start"), "end":x.get("end")} for x in diagnostics], "kwjaAlignmentComplete":bool(metadata.get("source_alignment_complete")), "dictionarySummary":{"ready":dictionary.get("dictionary_ready"), "candidateCount":dictionary.get("candidate_count"), "matchedCandidateCount":dictionary.get("matched_candidate_count"), "unmatchedCandidateCount":dictionary.get("unmatched_candidate_count"), "typeEvidenceCounts":dictionary.get("dictionary_type_evidence_counts") or {}}}

def snapshot_digest(snapshot):
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
````

### `JP analyzer/app/analyzer/service.py`

- Purpose: Python source.
- Size: 1167 bytes
- SHA-256: `163f92a16fca98727046da6f843ad81552c1339bf524bfa6273dd120fa12cb4a`

````python
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .layers.dictionary_api import router as dictionary_sync_router
from .layers.dictionary_evidence_api import router as dictionary_evidence_router
from .reader_corrections_api import router as reader_corrections_router

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
app.include_router(reader_corrections_router)


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
````

### `JP analyzer/app/analyzer/services.py`

- Purpose: Python source.
- Size: 394 bytes
- SHA-256: `85ef48e63be3f8747820e04978e83dd124685d1540aa80b353df185f3b0e40a7`

````python
from dataclasses import dataclass

from .adapters import DictionaryAdapter, KwjaAdapter
from .config import AnalyzerConfig


@dataclass(frozen=True)
class AnalyzerServices:
    kwja: KwjaAdapter
    dictionary: DictionaryAdapter

    @classmethod
    def from_config(cls, config: AnalyzerConfig) -> "AnalyzerServices":
        return cls(KwjaAdapter(config), DictionaryAdapter())
````

### `JP analyzer/app/analyzer/source_contract.py`

- Purpose: Python source.
- Size: 1445 bytes
- SHA-256: `aaa8493a6adb2d8d9dc5eff7ef6f0e941b0c96d73e59a73684f2b7feddd6eeb1`

````python
from __future__ import annotations

def validate_ranges(text, spans, *, require_partition):
    diagnostics = []
    cursor = 0
    for index, span in enumerate(sorted(spans, key=lambda x: (x.get("start", -1), x.get("end", -1)))):
        start, end = span.get("start"), span.get("end")
        if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= len(text)):
            diagnostics.append({"severity":"error", "code":"SOURCE_RANGE_INVALID", "index":index})
            continue
        if span.get("surface") != text[start:end]:
            diagnostics.append({"severity":"error", "code":"SOURCE_SURFACE_MISMATCH", "index":index})
        if require_partition and start != cursor:
            diagnostics.append({"severity":"error", "code":"SOURCE_PARTITION_GAP_OR_OVERLAP", "index":index, "expected":cursor, "actual":start})
        if require_partition:
            cursor = end
    if require_partition and cursor != len(text):
        diagnostics.append({"severity":"error", "code":"SOURCE_PARTITION_INCOMPLETE", "expected":len(text), "actual":cursor})
    return diagnostics

def validate_analysis_source(result):
    text = result.get("text", "")
    diagnostics = validate_ranges(text, result.get("resolved_spans_alpha2") or [], require_partition=True)
    diagnostics.extend(validate_ranges(text, result.get("morphemes") or [], require_partition=False))
    return diagnostics
````

### `JP analyzer/app/analyzer/version.py`

- Purpose: Python source.
- Size: 153 bytes
- SHA-256: `2ace8b20208561b754ad9b242a47c76a8108428e7da9f626ccd2dce8ee95f445`

````python
ANALYZER_VERSION = "11.9.0-correction-aware-cache-contract"
SCHEMA_VERSION = "1.2"
ENGINE_CONTRACT_VERSION = "9.0.0-alpha2.2-evidence-gated-decision"
````

### `JP analyzer/CONSOLIDATED_ANALYZER.md`

- Purpose: Documentation.
- Size: 979 bytes
- SHA-256: `2e5122570b09ed1bac9744d9237aa981b18e2b70af77381cf6253a6eef092312`

````markdown
# Consolidated JP Analyzer

The supported production implementation is `app.analyzer.analyze`. The analyzer owns morphology, protected ranges, structure, candidates, dictionary evidence, KWJA evidence, evidence gating, the final decision, diagnostics, and compact/full output.

Historical Phase 8, Phase 9, and Phase 10 wrapper implementations were removed after exact semantic parity on 200 development and 200 fresh unseen sentences. Existing phase-named debug fields remain temporarily for response-schema compatibility; they are not separate runtime implementations.

## Run tests

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\run_tests.ps1
```

## Run frozen snapshot regression

```powershell
& .\.venv\Scripts\python.exe .\run_snapshot_regression.py .\tests\corpora\development\random_sentences.txt --reference .\consolidation_dev_reference_200.json --output .\post_cleanup_dev_actual.json --report .\post_cleanup_dev_report.json
```

````

### `JP analyzer/direct_analyzer_timing.py`

- Purpose: Python source.
- Size: 1405 bytes
- SHA-256: `149fcb9290d5175cbd4c76ac4468caf1bca4ebd705557e0a80f7eae9965aa75c`

````python
import json
import statistics
import time
import urllib.request

sentences = [
    "彼は静かに頷いて答えた。",
    "二人は部屋から出て行った。",
    "本を読んで寝た。",
    "窓を開けて空気を入れた。",
    "少年が走ってきた。",
]

times = []

for index, text in enumerate(sentences, start=1):
    request = urllib.request.Request(
        "http://127.0.0.1:8766/analyze",
        data=json.dumps(
            {"text": text},
            ensure_ascii=False,
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        },
        method="POST",
    )

    started = time.perf_counter()

    with urllib.request.urlopen(
        request,
        timeout=300,
    ) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    elapsed = time.perf_counter() - started
    times.append(elapsed)

    partition = " | ".join(
        span.get("surface", "")
        for span in result.get("readerSpans", [])
    )

    print(
        f"{index}. {elapsed:.2f}s | "
        f"{result.get('analyzerVersion')} | "
        f"{partition}"
    )

print()
print(f"minimum: {min(times):.2f}s")
print(f"maximum: {max(times):.2f}s")
print(f"mean: {statistics.mean(times):.2f}s")
print(f"median: {statistics.median(times):.2f}s")
````

### `JP analyzer/docs/KWJA_SETUP_WINDOWS.md`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 1009 bytes
- SHA-256: `4f1afa87db391b26bd6f5e88ba8a0a834421889831fcfdb40bcbd8bf93c1cac9`

````markdown
# KWJA setup on Windows

KWJA is an internal JP Analyzer layer. Its Python 3.11 environment is isolated in `.kwja-venv`; it is not a separate application or repository.

## Install or refresh models online

```powershell
$env:HF_HUB_OFFLINE = "0"
$env:TRANSFORMERS_OFFLINE = "0"
$env:HF_DATASETS_OFFLINE = "0"
powershell.exe -ExecutionPolicy Bypass -File .\scripts\setup_kwja_windows.ps1
$env:KWJA_EXE = "$PWD\.kwja-venv\Scripts\kwja.exe"
```

Never disable TLS certificate verification. The pure-Python `pure-cdb` installation avoids requiring Microsoft C++ Build Tools.

## Routine analysis

The analyzer's KWJA subprocess defaults to cache-only mode by setting `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_DATASETS_OFFLINE=1` when those variables are absent. This prevents runtime stalls caused by model-metadata requests.

To deliberately allow Hub access for a controlled refresh, set the variables to `0` before starting the analyzer. Explicit caller values are preserved.
````

### `JP analyzer/docs/PROJECT_SNAPSHOT_CURRENT.md`

- Purpose: Documentation.
- Size: 215853 bytes
- SHA-256: `5d26af018006aed383c32dec3d7ed10c4a4479f5db9280d3a719a6d004bc2ffd`

````markdown
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
& ".
un_tests.ps1"
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
````

### `JP analyzer/docs/READER_PROJECTION_CONTRACT.md`

- Purpose: Reader contract, rendering, or UI.
- Size: 3166 bytes
- SHA-256: `558629abe4f478c7725a53a29bbe09482c93e1ef58d9054bf8ed48352835cfb6`

````markdown
\# JP Analyzer Reader Projection Contract



\## Status



This document defines the ownership boundary between JP Analyzer and Novel Audio Miner.



JP Analyzer is the sole owner of linguistic analysis and learner-facing span decisions.



Novel Audio Miner must not infer linguistic boundaries, merge analyzer spans, construct compound headwords, or reclassify analyzer output.



\## Analyzer responsibilities



JP Analyzer must produce authoritative, exact, non-overlapping reader spans.



For every reader span, JP Analyzer decides:



\- source start offset

\- source end offset

\- surface text

\- display role

\- lexical type

\- canonical headword

\- known-word lookup key

\- frequency lookup key

\- unknown-word colour policy

\- comprehension eligibility

\- New Words eligibility

\- mining eligibility

\- grammar ID, where applicable

\- confidence

\- supporting evidence IDs

\- correction information, where applicable



\## Required reader roles



The reader projection may produce:



\- lexical

\- lexical-compound

\- numeric-lexical

\- name

\- learnable-grammar

\- function

\- punctuation

\- unresolved



\## Reader-span invariants



Every reader span must satisfy:



1\. `start` and `end` are integer offsets.

2\. `0 <= start < end <= len(text)`.

3\. `surface == text\[start:end]`.

4\. Reader spans are ordered.

5\. Reader spans do not overlap.

6\. Reader spans respect protected punctuation boundaries.

7\. Reader spans provide complete source coverage.

8\. Lexical lookup keys are explicit.

9\. Novel Audio Miner is not required to reconstruct a headword.

10\. Novel Audio Miner is not required to merge spans.



\## Display-unit requirement



Inflected words and validated compounds must be emitted as complete learner-facing display units.



Examples:



\- `頷いて` with lookup key `頷く`

\- `出て行った` with lookup key `出て行く`

\- `とばかりに` as one learnable grammar span

\- `二人` as numeric lexical material with lookup key `二人`



Internal morphology remains available separately and must not force fragmented reader colouring.



\## User-specific colour resolution



JP Analyzer supplies:



\- the display role

\- known-word lookup key

\- frequency lookup key

\- unknown-word colour policy



Novel Audio Miner may then consult user-specific known-word and frequency data.



This lookup does not constitute a linguistic decision.



\## Corrections and learning



Saved reader corrections belong to JP Analyzer.



Novel Audio Miner may collect corrections through its interface, but corrections must be stored and applied by JP Analyzer.



A correction is an example or exact constraint. A correction must not automatically become a global handwritten rule.



\## Compatibility



Existing `resolvedSpans` may remain for diagnostics and backward compatibility.



A new `readerSpans` output will become the authoritative Novel Audio Miner display contract.

````

### `JP analyzer/README.md`

- Purpose: Documentation.
- Size: 1061 bytes
- SHA-256: `fcf72fa570947e45689bb873f1733dc591cfee7e5d8b65d4f57465dc1d5b2d4b`

````markdown
# JP Analyzer

JP Analyzer is the single supported Japanese linguistic-analysis service in this repository.

## Production entry points

- Python: `app.analyzer.analyze` and `app.analyzer.analyze_full`
- FastAPI: `app.analyzer.service:app`
- Health: `GET /health`
- Analysis: `POST /analyze`

The implementation is organized under `app/analyzer/layers` and owns morphology, structure, candidate generation, dictionary evidence, KWJA evidence, evidence gating, final resolution, diagnostics, and compact/full output.

## Test suite

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\run_tests.ps1
```

Regression corpora are versioned under `tests/corpora`. Generated snapshots and reports remain local.

## KWJA runtime

Routine analysis is cache-only by default and does not contact Hugging Face. Install or refresh the isolated KWJA environment with `scripts/setup_kwja_windows.ps1` during a controlled online session, then set `KWJA_EXE` to that environment's executable. See `docs/KWJA_SETUP_WINDOWS.md`.
````

### `JP analyzer/requirements-frozen-py311.txt`

- Purpose: Python dependency configuration.
- Size: 1023 bytes
- SHA-256: `a7e463ebdcf1c92c108db2c013ee0c9beda3aeae92d0bf6c80c0b1311b2bbbb1`

````text
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.14.2
blis==1.3.3
catalogue==2.0.10
certifi==2026.6.17
charset-normalizer==3.4.9
click==8.4.2
cloudpathlib==0.24.0
colorama==0.4.6
confection==1.3.3
cymem==2.0.13
fastapi==0.116.1
ginza==5.2.0
h11==0.16.0
httpcore==1.0.9
httptools==0.8.0
httpx==0.28.1
idna==3.18
ja-ginza==5.2.0
Jinja2==3.1.6
markdown-it-py==4.2.0
MarkupSafe==3.0.3
mdurl==0.1.2
murmurhash==1.0.15
numpy==2.4.6
packaging==26.2
plac==1.4.5
preshed==3.0.13
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.20.0
python-dotenv==1.2.2
PyYAML==6.0.3
requests==2.34.2
rich==15.0.0
shellingham==1.5.4
smart_open==8.0.0
spacy==3.8.14
spacy-legacy==3.0.12
spacy-loggers==1.0.5
srsly==2.5.3
starlette==0.47.3
SudachiDict-core==20260428
SudachiPy==0.6.11
thinc==8.3.13
tqdm==4.68.4
typer==0.26.8
typing-inspection==0.4.2
typing_extensions==4.16.0
urllib3==2.7.0
uvicorn==0.35.0
wasabi==1.1.3
watchfiles==1.2.0
weasel==1.0.0
websockets==16.1
wrapt==2.2.2
````

### `JP analyzer/requirements-kwja-py311.txt`

- Purpose: Python dependency configuration.
- Size: 146 bytes
- SHA-256: `bb2685f638dc7d1b4d108c2dfdbafef186bd15482a9a9349b319b3f3e60462c6`

````text
kwja==2.5.1
pure-cdb==4.0.0
torch==2.7.1
transformers==4.50.3
tokenizers==0.21.4
safetensors==0.8.0
sentencepiece==0.2.1
protobuf==7.35.1
````

### `JP analyzer/requirements.txt`

- Purpose: Python dependency configuration.
- Size: 156 bytes
- SHA-256: `504419d8379e69ad3e687bcfd288eb964771836c83415fed2faf359708426722`

````text
fastapi==0.116.1
uvicorn[standard]==0.35.0
sudachipy>=0.6.11,<0.7
sudachidict_core>=20250129
spacy>=3.8,<3.9
ginza==5.2.0
ja_ginza==5.2.0
pydantic>=2.11,<3
````

### `JP analyzer/run_snapshot_regression.py`

- Purpose: Python source.
- Size: 3332 bytes
- SHA-256: `34c6b5b98f982a8b6f8702d0a3b7b33f1bf64292f035057eb36d0ba4cda78e53`

````python
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from app.analyzer.pipeline import analyze_full
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest


def read_sentences(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path | None, value) -> None:
    if path is not None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, default=Path("snapshot_regression_report.json"))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()

    sentences = read_sentences(args.input_file)
    references = json.loads(args.reference.read_text(encoding="utf-8-sig"))
    if len(references) != len(sentences):
        raise RuntimeError("Reference count mismatch")

    actuals = []
    if args.resume and args.output and args.output.exists():
        actuals = json.loads(args.output.read_text(encoding="utf-8-sig"))
        print(f"Resuming after {len(actuals)} sentence(s).")

    mismatches = []
    timings = []
    for index in range(len(actuals), len(sentences)):
        sentence_id = f"S{index + 1:04d}"
        started = time.perf_counter()
        last_error = None
        for attempt in range(args.retries + 1):
            try:
                actual = semantic_snapshot(analyze_full(sentences[index]))
                last_error = None
                break
            except Exception as error:
                last_error = error
                print(f"{sentence_id} attempt={attempt + 1} ERROR {type(error).__name__}: {error}")
        if last_error is not None:
            raise last_error
        elapsed = (time.perf_counter() - started) * 1000
        timings.append(elapsed)
        actuals.append(actual)
        write_json(args.output, actuals)
        expected = references[index]
        passed = actual == expected
        if not passed:
            mismatches.append({
                "sentenceId": sentence_id,
                "expectedDigest": snapshot_digest(expected),
                "actualDigest": snapshot_digest(actual),
                "text": sentences[index],
            })
        report = {
            "sentences": len(sentences),
            "completed": len(actuals),
            "passed": len(actuals) - len(mismatches),
            "failed": len(mismatches),
            "semanticParity": len(actuals) == len(sentences) and not mismatches,
            "meanRuntimeMs": sum(timings) / len(timings) if timings else None,
            "mismatches": mismatches,
        }
        write_json(args.report, report)
        print(f"{sentence_id} {'PASS' if passed else 'FAIL'} elapsed_ms={elapsed:.2f} checkpoint={len(actuals)}/{len(sentences)}")

    raise SystemExit(0 if not mismatches else 1)


if __name__ == "__main__":
    main()
````

### `JP analyzer/run_tests.ps1`

- Purpose: Project source or support file.
- Size: 647 bytes
- SHA-256: `4e56bcad3c84d3c11db1fbe9fd04c2f48824fdc3282c671eb0ce688c263fa2a6`

````powershell
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
````

### `JP analyzer/scripts/setup_kwja_windows.ps1`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 511 bytes
- SHA-256: `d88cc37b3440bf30c333a15b4658bd48647d52d722d0c0a8a921989ab812140e`

````powershell
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
py -3.11 -m venv .kwja-venv
$Python = ".\.kwja-venv\Scripts\python.exe"
& $Python -m pip install --upgrade pip wheel
$env:ENABLE_DJB_HASH_CEXT = "0"
$env:SETUPTOOLS_USE_DISTUTILS = "stdlib"
& $Python -m pip install --no-build-isolation --no-binary pure-cdb "pure-cdb==4.0.0"
& $Python -m pip install -r ".\requirements-kwja-py311.txt"
Write-Host "KWJA executable: $PWD\.kwja-venv\Scripts\kwja.exe" -ForegroundColor Green
````

### `JP analyzer/tests/__init__.py`

- Purpose: Automated test or fixture.
- Size: 0 bytes
- SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

````python

````

### `JP analyzer/tests/corpora/development/random_sentences.txt`

- Purpose: Automated test or fixture.
- Size: 17647 bytes
- SHA-256: `b074dc201ea445bd8d0f349c15bbe87af303281ffea814571bb1774d9b6ed3ca`

````text
そこまで大きな声ではなかったけれど、静かな覚悟を伴うような強い声は、この場の鬱々とした空気を切り裂くようだった。

彼をそういう対象として見てしまうことには、忌避感みたいな感情が常につきまとう。

それは優しさや愛情、あるいは正義感と呼べる感情だったのかもしれない。

「……いやいや、まだ早すぎるから」

私が初めて一から考えた企画だったのに、もう私は関係なくなっちゃった……」

「告白する前から諦めるなんて、つまらないわよ？

まだ小さくて、自分のことも『僕』と言っていたタッくんは、仕事と育児で手一杯になっていた私に、そんなこと言ってくれたんだった。

それでダメなら、別れればいいだけの話だ』

本当に、わからないことだらけ。

三十路を越えた女が、子供向けアニメに夢中だなんて──

お酒が入ると──そのタイミングを待っていたとばかりに、大人達は現実的な話を始めた。

タッくんは困惑の表情を浮かべていたが──そこへ。

言い終わると、また恥ずかしそうに口元を隠す。

「俺……ずっと、その人のことが好きで……その人以外と、付き合うとか全然考えられなくて」

『寝坊った』という動詞が娘の造語なのか、それとも最近の若者言葉なのかは、やっぱり私にはわからない。

そして……社長ではなく一人の女として、きみのことを応援したくなってしまったのさ。

端的に言えば、かわいい顔でファッショナブルなイケメン、となる。

『ラブカイザー同士が最後の一人になるまで殺し合う』なんて設定、今の時代じゃ絶対無理だと思うわ。

「また、タク兄のことで悩んでるの？

私にとって──身を切る覚悟で臨む作戦とも言えよう。

なんでこんなに──恥ずかしいの？

あと、こっち押すと主題歌や挿入歌も流れるの！

今から大体、十年前ぐらいの話──

となれば……やっぱりあの二人には、早くくっついてもらわないとね！

テーブルの料理は大体片付いていて、お摘まみ用のチーズとクラッカーだけがあった。

私はなにも言えなくなってしまう。

「いつだかうちで夕飯食べたときだって……親父が酒勧めても、しっかり断ってたでしょ。

だって──急に真面目な顔をするから。

姉夫婦の子供を、私がきちんと育てようと、決意した。

今までの軽薄な雰囲気が消え、口調に真剣味が増す。

「何っ回も言ったけど、それはママの勘違いだってば」

タオル巻いただけって……ちゃんと、服着てこなきゃ」

すごく綺麗で、女性として、とても魅力的だと思います。

いや、その……ま、まあ、そうね。

私の言葉を遮るように、美羽は言う。

ほんと、今すぐにでも婿に欲しいっ！

あなたも、私にばっかり任せてないで、少しはお義父さんの介護を手伝ったらどうなの？

でも、しょうがないじゃないですか。

あのとき、綾子さんが勝手に入ってきたんじゃないですか！

でも、いつまでも引き延ばしてもいられない。

私は、へなへなとその場にへたり込んでしまう。

顔立ちは中学生でも通用しそうなぐらいに幼く、長く伸ばした髪は後ろで一つに束ねてある。

けど私には──なにもなかった。

覚悟を決めたような声で呟いた後──ひょい、と。

酔っ払ったせいなのか、かなり知った風なことを言ってしまう。

なんかもう、普通にすっぽんぽんでタッくんの前を歩き回ってた気がする。

「最初に見たときから綺麗な人だと思ってて……極めつきは、一緒にお風呂入ったときに──」

すみません、美羽がなんか飲み物が欲しいって──えっ！

「綾子さんは……おばさんじゃないです。

アニメキャラになりきるエネルギーは、最初の一回で全て使い果たしてしまったのだ。

社員が最大限に働ける環境を作るのは、会社として当然のことだからね。

十歳になったばかりの子供が、追い詰められていた私の心を優しく温めてくれた。

気を抜くと鼻血が出そう……よし。

俺が告白なんかしたせいで、たぶん面倒な思いさせちまってるんだから」

これでは泥棒も僕も家には入れない。

「タッくんが夢に生きてるなら、その夢から覚めさせてあげなきゃね。

ソファに体を預けていた私は、体を引きずるように立ち上がる。

隣の家に入るのはこれが初めてだった。

「……そういうわけにはいかないでしょ」

告白自体は衝動的なものだったのかもしれないけれど、でもタッくんは、私との将来を予想以上に真面目に考えてくれていたようだった。

鍵、もらってたんだけど、家の中に忘れちゃった」

仕事帰りはあちこち飲み歩くし、朝帰りなんてザラだし、酔った勢いでお持ち帰りされちゃうことだって──」

パジャマ姿より、パジャマ姿を恥ずかしいと思ってしまった自分が恥ずかしい。

娘と二人で玄関に向かうと──そこには、彼がいた。

犠牲とまではいかなくてもさ、私に気を遣って、恋愛とかそういうの、遠慮してた感じではあったんでしょ？

──施設にでも入れるしかないだろうな。

ごめんね、明日からはちゃんと作るから」

なんでこんな思春期の乙女みたいな反応してるの!

「ママ……もう、また寝坊したの？

こんなご馳走まで用意してもらって」

びしょ濡れになって肌に張り付いた服が気持ち悪い。

なにに怒ってるんだろう、私は？

頭の中は……綾子ママのことでいっぱいだった。

「綾子さん、もしかして……俺とのこと、美羽に話しました？

「なにやってるんですか、こんなところで……」

在宅での仕事を早めに切り上げてから、私は夜のために準備に取りかかった。

真剣な声音で、タッくんは言った。

話を聞けば聞くほど、真剣さが痛いぐらいに伝わってきた。

手のひらで感じる彼の手は──とても大きかった。

そして僕のことを、巧の彼女だと誤解していた……」

クラスメイトからも女顔をからかわれたりして、それを少々コンプレックスにも感じていた、そんな頃。

ほ、ほんとにちょっとだけどね！

「おばさん、毎日が寂しくてつまらないから、美羽ちゃんと一緒に暮らしたいの。

タッくんって、私のこと大好きなの!

「庶民的な角ハイとかも大好きよ！

ジャンル、というかシリーズとしての方針は──青年主人公と隣家のママ、一対一の純愛ラブコメで行くつもりです。

あのときの綾子ママは、まるでヒーローみたいだった」

もう少し時間をかけてじっくり考えたいっていうか……」

だから昨日の夜、『明日はこれで家に入ってね』と、家の鍵を渡されていたのに……勉強机の上に置きっぱなしにしたまま忘れてしまった。

寝起きのパジャマ姿で、髪もボサボサ。

なにも、間違ってないですけど」

よ、よ、酔っ払っちゃったのー」

わかった、聞かなかったことにする」

十歳にもなって人に服を脱がせてもらうのは、さすがに恥ずかしかった。

ああ、お昼は適当に買って食べるから、心配しなくていいよ」

言うまでもなく僕の趣味全開の作品です。

記憶の奥底に眠っていた過去を、ぼんやりと思い出す。

結婚した娘が、徒歩一分のお隣に住んでる──うんうん、なんかいいわね！

大人をからかうんじゃありません」

いろんな人から『今は子供との時間を大事にした方がいいよ』って、嫌みなのか優しさなのかわからないこと言われて……。

だから……イエスともノーともつかない、すごく曖昧な笑みを浮かべてその場を乗り切るのだった。

もう言葉を、止めることができない。

「でも巧は、その幻想を二十歳になるまでずっと抱き続けてきたわけだ。

ブランドバッグには躊躇しまくりの私だったけれど、この手のグッズには割と財布の紐が緩くなってしまう。

「朝から辛気くさい顔見せられるこっちの身にもなってよね」

すね毛一つ生えていない美脚で、淑やかな足取りで颯爽と歩いていく。

──私はお義父さんの世話で手一杯なのよ。

私は……衝撃のあまり、放心状態となってしまう。

大きく口を開けて、声を出して笑う。

「十年前の裸が忘れられなくて未だに恋してるなんて……巧もなかなかに変態だね。

あのときタッくんは『合宿』と称して、一週間ぐらいうちに泊まって最後の追い込みをかけてくれた。

子供を育てた経験も皆無……それでもきみは、美羽ちゃんを引き取ると決めた。

──綾子さんが俺のこと好きになってくれるように、頑張ります。

彼女はいなくても、気になってる子ぐらいはいるんじゃないの？

その生真面目さ、一途さに──きゅん、と胸が高鳴ってしまう。

「十年前って……タッくん、あなたまだ、十歳ぐらいのときじゃないの!

私が一人で『ラブカイザー』の映画やイベントに通ってたら……なんていうか、浮くのよ！

無意識のうちに、私は声を上げていた。

それでも私は──気づけば喫茶店を飛び出し、二人の後をつけていた。

今の自分の格好を思い出し、羞恥心が一気にこみ上げた。

私は頭を抱えて悶絶してしまう。

タッくんをエッチな格好で悩殺したいとかそういうことじゃなくてね！

巧の友達で、同じ大学に通ってます」

俺、ちょっと先走りすぎましたもんね。

返事をする私は──シャワー中だった。

亡くなった夫婦には五歳になる娘がいた。

でも今は、どんな顔をして彼に会えばいいかわからない──

それから照れ隠しみたいに、ぐいっとワインを飲み干す。

──綾子ママには、僕がいるよ。

高級ワイン特有のまろやかな舌触りやフルーティーな香りも一切感じない。

階段を降りて洗面所へと向かい、ドタドタと準備を終えるとリビングへと入ってくる。

ちょっと放心状態になってしまう。

うちの隣に住んでいる夫婦が──交通事故で亡くなった。

そう告げると、タッくんの表情に一瞬、安心が滲んだ。

一番下のランクでも、かなり高い。

「タク兄と仲直りできた途端、急に元気になるんだから」

すでに制服に着替えていて、いつでも学校に行けそうな様子。

簡単になんて、どうしたって考えられない──

今打ち合わせた内容を、イラストレーターには私の方から伝えておきますね。

「高校に入っても大学に入っても、全然変わらないの……」

テーブルを強く叩く音と共に、一人の女性が立ち上がった。

観念した私はサングラスを外す。

私の自虐を遮るように、タッくんは強く言った。

それどころか……どんどん距離が縮まっている気さえする。

緊張から解放された私がゆっくりとリビングに戻ると──テーブルに置いておいたスマホに、ラインのメッセージが来ていた。

胸の奥底で燃え上がる感情に、押し出されるように。

ほんとに彼女だと思ってたんですか？

人生は、大人になってからの方が長いのだから。

そんな彼を見て、また胸が痛くなるけれど──でも、私は続ける。

どんな顔をすればいいかわからなかった。

日曜日の朝にやっている、国民的女子児童向けアニメである。

「すみません……危なっかしくて、ほっとけないんで」

さすがは敏腕女社長というべきか。

もう、三十も超えてるのに……」

美羽は一瞬、片眉をぴくりと動かした。

「そんな簡単に、ふっ切れるわけないじゃないですか。

言ってることメチャクチャですし……」

もしも関係が明るみになれば、世間からどんな目で見られるかわからない。

「……タッくんは今、一時の気分で舞い上がってるだけなのよ。

ママは──一回も自分の気持ちを言ってない」

不安に揺れる瞳で、しかし譲れない感情を滲ませながら。

恋をすると、仕事に張りが出てくる』

綾子さんには、フラれたって言ってたよね？

それに俺だって……自分の親のことは大事ですし、がっかりさせるようなことはしたくない」

濡れたままだと、風邪引いちゃうでしょ」

子供向けとは思えないぐらい、ストーリーが凝ってるし、深いテーマ性がある。

なにも言えない私を無視して、美羽は二階に上がっていってしまった。

「……め、迷惑になったら、やだな、って思って。

「美羽が普通に愚痴ってましたし。

「今の私が、十も年下の男の子と付き合うなんて……常識的に考えて、無理なんですよ。

美羽が拗ねたように頰を膨らませていた。

恥ずかしさと虚しさで涙が溢れそうだけれど……でも、これでいいの。

あっという間で、怒濤の十年間だった。

……まあ、私のガードが甘いってのも、大いに関係してそうだけど。

「美羽なんて、いっつもいっつもバカにしてくるだけだったのに……」

「そう、謙虚なのね、タッくんは」

向こうだって、なんとも思ってないってことはないでしょう。

一人でちゃっちゃと朝食を食べ終え、美羽は学校へと向かう。

肩を摑まれて強引に引っ張られ、僕は綾子ママに後ろから抱きしめられる形となった。

「えと、あの、た、巧くんが不満とか嫌いとかそういうことではなくて、やはり常識的に考えて、私達の関係は難しいと思いましたので……」

膝を折り、彼女と目線を合わせた。

「嫌なことや辛いことがあったら、僕が綾子ママを守るから。

「そ、それはわかってるけど……でも、ちょっとどうかと思うなあ。

私は慌てて、持ってきていた雑誌で顔を隠す。

「俺のこと、真剣に考えてくれて……ありがとうございます。

「うちは外食しただけですから。

私への想いを伝えるための言葉を──

なぜなら──失うものがなかったから』

じゃあ……水泳とか、どうかしら？

その後も私達は『ラブカイザー』トークに花を咲かせた。

雨が降り出してから買ったのか、服や髪は濡れている。

惚れている女から男扱いされず、子供扱いされ続けることが、虚しくて切なくて悔しくて悲しくて、我慢できなくなっていたのだ。

タッくんて、本当に小さくてかわいいわね。

「ちょっとは俺のこと、男として意識してくれてるってことですか？

呆れ口調で言う美羽に、私は軽く肩をすくめた。

三回の離婚、その全てが自分の浮気が理由──狼森夢美は、そういう奔放で豪快な女性だ。

社長は最後まで私を担当にしようと頑張ってくれたんだけど……申し訳なくって、誰かに代わってもらえるように自分からお願いしたの」

仕事の確認が済んだ後、軽い相談のつもりでタッくんとのことを「私じゃなくて友達の話なんですけど～」と始めたら、一瞬で噓がバレてしまい、あれよあれよという間に全ての情報を抜き取られてしまった。

完成した朝食をテーブルに並べているタイミングで、

「あのね……いつも言ってるけど、私とタク兄はそういうんじゃないから。
````

### `JP analyzer/tests/corpora/parity/consolidation_fresh_unseen_200.txt`

- Purpose: Automated test or fixture.
- Size: 22543 bytes
- SHA-256: `5fec594ffe3b3c3159e53db965d959054af54bdfdcef91ec1145845772ac6955`

````text
無線が途切れたため、剣士ナナは予定を変え、夜の操車場の裏口から突入した。
雪原の砦の奥から低い鐘の音が響き、薬草師レンは足を止めて耳を澄ませた。
遠征の最後に旅人のユウが見つけたのは宝ではなく、次の旅へ続く新しい地図だった。
遠征の最後に地図師ミナが見つけたのは宝ではなく、次の旅へ続く新しい地図だった。
「今日は早かったね」と声を掛けられ、書店員の恵は照れながら靴をそろえた。
雨が本降りになる前に夜明け前に北門へ着くため、旅人のユウの隊は休憩を十分で切り上げた。
底の見えない裂け目の向こうで小さな火が揺れ、見習い騎士アオイは行方不明の一隊が近いと悟った。
弁当の卵焼きを作る途中で猫が前を横切り、高校生の真琴は急ぐのをやめてその背中を見送った。
「今日は早かったね」と声を掛けられ、小学生の陸は照れながら靴をそろえた。
悠真の短いメッセージを読み返しながら、美月は送信ボタンを押せずにいた。
老船員ガクが琥珀の護符を岩のくぼみにはめると、青い洞窟の壁が静かに二つへ割れた。
朝霧が晴れるころ、地図師ミナたちは増水した地下水路を一列になって渡った。
旅人のユウは霧の峡谷の入口で欠けた羅針盤を掲げ、道が正しいことを確かめた。
春香は駅前の喫茶店の窓際で、直人が来るたびに時計を見ないふりをした。
戦いが終わると、追跡者レイは武器を収め、負傷者の数を静かに確認した。
大学の図書館で偶然会った莉子と蒼は、用事が済んでも十分ほど立ち話を続けた。
最後の扉が閉まる寸前、機関士ソウは床を滑って向こう側へ抜けた。
地図師ミナが銀色の鍵を岩のくぼみにはめると、沈んだ神殿の壁が静かに二つへ割れた。
逃走中の密輸団との距離が五歩まで縮まり、護衛のトウマは呼吸を整えて構え直した。
暴走する装甲車との距離が五歩まで縮まり、剣士ナナは呼吸を整えて構え直した。
眠る石像の列の向こうで小さな火が揺れ、薬草師レンは行方不明の一隊が近いと悟った。
無線が途切れたため、護衛のトウマは予定を変え、閉鎖された工場の裏口から突入した。
朝霧が晴れるころ、見習い騎士アオイたちは底の見えない裂け目を一列になって渡った。
日没まで残り一刻しかなく、老船員ガクは山頂の灯台を再びともすという約束を胸に走った。
遠征の最後に老船員ガクが見つけたのは宝ではなく、次の旅へ続く新しい地図だった。
書店員の恵が昼休みに五分だけ外へ出ると、風が思ったより冷たくて気分が変わった。
高校生の真琴は朝の台所で湯気の立つマグカップを両手で包んだ。
時計が七時を知らせると、小学生の陸は回覧板を隣へ届けるために立ち上がった。
一日の終わり、会社員の佐和は明日の予定を一つだけ手帳に書き、明かりを消した。
小さな音楽箱に残された小さな傷を見て、亮は千夏と初めて会った日を思い出した。
一日の終わり、料理人の修平は明日の予定を一つだけ手帳に書き、明かりを消した。
「右から二人、正面に一人」と剣士ナナが告げ、仲間たちは同時に散った。
夕食の材料を選ぶ途中で猫が前を横切り、会社員の佐和は急ぐのをやめてその背中を見送った。
警報が鳴るより早く、警備隊長カイは赤い解除レバーへ手を伸ばした。
小さな商店街には焼きたてのパンの匂いが流れ、小学生の陸も思わず足を緩めた。
古い写真に残された小さな傷を見て、蒼は莉子と初めて会った日を思い出した。
一日の終わり、書店員の恵は明日の予定を一つだけ手帳に書き、明かりを消した。
小学生の陸の家では夕飯の味噌汁が少し薄かったけれど、誰も文句を言わずにおかわりした。
青い洞窟の奥から低い鐘の音が響き、老船員ガクは足を止めて耳を澄ませた。
帰り道、直人が差し出した青い栞を受け取ると、春香の返事は少しだけ遅れた。
一日の終わり、高校生の真琴は明日の予定を一つだけ手帳に書き、明かりを消した。
閉鎖された工場で足音が三つ重なり、護衛のトウマは追っ手の位置を一瞬で読んだ。
料理人の修平の家では夕飯の味噌汁が少し薄かったけれど、誰も文句を言わずにおかわりした。
遠回りになると知りながら、千夏と亮は商店街の花屋まで同じ道を歩いた。
「右から二人、正面に一人」と機関士ソウが告げ、仲間たちは同時に散った。
帰り道、亮が差し出した小さな音楽箱を受け取ると、千夏の返事は少しだけ遅れた。
「右から二人、正面に一人」と追跡者レイが告げ、仲間たちは同時に散った。
爆風で窓が震え、追跡者レイは倒れた棚を盾にして次の機会を待った。
爆風で窓が震え、剣士ナナは倒れた棚を盾にして次の機会を待った。
黒い外套の一団との距離が五歩まで縮まり、警備隊長カイは呼吸を整えて構え直した。
雨が本降りになる前に失われた街道を見つけるため、見習い騎士アオイの隊は休憩を十分で切り上げた。
莉子が笑う理由を尋ねると、蒼は答えずに赤くなった空を指さした。
「また明日」と言った亮の声が、千夏にはいつもより近く聞こえた。
祭りの帰り、楓は迷子にならないようにと言って拓海の袖をつかんだ。
爆風で窓が震え、機関士ソウは倒れた棚を盾にして次の機会を待った。
朝霧が晴れるころ、旅人のユウたちは崩れかけた吊り橋を一列になって渡った。
商店街の花屋で偶然会った千夏と亮は、用事が済んでも十分ほど立ち話を続けた。
霧の峡谷の奥から低い鐘の音が響き、旅人のユウは足を止めて耳を澄ませた。
青い栞に残された小さな傷を見て、直人は春香と初めて会った日を思い出した。
「戻るなら今だ」と言われても、老船員ガクは青い洞窟へ続く階段を下りていった。
回覧板を隣へ届ける途中で猫が前を横切り、小学生の陸は急ぐのをやめてその背中を見送った。
春香が笑う理由を尋ねると、直人は答えずに赤くなった空を指さした。
戦いが終わると、機関士ソウは武器を収め、負傷者の数を静かに確認した。
閉鎖された工場の照明が落ちても、護衛のトウマは反射した金属の光を見逃さなかった。
美月は川沿いの遊歩道の窓際で、悠真が来るたびに時計を見ないふりをした。
無人の警備機が通路を塞ぐと、機関士ソウは煙幕の向こうへ短く合図した。
冷蔵庫の奥から昨日のプリンを見つけ、会社員の佐和は名前の札を確かめてから戻した。
薬草師レンが古代文字の石板を岩のくぼみにはめると、雪原の砦の壁が静かに二つへ割れた。
最後の扉が閉まる寸前、剣士ナナは床を滑って向こう側へ抜けた。
夜の操車場で足音が三つ重なり、剣士ナナは追っ手の位置を一瞬で読んだ。
「戻るなら今だ」と言われても、見習い騎士アオイは風鳴りの森へ続く階段を下りていった。
「また明日」と言った悠真の声が、美月にはいつもより近く聞こえた。
日没まで残り一刻しかなく、薬草師レンは仲間への合図を送るという約束を胸に走った。
一日の終わり、小学生の陸は明日の予定を一つだけ手帳に書き、明かりを消した。
祭りの帰り、千夏は迷子にならないようにと言って亮の袖をつかんだ。
正体不明の狙撃手との距離が五歩まで縮まり、追跡者レイは呼吸を整えて構え直した。
千夏が笑う理由を尋ねると、亮は答えずに赤くなった空を指さした。
会社員の佐和は夕方のスーパーで湯気の立つマグカップを両手で包んだ。
町の図書室には焼きたてのパンの匂いが流れ、書店員の恵も思わず足を緩めた。
冷蔵庫の奥から昨日のプリンを見つけ、小学生の陸は名前の札を確かめてから戻した。
高校生の真琴の家では夕飯の味噌汁が少し薄かったけれど、誰も文句を言わずにおかわりした。
沈んだ神殿の奥から低い鐘の音が響き、地図師ミナは足を止めて耳を澄ませた。
夕方のスーパーには焼きたてのパンの匂いが流れ、会社員の佐和も思わず足を緩めた。
返却本を棚へ戻す途中で猫が前を横切り、書店員の恵は急ぐのをやめてその背中を見送った。
手編みの小袋に残された小さな傷を見て、拓海は楓と初めて会った日を思い出した。
無人の警備機との距離が五歩まで縮まり、機関士ソウは呼吸を整えて構え直した。
最後の扉が閉まる寸前、警備隊長カイは床を滑って向こう側へ抜けた。
逃走中の密輸団が通路を塞ぐと、護衛のトウマは非常梯子を使って上階へ回り込んだ。
海辺のバス停で偶然会った楓と拓海は、用事が済んでも十分ほど立ち話を続けた。
最後の扉が閉まる寸前、護衛のトウマは床を滑って向こう側へ抜けた。
洗濯物を取り込んだあと、料理人の修平は一枚だけ残った靴下を不思議そうに眺めた。
正体不明の狙撃手が通路を塞ぐと、追跡者レイは相手の踏み込みを半歩だけ外した。
「また明日」と言った直人の声が、春香にはいつもより近く聞こえた。
風鳴りの森の奥から低い鐘の音が響き、見習い騎士アオイは足を止めて耳を澄ませた。
帰り道、悠真が差し出した借りた傘を受け取ると、美月の返事は少しだけ遅れた。
小学生の陸が昼休みに五分だけ外へ出ると、風が思ったより冷たくて気分が変わった。
「今日は早かったね」と声を掛けられ、高校生の真琴は照れながら靴をそろえた。
莉子は大学の図書館の窓際で、蒼が来るたびに時計を見ないふりをした。
市場の屋根で足音が三つ重なり、警備隊長カイは追っ手の位置を一瞬で読んだ。
洗濯物を取り込んだあと、会社員の佐和は一枚だけ残った靴下を不思議そうに眺めた。
遠回りになると知りながら、莉子と蒼は大学の図書館まで同じ道を歩いた。
莉子と蒼が雨宿りをしていると、軒下で肩が触れ、二人は同時に半歩だけ離れた。
無線が途切れたため、機関士ソウは予定を変え、燃える倉庫の裏口から突入した。
崩れかけた吊り橋の向こうで小さな火が揺れ、旅人のユウは行方不明の一隊が近いと悟った。
旅人のユウが欠けた羅針盤を岩のくぼみにはめると、霧の峡谷の壁が静かに二つへ割れた。
帰り道、拓海が差し出した手編みの小袋を受け取ると、楓の返事は少しだけ遅れた。
増水した地下水路の向こうで小さな火が揺れ、地図師ミナは行方不明の一隊が近いと悟った。
駅前の喫茶店で偶然会った春香と直人は、用事が済んでも十分ほど立ち話を続けた。
古い団地の庭には焼きたてのパンの匂いが流れ、料理人の修平も思わず足を緩めた。
植木鉢に水をやる途中で猫が前を横切り、料理人の修平は急ぐのをやめてその背中を見送った。
千夏は商店街の花屋の窓際で、亮が来るたびに時計を見ないふりをした。
「戻るなら今だ」と言われても、地図師ミナは沈んだ神殿へ続く階段を下りていった。
地図にはない分かれ道を前に、老船員ガクは琥珀の護符の傷を手掛かりに左を選んだ。
遠回りになると知りながら、楓と拓海は海辺のバス停まで同じ道を歩いた。
戦いが終わると、剣士ナナは武器を収め、負傷者の数を静かに確認した。
川沿いの遊歩道で偶然会った美月と悠真は、用事が済んでも十分ほど立ち話を続けた。
小学生の陸は小さな商店街で湯気の立つマグカップを両手で包んだ。
書店員の恵は町の図書室で湯気の立つマグカップを両手で包んだ。
地図にはない分かれ道を前に、旅人のユウは欠けた羅針盤の傷を手掛かりに左を選んだ。
朝霧が晴れるころ、薬草師レンたちは眠る石像の列を一列になって渡った。
戦いが終わると、護衛のトウマは武器を収め、負傷者の数を静かに確認した。
雨の高架橋で足音が三つ重なり、追跡者レイは追っ手の位置を一瞬で読んだ。
蒼の短いメッセージを読み返しながら、莉子は送信ボタンを押せずにいた。
無線が途切れたため、警備隊長カイは予定を変え、市場の屋根の裏口から突入した。
帰り道、蒼が差し出した古い写真を受け取ると、莉子の返事は少しだけ遅れた。
地図師ミナは沈んだ神殿の入口で銀色の鍵を掲げ、道が正しいことを確かめた。
亮の短いメッセージを読み返しながら、千夏は送信ボタンを押せずにいた。
借りた傘に残された小さな傷を見て、悠真は美月と初めて会った日を思い出した。
美月が笑う理由を尋ねると、悠真は答えずに赤くなった空を指さした。
祭りの帰り、莉子は迷子にならないようにと言って蒼の袖をつかんだ。
遠回りになると知りながら、美月と悠真は川沿いの遊歩道まで同じ道を歩いた。
警報が鳴るより早く、護衛のトウマは赤い解除レバーへ手を伸ばした。
楓と拓海が雨宿りをしていると、軒下で肩が触れ、二人は同時に半歩だけ離れた。
「また明日」と言った拓海の声が、楓にはいつもより近く聞こえた。
雨が本降りになる前に山頂の灯台を再びともすため、老船員ガクの隊は休憩を十分で切り上げた。
最後の扉が閉まる寸前、追跡者レイは床を滑って向こう側へ抜けた。
朝の台所には焼きたてのパンの匂いが流れ、高校生の真琴も思わず足を緩めた。
「戻るなら今だ」と言われても、薬草師レンは雪原の砦へ続く階段を下りていった。
「今日は早かったね」と声を掛けられ、会社員の佐和は照れながら靴をそろえた。
夜の操車場の照明が落ちても、剣士ナナは反射した金属の光を見逃さなかった。
料理人の修平は古い団地の庭で湯気の立つマグカップを両手で包んだ。
時計が七時を知らせると、会社員の佐和は夕食の材料を選ぶために立ち上がった。
楓は海辺のバス停の窓際で、拓海が来るたびに時計を見ないふりをした。
冷蔵庫の奥から昨日のプリンを見つけ、料理人の修平は名前の札を確かめてから戻した。
日没まで残り一刻しかなく、見習い騎士アオイは失われた街道を見つけるという約束を胸に走った。
「右から二人、正面に一人」と護衛のトウマが告げ、仲間たちは同時に散った。
会社員の佐和が昼休みに五分だけ外へ出ると、風が思ったより冷たくて気分が変わった。
時計が七時を知らせると、書店員の恵は返却本を棚へ戻すために立ち上がった。
美月と悠真が雨宿りをしていると、軒下で肩が触れ、二人は同時に半歩だけ離れた。
地図にはない分かれ道を前に、薬草師レンは古代文字の石板の傷を手掛かりに左を選んだ。
「今日は早かったね」と声を掛けられ、料理人の修平は照れながら靴をそろえた。
爆風で窓が震え、護衛のトウマは倒れた棚を盾にして次の機会を待った。
千夏と亮が雨宿りをしていると、軒下で肩が触れ、二人は同時に半歩だけ離れた。
薬草師レンは雪原の砦の入口で古代文字の石板を掲げ、道が正しいことを確かめた。
洗濯物を取り込んだあと、小学生の陸は一枚だけ残った靴下を不思議そうに眺めた。
雨が本降りになる前に封印の間を探し出すため、地図師ミナの隊は休憩を十分で切り上げた。
「また明日」と言った蒼の声が、莉子にはいつもより近く聞こえた。
祭りの帰り、春香は迷子にならないようにと言って直人の袖をつかんだ。
警報が鳴るより早く、機関士ソウは赤い解除レバーへ手を伸ばした。
朝霧が晴れるころ、老船員ガクたちは逆巻く砂の壁を一列になって渡った。
遠回りになると知りながら、春香と直人は駅前の喫茶店まで同じ道を歩いた。
遠征の最後に見習い騎士アオイが見つけたのは宝ではなく、次の旅へ続く新しい地図だった。
時計が七時を知らせると、高校生の真琴は弁当の卵焼きを作るために立ち上がった。
「戻るなら今だ」と言われても、旅人のユウは霧の峡谷へ続く階段を下りていった。
遠征の最後に薬草師レンが見つけたのは宝ではなく、次の旅へ続く新しい地図だった。
時計が七時を知らせると、料理人の修平は植木鉢に水をやるために立ち上がった。
老船員ガクは青い洞窟の入口で琥珀の護符を掲げ、道が正しいことを確かめた。
地図にはない分かれ道を前に、地図師ミナは銀色の鍵の傷を手掛かりに左を選んだ。
拓海の短いメッセージを読み返しながら、楓は送信ボタンを押せずにいた。
市場の屋根の照明が落ちても、警備隊長カイは反射した金属の光を見逃さなかった。
書店員の恵の家では夕飯の味噌汁が少し薄かったけれど、誰も文句を言わずにおかわりした。
燃える倉庫の照明が落ちても、機関士ソウは反射した金属の光を見逃さなかった。
直人の短いメッセージを読み返しながら、春香は送信ボタンを押せずにいた。
雨の高架橋の照明が落ちても、追跡者レイは反射した金属の光を見逃さなかった。
春香と直人が雨宿りをしていると、軒下で肩が触れ、二人は同時に半歩だけ離れた。
燃える倉庫で足音が三つ重なり、機関士ソウは追っ手の位置を一瞬で読んだ。
警報が鳴るより早く、剣士ナナは赤い解除レバーへ手を伸ばした。
雨が本降りになる前に仲間への合図を送るため、薬草師レンの隊は休憩を十分で切り上げた。
料理人の修平が昼休みに五分だけ外へ出ると、風が思ったより冷たくて気分が変わった。
高校生の真琴が昼休みに五分だけ外へ出ると、風が思ったより冷たくて気分が変わった。
会社員の佐和の家では夕飯の味噌汁が少し薄かったけれど、誰も文句を言わずにおかわりした。
冷蔵庫の奥から昨日のプリンを見つけ、高校生の真琴は名前の札を確かめてから戻した。
「右から二人、正面に一人」と警備隊長カイが告げ、仲間たちは同時に散った。
見習い騎士アオイが星図の巻物を岩のくぼみにはめると、風鳴りの森の壁が静かに二つへ割れた。
楓が笑う理由を尋ねると、拓海は答えずに赤くなった空を指さした。
洗濯物を取り込んだあと、書店員の恵は一枚だけ残った靴下を不思議そうに眺めた。
警報が鳴るより早く、追跡者レイは赤い解除レバーへ手を伸ばした。
地図にはない分かれ道を前に、見習い騎士アオイは星図の巻物の傷を手掛かりに左を選んだ。
冷蔵庫の奥から昨日のプリンを見つけ、書店員の恵は名前の札を確かめてから戻した。
日没まで残り一刻しかなく、旅人のユウは夜明け前に北門へ着くという約束を胸に走った。
祭りの帰り、美月は迷子にならないようにと言って悠真の袖をつかんだ。
暴走する装甲車が通路を塞ぐと、剣士ナナは床を蹴って手すりを飛び越えた。
無線が途切れたため、追跡者レイは予定を変え、雨の高架橋の裏口から突入した。
爆風で窓が震え、警備隊長カイは倒れた棚を盾にして次の機会を待った。
逆巻く砂の壁の向こうで小さな火が揺れ、老船員ガクは行方不明の一隊が近いと悟った。
黒い外套の一団が通路を塞ぐと、警備隊長カイは身を低くして柱の陰へ滑り込んだ。
洗濯物を取り込んだあと、高校生の真琴は一枚だけ残った靴下を不思議そうに眺めた。
日没まで残り一刻しかなく、地図師ミナは封印の間を探し出すという約束を胸に走った。
戦いが終わると、警備隊長カイは武器を収め、負傷者の数を静かに確認した。
見習い騎士アオイは風鳴りの森の入口で星図の巻物を掲げ、道が正しいことを確かめた。
````

### `JP analyzer/tests/corpora/parity/consolidation_fresh_unseen_200_manifest.json`

- Purpose: Automated test or fixture.
- Size: 552 bytes
- SHA-256: `55816540e341f62a17205e1800a6fde67984d02303dbce44790f3c63be058e7d`

````json
{
  "corpus": "consolidation_fresh_unseen_200.txt",
  "synthetic": true,
  "original": true,
  "seed": 20260715,
  "sentenceCount": 200,
  "nonEmptySentenceCount": 200,
  "uniqueSentenceCount": 200,
  "genreCounts": {
    "adventure": 50,
    "action": 50,
    "romance": 50,
    "slice_of_life": 50
  },
  "sha256": "33b32d7297358d2a11ab4eec0d4fce3a6e23f3d326b3d7641d937d8535d1e50b",
  "notes": "Original synthetic Japanese novel-style regression corpus; one sentence per line; four genres balanced and shuffled deterministically."
}
````

### `JP analyzer/tests/corpora/README.md`

- Purpose: Automated test or fixture.
- Size: 1212 bytes
- SHA-256: `ce8c59c1fcd3b417d65106adc1d3ceb35cad827ca594d39ba5492e675af635f6`

````markdown
# Analyzer Test Corpora

## Development corpus

Path:

tests/corpora/development/random_sentences.txt

Purpose:

- Existing 200-sentence development regression corpus.
- Used during phased analyzer development.
- Used for semantic regression and compatibility testing.

Count:

200 non-empty Japanese sentences.

## Consolidation parity corpus

Path:

tests/corpora/parity/consolidation_fresh_unseen_200.txt

Purpose:

- Fresh corpus created after the consolidated analyzer implementation.
- Used only for old-versus-consolidated semantic parity.
- Contains original synthetic Japanese novel-style sentences.
- It is not a native-corpus accuracy benchmark.

Composition:

- Adventure: 50
- Action: 50
- Romance: 50
- Slice of life: 50
- Total: 200

Sampling seed:

20260715

Expected SHA-256:

33b32d7297358d2a11ab4eec0d4fce3a6e23f3d326b3d7641d937d8535d1e50b

## Important distinction

These corpora verify behavior preservation and regression stability.

They are not the future linguistic-accuracy corpus. Accuracy tuning will use a separate 500-sentence corpus derived from authentic novel text, with development, validation, and final held-out subsets.
````

### `JP analyzer/tests/fixtures/single_case_semantic_reference.json`

- Purpose: Automated test or fixture.
- Size: 7839 bytes
- SHA-256: `574121c0b509db1fcd5a8306af51689b4d415f7a0af89f605a346c4524eb5d0d`

````json
[
  {
    "contractVersion": "1.0",
    "textSha256": "6baa1927023b118dacec14328f7b6124bfc19a6b81fd067ce23c4c443f3b400f",
    "textLength": 56,
    "resolvedSpans": [
      {
        "start": 0,
        "end": 2,
        "surface": "そこ",
        "role": "term",
        "headword": "そこ",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 2,
        "end": 4,
        "surface": "まで",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 4,
        "end": 7,
        "surface": "大きな",
        "role": "term",
        "headword": "大きな",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 7,
        "end": 8,
        "surface": "声",
        "role": "term",
        "headword": "声",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 8,
        "end": 14,
        "surface": "ではなかった",
        "role": "grammar",
        "headword": null,
        "grammarId": "NEGATIVE_COPULA_PAST",
        "confidence": 0.98,
        "sourceLayer": "grammar"
      },
      {
        "start": 14,
        "end": 17,
        "surface": "けれど",
        "role": "grammar",
        "headword": null,
        "grammarId": "KEREDO",
        "confidence": 0.95,
        "sourceLayer": "grammar"
      },
      {
        "start": 17,
        "end": 18,
        "surface": "、",
        "role": "punctuation",
        "headword": null,
        "grammarId": null,
        "confidence": 1.0,
        "sourceLayer": "orthography"
      },
      {
        "start": 18,
        "end": 20,
        "surface": "静か",
        "role": "term",
        "headword": "静か",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 20,
        "end": 21,
        "surface": "な",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 21,
        "end": 23,
        "surface": "覚悟",
        "role": "term",
        "headword": "覚悟",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 23,
        "end": 24,
        "surface": "を",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 24,
        "end": 26,
        "surface": "伴う",
        "role": "term",
        "headword": "伴う",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 26,
        "end": 28,
        "surface": "よう",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 28,
        "end": 29,
        "surface": "な",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 29,
        "end": 31,
        "surface": "強い",
        "role": "term",
        "headword": "強い",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 31,
        "end": 32,
        "surface": "声",
        "role": "term",
        "headword": "声",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 32,
        "end": 33,
        "surface": "は",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 33,
        "end": 34,
        "surface": "、",
        "role": "punctuation",
        "headword": null,
        "grammarId": null,
        "confidence": 1.0,
        "sourceLayer": "orthography"
      },
      {
        "start": 34,
        "end": 36,
        "surface": "この",
        "role": "term",
        "headword": "この",
        "grammarId": null,
        "confidence": 0.88,
        "sourceLayer": "lexical"
      },
      {
        "start": 36,
        "end": 37,
        "surface": "場",
        "role": "term",
        "headword": "場",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 37,
        "end": 38,
        "surface": "の",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 38,
        "end": 40,
        "surface": "鬱々",
        "role": "term",
        "headword": "鬱々",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 40,
        "end": 41,
        "surface": "と",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 41,
        "end": 42,
        "surface": "し",
        "role": "term",
        "headword": "する",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 42,
        "end": 43,
        "surface": "た",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 43,
        "end": 45,
        "surface": "空気",
        "role": "term",
        "headword": "空気",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 45,
        "end": 46,
        "surface": "を",
        "role": "particle",
        "headword": null,
        "grammarId": null,
        "confidence": 0.8,
        "sourceLayer": "morphology-fallback"
      },
      {
        "start": 46,
        "end": 50,
        "surface": "切り裂く",
        "role": "term",
        "headword": "切り裂く",
        "grammarId": null,
        "confidence": 0.84,
        "sourceLayer": "lexical"
      },
      {
        "start": 50,
        "end": 55,
        "surface": "ようだった",
        "role": "grammar",
        "headword": null,
        "grammarId": "YOU_DA_PAST",
        "confidence": 0.95,
        "sourceLayer": "grammar"
      },
      {
        "start": 55,
        "end": 56,
        "surface": "。",
        "role": "punctuation",
        "headword": null,
        "grammarId": null,
        "confidence": 1.0,
        "sourceLayer": "orthography"
      }
    ],
    "unresolvedSpans": [],
    "diagnostics": [],
    "kwjaAlignmentComplete": true,
    "dictionarySummary": {
      "ready": true,
      "candidateCount": 13,
      "matchedCandidateCount": 13,
      "unmatchedCandidateCount": 0,
      "typeEvidenceCounts": {
        "term": 357,
        "grammar": 11,
        "name": 7,
        "expression": 1
      }
    }
  }
]
````

### `JP analyzer/tests/test_correction_revision.py`

- Purpose: Teaching correction workflow.
- Size: 1703 bytes
- SHA-256: `9ded1b0095391a49a5d5737d198e6680789d992ef8cea2122e3eda19a8ca241d`

````python
from __future__ import annotations

from unittest.mock import patch

from app.analyzer import reader_corrections as corrections


def main() -> None:
    records = [
        {
            "correctionId": "b",
            "sentenceFingerprint": "sentence-2",
            "start": 1,
            "end": 2,
            "surface": "乙",
            "action": "mark-unresolved",
            "displayRole": "unresolved",
            "scope": "occurrence",
            "replacementReaderSpans": [],
        },
        {
            "correctionId": "a",
            "sentenceFingerprint": "sentence-1",
            "start": 0,
            "end": 1,
            "surface": "甲",
            "action": "show-as-one-unit",
            "displayRole": "lexical",
            "scope": "occurrence",
            "replacementReaderSpans": [
                {"start": 0, "end": 1, "surface": "甲"}
            ],
        },
    ]

    with patch.object(
        corrections,
        "list_corrections",
        return_value=records,
    ):
        first = corrections.correction_revision()

    with patch.object(
        corrections,
        "list_corrections",
        return_value=list(reversed(records)),
    ):
        assert corrections.correction_revision() == first

    changed = [dict(record) for record in records]
    changed[0]["displayRole"] = "function"

    with patch.object(
        corrections,
        "list_corrections",
        return_value=changed,
    ):
        assert corrections.correction_revision() != first

    assert len(first) == 64
    print("correction revision tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_decision.py`

- Purpose: Automated test or fixture.
- Size: 3205 bytes
- SHA-256: `96c88170c0390d2bd006c47a50b8d3b2e18c5857f3d76df421404167e54e781d`

````python
from app.analyzer.layers.decision import normalize_candidates, resolve_candidates


def base_analysis(text):
    return {
        "text": text,
        "morphemes": [],
        "orthographic_spans": [],
        "person_references": [],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [],
        "discourse_connectives_alpha321": [],
        "lexical_items_alpha32": [],
    }


def main():
    # Specific complete grammar must outrank internal dictionary-valid term.
    a = base_analysis("ならない")
    a["grammar_matches_alpha321"] = [{"id":"g1","start":0,"end":4,"surface":"ならない","grammar_id":"NAKEREBA_NARANAI","confidence":.98,"morpheme_ids":[]}]
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"なら","headword":"なる","lexical_type":"term","confidence":.9,"morpheme_ids":[]}]
    c = normalize_candidates(a, None)
    spans, decisions, conflicts = resolve_candidates(a["text"], c)
    assert spans[0]["surface"] == "ならない" and spans[0]["candidate_family"] == "grammar"

    # Complete person reference must outrank component term.
    a = base_analysis("綾子さん")
    a["person_references"] = [{"id":"p1","start":0,"end":4,"surface":"綾子さん","base_name":"綾子","confidence":.96,"morpheme_ids":["m0","m1"]}]
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"綾子","headword":"綾子","lexical_type":"term","confidence":.9,"morpheme_ids":["m0"]}]
    spans, _, _ = resolve_candidates(a["text"], normalize_candidates(a, None))
    assert spans[0]["surface"] == "綾子さん" and spans[0]["candidate_family"] == "proper-name"

    # Dictionary miss must not remove a morphology-backed term.
    a = base_analysis("未知語")
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":3,"surface":"未知語","headword":"未知語","lexical_type":"term","confidence":.84,"morpheme_ids":[]}]
    dictionary = {"evidence":[{"start":0,"end":3,"surface":"未知語","matched":False,"dictionary_type_counts":{},"source_names":[]}]}
    spans, decisions, _ = resolve_candidates(a["text"], normalize_candidates(a, dictionary))
    assert spans[0]["candidate_family"] == "term"
    assert "dictionary-corroboration" not in decisions[0]["decision_policies"]

    # Dictionary support strengthens but does not create a range.
    a = base_analysis("終え")
    a["lexical_items_alpha32"] = [{"id":"l1","start":0,"end":2,"surface":"終え","headword":"終える","lexical_type":"term","confidence":.84,"morpheme_ids":[]}]
    dictionary = {"evidence":[{"start":0,"end":2,"surface":"終え","matched":True,"confidence":.98,"dictionary_type_counts":{"term":4},"source_names":["A","B"],"matched_headwords":["終える"]}]}
    candidates = normalize_candidates(a, dictionary)
    term = next(x for x in candidates if x["candidate_family"] == "term")
    assert term["dictionary_evidence"]["matched"] is True
    spans, decisions, _ = resolve_candidates(a["text"], candidates)
    assert "dictionary-corroboration" in decisions[0]["decision_policies"]

    print("Alpha 3.4 resolver tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_dictionary_adapter.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 501 bytes
- SHA-256: `ad3f15c285dd0c3a185a623a03ffbf5e003326114f1e5cd63b7a0ba76db5d867`

````python
from app.analyzer.adapters.dictionary_adapter import DictionaryAdapter


def main():
    adapter = DictionaryAdapter()
    status = adapter.status()
    assert {"ready", "entryCount", "database"} <= set(status)
    result = adapter.evaluate_candidate({
        "id": "test", "start": 0, "end": 2, "surface": "検証"
    })
    assert result["candidate_id"] == "test"
    assert "matched" in result
    print("dictionary adapter tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_dictionary_evidence.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 4427 bytes
- SHA-256: `82c8a811096d4ebb08c9f85ef411a80d254d963037999d584ffa05261e0ce141`

````python
from __future__ import annotations

import tempfile
from pathlib import Path

from app.analyzer.layers import dictionary as evidence_module
from app.analyzer.layers import dictionary_store
from app.analyzer.layers.dictionary import (
    evaluate_analysis_candidates,
    evaluate_candidate,
)


def main():
    original_store_path = dictionary_store.DB_PATH
    original_evidence_path = evidence_module.DB_PATH
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            test_path = Path(tmp) / "lexicon.sqlite3"
            dictionary_store.DB_PATH = test_path
            # dictionary.py imports DB_PATH at module import, so update its test seam too.
            evidence_module.DB_PATH = test_path

            session = dictionary_store.start_sync(5, 4)
            entries = [
                {"term": "終える", "reading": "おえる", "dictionaryId": "d1", "dictionaryTitle": "Term A", "dictionaryType": "term", "dictionaryPriority": 10, "tags": ["v1", "vt"], "rules": ["v1"]},
                {"term": "終える", "reading": "おえる", "dictionaryId": "d2", "dictionaryTitle": "Term B", "dictionaryType": "term", "dictionaryPriority": 20, "tags": ["verb"]},
                {"term": "終える", "reading": "おえる", "dictionaryId": "d3", "dictionaryTitle": "Expression C", "dictionaryType": "expression", "dictionaryPriority": 30, "tags": ["exp"]},
                {"term": "らしい", "reading": "らしい", "dictionaryId": "g1", "dictionaryTitle": "Grammar", "dictionaryType": "grammar", "dictionaryPriority": 5, "grammarType": "evidential"},
                {"term": "美羽", "reading": "みう", "dictionaryId": "n1", "dictionaryTitle": "Names", "dictionaryType": "name", "dictionaryPriority": 5, "nameType": "given"},
            ]
            dictionary_store.add_batch(session["syncId"], entries)
            dictionary_store.finish_sync(session["syncId"])

            candidate = {
                "id": "adc0",
                "start": 3,
                "end": 5,
                "surface": "終え",
                "lookup_forms": ["終え", "終える"],
                "candidate_type": "lexical-proposal",
            }
            result = evaluate_candidate(candidate, "VERB")
            assert result["matched"] is True
            assert result["selected_lookup_form"] == "終える"
            assert result["entry_count"] == 3
            assert result["independent_source_count"] == 3
            assert result["dictionary_type_counts"] == {"term": 2, "expression": 1}
            assert result["pos_compatibility"]["status"] == "compatible"

            missing = evaluate_candidate(
                {
                    "id": "adc1",
                    "start": 0,
                    "end": 3,
                    "surface": "架空語",
                    "lookup_forms": ["架空語"],
                },
                "NOUN",
            )
            assert missing["matched"] is False
            assert "not a candidate rejection" in missing["meaning"]

            analysis = {
                "morphemes": [
                    {
                        "id": "m0",
                        "start": 3,
                        "end": 5,
                        "surface": "終え",
                        "lemma": "終える",
                        "pos": "VERB",
                    }
                ],
                "dictionary_candidates_alpha31": [candidate],
                "color_spans_alpha321": [
                    {
                        "start": 3,
                        "end": 5,
                        "surface": "終え",
                        "role": "term",
                        "headword": "終える",
                    }
                ],
            }
            before = repr(analysis)
            aggregate = evaluate_analysis_candidates(analysis)
            assert aggregate["matched_candidate_count"] == 1
            assert repr(analysis) == before, "Evidence evaluation mutated analysis"
            assert aggregate["contract"]["reader_projection_unchanged"] is True
    finally:
        dictionary_store.DB_PATH = original_store_path
        evidence_module.DB_PATH = original_evidence_path

    print("Dictionary evidence test passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_dictionary_path.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 459 bytes
- SHA-256: `c01ce0a324df703fcfc9d831e54e9763fd040cfc01a0a7b9908fb1bfe74890ec`

````python
from pathlib import Path
from app.analyzer.config import AnalyzerConfig
from app.analyzer.layers.dictionary_store import DB_PATH


def main():
    expected = Path(__file__).resolve().parents[1] / "data" / "phase8_analysis_lexicon.sqlite3"
    assert DB_PATH == expected, (DB_PATH, expected)
    assert AnalyzerConfig().dictionary_database == expected
    print("Consolidated dictionary path test passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_engine_routing.py`

- Purpose: Automated test or fixture.
- Size: 1648 bytes
- SHA-256: `46d8a3ba0856e1930d69e9e77a37532df7336dfc1cd701b9aba3bfa230a1d49b`

````python
from __future__ import annotations

from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine


class FakeRuntime:
    def __init__(self):
        self.nlp = object()
        self.calls = 0

    def get_nlp(self):
        self.calls += 1
        return self.nlp


def main():
    runtime = FakeRuntime()
    calls = []

    def legacy(text, nlp, **kwargs):
        calls.append((text, nlp, kwargs))
        return {
            "version": "9.0.0-alpha2.2-evidence-gated-decision",
            "text": text,
            "morphemes": [
                {"start": 0, "end": 2, "surface": "検証"},
                {"start": 2, "end": 3, "surface": "。"},
            ],
            "resolved_spans_alpha2": [
                {"start": 0, "end": 2, "surface": "検証", "role": "term"},
                {"start": 2, "end": 3, "surface": "。", "role": "punctuation"},
            ],
        }

    engine = AnalyzerEngine(runtime=runtime, analyzer_fn=legacy)
    result = engine.analyze_full(
        "検証。",
        options=AnalyzeOptions(use_dictionary=False, raw_knp="RAW"),
    )
    assert result["text"] == "検証。"
    assert runtime.calls == 1
    assert calls[0][1] is runtime.nlp
    assert calls[0][2] == {
        "use_dictionary": False,
        "raw_knp": "RAW",
        "kwja_executable": None,
    }

    supplied_nlp = object()
    engine.analyze_full("検証。", supplied_nlp)
    assert runtime.calls == 1
    assert calls[1][1] is supplied_nlp
    print("engine routing tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_evidence_routing.py`

- Purpose: Automated test or fixture.
- Size: 2021 bytes
- SHA-256: `c3c60f8d2f5e6ad85cc0812e70ffcfcfccc57cfb474eba7817f5f26992fb2c93`

````python
from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine


class FakeRuntime:
    config = object()
    nlp = object()

    def get_nlp(self):
        return self.nlp


class FakeKwja:
    def analyze(self, text, *, raw_knp=None, executable=None):
        return {"source": "stable-kwja"}


class FakeDictionary:
    def evaluate_analysis(self, analysis):
        return {"source": "stable-dictionary-analysis"}

    def evaluate_candidate(self, candidate, parser_pos=None):
        return {"source": "stable-dictionary-candidate"}


def main():
    calls = []

    def legacy(
        text, nlp, *, use_dictionary=True, raw_knp=None, kwja_executable=None,
        analyze_kwja_fn=None, evaluate_analysis_fn=None, evaluate_candidate_fn=None,
    ):
        kwargs = {
            "analyze_kwja_fn": analyze_kwja_fn,
            "evaluate_analysis_fn": evaluate_analysis_fn,
            "evaluate_candidate_fn": evaluate_candidate_fn,
        }
        calls.append(kwargs)
        assert kwargs["analyze_kwja_fn"]("x", raw_knp="RAW")["source"] == "stable-kwja"
        assert kwargs["evaluate_analysis_fn"]({})["source"] == "stable-dictionary-analysis"
        assert kwargs["evaluate_candidate_fn"]({})["source"] == "stable-dictionary-candidate"
        return {
            "version": "9.0.0-alpha2.2-evidence-gated-decision",
            "text": text,
            "morphemes": [{"start": 0, "end": 3, "surface": text}],
            "resolved_spans_alpha2": [
                {"start": 0, "end": 3, "surface": text, "role": "term"}
            ],
        }

    engine = AnalyzerEngine(
        runtime=FakeRuntime(),
        analyzer_fn=legacy,
        kwja_adapter=FakeKwja(),
        dictionary_adapter=FakeDictionary(),
    )
    engine.analyze_full("検証。", options=AnalyzeOptions(raw_knp="RAW"))
    assert len(calls) == 1
    print("evidence routing tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_facade.py`

- Purpose: Automated test or fixture.
- Size: 1531 bytes
- SHA-256: `67e0e55c67cd09b2a6c2b56f02b4b0f8ad5060bc7561fa6bf25d9530a8b72e46`

````python
from __future__ import annotations

from app.analyzer import pipeline
from app.analyzer.compact_output import compact_analysis
from app.analyzer.version import ANALYZER_VERSION


def main():
    sentinel = {
        "version": "9.0.0-alpha2.2-evidence-gated-decision",
        "text": "検証。",
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "検証", "role": "term"},
            {"start": 2, "end": 3, "surface": "。", "role": "punctuation"},
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {"final_projection_changed": False},
    }

    original = pipeline.analyze_layers
    try:
        pipeline.analyze_layers = lambda *args, **kwargs: sentinel
        full = pipeline.analyze_full("検証。", object())
        assert full is sentinel
        debug = pipeline.analyze("検証。", object(), debug=True)
        assert debug is sentinel
        compact = pipeline.analyze("検証。", object(), debug=False)
    finally:
        pipeline.analyze_layers = original

    assert compact == compact_analysis(sentinel, analyzer_version=ANALYZER_VERSION)
    assert compact["text"] == "検証。"
    assert compact["coverage"]["complete"] is True
    assert compact["coverage"]["unresolvedSpanCount"] == 0
    assert compact["coverage"]["kwjaAlignmentComplete"] is True
    print("stable facade tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_health_contract.py`

- Purpose: Automated test or fixture.
- Size: 810 bytes
- SHA-256: `4a0e13bd70ff165abd1a1b81bfe74bca51af6eab9379720e9154d5023e7bfec9`

````python
from app.analyzer.health import health_report
from app.analyzer.version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION


class FakeRuntime:
    class Status:
        ginza_model = "ja_ginza"
        kwja = {"available": True, "modelSize": "base"}
        dictionary = {"ready": True, "entryCount": 10}

    def status(self):
        return self.Status()


def main():
    result = health_report(FakeRuntime())
    assert result["status"] == "ok"
    assert result["version"] == ANALYZER_VERSION
    assert result["engineVersion"] == ENGINE_CONTRACT_VERSION
    assert result["ginzaModel"] == "ja_ginza"
    assert result["kwja"]["available"] is True
    assert result["dictionary"]["ready"] is True
    print("health contract tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_import_boundary.py`

- Purpose: Automated test or fixture.
- Size: 665 bytes
- SHA-256: `ad5693a212a9a78c18b79958686459bee1c3edcd6ea6141f533d994827e62082`

````python
from pathlib import Path


FORBIDDEN_IMPORT_PREFIXES = (
    "app." + "phase" + "8",
    "app." + "phase" + "9",
)


def main():
    package = Path(__file__).resolve().parents[1] / "app" / "analyzer"
    offenders = []
    for path in package.rglob("*.py"):
        text = path.read_text(encoding="utf-8-sig")
        if any(prefix in text for prefix in FORBIDDEN_IMPORT_PREFIXES):
            offenders.append(str(path.relative_to(package.parent.parent)))
    assert not offenders, f"Consolidated analyzer imports historical packages: {offenders}"
    print("Consolidated import-boundary test passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_kwja_adapter.py`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 537 bytes
- SHA-256: `e34c28992d459e0822498215f72b93fdb11697fb58efe61106cd32dac7eedd70`

````python
from app.analyzer.adapters.kwja_adapter import KwjaAdapter
from app.analyzer.config import AnalyzerConfig

RAW = """# S-ID:test kwja:2.5.1
* -1D
+ -1D <体言>
検証 けんしょう 検証 名詞 6 普通名詞 1 * 0 * 0
。 。 。 特殊 1 句点 1 * 0 * 0
EOS
"""


def main():
    result = KwjaAdapter(AnalyzerConfig()).analyze("検証。", raw_knp=RAW)
    assert result["kwja_metadata_alpha1"]["source_alignment_complete"] is True
    print("KWJA adapter tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_kwja_timeout.py`

- Purpose: KWJA runtime, evidence, or tests.
- Size: 1731 bytes
- SHA-256: `27aa587eb617d79d91197042d42e61bbee8d66b4c1d66275d70df6bc1b1d59d1`

````python
import inspect
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from app.analyzer.layers import kwja


class Completed:
    stdout = b"KNP"
    stderr = b""


def main():
    timeout = inspect.signature(kwja.run_kwja).parameters["timeout_seconds"].default
    assert timeout == 300, timeout

    captured = {}

    def fake_run(*args, **kwargs):
        captured.update(kwargs)
        return Completed()

    with tempfile.TemporaryDirectory() as tmp:
        executable = Path(tmp) / "kwja.exe"
        executable.write_bytes(b"")
        with patch.object(kwja.os, "environ", {}), patch.object(kwja.subprocess, "run", fake_run):
            output, _ = kwja.run_kwja("検証。", executable=str(executable))

    assert output == "KNP"
    env = captured["env"]
    assert env["PYTHONUTF8"] == "1"
    assert env["HF_HUB_OFFLINE"] == "1"
    assert env["TRANSFORMERS_OFFLINE"] == "1"
    assert env["HF_DATASETS_OFFLINE"] == "1"
    assert captured["timeout"] == 300

    explicit = {"HF_HUB_OFFLINE": "0", "TRANSFORMERS_OFFLINE": "0", "HF_DATASETS_OFFLINE": "0"}
    with tempfile.TemporaryDirectory() as tmp:
        executable = Path(tmp) / "kwja.exe"
        executable.write_bytes(b"")
        captured.clear()
        with patch.object(kwja.os, "environ", explicit), patch.object(kwja.subprocess, "run", fake_run):
            kwja.run_kwja("検証。", executable=str(executable))
    assert captured["env"]["HF_HUB_OFFLINE"] == "0"
    assert captured["env"]["TRANSFORMERS_OFFLINE"] == "0"
    assert captured["env"]["HF_DATASETS_OFFLINE"] == "0"
    print("KWJA runtime policy test passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_no_legacy_imports.py`

- Purpose: Automated test or fixture.
- Size: 705 bytes
- SHA-256: `1e62f41e2a4cbdbb3d6d9aaf622f7b3fd433b73a997aeb3c9556210adeafd58d`

````python
from pathlib import Path


FORBIDDEN_IMPORT_PREFIXES = (
    "app." + "phase" + "8",
    "app." + "phase" + "9",
)


def main():
    repository = Path(__file__).resolve().parents[1]
    offenders = []
    for directory in (repository / "app" / "analyzer", repository / "tests"):
        for path in directory.rglob("*.py"):
            text = path.read_text(encoding="utf-8-sig")
            if any(prefix in text for prefix in FORBIDDEN_IMPORT_PREFIXES):
                offenders.append(str(path.relative_to(repository)))
    assert not offenders, f"Historical package imports remain: {offenders}"
    print("No-legacy-import test passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_candidate_dictionary.py`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 4813 bytes
- SHA-256: `b4a11d9454e5d7816ae634637aed8ed9d4bf1eb627dce5a3347d2b4e96a6cb46`

````python
from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_dictionary import evaluate_reader_candidate_dictionary


def candidate():
    return {
        "candidateId": "reader-generated-test",
        "candidateSource": "reader-evidence-generator",
        "candidateFamily": "compound-predicate",
        "start": 0,
        "end": 5,
        "surface": "出て行った",
        "proposedRole": "lexical-compound",
        "possibleLookupKeys": ["出る", "行く"],
        "lookupHypotheses": [
            {"text":"出て行く","type":"complete-final-predicate-normalization","status":"generated","dictionaryStatus":"not-evaluated"},
            {"text":"出る","type":"component-or-lexical-headword","status":"generated","dictionaryStatus":"not-evaluated"},
            {"text":"行く","type":"component-or-lexical-headword","status":"generated","dictionaryStatus":"not-evaluated"},
        ],
        "preferredLookupKey": None,
        "features": {},
        "hardRejectionReasons": [],
        "selected": False,
        "selectionReason": None,
    }


def fake(request, parser_pos):
    form = request["surface"]
    matched = form in {"出て行く", "出る", "行く"}
    return {
        "matched": matched,
        "dictionary_ready": True,
        "match_type": "surface-exact" if matched else "none",
        "selected_lookup_form": form if matched else None,
        "selected_lookup_form_type": request["lookup_forms"][0]["type"] if matched else None,
        "entry_count": 1 if matched else 0,
        "independent_source_count": 1 if matched else 0,
        "dictionary_type_counts": {"term": 1} if matched else {},
        "matched_headwords": [form] if matched else [],
        "source_names": ["test"] if matched else [],
        "pos_compatibility": {"status":"compatible","parserPos":parser_pos},
        "confidence": .83 if matched else None,
        "lookup_attempts": [{"form":form,"form_type":"test","match_count":1 if matched else 0}],
        "entries": [{"definition":"must not leak"}],
    }


def main():
    analysis = {"morphemes":[{"start":0,"end":1,"pos":"VERB"},{"start":2,"end":4,"pos":"VERB"}]}
    original = candidate()
    evaluated = evaluate_reader_candidate_dictionary(analysis, original, fake)
    assert original["lookupHypotheses"][0]["dictionaryStatus"] == "not-evaluated"
    assert evaluated["dictionaryEvaluation"]["status"] == "evaluated"
    assert evaluated["dictionaryEvaluation"]["completeCandidateMatched"] is True
    assert evaluated["dictionaryEvaluation"]["componentOnlyMatched"] is False
    assert evaluated["dictionaryEvaluation"]["matchedCompleteLookupKeys"] == ["出て行く"]
    assert evaluated["dictionaryEvaluation"]["matchedComponentKeys"] == ["出る", "行く"]
    assert all(x["dictionaryStatus"] == "matched" for x in evaluated["lookupHypotheses"])
    assert "entries" not in evaluated["lookupHypotheses"][0]["dictionaryEvidence"]
    assert evaluated["preferredLookupKey"] is None and evaluated["selected"] is False

    component_only = candidate()
    def components(request, parser_pos):
        result = fake(request, parser_pos)
        if request["surface"] == "出て行く":
            result.update({"matched":False,"match_type":"none","selected_lookup_form":None,
                           "selected_lookup_form_type":None,"entry_count":0,
                           "independent_source_count":0,"dictionary_type_counts":{},
                           "matched_headwords":[],"source_names":[],"confidence":None})
        return result
    evaluated = evaluate_reader_candidate_dictionary(analysis, component_only, components)
    assert evaluated["dictionaryEvaluation"]["completeCandidateMatched"] is False
    assert evaluated["dictionaryEvaluation"]["componentOnlyMatched"] is True
    assert evaluated["lookupHypotheses"][0]["dictionaryStatus"] == "evaluated-no-match"
    assert evaluated["hardRejectionReasons"] == []

    def unavailable(request, parser_pos):
        return {"matched":False,"dictionary_ready":False,"match_type":"dictionary-not-ready",
                "entry_count":0,"independent_source_count":0,"dictionary_type_counts":{},
                "matched_headwords":[],"source_names":[],"pos_compatibility":{"status":"unknown"},
                "confidence":None,"lookup_attempts":[]}
    evaluated = evaluate_reader_candidate_dictionary(analysis, candidate(), unavailable)
    assert evaluated["dictionaryEvaluation"]["status"] == "dictionary-not-ready"
    assert all(x["dictionaryStatus"] == "dictionary-not-ready" for x in evaluated["lookupHypotheses"])

    print("reader candidate dictionary tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_candidate_evidence.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 4649 bytes
- SHA-256: `a306e0c75892a500de0f608481a65092f19e05744a56bc5b6a25de4f7a75c271`

````python
from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_evidence import attach_reader_candidate_structural_evidence


def candidate(surface="出て行った", complete=True):
    return {
        "candidateId":"rc-compound", "candidateSource":"reader-evidence-generator",
        "candidateFamily":"compound-predicate", "start":0, "end":len(surface),
        "surface":surface, "proposedRole":"lexical-compound", "possibleLookupKeys":["出る","行く"],
        "preferredLookupKey":None, "selected":False, "selectionReason":None,
        "dictionaryEvaluation":{
            "status":"evaluated", "completeCandidateMatched":complete,
            "componentOnlyMatched":not complete,
            "matchedCompleteLookupKeys":["出て行く"] if complete else [],
            "matchedComponentKeys":["出る","行く"],
        },
        "features":{}, "hardRejectionReasons":[],
    }


def analysis(surface="出て行った", relation="sequential-or-coordinate"):
    return {
        "text":surface,
        "morphemes":[
            {"id":"m0","start":0,"end":1,"surface":"出","pos":"VERB"},
            {"id":"m1","start":1,"end":2,"surface":"て","pos":"SCONJ"},
            {"id":"m2","start":2,"end":4,"surface":"行っ","pos":"VERB"},
            {"id":"m3","start":4,"end":5,"surface":"た","pos":"AUX"},
        ],
        "predicates":[
            {"id":"p0","start":0,"end":1,"surface":"出","headword":"出る"},
            {"id":"p1","start":2,"end":4,"surface":"行っ","headword":"行く"},
        ],
        "predicate_relations_alpha31":[
            {"id":"pr0","from_predicate_id":"p0","to_predicate_id":"p1","relation":relation}
        ],
        "grammar_matches_alpha321":[
            {"id":"g0","start":1,"end":2,"surface":"て","grammar_id":"V_TE"}
        ],
        "kwja_basic_phrases_alpha1":[
            {"id":"kb0","start":0,"end":5,"surface":surface}
        ],
        "kwja_predicate_phrases_alpha1":[
            {"id":"kp0","start":0,"end":5,"surface":surface}
        ],
    }


def main():
    original = candidate()
    evaluated = attach_reader_candidate_structural_evidence(analysis(), [original])
    item = evaluated[0]
    assert original.get("candidateStructuralEvidence") is None
    assert item["structuralEvidenceVersion"] == "1.0"
    assert item["candidateStructuralEvidence"]["morphology"]["sourceRangeContiguous"] is True
    assert item["candidateStructuralEvidence"]["morphology"]["interveningArgumentMaterial"] is False
    assert item["candidateStructuralEvidence"]["kwja"]["exactBasicPhrase"] is True
    assert item["candidateStructuralEvidence"]["kwja"]["exactPredicatePhrase"] is True
    assert item["candidateStructuralEvidence"]["predicates"]["predicateCount"] == 2
    assert item["candidateStructuralEvidence"]["predicates"]["independentOrSequentialActionConflict"] is True
    assert item["candidateStructuralEvidence"]["grammar"]["structuralGrammarIds"] == ["V_TE"]
    assert "multiple-independent-or-sequential-predicates" in item["abstentionReasons"]
    assert "complete-lookup-key-not-corroborated" not in item["abstentionReasons"]
    assert item["rankingStatus"] == "evidence-evaluated-unselected"
    assert item["selected"] is False and item["preferredLookupKey"] is None

    no_complete = attach_reader_candidate_structural_evidence(analysis(), [candidate(complete=False)])[0]
    assert "complete-lookup-key-not-corroborated" in no_complete["abstentionReasons"]
    assert no_complete["hardRejectionReasons"] == []

    with_argument = analysis("開けて空気を入れた")
    with_argument["morphemes"] = [
        {"id":"m0","start":0,"end":2,"surface":"開け","pos":"VERB"},
        {"id":"m1","start":2,"end":3,"surface":"て","pos":"SCONJ"},
        {"id":"m2","start":3,"end":5,"surface":"空気","pos":"NOUN"},
        {"id":"m3","start":5,"end":6,"surface":"を","pos":"ADP"},
        {"id":"m4","start":6,"end":8,"surface":"入れ","pos":"VERB"},
        {"id":"m5","start":8,"end":9,"surface":"た","pos":"AUX"},
    ]
    wide = candidate("開けて空気を入れた", complete=False)
    wide["end"] = 9
    wide["candidateId"] = "rc-wide"
    evidence = attach_reader_candidate_structural_evidence(with_argument, [wide])[0]
    assert evidence["candidateStructuralEvidence"]["morphology"]["interveningArgumentMaterial"] is True
    assert "intervening-argument-material" in evidence["abstentionReasons"]

    print("reader candidate structural evidence tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_candidate_generation.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 5498 bytes
- SHA-256: `704cff08ec89b8701beeea9e81f7690a2f80d127c044db50265f556ceffa26d9`

````python
from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def fixture():
    text = "頷いて、二人は出て行った。"
    return {
        "text": text,
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "頷い", "role": "term", "headword": "頷く", "confidence": .9, "selected_candidate_id": "c0"},
            {"start": 2, "end": 3, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .8, "selected_candidate_id": "c1"},
            {"start": 3, "end": 4, "surface": "、", "role": "punctuation", "confidence": 1, "selected_candidate_id": "c2"},
            {"start": 4, "end": 6, "surface": "二人", "role": "term", "headword": "二人", "confidence": .9, "selected_candidate_id": "c3"},
            {"start": 6, "end": 7, "surface": "は", "role": "particle", "confidence": .8, "selected_candidate_id": "c4"},
            {"start": 7, "end": 8, "surface": "出", "role": "term", "headword": "出る", "confidence": .9, "selected_candidate_id": "c5"},
            {"start": 8, "end": 9, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .8, "selected_candidate_id": "c6"},
            {"start": 9, "end": 11, "surface": "行っ", "role": "term", "headword": "行く", "confidence": .9, "selected_candidate_id": "c7"},
            {"start": 11, "end": 12, "surface": "た", "role": "particle", "confidence": .8, "selected_candidate_id": "c8"},
            {"start": 12, "end": 13, "surface": "。", "role": "punctuation", "confidence": 1, "selected_candidate_id": "c9"},
        ],
        "resolver_candidates_alpha2": [],
        "morphemes": [
            {"id": "m0", "start": 0, "end": 2, "surface": "頷い", "lemma": "頷く", "pos": "VERB"},
            {"id": "m1", "start": 2, "end": 3, "surface": "て", "lemma": "て", "pos": "SCONJ"},
            {"id": "m2", "start": 3, "end": 4, "surface": "、", "lemma": "、", "pos": "PUNCT"},
            {"id": "m3", "start": 4, "end": 5, "surface": "二", "lemma": "二", "pos": "NUM"},
            {"id": "m4", "start": 5, "end": 6, "surface": "人", "lemma": "人", "pos": "NOUN"},
            {"id": "m5", "start": 6, "end": 7, "surface": "は", "lemma": "は", "pos": "ADP"},
            {"id": "m6", "start": 7, "end": 8, "surface": "出", "lemma": "出る", "pos": "VERB"},
            {"id": "m7", "start": 8, "end": 9, "surface": "て", "lemma": "て", "pos": "SCONJ"},
            {"id": "m8", "start": 9, "end": 11, "surface": "行っ", "lemma": "行く", "pos": "VERB"},
            {"id": "m9", "start": 11, "end": 12, "surface": "た", "lemma": "た", "pos": "AUX"},
            {"id": "m10", "start": 12, "end": 13, "surface": "。", "lemma": "。", "pos": "PUNCT"},
        ],
        "predicates": [
            {"id": "p0", "start": 0, "end": 2, "surface": "頷い", "headword": "頷く"},
            {"id": "p1", "start": 7, "end": 8, "surface": "出", "headword": "出る"},
            {"id": "p2", "start": 9, "end": 11, "surface": "行っ", "headword": "行く"},
        ],
        "predicate_relations_alpha31": [
            {"id": "r0", "from_predicate_id": "p1", "to_predicate_id": "p2", "relation": "sequential-or-subordinate", "confidence": .82, "marker_range": {"start": 8, "end": 9, "surface": "て"}},
        ],
        "numeral_expressions_alpha32": [
            {"id": "n0", "start": 4, "end": 6, "surface": "二人", "morpheme_ids": ["m3", "m4"], "confidence": .96},
        ],
        "grammar_matches_alpha321": [
            {"id": "g0", "start": 2, "end": 3, "surface": "て", "grammar_id": "V_TE", "morpheme_ids": ["m1"], "confidence": .85},
        ],
        "kwja_basic_phrases_alpha1": [
            {"id": "kb0", "start": 0, "end": 3, "surface": "頷いて"},
            {"id": "kb1", "start": 7, "end": 12, "surface": "出て行った"},
        ],
        "kwja_predicate_phrases_alpha1": [
            {"id": "kp0", "start": 0, "end": 3, "surface": "頷いて"},
            {"id": "kp1", "start": 7, "end": 12, "surface": "出て行った"},
        ],
    }


def main():
    result = fixture()
    before_resolved = deepcopy(result["resolved_spans_alpha2"])
    before_reader = project_reader_spans(result)
    generated = generate_reader_candidates(result)

    assert result["resolved_spans_alpha2"] == before_resolved
    assert project_reader_spans(result) == before_reader
    assert all(x["selected"] is False for x in generated)
    assert any(x["surface"] == "頷いて" and x["candidateFamily"] == "inflected-lexical" for x in generated)
    assert any(x["surface"] == "二人" and x["candidateFamily"] == "term" and x["proposedRole"] == "lexical" for x in generated)
    assert all(x["candidateFamily"] != "numeric-lexical" and x["proposedRole"] != "numeric-lexical" for x in generated)
    compound = next(x for x in generated if x["surface"] == "出て行った" and x["candidateFamily"] == "compound-predicate")
    assert compound["conflictingEvidence"]
    assert compound["features"]["conflictingEvidenceCount"] > 0
    assert not compound["hardRejectionReasons"]
    assert all("、" not in x["surface"] and "。" not in x["surface"] for x in generated)
    print("reader candidate generation tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_candidate_safeguards.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 5471 bytes
- SHA-256: `e225623c8a99082e2325f8a2ded199ddb49206a087dd14fe9f82913f805ee866`

````python
from __future__ import annotations

from copy import deepcopy

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def base(text, spans, morphemes, predicates, relations, grammar=None):
    return {
        "text": text,
        "resolved_spans_alpha2": spans,
        "resolver_candidates_alpha2": [],
        "morphemes": morphemes,
        "predicates": predicates,
        "predicate_relations_alpha31": relations,
        "grammar_matches_alpha321": grammar or [],
        "numeral_expressions_alpha32": [],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def span(a, b, surface, role, headword=None, grammar_id=None, cid="x"):
    return {"start": a, "end": b, "surface": surface, "role": role, "headword": headword,
            "grammar_id": grammar_id, "confidence": .8, "selected_candidate_id": cid}


def main():
    # Valid contiguous VてV remains an unselected, component-key-only candidate.
    result = base(
        "出て行った。",
        [span(0,1,"出","term","出る",cid="c0"), span(1,2,"て","grammar",grammar_id="V_TE",cid="c1"),
         span(2,4,"行っ","term","行く",cid="c2"), span(4,5,"た","particle",cid="c3"), span(5,6,"。","punctuation",cid="c4")],
        [{"id":"m0","start":0,"end":1,"surface":"出","lemma":"出る","pos":"VERB"},
         {"id":"m1","start":1,"end":2,"surface":"て","lemma":"て","pos":"SCONJ"},
         {"id":"m2","start":2,"end":4,"surface":"行っ","lemma":"行く","pos":"VERB"},
         {"id":"m3","start":4,"end":5,"surface":"た","lemma":"た","pos":"AUX"},
         {"id":"m4","start":5,"end":6,"surface":"。","lemma":"。","pos":"PUNCT"}],
        [{"id":"p0","start":0,"end":1,"surface":"出","headword":"出る","head_morpheme_id":"m0","morpheme_ids":["m0"]},
         {"id":"p1","start":2,"end":4,"surface":"行っ","headword":"行く","head_morpheme_id":"m2","morpheme_ids":["m2"]}],
        [{"id":"r0","from_predicate_id":"p0","to_predicate_id":"p1","relation":"sequential-or-coordinate","confidence":.82,
          "marker_range":{"start":1,"end":2,"surface":"て"}}],
        [{"id":"g0","start":1,"end":2,"surface":"て","grammar_id":"V_TE","morpheme_ids":["m1"],"confidence":.85}],
    )
    before = deepcopy(project_reader_spans(result))
    candidates = generate_reader_candidates(result)
    compound = next(x for x in candidates if x["surface"] == "出て行った")
    assert compound["possibleLookupKeys"] == ["出る", "行く"]
    assert compound["preferredLookupKey"] is None
    assert compound["features"]["completeLookupKeyCorroborated"] is False
    assert compound["selected"] is False and compound["rankingEligible"] is True
    assert all(x.get("grammarId") != "V_TE" for x in candidates)
    assert project_reader_spans(result) == before

    # Intervening argument material blocks a lexical-compound proposal.
    separate = base(
        "開けて空気を入れた。",
        [],
        [{"id":"a0","start":0,"end":2,"surface":"開け","lemma":"開ける","pos":"VERB"},
         {"id":"a1","start":2,"end":3,"surface":"て","lemma":"て","pos":"SCONJ"},
         {"id":"a2","start":3,"end":5,"surface":"空気","lemma":"空気","pos":"NOUN"},
         {"id":"a3","start":5,"end":6,"surface":"を","lemma":"を","pos":"ADP"},
         {"id":"a4","start":6,"end":8,"surface":"入れ","lemma":"入れる","pos":"VERB"},
         {"id":"a5","start":8,"end":9,"surface":"た","lemma":"た","pos":"AUX"}],
        [{"id":"q0","start":0,"end":2,"surface":"開け","headword":"開ける","head_morpheme_id":"a0","morpheme_ids":["a0"]},
         {"id":"q1","start":6,"end":8,"surface":"入れ","headword":"入れる","head_morpheme_id":"a4","morpheme_ids":["a4"]}],
        [{"id":"rq","from_predicate_id":"q0","to_predicate_id":"q1","relation":"sequential-or-coordinate","confidence":.82,
          "marker_range":{"start":2,"end":3,"surface":"て"}}],
    )
    assert not any(x["candidateFamily"] == "compound-predicate" for x in generate_reader_candidates(separate))

    # Non-verbal predicate-like records and punctuation-crossing ranges are blocked.
    unsafe = base(
        "静かに、頷いた。",
        [],
        [{"id":"s0","start":0,"end":2,"surface":"静か","lemma":"静か","pos":"ADJ"},
         {"id":"s1","start":2,"end":3,"surface":"に","lemma":"だ","pos":"AUX"},
         {"id":"s2","start":3,"end":4,"surface":"、","lemma":"、","pos":"PUNCT"},
         {"id":"s3","start":4,"end":6,"surface":"頷い","lemma":"頷く","pos":"VERB"}],
        [{"id":"z0","start":0,"end":2,"surface":"静か","headword":"静か","head_morpheme_id":"s0","morpheme_ids":["s0"]},
         {"id":"z1","start":4,"end":6,"surface":"頷い","headword":"頷く","head_morpheme_id":"s3","morpheme_ids":["s3"]}],
        [{"id":"rz","from_predicate_id":"z0","to_predicate_id":"z1","relation":"direct-subordinate","confidence":.8}],
    )
    unsafe_candidates = generate_reader_candidates(unsafe)
    assert not any(x["candidateFamily"] == "compound-predicate" for x in unsafe_candidates)
    assert all(not x["hardRejectionReasons"] for x in unsafe_candidates)
    assert all("、" not in x["surface"] for x in unsafe_candidates)

    print("reader candidate safeguard tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_candidate_selection.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 4396 bytes
- SHA-256: `06e2ec5c9ec30e936cc03c25e4e6307074c8fec0529c4e1cb21574030a3c5edd`

````python
from __future__ import annotations

from app.analyzer.reader_candidate_selection import select_reader_output


def baseline(text="頷いて読んで寝た"):
    return {
        "text": text,
        "resolver_candidates_alpha2": [],
        "resolved_spans_alpha2": [
            {"start":0,"end":2,"surface":"頷い","role":"term","headword":"頷く","confidence":.9,"selected_candidate_id":"e0"},
            {"start":2,"end":3,"surface":"て","role":"particle","confidence":.8,"selected_candidate_id":"e1"},
            {"start":3,"end":5,"surface":"読ん","role":"term","headword":"読む","confidence":.9,"selected_candidate_id":"e2"},
            {"start":5,"end":6,"surface":"で","role":"particle","confidence":.8,"selected_candidate_id":"e3"},
            {"start":6,"end":7,"surface":"寝","role":"term","headword":"寝る","confidence":.9,"selected_candidate_id":"e4"},
            {"start":7,"end":8,"surface":"た","role":"particle","confidence":.8,"selected_candidate_id":"e5"},
        ],
    }


def structural(single=True, boundary=False, grammar=False, sequential=False):
    return {
        "morphology":{"sourceRangeContiguous":True,"interveningArgumentMaterial":False},
        "kwja":{"crossesBasicPhraseBoundary":boundary,"crossesPredicatePhraseBoundary":False},
        "predicates":{"singlePredicateInterpretation":single,"independentOrSequentialActionConflict":sequential},
        "grammar":{"completeLearnableGrammarConflict":grammar,"completeLearnableGrammarIds":[]},
        "competition":{"sameRangeCandidateIds":[]},
    }


def candidate(cid, start, end, surface, family, keys, dictionary, evidence):
    return {
        "candidateId":cid,"candidateSource":"reader-evidence-generator","start":start,"end":end,
        "surface":surface,"candidateFamily":family,"proposedRole":"lexical","possibleLookupKeys":keys,
        "preferredLookupKey":None,"selected":False,"hardRejectionReasons":[],
        "candidateStructuralEvidence":evidence,"dictionaryEvaluation":dictionary,"lookupHypotheses":[],
    }


def main():
    inflected = candidate("g0",0,3,"頷いて","inflected-lexical",["頷く"],{
        "status":"evaluated","matchedComponentKeys":["頷く"],"completeCandidateMatched":False
    }, structural())
    broad = candidate("g1",3,8,"読んで寝た","compound-predicate",["読む","寝る"],{
        "status":"evaluated","matchedCompleteLookupKeys":[],"matchedComponentKeys":["読む","寝る"],
        "completeCandidateMatched":False,"componentOnlyMatched":True
    }, structural(single=False,boundary=True,sequential=True))
    spans, candidates, selection = select_reader_output(baseline(), [inflected,broad])
    assert [x["surface"] for x in spans] == ["頷いて","読ん","で","寝","た"]
    assert spans[0]["knownLookupKey"] == "頷く"
    assert next(x for x in candidates if x["candidateId"]=="g0")["selected"] is True
    assert next(x for x in candidates if x["candidateId"]=="g1")["selected"] is False
    assert selection["selectedGeneratedCandidateCount"] == 1

    compound = candidate("g2",0,5,"出て行った","compound-predicate",["出る","行く"],{
        "status":"evaluated","matchedCompleteLookupKeys":["出て行く"],"matchedComponentKeys":["出る","行く"],
        "completeCandidateMatched":True,"componentOnlyMatched":False
    }, structural(single=False,sequential=True))
    source = baseline("出て行った")
    source["resolved_spans_alpha2"] = [
        {"start":0,"end":1,"surface":"出","role":"term","headword":"出る","confidence":.9,"selected_candidate_id":"a"},
        {"start":1,"end":2,"surface":"て","role":"particle","confidence":.8,"selected_candidate_id":"b"},
        {"start":2,"end":4,"surface":"行っ","role":"term","headword":"行く","confidence":.9,"selected_candidate_id":"c"},
        {"start":4,"end":5,"surface":"た","role":"particle","confidence":.8,"selected_candidate_id":"d"},
    ]
    spans, candidates, selection = select_reader_output(source,[compound])
    assert len(spans)==1 and spans[0]["surface"]=="出て行った"
    assert spans[0]["displayRole"]=="lexical-compound"
    assert spans[0]["knownLookupKey"]=="出て行く"
    assert selection["selectedGeneratedCandidateCount"]==1
    print("reader conservative selection tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_correction_compact_output.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 3224 bytes
- SHA-256: `a8146448ec96515f4dd7c8a568eed663524e5407755e71ec9b377ea6f2409b32`

````python
from __future__ import annotations

import tempfile
from pathlib import Path

import app.analyzer.reader_corrections as rc
from app.analyzer.compact_output import compact_analysis


def result_fixture():
    return {
        "text": "少年が走ってきた。",
        "version": "test-engine",
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "少年", "role": "term", "headword": "少年", "selected_candidate_id": "r0", "source_layer": "lexical"},
            {"start": 2, "end": 3, "surface": "が", "role": "particle", "selected_candidate_id": "r1", "source_layer": "morphology-fallback"},
            {"start": 3, "end": 5, "surface": "走っ", "role": "term", "headword": "走る", "selected_candidate_id": "r2", "source_layer": "lexical"},
            {"start": 5, "end": 8, "surface": "てきた", "role": "grammar", "grammar_id": "TE_KURU", "selected_candidate_id": "r3", "source_layer": "grammar"},
            {"start": 8, "end": 9, "surface": "。", "role": "punctuation", "selected_candidate_id": "r4", "source_layer": "orthography"},
        ],
        "resolver_candidates_alpha2": [
            {"candidate_id": "r0", "candidate_family": "term", "source_layer": "lexical"},
            {"candidate_id": "r1", "candidate_family": "particle", "source_layer": "morphology-fallback"},
            {"candidate_id": "r2", "candidate_family": "term", "source_layer": "lexical"},
            {"candidate_id": "r3", "candidate_family": "grammar", "source_layer": "grammar"},
            {"candidate_id": "r4", "candidate_family": "punctuation", "source_layer": "orthography"},
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {},
    }


def main():
    with tempfile.TemporaryDirectory() as directory:
        rc.DB_PATH = Path(directory) / "corrections.sqlite3"
        normal = compact_analysis(result_fixture(), analyzer_version="test")
        baseline = normal["readerSpans"]
        assert [item["surface"] for item in baseline] == ["少年", "が", "走っ", "てきた", "。"]

        rc.save(
            {
                "sentence": "少年が走ってきた。",
                "start": 3,
                "end": 8,
                "surface": "走ってきた",
                "action": "show-as-one-unit",
                "scope": "occurrence",
            },
            baseline,
            "test",
            "1.1",
        )
        corrected = compact_analysis(result_fixture(), analyzer_version="test")
        assert [item["surface"] for item in corrected["readerSpans"]] == ["少年", "が", "走ってきた", "。"]
        assert corrected["readerSpans"][2]["grammarId"] == "TE_KURU"
        assert corrected["readerSpans"][2]["hostLookupKey"] == "走る"
        assert corrected["readerSelection"]["appliedCorrectionCount"] == 1
        assert corrected["coverage"]["readerSpansComplete"] is True
        assert corrected["resolvedSpans"] == result_fixture()["resolved_spans_alpha2"]

    print("reader correction compact-output tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_corrections_backend.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 4347 bytes
- SHA-256: `686814e765c41cde1a54908fd380cfdce77f2f80ce393a551f57ce9f34b539f1`

````python
from __future__ import annotations

import tempfile
from pathlib import Path

import app.analyzer.reader_corrections as rc


def base_run():
    return [
        {
            "start": 0, "end": 2, "surface": "少年",
            "displayRole": "lexical", "knownLookupKey": "少年",
            "frequencyLookupKey": "少年", "headword": "少年",
        },
        {"start": 2, "end": 3, "surface": "が", "displayRole": "function"},
        {
            "start": 3, "end": 5, "surface": "走っ",
            "displayRole": "lexical", "knownLookupKey": "走る",
            "frequencyLookupKey": "走る", "headword": "走る",
        },
        {
            "start": 5, "end": 8, "surface": "てきた",
            "displayRole": "learnable-grammar", "grammarId": "TE_KURU",
        },
        {"start": 8, "end": 9, "surface": "。", "displayRole": "punctuation"},
    ]


def main():
    with tempfile.TemporaryDirectory() as directory:
        rc.DB_PATH = Path(directory) / "corrections.sqlite3"
        data = {
            "sentence": "少年が走ってきた。",
            "start": 3,
            "end": 8,
            "surface": "走ってきた",
            "action": "show-as-one-unit",
            "scope": "occurrence",
        }
        baseline = base_run()

        preview = rc.preview(data, baseline)
        assert preview["saved"] is False
        assert not rc.DB_PATH.exists()
        taught = preview["previewReaderSpans"][2]
        assert taught["surface"] == "走ってきた"
        assert taught["displayRole"] == "learnable-grammar"
        assert taught["grammarId"] == "TE_KURU"
        assert taught["hostLookupKey"] == "走る"
        assert taught["grammarFocusRanges"] == [
            {"start": 5, "end": 8, "surface": "てきた", "grammarId": "TE_KURU"}
        ]
        assert taught["knownLookupKey"] is None

        saved = rc.save(data, baseline, "test", "1.1")
        correction_id = saved["correctionId"]
        assert saved["saved"] is True
        rows = rc.list_corrections()
        assert len(rows) == 1
        assert rows[0]["known_lookup_key"] is None
        assert rows[0]["grammar_id"] == "TE_KURU"

        applied, provenance = rc.apply_active_corrections(data["sentence"], baseline)
        assert [item["surface"] for item in applied] == ["少年", "が", "走ってきた", "。"]
        assert applied[2]["projectionStatus"] == "user-corrected"
        assert applied[2]["correctionId"] == correction_id
        assert provenance[0]["action"] == "show-as-one-unit"

        other, other_provenance = rc.apply_active_corrections(
            "彼が走ってきた。",
            [
                {"start": 0, "end": 1, "surface": "彼", "displayRole": "lexical"},
                {"start": 1, "end": 2, "surface": "が", "displayRole": "function"},
                {"start": 2, "end": 4, "surface": "走っ", "displayRole": "lexical"},
                {"start": 4, "end": 7, "surface": "てきた", "displayRole": "learnable-grammar"},
                {"start": 7, "end": 8, "surface": "。", "displayRole": "punctuation"},
            ],
        )
        assert [item["surface"] for item in other] == ["彼", "が", "走っ", "てきた", "。"]
        assert other_provenance == []

        neutral = rc.preview(
            {
                "sentence": "少年が走ってきた。",
                "start": 3,
                "end": 8,
                "surface": "走ってきた",
                "action": "mark-unresolved",
                "scope": "occurrence",
            },
            baseline,
        )
        assert neutral["previewReaderSpans"][2]["displayRole"] == "unresolved"
        assert neutral["previewReaderSpans"][2]["colorPolicy"] == "neutral"

        rc.deactivate(correction_id)
        restored, restored_provenance = rc.apply_active_corrections(data["sentence"], baseline)
        assert [item["surface"] for item in restored] == ["少年", "が", "走っ", "てきた", "。"]
        assert restored_provenance == []
        assert rc.list_corrections() == []
        assert len(rc.list_corrections(True)) == 1

    print("reader structural teaching backend tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_lookup_hypotheses.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 3449 bytes
- SHA-256: `21421bc2497fe1b77d9f0757925eda8bf7c258e9a0ed78280c6b62144915ad68`

````python
from __future__ import annotations

from app.analyzer.reader_candidate_generation import generate_reader_candidates


def fixture(surface, first_surface, first_lemma, second_surface, second_lemma, trailing_surface):
    first_start = 0
    first_end = len(first_surface)
    second_start = first_end
    second_end = second_start + len(second_surface)
    trailing_end = second_end + len(trailing_surface)
    return {
        "text": surface,
        "resolved_spans_alpha2": [],
        "resolver_candidates_alpha2": [],
        "morphemes": [
            {"id":"m0","start":first_start,"end":first_end,"surface":first_surface,"lemma":first_lemma,"pos":"VERB"},
            {"id":"m1","start":second_start,"end":second_end,"surface":second_surface,"lemma":second_lemma,"pos":"VERB"},
            {"id":"m2","start":second_end,"end":trailing_end,"surface":trailing_surface,"lemma":"た","pos":"AUX"},
        ],
        "predicates": [
            {"id":"p0","start":first_start,"end":first_end,"surface":first_surface,"headword":first_lemma,"head_morpheme_id":"m0","morpheme_ids":["m0"]},
            {"id":"p1","start":second_start,"end":second_end,"surface":second_surface,"headword":second_lemma,"head_morpheme_id":"m1","morpheme_ids":["m1"]},
        ],
        "predicate_relations_alpha31": [
            {"id":"r0","from_predicate_id":"p0","to_predicate_id":"p1","relation":"direct-compound","confidence":.82},
        ],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def complete_hypothesis(candidate):
    return next(
        item for item in candidate["lookupHypotheses"]
        if item["type"] == "complete-final-predicate-normalization"
    )


def main():
    cases = [
        ("出て行った", "出て", "出る", "行っ", "行く", "た", "出て行く"),
        ("読み終わった", "読み", "読む", "終わっ", "終わる", "た", "読み終わる"),
        ("走り出した", "走り", "走る", "出し", "出す", "た", "走り出す"),
        ("読んで寝た", "読んで", "読む", "寝", "寝る", "た", "読んで寝る"),
    ]
    forbidden = {"読みて終わる", "走りて出す", "読んて寝る"}
    for surface, first_surface, first_lemma, second_surface, second_lemma, trailing, expected in cases:
        generated = generate_reader_candidates(
            fixture(surface, first_surface, first_lemma, second_surface, second_lemma, trailing)
        )
        compound = next(x for x in generated if x["candidateFamily"] == "compound-predicate")
        hypothesis = complete_hypothesis(compound)
        assert hypothesis["text"] == expected
        assert hypothesis["status"] == "generated"
        assert hypothesis["dictionaryStatus"] == "not-evaluated"
        assert hypothesis["generationSource"] == "candidate-final-predicate"
        assert compound["preferredLookupKey"] is None
        assert compound["selected"] is False
        assert compound["features"]["completeLookupHypothesisGenerated"] is True
        assert compound["features"]["completeLookupHypothesisStatus"] == "not-evaluated"
        assert not forbidden.intersection(x["text"] for x in compound["lookupHypotheses"])

    print("reader lookup hypothesis tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_numeric_terms.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 4274 bytes
- SHA-256: `ef905e2733a2f55f2b84428ffa9d0dc20e33c478257fecd4237ca56c0f8e6dcd`

````python
from __future__ import annotations

from app.analyzer.reader_candidate_generation import generate_reader_candidates
from app.analyzer.reader_projection import project_reader_spans


def analysis(text: str, start: int, end: int, morphemes: list[dict], value: str, counter: str | None):
    return {
        "text": text,
        "resolved_spans_alpha2": [],
        "resolver_candidates_alpha2": [],
        "morphemes": morphemes,
        "predicates": [],
        "predicate_relations_alpha31": [],
        "grammar_matches_alpha321": [],
        "numeral_expressions_alpha32": [{
            "id": "num0", "start": start, "end": end, "surface": text[start:end],
            "value_surface": value, "counter_surface": counter,
            "morpheme_ids": [m["id"] for m in morphemes], "confidence": .96,
        }],
        "kwja_basic_phrases_alpha1": [],
        "kwja_predicate_phrases_alpha1": [],
    }


def main():
    cases = [
        ("二人", [{"id":"m0","start":0,"end":1,"surface":"二","lemma":"二","pos":"NUM"}, {"id":"m1","start":1,"end":2,"surface":"人","lemma":"人","pos":"NOUN"}], "二", "人"),
        ("十歳", [{"id":"m0","start":0,"end":1,"surface":"十","lemma":"十","pos":"NUM"}, {"id":"m1","start":1,"end":2,"surface":"歳","lemma":"歳","pos":"NOUN"}], "十", "歳"),
        ("二十歳", [{"id":"m0","start":0,"end":2,"surface":"二十","lemma":"二十","pos":"NUM"}, {"id":"m1","start":2,"end":3,"surface":"歳","lemma":"歳","pos":"NOUN"}], "二十", "歳"),
    ]
    for text, morphemes, value, counter in cases:
        candidates = generate_reader_candidates(analysis(text, 0, len(text), morphemes, value, counter))
        candidate = next(x for x in candidates if x["surface"] == text)
        assert candidate["candidateFamily"] == "term"
        assert candidate["proposedRole"] == "lexical"
        assert candidate["features"]["containsNumeral"] is True
        assert candidate["features"]["numericExpressionSupported"] is True
        assert candidate["features"]["numericEvidenceOnly"] is True
        assert candidate["numericEvidence"]["counterSurface"] == counter
        assert candidate["possibleLookupKeys"] == [text]
        assert candidate["preferredLookupKey"] is None
        assert candidate["selected"] is False
        assert candidate["rankingStatus"].startswith("unscored")
        assert all(x["candidateFamily"] != "numeric-lexical" for x in candidates)
        assert all(x["proposedRole"] != "numeric-lexical" for x in candidates)
        compatibility_result = {
        "text": "十歳",
        "resolver_candidates_alpha2": [
            {
                "candidate_id": "a34c0",
                "candidate_family": "numeral",
                "source_annotation_id": "num0",
                "source_layer": "numeral",
            }
        ],
        "resolved_spans_alpha2": [
            {
                "start": 0,
                "end": 2,
                "surface": "十歳",
                "role": "term",
                "headword": "十歳",
                "grammar_id": None,
                "confidence": 0.96,
                "selected_candidate_id": "a34c0",
                "source_layer": "numeral",
            }
        ],
    }

    projected = project_reader_spans(
        compatibility_result
    )

    assert projected == [
        {
            "start": 0,
            "end": 2,
            "surface": "十歳",
            "displayRole": "lexical",
            "lexicalType": "term",
            "colorPolicy": "known-or-frequency",
            "unknownColorPolicy": "frequency",
            "knownLookupKey": "十歳",
            "frequencyLookupKey": "十歳",
            "countsForComprehension": True,
            "showInNewWords": True,
            "eligibleForMining": True,
            "headword": "十歳",
            "grammarId": None,
            "confidence": 0.96,
            "sourceSpanIds": [
                "a34c0",
                "num0",
            ],
            "sourceLayer": "numeral",
            "projectionStatus": "compatibility",
        }
    ]
    print("reader numeric term tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_reader_projection_contract.py`

- Purpose: Reader contract, rendering, or UI.
- Size: 3559 bytes
- SHA-256: `fff5baa30b9f05d074c1387346972b2b71125745be8f92b65aae51d3dbe58d23`

````python
from __future__ import annotations

from app.analyzer.compact_output import compact_analysis
from app.analyzer.reader_projection import validate_reader_spans
from app.analyzer.version import ANALYZER_VERSION


def _candidate(candidate_id, family, source_layer="test"):
    return {
        "candidate_id": candidate_id,
        "candidate_family": family,
        "source_layer": source_layer,
    }


def main():
    text = "二人はとばかりに頷いて。"
    result = {
        "version": "9.0.0-alpha2.2-evidence-gated-decision",
        "text": text,
        "resolved_spans_alpha2": [
            {"start": 0, "end": 2, "surface": "二人", "role": "term", "headword": "二人", "confidence": .9, "selected_candidate_id": "num"},
            {"start": 2, "end": 3, "surface": "は", "role": "particle", "headword": None, "confidence": .8, "selected_candidate_id": "particle"},
            {"start": 3, "end": 8, "surface": "とばかりに", "role": "grammar", "grammar_id": "TO_BAKARI_NI", "confidence": .96, "selected_candidate_id": "grammar"},
            {"start": 8, "end": 10, "surface": "頷い", "role": "term", "headword": "頷く", "confidence": .9, "selected_candidate_id": "term"},
            {"start": 10, "end": 11, "surface": "て", "role": "grammar", "grammar_id": "V_TE", "confidence": .85, "selected_candidate_id": "te"},
            {"start": 11, "end": 12, "surface": "。", "role": "punctuation", "confidence": 1.0, "selected_candidate_id": "punct"},
        ],
        "resolver_candidates_alpha2": [
            _candidate("num", "numeral"),
            _candidate("particle", "particle"),
            _candidate("grammar", "grammar"),
            _candidate("term", "term"),
            _candidate("te", "grammar"),
            _candidate("punct", "punctuation"),
        ],
        "diagnostics_alpha2": [],
        "kwja_metadata_alpha1": {"source_alignment_complete": True},
        "alpha2_change_summary": {},
    }

    compact = compact_analysis(result, analyzer_version=ANALYZER_VERSION)
    spans = compact["readerSpans"]
    validate_reader_spans(text, spans)

    assert compact["schemaVersion"] == "1.2"
    assert compact["readerSpanSchemaVersion"] == "1.1"

    assert compact["readerCandidateSchemaVersion"] == "2.0"
    assert isinstance(compact["readerCandidates"], list)
    assert compact["resolvedSpans"] is result["resolved_spans_alpha2"]
    assert compact["coverage"]["readerSpansComplete"] is True

    numeric, function, grammar, lexical, te_function, punctuation = spans
    assert numeric["displayRole"] == "lexical"
    assert numeric["lexicalType"] == "term"
    assert numeric["colorPolicy"] == "known-or-frequency"
    assert numeric["unknownColorPolicy"] == "frequency"
    assert function["displayRole"] == "function"
    assert function["colorPolicy"] == "muted"
    assert grammar["displayRole"] == "learnable-grammar"
    assert grammar["grammarId"] == "TO_BAKARI_NI"
    assert lexical["displayRole"] == "lexical"
    assert lexical["knownLookupKey"] == "頷く"
    assert te_function["displayRole"] == "function"
    assert punctuation["displayRole"] == "punctuation"

    broken = [dict(item) for item in spans]
    broken[1]["start"] = 1
    try:
        validate_reader_spans(text, broken)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid reader span partition was accepted")

    print("readerSpans contract tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_runtime_contracts.py`

- Purpose: Automated test or fixture.
- Size: 957 bytes
- SHA-256: `6c1b501f0385e95b1b7e241f5c10641bb1572fa93ee120cd910db2a375c6cdab`

````python
from pathlib import Path
from app.analyzer.config import AnalyzerConfig
from app.analyzer.kwja_runtime import kwja_status
from app.analyzer.source_contract import validate_analysis_source

def main():
    cfg = AnalyzerConfig(kwja_executable=Path("missing-kwja.exe"))
    assert not cfg.kwja_available() and not kwja_status(cfg)["available"]
    valid = {"text":"検証。", "morphemes":[{"start":0,"end":2,"surface":"検証"},{"start":2,"end":3,"surface":"。"}], "resolved_spans_alpha2":[{"start":0,"end":2,"surface":"検証"},{"start":2,"end":3,"surface":"。"}]}
    assert validate_analysis_source(valid) == []
    invalid = dict(valid); invalid["resolved_spans_alpha2"] = [{"start":0,"end":2,"surface":"誤り"}]
    codes = {x["code"] for x in validate_analysis_source(invalid)}
    assert {"SOURCE_SURFACE_MISMATCH", "SOURCE_PARTITION_INCOMPLETE"} <= codes
    print("runtime contract tests passed")
if __name__ == "__main__": main()
````

### `JP analyzer/tests/test_runtime_reuse.py`

- Purpose: Automated test or fixture.
- Size: 601 bytes
- SHA-256: `90ae6a8ee49d3218a9d085c1a673294a4ce4125df41554d97fd6114ae99d3e0a`

````python
from app.analyzer.config import AnalyzerConfig
from app.analyzer.runtime import get_runtime, reset_runtime_for_tests


def main():
    reset_runtime_for_tests()
    config = AnalyzerConfig()
    first = get_runtime(config)
    second = get_runtime()
    assert first is second
    try:
        get_runtime(AnalyzerConfig(ginza_split_mode="C"))
    except RuntimeError:
        pass
    else:
        raise AssertionError("Runtime accepted a conflicting configuration")
    reset_runtime_for_tests()
    print("runtime reuse tests passed")


if __name__ == "__main__":
    main()
````

### `JP analyzer/tests/test_semantic_snapshot.py`

- Purpose: Automated test or fixture.
- Size: 1097 bytes
- SHA-256: `eaf526c3c3998edf88128f048801230de844fbcf6f3a16fac5382a07da95d2f7`

````python
from copy import deepcopy
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest

def main():
    base = {"text":"検証。", "resolved_spans_alpha2":[{"start":0,"end":2,"surface":"検証","role":"term","headword":"検証","confidence":.9},{"start":2,"end":3,"surface":"。","role":"punctuation","confidence":1.0}], "diagnostics_alpha2":[], "kwja_metadata_alpha1":{"source_alignment_complete":True,"elapsed_ms":123}, "dictionary_evidence_alpha34":{"dictionary_ready":True,"candidate_count":1,"matched_candidate_count":1,"unmatched_candidate_count":0}, "runtimeElapsedMs":10}
    changed = deepcopy(base); changed["runtimeElapsedMs"] = 999; changed["kwja_metadata_alpha1"]["elapsed_ms"] = 777
    assert semantic_snapshot(base) == semantic_snapshot(changed)
    assert snapshot_digest(semantic_snapshot(base)) == snapshot_digest(semantic_snapshot(changed))
    changed["resolved_spans_alpha2"][0]["role"] = "unresolved"
    assert semantic_snapshot(base) != semantic_snapshot(changed)
    print("semantic snapshot tests passed")
if __name__ == "__main__": main()
````

### `JP analyzer/tests/test_single_pass.py`

- Purpose: Automated test or fixture.
- Size: 771 bytes
- SHA-256: `535c46e5dd5a03b3ae6e04b3610259bbe68761fe7f9ef20c77ad1607ecd32a7f`

````python
from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine

class Runtime:
    config = None
    services = None
    def get_nlp(self): return object()

def main():
    calls = {"engine": 0}
    def layer_engine(text, nlp, **kwargs):
        calls["engine"] += 1
        return {"version":"9.0.0-alpha2.2-evidence-gated-decision","text":text,"morphemes":[{"start":0,"end":1,"surface":text}],"resolved_spans_alpha2":[{"start":0,"end":1,"surface":text,"role":"term"}]}
    engine = AnalyzerEngine(runtime=Runtime(), analyzer_fn=layer_engine)
    engine.analyze_full("検", options=AnalyzeOptions())
    assert calls["engine"] == 1
    print("Consolidated single-pass test passed")

if __name__ == "__main__": main()
````


### Repository B — Novel Audio Miner

### `novel-audio-miner/.gitattributes`

- Purpose: Project source or support file.
- Size: 495 bytes
- SHA-256: `39c7511572246661bf73790ae3658d61e73e77623a5e08cd463ad402e466b0f8`

````text
# Normalize text files in Git
* text=auto

# Web and configuration source
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.json text eol=lf
*.html text eol=lf
*.css text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

# Windows command files
*.ps1 text eol=crlf
*.cmd text eol=crlf
*.bat text eol=crlf

# Binary assets
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.woff binary
*.woff2 binary
*.ttf binary
*.zip binary
````

### `novel-audio-miner/.gitignore`

- Purpose: Project source or support file.
- Size: 1641 bytes
- SHA-256: `2523690971b97378a0438892b75233178330006644d668bf4e272de8386c79e3`

````text
# ============================================================
# Node dependencies and generated builds
# ============================================================

node_modules/
dist/
build/
coverage/
.vite/
.next/

# ============================================================
# Large local dictionary and frequency data
# ============================================================

public/dict/*.json

# Keep small seed/config files if they exist
!public/dict/user_dictionary_seed.json

# ============================================================
# Generated application data
# ============================================================

*.log
logs/
*.tmp
*.temp

# ============================================================
# Temporary development artifacts
# ============================================================

*_inventory.txt
*_current_source.txt
*_source_bundle.txt
*_debug.json
npm_dependency_snapshot.json

*.bak
*.backup
*.orig

# One-time patching and cleanup files
apply_*.py
patch_*.py
cleanup_*.ps1
restore_*.ps1
delete_*.ps1

# ============================================================
# Local configuration and secrets
# ============================================================

.env
.env.*
!.env.example

# ============================================================
# Editors and operating-system files
# ============================================================

.vscode/
.idea/
*.code-workspace
.DS_Store
Thumbs.db
desktop.ini

# ============================================================
# Archives
# ============================================================

*.zip
*.7z
*.rar
````

### `novel-audio-miner/docs/ANALYZER_INTEGRATION_CONTRACT.md`

- Purpose: Documentation.
- Size: 659 bytes
- SHA-256: `31ea9b689bb25a99b47e209fda178f5d5afd521ac068a68a29843a65894bbdbc`

````markdown
# Novel Audio Miner Analyzer Integration Contract

JP Analyzer is the sole owner of Japanese linguistic boundaries, roles, lookup identities and learning/mining eligibility. Novel Audio Miner owns EPUB parsing, rendering, known/frequency lookup, aggregation, UI and integrations.

Novel Audio Miner must not merge or split analyzer spans, infer grammar/names/compounds, derive lookup identities, or use surface search when authoritative offsets exist. Invalid analyzer output is rendered as neutral text.

Kuromoji and the legacy tokenizer model were retired in Phase 5.2E. Plain Text is a presentation mode and continues to use JP Analyzer structure.
````

### `novel-audio-miner/FINAL_STABLE_STATUS.md`

- Purpose: Documentation.
- Size: 2863 bytes
- SHA-256: `1ac1fbfb34f027183dc60c67dad212f3957b5d0dd2c9ed855785838a5a4b4edc`

````markdown
# Final Stable Core Status

## Version

```text
Novel Audio Miner v4.1 Stable Core
```

## Status

```text
Stable cleanup complete.
Ready for Debug Mode / Token Inspector foundation.
```

## Purpose of this stable baseline

This baseline exists to provide a clean, efficient, formalized, and predictable app state before adding Debug Mode.

The stable baseline intentionally avoids risky feature changes and removes/deactivates unfinished experimental logic.

## Completed cleanup scope

Cleanup Patches 1-22 completed the following stabilization work:

```text
- Removed deferred composite-known runtime logic.
- Removed unused imports and unused helper exports.
- Removed obsolete content-word filtering from tokenizer.js.
- Formalized tokenizer responsibility.
- Formalized word model responsibility.
- Formalized known-word cache/storage responsibility.
- Formalized reader-progress storage responsibility.
- Formalized EPUB parser responsibility.
- Formalized AnkiConnect responsibility.
- Formalized Nadeshiko/VOICEVOX enrichment responsibility.
- Formalized frequency-map responsibility.
- Removed normal-operation console noise.
- Removed unused/no-op CSS.
- Removed/reclassified unused sentence grouping code as deferred.
- Removed hard page reload for Load another book.
- Updated package metadata and exact dependency versions.
- Added project documentation and release checklist.
```

## Stable behavior expected

The stable app should support:

```text
- EPUB upload and parsing.
- Sentence/image reading stream.
- Vertical and horizontal reading modes.
- Furigana ON/OFF.
- Stable word coloring.
- Frequency-based unknown word colors.
- Proper noun/name coloring and exclusion.
- Grammar/function-token exclusion.
- Numeric/counter expression grouping.
- Comprehension percentage.
- New Words list.
- Manual Mark Known.
- Undo Known.
- Persistent manual-known database.
- Anki known-word cache.
- Clear/Rebuild Anki cache while preserving manual-known words.
- Latest Kiku note update.
- Nadeshiko enrichment.
- VOICEVOX fallback / Force TTS.
```

## Deferred intentionally

The following are intentionally not part of this stable runtime yet:

```text
- Broad compound-word merging.
- Composite-known logic.
- Click-to-select token spans.
- Sentence grouping rewrite.
- EPUB image-order diagnostics.
- Parser debug export.
- Token Inspector.
- Full Debug Mode.
```

## Reason for deferral

These features depend on hidden tokenizer/parser state. Adding them without diagnostics created instability earlier, especially around compound words such as:

```text
交通事故
響き渡る
現実的
精一杯
一瞬間
```

The next changes should therefore expose diagnostics first instead of adding more guessing rules.

## Final recommendation

After final release checklist passes:

```text
Stop stable cleanup.
Start Phase 3A: Token Inspector.
```
````

### `novel-audio-miner/index.html`

- Purpose: Project source or support file.
- Size: 413 bytes
- SHA-256: `755b0049db5826b6b77e22bcf3c129f5ffe1ab0c2a55ff8411d99999d18bdabd`

````html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta
      name="description"
      content="Local Japanese EPUB reader and Anki mining helper."
    />
    <title>Novel Audio Miner</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
````

### `novel-audio-miner/LOCAL_DATA_MANIFEST.example.json`

- Purpose: Project source or support file.
- Size: 397 bytes
- SHA-256: `6857a0d0f03ddb6470cbf91ec80b422afab795503c6579585ffde310745b8e6c`

````json
[
    {
        "Name":  "bccwj.json",
        "Length":  81306805
    },
    {
        "Name":  "cc100.json",
        "Length":  11671168
    },
    {
        "Name":  "jiten.json",
        "Length":  54632568
    },
    {
        "Name":  "jpdb.json",
        "Length":  31488509
    },
    {
        "Name":  "user_dictionary_seed.json",
        "Length":  798
    }
]
````

### `novel-audio-miner/package-lock.json`

- Purpose: Node dependency and script configuration.
- Size: 34500 bytes
- SHA-256: `a08886d11b538d77d6e14a16e230a90bea29e70ebfe4257d8830fb12e0313915`

````json
{
  "name": "novel-audio-miner",
  "version": "4.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "novel-audio-miner",
      "version": "4.1.0",
      "dependencies": {
        "@vitejs/plugin-react": "6.0.3",
        "jszip": "3.10.1",
        "react": "19.2.7",
        "react-dom": "19.2.7",
        "vite": "8.1.3"
      }
    },
    "node_modules/@emnapi/core": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@emnapi/core/-/core-1.11.1.tgz",
      "integrity": "sha512-RSvbQmHzdKzNsLYa/wHrbc3KN4sYLKAdPZxqiM2HATqv/SBk2/ENSHpvXGaLOMcsAyz0poEGqkmmKYG3OWiJEQ==",
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/wasi-threads": "1.2.2",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/runtime": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@emnapi/runtime/-/runtime-1.11.1.tgz",
      "integrity": "sha512-vgj7R3y3Wgx24IQaGPA/R6YFXLHVMOZ0uVEyIQPaWs+rd1AzfEMXlAC22FYwO1XkKR6NPsq7mUandH8oIRdZFw==",
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/wasi-threads": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/@emnapi/wasi-threads/-/wasi-threads-1.2.2.tgz",
      "integrity": "sha512-c95qOXkHdydNKhscBTebqEC1CVAZpyqOfVfBzQ1qgzyl3gfeldUjIggDbIZgDKsHLgnsM+igH7TJ/eAasaVuMA==",
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@napi-rs/wasm-runtime": {
      "version": "1.1.6",
      "resolved": "https://registry.npmjs.org/@napi-rs/wasm-runtime/-/wasm-runtime-1.1.6.tgz",
      "integrity": "sha512-ZLv/JdUfkvOy9eCnnBaGfiO+XimbjebAeO+MRQqD/B+FR1tnRN0tpKSJHRbE8sFfS6aqsXZ67TQjfwfsxULVbg==",
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@tybys/wasm-util": "^0.10.3"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/Brooooooklyn"
      },
      "peerDependencies": {
        "@emnapi/core": "^1.7.1",
        "@emnapi/runtime": "^1.7.1"
      }
    },
    "node_modules/@oxc-project/types": {
      "version": "0.138.0",
      "resolved": "https://registry.npmjs.org/@oxc-project/types/-/types-0.138.0.tgz",
      "integrity": "sha512-1a7ZKmrRTCoN1XMZ4L0PyyqrMnrNlLyPuOkdSX2MZg7IiIGRUyurNhAm73ptDOraoBcIordsIGKNPKUzy3ZmfA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/Boshen"
      }
    },
    "node_modules/@rolldown/binding-android-arm64": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-android-arm64/-/binding-android-arm64-1.1.4.tgz",
      "integrity": "sha512-EZLpf/8y7GXkkra90ML47kzik/GMP3EMcE9bPyHmRfxLC6z9+aW5A8poCsoxjrT5GfEcNAAvWwUHjvP1pUQkfw==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-darwin-arm64": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-darwin-arm64/-/binding-darwin-arm64-1.1.4.tgz",
      "integrity": "sha512-aUi+HBvmYb7j8krl1+qJgkG8C17fO79gk3c+jPw4S8glRFc1DTija9S3EyaTSQUm5GJXYKDAsugBEhFHH2vYiQ==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-darwin-x64": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-darwin-x64/-/binding-darwin-x64-1.1.4.tgz",
      "integrity": "sha512-F7hHC3gwY11+vByKPRWqwGbeXWVgKmL+pTGCinaEhdihzBV2aQ0fvZOch9cXYUOKuKKq429HeYXOqQLc7wFCEg==",
      "cpu": [
        "x64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-freebsd-x64": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-freebsd-x64/-/binding-freebsd-x64-1.1.4.tgz",
      "integrity": "sha512-sI5yw+7s92SK6odiEhD5lKCBlWcpjHS5qyqpVQbZAJ0fIzEUXrmbl3DH2ybR3PZogulNJF+COLtmA8hUfvkCCQ==",
      "cpu": [
        "x64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm-gnueabihf": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm-gnueabihf/-/binding-linux-arm-gnueabihf-1.1.4.tgz",
      "integrity": "sha512-mCi0OKgEieFircrtVYmQAFGszRtMnZ6fpZAXrxanXAu7lqZcsK1E1RAaZNG0uKAnxox3B1f4EyQNnoyMfN1vAA==",
      "cpu": [
        "arm"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm64-gnu": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm64-gnu/-/binding-linux-arm64-gnu-1.1.4.tgz",
      "integrity": "sha512-B9Ial3Kv5sh0SHnB1g/QWcUQCEvCF6QKGAl4zXypYj65mVI+B4AhFBwPtSN7pDrJeIx8Z7zdy4ntx+wQABom7w==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm64-musl": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm64-musl/-/binding-linux-arm64-musl-1.1.4.tgz",
      "integrity": "sha512-lZVym0PuHE1KZ22gmFTC15lAkrg9iTszR617oYRB/iPY1A56ywoJzVKOJBKaot5RiikCObmur6pogpse3gRcng==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-ppc64-gnu": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-ppc64-gnu/-/binding-linux-ppc64-gnu-1.1.4.tgz",
      "integrity": "sha512-t2DNiLJWNTbnEHyUzTumldML6ET4/g16467LZoDDJ3tSxGvguL5/NyC2lCsNKuyRycg9XeDQF5SSv+TNOhQEXg==",
      "cpu": [
        "ppc64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-s390x-gnu": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-s390x-gnu/-/binding-linux-s390x-gnu-1.1.4.tgz",
      "integrity": "sha512-0WIRnL1Uw4BvTZRLQt+PVgo6ZKTJadlC2btP+/EOXv2f/DWbY0rEgl+y834mIVwP1FkTlWVTrGGJXf12lru7EQ==",
      "cpu": [
        "s390x"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-x64-gnu": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-x64-gnu/-/binding-linux-x64-gnu-1.1.4.tgz",
      "integrity": "sha512-JWtGshGfX+oENAKonoNkqEJX+7hC8yfhi9GUyPX1VX4mdh1y5r+ZiJLR5XzAB0aoP6s/PcILsGjKq8O0mm24bw==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-x64-musl": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-x64-musl/-/binding-linux-x64-musl-1.1.4.tgz",
      "integrity": "sha512-rT6yQcxUuXs4CnbofqwHRRV0iem349rLMYpTjkgQGLjrY4ado/eDzwPZPTCgTOlF6Nkp8NEv70yLMTn6qkWxsQ==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-openharmony-arm64": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-openharmony-arm64/-/binding-openharmony-arm64-1.1.4.tgz",
      "integrity": "sha512-KXMGoboq5cyaCQjDA4GLuRiOwBQ0EyFnJoVViLeZ45/3rFItRODEr+NdsBcVpll40hhNArlm/speWGRvj08LzA==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-wasm32-wasi": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-wasm32-wasi/-/binding-wasm32-wasi-1.1.4.tgz",
      "integrity": "sha512-5K83rb36oJiY7BCyE9zLZtGcPV4g5wvq+xwdO0XPIwDVZI8cyB/AUjkNXGb92/rnmezEkjMOpgY61rtwjQtFwg==",
      "cpu": [
        "wasm32"
      ],
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/core": "1.11.1",
        "@emnapi/runtime": "1.11.1",
        "@napi-rs/wasm-runtime": "^1.1.6"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-win32-arm64-msvc": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-win32-arm64-msvc/-/binding-win32-arm64-msvc-1.1.4.tgz",
      "integrity": "sha512-PnWBtw3TV5KOg69HQQDR0mnQuyCmSGR2pAB4DC1rPF808fgKeTUMj2EOEyKATpgiuxuR5APQmiDO7PDgEjTFSA==",
      "cpu": [
        "arm64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-win32-x64-msvc": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-win32-x64-msvc/-/binding-win32-x64-msvc-1.1.4.tgz",
      "integrity": "sha512-M1lpniBePobTfsa7Ks9a199e1akxsXn+GYBUKsEzv3YFzOm1HJAMNwKI3qr0Zq+mxwx9gOZoTdP1yXRYsZUocQ==",
      "cpu": [
        "x64"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/pluginutils": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@rolldown/pluginutils/-/pluginutils-1.0.1.tgz",
      "integrity": "sha512-2j9bGt5Jh8hj+vPtgzPtl72j0yRxHAyumoo6TNfAjsLB04UtpSvPbPcDcBMxz7n+9CYB0c1GxQFxYRg2jimqGw==",
      "license": "MIT"
    },
    "node_modules/@tybys/wasm-util": {
      "version": "0.10.3",
      "resolved": "https://registry.npmjs.org/@tybys/wasm-util/-/wasm-util-0.10.3.tgz",
      "integrity": "sha512-F3fo1MYrRJYL3zER0OUOmkutjr1Vp23m7OsSgp7nq4SP6OqX6C/56XFIPAl5bt3zaBRjmW7SGz3u/6LwFpYcOg==",
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@vitejs/plugin-react": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/@vitejs/plugin-react/-/plugin-react-6.0.3.tgz",
      "integrity": "sha512-vmFvco5/QuC2f9Oj+wTk0+9XeDFkHxSamwZKYc7MxYwKICfvUvlMhqKI0VuICPltGqh1neqBKDvO4kes1ya8vg==",
      "license": "MIT",
      "dependencies": {
        "@rolldown/pluginutils": "^1.0.1"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "peerDependencies": {
        "@rolldown/plugin-babel": "^0.1.7 || ^0.2.0",
        "babel-plugin-react-compiler": "^1.0.0",
        "vite": "^8.0.0"
      },
      "peerDependenciesMeta": {
        "@rolldown/plugin-babel": {
          "optional": true
        },
        "babel-plugin-react-compiler": {
          "optional": true
        }
      }
    },
    "node_modules/core-util-is": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/core-util-is/-/core-util-is-1.0.3.tgz",
      "integrity": "sha512-ZQBvi1DcpJ4GDqanjucZ2Hj3wEO5pZDS89BWbkcrvdxksJorwUDDZamX9ldFkp9aw2lmBDLgkObEA4DWNJ9FYQ==",
      "license": "MIT"
    },
    "node_modules/detect-libc": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/detect-libc/-/detect-libc-2.1.2.tgz",
      "integrity": "sha512-Btj2BOOO83o3WyH59e8MgXsxEQVcarkUOpEYrubB0urwnN10yQ364rsiByU11nZlqWYZm05i/of7io4mzihBtQ==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/immediate": {
      "version": "3.0.6",
      "resolved": "https://registry.npmjs.org/immediate/-/immediate-3.0.6.tgz",
      "integrity": "sha512-XXOFtyqDjNDAQxVfYxuF7g9Il/IbWmmlQg2MYKOH8ExIT1qg6xc4zyS3HaEEATgs1btfzxq15ciUiY7gjSXRGQ==",
      "license": "MIT"
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "license": "ISC"
    },
    "node_modules/isarray": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-1.0.0.tgz",
      "integrity": "sha512-VLghIWNM6ELQzo7zwmcg0NmTVyWKYjvIeM83yjp0wRDTmUnrM678fQbcKBo6n2CJEF0szoG//ytg+TKla89ALQ==",
      "license": "MIT"
    },
    "node_modules/jszip": {
      "version": "3.10.1",
      "resolved": "https://registry.npmjs.org/jszip/-/jszip-3.10.1.tgz",
      "integrity": "sha512-xXDvecyTpGLrqFrvkrUSoxxfJI5AH7U8zxxtVclpsUtMCq4JQ290LY8AW5c7Ggnr/Y/oK+bQMbqK2qmtk3pN4g==",
      "license": "(MIT OR GPL-3.0-or-later)",
      "dependencies": {
        "lie": "~3.3.0",
        "pako": "~1.0.2",
        "readable-stream": "~2.3.6",
        "setimmediate": "^1.0.5"
      }
    },
    "node_modules/lie": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/lie/-/lie-3.3.0.tgz",
      "integrity": "sha512-UaiMJzeWRlEujzAuw5LokY1L5ecNQYZKfmyZ9L7wDHb/p5etKaxXhohBcrw0EYby+G/NA52vRSN4N39dxHAIwQ==",
      "license": "MIT",
      "dependencies": {
        "immediate": "~3.0.5"
      }
    },
    "node_modules/lightningcss": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss/-/lightningcss-1.32.0.tgz",
      "integrity": "sha512-NXYBzinNrblfraPGyrbPoD19C1h9lfI/1mzgWYvXUTe414Gz/X1FD2XBZSZM7rRTrMA8JL3OtAaGifrIKhQ5yQ==",
      "license": "MPL-2.0",
      "dependencies": {
        "detect-libc": "^2.0.3"
      },
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      },
      "optionalDependencies": {
        "lightningcss-android-arm64": "1.32.0",
        "lightningcss-darwin-arm64": "1.32.0",
        "lightningcss-darwin-x64": "1.32.0",
        "lightningcss-freebsd-x64": "1.32.0",
        "lightningcss-linux-arm-gnueabihf": "1.32.0",
        "lightningcss-linux-arm64-gnu": "1.32.0",
        "lightningcss-linux-arm64-musl": "1.32.0",
        "lightningcss-linux-x64-gnu": "1.32.0",
        "lightningcss-linux-x64-musl": "1.32.0",
        "lightningcss-win32-arm64-msvc": "1.32.0",
        "lightningcss-win32-x64-msvc": "1.32.0"
      }
    },
    "node_modules/lightningcss-android-arm64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-android-arm64/-/lightningcss-android-arm64-1.32.0.tgz",
      "integrity": "sha512-YK7/ClTt4kAK0vo6w3X+Pnm0D2cf2vPHbhOXdoNti1Ga0al1P4TBZhwjATvjNwLEBCnKvjJc2jQgHXH0NEwlAg==",
      "cpu": [
        "arm64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-arm64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-arm64/-/lightningcss-darwin-arm64-1.32.0.tgz",
      "integrity": "sha512-RzeG9Ju5bag2Bv1/lwlVJvBE3q6TtXskdZLLCyfg5pt+HLz9BqlICO7LZM7VHNTTn/5PRhHFBSjk5lc4cmscPQ==",
      "cpu": [
        "arm64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-x64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-x64/-/lightningcss-darwin-x64-1.32.0.tgz",
      "integrity": "sha512-U+QsBp2m/s2wqpUYT/6wnlagdZbtZdndSmut/NJqlCcMLTWp5muCrID+K5UJ6jqD2BFshejCYXniPDbNh73V8w==",
      "cpu": [
        "x64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-freebsd-x64": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-freebsd-x64/-/lightningcss-freebsd-x64-1.32.0.tgz",
      "integrity": "sha512-JCTigedEksZk3tHTTthnMdVfGf61Fky8Ji2E4YjUTEQX14xiy/lTzXnu1vwiZe3bYe0q+SpsSH/CTeDXK6WHig==",
      "cpu": [
        "x64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm-gnueabihf": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm-gnueabihf/-/lightningcss-linux-arm-gnueabihf-1.32.0.tgz",
      "integrity": "sha512-x6rnnpRa2GL0zQOkt6rts3YDPzduLpWvwAF6EMhXFVZXD4tPrBkEFqzGowzCsIWsPjqSK+tyNEODUBXeeVHSkw==",
      "cpu": [
        "arm"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-gnu": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-gnu/-/lightningcss-linux-arm64-gnu-1.32.0.tgz",
      "integrity": "sha512-0nnMyoyOLRJXfbMOilaSRcLH3Jw5z9HDNGfT/gwCPgaDjnx0i8w7vBzFLFR1f6CMLKF8gVbebmkUN3fa/kQJpQ==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-musl": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-musl/-/lightningcss-linux-arm64-musl-1.32.0.tgz",
      "integrity": "sha512-UpQkoenr4UJEzgVIYpI80lDFvRmPVg6oqboNHfoH4CQIfNA+HOrZ7Mo7KZP02dC6LjghPQJeBsvXhJod/wnIBg==",
      "cpu": [
        "arm64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-gnu": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-gnu/-/lightningcss-linux-x64-gnu-1.32.0.tgz",
      "integrity": "sha512-V7Qr52IhZmdKPVr+Vtw8o+WLsQJYCTd8loIfpDaMRWGUZfBOYEJeyJIkqGIDMZPwPx24pUMfwSxxI8phr/MbOA==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "glibc"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-musl": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-musl/-/lightningcss-linux-x64-musl-1.32.0.tgz",
      "integrity": "sha512-bYcLp+Vb0awsiXg/80uCRezCYHNg1/l3mt0gzHnWV9XP1W5sKa5/TCdGWaR/zBM2PeF/HbsQv/j2URNOiVuxWg==",
      "cpu": [
        "x64"
      ],
      "libc": [
        "musl"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-arm64-msvc": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-arm64-msvc/-/lightningcss-win32-arm64-msvc-1.32.0.tgz",
      "integrity": "sha512-8SbC8BR40pS6baCM8sbtYDSwEVQd4JlFTOlaD3gWGHfThTcABnNDBda6eTZeqbofalIJhFx0qKzgHJmcPTnGdw==",
      "cpu": [
        "arm64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-x64-msvc": {
      "version": "1.32.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-x64-msvc/-/lightningcss-win32-x64-msvc-1.32.0.tgz",
      "integrity": "sha512-Amq9B/SoZYdDi1kFrojnoqPLxYhQ4Wo5XiL8EVJrVsB8ARoC1PWW6VGtT0WKCemjy8aC+louJnjS7U18x3b06Q==",
      "cpu": [
        "x64"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.15",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.15.tgz",
      "integrity": "sha512-y7Wygv/7mEOvxTuEQDB8StXdMRBWf1kR/tlhAzBRUFkB2jfcLOAxO/SHmOO2zgz1pVgK29/kyupn059/bCHdjA==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/pako": {
      "version": "1.0.11",
      "resolved": "https://registry.npmjs.org/pako/-/pako-1.0.11.tgz",
      "integrity": "sha512-4hLB8Py4zZce5s4yd9XzopqwVv/yGNhV1Bl8NTmCq1763HeK2+EwVTv+leGeL13Dnh2wfbqowVPXCIO0z4taYw==",
      "license": "(MIT AND Zlib)"
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "4.0.5",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.5.tgz",
      "integrity": "sha512-RvwwcruNjI1ncT5xRakeyS9Lf8lcItv34KD+aif+VH9kduAyfYBipGh12274xtenIPZ119/R9BdTBa8gAwSh0A==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.16",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.16.tgz",
      "integrity": "sha512-vuwillviilfKZsg0VGj5R/YwwcHx4SLsIOI/7K6mQkWx+l5cUHTjj5g0AasTBcyXsbfTgrwsUNmVUb5xVwyPwg==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.12",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/process-nextick-args": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/process-nextick-args/-/process-nextick-args-2.0.1.tgz",
      "integrity": "sha512-3ouUOpQhtgrbOa17J7+uxOTpITYWaGP7/AhoR3+A+/1e9skrzelGi/dXzEYyvbxubEF6Wn2ypscTKiKJFFn1ag==",
      "license": "MIT"
    },
    "node_modules/react": {
      "version": "19.2.7",
      "resolved": "https://registry.npmjs.org/react/-/react-19.2.7.tgz",
      "integrity": "sha512-HNe9WslTbXmFK8o8cmwgAeJFSBvt1bPdHCVKtaaV+WlAN36mpT4hcRpwbf3fY56ar2oIXzsBpOAiIRHAdY0OlQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-dom": {
      "version": "19.2.7",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-19.2.7.tgz",
      "integrity": "sha512-t0BRVXvbiE/o20Hfw669rLbMCDWtYZLvmJigy2f0MxsXF+71pxhR3xOkspmsO8h3ZlNzyibAmtCa3l4lYKk6gQ==",
      "license": "MIT",
      "dependencies": {
        "scheduler": "^0.27.0"
      },
      "peerDependencies": {
        "react": "^19.2.7"
      }
    },
    "node_modules/readable-stream": {
      "version": "2.3.8",
      "resolved": "https://registry.npmjs.org/readable-stream/-/readable-stream-2.3.8.tgz",
      "integrity": "sha512-8p0AUk4XODgIewSi0l8Epjs+EVnWiK7NoDIEGU0HhE7+ZyY8D1IMY7odu5lRrFXGg71L15KG8QrPmum45RTtdA==",
      "license": "MIT",
      "dependencies": {
        "core-util-is": "~1.0.0",
        "inherits": "~2.0.3",
        "isarray": "~1.0.0",
        "process-nextick-args": "~2.0.0",
        "safe-buffer": "~5.1.1",
        "string_decoder": "~1.1.1",
        "util-deprecate": "~1.0.1"
      }
    },
    "node_modules/rolldown": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/rolldown/-/rolldown-1.1.4.tgz",
      "integrity": "sha512-IjZYiLxZwpnhwhdBH2ugdTGVSdhCQUmLxLoqyjiL0JxYjyRst+5a0P3xfrTxJ5F638j4Mvvw5FAX5XE6eHpXbA==",
      "license": "MIT",
      "dependencies": {
        "@oxc-project/types": "=0.138.0",
        "@rolldown/pluginutils": "^1.0.0"
      },
      "bin": {
        "rolldown": "bin/cli.mjs"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "optionalDependencies": {
        "@rolldown/binding-android-arm64": "1.1.4",
        "@rolldown/binding-darwin-arm64": "1.1.4",
        "@rolldown/binding-darwin-x64": "1.1.4",
        "@rolldown/binding-freebsd-x64": "1.1.4",
        "@rolldown/binding-linux-arm-gnueabihf": "1.1.4",
        "@rolldown/binding-linux-arm64-gnu": "1.1.4",
        "@rolldown/binding-linux-arm64-musl": "1.1.4",
        "@rolldown/binding-linux-ppc64-gnu": "1.1.4",
        "@rolldown/binding-linux-s390x-gnu": "1.1.4",
        "@rolldown/binding-linux-x64-gnu": "1.1.4",
        "@rolldown/binding-linux-x64-musl": "1.1.4",
        "@rolldown/binding-openharmony-arm64": "1.1.4",
        "@rolldown/binding-wasm32-wasi": "1.1.4",
        "@rolldown/binding-win32-arm64-msvc": "1.1.4",
        "@rolldown/binding-win32-x64-msvc": "1.1.4"
      }
    },
    "node_modules/safe-buffer": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.1.2.tgz",
      "integrity": "sha512-Gd2UZBJDkXlY7GbJxfsE8/nvKkUEU1G38c1siN6QP6a9PT9MmHB8GnpscSmMJSoF8LOIrt8ud/wPtojys4G6+g==",
      "license": "MIT"
    },
    "node_modules/scheduler": {
      "version": "0.27.0",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.27.0.tgz",
      "integrity": "sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q==",
      "license": "MIT"
    },
    "node_modules/setimmediate": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/setimmediate/-/setimmediate-1.0.5.tgz",
      "integrity": "sha512-MATJdZp8sLqDl/68LfQmbP8zKPLQNV6BIZoIgrscFDQ+RsvK/BxeDQOgyxKKoh0y/8h3BqVFnCqQ/gd+reiIXA==",
      "license": "MIT"
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/string_decoder": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/string_decoder/-/string_decoder-1.1.1.tgz",
      "integrity": "sha512-n/ShnvDi6FHbbVfviro+WojiFzv+s8MPMHBczVePfUpDJLwoLT0ht1l4YwBCbi8pJAveEEdnkHyPyTP/mzRfwg==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "~5.1.0"
      }
    },
    "node_modules/tinyglobby": {
      "version": "0.2.17",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.17.tgz",
      "integrity": "sha512-wXR/dYpcqKmfWpEdZjiKJOwCNFndD0DMnrW/cYjVGttEkBfVgcLFHoNrlj47mjOVic9yyNu65alsgF4NQyTa2g==",
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "license": "0BSD",
      "optional": true
    },
    "node_modules/util-deprecate": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz",
      "integrity": "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw==",
      "license": "MIT"
    },
    "node_modules/vite": {
      "version": "8.1.3",
      "resolved": "https://registry.npmjs.org/vite/-/vite-8.1.3.tgz",
      "integrity": "sha512-Ds+gBRbj0lwRO2Y5hwnUBdxSwlAve9LeRyU4sNnAr0ewW0gWF0n5bgXgUzbgZ49MV9BVUAQUFYVcDUcilUExMA==",
      "license": "MIT",
      "dependencies": {
        "lightningcss": "^1.32.0",
        "picomatch": "^4.0.4",
        "postcss": "^8.5.16",
        "rolldown": "~1.1.3",
        "tinyglobby": "^0.2.17"
      },
      "bin": {
        "vite": "bin/vite.js"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "funding": {
        "url": "https://github.com/vitejs/vite?sponsor=1"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.3"
      },
      "peerDependencies": {
        "@types/node": "^20.19.0 || >=22.12.0",
        "@vitejs/devtools": "^0.3.0",
        "esbuild": "^0.27.0 || ^0.28.0",
        "jiti": ">=1.21.0",
        "less": "^4.0.0",
        "sass": "^1.70.0",
        "sass-embedded": "^1.70.0",
        "stylus": ">=0.54.8",
        "sugarss": "^5.0.0",
        "terser": "^5.16.0",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "@types/node": {
          "optional": true
        },
        "@vitejs/devtools": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        },
        "jiti": {
          "optional": true
        },
        "less": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        },
        "stylus": {
          "optional": true
        },
        "sugarss": {
          "optional": true
        },
        "terser": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    }
  }
}
````

### `novel-audio-miner/package.json`

- Purpose: Node dependency and script configuration.
- Size: 2000 bytes
- SHA-256: `02fc98336ec170b23937ff560dff7e26748fa031cb641d74be7c03d56307b8bb`

````json
{
  "name": "novel-audio-miner",
  "private": true,
  "version": "4.1.0",
  "type": "module",
  "description": "Local Japanese EPUB reader and Anki mining helper.",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test:reader-spans": "node scripts/test-analyzer-reader-spans.mjs",
    "test:color-sources": "node scripts/test-color-sources.mjs",
    "test:phase3": "npm run test:reader-spans && npm run test:color-sources && npm run test:analyzer-cache && npm run test:scene-prefetch && npm run test:analyzer-metadata-lease",
    "test:analyzer-cache": "node scripts/test-analyzer-cache.mjs",
    "test:scene-prefetch": "node scripts/test-scene-prefetch.mjs",
    "test:analyzer-metadata-lease": "node scripts/test-analyzer-metadata-lease.mjs",
    "test:analyzer-presentation": "node scripts/test-analyzer-presentation.mjs",
    "test:phase4": "npm run test:phase3 && npm run test:analyzer-presentation",
    "test:analyzer-learning-model": "node scripts/test-analyzer-learning-model.mjs",
    "test:phase5-shadow": "npm run test:phase4 && npm run test:analyzer-learning-model",
    "test:analyzer-learning-activation": "node scripts/test-analyzer-learning-activation.mjs",
    "test:phase5": "npm run test:phase5-shadow && npm run test:analyzer-learning-activation && npm run test:analyzer-mining-selection && npm run test:analyzer-selection-ownership && npm run test:tokenizer-retirement && npm run test:debug-report-v2",
    "test:analyzer-mining-selection": "node scripts/test-analyzer-mining-selection.mjs",
    "test:analyzer-selection-ownership": "node scripts/test-analyzer-selection-ownership.mjs",
    "test:tokenizer-retirement": "node scripts/test-tokenizer-retirement.mjs",
    "test:debug-report-v2": "node scripts/test-debug-report-v2.mjs"
  },
  "dependencies": {
    "@vitejs/plugin-react": "6.0.3",
    "jszip": "3.10.1",
    "react": "19.2.7",
    "react-dom": "19.2.7",
    "vite": "8.1.3"
  }
}
````

### `novel-audio-miner/PROJECT_STRUCTURE.md`

- Purpose: Documentation.
- Size: 3030 bytes
- SHA-256: `f329ab81ce6a78991cf0654082d7fb55f63a4a853cc6e9da0f35b1f15b676768`

````markdown
# Project Structure

This document records the stable v4.1 source ownership after Cleanup Patches 1-20.

## Root files

### `package.json`

Owns package metadata, scripts, and exact dependency versions.

### `package-lock.json`

Owns reproducible installed dependency resolution.

### `index.html`

Owns the browser document shell and Kuromoji script loading.

### `vite.config.js`

Owns local dev server configuration and proxy routing for:

- Nadeshiko
- VOICEVOX

## Source entry files

### `src/main.jsx`

Owns React app mounting.

### `src/App.jsx`

Owns top-level app state:

- current book
- load state
- parse errors
- upload screen vs reader screen

## Components

### `src/components/FileLoader.jsx`

Owns EPUB file selection UI.

### `src/components/Reader.jsx`

Owns the reader UI and runtime actions:

- scene navigation
- vertical/horizontal mode
- furigana toggle
- style controls
- selected text handling
- known/undo known actions
- mining action
- Anki field update orchestration

## Library modules

### `src/lib/storage.js`

Owns reader-progress persistence only.

Does not store known-word data.

### `src/lib/tokenizer.js`

Owns raw Kuromoji tokenization only.

Does not classify learning words.

### `src/lib/wordModel.js`

Owns vocabulary classification policy:

- learning words
- proper nouns/names
- grammar/function tokens
- numeric/counter expressions
- display words
- comprehension words
- mining candidates

### `src/lib/wordCache.js`

Owns known-word storage and lookup:

- Anki-derived known words
- manual-known words
- known count union
- Anki cache clearing while preserving manual-known words

### `src/lib/frequencyMap.js`

Owns local frequency dictionary loading and frequency category lookup.

### `src/lib/epubParser.js`

Owns EPUB extraction and reader-stream construction:

- container/package metadata
- spine traversal
- TOC reading
- sentence extraction
- image extraction
- token attachment
- word-model output attachment
- flat reader stream

### `src/lib/japaneseSentenceSplitter.js`

Owns Japanese sentence splitting only.

Does not group short dialogue or merge reading units.

### `src/lib/ankiConnect.js`

Owns local AnkiConnect requests:

- base request
- connection check
- latest note lookup
- note field update

### `src/lib/enrichService.js`

Owns enrichment data preparation:

- Nadeshiko search
- candidate sentence scoring
- Nadeshiko URL normalization
- VOICEVOX fallback data
- VOICEVOX audio generation

## Removed/deferred modules

### `src/lib/readingUnitGrouper.js`

This file is not part of the active stable flow and can be removed.

Reason:

- It is not imported by the current source.
- The current reader uses `flatItems` from `epubParser.js`.
- Sentence grouping is deferred until Debug Mode.

## Design rule for future work

Before adding feature logic, first add diagnostics when the behavior depends on hidden parser/tokenizer state.

This applies especially to:

- compound words
- click-to-select token spans
- sentence grouping
- EPUB image ordering
````

### `novel-audio-miner/public/dict/user_dictionary_seed.json`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 798 bytes
- SHA-256: `e8c3fff4439b237ce64a83f777f609cc29a917fcfd286b1eca09696f7fb93d25`

````json
{
  "title": "Novel Audio Miner User Dictionary Seed",
  "version": 1,
  "entries": [
    {
      "term": "後",
      "reading": "あと",
      "tags": [
        "noun",
        "time",
        "grammar-like"
      ],
      "definitions": [
        "after; later; behind"
      ],
      "source": "seed"
    },
    {
      "term": "途中",
      "reading": "とちゅう",
      "tags": [
        "noun",
        "adverbial",
        "dictionary-term"
      ],
      "definitions": [
        "on the way; midway; in the middle"
      ],
      "source": "seed"
    },
    {
      "term": "交通事故",
      "reading": "こうつうじこ",
      "tags": [
        "compound",
        "noun"
      ],
      "definitions": [
        "traffic accident"
      ],
      "source": "seed"
    }
  ]
}
````

### `novel-audio-miner/README.md`

- Purpose: Documentation.
- Size: 3581 bytes
- SHA-256: `a416acdfb86857e68bd7ac8967a61a079376dc107b111c8c3a596710e233de47`

````markdown
# Novel Audio Miner v4.1 Stable Core

Novel Audio Miner is a local Japanese EPUB reader and Anki mining helper focused on stable reading, vocabulary visibility, known-word tracking, and controlled card enrichment.

This stable core is the cleaned baseline before adding Debug Mode / Token Inspector.

## Current workflow

1. Load a Japanese EPUB locally in the browser.
2. Read sentence and illustration scenes in vertical or horizontal mode.
3. Toggle furigana while preserving word coloring.
4. Review known and unknown words with frequency-based colors.
5. Mark already-known words manually without creating Anki cards.
6. Undo manually marked known words when needed.
7. Mine selected words to the latest Kiku note through AnkiConnect.
8. Use Nadeshiko when available, with VOICEVOX fallback when online enrichment is unavailable or forced TTS is enabled.

## Stable features

- Local EPUB parsing.
- Sentence/image reading stream.
- Vertical and horizontal reading modes.
- Furigana ON/OFF support.
- Stable word coloring in furigana and non-furigana modes.
- Frequency-based unknown word colors.
- Known-word cache from Anki.
- Persistent manual-known word database.
- Undo manual-known words.
- Proper noun/name coloring and exclusion from comprehension.
- Grammar/function-token exclusion from comprehension and New Words.
- Numeric/counter grouping such as `二十歳`, `二人`, and `三日`.
- Kiku note update through AnkiConnect.
- Nadeshiko enrichment with VOICEVOX fallback.
- Stable package metadata with exact dependency versions.

## Deferred until diagnostics/debug mode

The following are intentionally deferred until a Token Inspector / Debug Mode exists:

- Broad compound-word merging.
- Composite-known judgement based on component words.
- Click-to-select token spans.
- Sentence grouping rewrite.
- EPUB parser/image-order diagnostics.
- Full debug report export.

## Run

```bash
npm install
npm run dev
```

Open the local Vite URL shown in the terminal, usually:

```text
http://127.0.0.1:5173
```

## Requirements

- Anki must be running.
- AnkiConnect must be installed and available at `http://127.0.0.1:8765`.
- The Kuromoji browser script must be loaded from `index.html`.
- Local frequency dictionaries should exist in `public/dict/`.

## Expected local dictionary files

```text
public/dict/jpdb.json
public/dict/jiten.json
public/dict/cc100.json
public/dict/bccwj.json
```

## Kiku field usage

- `SelectionText`: original novel sentence / reading context.
- `Sentence`: mined/enriched example sentence or fallback novel sentence.
- `SentenceFurigana`: sentence with furigana where available.
- `SentenceAudio`: sentence audio where available.
- `Picture`: image where available.
- `MiscInfo`: cleaned book title and chapter.

## Stable source ownership

- `src/components/Reader.jsx`: reader UI, navigation, selection, known/undo actions, and mining action.
- `src/lib/tokenizer.js`: raw Kuromoji tokenization only.
- `src/lib/wordModel.js`: vocabulary classification policy.
- `src/lib/wordCache.js`: Anki known cache and manual-known database.
- `src/lib/epubParser.js`: EPUB extraction, ordering, and token attachment.
- `src/lib/frequencyMap.js`: frequency dictionary loading and lookup.
- `src/lib/enrichService.js`: Nadeshiko/VOICEVOX enrichment preparation.
- `src/lib/ankiConnect.js`: local AnkiConnect client.

## Important design rule

If a future improvement depends on hidden tokenizer/parser state, add diagnostics first.

This applies especially to:

- compound words
- token click selection
- sentence grouping
- image ordering
````

### `novel-audio-miner/RELEASE_CHECKLIST.md`

- Purpose: Documentation.
- Size: 2807 bytes
- SHA-256: `ce9264ede71ba2bb6b958b17ab0f4b20d732b57b400a45af1d57e79be8b3007f`

````markdown
# v4.1 Stable Core Release Checklist

Use this checklist after applying Cleanup Patches 1-21.

## File placement checks

Confirm these files exist:

```text
README.md
STABILIZATION.md
WORD_MODEL_POLICY.md
PROJECT_STRUCTURE.md
package.json
package-lock.json
index.html
vite.config.js
src/main.jsx
src/App.jsx
src/styles.css
src/components/FileLoader.jsx
src/components/Reader.jsx
src/lib/ankiConnect.js
src/lib/enrichService.js
src/lib/epubParser.js
src/lib/frequencyMap.js
src/lib/japaneseSentenceSplitter.js
src/lib/storage.js
src/lib/tokenizer.js
src/lib/wordCache.js
src/lib/wordModel.js
```

Confirm this unused/deferred file has been removed:

```text
src/lib/readingUnitGrouper.js
```

## Install/build checks

Run:

```powershell
npm install
npm run dev
```

Expected:

```text
Vite starts on http://127.0.0.1:5173
Upload screen appears
No compile overlay appears
```

Optional production build check:

```powershell
npm run build
```

## Reader checks

Test with at least one EPUB:

```text
1. EPUB loads.
2. Sentences appear.
3. Images appear.
4. Vertical mode works.
5. Horizontal mode works.
6. Furigana ON works.
7. Furigana OFF works.
8. Long dashes display correctly in vertical mode.
9. Load another book returns to upload screen without full page reload.
```

## Word model checks

Confirm:

```text
1. Known words are green.
2. Unknown words use frequency colors.
3. Unlisted unknown words are grey.
4. Names/proper nouns use name color.
5. Names/proper nouns do not reduce comprehension.
6. Grammar/particles do not appear in New Words.
7. Numeric/counter expressions such as 二十歳 and 二人 are grouped/excluded.
8. Comprehension percentage appears.
9. New Words list appears.
```

## Manual known checks

Confirm:

```text
1. Mark Known works from New Words.
2. Mark Known works from selected word.
3. Undo Known works.
4. Manual-known words persist after refresh.
5. Clear Anki Cache does not remove manual-known words.
6. Rebuild cache keeps manual-known words in the known union.
```

## Mining checks

With Anki and AnkiConnect running:

```text
1. Anki status connects.
2. Latest Kiku note can be found.
3. Mine to Anki updates expected fields.
4. Nadeshiko enrichment works when available.
5. Force TTS uses VOICEVOX when enabled.
6. VOICEVOX fallback works when Nadeshiko fails.
```

## Console cleanliness checks

Expected:

```text
No normal tokenizer-loaded logs.
No normal parser tokenization logs.
No normal word-cache operation logs.
Warnings appear only for actual failures or missing optional resources.
```

## Ready for Debug Mode when

All of the following are true:

```text
- EPUB reading is stable.
- Coloring is stable.
- Comprehension/New Words are stable.
- Manual Known/Undo Known are stable.
- Mining works.
- No experimental compound logic is active.
```
````

### `novel-audio-miner/scripts/test-analyzer-cache.mjs`

- Purpose: Automated test or fixture.
- Size: 1542 bytes
- SHA-256: `6303f3706222905b74d7053873f54e3ca3257a05b0ab0e73b37cd7e6fa916fe1`

````javascript
import assert from 'node:assert/strict';
import { ANALYZER_CACHE_SCHEMA_VERSION, createAnalyzerCacheIdentity, createAnalyzerCacheRecord, normalizeAnalyzerMetadata, validateAnalyzerCacheRecord } from '../src/lib/analyzerCacheIdentity.js';
const text='少年。', meta={analyzerVersion:'11.9.0-correction-aware-cache-contract',readerSpanSchemaVersion:'1.1',correctionRevision:'rev-a'};
const result={...meta,text,readerSpans:[{start:0,end:2,surface:'少年',displayRole:'lexical',knownLookupKey:'少年',frequencyLookupKey:'少年',countsForComprehension:true,showInNewWords:true,eligibleForMining:true},{start:2,end:3,surface:'。',displayRole:'punctuation',knownLookupKey:null,frequencyLookupKey:null,countsForComprehension:false,showInNewWords:false,eligibleForMining:false}]};
assert.equal(normalizeAnalyzerMetadata(meta).valid,true);
const identity=createAnalyzerCacheIdentity('hash-a',meta); assert.ok(identity.includes('rev-a'));
const record=createAnalyzerCacheRecord(result,'hash-a',meta,new Date('2026-07-21T00:00:00Z'));
assert.equal(record.cacheSchemaVersion,ANALYZER_CACHE_SCHEMA_VERSION);
assert.equal(validateAnalyzerCacheRecord(record,text,'hash-a',meta).valid,true);
assert.equal(validateAnalyzerCacheRecord(record,text,'hash-a',{...meta,correctionRevision:'rev-b'}).reason,'cache-identity-mismatch');
assert.equal(validateAnalyzerCacheRecord({...record,readerSpans:[{...record.readerSpans[0],end:1}]},text,'hash-a',meta).reason,'reader-spans-invalid');
console.log('correction-aware analyzer cache tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-learning-activation.mjs`

- Purpose: Automated test or fixture.
- Size: 704 bytes
- SHA-256: `eb67aa3c05e3194e79431101c3780534eb36247d26f32cd31ac94f98750b269a`

````javascript
import assert from 'node:assert/strict';
import { resolveLearningOwnership } from '../src/lib/analyzerLearningModel.js';
const model={available:true,comprehension:{known:1,total:2,percent:50},newWords:[{key:'走る',surface:'走った'}]};
const active=resolveLearningOwnership({analyzerValid:true,analyzerModel:model});
assert.equal(active.source,'jp-analyzer'); assert.equal(active.comprehension.percent,50); assert.equal(active.newWords[0].word,'走る');
const unavailable=resolveLearningOwnership({analyzerValid:false,analyzerModel:null});
assert.equal(unavailable.available,false); assert.equal(unavailable.comprehension,null);
console.log('analyzer-only learning ownership tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-learning-model.mjs`

- Purpose: Automated test or fixture.
- Size: 1632 bytes
- SHA-256: `f661aa1f08a1208ba49cbda0381ab3ef87ba0ed03d7ea75c423f622bf2bde850`

````javascript
import assert from 'node:assert/strict';
import { buildAnalyzerLearningModel } from '../src/lib/analyzerLearningModel.js';
const span=(surface,role,overrides={})=>({analysisSource:'jp-analyzer-reader-spans',start:0,end:surface.length,surface,displayRole:role,countsForComprehension:false,showInNewWords:false,eligibleForMining:false,knownLookupKey:null,frequencyLookupKey:null,...overrides});
const words=[
 span('少年','lexical',{countsForComprehension:true,showInNewWords:true,eligibleForMining:true,knownLookupKey:'少年',frequencyLookupKey:'少年'}),
 span('が','function'),
 span('走る','lexical',{countsForComprehension:true,showInNewWords:true,eligibleForMining:true,knownLookupKey:'走る',frequencyLookupKey:'走る'}),
 span('てきた','learnable-grammar',{eligibleForMining:true,grammarId:'TE_KURU'}),
 span('走った','lexical',{showInNewWords:true,knownLookupKey:'走る',frequencyLookupKey:'走る'}),
 span('。','punctuation')
];
const model=buildAnalyzerLearningModel(words,{isKnown:key=>key==='少年',getFrequency:key=>({key,category:'common'})});
assert.deepEqual(model.comprehension,{known:1,unknown:1,total:2,percent:50,spans:model.comprehension.spans,excludedByRole:{function:1,'learnable-grammar':1,lexical:1,punctuation:1}});
assert.equal(model.newWords.length,1); assert.equal(model.newWords[0].key,'走る');
assert.equal(model.miningCandidates.length,3); assert.equal(model.miningCandidates[2].grammarId,'TE_KURU');
assert.throws(()=>buildAnalyzerLearningModel([span('語','lexical',{countsForComprehension:true})]),/knownLookupKey/);
console.log('analyzer learning shadow model tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-metadata-lease.mjs`

- Purpose: Automated test or fixture.
- Size: 1214 bytes
- SHA-256: `acf2b1710aa409fae1e6e7492a8291f384cd0596790d9c4f6b12342a118e8897`

````javascript
import assert from 'node:assert/strict';
import {
  ANALYZER_METADATA_LEASE_MS,
  clearAnalyzerMetadataLease,
  getAnalyzerMetadataLease,
  setAnalyzerMetadataLease
} from '../src/lib/analyzerMetadataLease.js';

const metadata = {
  analyzerVersion: '11.9.0-correction-aware-cache-contract',
  readerSpanSchemaVersion: '1.1',
  correctionRevision: 'rev-a',
  valid: true
};

clearAnalyzerMetadataLease();
assert.equal(getAnalyzerMetadataLease(1000), null);
setAnalyzerMetadataLease(metadata, 1000);
assert.equal(getAnalyzerMetadataLease(1001).correctionRevision, 'rev-a');
assert.equal(
  getAnalyzerMetadataLease(1000 + ANALYZER_METADATA_LEASE_MS).analyzerVersion,
  metadata.analyzerVersion
);
assert.equal(getAnalyzerMetadataLease(1001 + ANALYZER_METADATA_LEASE_MS), null);
setAnalyzerMetadataLease(metadata, 3000);
setAnalyzerMetadataLease(metadata, 7000);
assert.equal(
  getAnalyzerMetadataLease(7000 + ANALYZER_METADATA_LEASE_MS).verifiedAt,
  7000
);
assert.equal(
  getAnalyzerMetadataLease(7001 + ANALYZER_METADATA_LEASE_MS),
  null
);
setAnalyzerMetadataLease({ ...metadata, valid: false }, 2000);
assert.equal(getAnalyzerMetadataLease(2000), null);
console.log('analyzer metadata lease tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-mining-selection.mjs`

- Purpose: Automated test or fixture.
- Size: 1346 bytes
- SHA-256: `8ddb97c473af861c104bb182b4a3339e452c8df06660c481089c80ea3fdaccef`

````javascript
import assert from 'node:assert/strict';
import { createAnalyzerMiningContext, getAnalyzerMiningLookupKey, resolveAnalyzerMiningCandidateForOffsets } from '../src/lib/analyzerMiningSelection.js';
const lexical={start:3,end:6,surface:'走った',displayRole:'lexical',eligibleForMining:true,knownLookupKey:'走る',headword:'走る'};
const grammar={start:6,end:9,surface:'てきた',displayRole:'learnable-grammar',eligibleForMining:true,grammarId:'TE_KURU',hostLookupKey:'来る',grammarFocusRanges:[{start:6,end:9,surface:'てきた'}]};
assert.equal(resolveAnalyzerMiningCandidateForOffsets([lexical,grammar],3,6).candidate,lexical);
assert.equal(resolveAnalyzerMiningCandidateForOffsets([lexical,grammar],4,5).candidate,lexical);
assert.equal(resolveAnalyzerMiningCandidateForOffsets([lexical,grammar],5,7).reason,'selection-not-minable');
assert.equal(resolveAnalyzerMiningCandidateForOffsets([{...lexical},{...lexical}],4,5).reason,'ambiguous-selection');
assert.equal(getAnalyzerMiningLookupKey(lexical),'走る');
assert.equal(getAnalyzerMiningLookupKey(grammar),'来る');
const context=createAnalyzerMiningContext(grammar,7,8);
assert.equal(context.spanStart,6); assert.equal(context.grammarId,'TE_KURU'); assert.notEqual(context.grammarFocusRanges,grammar.grammarFocusRanges);
console.log('offset-aware analyzer mining tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-presentation.mjs`

- Purpose: Automated test or fixture.
- Size: 1807 bytes
- SHA-256: `1f1e2d884d3b4b923b14a3d64335f385912263c7bbe76cd9cce28db09e3c5ab3`

````javascript
import assert from 'node:assert/strict';
import { resolveAnalyzerPresentationClass } from '../src/lib/analyzerPresentationPolicy.js';

const base = { analysisSource: 'jp-analyzer-reader-spans', start: 0, end: 1, surface: '語' };
const classify = (span, known = new Set(), frequencies = {}) =>
  resolveAnalyzerPresentationClass({ ...base, ...span }, {
    isKnown: key => known.has(key),
    getFrequencyCategory: key => frequencies[key] ?? null
  });

assert.equal(classify({ displayRole: 'function' }), 'word-function');
assert.equal(classify({ displayRole: 'learnable-grammar' }), 'word-grammar');
assert.notEqual(classify({ displayRole: 'function' }), classify({ displayRole: 'learnable-grammar' }));
assert.equal(classify({ displayRole: 'name' }), 'word-name');
assert.equal(classify({ displayRole: 'punctuation' }), 'word-neutral');
assert.equal(classify({ displayRole: 'unresolved' }), 'word-unresolved');
assert.equal(classify({ displayRole: 'lexical', knownLookupKey: '語', frequencyLookupKey: '語' }, new Set(['語'])), 'word-known');
assert.equal(classify({ displayRole: 'lexical-compound', knownLookupKey: '複合語', frequencyLookupKey: '複合語' }, new Set(), { 複合語: 'rare' }), 'word-unknown word-freq-rare');
assert.equal(classify({ displayRole: 'lexical', knownLookupKey: null, frequencyLookupKey: null }), 'word-unknown word-freq-unlisted');
assert.equal(resolveAnalyzerPresentationClass({ ...base, analysisSource: 'legacy', displayRole: 'function' }), '');
const original = { ...base, displayRole: 'learnable-grammar', grammarId: 'TE_KURU', sourceSpanIds: ['reader-generated-1'] };
const snapshot = JSON.stringify(original);
resolveAnalyzerPresentationClass(original);
assert.equal(JSON.stringify(original), snapshot);
console.log('analyzer presentation policy tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-reader-spans.mjs`

- Purpose: Reader contract, rendering, or UI.
- Size: 4092 bytes
- SHA-256: `0dbd4de79ae6ca903ec67a8125933953033876205a732b47c5ff36a29fa947b4`

````javascript
import assert from 'node:assert/strict';
import {
  adaptReaderSpansForRendering
} from '../src/lib/analyzerReaderSpanAdapter.js';

function lexical(start, end, surface, key) {
  return {
    start,
    end,
    surface,
    displayRole: 'lexical',
    lexicalType: 'term',
    colorPolicy: 'known-or-frequency',
    unknownColorPolicy: 'frequency',
    knownLookupKey: key,
    frequencyLookupKey: key,
    countsForComprehension: true,
    showInNewWords: true,
    eligibleForMining: true,
    sourceSpanIds: [],
    sourceLayer: 'lexical',
    projectionStatus: 'selected'
  };
}

const text = '少年が走ってきた。';
const compact = {
  text,
  readerSpanSchemaVersion: '1.1',
  readerSpans: [
    lexical(0, 2, '少年', '少年'),
    {
      start: 2,
      end: 3,
      surface: 'が',
      displayRole: 'function',
      lexicalType: null,
      colorPolicy: 'muted',
      unknownColorPolicy: null,
      knownLookupKey: null,
      frequencyLookupKey: null,
      countsForComprehension: false,
      showInNewWords: false,
      eligibleForMining: false,
      sourceSpanIds: [],
      sourceLayer: 'morphology-fallback',
      projectionStatus: 'compatibility'
    },
    {
      start: 3,
      end: 8,
      surface: '走ってきた',
      displayRole: 'learnable-grammar',
      lexicalType: null,
      colorPolicy: 'grammar',
      unknownColorPolicy: null,
      knownLookupKey: null,
      frequencyLookupKey: null,
      countsForComprehension: false,
      showInNewWords: false,
      eligibleForMining: true,
      sourceSpanIds: [],
      sourceLayer: 'reader-correction',
      projectionStatus: 'user-corrected',
      correctionId: 'correction-1',
      correctionScope: 'occurrence',
      correctionAction: 'show-as-one-unit',
      hostLookupKey: '走る',
      grammarId: 'TE_KURU',
      grammarFocusRanges: [
        { start: 5, end: 8, surface: 'てきた' }
      ]
    },
    {
      start: 8,
      end: 9,
      surface: '。',
      displayRole: 'punctuation',
      lexicalType: null,
      colorPolicy: 'neutral',
      unknownColorPolicy: null,
      knownLookupKey: null,
      frequencyLookupKey: null,
      countsForComprehension: false,
      showInNewWords: false,
      eligibleForMining: false,
      sourceSpanIds: [],
      sourceLayer: 'orthography',
      projectionStatus: 'compatibility'
    }
  ]
};

const result = adaptReaderSpansForRendering(compact, text);
assert.equal(result.valid, true);
assert.deepEqual(result.errors, []);
assert.equal(result.words.map((word) => word.surface).join(''), text);
assert.equal(result.words[2].surface, '走ってきた');
assert.equal(result.words[2].grammarId, 'TE_KURU');
assert.equal(result.words[2].hostLookupKey, '走る');
assert.equal(result.words[2].projectionStatus, 'user-corrected');
assert.equal(result.correctionAware, true);
assert.equal(result.summary.corrected, 1);
assert.equal(result.words[0].dictionaryForm, '少年');

const gap = structuredClone(compact);
gap.readerSpans[1].start = 3;
const gapResult = adaptReaderSpansForRendering(gap, text);
assert.equal(gapResult.valid, false);
assert.equal(gapResult.words.length, 0);
assert.ok(gapResult.errors.some((error) => error.includes('gap')));

const wrongSurface = structuredClone(compact);
wrongSurface.readerSpans[2].surface = '走って来た';
const wrongSurfaceResult = adaptReaderSpansForRendering(wrongSurface, text);
assert.equal(wrongSurfaceResult.valid, false);
assert.equal(wrongSurfaceResult.words.length, 0);

const unsupportedSchema = structuredClone(compact);
unsupportedSchema.readerSpanSchemaVersion = '9.9';
assert.equal(
  adaptReaderSpansForRendering(unsupportedSchema, text).valid,
  false
);

const unsupportedRole = structuredClone(compact);
unsupportedRole.readerSpans[1].displayRole = 'numeric-lexical';
assert.equal(
  adaptReaderSpansForRendering(unsupportedRole, text).valid,
  false
);

console.log('authoritative readerSpans adapter tests passed');
````

### `novel-audio-miner/scripts/test-analyzer-selection-ownership.mjs`

- Purpose: Automated test or fixture.
- Size: 2508 bytes
- SHA-256: `00987e4b6044d66e7208b5745f30102cfa05ed02b5f7a83bd1883545aa26ab65`

````javascript
import assert from 'node:assert/strict';
import {
  createAnalyzerReaderContext,
  getAnalyzerSelectionActionState,
  resolveAnalyzerReaderContextForOffsets
} from '../src/lib/analyzerMiningSelection.js';

const compound = {
  start: 3, end: 8, surface: '出て行った', displayRole: 'lexical-compound',
  headword: '出て行く', knownLookupKey: '出て行く', frequencyLookupKey: '出て行く',
  countsForComprehension: true, showInNewWords: true, eligibleForMining: true
};
const particle = {
  start: 8, end: 9, surface: 'を', displayRole: 'function',
  knownLookupKey: null, eligibleForMining: false
};
const grammar = {
  start: 9, end: 12, surface: 'てきた', displayRole: 'learnable-grammar',
  knownLookupKey: null, eligibleForMining: true, grammarId: 'TE_KURU', hostLookupKey: '来る'
};

const partial = resolveAnalyzerReaderContextForOffsets([compound, particle, grammar], 4, 6, '行っ');
assert.equal(partial.valid, true);
assert.equal(partial.context.surface, '出て行った');
assert.equal(partial.context.knownLookupKey, '出て行く');
assert.equal(partial.context.rawSelectedText, '行っ');

const crossing = resolveAnalyzerReaderContextForOffsets([compound, particle], 7, 9, 'たを');
assert.equal(crossing.valid, false);
assert.equal(crossing.reason, 'selection-crosses-analyzer-spans');

const lexicalActions = getAnalyzerSelectionActionState(partial.context, {
  isKnown: () => false,
  isManualKnown: () => false
});
assert.equal(lexicalActions.canMarkKnown, true);
assert.equal(lexicalActions.canMine, true);
assert.equal(lexicalActions.knownKey, '出て行く');

const functionContext = createAnalyzerReaderContext(particle, 8, 9, 'を');
const functionActions = getAnalyzerSelectionActionState(functionContext);
assert.equal(functionActions.canMarkKnown, false);
assert.equal(functionActions.canMine, false);
assert.match(functionActions.miningMessage, /not eligible for mining/);

const grammarContext = createAnalyzerReaderContext(grammar, 10, 11, 'き');
const grammarActions = getAnalyzerSelectionActionState(grammarContext);
assert.equal(grammarActions.canMarkKnown, false);
assert.equal(grammarActions.canMine, true);
assert.match(grammarActions.knownMessage, /grammar span/);

const manualActions = getAnalyzerSelectionActionState(partial.context, {
  isKnown: key => key === '出て行く',
  isManualKnown: key => key === '出て行く'
});
assert.equal(manualActions.canUndoKnown, true);

console.log('unified analyzer selection ownership tests passed');
````

### `novel-audio-miner/scripts/test-color-sources.mjs`

- Purpose: Automated test or fixture.
- Size: 1127 bytes
- SHA-256: `e069018b53661672b54ae1ca5a53c71b30282af4ab84fd0f3253ad0be3e800a6`

````javascript
import assert from 'node:assert/strict';
import { COLOR_SOURCES, DEFAULT_COLOR_SOURCE, normalizeColorSource, resolveVisibleColourSource } from '../src/lib/colorSource.js';
const analyzerWords=[{surface:'走ってきた',start:3,end:8}];
assert.equal(DEFAULT_COLOR_SOURCE,COLOR_SOURCES.JP_ANALYZER);
assert.equal(normalizeColorSource('legacy-kuromoji'),COLOR_SOURCES.JP_ANALYZER);
assert.equal(normalizeColorSource(COLOR_SOURCES.PLAIN_TEXT),COLOR_SOURCES.PLAIN_TEXT);
const ready=resolveVisibleColourSource({requestedSource:'jp-analyzer',analyzerReady:true,analyzerWords});
assert.equal(ready.activeSource,'jp-analyzer'); assert.equal(ready.words,analyzerWords);
const failed=resolveVisibleColourSource({requestedSource:'jp-analyzer',analyzerReady:false,analyzerWords:[]});
assert.equal(failed.activeSource,'plain-text'); assert.equal(failed.neutralFallback,true);
const plain=resolveVisibleColourSource({requestedSource:'plain-text',analyzerReady:true,analyzerWords});
assert.equal(plain.activeSource,'plain-text'); assert.deepEqual(plain.words,[]);
console.log('analyzer-only colour-source policy tests passed');
````

### `novel-audio-miner/scripts/test-debug-report-v2.mjs`

- Purpose: Automated test or fixture.
- Size: 2870 bytes
- SHA-256: `7882df3c8b01510e809ae3aa8c27d0cdedde9add48f64b33587f126df60b03b1`

````javascript
import assert from 'node:assert/strict';
import { buildDebugReportV2, buildDiagnosticSummaryV2, DEBUG_REPORT_SCHEMA_VERSION } from '../src/lib/debugReportV2.js';

const span = { start: 0, end: 2, surface: '返事', displayRole: 'lexical', knownLookupKey: '返事', frequencyLookupKey: '返事', countsForComprehension: true, showInNewWords: true, eligibleForMining: true };
const report = buildDebugReportV2({
  application: { name: 'Novel Audio Miner', version: '4.1.0' },
  book: { id: 'b', title: 'Book', chapters: [{}], toc: [{}], debug: { totalItems: 5, sentenceCount: 4, imageCount: 1, pageList: [{ href: 'a' }] } },
  reader: { sceneIndex: 0, sceneNumber: 1, totalScenes: 5 },
  scene: { plainText: '返事。', htmlText: '返事。', parserDebug: { pageHref: 'a' } },
  analyzerShadow: { status: 'ready', source: 'memory-cache', elapsedMs: 0, cacheIdentity: 'id', cacheReason: 'hit', analyzerVersion: '11.9.0', readerSpanSchemaVersion: '1.1', correctionRevision: 'rev', prefetchStatus: 'complete', prefetchTargetCount: 2, prefetchCompletedCount: 2, prefetchFailedCount: 0 },
  analyzerReader: { valid: true, errors: [], words: [span], schemaVersion: '1.1', summary: { lexical: 1 } },
  analyzerResult: { analyzerVersion: '11.9.0', readerSpanSchemaVersion: '1.1', correctionRevision: 'rev', readerSpans: [span, { start: 2, end: 3, surface: '。', displayRole: 'punctuation' }], readerSelection: { decisions: [] } },
  presentationSpans: [{ ...span, className: 'word-known' }],
  learning: { available: true, source: 'jp-analyzer', comprehension: { known: 1, total: 1, percent: 100 }, newWords: [] },
  selection: { raw: '返', readerContext: span, actionState: { canMine: true } },
  mining: { candidate: span, lookupIdentity: '返事', debug: { status: 'ready' } },
  prefetchTargets: [{ index: 1, text: '次。' }],
  includeFullParserInventory: false,
  now: new Date('2026-07-24T08:00:00Z')
});
assert.equal(report.report.schemaVersion, DEBUG_REPORT_SCHEMA_VERSION);
assert.ok(report.report.diagnosticId);
assert.equal(report.analyzer.readerSpans.length, 2);
assert.equal(report.analyzer.contract.valid, true);
assert.equal(report.cache.resultSource, 'memory-cache');
assert.equal(report.prefetch.completedCount, 2);
assert.equal(report.selection.readerContext.knownLookupKey, '返事');
assert.equal(report.mining.lookupIdentity, '返事');
assert.equal(report.epub.fullInventory, null);
assert.equal('debugPanels' in report, false);
assert.equal('tokens' in report, false);
const full = buildDebugReportV2({ book: { debug: { pageList: [1] } }, includeFullParserInventory: true });
assert.deepEqual(full.epub.fullInventory.pageList, [1]);
const summary = buildDiagnosticSummaryV2(report);
assert.match(summary, /contract=valid/);
assert.match(summary, /source=memory-cache/);
console.log('Debug Report v2 tests passed');
````

### `novel-audio-miner/scripts/test-scene-prefetch.mjs`

- Purpose: Automated test or fixture.
- Size: 1343 bytes
- SHA-256: `d513454fefd883860526bc6d8807f057b913d1e8a32b7b3b280b442b2f075399`

````javascript
import assert from 'node:assert/strict';
import { findAdjacentTextScenes } from '../src/lib/scenePrefetch.js';

const scene = text => ({ type: 'scene', data: { plainText: text } });
const image = () => ({ type: 'illustration', data: { dataUri: 'data:image/png;base64,x' } });

const items = [
  scene('first'),
  image(),
  scene('second'),
  image(),
  image(),
  scene('third'),
  scene('   '),
  scene('fourth')
];

const middle = findAdjacentTextScenes(items, 2);
assert.deepEqual(middle.next, { index: 5, text: 'third', direction: 'next' });
assert.deepEqual(middle.previous, { index: 0, text: 'first', direction: 'previous' });
assert.deepEqual(middle.ordered.map(target => target.text), ['third', 'first']);

const illustration = findAdjacentTextScenes(items, 3);
assert.equal(illustration.next.index, 5);
assert.equal(illustration.previous.index, 2);

const start = findAdjacentTextScenes(items, 0);
assert.equal(start.previous, null);
assert.equal(start.next.index, 2);

const duplicate = findAdjacentTextScenes([scene('same'), image(), scene('current'), image(), scene('same')], 2);
assert.equal(duplicate.ordered.length, 1);
assert.equal(duplicate.ordered[0].direction, 'next');

assert.deepEqual(findAdjacentTextScenes([], 0), { next: null, previous: null, ordered: [] });
console.log('adjacent text-scene prefetch tests passed');
````

### `novel-audio-miner/scripts/test-tokenizer-retirement.mjs`

- Purpose: Automated test or fixture.
- Size: 1284 bytes
- SHA-256: `a90b59f6407324f7060bb7ba3bc9bc0a4d0bbaca628f0c6dc388db5906265528`

````javascript
import assert from 'node:assert/strict';
import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const absent=['src/lib/tokenizer.js','src/lib/wordModel.js','src/lib/legacyKuromojiSceneModel.js','src/lib/analyzerShadowComparison.js','src/lib/analyzerWordAdapter.js'];
for(const rel of absent) assert.equal(fs.existsSync(new URL(rel,root)),false,rel);
const pkg=JSON.parse(fs.readFileSync(new URL('package.json',root),'utf8'));
assert.equal('kuromoji' in pkg.dependencies,false);
const reader=fs.readFileSync(new URL('src/components/Reader.jsx',root),'utf8');
for(const marker of ['LEGACY_KUROMOJI','getLegacyKuromojiSceneModel','isLearningCandidate','getSelectedLearningTokens','DictionaryDebugPanel','JpAnalyzerIntegrationPanel']) assert.equal(reader.includes(marker),false,marker);
assert.equal(reader.includes('Export Debug Report'),true);
assert.equal(reader.includes('Copy Diagnostic Summary'),true);
assert.equal(reader.includes('Clear Analyzer Cache'),true);
const parser=fs.readFileSync(new URL('src/lib/epubParser.js',root),'utf8');
for(const marker of ['loadTokenizer','tokenizeText','classifiedWords','displayWords']) assert.equal(parser.includes(marker),false,marker);
console.log('tokenizer retirement and compact debug report tests passed');
````

### `novel-audio-miner/src/App.jsx`

- Purpose: JavaScript/React source.
- Size: 1160 bytes
- SHA-256: `a1eead4a27bcbfb2026b94ad64e96ea661f628fb42bd8d3e41e5cdd38140e9b1`

````jsx
import { useState } from 'react';
import FileLoader from './components/FileLoader.jsx';
import Reader from './components/Reader.jsx';
import { parseEpubFile } from './lib/epubParser.js';

export default function App() {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleFile(file) {
    setError('');
    setLoading(true);

    try {
      const parsedBook = await parseEpubFile(file);
      setBook(parsedBook);
    } catch (err) {
      console.error(err);
      setError(err?.message || 'Failed to parse EPUB.');
    } finally {
      setLoading(false);
    }
  }

  function handleLoadAnotherBook() {
    setBook(null);
    setError('');
  }

  return (
    <div className="app-shell">
      {!book && <FileLoader onFile={handleFile} loading={loading} />}
      {error && <div className="error-box">{error}</div>}
      {book && (
        <Reader
          book={book}
          flatItems={book.flatItems}
          chapterImageLists={book.chapterImageLists}
          onLoadAnotherBook={handleLoadAnotherBook}
        />
      )}
    </div>
  );
}
````

### `novel-audio-miner/src/components/FileLoader.jsx`

- Purpose: JavaScript/React source.
- Size: 780 bytes
- SHA-256: `d04564c7aa49684a1ae63566a5f87cccd43c8aa9a6c057ad774957cfc069237c`

````jsx
export default function FileLoader({ onFile, loading }) {
  function handleChange(event) {
    const file = event.target.files?.[0];
    if (file) onFile(file);
  }

  return (
    <section className="upload-card">
      <h2>Load a Japanese EPUB</h2>
      <p>Select an EPUB from your laptop. The file stays local in your browser.</p>

      <label className="file-button">
        {loading ? 'Parsing EPUB...' : 'Choose EPUB'}
        <input
          type="file"
          accept=".epub,application/epub+zip"
          disabled={loading}
          onChange={handleChange}
        />
      </label>

      <p className="small-note">
        Read locally, color known and unknown words, mark known words manually, and mine selected words to Anki.
      </p>
    </section>
  );
}
````

### `novel-audio-miner/src/components/Phase8DictionarySyncPanel.jsx`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 2235 bytes
- SHA-256: `9e047339d1bff0b5cd30cbf8d0226a4e7d0e3e497663b67dd10ccd3e194384b7`

````jsx
import { useEffect, useRef, useState } from 'react';
import { clearAnalyzerDictionaryCache, getAnalyzerDictionaryStatus, syncIndexedDbDictionariesToAnalyzer } from '../lib/phase8DictionarySync.js';
export default function Phase8DictionarySyncPanel(){const [status,setStatus]=useState(null),[message,setMessage]=useState('Not checked.'),[running,setRunning]=useState(false);const abortRef=useRef(null);async function refresh(){try{const s=await getAnalyzerDictionaryStatus();setStatus(s);setMessage(s.ready?`Analyzer has ${s.entryCount.toLocaleString()} entries from ${s.dictionaryCount} dictionaries.`:'Analyzer dictionary cache is empty.');}catch(e){setMessage(e?.message||String(e));}}useEffect(()=>{refresh();},[]);async function sync(){setRunning(true);abortRef.current=new AbortController();try{const r=await syncIndexedDbDictionariesToAnalyzer({signal:abortRef.current.signal,onProgress:p=>setMessage(`Syncing ${p.sent.toLocaleString()} / ${p.total.toLocaleString()} entries — ${p.dictionaryTitle}`)});setMessage(`Sync complete: ${r.entryCount.toLocaleString()} entries from ${r.dictionaryCount} dictionaries.`);await refresh();}catch(e){setMessage(e?.name==='AbortError'?'Sync cancelled.':e?.message||String(e));}finally{setRunning(false);abortRef.current=null;}}async function clear(){try{await clearAnalyzerDictionaryCache();await refresh();}catch(e){setMessage(e?.message||String(e));}}return <details className="debug-nested"><summary>Phase 8 analyzer dictionary sync</summary><div className="debug-empty">Copies compact evidence from existing IndexedDB dictionaries. Existing search and scan controls are untouched.</div><div className="dictionary-import-row"><button type="button" className="secondary" onClick={sync} disabled={running}>Sync dictionaries to JP Analyzer</button>{running&&<button type="button" className="secondary" onClick={()=>abortRef.current?.abort()}>Cancel sync</button>}<button type="button" className="secondary" onClick={refresh} disabled={running}>Refresh status</button><button type="button" className="secondary" onClick={clear} disabled={running}>Clear analyzer cache</button></div><div className="debug-empty">{message}</div>{status&&<pre>{JSON.stringify(status,null,2)}</pre>}</details>;}
````

### `novel-audio-miner/src/components/Reader.jsx`

- Purpose: Reader contract, rendering, or UI.
- Size: 54066 bytes
- SHA-256: `01dee1b69d454fe7df9a5bbb61c7f52295ef5f67738cf33006943befd8174cee`

````jsx
import { useEffect, useMemo, useState, useRef } from 'react';
import { getProgress, saveProgress } from '../lib/storage.js';
import { checkAnkiConnect, findLatestNote, updateNoteFields, ankiRequest } from '../lib/ankiConnect.js';
import { autoEnrichWordWithFallback, generateVoicevoxAudio } from '../lib/enrichService.js';
import { buildCache, clearCache, getCacheSize, addKnownWord, addManualKnownWord, removeManualKnownWord, isManualKnownWord, isKnownWord } from '../lib/wordCache.js';
import { getFrequency, startLoadingGlobalFrequency } from '../lib/frequencyMap.js';
import {
  clearJpAnalyzerShadowCache,
  useJpAnalyzerShadow
} from '../lib/useJpAnalyzerShadow.js';
import { adaptReaderSpansForRendering } from '../lib/analyzerReaderSpanAdapter.js';
import { findAdjacentTextScenes } from '../lib/scenePrefetch.js';
import { resolveAnalyzerPresentationClass } from '../lib/analyzerPresentationPolicy.js';
import { buildAnalyzerLearningModel, resolveLearningOwnership } from '../lib/analyzerLearningModel.js';
import { createAnalyzerReaderContext, getAnalyzerMiningLookupKey, getAnalyzerSelectionActionState, resolveAnalyzerReaderContextForOffsets } from '../lib/analyzerMiningSelection.js';
import { buildDebugReportV2, buildDiagnosticSummaryV2 } from '../lib/debugReportV2.js';
import { ANALYZER_METADATA_LEASE_MS, getAnalyzerMetadataLease } from '../lib/analyzerMetadataLease.js';
import {
  COLOR_SOURCES,
  normalizeColorSource,
  resolveVisibleColourSource
} from '../lib/colorSource.js';

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
  return tokenOrWord?.knownLookupKey || tokenOrWord?.dictionaryForm || tokenOrWord?.surface || '';
}

function getTokenFrequencyKey(tokenOrWord) {
  if (typeof tokenOrWord === 'string') return tokenOrWord;
  return tokenOrWord?.frequencyLookupKey || getTokenKnownKey(tokenOrWord);
}

function isTokenKnownForLearning(tokenOrWord) {
  return isKnownWord(getTokenKnownKey(tokenOrWord));
}

function getWordColorClass(wordOrToken) {
  const token = typeof wordOrToken === 'object' ? wordOrToken : null;

  if (token?.analysisSource === 'jp-analyzer-reader-spans') {
    return resolveAnalyzerPresentationClass(token, {
      isKnown: isKnownWord,
      getFrequencyCategory: key => getFrequency(key)?.category ?? null
    });
  }

  const word = getTokenKnownKey(wordOrToken);
  if (token?.colorRole === 'neutral') return '';
  if (token?.colorRole === 'name' || token?.tokenCategory === 'proper-noun') return 'word-name';
  if (token?.colorRole === 'numeric' || token?.tokenCategory === 'numeric') return 'word-numeric';
  if (token?.colorRole === 'grammar' || token?.tokenCategory === 'grammar') return 'word-grammar';
  if (token?.colorRole === 'unknown' || token?.tokenCategory === 'unresolved') return 'word-unknown word-freq-unlisted';
  if (token?.tokenCategory === 'ignored') return 'word-grammar';
  if (!word) return 'word-unknown word-freq-unlisted';
  if (isKnownWord(word)) return 'word-known';
  const freq = getFrequency(word);
  if (freq && freq.category) return `word-unknown word-freq-${freq.category}`;
  return 'word-unknown word-freq-unlisted';
}


function downloadJsonFile(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' }); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = filename; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
}

/* ─── Stable token range colouriser ─── */
function normalizeTokenList(tokens) {
  const normalized = (tokens || [])
    .filter(token => token?.surface)
    .map(token => ({
      ...token,
      surface: String(token.surface || ''),
      dictionaryForm:
        token.analysisSource === 'jp-analyzer-reader-spans'
          ? String(token.dictionaryForm ?? '')
          : String(token.dictionaryForm || token.surface || '')
    }))
    .filter(token => token.surface.length > 0);

  const allHaveOffsets = normalized.length > 0 && normalized.every(
    token => Number.isInteger(token.start) && Number.isInteger(token.end)
  );

  if (allHaveOffsets) {
    return normalized.sort((a, b) => a.start - b.start || a.end - b.end);
  }

  return normalized.sort((a, b) => b.surface.length - a.surface.length);
}

function buildTokenRangesFromText(text, tokens) {
  const source = text || '';
  const normalized = normalizeTokenList(tokens);
  const ranges = [];
  const occupied = new Array(source.length).fill(false);

  for (const token of normalized) {
    const exactStart = Number.isInteger(token.start) ? token.start : null;
    const exactEnd = Number.isInteger(token.end) ? token.end : null;
    const hasValidExactRange =
      exactStart !== null &&
      exactEnd !== null &&
      exactStart >= 0 &&
      exactEnd > exactStart &&
      exactEnd <= source.length &&
      source.slice(exactStart, exactEnd) === token.surface;

    if (hasValidExactRange) {
      const overlaps = occupied.slice(exactStart, exactEnd).some(Boolean);
      if (!overlaps) {
        for (let i = exactStart; i < exactEnd; i++) occupied[i] = true;
        ranges.push({
          start: exactStart,
          end: exactEnd,
          className: getWordColorClass(token),
          surface: token.surface
        });
        continue;
      }
    }

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
    parts.push(<span key={`plain-token-${index}`} className={range.className} data-token={range.surface} data-analyzer-start={range.start} data-analyzer-end={range.end}>{renderTextFragment(source.slice(range.start, range.end), verticalMode, `plain-token-${index}`)}</span>);
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
        byNodeIndex.get(nodeIndex).push({ localStart: start - info.start, localEnd: end - info.start, className: range.className, surface: range.surface, analyzerStart: range.start, analyzerEnd: range.end });
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
        span.dataset.analyzerStart = String(segment.analyzerStart);
        span.dataset.analyzerEnd = String(segment.analyzerEnd);
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
  const [selectedReaderContext, setSelectedReaderContext] = useState(null);
  const [selectionIssue, setSelectionIssue] = useState('');
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
  const [includeFullParserInventory, setIncludeFullParserInventory] = useState(false);
  const hasSavedColorSource = Object.prototype.hasOwnProperty.call(
    saved,
    'colorSource'
  );
  const [colorSource, setColorSource] = useState(() =>
    normalizeColorSource(saved.colorSource)
  );
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
  const adjacentTextScenes = useMemo(
    () => findAdjacentTextScenes(displayItems, itemIndex),
    [displayItems, itemIndex]
  );
  const jpAnalyzerShadow = useJpAnalyzerShadow(
    isText ? currentData?.plainText : '',
    {
      enabled: true,
      prefetchTexts: adjacentTextScenes.ordered.map(target => target.text)
    }
  );
  const jpAnalyzerReader = useMemo(() => {
    if (
      !isText ||
      !currentData?.plainText ||
      !jpAnalyzerShadow?.result
    ) {
      return {
        valid: false,
        errors: [],
        words: [],
        schemaVersion: '',
        summary: null,
        correctionAware: false
      };
    }

    return adaptReaderSpansForRendering(
      jpAnalyzerShadow.result,
      currentData.plainText
    );
  }, [
    isText,
    currentData?.plainText,
    jpAnalyzerShadow?.result
  ]);

  const jpAnalyzerPreviewAvailable =
    jpAnalyzerShadow?.status === 'ready' &&
    jpAnalyzerReader.valid === true &&
    jpAnalyzerReader.words.length > 0;

  const colourSourceResolution = resolveVisibleColourSource({
    requestedSource: colorSource,
    analyzerReady: jpAnalyzerPreviewAvailable,
    analyzerWords: jpAnalyzerReader.words
  });

  const activeDisplayWords = colourSourceResolution.words;
  const activeColorSource = colourSourceResolution.activeSource;
  const analyzerNeutralFallback =
    colourSourceResolution.neutralFallback;

  const analyzerLearningModel = useMemo(() => {
    if (!isText || !jpAnalyzerReader.valid) return null;
    try {
      return buildAnalyzerLearningModel(jpAnalyzerReader.words, {
        isKnown: isKnownWord,
        getFrequency
      });
    } catch {
      return null;
    }
  }, [isText, jpAnalyzerReader, cacheVersion, globalFreqReady]);

  const learningOwnership = useMemo(() => resolveLearningOwnership({
    analyzerValid: jpAnalyzerPreviewAvailable && Boolean(analyzerLearningModel),
    analyzerModel: analyzerLearningModel
  }), [jpAnalyzerPreviewAvailable, analyzerLearningModel]);

  const comprehension = learningOwnership.comprehension;
  const unknownWords = learningOwnership.newWords;

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
  useEffect(() => {
    saveProgress(book.id, {
      itemIndex,
      showFurigana,
      verticalMode,
      readerStyle,
      sidebarOpen,
      noteType,
      fields,
      debugMode,
      colorSource
    });
  }, [
    book.id,
    itemIndex,
    showFurigana,
    verticalMode,
    readerStyle,
    sidebarOpen,
    noteType,
    fields,
    debugMode,
    colorSource
  ]);
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

  useEffect(() => {
    setSelectedText('');
    setSelectedReaderContext(null);
    setSelectionIssue('');
  }, [itemIndex]);

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

  function handleTextSelection() {
    setTimeout(() => {
      const rawSelectedText = getSelectedWord();
      if (!rawSelectedText) return;
      setSelectedText(rawSelectedText);
      setSelectedReaderContext(null);
      setSelectionIssue('');
      if (learningOwnership.source !== 'jp-analyzer') return;

      const selection = window.getSelection();
      if (!selection || selection.isCollapsed || !selection.rangeCount || !sentenceBoxRef.current) {
        setSelectionIssue('Analyzer structure is unavailable for this selection.');
        return;
      }
      const range = selection.getRangeAt(0);
      const startElement = range.startContainer.nodeType === Node.ELEMENT_NODE ? range.startContainer : range.startContainer.parentElement;
      const endElement = range.endContainer.nodeType === Node.ELEMENT_NODE ? range.endContainer : range.endContainer.parentElement;
      const startSpan = startElement?.closest?.('[data-analyzer-start][data-analyzer-end]');
      const endSpan = endElement?.closest?.('[data-analyzer-start][data-analyzer-end]');
      if (!startSpan || !endSpan || !sentenceBoxRef.current.contains(startSpan) || !sentenceBoxRef.current.contains(endSpan)) {
        setSelectionIssue('Analyzer structure is unavailable for this selection.');
        return;
      }
      const spanStart = Number(startSpan.dataset.analyzerStart);
      const spanEnd = Number(startSpan.dataset.analyzerEnd);
      const endSpanStart = Number(endSpan.dataset.analyzerStart);
      const endSpanEnd = Number(endSpan.dataset.analyzerEnd);
      if (spanStart !== endSpanStart || spanEnd !== endSpanEnd) {
        setSelectionIssue('The selection crosses multiple analyzer spans.');
        return;
      }
      const resolution = resolveAnalyzerReaderContextForOffsets(
        jpAnalyzerReader.words,
        spanStart,
        spanEnd,
        rawSelectedText
      );
      if (!resolution.valid) {
        setSelectionIssue('Select within one analyzer span.');
        return;
      }
      setSelectedReaderContext(resolution.context);
      setSelectedText(resolution.context.surface);
    }, 10);
  }

  function selectNewWord(newWord) {
    const span = newWord.analyzerSpan;
    if (learningOwnership.source === 'jp-analyzer' && span) {
      const context = createAnalyzerReaderContext(span, span.start, span.end, newWord.surface || newWord.word);
      setSelectedReaderContext(context);
      setSelectedText(context.surface);
      setSelectionIssue('');
      return;
    }
    setSelectedReaderContext(null);
    setSelectionIssue('');
    setSelectedText(newWord.word);
  }

  function getKnownKeyCandidates() {
    const key = String(selectedReaderContext?.knownLookupKey || '').trim();
    return key ? [key] : [];
  }

  function getPrimaryKnownKey(word) { return getKnownKeyCandidates()[0] || String(word || '').trim(); }
  function isManualKnownCandidate() { return getKnownKeyCandidates().some(candidate => isManualKnownWord(candidate)); }
  function isKnownCandidate() { return getKnownKeyCandidates().some(candidate => isKnownWord(candidate)); }

  function getAnalyzerActionState() {
    return getAnalyzerSelectionActionState(selectedReaderContext, {
      isKnown: isKnownWord,
      isManualKnown: isManualKnownWord
    });
  }

  function handleMarkKnown(word) {
    const target = String(word || '').trim();
    if (!target) return;
    const primary = learningOwnership.source === 'jp-analyzer'
      ? String(selectedReaderContext?.knownLookupKey || '').trim()
      : getPrimaryKnownKey(target);
    if (!primary) {
      setStatus({ type: 'error', message: 'This analyzer span has no vocabulary known-word identity.' });
      return;
    }
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

  function createCurrentDebugReport() {
    const actionState = getAnalyzerActionState();
    return buildDebugReportV2({
      application: {
        name: 'Novel Audio Miner',
        version: '4.1.0',
        colorSource,
        activeColorSource,
        learningSource: learningOwnership.source
      },
      book,
      reader: {
        sceneIndex: itemIndex,
        sceneNumber: itemIndex + 1,
        totalScenes,
        selectedText: selectedText || '',
        showFurigana: Boolean(showFurigana),
        verticalMode: Boolean(verticalMode),
        readerStyle,
        ankiStatus,
        globalFreqReady: Boolean(globalFreqReady),
        forceTts: Boolean(forceTts)
      },
      scene: {
        displayItemType: isImage ? 'image' : (isText ? 'sentence' : 'none'),
        chapterIndex: currentData?.chapterIndex ?? null,
        chapterTitle: currentData?.chapterTitle || '',
        plainText: currentData?.plainText || '',
        htmlText: currentData?.htmlText || '',
        imageAlt: currentData?.alt || '',
        hasImageDataUri: Boolean(currentData?.dataUri),
        parserDebug: currentData?.parserDebug || null
      },
      adjacentScenes: displayItems.slice(Math.max(0, itemIndex - 2), itemIndex + 3).map((item, offset) => {
        const absoluteIndex = Math.max(0, itemIndex - 2) + offset;
        const data = item?.data || null;
        return {
          index: absoluteIndex,
          relative: absoluteIndex - itemIndex,
          type: item?.type === 'illustration' ? 'image' : 'sentence',
          chapterIndex: data?.chapterIndex ?? null,
          chapterTitle: data?.chapterTitle || '',
          plainText: data?.plainText || '',
          parserDebug: data?.parserDebug || null
        };
      }),
      analyzerShadow: jpAnalyzerShadow,
      analyzerReader: jpAnalyzerReader,
      analyzerResult: jpAnalyzerShadow?.result || null,
      metadataLease: getAnalyzerMetadataLease(),
      metadataLeaseMs: ANALYZER_METADATA_LEASE_MS,
      presentationSpans: jpAnalyzerReader.words.map(span => ({
        start: span.start,
        end: span.end,
        surface: span.surface,
        displayRole: span.displayRole,
        className: getWordColorClass(span),
        known: span.knownLookupKey ? isKnownWord(span.knownLookupKey) : false,
        frequency: span.frequencyLookupKey ? getFrequency(span.frequencyLookupKey) : null
      })),
      learning: {
        available: learningOwnership.available,
        source: learningOwnership.source,
        comprehension,
        newWords: unknownWords
      },
      selection: {
        raw: selectedText || '',
        readerContext: selectedReaderContext,
        actionState,
        issue: selectionIssue || null
      },
      mining: {
        candidate: selectedReaderContext?.eligibleForMining ? selectedReaderContext : null,
        lookupIdentity: selectedReaderContext ? getAnalyzerMiningLookupKey(selectedReaderContext) : null,
        debug: miningDebug,
        enrichment: enrichResult,
        working: isWorking
      },
      prefetchTargets: adjacentTextScenes.ordered,
      includeFullParserInventory
    });
  }

  function handleExportDebugReport() {
    const report = createCurrentDebugReport();
    const safeTitle = cleanBookTitle(book?.title || book?.fileName || 'book').replace(/[\/:*?"<>|\s]+/g, '_').slice(0, 60) || 'book';
    downloadJsonFile(`novel-audio-miner-debug-v2-${safeTitle}-scene-${itemIndex + 1}.json`, report);
  }

  function handleCopyDiagnosticSummary() {
    navigator.clipboard?.writeText(buildDiagnosticSummaryV2(createCurrentDebugReport()));
  }

  function updateMiningDebug(patch) {
    setMiningDebug(prev => ({ ...(prev || {}), ...patch, updatedAt: new Date().toISOString() }));
  }

  async function handleMine() {
    if (!selectedText) { setMiningDebug({ status: 'blocked', stage: 'validation', selectedWord: '', error: 'Select a word first.', updatedAt: new Date().toISOString() }); setStatus({ type: 'error', message: 'Select a word first.' }); return; }
    if (!isText) { setMiningDebug({ status: 'blocked', stage: 'validation', selectedWord: selectedText, error: 'Navigate to text first.', updatedAt: new Date().toISOString() }); setStatus({ type: 'error', message: 'Navigate to text first.' }); return; }
    const novelSentence = currentData?.plainText || '';
    const analyzerCandidate = learningOwnership.source === 'jp-analyzer'
      ? selectedReaderContext
      : null;
    if (learningOwnership.source === 'jp-analyzer' && (!analyzerCandidate || analyzerCandidate.eligibleForMining !== true)) {
      const message = selectionIssue || getAnalyzerActionState().miningMessage;
      setMiningDebug({ status: 'blocked', stage: 'eligibility', selectedWord: selectedText, error: message, updatedAt: new Date().toISOString() });
      setStatus({ type: 'error', message });
      return;
    }
    const miningLookupKey = analyzerCandidate ? getAnalyzerMiningLookupKey(analyzerCandidate) : selectedText;
    setMiningDebug({ status: 'running', stage: 'start', startedAt: new Date().toISOString(), updatedAt: new Date().toISOString(), selectedWord: selectedText, miningLookupKey, analyzerMiningSelection: selectedReaderContext, learningSource: learningOwnership.source, noteType, scene: `${itemIndex + 1} / ${totalScenes}`, chapterTitle: currentData?.chapterTitle || '', novelSentence });
    setIsWorking(true); setEnrichResult(null); setStatus({ type: 'working', message: 'Connecting to Anki...' });
    try {
      updateMiningDebug({ status: 'running', stage: 'checkAnkiConnect' }); await checkAnkiConnect();
      setStatus({ type: 'working', message: 'Finding latest note...' }); updateMiningDebug({ status: 'running', stage: 'findLatestNote' });
      const noteResult = await findLatestNote(noteType);
      updateMiningDebug({ latestNoteQuery: noteResult.query, latestNoteCount: noteResult.ids?.length ?? 0, latestNoteId: noteResult.note?.noteId || '' });
      if (!noteResult.note) { updateMiningDebug({ status: 'error', stage: 'findLatestNote', error: 'No Kiku note found.' }); setStatus({ type: 'error', message: 'No Kiku note found.' }); setIsWorking(false); return; }
      const noteId = noteResult.note.noteId;
      updateMiningDebug({ status: 'running', stage: 'enrichment' });
      const result = await autoEnrichWordWithFallback(miningLookupKey, novelSentence, ankiRequest, noteType, msg => { updateMiningDebug({ status: 'running', stage: msg }); setStatus({ type: 'working', message: msg }); });
      setEnrichResult(result);
      updateMiningDebug({ status: 'running', stage: 'enrichmentComplete', enrichmentMethod: result.method || '', source: result.source || '', mode: result.mode || '', unknownCount: result.unknownCount ?? null, chosenSentence: result.sentence || '', sentenceFurigana: result.sentenceFurigana || '', hasAudioUrl: Boolean(result.audioUrl), hasImageUrl: Boolean(result.imageUrl), audioUrl: result.audioUrl || '', imageUrl: result.imageUrl || '' });
      setStatus({ type: 'working', message: 'Downloading media...' });
      const fieldUpdates = { [fields.sentence]: result.sentence, [fields.sentenceFurigana]: result.sentenceFurigana || result.sentence, [fields.miscInfo]: [cleanedTitle, currentData?.chapterTitle || ''].filter(Boolean).join(' · ') };
      if (result.method !== 'voicevox') fieldUpdates[fields.selectionText] = novelSentence;
      if (result.method === 'voicevox') { try { updateMiningDebug({ status: 'running', stage: 'voicevoxAudio' }); const { audioBase64, filename } = await generateVoicevoxAudio(novelSentence); await ankiRequest('storeMediaFile', { filename, data: audioBase64 }); fieldUpdates[fields.sentenceAudio] = `[sound:${filename}]`; updateMiningDebug({ sentenceAudio: `[sound:${filename}]` }); } catch (err) { updateMiningDebug({ voicevoxError: err?.message || String(err) }); } }
      else if (result.audioUrl) { try { updateMiningDebug({ status: 'running', stage: 'nadeshikoAudio' }); const filename = `nade_audio_${Date.now()}.mp3`; await ankiRequest('storeMediaFile', { filename, url: result.audioUrl }); fieldUpdates[fields.sentenceAudio] = `[sound:${filename}]`; updateMiningDebug({ sentenceAudio: `[sound:${filename}]` }); } catch (e) { updateMiningDebug({ audioError: e?.message || String(e) }); } }
      if (result.method !== 'voicevox' && result.imageUrl) { try { updateMiningDebug({ status: 'running', stage: 'nadeshikoImage' }); const filename = `nade_img_${Date.now()}.jpg`; await ankiRequest('storeMediaFile', { filename, url: result.imageUrl }); fieldUpdates[fields.picture] = `<img src="${filename}">`; updateMiningDebug({ picture: `<img src="${filename}">` }); } catch (e) { updateMiningDebug({ imageError: e?.message || String(e) }); } }
      updateMiningDebug({ status: 'running', stage: 'updateNoteFields', preparedFields: fieldUpdates }); await updateNoteFields(noteId, fieldUpdates);
      if (analyzerCandidate?.knownLookupKey) addKnownWord(miningLookupKey); setCacheVersion(v => v + 1); try { await ankiRequest('guiBrowse', { query: `nid:${noteId}` }); } catch (e) {}
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
          {isText && !learningOwnership.available && (
            <>
              <span>·</span>
              <span>Analyzer learning model unavailable</span>
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
                        onClick={() => selectNewWord(uw)}>
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
              <label style={{ fontSize: '11px', color: 'var(--muted)', display: 'grid', gap: '4px' }}>
                Colour source:
                <select
                  value={colorSource}
                  onChange={event => setColorSource(
                    normalizeColorSource(event.target.value)
                  )}
                >
                  <option value={COLOR_SOURCES.JP_ANALYZER}>JP Analyzer</option>
                  <option value={COLOR_SOURCES.PLAIN_TEXT}>Plain text</option>
                </select>
                <span style={{ fontSize: '10px' }}>
                  JP Analyzer is the sole linguistic source. Plain Text changes presentation only; invalid analyzer output remains neutral.
                </span>
              </label>
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
                <div className="debug-panel-title">Debug Report</div>
              </div>
              <div className="debug-summary-grid">
                <div className="debug-mini-card"><span>Analyzer</span><strong>{jpAnalyzerShadow?.status ?? 'idle'}</strong></div>
                <div className="debug-mini-card"><span>Reader contract</span><strong>{jpAnalyzerReader.valid ? 'valid' : 'invalid'}</strong></div>
                <div className="debug-mini-card"><span>Result source</span><strong>{jpAnalyzerShadow?.source ?? '-'}</strong></div>
                <div className="debug-mini-card"><span>Scene</span><strong>{itemIndex + 1} / {totalScenes}</strong></div>
              </div>
              <label style={{ display: 'flex', gap: '6px', alignItems: 'center', marginTop: '8px', fontSize: '10px', color: 'var(--muted)' }}>
                <input type="checkbox" checked={includeFullParserInventory} onChange={event => setIncludeFullParserInventory(event.target.checked)} />
                Include full EPUB parser inventory
              </label>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '8px' }}>
                <button type="button" className="debug-export-btn" onClick={handleExportDebugReport}>Export Debug Report</button>
                <button type="button" className="secondary" onClick={handleCopyDiagnosticSummary}>Copy Diagnostic Summary</button>
                <button type="button" className="secondary" onClick={clearJpAnalyzerShadowCache}>Clear Analyzer Cache</button>
              </div>
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
                  tokens: activeDisplayWords,
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
                {(() => {
                  const action = getAnalyzerActionState();
                  if (!selectedText) return <button className="secondary mark-known-btn" disabled>Mark as Known</button>;
                  if (action.canUndoKnown) return <button className="secondary mark-known-btn" onClick={() => handleUndoKnown(selectedText)} disabled={isWorking}>Undo Known</button>;
                  if (action.knownFromAnki) return <button className="secondary mark-known-btn known-from-anki-btn" disabled title="This analyzer lookup key is already known from Anki/cache.">Known from Anki</button>;
                  if (action.canMarkKnown) return <button className="secondary mark-known-btn" onClick={() => handleMarkKnown(selectedText)} disabled={isWorking}>Mark as Known</button>;
                  return <button className="secondary mark-known-btn non-learning-word-btn" disabled title={selectionIssue || action.knownMessage}>{action.knownMessage || 'Not vocabulary-known eligible'}</button>;
                })()}
                <button className="mine-btn" onClick={handleMine} disabled={!selectedText || isWorking || (!selectedReaderContext || selectedReaderContext.eligibleForMining !== true)}>⚡ Mine to Anki</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
````

### `novel-audio-miner/src/lib/analyzerCacheIdentity.js`

- Purpose: JavaScript/React source.
- Size: 2398 bytes
- SHA-256: `b68c876cc2160d45cf3d3bb873f042dda4d98506996dc026472915034370c5dc`

````javascript
import { adaptReaderSpansForRendering } from './analyzerReaderSpanAdapter.js';

export const ANALYZER_CACHE_SCHEMA_VERSION = '3.1';
export const ANALYZER_CACHE_PREFIX = 'jp-analyzer-reader-cache-v3:';

export function normalizeAnalyzerMetadata(value) {
  const metadata = {
    analyzerVersion: String(value?.analyzerVersion ?? value?.version ?? '').trim(),
    readerSpanSchemaVersion: String(value?.readerSpanSchemaVersion ?? '').trim(),
    correctionRevision: String(value?.correctionRevision ?? '').trim()
  };
  return { ...metadata, valid: Object.values(metadata).every(Boolean) };
}

export function createAnalyzerCacheIdentity(sentenceHash, metadata) {
  const normalized = normalizeAnalyzerMetadata(metadata);
  if (!sentenceHash || !normalized.valid) return null;
  return [ANALYZER_CACHE_SCHEMA_VERSION, sentenceHash, normalized.analyzerVersion,
    normalized.readerSpanSchemaVersion, normalized.correctionRevision].join(':');
}

export function createAnalyzerCacheRecord(result, sentenceHash, metadata, now = new Date()) {
  const identity = createAnalyzerCacheIdentity(sentenceHash, metadata);
  if (!identity) throw new Error('Cannot cache without complete analyzer metadata.');
  return { ...result, cacheSchemaVersion: ANALYZER_CACHE_SCHEMA_VERSION,
    sentenceHash, analyzerVersion: metadata.analyzerVersion,
    readerSpanSchemaVersion: metadata.readerSpanSchemaVersion,
    correctionRevision: metadata.correctionRevision,
    cacheIdentity: identity, savedAt: now.toISOString(), lastAccessedAt: now.toISOString() };
}

export function validateAnalyzerCacheRecord(record, expectedText, sentenceHash, metadata) {
  const expectedIdentity = createAnalyzerCacheIdentity(sentenceHash, metadata);
  if (!record || !expectedIdentity) return { valid: false, reason: 'metadata-unavailable' };
  if (record.cacheSchemaVersion !== ANALYZER_CACHE_SCHEMA_VERSION) return { valid: false, reason: 'cache-schema-mismatch' };
  if (record.cacheIdentity !== expectedIdentity) return { valid: false, reason: 'cache-identity-mismatch' };
  if (record.text !== expectedText || record.sentenceHash !== sentenceHash) return { valid: false, reason: 'sentence-mismatch' };
  const validation = adaptReaderSpansForRendering(record, expectedText);
  if (!validation.valid) return { valid: false, reason: 'reader-spans-invalid', errors: validation.errors };
  return { valid: true, reason: 'valid' };
}
````

### `novel-audio-miner/src/lib/analyzerLearningModel.js`

- Purpose: JavaScript/React source.
- Size: 3198 bytes
- SHA-256: `324bf646b36f9c4c46fe680f6411b64dd9aaf99e9e4eaa388a1fc7888ad0c25e`

````javascript
/** Phase 5.1: pure, read-only learning projection from validated readerSpans. */
export function buildAnalyzerLearningModel(words, { isKnown = () => false, getFrequency = () => null } = {}) {
  const spans = Array.isArray(words) ? words : [];
  const comprehensionSpans = [];
  const newWords = [];
  const miningCandidates = [];
  const seenNewWords = new Set();
  const excludedByRole = {};
  let known = 0;

  for (const span of spans) {
    if (!span || span.analysisSource !== 'jp-analyzer-reader-spans') continue;
    if (span.countsForComprehension) {
      const key = requiredKey(span.knownLookupKey, span, 'countsForComprehension');
      const knownState = isKnown(key);
      if (knownState) known += 1;
      comprehensionSpans.push(copySpan(span, { key, known: knownState }));
    } else {
      const role = span.displayRole || 'missing';
      excludedByRole[role] = (excludedByRole[role] || 0) + 1;
    }

    if (span.showInNewWords) {
      const key = requiredKey(span.knownLookupKey, span, 'showInNewWords');
      if (!isKnown(key) && !seenNewWords.has(key)) {
        seenNewWords.add(key);
        const frequencyKey = optionalKey(span.frequencyLookupKey);
        newWords.push(copySpan(span, { key, frequencyKey, frequency: frequencyKey ? getFrequency(frequencyKey) : null }));
      }
    }

    if (span.eligibleForMining) {
      miningCandidates.push(copySpan(span));
    }
  }

  const total = comprehensionSpans.length;
  return {
    available: true,
    comprehension: { known, unknown: total - known, total, percent: total ? Math.round((known / total) * 100) : null, spans: comprehensionSpans, excludedByRole },
    newWords,
    miningCandidates
  };
}

function requiredKey(value, span, flag) {
  const key = optionalKey(value);
  if (!key) throw new Error(`${flag} span lacks analyzer knownLookupKey: ${span.surface || ''}`);
  return key;
}
function optionalKey(value) { return typeof value === 'string' && value.trim() ? value.trim() : ''; }
function copySpan(span, extra = {}) {
  return {
    start: span.start, end: span.end, surface: span.surface, displayRole: span.displayRole,
    headword: span.headword ?? null, knownLookupKey: span.knownLookupKey ?? null,
    frequencyLookupKey: span.frequencyLookupKey ?? null, grammarId: span.grammarId ?? null,
    hostLookupKey: span.hostLookupKey ?? null, correctionId: span.correctionId ?? null,
    correctionScope: span.correctionScope ?? null, correctionAction: span.correctionAction ?? null,
    grammarFocusRanges: Array.isArray(span.grammarFocusRanges) ? span.grammarFocusRanges.map(r => ({ ...r })) : [],
    ...extra
  };
}


/** JP Analyzer is the sole production learning model. */
export function resolveLearningOwnership({ analyzerValid, analyzerModel }) {
  if (!analyzerValid || !analyzerModel?.available) return { source: 'jp-analyzer', available: false, comprehension: null, newWords: [] };
  return { source: 'jp-analyzer', available: true, comprehension: analyzerModel.comprehension, newWords: analyzerModel.newWords.map(span => ({ word: span.key, surface: span.surface, freq: span.frequency, analyzerSpan: span })) };
}
````

### `novel-audio-miner/src/lib/analyzerMetadataLease.js`

- Purpose: JavaScript/React source.
- Size: 780 bytes
- SHA-256: `a95d758702a22cc7ea9cca9585eb355044b9f8b1c84d1a261c0020f9c2ebbd8c`

````javascript
export const ANALYZER_METADATA_LEASE_MS = 5000;

let activeLease = null;

export function setAnalyzerMetadataLease(metadata, now = Date.now()) {
  if (!metadata?.valid) {
    activeLease = null;
    return null;
  }
  activeLease = {
    analyzerVersion: metadata.analyzerVersion,
    readerSpanSchemaVersion: metadata.readerSpanSchemaVersion,
    correctionRevision: metadata.correctionRevision,
    valid: true,
    verifiedAt: now
  };
  return { ...activeLease };
}

export function getAnalyzerMetadataLease(now = Date.now()) {
  if (!activeLease) return null;
  if (now - activeLease.verifiedAt > ANALYZER_METADATA_LEASE_MS) {
    activeLease = null;
    return null;
  }
  return { ...activeLease };
}

export function clearAnalyzerMetadataLease() {
  activeLease = null;
}
````

### `novel-audio-miner/src/lib/analyzerMiningSelection.js`

- Purpose: JavaScript/React source.
- Size: 4789 bytes
- SHA-256: `216a9ddcd722163ec091a74a0f0a64ca7bc894143839fdfb010f805d8523aba7`

````javascript
/**
 * Authoritative JP Analyzer selection and action ownership.
 *
 * This module never searches by surface text and never consults Kuromoji.
 * Browser selections are resolved only through exact analyzer source offsets.
 */

function cloneRanges(ranges) {
  return Array.isArray(ranges) ? ranges.map(range => ({ ...range })) : [];
}

export function createAnalyzerReaderContext(span, selectionStart, selectionEnd, rawSelectedText = '') {
  if (!span) return null;
  return {
    source: 'jp-analyzer',
    rawSelectedText: String(rawSelectedText ?? ''),
    selectionStart,
    selectionEnd,
    spanStart: span.start,
    spanEnd: span.end,
    surface: span.surface,
    displayRole: span.displayRole,
    headword: span.headword ?? null,
    knownLookupKey: span.knownLookupKey ?? null,
    frequencyLookupKey: span.frequencyLookupKey ?? null,
    countsForComprehension: span.countsForComprehension === true,
    showInNewWords: span.showInNewWords === true,
    eligibleForMining: span.eligibleForMining === true,
    grammarId: span.grammarId ?? null,
    hostLookupKey: span.hostLookupKey ?? null,
    correctionId: span.correctionId ?? null,
    correctionScope: span.correctionScope ?? null,
    correctionAction: span.correctionAction ?? null,
    grammarFocusRanges: cloneRanges(span.grammarFocusRanges)
  };
}

export function resolveAnalyzerReaderContextForOffsets(spans, selectionStart, selectionEnd, rawSelectedText = '') {
  if (!Number.isInteger(selectionStart) || !Number.isInteger(selectionEnd) || selectionStart < 0 || selectionEnd <= selectionStart) {
    return { valid: false, context: null, reason: 'invalid-selection-offsets' };
  }
  const containing = (spans || []).filter(span =>
    Number.isInteger(span?.start) && Number.isInteger(span?.end) &&
    span.start <= selectionStart && span.end >= selectionEnd
  );
  if (containing.length !== 1) {
    return {
      valid: false,
      context: null,
      reason: containing.length ? 'ambiguous-selection' : 'selection-crosses-analyzer-spans'
    };
  }
  return {
    valid: true,
    context: createAnalyzerReaderContext(containing[0], selectionStart, selectionEnd, rawSelectedText),
    reason: 'analyzer-span-selected'
  };
}

export function getAnalyzerSelectionActionState(context, { isKnown = () => false, isManualKnown = () => false } = {}) {
  if (!context) {
    return {
      canMarkKnown: false,
      canUndoKnown: false,
      knownFromAnki: false,
      canMine: false,
      knownKey: '',
      miningMessage: 'Analyzer structure is unavailable for this selection.',
      knownMessage: 'Select within one analyzer span.'
    };
  }
  const knownKey = String(context.knownLookupKey ?? '').trim();
  const manualKnown = Boolean(knownKey && isManualKnown(knownKey));
  const known = Boolean(knownKey && isKnown(knownKey));
  const canMine = context.eligibleForMining === true;
  return {
    canMarkKnown: Boolean(knownKey && !known),
    canUndoKnown: manualKnown,
    knownFromAnki: Boolean(known && !manualKnown),
    canMine,
    knownKey,
    miningMessage: canMine ? '' : 'This analyzer span is not eligible for mining.',
    knownMessage: knownKey
      ? ''
      : context.displayRole === 'learnable-grammar'
        ? 'This grammar span can be mined but cannot be marked as known vocabulary.'
        : 'This analyzer span has no vocabulary known-word identity.'
  };
}

/** Backwards-compatible Phase 5.2B exports. */
export function resolveAnalyzerMiningCandidateForOffsets(candidates, selectionStart, selectionEnd) {
  const result = resolveAnalyzerReaderContextForOffsets(candidates, selectionStart, selectionEnd);
  if (!result.valid || result.context?.eligibleForMining !== true) {
    const legacyReason = result.reason === 'ambiguous-selection'
      ? 'ambiguous-selection'
      : 'selection-not-minable';
    return { valid: false, candidate: null, reason: legacyReason };
  }
  const candidate = (candidates || []).find(item =>
    item.start === result.context.spanStart && item.end === result.context.spanEnd
  ) ?? null;
  return { valid: Boolean(candidate), candidate, reason: candidate ? 'analyzer-span-selected' : 'selection-not-minable' };
}

export function getAnalyzerMiningLookupKey(candidateOrContext) {
  if (!candidateOrContext) return '';
  const ordered = candidateOrContext.displayRole === 'learnable-grammar'
    ? [candidateOrContext.hostLookupKey, candidateOrContext.surface]
    : [candidateOrContext.knownLookupKey, candidateOrContext.headword, candidateOrContext.surface];
  return ordered.map(value => String(value ?? '').trim()).find(Boolean) ?? '';
}

export function createAnalyzerMiningContext(candidate, selectionStart, selectionEnd) {
  return createAnalyzerReaderContext(candidate, selectionStart, selectionEnd, candidate?.surface ?? '');
}
````

### `novel-audio-miner/src/lib/analyzerPresentationPolicy.js`

- Purpose: JavaScript/React source.
- Size: 1505 bytes
- SHA-256: `beb654d4a6cd8552c2e7be25225a69dd13a713a7531c9b3fb796084537182a2c`

````javascript
/**
 * Presentation-only policy for authoritative JP Analyzer reader spans.
 * Never changes analyzer boundaries, roles, lookup keys, or metadata.
 */
const LEXICAL_ROLES = new Set(['lexical', 'lexical-compound']);

export function resolveAnalyzerPresentationClass(span, {
  isKnown = () => false,
  getFrequencyCategory = () => null
} = {}) {
  if (!span || span.analysisSource !== 'jp-analyzer-reader-spans') return '';

  switch (span.displayRole) {
    case 'punctuation': return 'word-neutral';
    case 'unresolved': return 'word-unresolved';
    case 'name': return 'word-name';
    case 'function': return 'word-function';
    case 'learnable-grammar': return 'word-grammar';
    default: break;
  }

  if (!LEXICAL_ROLES.has(span.displayRole)) return 'word-neutral';

  const knownKey = optionalKey(span.knownLookupKey);
  const frequencyKey = optionalKey(span.frequencyLookupKey);
  if (knownKey && isKnown(knownKey)) return 'word-known';

  const category = frequencyKey
    ? normalizeFrequencyCategory(getFrequencyCategory(frequencyKey))
    : null;
  return category
    ? `word-unknown word-freq-${category}`
    : 'word-unknown word-freq-unlisted';
}

function optionalKey(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : '';
}

function normalizeFrequencyCategory(value) {
  const category = typeof value === 'string' ? value : value?.category;
  return ['very-common', 'common', 'uncommon', 'rare', 'unlisted'].includes(category)
    ? category
    : null;
}
````

### `novel-audio-miner/src/lib/analyzerReaderSpanAdapter.js`

- Purpose: Reader contract, rendering, or UI.
- Size: 7222 bytes
- SHA-256: `5d3903b2306d88474973a5e59b7394afe6932846978952d4379e4ab8d7a0d6cb`

````javascript
/**
 * Thin adapter for JP Analyzer's authoritative readerSpans contract.
 *
 * This module performs validation and mechanical field preservation only.
 * It must not infer boundaries, repair offsets, derive headwords, or
 * reclassify linguistic roles.
 */

export const SUPPORTED_READER_SPAN_SCHEMAS = new Set(['1.1']);

export const SUPPORTED_DISPLAY_ROLES = new Set([
  'lexical',
  'lexical-compound',
  'learnable-grammar',
  'function',
  'name',
  'punctuation',
  'unresolved'
]);

export function adaptReaderSpansForRendering(compact, expectedText) {
  const sourceText = String(expectedText ?? '');
  const errors = [];

  if (!compact || typeof compact !== 'object') {
    return invalidResult(['Compact analysis is not an object.']);
  }

  if (compact.text !== sourceText) {
    errors.push('Analyzer source text differs from reader source text.');
  }

  const schemaVersion = String(
    compact.readerSpanSchemaVersion ?? ''
  ).trim();

  if (!SUPPORTED_READER_SPAN_SCHEMAS.has(schemaVersion)) {
    errors.push(
      `Unsupported reader span schema: ${schemaVersion || 'missing'}.`
    );
  }

  if (!Array.isArray(compact.readerSpans)) {
    errors.push('readerSpans is missing or is not an array.');
    return invalidResult(errors, schemaVersion);
  }

  if (sourceText.length > 0 && compact.readerSpans.length === 0) {
    errors.push('readerSpans is empty for non-empty source text.');
  }

  const words = [];
  let previousEnd = 0;

  compact.readerSpans.forEach((span, index) => {
    const spanErrors = validateReaderSpan(
      span,
      index,
      sourceText,
      previousEnd
    );

    errors.push(...spanErrors);

    if (spanErrors.length === 0) {
      words.push(preserveReaderSpan(span));
      previousEnd = span.end;
    }
  });

  if (compact.readerSpans.length > 0) {
    const first = compact.readerSpans[0];
    const last = compact.readerSpans[compact.readerSpans.length - 1];

    if (first?.start !== 0) {
      errors.push('readerSpans does not start at source offset 0.');
    }

    if (last?.end !== sourceText.length) {
      errors.push('readerSpans does not end at the source text length.');
    }
  }

  const reconstructed = compact.readerSpans
    .map((span) => String(span?.surface ?? ''))
    .join('');

  if (reconstructed !== sourceText) {
    errors.push('readerSpans surfaces do not reconstruct the source text.');
  }

  const valid = errors.length === 0;

  return {
    valid,
    errors,
    words: valid ? words : [],
    schemaVersion,
    summary: summarizeReaderSpans(valid ? words : []),
    correctionAware: valid && words.some(
      (word) => word.projectionStatus === 'user-corrected'
    )
  };
}

function invalidResult(errors, schemaVersion = '') {
  return {
    valid: false,
    errors,
    words: [],
    schemaVersion,
    summary: summarizeReaderSpans([]),
    correctionAware: false
  };
}

function validateReaderSpan(span, index, sourceText, previousEnd) {
  const errors = [];
  const label = `readerSpans[${index}]`;

  if (!span || typeof span !== 'object') {
    return [`${label} is not an object.`];
  }

  if (!Number.isInteger(span.start)) {
    errors.push(`${label}.start is not an integer.`);
  }

  if (!Number.isInteger(span.end)) {
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
    errors.push(`${label} has an invalid source range.`);
    return errors;
  }

  if (span.start !== previousEnd) {
    errors.push(
      span.start < previousEnd
        ? `${label} overlaps the previous reader span.`
        : `${label} leaves a gap after the previous reader span.`
    );
  }

  const expectedSurface = sourceText.slice(span.start, span.end);

  if (span.surface !== expectedSurface) {
    errors.push(`${label}.surface does not match its source offsets.`);
  }

  if (!SUPPORTED_DISPLAY_ROLES.has(span.displayRole)) {
    errors.push(
      `${label}.displayRole is unsupported: ${String(span.displayRole)}.`
    );
  }

  for (const field of [
    'countsForComprehension',
    'showInNewWords',
    'eligibleForMining'
  ]) {
    if (typeof span[field] !== 'boolean') {
      errors.push(`${label}.${field} is not a boolean.`);
    }
  }

  if (
    ['lexical', 'lexical-compound'].includes(span.displayRole) &&
    (!isOptionalString(span.knownLookupKey) ||
      !isOptionalString(span.frequencyLookupKey))
  ) {
    errors.push(`${label} has invalid analyzer lookup-key fields.`);
  }

  return errors;
}

function isOptionalString(value) {
  return value == null || typeof value === 'string';
}

function preserveReaderSpan(span) {
  return {
    ...span,
    start: span.start,
    end: span.end,
    surface: span.surface,
    displayRole: span.displayRole,
    lexicalType: span.lexicalType ?? null,
    colorPolicy: span.colorPolicy ?? null,
    unknownColorPolicy: span.unknownColorPolicy ?? null,
    knownLookupKey: span.knownLookupKey ?? null,
    frequencyLookupKey: span.frequencyLookupKey ?? null,
    headword: span.headword ?? null,
    grammarId: span.grammarId ?? null,
    confidence:
      typeof span.confidence === 'number' ? span.confidence : null,
    countsForComprehension: span.countsForComprehension,
    showInNewWords: span.showInNewWords,
    eligibleForMining: span.eligibleForMining,
    sourceSpanIds: Array.isArray(span.sourceSpanIds)
      ? [...span.sourceSpanIds]
      : [],
    sourceLayer: span.sourceLayer ?? null,
    projectionStatus: span.projectionStatus ?? null,
    correctionId: span.correctionId ?? null,
    correctionScope: span.correctionScope ?? null,
    correctionAction: span.correctionAction ?? null,
    hostLookupKey: span.hostLookupKey ?? null,
    grammarFocusRanges: Array.isArray(span.grammarFocusRanges)
      ? span.grammarFocusRanges.map((range) => ({ ...range }))
      : [],

    // Mechanical compatibility aliases only. No missing key is derived.
    dictionaryForm: span.knownLookupKey ?? '',
    analysisSource: 'jp-analyzer-reader-spans',
    authoritativeRange: true
  };
}

function summarizeReaderSpans(words) {
  const summary = {
    total: words.length,
    lexical: 0,
    compounds: 0,
    grammar: 0,
    functions: 0,
    names: 0,
    punctuation: 0,
    unresolved: 0,
    corrected: 0,
    comprehension: 0,
    newWords: 0,
    miningEligible: 0
  };

  for (const word of words) {
    if (word.displayRole === 'lexical') summary.lexical += 1;
    else if (word.displayRole === 'lexical-compound') summary.compounds += 1;
    else if (word.displayRole === 'learnable-grammar') summary.grammar += 1;
    else if (word.displayRole === 'function') summary.functions += 1;
    else if (word.displayRole === 'name') summary.names += 1;
    else if (word.displayRole === 'punctuation') summary.punctuation += 1;
    else if (word.displayRole === 'unresolved') summary.unresolved += 1;

    if (word.projectionStatus === 'user-corrected') summary.corrected += 1;
    if (word.countsForComprehension) summary.comprehension += 1;
    if (word.showInNewWords) summary.newWords += 1;
    if (word.eligibleForMining) summary.miningEligible += 1;
  }

  return summary;
}
````

### `novel-audio-miner/src/lib/ankiConnect.js`

- Purpose: Anki integration.
- Size: 1720 bytes
- SHA-256: `a32bb91991fa25724ff32c541a4e76233224eded2744e63af41a5ef9edc5a1c0`

````javascript
/**
 * AnkiConnect client.
 *
 * Responsibility:
 * - Send JSON-RPC style requests to the local AnkiConnect endpoint.
 * - Check AnkiConnect availability.
 * - Find the latest note of a configured note type.
 * - Update note fields.
 *
 * Media upload/download orchestration belongs in Reader.jsx and enrichment helpers.
 */

const ANKI_URL = 'http://127.0.0.1:8765';
const ANKI_CONNECT_VERSION = 6;

function escapeAnkiQueryValue(value) {
  return String(value || '').replace(/"/g, '\"');
}

export async function ankiRequest(action, params = {}) {
  const response = await fetch(ANKI_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action,
      version: ANKI_CONNECT_VERSION,
      params
    })
  });

  if (!response.ok) throw new Error(`AnkiConnect HTTP ${response.status}`);

  const data = await response.json();
  if (data.error) throw new Error(data.error);

  return data.result;
}

export async function checkAnkiConnect() {
  const version = await ankiRequest('version');
  return { ok: true, version };
}

export async function findLatestNote(noteType = 'Kiku') {
  const safeNoteType = escapeAnkiQueryValue(noteType);
  const query = `note:"${safeNoteType}" added:1`;
  const ids = await ankiRequest('findNotes', { query });

  if (!ids.length) return { query, note: null, ids: [] };

  const sorted = [...ids].sort((a, b) => Number(b) - Number(a));
  const notes = await ankiRequest('notesInfo', { notes: [sorted[0]] });

  return { query, note: notes[0] || null, ids: sorted };
}

export async function updateNoteFields(noteId, fields) {
  return ankiRequest('updateNoteFields', {
    note: {
      id: noteId,
      fields
    }
  });
}
````

### `novel-audio-miner/src/lib/colorSource.js`

- Purpose: JavaScript/React source.
- Size: 1211 bytes
- SHA-256: `539b933deb2418ad079fbd44f38f36caae2d2059e1ee149631d7bd66510b1066`

````javascript
/** Visible presentation ownership. JP Analyzer is the only linguistic source. */
export const COLOR_SOURCES = Object.freeze({
  JP_ANALYZER: 'jp-analyzer',
  PLAIN_TEXT: 'plain-text'
});
export const DEFAULT_COLOR_SOURCE = COLOR_SOURCES.JP_ANALYZER;
const VALID_COLOR_SOURCES = new Set(Object.values(COLOR_SOURCES));
export function normalizeColorSource(value) {
  return VALID_COLOR_SOURCES.has(value) ? value : DEFAULT_COLOR_SOURCE;
}
export function resolveVisibleColourSource({ requestedSource, analyzerReady, analyzerWords }) {
  const requested = normalizeColorSource(requestedSource);
  if (requested === COLOR_SOURCES.PLAIN_TEXT) return { requestedSource: requested, activeSource: COLOR_SOURCES.PLAIN_TEXT, words: [], neutralFallback: false, reason: 'plain-text-selected' };
  if (analyzerReady && Array.isArray(analyzerWords) && analyzerWords.length > 0) return { requestedSource: requested, activeSource: COLOR_SOURCES.JP_ANALYZER, words: analyzerWords, neutralFallback: false, reason: 'authoritative-reader-spans-ready' };
  return { requestedSource: requested, activeSource: COLOR_SOURCES.PLAIN_TEXT, words: [], neutralFallback: true, reason: 'analyzer-unavailable-or-invalid' };
}
````

### `novel-audio-miner/src/lib/debugReportV2.js`

- Purpose: JavaScript/React source.
- Size: 6069 bytes
- SHA-256: `c337caac8823febe71ded5822013f37738d20ccd3cc57888688d3be261edc949`

````javascript
export const DEBUG_REPORT_SCHEMA_VERSION = '2.0';

function clone(value) {
  if (value == null) return value;
  try { return structuredClone(value); }
  catch {
    try { return JSON.parse(JSON.stringify(value)); }
    catch { return null; }
  }
}

function diagnosticId(now = new Date()) {
  const stamp = now.toISOString().replace(/[-:.TZ]/g, '').slice(0, 14);
  const random = Math.random().toString(36).slice(2, 10);
  return `nam-${stamp}-${random}`;
}

function compactBookSummary(book) {
  return {
    id: book?.id || '',
    fileName: book?.fileName || '',
    title: book?.title || '',
    author: book?.author || '',
    tocCount: book?.toc?.length || 0,
    chapterCount: book?.chapters?.length || 0,
    totalItems: book?.debug?.totalItems ?? null,
    sentenceCount: book?.debug?.sentenceCount ?? null,
    imageCount: book?.debug?.imageCount ?? null
  };
}

function readerContract(reader) {
  return {
    valid: Boolean(reader?.valid),
    schemaVersion: reader?.schemaVersion || '',
    errors: clone(reader?.errors || []),
    reconstructsSource: Boolean(reader?.valid),
    spanCount: reader?.words?.length || 0,
    summary: clone(reader?.summary || null),
    correctionAware: Boolean(reader?.correctionAware)
  };
}

export function buildDebugReportV2({
  application = {}, book = null, reader = {}, scene = {}, adjacentScenes = [],
  analyzerShadow = {}, analyzerReader = {}, analyzerResult = null,
  metadataLease = null, metadataLeaseMs = null,
  presentationSpans = [], learning = {}, selection = {}, mining = {},
  prefetchTargets = [], includeFullParserInventory = false, now = new Date()
} = {}) {
  const result = analyzerResult || {};
  const report = {
    report: {
      schemaVersion: DEBUG_REPORT_SCHEMA_VERSION,
      generatedAt: now.toISOString(),
      diagnosticId: diagnosticId(now)
    },
    application: clone(application),
    book: {
      summary: compactBookSummary(book),
      fullParserInventoryIncluded: Boolean(includeFullParserInventory)
    },
    reader: clone(reader),
    scene: {
      current: clone(scene),
      adjacent: clone(adjacentScenes)
    },
    analyzer: {
      health: {
        status: analyzerShadow?.status || 'idle',
        error: analyzerShadow?.error?.message || analyzerShadow?.error || null,
        analyzerVersion: analyzerShadow?.analyzerVersion || result?.analyzerVersion || null,
        readerSpanSchemaVersion: analyzerShadow?.readerSpanSchemaVersion || result?.readerSpanSchemaVersion || null,
        readerCandidateSchemaVersion: result?.readerCandidateSchemaVersion || null,
        correctionRevision: analyzerShadow?.correctionRevision || result?.correctionRevision || null
      },
      contract: readerContract(analyzerReader),
      readerSpans: clone(result?.readerSpans || []),
      readerSelection: clone(result?.readerSelection || null),
      appliedCorrections: clone(
        result?.appliedReaderCorrections ||
        result?.readerSelection?.appliedCorrections ||
        []
      )
    },
    cache: {
      resultSource: analyzerShadow?.source || null,
      requestDurationMs: analyzerShadow?.elapsedMs ?? null,
      cacheKey: analyzerShadow?.cacheKey || null,
      cacheIdentity: analyzerShadow?.cacheIdentity || null,
      cacheReason: analyzerShadow?.cacheReason || null,
      inFlightRequestCount: analyzerShadow?.inFlightRequestCount ?? 0,
      metadataLease: {
        valid: Boolean(metadataLease),
        verifiedAt: metadataLease?.verifiedAt ?? null,
        ageMs: metadataLease?.verifiedAt != null ? Math.max(0, Date.now() - metadataLease.verifiedAt) : null,
        durationMs: metadataLeaseMs,
        analyzerVersion: metadataLease?.analyzerVersion || null,
        readerSpanSchemaVersion: metadataLease?.readerSpanSchemaVersion || null,
        correctionRevision: metadataLease?.correctionRevision || null
      }
    },
    prefetch: {
      status: analyzerShadow?.prefetchStatus || 'idle',
      targetCount: analyzerShadow?.prefetchTargetCount ?? 0,
      completedCount: analyzerShadow?.prefetchCompletedCount ?? 0,
      failureCount: analyzerShadow?.prefetchFailedCount ?? 0,
      targets: clone(prefetchTargets)
    },
    presentation: { spans: clone(presentationSpans) },
    learning: {
      available: Boolean(learning?.available),
      source: learning?.source || null,
      comprehension: clone(learning?.comprehension || null),
      newWords: clone(learning?.newWords || [])
    },
    selection: {
      raw: selection?.raw || '',
      readerContext: clone(selection?.readerContext || null),
      actionState: clone(selection?.actionState || null),
      issue: selection?.issue || null
    },
    mining: {
      candidate: clone(mining?.candidate || null),
      lookupIdentity: mining?.lookupIdentity || null,
      debug: clone(mining?.debug || null),
      enrichment: clone(mining?.enrichment || null),
      working: Boolean(mining?.working)
    },
    epub: {
      parserSummary: {
        ...compactBookSummary(book),
        currentSource: clone(scene?.parserDebug || null)
      },
      currentSource: clone(scene),
      fullInventory: includeFullParserInventory ? clone(book?.debug || null) : null
    }
  };
  return report;
}

export function buildDiagnosticSummaryV2(report) {
  const r = report || {};
  return [
    `diagnostic=${r.report?.diagnosticId || '-'}`,
    `scene=${r.reader?.sceneNumber || '-'}/${r.reader?.totalScenes || '-'}`,
    `analyzer=${r.analyzer?.health?.status || 'idle'}`,
    `contract=${r.analyzer?.contract?.valid ? 'valid' : 'invalid'}`,
    `source=${r.cache?.resultSource || '-'}`,
    `durationMs=${r.cache?.requestDurationMs ?? '-'}`,
    `prefetch=${r.prefetch?.status || 'idle'} ${r.prefetch?.completedCount || 0}/${r.prefetch?.targetCount || 0}`,
    `selection=${r.selection?.readerContext?.surface || r.selection?.raw || '-'}`,
    `mining=${r.mining?.debug?.status || 'idle'}`
  ].join('; ');
}
````

### `novel-audio-miner/src/lib/dictionaryDetection.js`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 17790 bytes
- SHA-256: `25ff52f8388c33bf475af42463bf68f40486d6f76bba5a23fa6c40feb725d603`

````javascript
export const DICTIONARY_TYPES = {
  TERM: 'term',
  EXPRESSION: 'expression',
  NAME: 'name',
  GRAMMAR: 'grammar',
  FREQUENCY: 'frequency',
  KANJI: 'kanji',
  PITCH: 'pitch',
  UNKNOWN: 'unknown'
};

export const ADAPTERS = {
  YOMITAN_TERM_V3: 'yomitan-term-v3',
  YOMITAN_EXPRESSION_V3: 'yomitan-expression-v3',
  YOMITAN_NAME_V3: 'yomitan-name-v3',
  YOMITAN_GRAMMAR_V3: 'yomitan-grammar-v3',
  UNSUPPORTED: 'unsupported'
};

const CLASSIFIABLE_TYPES = [
  DICTIONARY_TYPES.TERM,
  DICTIONARY_TYPES.EXPRESSION,
  DICTIONARY_TYPES.NAME,
  DICTIONARY_TYPES.GRAMMAR,
  DICTIONARY_TYPES.FREQUENCY,
  DICTIONARY_TYPES.KANJI,
  DICTIONARY_TYPES.PITCH
];

export function normalizeText(value) {
  return String(value || '').normalize('NFKC').trim();
}

export function createDictionaryId(title = 'dictionary', fileName = '') {
  const base = normalizeText(title || fileName || 'dictionary')
    .replace(/[^\p{L}\p{N}]+/gu, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 80) || 'dictionary';
  return `${base}-${Date.now()}`;
}

function addEvidence(state, type, points, reason, source = 'content') {
  if (!state.scores[type]) state.scores[type] = 0;
  state.scores[type] += points;
  state.evidence.push({ type, points, reason, source });
}

function textIncludesAny(text, needles) {
  const value = normalizeText(text).toLowerCase();
  return needles.some(needle => value.includes(String(needle).toLowerCase()));
}

function flattenGlossaryText(value, depth = 0) {
  if (depth > 4 || value == null) return '';
  if (typeof value === 'string' || typeof value === 'number') return String(value);
  if (Array.isArray(value)) return value.map(item => flattenGlossaryText(item, depth + 1)).join(' ');
  if (typeof value === 'object') return Object.values(value).map(item => flattenGlossaryText(item, depth + 1)).join(' ');
  return '';
}

export function detectYomitanTermRowShape(row) {
  if (!Array.isArray(row)) return { supported: false, reason: 'Row is not an array.' };
  if (row.length < 6) return { supported: false, reason: `Row has ${row.length} columns; expected at least 6.` };
  if (typeof row[0] !== 'string') return { supported: false, reason: 'Column 0 is not a string expression.' };
  if (!Array.isArray(row[5])) return { supported: false, reason: 'Column 5 is not glossary/readings array.' };
  return {
    supported: true,
    reason: 'Looks like a Yomitan term_bank row.',
    length: row.length,
    columns: row.map(value => Array.isArray(value)
      ? `array(${value.length})`
      : value && typeof value === 'object' ? 'object' : typeof value)
  };
}

function analyzeSampleRows(sampleRows = []) {
  const termRows = sampleRows
    .filter(item => item?.type === 'term_bank' && Array.isArray(item.row))
    .map(item => item.row)
    .slice(0, 100);

  const metrics = {
    sampledTermRows: termRows.length,
    validTermRows: 0,
    nameTaggedRows: 0,
    grammarTaggedRows: 0,
    expressionTaggedRows: 0,
    grammarPatternRows: 0,
    multiwordRows: 0,
    singleCharacterRows: 0,
    metadataLikeRows: 0
  };

  const nameTagPattern = /(?:surname|given|masc|fem|person|place|station|company|organization|product|work|unclass|名|姓|地名|人名)/i;
  const grammarTagPattern = /(?:grammar|文法|文型|助詞|助動詞|接続|bunpro|dojg)/i;
  const expressionTagPattern = /(?:expression|表現|慣用|成句|連語|idiom|phrase)/i;
  const grammarHeadwordPattern = /[〜～~]|(?:こと|もの|わけ|はず|よう|ため|ところ|うち|まま|つもり|によって|に対して|に関して|として|てしまう|なければ|ではない|のでは|という)$/;

  for (const row of termRows) {
    const shape = detectYomitanTermRowShape(row);
    if (!shape.supported) continue;
    metrics.validTermRows += 1;
    const expression = normalizeText(row[0]);
    const tags = `${row[2] || ''} ${row[7] || ''}`;
    const glossary = flattenGlossaryText(row[5]);
    const combined = `${tags} ${glossary}`;

    if (nameTagPattern.test(tags)) metrics.nameTaggedRows += 1;
    if (grammarTagPattern.test(combined)) metrics.grammarTaggedRows += 1;
    if (expressionTagPattern.test(combined)) metrics.expressionTaggedRows += 1;
    if (grammarHeadwordPattern.test(expression)) metrics.grammarPatternRows += 1;
    if (/\s/.test(expression) || expression.length >= 5) metrics.multiwordRows += 1;
    if (expression.length === 1) metrics.singleCharacterRows += 1;
    if (row.length <= 4 || (typeof row[2] === 'number' && typeof row[3] !== 'string')) metrics.metadataLikeRows += 1;
  }

  return metrics;
}

function rankScores(scores) {
  return CLASSIFIABLE_TYPES
    .map(type => ({ type, score: Number(scores[type] || 0) }))
    .sort((a, b) => b.score - a.score);
}

function getConfidence(ranked, sampleCount) {
  const top = ranked[0] || { score: 0 };
  const second = ranked[1] || { score: 0 };
  const margin = top.score - second.score;
  if (top.score >= 110 && margin >= 35 && sampleCount >= 5) return 'high';
  if (top.score >= 70 && margin >= 15) return 'medium';
  return 'low';
}

function adapterForType(type) {
  if (type === DICTIONARY_TYPES.TERM) return ADAPTERS.YOMITAN_TERM_V3;
  if (type === DICTIONARY_TYPES.EXPRESSION) return ADAPTERS.YOMITAN_EXPRESSION_V3;
  if (type === DICTIONARY_TYPES.NAME) return ADAPTERS.YOMITAN_NAME_V3;
  if (type === DICTIONARY_TYPES.GRAMMAR) return ADAPTERS.YOMITAN_GRAMMAR_V3;
  return ADAPTERS.UNSUPPORTED;
}

export function classifyDictionaryEvidence(summary = {}, sampleRows = []) {
  const state = {
    scores: Object.fromEntries(CLASSIFIABLE_TYPES.map(type => [type, 0])),
    evidence: []
  };

  const termBankFiles = summary.termBankFiles?.length || 0;
  const termMetaBankFiles = summary.termMetaBankFiles?.length || 0;
  const kanjiBankFiles = summary.kanjiBankFiles?.length || 0;
  const metadataText = [
    summary.index?.title,
    summary.index?.description,
    summary.index?.author,
    summary.index?.revision,
    summary.fileName
  ].filter(Boolean).join(' ');

  // Structural evidence has the highest reliability.
  if (termBankFiles > 0) addEvidence(state, DICTIONARY_TYPES.TERM, 60, `${termBankFiles} term_bank file(s) found.`, 'structure');
  if (kanjiBankFiles > 0) addEvidence(state, DICTIONARY_TYPES.KANJI, termBankFiles > 0 ? 80 : 170, `${kanjiBankFiles} kanji_bank file(s) found.`, 'structure');
  if (termMetaBankFiles > 0) {
    if (termBankFiles === 0) addEvidence(state, DICTIONARY_TYPES.FREQUENCY, 150, 'term_meta_bank files found without term_bank content.', 'structure');
    else addEvidence(state, DICTIONARY_TYPES.FREQUENCY, 15, 'term_meta_bank files coexist with term entries; weak metadata signal only.', 'structure');
  }

  const metrics = analyzeSampleRows(sampleRows);
  if (metrics.validTermRows > 0) addEvidence(state, DICTIONARY_TYPES.TERM, 35, `${metrics.validTermRows}/${metrics.sampledTermRows} sampled rows match Yomitan term schema.`, 'row-shape');

  const denominator = Math.max(metrics.validTermRows, 1);
  const nameRatio = metrics.nameTaggedRows / denominator;
  const grammarRatio = (metrics.grammarTaggedRows + metrics.grammarPatternRows) / denominator;
  const expressionRatio = (metrics.expressionTaggedRows + metrics.multiwordRows * 0.35) / denominator;

  if (metrics.nameTaggedRows >= 3 && nameRatio >= 0.3) addEvidence(state, DICTIONARY_TYPES.NAME, 110, `${metrics.nameTaggedRows}/${denominator} sampled rows contain name-type evidence.`, 'sample-content');
  else if (metrics.nameTaggedRows > 0) addEvidence(state, DICTIONARY_TYPES.NAME, 25, `${metrics.nameTaggedRows} sampled row(s) contain name-type tags.`, 'sample-content');

  if ((metrics.grammarTaggedRows >= 2 || metrics.grammarPatternRows >= 3) && grammarRatio >= 0.25) addEvidence(state, DICTIONARY_TYPES.GRAMMAR, 115, 'Sampled headwords/tags show repeated grammar-pattern evidence.', 'sample-content');
  else if (metrics.grammarTaggedRows || metrics.grammarPatternRows) addEvidence(state, DICTIONARY_TYPES.GRAMMAR, 25, 'Some sampled rows look grammar-related.', 'sample-content');

  if ((metrics.expressionTaggedRows >= 2 || metrics.multiwordRows >= 4) && expressionRatio >= 0.3) addEvidence(state, DICTIONARY_TYPES.EXPRESSION, 105, 'Sampled entries show repeated fixed-expression/phrase evidence.', 'sample-content');
  else if (metrics.expressionTaggedRows || metrics.multiwordRows) addEvidence(state, DICTIONARY_TYPES.EXPRESSION, 18, 'Some sampled entries look expression-like.', 'sample-content');

  // Metadata is a supporting hint, never sufficient to override contradictory bank structure by itself.
  if (textIncludesAny(metadataText, ['jmnedict', 'proper name', 'proper names', '人名辞典', '姓名'])) addEvidence(state, DICTIONARY_TYPES.NAME, 55, 'Metadata suggests a proper-name dictionary.', 'metadata');
  if (textIncludesAny(metadataText, ['bunpro', 'dojg', 'grammar dictionary', '文法辞典', '文型辞典', '文法', '文型'])) addEvidence(state, DICTIONARY_TYPES.GRAMMAR, 55, 'Metadata suggests a grammar dictionary.', 'metadata');
  if (textIncludesAny(metadataText, ['expression dictionary', '表現辞典', '実用日本語表現', '慣用句辞典', 'idiom dictionary'])) addEvidence(state, DICTIONARY_TYPES.EXPRESSION, 55, 'Metadata suggests an expression dictionary.', 'metadata');
  if (textIncludesAny(metadataText, ['frequency dictionary', 'frequency list', 'frequency rank', '頻度辞典', '頻度リスト'])) addEvidence(state, DICTIONARY_TYPES.FREQUENCY, 45, 'Metadata explicitly describes a frequency resource.', 'metadata');
  if (textIncludesAny(metadataText, ['pitch accent', 'アクセント辞典', '発音アクセント'])) addEvidence(state, DICTIONARY_TYPES.PITCH, 85, 'Metadata explicitly describes pitch-accent data.', 'metadata');
  if (textIncludesAny(metadataText, ['kanjidic', 'kanji dictionary', '漢字辞典'])) addEvidence(state, DICTIONARY_TYPES.KANJI, 55, 'Metadata explicitly describes a kanji dictionary.', 'metadata');

  // Prevent normal term dictionaries from being misclassified by a weak metadata word.
  if (termBankFiles > 0 && kanjiBankFiles === 0) addEvidence(state, DICTIONARY_TYPES.TERM, 20, 'Term banks are present and no kanji_bank files exist.', 'structure');
  if (termBankFiles > 0 && termMetaBankFiles === 0) addEvidence(state, DICTIONARY_TYPES.TERM, 15, 'Term content exists without metadata-only bank structure.', 'structure');

  const ranked = rankScores(state.scores);
  let detectedType = ranked[0]?.type || DICTIONARY_TYPES.UNKNOWN;
  const confidence = getConfidence(ranked, metrics.sampledTermRows);

  if ((ranked[0]?.score || 0) < 35) detectedType = DICTIONARY_TYPES.UNKNOWN;

  const supported = [
    DICTIONARY_TYPES.TERM,
    DICTIONARY_TYPES.EXPRESSION,
    DICTIONARY_TYPES.NAME,
    DICTIONARY_TYPES.GRAMMAR
  ].includes(detectedType) && confidence !== 'low';

  const adapter = supported ? adapterForType(detectedType) : ADAPTERS.UNSUPPORTED;
  const top = ranked[0] || { type: DICTIONARY_TYPES.UNKNOWN, score: 0 };
  const second = ranked[1] || { type: DICTIONARY_TYPES.UNKNOWN, score: 0 };
  const reason = detectedType === DICTIONARY_TYPES.UNKNOWN
    ? 'Insufficient structural/content evidence to classify safely.'
    : `${detectedType} scored ${top.score}; next candidate ${second.type} scored ${second.score}.`;

  return {
    type: detectedType,
    supported,
    adapter,
    confidence,
    reason,
    scores: state.scores,
    rankedScores: ranked,
    evidence: state.evidence.sort((a, b) => Math.abs(b.points) - Math.abs(a.points)),
    metrics
  };
}

export function detectDictionaryType(summary = {}, sampleRows = []) {
  return classifyDictionaryEvidence(summary, sampleRows);
}

function baseRow(row, dictionaryTitle, priority, dictionaryId, type, adapter) {
  const shape = detectYomitanTermRowShape(row);
  if (!shape.supported) return null;
  const text = normalizeText(row[0]);
  if (!text) return null;
  const tags = typeof row[2] === 'string' ? row[2].split(' ').filter(Boolean) : [];
  return { text, reading: normalizeText(row[1]), type, sourceDictionary: dictionaryTitle, dictionaryId, tags, rules: row[3] || '', score: Number(row[4] || 0), sequence: row[6] ?? null, termTags: row[7] || '', priority, confidence: 'dictionary', adapter };
}

function inferNameType(tags = []) {
  const joined = Array.isArray(tags) ? tags.join(' ') : String(tags || '');
  if (/place|station|company|organization|product|work/i.test(joined)) return 'place-or-organization';
  if (/surname|given|masc|fem|person/i.test(joined)) return 'person';
  if (/unclass/i.test(joined)) return 'unclassified-name';
  return 'name';
}

function inferGrammarType(dictionaryTitle = '', termTags = '', tags = []) {
  const haystack = `${dictionaryTitle} ${termTags} ${Array.isArray(tags) ? tags.join(' ') : tags}`.toLowerCase();
  if (haystack.includes('bunpro')) return 'bunpro-grammar-point';
  if (haystack.includes('dojg') || haystack.includes('文法辞典')) return 'dojg-grammar-item';
  if (haystack.includes('文型') || haystack.includes('grammar') || haystack.includes('handbook')) return 'grammar-pattern';
  return 'grammar-expression';
}

export function normalizeYomitanTermRow(row, dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '') { return baseRow(row, dictionaryTitle, priority, dictionaryId, DICTIONARY_TYPES.TERM, ADAPTERS.YOMITAN_TERM_V3); }
export function normalizeYomitanExpressionRow(row, dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '') { const entry = baseRow(row, dictionaryTitle, priority, dictionaryId, DICTIONARY_TYPES.EXPRESSION, ADAPTERS.YOMITAN_EXPRESSION_V3); return entry ? { ...entry, expressionType: 'practical-expression' } : null; }
export function normalizeYomitanNameRow(row, dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '') { const entry = baseRow(row, dictionaryTitle, priority, dictionaryId, DICTIONARY_TYPES.NAME, ADAPTERS.YOMITAN_NAME_V3); if (!entry) return null; const readings = Array.isArray(row[5]) ? row[5].map(normalizeText).filter(Boolean) : []; return { ...entry, reading: entry.reading || readings[0] || '', readings, nameType: inferNameType(entry.tags) }; }
export function normalizeYomitanGrammarRow(row, dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '') { const entry = baseRow(row, dictionaryTitle, priority, dictionaryId, DICTIONARY_TYPES.GRAMMAR, ADAPTERS.YOMITAN_GRAMMAR_V3); return entry ? { ...entry, grammarType: inferGrammarType(dictionaryTitle, entry.termTags, entry.tags) } : null; }

function normalizeRows(rows, fn, dictionaryTitle, priority, dictionaryId, limit = Infinity) {
  const output = [];
  for (const row of rows || []) {
    const item = fn(row, dictionaryTitle, priority, dictionaryId);
    if (item) output.push(item);
    if (output.length >= limit) break;
  }
  return output;
}

export function normalizeYomitanTermRows(rows = [], dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '', limit = Infinity) { return normalizeRows(rows, normalizeYomitanTermRow, dictionaryTitle, priority, dictionaryId, limit); }
export function normalizeYomitanExpressionRows(rows = [], dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '', limit = Infinity) { return normalizeRows(rows, normalizeYomitanExpressionRow, dictionaryTitle, priority, dictionaryId, limit); }
export function normalizeYomitanNameRows(rows = [], dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '', limit = Infinity) { return normalizeRows(rows, normalizeYomitanNameRow, dictionaryTitle, priority, dictionaryId, limit); }
export function normalizeYomitanGrammarRows(rows = [], dictionaryTitle = 'dictionary', priority = 1, dictionaryId = '', limit = Infinity) { return normalizeRows(rows, normalizeYomitanGrammarRow, dictionaryTitle, priority, dictionaryId, limit); }

export function createDictionaryProfile(summary = {}, sampleRows = [], priority = 1) {
  const title = summary.index?.title || summary.index?.name || summary.fileName || 'Dictionary';
  const detected = classifyDictionaryEvidence(summary, sampleRows);
  const sampleTermRows = sampleRows.filter(item => item?.type === 'term_bank').map(item => item.row);
  const dictionaryId = summary.dictionaryId || createDictionaryId(title, summary.fileName || '');
  const sampleNormalizedEntries = detected.supported && detected.adapter === ADAPTERS.YOMITAN_TERM_V3
    ? normalizeYomitanTermRows(sampleTermRows, title, priority, dictionaryId, 5)
    : detected.supported && detected.adapter === ADAPTERS.YOMITAN_EXPRESSION_V3
      ? normalizeYomitanExpressionRows(sampleTermRows, title, priority, dictionaryId, 5)
      : detected.supported && detected.adapter === ADAPTERS.YOMITAN_NAME_V3
        ? normalizeYomitanNameRows(sampleTermRows, title, priority, dictionaryId, 5)
        : detected.supported && detected.adapter === ADAPTERS.YOMITAN_GRAMMAR_V3
          ? normalizeYomitanGrammarRows(sampleTermRows, title, priority, dictionaryId, 5)
          : [];

  return {
    id: dictionaryId,
    title,
    fileName: summary.fileName || '',
    format: summary.index?.format || null,
    revision: summary.index?.revision || '',
    detectedType: detected.type,
    supported: detected.supported,
    adapter: detected.adapter,
    confidence: detected.confidence,
    reason: detected.reason,
    scores: detected.scores,
    rankedScores: detected.rankedScores,
    categoryEvidence: detected.evidence,
    sampleMetrics: detected.metrics,
    priority,
    termBankFiles: summary.termBankFiles?.length || 0,
    termMetaBankFiles: summary.termMetaBankFiles?.length || 0,
    tagBankFiles: summary.tagBankFiles?.length || 0,
    kanjiBankFiles: summary.kanjiBankFiles?.length || 0,
    estimatedRowsByType: summary.estimatedRowsByType || {},
    rowShape: sampleTermRows[0] ? detectYomitanTermRowShape(sampleTermRows[0]) : null,
    sampleNormalizedEntries
  };
}
````

### `novel-audio-miner/src/lib/dictionaryLookup.js`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 35341 bytes
- SHA-256: `83a45364c35e0e388c98b95b8809d396facb01a0829ba64c813c4f3f741a1159`

````javascript
export function normalizeDictionaryText(value) { return String(value || '').normalize('NFKC').trim(); }
function normalizeDefinitions(value) { if (!value) return []; if (Array.isArray(value)) return value; return [value]; }
function tagsFrom(value) { return Array.isArray(value) ? value : typeof value === 'string' ? value.split(' ').filter(Boolean) : []; }
function inferNameType(tags = []) { const s = Array.isArray(tags) ? tags.join(' ') : String(tags || ''); if (/place|station|company|organization|product|work/i.test(s)) return 'place-or-organization'; if (/surname|given|masc|fem|person/i.test(s)) return 'person'; if (/unclass/i.test(s)) return 'unclassified-name'; return 'name'; }
function inferGrammarType(title = '', termTags = '', tags = []) { const s = `${title} ${termTags} ${Array.isArray(tags) ? tags.join(' ') : tags}`.toLowerCase(); if (s.includes('bunpro')) return 'bunpro-grammar-point'; if (s.includes('dojg') || s.includes('文法辞典')) return 'dojg-grammar-item'; if (s.includes('文型') || s.includes('grammar') || s.includes('handbook')) return 'grammar-pattern'; return 'grammar-expression'; }

export function normalizeDictionaryEntry(rawEntry, fallbackSource = 'unknown') {
  const term = normalizeDictionaryText(rawEntry.term || rawEntry.expression || rawEntry.text || rawEntry[0]);
  if (!term) return null;
  const reading = normalizeDictionaryText(rawEntry.reading || rawEntry.kana || rawEntry[1]);
  const source = normalizeDictionaryText(rawEntry.source || rawEntry.sourceDictionary || fallbackSource || 'unknown');
  return { term, reading, source, sourceDictionary: rawEntry.sourceDictionary || source, dictionaryId: rawEntry.dictionaryId || '', dictionaryPriority: Number(rawEntry.dictionaryPriority ?? rawEntry.priority ?? 9999), tags: tagsFrom(rawEntry.tags), rules: rawEntry.rules || '', score: Number(rawEntry.score || rawEntry.popularity || 0), definitions: normalizeDefinitions(rawEntry.definitions || rawEntry.glossary || rawEntry[5]), sequence: rawEntry.sequence ?? rawEntry.seq ?? rawEntry[6] ?? null, termTags: rawEntry.termTags || rawEntry[7] || '', dictionaryType: rawEntry.dictionaryType || rawEntry.type || 'term', nameType: rawEntry.nameType || '', grammarType: rawEntry.grammarType || '', expressionType: rawEntry.expressionType || '', readings: Array.isArray(rawEntry.readings) ? rawEntry.readings : [], raw: rawEntry.raw || rawEntry };
}

function convertRow(row, dictionaryTitle, dictionaryId, dictionaryPriority, dictionaryType) {
  if (!Array.isArray(row)) return null;
  const tags = tagsFrom(row[2]);
  const readings = Array.isArray(row[5]) ? row[5].map(normalizeDictionaryText).filter(Boolean) : [];
  const extra = dictionaryType === 'name' ? { nameType: inferNameType(tags), readings, definitions: readings }
    : dictionaryType === 'grammar' ? { grammarType: inferGrammarType(dictionaryTitle, row[7] || '', tags) }
      : dictionaryType === 'expression' ? { expressionType: 'practical-expression' }
        : {};
  return normalizeDictionaryEntry({ term: row[0], reading: row[1] || (dictionaryType === 'name' ? readings[0] : '') || '', tags, rules: row[3] || '', score: Number(row[4] || 0), definitions: Array.isArray(row[5]) ? row[5] : row[5] ? [row[5]] : [], sequence: row[6] ?? null, termTags: row[7] || '', source: dictionaryTitle, sourceDictionary: dictionaryTitle, dictionaryId, dictionaryPriority, dictionaryType, raw: row, ...extra }, dictionaryTitle);
}
export function convertYomitanTermBankRow(row, dictionaryTitle = 'yomitan-import', dictionaryId = '', dictionaryPriority = 9999) { return convertRow(row, dictionaryTitle, dictionaryId, dictionaryPriority, 'term'); }
export function convertYomitanExpressionBankRow(row, dictionaryTitle = 'yomitan-expression-import', dictionaryId = '', dictionaryPriority = 9999) { return convertRow(row, dictionaryTitle, dictionaryId, dictionaryPriority, 'expression'); }
export function convertYomitanNameBankRow(row, dictionaryTitle = 'yomitan-name-import', dictionaryId = '', dictionaryPriority = 9999) { return convertRow(row, dictionaryTitle, dictionaryId, dictionaryPriority, 'name'); }
export function convertYomitanGrammarBankRow(row, dictionaryTitle = 'yomitan-grammar-import', dictionaryId = '', dictionaryPriority = 9999) { return convertRow(row, dictionaryTitle, dictionaryId, dictionaryPriority, 'grammar'); }
export function convertYomitanTermBankRows(rows = [], dictionaryTitle = 'yomitan-import', dictionaryId = '', dictionaryPriority = 9999) { return rows.map(row => convertYomitanTermBankRow(row, dictionaryTitle, dictionaryId, dictionaryPriority)).filter(Boolean); }
export function convertYomitanExpressionBankRows(rows = [], dictionaryTitle = 'yomitan-expression-import', dictionaryId = '', dictionaryPriority = 9999) { return rows.map(row => convertYomitanExpressionBankRow(row, dictionaryTitle, dictionaryId, dictionaryPriority)).filter(Boolean); }
export function convertYomitanNameBankRows(rows = [], dictionaryTitle = 'yomitan-name-import', dictionaryId = '', dictionaryPriority = 9999) { return rows.map(row => convertYomitanNameBankRow(row, dictionaryTitle, dictionaryId, dictionaryPriority)).filter(Boolean); }
export function convertYomitanGrammarBankRows(rows = [], dictionaryTitle = 'yomitan-grammar-import', dictionaryId = '', dictionaryPriority = 9999) { return rows.map(row => convertYomitanGrammarBankRow(row, dictionaryTitle, dictionaryId, dictionaryPriority)).filter(Boolean); }

export function buildDictionaryIndex(entries = []) {
  const index = { entries: [], byTerm: new Map(), byFirstChar: new Map(), sources: new Set(), builtAt: new Date().toISOString() };
  const normalizedEntries = entries.map(entry => entry?.term ? normalizeDictionaryEntry(entry, entry.source || entry.sourceDictionary || 'imported') : entry).filter(entry => entry?.term).sort((a,b)=>(a.dictionaryPriority??9999)-(b.dictionaryPriority??9999)||b.score-a.score);
  for (const entry of normalizedEntries) { index.entries.push(entry); index.sources.add(entry.source || entry.sourceDictionary || 'unknown'); if (!index.byTerm.has(entry.term)) index.byTerm.set(entry.term, []); index.byTerm.get(entry.term).push(entry); const c = entry.term[0]; if (!index.byFirstChar.has(c)) index.byFirstChar.set(c, []); index.byFirstChar.get(c).push(entry); }
  for (const bucket of index.byFirstChar.values()) bucket.sort((a,b)=>b.term.length-a.term.length||(a.dictionaryPriority??9999)-(b.dictionaryPriority??9999)||b.score-a.score);
  return index;
}
export async function loadLocalDictionary(url = '/dict/user_dictionary_seed.json') { const res = await fetch(url); if (!res.ok) throw new Error(`Dictionary load failed: ${url} HTTP ${res.status}`); const data = await res.json(); const source = data.title || data.source || 'local-dictionary'; const entries = (data.entries || []).map(entry => normalizeDictionaryEntry({ ...entry, source: entry.source || source, sourceDictionary: entry.source || source, dictionaryPriority: 9999 }, source)).filter(Boolean); return buildDictionaryIndex(entries); }
export function lookupExact(index, text) { const term = normalizeDictionaryText(text); if (!term || !index?.byTerm) return []; return index.byTerm.get(term) || []; }
export function findPrefixMatches(index, text, startIndex = 0, options = {}) { const maxChars = options.maxChars || 24; const src = String(text || ''); const first = src[startIndex]; if (!first || !index?.byFirstChar?.has(first)) return []; const slice = src.slice(startIndex, startIndex + maxChars); const matches = []; for (const entry of index.byFirstChar.get(first)) if (slice.startsWith(entry.term)) matches.push({ term: entry.term, start: startIndex, end: startIndex + entry.term.length, length: entry.term.length, entries: lookupExact(index, entry.term) }); return matches.sort((a,b)=>b.length-a.length||b.entries.length-a.entries.length); }
export function findSentenceDictionaryMatches(index, text, options = {}) { const src = String(text || ''); const matches = []; for (let i=0;i<src.length;i+=1) matches.push(...findPrefixMatches(index, src, i, options)); return matches; }
export function getLongestDictionaryMatches(index, text, options = {}) { const all = findSentenceDictionaryMatches(index, text, options); const occupied = new Set(); const selected = []; for (const m of all.sort((a,b)=>b.length-a.length||a.start-b.start)) { let overlap=false; for(let i=m.start;i<m.end;i+=1) if(occupied.has(i)){overlap=true;break;} if(overlap) continue; selected.push(m); for(let i=m.start;i<m.end;i+=1) occupied.add(i); } return selected.sort((a,b)=>a.start-b.start); }

function compactAnalysisText(value) {
  return normalizeDictionaryText(value).replace(/[\s\u3000]+/g, '');
}

function analysisTokenSurface(token) {
  return compactAnalysisText(token?.surface || token?.text || '');
}

function analysisTokenLemma(token) {
  const value = token?.dictionaryForm || token?.basicForm || token?.baseForm || token?.lemma || token?.surface || '';
  return value && value !== '*' ? compactAnalysisText(value) : analysisTokenSurface(token);
}

function analysisTokenPos(token) {
  return [token?.pos, token?.posDetail1, token?.posDetail2, token?.posDetail3, token?.tokenCategory]
    .filter(Boolean).join(' ').toLowerCase();
}

function isPunctuationToken(token) {
  return /^[。、！？!?「」『』（）()［］\[\]…・：:；;]+$/.test(analysisTokenSurface(token)) || /記号|symbol|punct/.test(analysisTokenPos(token));
}

function isParticleToken(token) {
  return /助詞|particle/.test(analysisTokenPos(token)) || /^(?:は|が|を|に|へ|で|と|の|も|や|か|ね|よ|ぞ|さ|から|まで|より)$/.test(analysisTokenSurface(token));
}

function isDependentLexicalVerb(token) {
  const pos = analysisTokenPos(token);
  const lemma = analysisTokenLemma(token);
  if (!/動詞|verb/.test(pos) || !/非自立|補助/.test(pos)) return false;
  // These productive verbs can form compound mining words and can also be valid
  // standalone lemmas. They must not be discarded as generic grammar.
  return /(?:始める|続ける|終わる|終える|かける|直す|切る|込む|出す|合う|過ぎる|忘れる)$/.test(lemma);
}

function isAuxiliaryVerbToken(token) {
  const lemma = analysisTokenLemma(token);
  const pos = analysisTokenPos(token);
  if (!/動詞|verb/.test(pos) || !/非自立|補助/.test(pos)) return false;
  return /^(?:いる|ある|おく|みる|しまう|いく|くる|くださる|もらう|いただく)$/.test(lemma);
}

function isAuxiliaryToken(token) {
  const surface = analysisTokenSurface(token);
  const pos = analysisTokenPos(token);
  if (/助動詞|auxiliary/.test(pos)) return true;
  if (isAuxiliaryVerbToken(token)) return true;
  return /^(?:た|だ|いる|いた|いない|ある|あった|ない|なかった|ます|ました|ません|たい|たく|られる|れる|させる|せる|ん)$/.test(surface);
}

function isLexicalToken(token) {
  const pos = analysisTokenPos(token);
  if (isPunctuationToken(token) || isParticleToken(token) || isAuxiliaryToken(token)) return false;
  if (isDependentLexicalVerb(token)) return true;
  if (/動詞|形容詞|形状詞|名詞|代名詞|固有名詞|verb|adjective|noun|pronoun|proper/.test(pos)) return true;
  return /[一-龯々ァ-ヶぁ-ん]/.test(analysisTokenSurface(token));
}

function isConjunctiveParticleToken(token) {
  const surface = analysisTokenSurface(token);
  const pos = analysisTokenPos(token);
  // Only tokenizer-confirmed conjunctive て/で can bridge a lexical verb to
  // following aspect/auxiliary material. Case-particle で is a hard boundary.
  return /^(?:て|で)$/.test(surface) && /助詞/.test(pos) && /接続助詞/.test(pos);
}

function isConjugationBridge(token) {
  return isAuxiliaryToken(token) || isConjunctiveParticleToken(token);
}

function isHardBoundaryParticle(token) {
  return isParticleToken(token) && !isConjunctiveParticleToken(token);
}

function isCopulaToken(token) {
  return isAuxiliaryToken(token) && analysisTokenLemma(token) === 'だ';
}
function isNominalLexicalToken(token) {
  const pos = analysisTokenPos(token);
  return /名詞|形容動詞語幹|形状詞|noun|na-adjective/.test(pos) && !/(?:^| )動詞(?: |$)|(?:^| )verb(?: |$)/.test(pos);
}
function shouldAttachConjugationBridge(headToken, bridgeToken) {
  if (isCopulaToken(bridgeToken) && isNominalLexicalToken(headToken)) return false;
  return isConjugationBridge(bridgeToken);
}
function isExpressiveSokuonToken(token) { return analysisTokenSurface(token) === 'っ'; }

function selectTokenSource(currentData = {}) {
  const sources = [currentData.classifiedWords, currentData.displayWords, currentData.contentWords, currentData.tokens];
  return sources.find(source => Array.isArray(source) && source.some(token => analysisTokenSurface(token))) || [];
}

function evidenceCounts(entries = []) {
  const counts = { term: 0, expression: 0, grammar: 0, name: 0 };
  const sources = { term: new Set(), expression: new Set(), grammar: new Set(), name: new Set() };
  for (const entry of entries || []) {
    const type = ['term', 'expression', 'grammar', 'name'].includes(entry?.dictionaryType || entry?.type)
      ? (entry.dictionaryType || entry.type) : 'term';
    counts[type] += 1;
    sources[type].add(entry.sourceDictionary || entry.source || entry.dictionaryId || 'unknown');
  }
  return {
    counts,
    sourceCounts: Object.fromEntries(Object.entries(sources).map(([key, value]) => [key, value.size]))
  };
}

function categoryFromEvidence(surface, tokens, entries) {
  const { counts, sourceCounts } = evidenceCounts(entries);
  const pos = tokens.map(analysisTokenPos).join(' ');
  const multiToken = tokens.length > 1;
  const hasParticle = tokens.some(isParticleToken);
  const tokenizerProper = /固有名詞|proper/.test(pos);
  const tokenizerPronoun = /代名詞|pronoun/.test(pos);
  const tokenizerGrammar = tokens.every(token => isParticleToken(token) || isAuxiliaryToken(token));

  if (tokens.every(isPunctuationToken)) return { category: 'ignored', subtype: 'punctuation', confidence: 'high', reason: 'Punctuation token.' };
  if (tokenizerGrammar) return { category: 'grammar', subtype: tokens.some(isParticleToken) ? 'particle' : 'auxiliary', confidence: 'high', reason: 'Tokenizer identifies only particle/auxiliary material.' };
  if (tokenizerPronoun && counts.term >= counts.name) return { category: 'term', subtype: 'pronoun', confidence: 'high', reason: 'Tokenizer pronoun evidence outweighs incidental name entries.' };
  if (tokenizerProper && counts.name > 0) return { category: 'proper-name', subtype: 'name', confidence: 'high', reason: 'Tokenizer proper-noun evidence agrees with a name dictionary.' };

  const nameStrong = sourceCounts.name >= 2 && (counts.name >= counts.term || tokenizerProper);
  if (nameStrong) return { category: 'proper-name', subtype: 'name', confidence: tokenizerProper ? 'high' : 'medium', reason: 'Multiple name sources and supporting evidence.' };

  const grammarStrong = counts.grammar > 0 && (hasParticle || multiToken) && sourceCounts.grammar >= 1;
  if (grammarStrong && counts.grammar >= Math.max(1, counts.term * 0.4)) return { category: 'grammar', subtype: 'grammar-expression', confidence: 'medium', reason: 'Multi-token/particle span with grammar dictionary evidence.' };

  const expressionStrong = counts.expression > 0 && multiToken && (hasParticle || surface.length >= 4) && counts.expression >= Math.max(1, counts.term * 0.35);
  if (expressionStrong) return { category: 'term', subtype: 'fixed-expression', confidence: 'medium', reason: 'Dictionary-backed multi-token fixed expression; treated as a learnable lexical span.' };

  if (counts.term > 0 || isLexicalToken(tokens[0])) {
    const subtype = /動詞|verb/.test(pos) ? 'verb' : /形容詞|adjective/.test(pos) ? 'adjective' : /代名詞|pronoun/.test(pos) ? 'pronoun' : 'noun-or-term';
    return { category: 'term', subtype, confidence: counts.term > 0 ? 'high' : 'medium', reason: counts.term > 0 ? 'Term evidence and tokenizer lexical evidence.' : 'Tokenizer lexical evidence; dictionary evidence absent.' };
  }
  return { category: 'grammar', subtype: 'function-word', confidence: 'low', reason: 'No strong lexical evidence; conservative function-word fallback.' };
}

function behaviorForCategory(category) {
  if (category === 'term') return { countsForComprehension: true, showInNewWords: true, colorRole: 'frequency-or-known' };
  if (category === 'proper-name') return { countsForComprehension: false, showInNewWords: false, colorRole: 'name' };
  if (category === 'grammar') return { countsForComprehension: false, showInNewWords: false, colorRole: 'grammar' };
  return { countsForComprehension: false, showInNewWords: false, colorRole: 'ignored' };
}

function entriesAreGrammarOnly(entries = []) {
  return entries.length > 0 && entries.every(entry => (entry.dictionaryType || entry.type) === 'grammar');
}

function findBestDictionarySpan(index, tokens, start, maxTokens = 7) {
  let best = null;
  let text = '';
  for (let end = start; end < Math.min(tokens.length, start + maxTokens); end += 1) {
    if (isPunctuationToken(tokens[end])) break;
    text += analysisTokenSurface(tokens[end]);
    const exactMatches = lookupExact(index, text);
    if (!exactMatches.length) continue;

    const endsWithHardParticle = isHardBoundaryParticle(tokens[end]);
    // A trailing particle belongs to the next grammar span unless the whole exact
    // dictionary entry is itself grammar. Internal particles remain allowed.
    if (endsWithHardParticle && !entriesAreGrammarOnly(exactMatches)) continue;

    const useful = exactMatches.some(entry => ['term', 'grammar', 'expression', 'name'].includes(entry.dictionaryType || entry.type || 'term'));
    if (useful) best = { start, end, surface: text, lemma: text, entries: exactMatches, method: 'exact-dictionary-span' };
  }
  return best;
}

function findExpressiveSokuonSpan(index, tokens, start, maxTokens = 5) {
  let raw = '', normalized = '', removed = 0, best = null;
  for (let end = start; end < Math.min(tokens.length, start + maxTokens); end += 1) {
    const token = tokens[end];
    if (isPunctuationToken(token) || isParticleToken(token) || (isAuxiliaryToken(token) && !isExpressiveSokuonToken(token))) break;
    const part = analysisTokenSurface(token);
    raw += part;
    if (isExpressiveSokuonToken(token) && end > start && end + 1 < tokens.length) removed += 1;
    else normalized += part;
    if (removed && end >= start + 2) {
      const entries = lookupExact(index, normalized);
      if (entries.length) best = { start, end, surface: raw, lemma: normalized, entries, method: 'expressive-sokuon-normalization', reconstruction: { accepted: true, removedSokuonCount: removed, exactMatchCount: entries.length, reason: `Removed ${removed} expressive internal small-tsu token(s) and found an exact dictionary headword.` } };
    }
  }
  return best;
}

function generateVerbStemCandidates(surface) {
  const text = compactAnalysisText(surface);
  const rules = [['き','く'],['ぎ','ぐ'],['し','す'],['ち','つ'],['に','ぬ'],['び','ぶ'],['み','む'],['り','る'],['い','う']];
  return rules.filter(([a]) => text.endsWith(a)).map(([a,b]) => ({ text: `${text.slice(0,-a.length)}${b}`, stemEnding: a, dictionaryEnding: b }));
}

function findVerbStemHeadwordSpan(index, tokens, start, maxTokens = 4) {
  let raw = '', best = null;
  for (let end = start; end < Math.min(tokens.length, start + maxTokens); end += 1) {
    const token = tokens[end];
    if (isPunctuationToken(token) || isParticleToken(token) || isAuxiliaryToken(token)) break;
    raw += analysisTokenSurface(token);
    if (end === start) continue;
    const prefix = tokens.slice(start,end).map(analysisTokenSurface).join('');
    for (const candidate of generateVerbStemCandidates(analysisTokenSurface(token))) {
      const lemma = `${prefix}${candidate.text}`;
      const entries = lookupExact(index, lemma);
      if (entries.length) best = { start, end, surface: raw, lemma, entries, method: 'reconstructed-verb-stem-headword', verbLemma: candidate.text, reconstruction: { accepted: true, exactMatchCount: entries.length, ...candidate, reason: 'Controlled verb-stem reconstruction produced an exact complete dictionary headword.' } };
    }
  }
  return best;
}

function sourceKey(entry) {
  return entry?.sourceDictionary || entry?.source || entry?.dictionaryId || 'unknown';
}

function buildParticleCrossingCandidate(tokens, start, verbIndex) {
  if (verbIndex < start + 2) return null;
  const window = tokens.slice(start, verbIndex + 1);
  const beforeVerb = window.slice(0, -1);
  if (!beforeVerb.some(isParticleToken)) return null;
  if (beforeVerb.some(token => isPunctuationToken(token) || isAuxiliaryToken(token))) return null;
  const verb = tokens[verbIndex];
  if (!isLexicalToken(verb) || !/動詞|verb/.test(analysisTokenPos(verb))) return null;
  const lemma = `${beforeVerb.map(analysisTokenSurface).join('')}${analysisTokenLemma(verb)}`;
  return {
    lemma,
    verbLemma: analysisTokenLemma(verb),
    internalParticles: beforeVerb.filter(isParticleToken).map(analysisTokenSurface)
  };
}

function evaluateReconstructedHeadword(entries = []) {
  const sourceCount = new Set(entries.map(sourceKey)).size;
  const exactMatchCount = entries.length;
  const expressionCount = entries.filter(entry => (entry.dictionaryType || entry.type) === 'expression').length;
  const tagText = entries.map(entry => `${(entry.tags || []).join(' ')} ${entry.termTags || ''} ${entry.expressionType || ''}`).join(' ');
  const explicitLexicalTag = /idiom|idiomatic|fixed|set phrase|慣用|成句|熟語|連語|定型|lexical/i.test(tagText);
  // Word-understanding rule only: repeated exact headword evidence across independent
  // dictionaries establishes a stable lexical unit without deciding its category.
  const accepted = exactMatchCount > 0 && (sourceCount >= 3 || expressionCount > 0 || explicitLexicalTag);
  return {
    accepted,
    exactMatchCount,
    sourceCount,
    expressionCount,
    explicitLexicalTag,
    reason: accepted
      ? sourceCount >= 3
        ? `Exact reconstructed headword confirmed by ${sourceCount} independent dictionaries.`
        : expressionCount > 0
          ? 'Exact reconstructed headword confirmed by an expression dictionary.'
          : 'Exact reconstructed headword has an explicit lexical-unit tag.'
      : exactMatchCount === 0
        ? 'Reconstructed headword is absent from the runtime dictionary index.'
        : `Reconstructed headword has ${sourceCount} independent source(s); threshold is 3.`
  };
}

function findParticleCrossingHeadwordSpan(index, tokens, start, maxTokens = 7) {
  let best = null;
  for (let verbIndex = start + 2; verbIndex < Math.min(tokens.length, start + maxTokens); verbIndex += 1) {
    if (isPunctuationToken(tokens[verbIndex])) break;
    const candidate = buildParticleCrossingCandidate(tokens, start, verbIndex);
    if (!candidate) continue;
    const entries = lookupExact(index, candidate.lemma);
    const reconstruction = evaluateReconstructedHeadword(entries);
    if (!reconstruction.accepted) continue;
    let end = verbIndex;
    let cursor = end + 1;
    while (cursor < tokens.length && isConjugationBridge(tokens[cursor])) { end = cursor; cursor += 1; }
    best = {
      start,
      end,
      surface: tokens.slice(start, end + 1).map(analysisTokenSurface).join(''),
      lemma: candidate.lemma,
      entries,
      method: 'reconstructed-complete-headword',
      verbLemma: candidate.verbLemma,
      internalParticles: candidate.internalParticles,
      reconstruction
    };
  }
  return best;
}

function findCompoundVerbSpan(index, tokens, start) {
  const first = tokens[start];
  if (!isLexicalToken(first) || !/動詞|verb/.test(analysisTokenPos(first))) return null;
  const second = tokens[start + 1];
  if (!second || !isDependentLexicalVerb(second)) return null;

  const compoundLemma = `${analysisTokenSurface(first)}${analysisTokenLemma(second)}`;
  const entries = lookupExact(index, compoundLemma);
  if (!entries.length) return null;

  let end = start + 1;
  let cursor = end + 1;
  while (cursor < tokens.length && isConjugationBridge(tokens[cursor])) {
    end = cursor;
    cursor += 1;
  }
  return {
    start,
    end,
    surface: tokens.slice(start, end + 1).map(analysisTokenSurface).join(''),
    lemma: compoundLemma,
    entries,
    method: 'compound-verb-reconstruction'
  };
}

function findGrammarSpan(index, tokens, start, maxTokens = 5) {
  let best = null;
  let text = '';
  for (let end = start; end < Math.min(tokens.length, start + maxTokens); end += 1) {
    if (isPunctuationToken(tokens[end])) break;
    text += analysisTokenSurface(tokens[end]);
    const entries = lookupExact(index, text).filter(entry => (entry.dictionaryType || entry.type) === 'grammar');
    if (entries.length) best = { start, end, surface: text, lemma: text, entries, method: 'exact-grammar-span' };
  }
  return best;
}

function findCopulaChainSpan(tokens, start) {
  if (!isCopulaToken(tokens[start])) return null;
  let end = start;
  while (end + 1 < tokens.length && isAuxiliaryToken(tokens[end + 1]) && !isPunctuationToken(tokens[end + 1])) end += 1;
  return { start, end, surface: tokens.slice(start,end+1).map(analysisTokenSurface).join(''), lemma: 'だ', method: 'copula-chain' };
}

export function analyzeMiningWords(index, currentData = {}) {
  const tokens = selectTokenSource(currentData).map((token, index) => ({ ...token, _analysisIndex: index }));
  const rows = [];
  let i = 0;
  while (i < tokens.length) {
    const token = tokens[i];
    const surface = analysisTokenSurface(token);
    if (!surface) { i += 1; continue; }

    if (isPunctuationToken(token)) {
      const behavior = behaviorForCategory('ignored');
      rows.push({ surface, lemma: surface, category: 'ignored', subtype: 'punctuation', tokens: [token], evidence: evidenceCounts([]), confidence: 'high', reason: 'Punctuation token.', ...behavior });
      i += 1;
      continue;
    }

    // Grammar starts its own span. Do not attach ordinary particles to a preceding term.
    if (isParticleToken(token) || (isAuxiliaryToken(token) && !isLexicalToken(token))) {
      const grammarSpan = findCopulaChainSpan(tokens, i) || findGrammarSpan(index, tokens, i);
      const end = grammarSpan?.end ?? i;
      const spanTokens = tokens.slice(i, end + 1);
      const spanSurface = spanTokens.map(analysisTokenSurface).join('');
      const entries = grammarSpan?.entries || lookupExact(index, spanSurface);
      const decision = categoryFromEvidence(spanSurface, spanTokens, entries);
      const category = decision.category === 'term' ? 'grammar' : decision.category;
      const behavior = behaviorForCategory(category);
      rows.push({
        surface: spanSurface, lemma: grammarSpan?.lemma || spanSurface, category,
        subtype: decision.subtype === 'noun-or-term' ? 'function-word' : decision.subtype,
        tokens: spanTokens, trailingGrammar: spanTokens.map(analysisTokenSurface),
        evidence: evidenceCounts(entries), matchMethod: grammarSpan?.method || 'tokenizer-grammar-boundary',
        confidence: decision.confidence, reason: grammarSpan ? 'Exact grammar span.' : 'Tokenizer particle/auxiliary boundary.',
        frequencyKey: '', knownWordKey: '', ...behavior
      });
      i = end + 1;
      continue;
    }

    const expressiveSpan = findExpressiveSokuonSpan(index, tokens, i);
    const reconstructedSpan = findParticleCrossingHeadwordSpan(index, tokens, i);
    const stemSpan = findVerbStemHeadwordSpan(index, tokens, i);
    const compoundSpan = findCompoundVerbSpan(index, tokens, i);
    const dictionarySpan = findBestDictionarySpan(index, tokens, i);
    let chosenSpan = null;
    if (expressiveSpan) chosenSpan = expressiveSpan;
    else if (reconstructedSpan) chosenSpan = reconstructedSpan;
    else if (stemSpan && (!dictionarySpan || stemSpan.end >= dictionarySpan.end)) chosenSpan = stemSpan;
    else if (compoundSpan && (!dictionarySpan || compoundSpan.end >= dictionarySpan.end)) chosenSpan = compoundSpan;
    else if (dictionarySpan && dictionarySpan.end > i) chosenSpan = dictionarySpan;

    let end = chosenSpan?.end ?? i;
    if (!chosenSpan && isLexicalToken(token)) {
      let cursor = i + 1;
      while (cursor < tokens.length && shouldAttachConjugationBridge(token, tokens[cursor])) {
        end = cursor;
        cursor += 1;
      }
    }

    const spanTokens = tokens.slice(i, end + 1);
    const spanSurface = spanTokens.map(analysisTokenSurface).join('');
    const formResult = lookupWithDictionaryForms(index, spanSurface, { tokens: spanTokens });
    const directEntries = chosenSpan?.entries || lookupExact(index, spanSurface);
    const entries = directEntries.length ? directEntries : formResult.matches;
    const lemma = chosenSpan?.lemma || formResult.matchedText || analysisTokenLemma(spanTokens.find(isLexicalToken) || token) || spanSurface;
    const decision = categoryFromEvidence(spanSurface, spanTokens, entries);
    const behavior = behaviorForCategory(decision.category);
    rows.push({
      surface: spanSurface,
      lemma,
      category: decision.category,
      subtype: chosenSpan?.method === 'compound-verb-reconstruction' ? 'compound-verb' : chosenSpan?.method === 'reconstructed-complete-headword' ? 'dictionary-headword-span' : decision.subtype,
      tokens: spanTokens,
      trailingGrammar: spanTokens.slice(1).filter(isConjugationBridge).map(analysisTokenSurface),
      evidence: evidenceCounts(entries),
      matchMethod: chosenSpan?.method || (directEntries.length ? 'exact-dictionary-span' : formResult.matchedBy),
      confidence: decision.confidence,
      reason: chosenSpan?.reconstruction?.reason || (chosenSpan?.method === 'compound-verb-reconstruction' ? 'Dictionary-backed compound verb plus inflection chain.' : decision.reason),
      frequencyKey: decision.category === 'term' ? lemma : '',
      knownWordKey: decision.category === 'term' ? lemma : '',
      fallbackFrequencyKey: chosenSpan?.verbLemma || '',
      fallbackKnownWordKey: chosenSpan?.verbLemma || '',
      internalParticles: chosenSpan?.internalParticles || [],
      reconstruction: chosenSpan?.reconstruction || null,
      ...behavior
    });
    i = end + 1;
  }
  return { sentence: currentData?.plainText || tokens.map(analysisTokenSurface).join(''), tokenCount: tokens.length, rows };
}

function miningLookupTokenSpan(tokens, selectedText) {
  const target = compactAnalysisText(selectedText);
  const usable = (tokens || []).filter(token => analysisTokenSurface(token));
  for (let start = 0; start < usable.length; start += 1) {
    let joined = '';
    for (let end = start; end < usable.length && joined.length <= target.length; end += 1) {
      joined += analysisTokenSurface(usable[end]);
      if (joined === target) return usable.slice(start, end + 1);
    }
  }
  return [];
}

export function lookupWithDictionaryForms(index, selectedText, currentData = {}) {
  const surface = compactAnalysisText(selectedText);
  const attempts = [];
  const seen = new Set();
  const add = (text, method, detail = '') => {
    const normalized = compactAnalysisText(text);
    if (!normalized || seen.has(normalized)) return;
    seen.add(normalized);
    attempts.push({ text: normalized, method, detail, matches: lookupExact(index, normalized) });
  };
  add(surface, 'surface', 'Exact selected surface.');
  const sources = [currentData?.classifiedWords, currentData?.displayWords, currentData?.contentWords, currentData?.tokens]
    .filter(Array.isArray);
  for (const source of sources) {
    const span = miningLookupTokenSpan(source, surface);
    if (!span.length) continue;
    if (span.length === 1) add(analysisTokenLemma(span[0]), 'tokenizer-dictionary-form', `${analysisTokenSurface(span[0])} -> ${analysisTokenLemma(span[0])}`);
    if (span.length >= 3 && span.slice(1, -1).some(isExpressiveSokuonToken)) {
      const normalized = span.filter(token => !isExpressiveSokuonToken(token)).map(analysisTokenSurface).join('');
      if (lookupExact(index, normalized).length) add(normalized, 'expressive-sokuon-normalization', 'Removed expressive internal small-tsu; exact complete headword found.');
    }
    if (span.length >= 2) {
      const finalIndex = span.map(token => !isPunctuationToken(token) && !isParticleToken(token) && !isAuxiliaryToken(token)).lastIndexOf(true);
      if (finalIndex > 0) {
        const prefix = span.slice(0, finalIndex).map(analysisTokenSurface).join('');
        for (const candidate of generateVerbStemCandidates(analysisTokenSurface(span[finalIndex]))) {
          const lemma = `${prefix}${candidate.text}`;
          if (lookupExact(index, lemma).length) add(lemma, 'reconstructed-verb-stem-headword', 'Controlled verb-stem reconstruction found an exact complete headword.');
        }
      }
    }
    // Reconstruct complete particle-crossing headwords before component fallbacks.
    for (let verbIndex = 2; verbIndex < span.length; verbIndex += 1) {
      const candidate = buildParticleCrossingCandidate(span, 0, verbIndex);
      if (!candidate) continue;
      const matches = lookupExact(index, candidate.lemma);
      const reconstruction = evaluateReconstructedHeadword(matches);
      if (reconstruction.accepted) add(candidate.lemma, 'reconstructed-complete-headword', reconstruction.reason);
    }
    // If no complete lexical unit is confirmed, prefer the final lexical verb.
    const finalLexicalIndex = span.map(isLexicalToken).lastIndexOf(true);
    if (finalLexicalIndex >= 0) {
      const finalLexical = span[finalLexicalIndex];
      add(analysisTokenLemma(finalLexical), 'final-lexical-head', `Final lexical token ${analysisTokenSurface(finalLexical)} -> ${analysisTokenLemma(finalLexical)}.`);
    }
    // Component headwords are diagnostic fallbacks only.
    const lexicalIndex = span.findIndex(isLexicalToken);
    if (lexicalIndex >= 0) {
      const lexical = span[lexicalIndex];
      add(analysisTokenLemma(lexical), 'main-lexical-head', `Main lexical token ${analysisTokenSurface(lexical)} -> ${analysisTokenLemma(lexical)}.`);
      const prefix = span.slice(0, lexicalIndex).map(analysisTokenSurface).join('');
      if (prefix) add(`${prefix}${analysisTokenLemma(lexical)}`, 'phrase-lexical-head-reconstruction', 'Preserved token prefix and replaced lexical head with lemma.');
    }
    // Compound-verb reconstruction: combine preceding verb stem(s) with the final independent verb lemma.
    for (let i = 1; i < span.length; i += 1) {
      if (!isLexicalToken(span[i])) continue;
      const previous = span.slice(0, i).filter(token => !isParticleToken(token) && !isAuxiliaryToken(token));
      if (!previous.length) continue;
      const prefix = previous.map(analysisTokenSurface).join('');
      const lemma = analysisTokenLemma(span[i]);
      add(`${prefix}${lemma}`, 'compound-verb-reconstruction', `${prefix} + ${lemma}`);
    }
  }
  const selectedAttempt = attempts.find(attempt => attempt.matches.length > 0) || null;
  return {
    surface,
    attempts,
    selectedAttempt,
    matches: selectedAttempt?.matches || [],
    matchedText: selectedAttempt?.text || '',
    matchedBy: selectedAttempt?.method || 'none',
    matchDetail: selectedAttempt?.detail || ''
  };
}
````

### `novel-audio-miner/src/lib/dictionaryStorage.js`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 6668 bytes
- SHA-256: `32ed043b365e7ce6c68f813863c0521903105d1ff9fff9c5e1a16e04d5686c94`

````javascript
const DB_NAME = 'novel-audio-miner-dictionaries';
const DB_VERSION = 3;
const LEGACY_STORE_NAME = 'dictionarySnapshots';
const META_STORE_NAME = 'dictionaryMetas';
const ENTRY_STORE_NAME = 'dictionaryEntries';
const ACTIVE_KEY = 'active';
const TERM_ENTRY_CHUNK_SIZE = 5000;
function openDictionaryDatabase(){return new Promise((resolve,reject)=>{if(!('indexedDB'in window)){reject(new Error('IndexedDB is not available in this browser.'));return;}const req=indexedDB.open(DB_NAME,DB_VERSION);req.onupgradeneeded=()=>{const db=req.result;if(!db.objectStoreNames.contains(LEGACY_STORE_NAME))db.createObjectStore(LEGACY_STORE_NAME,{keyPath:'id'});if(!db.objectStoreNames.contains(META_STORE_NAME))db.createObjectStore(META_STORE_NAME,{keyPath:'id'});if(!db.objectStoreNames.contains(ENTRY_STORE_NAME))db.createObjectStore(ENTRY_STORE_NAME,{keyPath:'id'});};req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error||new Error('IndexedDB open failed.'));});}
function requestToPromise(request){return new Promise((resolve,reject)=>{request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error||new Error('IndexedDB request failed.'));});}
async function withStore(storeName,mode,callback){const db=await openDictionaryDatabase();try{return await new Promise((resolve,reject)=>{const tx=db.transaction(storeName,mode);const store=tx.objectStore(storeName);let result;tx.oncomplete=()=>resolve(result);tx.onerror=()=>reject(tx.error||new Error('IndexedDB transaction failed.'));result=callback(store);});}finally{db.close();}}
function chunkId(dictionaryId,chunkIndex){return `${dictionaryId}::chunk::${chunkIndex}`;}
function minimizeEntry(entry){return{term:entry.term||entry.text||'',reading:entry.reading||'',source:entry.source||entry.sourceDictionary||'',sourceDictionary:entry.sourceDictionary||entry.source||'',dictionaryId:entry.dictionaryId||'',dictionaryPriority:Number(entry.dictionaryPriority??entry.priority??9999),dictionaryType:entry.dictionaryType||entry.type||'term',nameType:entry.nameType||'',grammarType:entry.grammarType||'',expressionType:entry.expressionType||'',readings:Array.isArray(entry.readings)?entry.readings:[],tags:Array.isArray(entry.tags)?entry.tags:[],rules:entry.rules||'',score:Number(entry.score||0),sequence:entry.sequence??null,termTags:entry.termTags||''};}
export async function saveActiveDictionarySnapshot({title,entries,summary}){const now=new Date().toISOString();const minimized=(entries||[]).map(minimizeEntry);const snapshot={id:ACTIVE_KEY,title:title||summary?.importedTitle||summary?.index?.title||'Imported dictionary',savedAt:now,entryCount:minimized.length,summary:summary||null,entries:minimized};await withStore(LEGACY_STORE_NAME,'readwrite',store=>store.put(snapshot));return snapshot;}
export async function loadActiveDictionarySnapshot(){return await withStore(LEGACY_STORE_NAME,'readonly',store=>requestToPromise(store.get(ACTIVE_KEY)))||null;}
export async function clearActiveDictionarySnapshot(){await withStore(LEGACY_STORE_NAME,'readwrite',store=>store.delete(ACTIVE_KEY));}
async function deleteEntryChunksForMeta(meta){const n=Number(meta?.chunkCount||0);if(!meta?.id||!n)return;await withStore(ENTRY_STORE_NAME,'readwrite',store=>{for(let i=0;i<n;i+=1)store.delete(chunkId(meta.id,i));});}
export async function saveTermDictionarySnapshot({id,title,priority,entries,summary,profile}){const now=new Date().toISOString();const safeTitle=title||summary?.importedTitle||summary?.index?.title||'Imported dictionary';const safePriority=Number(priority||9999);const entryCount=entries?.length||0;const chunkCount=Math.ceil(entryCount/TERM_ENTRY_CHUNK_SIZE);const existing=await withStore(META_STORE_NAME,'readonly',store=>requestToPromise(store.get(id)));if(existing)await deleteEntryChunksForMeta(existing);const meta={id,title:safeTitle,priority:safePriority,type:profile?.detectedType||summary?.detectionProfile?.detectedType||'term',adapter:profile?.adapter||summary?.detectionProfile?.adapter||'yomitan-term-v3',supported:true,savedAt:now,entryCount,chunkCount,chunkSize:TERM_ENTRY_CHUNK_SIZE,storageMode:'chunked-minimal-detection-v1',profile:profile||summary?.detectionProfile||null,summary:summary?{fileName:summary.fileName||'',importedTitle:summary.importedTitle||safeTitle,importedEntries:summary.importedEntries||entryCount,importedRows:summary.importedRows||entryCount,normalizedEntries:summary.normalizedEntries||entryCount,detectionProfile:summary.detectionProfile||profile||null}:null};await withStore(META_STORE_NAME,'readwrite',store=>store.put(meta));for(let chunkIndex=0;chunkIndex<chunkCount;chunkIndex+=1){const start=chunkIndex*TERM_ENTRY_CHUNK_SIZE;const end=Math.min(start+TERM_ENTRY_CHUNK_SIZE,entryCount);const chunkEntries=[];for(let i=start;i<end;i+=1)chunkEntries.push(minimizeEntry({...entries[i],dictionaryId:id,dictionaryPriority:safePriority,sourceDictionary:safeTitle,source:safeTitle}));await withStore(ENTRY_STORE_NAME,'readwrite',store=>store.put({id:chunkId(id,chunkIndex),dictionaryId:id,chunkIndex,entries:chunkEntries}));}return meta;}
export async function loadTermDictionaryMetas(){const metas=await withStore(META_STORE_NAME,'readonly',store=>requestToPromise(store.getAll()));return(metas||[]).sort((a,b)=>Number(a.priority||9999)-Number(b.priority||9999));}
async function loadEntriesForMeta(meta){if(!meta)return[];if(meta.storageMode==='chunked-minimal-detection-v1'||meta.chunkCount){const entries=[];for(let i=0;i<Number(meta.chunkCount||0);i+=1){const chunk=await withStore(ENTRY_STORE_NAME,'readonly',store=>requestToPromise(store.get(chunkId(meta.id,i))));if(chunk?.entries?.length)entries.push(...chunk.entries);}return entries;}const payload=await withStore(ENTRY_STORE_NAME,'readonly',store=>requestToPromise(store.get(meta.id)));return payload?.entries||[];}
export async function loadTermDictionaryEntriesForMeta(meta){return loadEntriesForMeta(meta);}
export async function loadTermDictionarySnapshots(){const metas=await loadTermDictionaryMetas();const snapshots=[];for(const meta of metas){const entries=await loadEntriesForMeta(meta);snapshots.push({meta,entries});}return snapshots;}
export async function deleteTermDictionarySnapshot(id){const meta=await withStore(META_STORE_NAME,'readonly',store=>requestToPromise(store.get(id)));if(meta)await deleteEntryChunksForMeta(meta);await withStore(META_STORE_NAME,'readwrite',store=>store.delete(id));await withStore(ENTRY_STORE_NAME,'readwrite',store=>store.delete(id));}
export async function clearTermDictionarySnapshots(){await withStore(META_STORE_NAME,'readwrite',store=>store.clear());await withStore(ENTRY_STORE_NAME,'readwrite',store=>store.clear());}
````

### `novel-audio-miner/src/lib/dictionaryValidationBridge.js`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 2958 bytes
- SHA-256: `c85bb539b3b39fb9314be3c3693f235c914f561f92ce642bb4ff78d2913902ac`

````javascript
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
````

### `novel-audio-miner/src/lib/enrichService.js`

- Purpose: JavaScript/React source.
- Size: 7990 bytes
- SHA-256: `534da9370a40fad6a0f11ac68ab97dabdefc753e00de3da5a44b6070c68477f1`

````javascript
/**
 * Enrichment service.
 *
 * Responsibility:
 * - Search Nadeshiko for example sentences, audio, images, and media metadata.
 * - Score candidate sentences using the local known-word cache.
 * - Fall back to VOICEVOX sentence audio when Nadeshiko is unavailable or TTS is forced.
 *
 * This module prepares enrichment data only. Anki note updates are handled by Reader.jsx.
 */

import { getKnownWords } from './wordCache.js';

const NADESHIKO_API_KEY = 'nade_rGJBvOiBGNoLXjifckoSanCnSuoTtwjuhnlRqVVyhKyGZlGoxKRbgshSsJbifoMc';
const NADESHIKO_BASE_URL = 'https://nadeshiko.co';
const NADESHIKO_SEARCH_ENDPOINT = '/api/nadeshiko/v1/search';
const VOICEVOX_SPEAKER = 20;
const FUNCTION_POS = new Set(['助詞', '助動詞', '補助記号']);

function getSessionToken() {
  try { return localStorage.getItem('nadeshiko_session_token') || ''; } catch { return ''; }
}


function isTtsForced() {
  try { return localStorage.getItem('force_tts') === 'true'; } catch { return false; }
}

function makeAbsoluteUrl(url) {
  if (!url) return '';
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  if (url.startsWith('//')) return 'https:' + url;
  if (url.startsWith('/')) return NADESHIKO_BASE_URL + url;
  return `${NADESHIKO_BASE_URL}/${url}`;
}

function contentLength(text) {
  return (text || '').replace(/[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF]/g, '').length;
}


function buildFurigana(sentenceText, tokens) {
  if (!tokens || !tokens.length) return sentenceText || '';
  const sorted = [...tokens].sort((a, b) => a.b - b.b);
  let result = '';
  let lastEnd = 0;
  for (const token of sorted) {
    const surface = token.s || '';
    const reading = (token.r || '').replace(/[\u30A1-\u30FA]/g, c =>
      String.fromCharCode(c.charCodeAt(0) - 0x60)
    );
    if (token.b > lastEnd) result += sentenceText.slice(lastEnd, token.b);
    const hasKanji = /[\u4E00-\u9FFF]/.test(surface);
    if (hasKanji && reading && reading !== surface) {
      result += ` ${surface}[${reading}]`;
    } else {
      result += surface;
    }
    lastEnd = token.e;
  }
  if (lastEnd < sentenceText.length) result += sentenceText.slice(lastEnd);
  return result.replace(/\s+/g, '').trim();
}

async function searchNadeshiko(word) {
  if (isTtsForced()) throw new Error('TTS forced');
  const body = {
    query: { search: word },
    take: 15,
    filters: { contentRating: ['SAFE', 'SUGGESTIVE'] },
    include: ['media']
  };
  const headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'nadeshiko-sdk-ts/2.1.0',
    'Accept': '*/*'
  };
  const sessionToken = getSessionToken();
  if (sessionToken) {
    headers['Cookie'] = `__Secure-nadeshiko.session_token=${sessionToken}`;
  } else {
    headers['X-API-Key'] = NADESHIKO_API_KEY;
  }
  const response = await fetch(NADESHIKO_SEARCH_ENDPOINT, {
    method: 'POST', headers, body: JSON.stringify(body)
  });
  if (!response.ok) {
    throw new Error(`Nadeshiko API HTTP ${response.status}`);
  }
  return response.json();
}

function scoreSegment(segment, targetWord, knownWords) {
  const tokens = segment.textJa?.tokens || [];
  let unknownCount = 0;
  for (const token of tokens) {
    const d = token.d || token.s || '';
    if (d === targetWord) continue;
    const pos = token.p || '';
    if (FUNCTION_POS.has(pos)) continue;
    if (!knownWords.has(d)) unknownCount++;
  }
  const hasAudio = !!segment.urls?.audioUrl;
  const clen = contentLength(segment.textJa?.content || '');
  const lengthBonus = Math.floor(clen / 5);
  const score = unknownCount * 10 - lengthBonus - (hasAudio ? 2 : 0);
  return { score, unknownCount, hasAudio, contentLength: clen };
}

function pickBestSegment(segments, targetWord, knownWords) {
  if (!segments.length) return null;
  const scoredAll = segments.map(seg => ({
    seg,
    ...scoreSegment(seg, targetWord, knownWords)
  }));
  scoredAll.sort((a, b) => a.score - b.score);
  const i1Candidates = scoredAll.filter(s => s.unknownCount <= 1 && s.contentLength >= MIN_CONTENT_LENGTH);
  if (i1Candidates.length > 0) return { segment: i1Candidates[0].seg, mode: 'i+1', stats: i1Candidates[0] };
  const i2Candidates = scoredAll.filter(s => s.unknownCount <= 2 && s.contentLength >= MIN_CONTENT_LENGTH);
  if (i2Candidates.length > 0) return { segment: i2Candidates[0].seg, mode: 'i+2', stats: i2Candidates[0] };
  const anyLong = scoredAll.filter(s => s.contentLength >= MIN_CONTENT_LENGTH);
  if (anyLong.length > 0) return { segment: anyLong[0].seg, mode: 'fallback', stats: anyLong[0] };
  const longest = scoredAll.reduce((a, b) => a.contentLength >= b.contentLength ? a : b);
  return { segment: longest.seg, mode: 'fallback-short', stats: longest };
}

export async function generateVoicevoxAudio(text) {
  const queryResp = await fetch(
    `/api/voicevox/audio_query?text=${encodeURIComponent(text)}&speaker=${VOICEVOX_SPEAKER}`,
    { method: 'POST' }
  );

  if (!queryResp.ok) throw new Error(`VOICEVOX query failed (HTTP ${queryResp.status})`);

  const queryData = await queryResp.json();
  const synthResp = await fetch(`/api/voicevox/synthesis?speaker=${VOICEVOX_SPEAKER}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queryData)
  });

  if (!synthResp.ok) throw new Error(`VOICEVOX synthesis failed (HTTP ${synthResp.status})`);

  const blob = await synthResp.blob();
  const audioBase64 = await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });

  return { audioBase64, filename: `voicevox_${Date.now()}.wav` };
}

function voicevoxFallback(novelSentence) {
  return {
    sentence: novelSentence,
    sentenceFurigana: novelSentence,
    translation: '',
    audioUrl: '',
    imageUrl: '',
    source: 'VOICEVOX (もち子さん)',
    unknownCount: 0,
    mode: 'tts-voicevox',
    method: 'voicevox'
  };
}

export async function autoEnrichWord(word, ankiRequestFn, noteType = 'Kiku', onProgress) {
  const trimmed = word.trim();
  if (!trimmed) throw new Error('No word provided');
  try {
    if (onProgress) onProgress('Searching Nadeshiko...');
    const data = await searchNadeshiko(trimmed);
    const segments = data?.segments || [];
    if (segments.length > 0) {
      if (onProgress) onProgress('Loading word knowledge...');
      const knownWords = await getKnownWords(ankiRequestFn, onProgress);
      if (onProgress) onProgress('Picking best sentence...');
      const { segment, mode, stats } = pickBestSegment(segments, trimmed, knownWords);
      const sentence = segment.textJa?.content || '';
      const tokens = segment.textJa?.tokens || [];
      const sentenceFurigana = buildFurigana(sentence, tokens);
      const translation = segment.textEn?.content || '';
      const audioUrl = segment.urls?.audioUrl || '';
      const imageUrl = segment.urls?.imageUrl || '';
      const mediaInfo = data.includes?.media?.[segment.mediaPublicId];
      const sourceName = mediaInfo?.nameRomaji || mediaInfo?.nameEn || 'Nadeshiko';
      return {
        sentence, sentenceFurigana, translation,
        audioUrl: makeAbsoluteUrl(audioUrl),
        imageUrl: makeAbsoluteUrl(imageUrl),
        source: sourceName,
        unknownCount: stats?.unknownCount ?? 0,
        mode, method: 'nadeshiko'
      };
    }
  } catch (err) {
    console.warn('[Enrich] Nadeshiko failed:', err.message);
  }
  throw new Error('FALLBACK_TTS');
}

export async function autoEnrichWordWithFallback(word, novelSentence, ankiRequestFn, noteType, onProgress) {
  try {
    return await autoEnrichWord(word, ankiRequestFn, noteType, onProgress);
  } catch (err) {
    if (err.message === 'FALLBACK_TTS') {
      if (onProgress) onProgress('Generating VOICEVOX audio...');
      if (!novelSentence) throw new Error('No novel sentence available.');
      return voicevoxFallback(novelSentence);
    }
    throw err;
  }
}
````

### `novel-audio-miner/src/lib/epubParser.js`

- Purpose: EPUB parsing or diagnostics.
- Size: 15870 bytes
- SHA-256: `2016a1b37f63015ebab4f944b97d56b10ff17af38d2603ab5b856a2a850839ad`

````javascript
import JSZip from 'jszip';
import { splitJapaneseSentences } from './japaneseSentenceSplitter.js';

export async function parseEpubFile(file) {
  const zip = await JSZip.loadAsync(await file.arrayBuffer());
  const container = parseXml(await readZipText(zip, 'META-INF/container.xml'));
  const opfPath = container.querySelector('rootfile')?.getAttribute('full-path');
  if (!opfPath) throw new Error('Could not find OPF package file.');
  const opf = parseXml(await readZipText(zip, opfPath));
  const opfDir = dirname(opfPath);
  const manifest = readManifest(opf, opfDir);
  const spine = readSpine(opf, manifest);
  const toc = await readToc(zip, opf, manifest);
  const meta = readMetadata(opf, file.name);

  const rawPages = [];
  for (const item of spine) {
    if (!item?.href || !isHtmlLike(item) || item.properties?.includes('nav')) continue;
    try {
      const html = await readZipText(zip, item.href);
      const page = extractPageWithOrdering(html, item.href, rawPages.length);
      rawPages.push(page);
    } catch (err) { console.warn('[Parser] Skipping spine item:', item.href, err); }
  }

  await fillImageDataUris(rawPages, zip);

  const chapters = buildSectionsFromToc(rawPages, toc);
  const pageChapterMap = new Map();
  chapters.forEach((chapter, ci) => {
    chapter.sourceHrefs.forEach(href => pageChapterMap.set(href, ci));
  });

  const flatItems = [];
  const chapterImageLists = {};
  chapters.forEach((_, ci) => chapterImageLists[ci] = []);

  rawPages.forEach(page => {
    if (looksLikeContentsPage(page, toc)) return;
    const chapterIdx = pageChapterMap.get(page.href) ?? -1;
    const chapter = chapterIdx >= 0 ? chapters[chapterIdx] : null;
    const chapterTitle = chapter?.title || '';

    for (const oi of (page.orderedItems || [])) {
      if (oi.type === 'image') {
        if (!oi.dataUri) continue;
        const imgEntry = { type: 'image', dataUri: oi.dataUri, alt: oi.alt || '', chapterIndex: chapterIdx, chapterTitle, parserDebug: { ...(oi.parserDebug || {}), chapterIndex: chapterIdx, chapterTitle } };
        flatItems.push(imgEntry);
        if (chapterIdx >= 0) chapterImageLists[chapterIdx].push(imgEntry);
      } else {
        flatItems.push({
          type: 'sentence',
          plainText: oi.plainText || '',
          htmlText: oi.htmlText || '',
          chapterIndex: chapterIdx,
          chapterTitle,
          parserDebug: { ...(oi.parserDebug || {}), chapterIndex: chapterIdx, chapterTitle }
        });
      }
    }
  });

  return {
    id: await quickHash(`${file.name}:${file.size}:${file.lastModified}`),
    fileName: file.name,
    title: meta.title || file.name.replace(/\.epub$/i, ''),
    author: meta.creator || '',
    toc,
    chapters,
    flatItems,
    chapterImageLists,
    debug: {
      tocCount: toc.length,
      totalItems: flatItems.length,
      sentenceCount: flatItems.filter(i => i.type === 'sentence').length,
      imageCount: flatItems.filter(i => i.type === 'image').length,
      chapterList: chapters.map((c, i) => ({
        title: c.title,
        sentenceCount: c.sentences.length,
        imageCount: (chapterImageLists[i] || []).length,
        preview: (c.plainText || '').slice(0, 80)
      })),
      pageList: rawPages.map(page => ({ href: page.href, title: page.title, orderedItemCount: (page.orderedItems || []).length, sentenceCount: (page.sentences || []).length, imageCount: (page.images || []).length }))
    }
  };
}

// ─── Rest of the file unchanged (extractPageWithOrdering, fillImageDataUris, helpers) ───

function extractPageWithOrdering(html, href, i) {
  const doc = parseHtml(html);
  const baseDir = dirname(href);
  doc.querySelectorAll('script,style,nav,aside,iframe,object').forEach(e => e.remove());
  const body = doc.body || doc.documentElement;

  const orderedItems = [];
  const allImages = [];
  const allSentences = [];
  const seenZipPaths = new Set();

  function walk(node) {
    if (!node) return;
    if (node.tagName === 'IMG') {
      const src = node.getAttribute('src') || '';
      if (src && !src.startsWith('data:')) {
        const zipPath = resolvePath(baseDir, src);
        if (!seenZipPaths.has(zipPath)) {
          seenZipPaths.add(zipPath);
          const alt = node.getAttribute('alt') || node.getAttribute('title') || '';
          allImages.push({ zipPath, alt, sourceHref: href, imageSrc: src });
          orderedItems.push({ type: 'image', zipPath, alt, dataUri: null, parserDebug: { itemType: 'image', pageHref: href, pageIndex: i, orderedIndex: orderedItems.length, imageSrc: src, resolvedZipPath: zipPath, alt, imageExists: null, hasDataUri: false } });
        }
      }
      return;
    }

    const selector = 'p,h1,h2,h3,h4,h5,h6,li,blockquote,div';
    if (node.nodeType === 1 && node.matches && node.matches(selector)) {
      const c = node.cloneNode(true);
      c.querySelectorAll('rt,rp').forEach(n => n.remove());
      const plain = cleanupText(c.textContent || '');
      if (plain && plain.length >= 2) {
        const childBlocks = node.querySelectorAll(selector);
        const childLength = [...childBlocks].filter(x => x !== node)
          .map(x => { const cc = x.cloneNode(true); cc.querySelectorAll('rt,rp').forEach(n => n.remove()); return cleanupText(cc.textContent || '').length; })
          .reduce((a, b) => a + b, 0);
        if (childLength <= plain.length * 0.6) {
          const split = splitJapaneseSentences(plain);
          if (split.length) {
            const hasRuby = !!node.querySelector('ruby,rt');
            const htmlClean = sanitizeReaderHtml(node.innerHTML || '');
            if (split.length === 1 && hasRuby) {
              const sentenceItem = { plainText: split[0], htmlText: htmlClean, parserDebug: { itemType: 'sentence', pageHref: href, pageIndex: i, orderedIndex: orderedItems.length, plainTextLength: split[0].length, htmlTextLength: htmlClean.length, hasRuby: true } };
              allSentences.push(sentenceItem);
              orderedItems.push({ type: 'sentence', ...sentenceItem });
            } else {
              split.forEach(x => {
                const htmlText = escapeHtml(x);
                const s = { plainText: x, htmlText, parserDebug: { itemType: 'sentence', pageHref: href, pageIndex: i, orderedIndex: orderedItems.length, plainTextLength: x.length, htmlTextLength: htmlText.length, hasRuby: false } };
                allSentences.push(s);
                orderedItems.push({ type: 'sentence', ...s });
              });
            }
            return;
          }
        }
      }
    }

    if (node.childNodes) {
      for (const child of node.childNodes) {
        walk(child);
      }
    }
  }

  walk(body);

  if (orderedItems.length === 0) {
    const c = body.cloneNode(true);
    c.querySelectorAll('rt,rp').forEach(n => n.remove());
    const plain = cleanupText(c.textContent || '');
    splitJapaneseSentences(plain).forEach(x => {
      const htmlText = escapeHtml(x);
      const s = { plainText: x, htmlText, parserDebug: { itemType: 'sentence', pageHref: href, pageIndex: i, orderedIndex: orderedItems.length, plainTextLength: x.length, htmlTextLength: htmlText.length, fallback: true } };
      allSentences.push(s);
      orderedItems.push({ type: 'sentence', ...s });
    });
  }

  const title = getPageTitle(doc) || `Page ${i + 1}`;
  const plainText = cleanupText(allSentences.map(s => s.plainText).join('\n'));

  return { id: `page-${i}`, href, title, plainText, sentences: allSentences, images: allImages, orderedItems, parserDebug: { pageIndex: i, href, orderedItemCount: orderedItems.length, sentenceCount: allSentences.length, imageCount: allImages.length } };
}

function buildSectionsFromToc(rawPages, toc) {
  const pageIndexByHref = new Map(rawPages.map((p, i) => [stripFragment(p.href), i]));
  const contentHrefs = new Set(toc.filter(e => isGenericTocTitle(e.title)).map(e => stripFragment(e.href)));
  const tocSections = toc.filter(e => !isGenericTocTitle(e.title)).map(e => ({ ...e, pageIndex: pageIndexByHref.get(stripFragment(e.href)) })).filter(e => Number.isInteger(e.pageIndex)).sort((a, b) => a.pageIndex - b.pageIndex);
  const sections = [];
  const first = tocSections.length ? tocSections[0].pageIndex : 0;
  const prefacePages = rawPages.slice(0, first).filter(p => !contentHrefs.has(stripFragment(p.href)) && !looksLikeContentsPage(p, toc));
  if (prefacePages.some(p => p.sentences.length)) sections.push(combinePages('Preface', prefacePages, 'preface'));
  for (let i = 0; i < tocSections.length; i++) {
    const start = tocSections[i].pageIndex, end = i + 1 < tocSections.length ? tocSections[i + 1].pageIndex : rawPages.length;
    const pages = rawPages.slice(start, end).filter(p => !contentHrefs.has(stripFragment(p.href)) && !looksLikeContentsPage(p, toc));
    if (pages.some(p => p.sentences.length)) sections.push(combinePages(tocSections[i].title, pages, `section-${i}`));
  }
  if (!sections.length) rawPages.forEach((p, i) => { if (!looksLikeContentsPage(p, toc) && p.sentences.length) sections.push(combinePages(p.title || `Section ${i + 1}`, [p], `fallback-${i}`)); });
  return sections.map((s, i) => ({ ...s, id: `chapter-${i}`, index: i }));
}

function combinePages(title, pages, id) {
  const sentences = [], plainParts = [], sourceHrefs = [];
  pages.forEach(page => {
    sourceHrefs.push(page.href);
    if (!page.sentences.length && !page.plainText) return;
    if (page.plainText) plainParts.push(page.plainText);
    page.sentences.forEach(sentence => sentences.push(sentence));
  });
  return { id, href: pages[0]?.href || '', sourceHrefs, title, plainText: cleanupText(plainParts.join('\n')), sentences };
}

function looksLikeContentsPage(page, toc) {
  const title = cleanupText(page.title || ''), href = (page.href || '').toLowerCase(), text = cleanupText(page.plainText || '');
  if (isGenericTocTitle(title)) return true;
  if (/toc|contents?|nav|目次|もくじ|mokuji/i.test(href)) return true;
  if (/^(目次|もくじ|contents|index|table of contents)$/i.test(title)) return true;
  const chapterWords = (text.match(/プロローグ|エピローグ|第[一二三四五六七八九十百〇零0-9]+章|章|【|】|電撃文庫|奥付/g) || []).length;
  const punctuation = (text.match(/[。！？!?]/g) || []).length;
  if (chapterWords >= 4 && punctuation <= 1 && text.length < 900) return true;
  let matches = 0;
  toc.forEach(e => { if (e.title && text.includes(e.title)) matches += 1; });
  return toc.length >= 3 && matches >= Math.min(4, toc.length) && punctuation <= 2;
}

async function fillImageDataUris(pages, zip) {
  for (const page of pages) {
    if (!page.orderedItems) continue;
    for (const item of page.orderedItems) {
      if (item.type === 'image' && item.zipPath && item.dataUri === null) {
        try {
          const imgFile = zip.file(item.zipPath);
          if (item.parserDebug) item.parserDebug.imageExists = Boolean(imgFile);
          if (imgFile) {
            const blob = await imgFile.async('blob');
            item.dataUri = URL.createObjectURL(blob);
            if (item.parserDebug) item.parserDebug.hasDataUri = true;
          }
        } catch (e) { if (item.parserDebug) item.parserDebug.error = e?.message || String(e); }
      }
    }
  }
}

async function readZipText(zip, path) { const f = zip.file(path); if (!f) throw new Error(`Missing file: ${path}`); return f.async('text'); }
function parseXml(t) { return new DOMParser().parseFromString(t, 'application/xml'); }
function parseHtml(t) { return new DOMParser().parseFromString(t, 'text/html'); }
function readMetadata(doc, fallback) { return { title: textOf(doc, 'metadata title') || textOf(doc, 'title') || fallback, creator: textOf(doc, 'metadata creator') || textOf(doc, 'creator') }; }
function readManifest(doc, dir) { const map = new Map(); doc.querySelectorAll('manifest item').forEach(item => { const id = item.getAttribute('id'), href = resolvePath(dir, item.getAttribute('href') || ''); if (id && href) map.set(id, { id, href, mediaType: item.getAttribute('media-type') || '', properties: item.getAttribute('properties') || '' }); }); return map; }
function readSpine(doc, manifest) { return [...doc.querySelectorAll('spine itemref')].map(x => manifest.get(x.getAttribute('idref'))).filter(Boolean); }
async function readToc(zip, opf, manifest) {
  let toc = [];
  const nav = [...manifest.values()].find(i => i.properties?.split(/\s+/).includes('nav')) || [...manifest.values()].find(i => /nav|toc|contents/i.test(i.href) && isHtmlLike(i));
  if (nav) { try { toc = parseNavToc(await readZipText(zip, nav.href), nav.href); } catch {} }
  if (!toc.length) { const id = opf.querySelector('spine')?.getAttribute('toc'); const ncx = id ? manifest.get(id) : [...manifest.values()].find(i => /ncx/i.test(i.mediaType) || /\.ncx$/i.test(i.href)); if (ncx) { try { toc = parseNcxToc(await readZipText(zip, ncx.href), ncx.href); } catch {} } }
  const seen = new Set(); return toc.map((e, i) => ({ ...e, index: i, title: cleanupText(e.title || ''), href: stripFragment(e.href || '') })).filter(e => e.title && e.href).filter(e => { const key = `${e.title}|${e.href}`; if (seen.has(key)) return false; seen.add(key); return true; });
}
function parseNavToc(html, href) { const xml = new DOMParser().parseFromString(html, 'application/xhtml+xml'), doc = xml.querySelector('parsererror') ? parseHtml(html) : xml, navs = [...doc.getElementsByTagName('nav')], nav = navs.find(n => [...n.attributes].some(a => /toc|contents|目次/i.test(a.value))) || navs[0] || doc, base = dirname(href); return [...nav.querySelectorAll('a[href]')].map(a => ({ title: cleanupText(a.textContent || ''), href: resolvePath(base, a.getAttribute('href') || '') })); }
function parseNcxToc(xml, href) { const doc = parseXml(xml), base = dirname(href); return [...doc.getElementsByTagName('navPoint')].map(p => ({ title: cleanupText(p.getElementsByTagName('text')[0]?.textContent || ''), href: resolvePath(base, p.getElementsByTagName('content')[0]?.getAttribute('src') || '') })); }

function isGenericTocTitle(t) { return ['contents', 'content', 'tableofcontents', '目次', 'もくじ'].includes(cleanupText(t).toLowerCase()); }
function getPageTitle(doc) { return cleanupText(doc.querySelector('h1,h2,h3,h4,.title,.chapter-title,[epub\\:type="title"]')?.textContent || ''); }
function textOf(doc, selector) { return cleanupText(doc.querySelector(selector)?.textContent || ''); }
function cleanupText(t) { return (t || '').replace(/\u00a0/g, ' ').replace(/[\t\r\f]+/g, ' ').replace(/\n+/g, '\n').replace(/ {2,}/g, ' ').trim(); }
function dirname(p) { const i = p.lastIndexOf('/'); return i >= 0 ? p.slice(0, i) : ''; }
function stripFragment(p) { return (p || '').split('#')[0]; }
function resolvePath(base, href) { const clean = decodeURIComponent((href || '').split('#')[0]), raw = base ? `${base}/${clean}` : clean, parts = []; raw.split('/').forEach(x => { if (!x || x === '.') return; x === '..' ? parts.pop() : parts.push(x); }); return parts.join('/'); }
function isHtmlLike(i) { return /xhtml|html/i.test(i.mediaType) || /\.(xhtml|html|htm)$/i.test(i.href); }
function sanitizeReaderHtml(html) { const d = document.createElement('div'); d.innerHTML = html; d.querySelectorAll('script,style,nav,aside,iframe,object').forEach(e => e.remove()); d.querySelectorAll('*').forEach(e => [...e.attributes].forEach(a => { const n = a.name.toLowerCase(); if (n.startsWith('on') || n === 'style') e.removeAttribute(a.name); })); return d.innerHTML; }
function escapeHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;'); }
async function quickHash(input) { const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input)); return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 16); }
````

### `novel-audio-miner/src/lib/frequencyMap.js`

- Purpose: JavaScript/React source.
- Size: 5286 bytes
- SHA-256: `87b5cb0bd60d33399901fe2f87a2d88ac86bae90e9dc293aa7e0059b9b720b9b`

````javascript
/**
 * Frequency map.
 *
 * Responsibility:
 * - Load local Yomitan-style frequency dictionaries from /public/dict/.
 * - Combine dictionary ranks into one global frequency map.
 * - Provide frequency category lookup for reader word coloring.
 *
 * Expected dictionary files:
 * - public/dict/jpdb.json
 * - public/dict/jiten.json
 * - public/dict/cc100.json
 * - public/dict/bccwj.json
 */

let globalMap = null;
let loadPromise = null;

const DB_NAME = 'novel-audio-miner';
const DB_VERSION = 3;
const STORE_NAME = 'globalFreq';
const GLOBAL_FREQUENCY_KEY = 'globalFrequency';

const DICT_NAMES = ['jpdb', 'jiten', 'cc100', 'bccwj'];

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (db.objectStoreNames.contains(STORE_NAME)) db.deleteObjectStore(STORE_NAME);
      db.createObjectStore(STORE_NAME);
    };
    request.onsuccess = (event) => resolve(event.target.result);
  });
}

async function loadCachedGlobalMap() {
  try {
    const db = await openDB();

    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const request = store.get(GLOBAL_FREQUENCY_KEY);

      request.onsuccess = () => resolve(request.result ? new Map(request.result) : null);
      request.onerror = () => reject(request.error);
    });
  } catch {
    return null;
  }
}

async function saveGlobalMap(map) {
  try {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);

    store.put([...map.entries()], GLOBAL_FREQUENCY_KEY);

    return new Promise((resolve, reject) => {
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
    });
  } catch {
    return undefined;
  }
}

function readFrequencyRank(payload) {
  if (typeof payload !== 'object' || payload === null) return null;

  if (typeof payload.value === 'number') return payload.value;
  if (typeof payload.frequency === 'number') return payload.frequency;
  if (payload.frequency && typeof payload.frequency === 'object' && typeof payload.frequency.value === 'number') {
    return payload.frequency.value;
  }

  return null;
}

function parseFrequencyArray(entries) {
  const map = new Map();

  for (const entry of entries) {
    if (!Array.isArray(entry) || entry.length < 3) continue;

    const [surface, type, payload] = entry;
    if (type !== 'freq') continue;

    const rank = readFrequencyRank(payload);
    if (rank == null || rank <= 0) continue;

    const existing = map.get(surface);
    if (existing === undefined || rank < existing) {
      map.set(surface, rank);
    }
  }

  return map;
}

async function fetchDictionary(name) {
  const response = await fetch(`/dict/${name}.json`);
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${name}`);

  const data = await response.json();
  return parseFrequencyArray(data);
}

function harmonicMean(ranks) {
  if (!ranks || ranks.length === 0) return null;

  let reciprocalSum = 0;
  for (const rank of ranks) reciprocalSum += 1 / rank;

  return Math.round(ranks.length / reciprocalSum);
}

async function loadDictionaryMaps() {
  const dictMaps = {};

  for (const name of DICT_NAMES) {
    try {
      dictMaps[name] = await fetchDictionary(name);
    } catch (error) {
      console.warn(`[Freq] Could not load ${name}:`, error.message);
      dictMaps[name] = new Map();
    }
  }

  return dictMaps;
}

function collectAllWords(dictMaps) {
  const words = new Set();

  for (const name of DICT_NAMES) {
    for (const word of dictMaps[name].keys()) words.add(word);
  }

  return words;
}

function combineDictionaryMaps(dictMaps) {
  const combined = new Map();

  for (const word of collectAllWords(dictMaps)) {
    const ranks = [];

    for (const name of DICT_NAMES) {
      const rank = dictMaps[name].get(word);
      if (rank) ranks.push(rank);
    }

    const meanRank = harmonicMean(ranks);
    if (meanRank) combined.set(word, meanRank);
  }

  return combined;
}

async function buildGlobalMap() {
  const dictMaps = await loadDictionaryMaps();
  const combined = combineDictionaryMaps(dictMaps);
  await saveGlobalMap(combined);
  return combined;
}

async function ensureGlobalMap() {
  const cached = await loadCachedGlobalMap();

  if (cached && cached.size > 0) {
    globalMap = cached;
    return;
  }

  globalMap = await buildGlobalMap();
}

function getCategory(rank) {
  if (!rank || rank <= 0) return 'unlisted';
  if (rank <= 4000) return 'very-common';
  if (rank <= 10000) return 'common';
  if (rank <= 20000) return 'uncommon';
  return 'rare';
}

export function startLoadingGlobalFrequency() {
  if (loadPromise) return loadPromise;

  loadPromise = ensureGlobalMap().catch((error) => {
    console.warn('[Freq] Failed to build global map:', error);
    globalMap = new Map();
  });

  return loadPromise;
}

export function getFrequency(word) {
  if (!globalMap) return null;

  const rank = globalMap.get(word);
  if (rank === undefined) return null;

  return { rank, category: getCategory(rank) };
}
````

### `novel-audio-miner/src/lib/japaneseSentenceSplitter.js`

- Purpose: JavaScript/React source.
- Size: 2383 bytes
- SHA-256: `b080d45b6dbe17a4077fbd1e07d5c9b3c0522fefc2ab296055e37c93557d3e0e`

````javascript
/**
 * Japanese sentence splitter.
 *
 * Responsibility:
 * - Normalize extracted Japanese text.
 * - Split paragraph/block text into sentence-like reader units.
 *
 * This module does not group short dialogue or merge reading units.
 * Any future grouping should be rebuilt after Debug Mode / parser diagnostics.
 */

const CLOSERS = `」』）)】〕〉》"'`;
const ENDERS = '。！？!?';
const QUOTE_OPEN = '「『';
const QUOTE_CLOSE = '」』';

export function normalizeJapaneseText(text) {
  return (text || '')
    .replace(/\u00a0/g, ' ')
    .replace(/[\t\r\f]+/g, ' ')
    .replace(/\s*\n\s*/g, '')
    .replace(/ {2,}/g, ' ')
    .trim();
}

function consumeEndingCluster(input, index, buffer) {
  while (index + 1 < input.length && ENDERS.includes(input[index + 1])) {
    index += 1;
    buffer += input[index];
  }
  while (index + 1 < input.length && CLOSERS.includes(input[index + 1])) {
    index += 1;
    buffer += input[index];
  }
  return { index, buffer };
}

export function splitJapaneseSentences(text) {
  const input = normalizeJapaneseText(text);
  if (!input) return [];
  const out = [];
  let buffer = '';
  let quoteDepth = 0;
  let quoteHasEnder = false;

  for (let i = 0; i < input.length; i++) {
    const ch = input[i];
    buffer += ch;
    if (QUOTE_OPEN.includes(ch)) { quoteDepth += 1; quoteHasEnder = false; continue; }
    if (quoteDepth > 0 && ENDERS.includes(ch)) {
      quoteHasEnder = true;
      const consumed = consumeEndingCluster(input, i, buffer);
      i = consumed.index;
      buffer = consumed.buffer;
      continue;
    }
    if (QUOTE_CLOSE.includes(ch) && quoteDepth > 0) {
      quoteDepth -= 1;
      if (quoteDepth === 0 && quoteHasEnder) {
        const consumed = consumeEndingCluster(input, i, buffer);
        i = consumed.index;
        buffer = consumed.buffer;
        const sentence = buffer.trim();
        if (sentence) out.push(sentence);
        buffer = '';
        quoteHasEnder = false;
      }
      continue;
    }
    if (quoteDepth === 0 && ENDERS.includes(ch)) {
      const consumed = consumeEndingCluster(input, i, buffer);
      i = consumed.index;
      buffer = consumed.buffer;
      const sentence = buffer.trim();
      if (sentence) out.push(sentence);
      buffer = '';
      quoteHasEnder = false;
    }
  }

  const tail = buffer.trim();
  if (tail) out.push(tail);
  return out;
}
````

### `novel-audio-miner/src/lib/jpAnalyzerClient.js`

- Purpose: JavaScript/React source.
- Size: 6618 bytes
- SHA-256: `57ba68a64303333ec908334b239ef9d7113be4dfb0fa9c1c6c253e8d32ee5e75`

````javascript
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
````

### `novel-audio-miner/src/lib/phase8DictionarySync.js`

- Purpose: Dictionary storage, sync, lookup, evidence, or UI.
- Size: 2622 bytes
- SHA-256: `361fffb3677c99801dd21ce554e67a111d8cee5fc3b2c76bd5ea049d4c09cc48`

````javascript
import { loadTermDictionaryEntriesForMeta, loadTermDictionaryMetas } from './dictionaryStorage.js';
const DEFAULT_URL='http://127.0.0.1:8771';
function compact(entry,meta){const rules=Array.isArray(entry?.rules)?entry.rules:String(entry?.rules||'').split(' ').filter(Boolean);return {term:String(entry?.term||entry?.text||'').normalize('NFKC').trim(),reading:String(entry?.reading||'').normalize('NFKC').trim(),dictionaryId:String(entry?.dictionaryId||meta.id||''),dictionaryTitle:String(entry?.sourceDictionary||meta.title||'unknown'),dictionaryType:String(entry?.dictionaryType||meta.type||'term'),dictionaryPriority:Number(entry?.dictionaryPriority??meta.priority??9999),tags:Array.isArray(entry?.tags)?entry.tags:[],rules,score:Number(entry?.score||0),sequence:entry?.sequence??null,nameType:entry?.nameType||'',grammarType:entry?.grammarType||'',expressionType:entry?.expressionType||''};}
async function request(url,path,options={}){const res=await fetch(`${url}${path}`,{headers:{'Content-Type':'application/json; charset=utf-8'},...options});if(!res.ok)throw new Error(`Dictionary sync failed: ${res.status} ${res.statusText} ${await res.text()}`);return res.json();}
export const getAnalyzerDictionaryStatus=({analyzerBaseUrl=DEFAULT_URL}={})=>request(analyzerBaseUrl,'/dictionary-sync/status');
export const clearAnalyzerDictionaryCache=({analyzerBaseUrl=DEFAULT_URL}={})=>request(analyzerBaseUrl,'/dictionary-sync/cache',{method:'DELETE'});
export async function syncIndexedDbDictionariesToAnalyzer({analyzerBaseUrl=DEFAULT_URL,batchSize=2000,onProgress,signal}={}){const metas=await loadTermDictionaryMetas();const total=metas.reduce((n,m)=>n+Number(m.entryCount||0),0);const started=await request(analyzerBaseUrl,'/dictionary-sync/start',{method:'POST',body:JSON.stringify({expectedEntries:total,dictionaryCount:metas.length}),signal});let sent=0;for(let mi=0;mi<metas.length;mi++){const meta=metas[mi],entries=await loadTermDictionaryEntriesForMeta(meta);for(let i=0;i<entries.length;i+=batchSize){if(signal?.aborted)throw new DOMException('Dictionary sync aborted','AbortError');const batch=entries.slice(i,i+batchSize).map(e=>compact(e,meta)).filter(e=>e.term);await request(analyzerBaseUrl,'/dictionary-sync/batch',{method:'POST',body:JSON.stringify({syncId:started.syncId,entries:batch}),signal});sent+=batch.length;onProgress?.({sent,total,dictionaryTitle:meta.title,dictionaryIndex:mi,dictionaryCount:metas.length});}}const final=await request(analyzerBaseUrl,'/dictionary-sync/finish',{method:'POST',body:JSON.stringify({syncId:started.syncId}),signal});return {...final,sent,expectedEntries:total};}
````

### `novel-audio-miner/src/lib/scenePrefetch.js`

- Purpose: JavaScript/React source.
- Size: 1152 bytes
- SHA-256: `fed68e1677d41eb82d731f3e35cbb7f5ad0da125e610cd09715d2f84231b68de`

````javascript
function normalizeText(value) {
  return String(value ?? '').trim();
}

function getTextScene(item) {
  if (!item || item.type !== 'scene') return null;
  const text = normalizeText(item.data?.plainText);
  return text ? { text, data: item.data } : null;
}

function findInDirection(items, currentIndex, step) {
  for (let index = currentIndex + step; index >= 0 && index < items.length; index += step) {
    const scene = getTextScene(items[index]);
    if (scene) {
      return {
        index,
        text: scene.text,
        direction: step > 0 ? 'next' : 'previous'
      };
    }
  }
  return null;
}

export function findAdjacentTextScenes(items, currentIndex) {
  const source = Array.isArray(items) ? items : [];
  const safeIndex = Number.isInteger(currentIndex) ? currentIndex : -1;
  const next = findInDirection(source, safeIndex, 1);
  const previous = findInDirection(source, safeIndex, -1);
  const seen = new Set();
  const ordered = [];

  for (const target of [next, previous]) {
    if (!target || seen.has(target.text)) continue;
    seen.add(target.text);
    ordered.push(target);
  }

  return { next, previous, ordered };
}
````

### `novel-audio-miner/src/lib/storage.js`

- Purpose: JavaScript/React source.
- Size: 866 bytes
- SHA-256: `9d37c2cb67b10b366493c51ff7605aa34cc6030df1afce986e7a5ce9caa2ed43`

````javascript
/**
 * Reader progress storage.
 *
 * Responsibility:
 * - Persist per-book reader state in localStorage.
 * - Return null if progress cannot be read safely.
 *
 * This module intentionally stores only UI/reader progress, not vocabulary data.
 * Known-word data belongs in wordCache.js.
 */

const PREFIX = 'novel-audio-miner:';

function progressKey(id) {
  return id ? `${PREFIX}${id}` : '';
}

export function saveProgress(id, state) {
  const key = progressKey(id);
  if (!key) return;

  try {
    localStorage.setItem(key, JSON.stringify(state));
  } catch {
    // Ignore storage failures. Reader progress is useful but non-critical.
  }
}

export function getProgress(id) {
  const key = progressKey(id);
  if (!key) return null;

  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}
````

### `novel-audio-miner/src/lib/useJpAnalyzerShadow.js`

- Purpose: JavaScript/React source.
- Size: 11508 bytes
- SHA-256: `dda710873a39f1bc93137c3e129954bab6f1ba6d299825ef52b57213b1f3fe83`

````javascript
import { useEffect, useMemo, useRef, useState } from 'react';
import { analyzeSentence, getAnalyzerHealth } from './jpAnalyzerClient.js';
import {
  ANALYZER_CACHE_PREFIX,
  createAnalyzerCacheIdentity,
  createAnalyzerCacheRecord,
  normalizeAnalyzerMetadata,
  validateAnalyzerCacheRecord
} from './analyzerCacheIdentity.js';
import {
  clearAnalyzerMetadataLease,
  getAnalyzerMetadataLease,
  setAnalyzerMetadataLease
} from './analyzerMetadataLease.js';

const MAX_PERSISTED_ENTRIES = 100;
const memoryCache = new Map();
const pendingRequests = new Map();
let backgroundQueue = Promise.resolve();

function initial() {
  return {
    status: 'idle', source: null, result: null, error: null, elapsedMs: null,
    cacheKey: null, cacheIdentity: null, cacheReason: null, correctionRevision: null,
    analyzerVersion: null, readerSpanSchemaVersion: null,
    inFlightRequestCount: pendingRequests.size,
    prefetchStatus: 'idle', prefetchTargetCount: 0,
    prefetchCompletedCount: 0, prefetchFailedCount: 0
  };
}

async function textHash(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest))
    .map(value => value.toString(16).padStart(2, '0'))
    .join('');
}

function storageKey(identity) { return ANALYZER_CACHE_PREFIX + identity; }
function removeStored(identity) { try { localStorage.removeItem(storageKey(identity)); } catch {} }

function readStored(identity, text, hash, metadata) {
  try {
    const raw = localStorage.getItem(storageKey(identity));
    if (!raw) return null;
    const record = JSON.parse(raw);
    const check = validateAnalyzerCacheRecord(record, text, hash, metadata);
    if (!check.valid) { removeStored(identity); return null; }
    record.lastAccessedAt = new Date().toISOString();
    localStorage.setItem(storageKey(identity), JSON.stringify(record));
    return record;
  } catch {
    removeStored(identity);
    return null;
  }
}

function trimStorage() {
  try {
    const rows = [];
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index);
      if (!key?.startsWith(ANALYZER_CACHE_PREFIX)) continue;
      try {
        const value = JSON.parse(localStorage.getItem(key));
        rows.push({ key, at: value?.lastAccessedAt || value?.savedAt || '' });
      } catch {
        rows.push({ key, at: '' });
      }
    }
    rows.sort((a, b) => String(b.at).localeCompare(String(a.at)))
      .slice(MAX_PERSISTED_ENTRIES)
      .forEach(row => localStorage.removeItem(row.key));
  } catch {}
}

function persist(record) {
  try {
    localStorage.setItem(storageKey(record.cacheIdentity), JSON.stringify(record));
    trimStorage();
  } catch {}
}

function requestAnalysis(identity, text) {
  if (pendingRequests.has(identity)) return pendingRequests.get(identity);
  const started = performance.now();
  const request = analyzeSentence(text)
    .then(result => ({ result, elapsedMs: Math.round(performance.now() - started) }))
    .finally(() => pendingRequests.delete(identity));
  pendingRequests.set(identity, request);
  return request;
}

async function resolveSentence(text, metadata) {
  const sourceText = String(text ?? '').trim();
  if (!sourceText) return { source: 'skipped', record: null, elapsedMs: 0, hash: null, identity: null };

  const normalizedMetadata = normalizeAnalyzerMetadata(metadata);
  if (!normalizedMetadata.valid) throw new Error('JP Analyzer health lacks cache identity metadata.');
  const hash = await textHash(sourceText);
  const identity = createAnalyzerCacheIdentity(hash, normalizedMetadata);
  if (!identity) throw new Error('Could not create analyzer cache identity.');

  const memoryRecord = memoryCache.get(identity);
  const memoryCheck = validateAnalyzerCacheRecord(
    memoryRecord, sourceText, hash, normalizedMetadata
  );
  if (memoryCheck.valid) {
    return { source: 'memory-cache', record: memoryRecord, elapsedMs: 0, hash, identity };
  }
  if (memoryRecord) memoryCache.delete(identity);

  const stored = readStored(identity, sourceText, hash, normalizedMetadata);
  if (stored) {
    memoryCache.set(identity, stored);
    return { source: 'persistent-cache', record: stored, elapsedMs: 0, hash, identity };
  }

  const response = await requestAnalysis(identity, sourceText);
  const responseMetadata = normalizeAnalyzerMetadata(response.result);
  if (createAnalyzerCacheIdentity(hash, responseMetadata) !== identity) {
    throw new Error('Analyzer metadata changed during analysis; result was not cached.');
  }

  const record = createAnalyzerCacheRecord(
    response.result, hash, normalizedMetadata
  );
  const check = validateAnalyzerCacheRecord(
    record, sourceText, hash, normalizedMetadata
  );
  if (!check.valid) throw new Error(`Analyzer result is not cacheable: ${check.reason}`);
  memoryCache.set(identity, record);
  persist(record);
  return { source: 'network', record, elapsedMs: response.elapsedMs, hash, identity };
}

function enqueueBackground(task) {
  const result = backgroundQueue.then(task, task);
  backgroundQueue = result.catch(() => {});
  return result;
}

export async function prefetchJpAnalyzerSentences(texts, metadata, onProgress) {
  const uniqueTexts = [...new Set((texts || []).map(value => String(value ?? '').trim()).filter(Boolean))];
  const summary = { targetCount: uniqueTexts.length, completedCount: 0, failedCount: 0, results: [] };

  for (const text of uniqueTexts) {
    await enqueueBackground(async () => {
      try {
        const result = await resolveSentence(text, metadata);
        summary.completedCount += 1;
        summary.results.push({ text, source: result.source, status: 'ready' });
      } catch (error) {
        summary.failedCount += 1;
        summary.results.push({ text, status: 'error', error: error?.message ?? String(error) });
      }
      onProgress?.({ ...summary, results: [...summary.results] });
    });
  }
  return summary;
}

export function clearJpAnalyzerShadowCache() {
  memoryCache.clear();
  clearAnalyzerMetadataLease();
  try {
    const keys = [];
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index);
      if (key?.startsWith(ANALYZER_CACHE_PREFIX)) keys.push(key);
    }
    keys.forEach(key => localStorage.removeItem(key));
  } catch {}
}

export function getJpAnalyzerShadowCacheSize() { return memoryCache.size; }

export function useJpAnalyzerShadow(text, { enabled = true, prefetchTexts = [] } = {}) {
  const sourceText = String(text ?? '');
  const generation = useRef(0);
  const [state, setState] = useState(initial);
  const stablePrefetchTexts = useMemo(
    () => [...new Set((prefetchTexts || []).map(value => String(value ?? '').trim()).filter(Boolean))],
    [JSON.stringify(prefetchTexts || [])]
  );
  const prefetchSignature = stablePrefetchTexts.join('\u0000');

  useEffect(() => {
    generation.current += 1;
    const runId = generation.current;
    if (!enabled || !sourceText.trim()) { setState(initial()); return; }
    let disposed = false;

    async function runPrefetch(metadata) {
      if (!stablePrefetchTexts.length) return;
      setState(previous => previous.status === 'ready'
        ? { ...previous, prefetchStatus: 'running' }
        : previous);
      const summary = await prefetchJpAnalyzerSentences(
        stablePrefetchTexts,
        metadata,
        progress => {
          if (disposed || runId !== generation.current) return;
          setState(previous => previous.status === 'ready' ? {
            ...previous,
            prefetchStatus: 'running',
            prefetchTargetCount: progress.targetCount,
            prefetchCompletedCount: progress.completedCount,
            prefetchFailedCount: progress.failedCount,
            inFlightRequestCount: pendingRequests.size
          } : previous);
        }
      );
      if (disposed || runId !== generation.current) return;
      if (summary.completedCount > 0) {
        // Successful cache resolution under this authoritative identity keeps
        // the immediate-navigation lease fresh after a long prefetch cycle.
        setAnalyzerMetadataLease(metadata);
      }
      setState(previous => previous.status === 'ready' ? {
        ...previous,
        prefetchStatus: summary.failedCount ? 'complete-with-errors' : 'complete',
        prefetchTargetCount: summary.targetCount,
        prefetchCompletedCount: summary.completedCount,
        prefetchFailedCount: summary.failedCount,
        inFlightRequestCount: pendingRequests.size
      } : previous);
    }

    function publishForeground(foreground, metadata, reasonPrefix = 'validated') {
      const common = {
        correctionRevision: metadata.correctionRevision,
        analyzerVersion: metadata.analyzerVersion,
        readerSpanSchemaVersion: metadata.readerSpanSchemaVersion
      };
      setState({
        ...initial(), ...common, status: 'ready', source: foreground.source,
        result: foreground.record, elapsedMs: foreground.elapsedMs,
        cacheKey: foreground.hash, cacheIdentity: foreground.identity,
        cacheReason: foreground.source === 'network'
          ? 'network-result-cached'
          : `${reasonPrefix}-${foreground.source}-hit`,
        inFlightRequestCount: pendingRequests.size,
        prefetchStatus: stablePrefetchTexts.length ? 'queued' : 'idle',
        prefetchTargetCount: stablePrefetchTexts.length
      });
    }

    async function run() {
      const leasedMetadata = getAnalyzerMetadataLease();
      if (!leasedMetadata) {
        setState({ ...initial(), status: 'metadata', cacheReason: 'checking-authoritative-metadata' });
      }

      try {
        if (leasedMetadata) {
          const leasedForeground = await resolveSentence(sourceText, leasedMetadata);
          if (disposed || runId !== generation.current) return;
          publishForeground(leasedForeground, leasedMetadata, 'leased');
        }

        const health = await getAnalyzerHealth();
        const metadata = normalizeAnalyzerMetadata(health);
        if (!metadata.valid) throw new Error('JP Analyzer health lacks cache identity metadata.');
        setAnalyzerMetadataLease(metadata);

        const leaseStillMatches = leasedMetadata &&
          leasedMetadata.analyzerVersion === metadata.analyzerVersion &&
          leasedMetadata.readerSpanSchemaVersion === metadata.readerSpanSchemaVersion &&
          leasedMetadata.correctionRevision === metadata.correctionRevision;

        if (!leaseStillMatches) {
          const foreground = await resolveSentence(sourceText, metadata);
          if (disposed || runId !== generation.current) return;
          publishForeground(foreground, metadata);
        }

        await runPrefetch(metadata);
      } catch (error) {
        clearAnalyzerMetadataLease();
        if (disposed || runId !== generation.current) return;
        setState(previous => {
          if (previous.status === 'ready') {
            return {
              ...previous,
              prefetchStatus: 'complete-with-errors',
              prefetchFailedCount: Math.max(1, previous.prefetchFailedCount),
              error
            };
          }
          return {
            ...initial(), status: 'error', source: 'network', error,
            cacheReason: 'metadata-or-analysis-failed'
          };
        });
      }
    }

    run();
    return () => { disposed = true; };
  }, [sourceText, enabled, prefetchSignature]);

  return state;
}
````

### `novel-audio-miner/src/lib/wordCache.js`

- Purpose: JavaScript/React source.
- Size: 6299 bytes
- SHA-256: `9736d0cf5b2bdc96c5066037430246e49c4cbbdaddf7b797d4f3db2a4ec14236`

````javascript
/**
 * Known Words Cache v3.1
 *
 * Separates Anki-derived known words from words manually marked known in
 * Novel Audio Miner.
 *
 * - Anki cache can be cleared/rebuilt safely.
 * - Manual known words persist until explicitly removed.
 * - Known word count is the union of Anki known + manual known.
 */

const ANKI_CACHE_KEY = 'novel-audio-miner:ankiWordCache';
const MANUAL_KNOWN_KEY = 'novel-audio-miner:manualKnownWords';
const LEGACY_CACHE_KEY = 'novel-audio-miner:wordCache';
const CACHE_VERSION = 3;
const CACHE_TTL_DAYS = 7;

const NOTE_TYPE_FIELDS = {
  'Kaishi 1.5k': 'Word',
  'JP1Kv3': 'Word',
  'ImmersionKitCard': 'Word',
  'Kiku': 'Expression'
};

let ankiCache = null;
let manualKnownCache = null;

function loadSet(key, { ttl = false } = {}) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const data = JSON.parse(raw);
    if (data.version !== CACHE_VERSION) return null;
    if (ttl) {
      const age = Date.now() - (data.timestamp || 0);
      if (age > CACHE_TTL_DAYS * 24 * 60 * 60 * 1000) return null;
    }
    return new Set(data.words || []);
  } catch {
    return null;
  }
}

function saveSet(key, wordsSet) {
  try {
    localStorage.setItem(key, JSON.stringify({
      version: CACHE_VERSION,
      timestamp: Date.now(),
      words: [...wordsSet]
    }));
  } catch {
    console.warn(`[WordCache] Could not save ${key} to localStorage`);
  }
}

function loadManualKnownWords() {
  if (manualKnownCache) return manualKnownCache;
  manualKnownCache = loadSet(MANUAL_KNOWN_KEY) || new Set();
  return manualKnownCache;
}

function loadAnkiCache() {
  if (ankiCache) return ankiCache;
  ankiCache = loadSet(ANKI_CACHE_KEY, { ttl: true });
  return ankiCache;
}

function getUnionKnownWords() {
  const anki = loadAnkiCache() || new Set();
  const manual = loadManualKnownWords();
  return new Set([...anki, ...manual]);
}

export async function getKnownWords(ankiRequestFn, onProgress) {
  const cachedAnki = loadAnkiCache();
  loadManualKnownWords();
  if (cachedAnki && cachedAnki.size > 0) {
    console.log('[WordCache] Loaded Anki cache:', cachedAnki.size, 'manual:', manualKnownCache.size);
    return getUnionKnownWords();
  }
  return buildCache(ankiRequestFn, onProgress);
}

export async function buildCache(ankiRequestFn, onProgress) {
  console.log('[WordCache] Building Anki cache...');
  const words = new Set();

  for (const [noteType, fieldName] of Object.entries(NOTE_TYPE_FIELDS)) {
    if (onProgress) onProgress(`Reading ${noteType} cards...`);
    try {
      const noteIds = await ankiRequestFn('findNotes', { query: `note:\"${noteType}\"` });
      console.log(`[WordCache] ${noteType}: ${noteIds.length} notes found`);
      if (!noteIds.length) continue;

      for (let i = 0; i < noteIds.length; i += 500) {
        if (onProgress) onProgress(`Reading ${noteType}: ${Math.min(i + 500, noteIds.length)} / ${noteIds.length}`);
        const batch = noteIds.slice(i, i + 500);
        const notes = await ankiRequestFn('notesInfo', { notes: batch });

        for (const note of notes) {
          const value = note.fields?.[fieldName]?.value || '';
          const trimmed = value.trim();
          if (trimmed) words.add(trimmed);
        }
      }
    } catch (err) {
      console.warn(`[WordCache] Failed to read \"${noteType}\":`, err.message);
    }
  }

  ankiCache = words;
  saveSet(ANKI_CACHE_KEY, ankiCache);
  loadManualKnownWords();
  console.log('[WordCache] Built Anki:', ankiCache.size, 'manual:', manualKnownCache.size, 'total:', getUnionKnownWords().size);
  return getUnionKnownWords();
}

export function addManualKnownWord(word) {
  if (!word || typeof word !== 'string') return false;
  const trimmed = word.trim();
  if (!trimmed) return false;
  const manual = loadManualKnownWords();
  if (manual.has(trimmed)) return false;
  manual.add(trimmed);
  saveSet(MANUAL_KNOWN_KEY, manual);
  console.log('[WordCache] Added manual known:', trimmed, 'manual:', manual.size, 'total:', getUnionKnownWords().size);
  return true;
}

// Backward-compatible name. Manual UI and post-mining updates should persist.
export function addKnownWord(word) {
  addManualKnownWord(word);
}

export function removeManualKnownWord(word) {
  if (!word || typeof word !== 'string') return false;
  const trimmed = word.trim();
  if (!trimmed) return false;
  const manual = loadManualKnownWords();
  if (!manual.has(trimmed)) return false;
  manual.delete(trimmed);
  saveSet(MANUAL_KNOWN_KEY, manual);
  console.log('[WordCache] Removed manual known:', trimmed, 'manual:', manual.size, 'total:', getUnionKnownWords().size);
  return true;
}

export function isManualKnownWord(word) {
  if (!word || typeof word !== 'string') return false;
  return loadManualKnownWords().has(word.trim());
}

export function isAnkiKnownWord(word) {
  if (!word || typeof word !== 'string') return false;
  const anki = loadAnkiCache();
  return !!anki && anki.has(word.trim());
}

export function isKnownWord(word) {
  if (!word || typeof word !== 'string') return false;
  const trimmed = word.trim();
  if (!trimmed) return false;
  return isManualKnownWord(trimmed) || isAnkiKnownWord(trimmed);
}

export function getManualKnownWords() {
  return new Set(loadManualKnownWords());
}

// Important: return union size, not just Anki cache size and not anki+manual sum.
// This makes the status-bar count include persistent manual-known words while
// avoiding double-counting words that exist in both Anki and manual known.
export function getCacheSize() {
  return getUnionKnownWords().size;
}

export function getCacheStats() {
  const anki = loadAnkiCache() || new Set();
  const manual = loadManualKnownWords();
  return {
    anki: anki.size,
    manual: manual.size,
    total: getUnionKnownWords().size
  };
}

// Clears only the Anki-derived cache. Manual known words are preserved.
export function clearCache() {
  ankiCache = null;
  try {
    localStorage.removeItem(ANKI_CACHE_KEY);
    localStorage.removeItem(LEGACY_CACHE_KEY);
  } catch {}
  console.log('[WordCache] Cleared Anki cache. Manual known words preserved.');
}

export function clearManualKnownWords() {
  manualKnownCache = new Set();
  saveSet(MANUAL_KNOWN_KEY, manualKnownCache);
  console.log('[WordCache] Cleared manual known words.');
}
````

### `novel-audio-miner/src/main.jsx`

- Purpose: JavaScript/React source.
- Size: 347 bytes
- SHA-256: `e0184dd19789caef1e69388a6ae7ca5a2b92d4178f387a23605087edbe0bfa7f`

````jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element #root was not found.');
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>
);
````

### `novel-audio-miner/src/styles.css`

- Purpose: Project source or support file.
- Size: 15730 bytes
- SHA-256: `90f88426d3495668945e0d68ba41e276c3b65ecdc83ed50dd12fd3d034b5489b`

````css
/* ─── v4.1 Minimalist Dark Theme with Comprehension Colors ─── */
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #21262d;
  --text: #c9d1d9;
  --muted: #8b949e;
  --accent: #58a6ff;
  --accent-hover: #79c0ff;
  --success: #3fb950;
  --warning: #d2991d;
  --danger: #f85149;
  --radius: 10px;
  /* Word highlight colors */
  --word-known: #3fb950;
  --word-common: #d2991d;
  --word-uncommon: #db6d28;
  --word-rare: #f85149;
  --word-unlisted: #8b949e;
  --word-name: #a78bfa;
  --word-numeric: #7dd3fc;
  --word-function: #8b949e;
  --word-grammar: #79c0ff;
  --word-unresolved: #6e7681;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow: hidden;
  height: 100vh;
}
#root { height: 100%; }
.app-shell { display: flex; flex-direction: column; height: 100%; }

/* ─── Status Bar ─── */
.status-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 16px; background: var(--surface); border-bottom: 1px solid var(--border);
  font-size: 12px; color: var(--muted);
}
.status-bar .status-left, .status-bar .status-right { display: flex; align-items: center; gap: 12px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.ok { background: var(--success); }
.status-dot.error { background: var(--danger); }
.status-dot.warn { background: var(--warning); }

/* ─── Top bar ─── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px; background: var(--surface); border-bottom: 1px solid var(--border);
}
.topbar h1 { font-size: 18px; font-weight: 600; color: var(--text); }
.topbar .version { font-size: 11px; color: var(--muted); margin-left: 8px; }
.topbar button { padding: 6px 14px; font-size: 13px; }

/* ─── Main layout ─── */
.main-layout { display: flex; flex: 1; overflow: hidden; position: relative; }

/* ─── Collapsible Sidebar ─── */
.sidebar {
  width: 280px; flex-shrink: 0; background: var(--surface); border-right: 1px solid var(--border);
  padding: 16px; overflow-y: auto; transition: margin-left 0.25s ease, opacity 0.25s ease;
  display: flex; flex-direction: column; gap: 14px;
}
.sidebar.collapsed { margin-left: -280px; opacity: 0; pointer-events: none; }
.sidebar-toggle {
  position: absolute; left: 0; top: 0; z-index: 10; padding: 8px 10px;
  background: var(--surface); border: 1px solid var(--border); border-left: none;
  border-radius: 0 8px 8px 0; cursor: pointer; color: var(--text); font-size: 16px;
}
.sidebar h2 { font-size: 15px; font-weight: 600; color: var(--text); }
.sidebar .book-author { font-size: 12px; color: var(--muted); margin-top: -8px; }

/* ─── Chapter selector ─── */
.chapter-select { width: 100%; padding: 8px; border-radius: var(--radius); background: var(--bg); color: var(--text); border: 1px solid var(--border); font-size: 13px; }
.section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 4px; }

/* ─── Image thumbnails ─── */
.image-thumbs { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.image-thumb { border-radius: 8px; overflow: hidden; border: 1px solid var(--border); cursor: pointer; transition: border-color 0.2s; position: relative; }
.image-thumb:hover { border-color: var(--accent); }
.image-thumb img { width: 100%; height: 64px; object-fit: cover; display: block; filter: blur(4px) brightness(0.5); }
.image-thumb .thumb-label { position: absolute; bottom: 2px; left: 2px; font-size: 9px; background: rgba(0,0,0,0.7); color: var(--muted); padding: 1px 4px; border-radius: 4px; }

/* ─── Reader area ─── */
.reader-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 16px; }

/* ─── Navigation header ─── */
.nav-header {
  display: flex; align-items: center; justify-content: space-between;
  padding-bottom: 12px; gap: 12px;
}
.nav-header .chapter-info { font-size: 13px; color: var(--muted); }
.nav-header .nav-controls { display: flex; align-items: center; gap: 6px; }
.nav-controls input[type="number"] {
  width: 64px; text-align: center; background: var(--bg); color: var(--text);
  border: 1px solid var(--border); border-radius: 6px; padding: 6px 8px; font-size: 13px;
}
.nav-controls button { padding: 6px 10px; font-size: 13px; }
.nav-header .item-counter { font-size: 13px; color: var(--muted); }

/* ─── Sentence box ─── */
.sentence-box {
  flex: 1; display: flex; align-items: center; justify-content: center;
  padding: 40px; background: var(--surface); border-radius: 16px;
  border: 1px solid var(--border); min-height: 300px;
  user-select: text; cursor: pointer; white-space: pre-wrap;
  letter-spacing: 0.02em;
}
.sentence-box.vertical {
  writing-mode: vertical-rl; text-orientation: upright;
  align-items: flex-start; justify-content: flex-start;
  overflow-x: auto; overflow-y: hidden; padding: 40px 50px;
}
.sentence-box.vertical > span { display: inline-block; max-height: 100%; }
.sentence-box ruby rt { font-size: 0.4em; color: var(--accent); }
.vertical-dash-fix {
  display: inline-flex; writing-mode: horizontal-tb; text-orientation: mixed;
  width: 1em; height: 1em; align-items: center; justify-content: center;
  line-height: 1; transform: translateY(0.02em);
}

/* ─── Color-coded words ─── */
.word-known { color: var(--word-known); }
.word-unknown { color: var(--text); }
.word-unknown.word-freq-very-common { color: var(--word-common); font-weight: 600; }
.word-unknown.word-freq-common { color: var(--word-common); }
.word-unknown.word-freq-uncommon { color: var(--word-uncommon); }
.word-unknown.word-freq-rare { color: var(--word-rare); }
.word-unknown.word-freq-unlisted { color: var(--word-unlisted); }
.word-name { color: var(--word-name); }
.word-numeric { color: var(--word-numeric); }
.word-function { color: var(--word-function); }
.word-grammar { color: var(--word-grammar); font-weight: 600; }
.word-neutral { color: inherit; }
.word-unresolved { color: var(--word-unresolved); }


/* ─── New word controls ─── */
.word-badge-pair {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  margin: 1px;
}
.word-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  cursor: pointer;
}
.word-badge:hover { border-color: var(--accent); }
.mark-known-mini {
  padding: 2px 5px;
  border-radius: 4px;
  font-size: 11px;
  line-height: 1.2;
  background: rgba(63,185,80,0.14);
  color: var(--success);
  border: 1px solid rgba(63,185,80,0.35);
}
.mark-known-mini:hover { background: rgba(63,185,80,0.24); }
.mark-known-btn {
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 13px;
}

/* ─── Image panel ─── */
.image-panel {
  margin-top: 12px; border-radius: 14px; overflow: hidden;
  border: 1px solid var(--border); cursor: pointer; position: relative;
  background: var(--surface); display: flex; align-items: center; justify-content: center;
  min-height: 280px;
}
.image-panel img { width: 100%; height: auto; max-height: 70vh; object-fit: contain; display: block; transition: filter 0.3s; }
.image-panel img.blurred { filter: blur(36px) brightness(0.35); }
.image-panel .unblur-btn {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  background: rgba(0,0,0,0.8); color: #fff; border: 1px solid var(--border);
  padding: 10px 22px; border-radius: 999px; font-size: 14px; z-index: 2; cursor: pointer;
}
.image-panel .image-caption { font-size: 12px; color: var(--muted); padding: 8px 14px; text-align: center; background: rgba(0,0,0,0.5); }

/* ─── Floating Action Bar ─── */
.action-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px; background: var(--surface); border-top: 1px solid var(--border);
  margin-top: auto; border-radius: 12px 12px 0 0;
}
.action-bar .selected-word { display: flex; align-items: center; gap: 8px; overflow: hidden; }
.selected-word .label { font-size: 11px; color: var(--muted); white-space: nowrap; }
.selected-word .word {
  font-size: 20px; font-weight: 700; color: var(--text);
  max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.action-bar .mine-btn {
  background: var(--accent); color: #000; font-weight: 700; font-size: 15px;
  padding: 12px 24px; border-radius: 999px; cursor: pointer; border: none;
  transition: background 0.2s;
}
.action-bar .mine-btn:hover { background: var(--accent-hover); }
.action-bar .mine-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.action-bar .mine-status { font-size: 12px; color: var(--muted); }

/* ─── Buttons & inputs ─── */
button {
  background: var(--accent); color: #000; border: none; border-radius: 8px;
  padding: 8px 16px; font-weight: 600; cursor: pointer; font-size: 14px;
}
button.secondary { background: var(--border); color: var(--text); }
button:disabled { opacity: 0.35; cursor: not-allowed; }

/* ─── Upload card ─── */
.upload-card {
  max-width: 520px; margin: 100px auto 0; text-align: center;
  padding: 48px 32px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 20px;
}
.upload-card h2 { font-size: 24px; margin-bottom: 12px; }
.upload-card p { color: var(--muted); margin-bottom: 24px; }
.file-button {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 200px; height: 48px; border-radius: 999px; background: var(--accent);
  color: #000; font-weight: 700; cursor: pointer;
}
.file-button input { display: none; }
.small-note { font-size: 13px; color: var(--muted); margin-top: 20px; }
.error-box { padding: 12px 16px; color: var(--danger); background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.2); border-radius: 10px; margin: 8px 16px; }

/* ─── Style panel ─── */
.style-panel { background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 12px; }
.style-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--muted); margin: 8px 0; }
.style-row button { padding: 2px 8px; font-size: 12px; }
.style-row b { min-width: 32px; text-align: center; color: var(--text); }
input[type="range"] { width: 100%; accent-color: var(--accent); }

/* ─── Advanced settings ─── */
.advanced-settings summary { font-size: 12px; color: var(--muted); cursor: pointer; }
.advanced-settings input, .advanced-settings select {
  width: 100%; background: var(--bg); color: var(--text); border: 1px solid var(--border);
  border-radius: 6px; padding: 6px 8px; font-size: 12px;
}

/* ─── Status messages ─── */
.status-message {
  padding: 8px 12px; border-radius: 8px; font-size: 12px;
}
.status-message.error { background: rgba(248,81,73,0.1); color: var(--danger); }
.status-message.ok { background: rgba(63,185,80,0.1); color: var(--success); }
.status-message.working { background: rgba(210,153,29,0.1); color: var(--warning); }

/* ─── Responsive ─── */
@media (max-width: 768px) {
  .sidebar { width: 100%; position: fixed; top: 0; left: 0; bottom: 0; z-index: 50; }
  .sidebar.collapsed { margin-left: -100%; }
  .reader-area { padding: 10px; }
}


/* Debug Mode v5 */
.debug-panel { border: 1px solid var(--border); border-radius: 10px; background: rgba(13,17,23,0.45); padding: 10px; display: grid; gap: 10px; font-size: 11px; }
.debug-panel-title-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.debug-panel-title { font-size: 12px; font-weight: 700; color: var(--accent); letter-spacing: 0.02em; }
.debug-export-btn { border: 1px solid var(--border); border-radius: 999px; background: rgba(88,166,255,0.12); color: var(--accent); padding: 4px 9px; cursor: pointer; font-size: 10px; font-weight: 700; }
.debug-export-btn:hover { background: rgba(88,166,255,0.2); }
.debug-panel details { border: 1px solid rgba(139,148,158,0.18); border-radius: 8px; padding: 8px; background: rgba(1,4,9,0.35); }
.debug-panel summary { cursor: pointer; color: var(--muted); font-weight: 600; }
.debug-kv-list { display: grid; gap: 4px; margin-top: 8px; }
.debug-kv { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 6px; align-items: start; }
.debug-kv span { color: var(--muted); }
.debug-kv code, .debug-token-row code, .debug-neighbor-row code { color: var(--text); white-space: pre-wrap; word-break: break-word; }
.debug-nested { margin-top: 8px; }
.debug-nested pre { white-space: pre-wrap; word-break: break-word; max-height: 180px; overflow: auto; color: var(--text); background: rgba(0,0,0,0.18); border-radius: 6px; padding: 8px; }
.debug-empty { margin-top: 8px; color: var(--muted); }
.debug-neighbor-list { display: grid; gap: 6px; margin-top: 8px; }
.debug-neighbor-row { border: 1px solid rgba(139,148,158,0.16); border-radius: 8px; padding: 8px; background: rgba(255,255,255,0.025); }
.debug-neighbor-row.current { border-color: rgba(88,166,255,0.45); background: rgba(88,166,255,0.08); }
.debug-neighbor-row div { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 4px; }
.debug-neighbor-row div span, .debug-neighbor-row div strong { color: var(--muted); }
.debug-neighbor-row.current div strong { color: var(--accent); }
.debug-token-list { display: grid; gap: 8px; margin-top: 8px; max-height: 420px; overflow: auto; padding-right: 2px; }
.debug-token-row { border: 1px solid rgba(139,148,158,0.16); border-radius: 8px; padding: 8px; background: rgba(255,255,255,0.025); }
.debug-token-main { display: flex; gap: 6px; flex-wrap: wrap; align-items: baseline; margin-bottom: 6px; }
.debug-token-main strong { color: var(--text); font-size: 13px; }
.debug-token-main span { color: var(--muted); }
.debug-token-index { color: var(--accent) !important; font-weight: 700; }
.debug-token-meta { display: flex; flex-wrap: wrap; gap: 4px; }
.debug-token-meta span { border: 1px solid rgba(139,148,158,0.14); border-radius: 999px; padding: 2px 6px; color: var(--muted); background: rgba(255,255,255,0.025); }
.known-from-anki-btn { opacity: 0.72; cursor: default; color: var(--success); }
.non-learning-word-btn { opacity: 0.62; cursor: default; color: var(--muted); }

/* Debug UX v6 streamlined dashboard */
.debug-summary-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; margin-top: 8px; }
.debug-mini-card { border: 1px solid rgba(139,148,158,0.16); border-radius: 8px; padding: 7px; background: rgba(255,255,255,0.025); min-width: 0; }
.debug-mini-card span { display: block; color: var(--muted); font-size: 10px; margin-bottom: 3px; }
.debug-mini-card strong { display: block; color: var(--text); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.debug-result-card { border: 1px solid rgba(139,148,158,0.16); border-radius: 8px; padding: 8px; background: rgba(255,255,255,0.025); margin-top: 8px; }
.debug-result-title { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.debug-result-title strong { color: var(--text); font-size: 13px; }
.debug-result-title span { color: var(--muted); }
.debug-result-definition { color: var(--text); margin-top: 6px; line-height: 1.45; max-height: 64px; overflow: auto; }
.dictionary-import-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.dictionary-import-label { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; padding: 6px 10px; border-radius: 8px; }
.dictionary-import-label input { display: none; }

````

### `novel-audio-miner/STABILIZATION.md`

- Purpose: Documentation.
- Size: 6098 bytes
- SHA-256: `ef777bad9beecff78e8c47c4533c2eb77e655834a88609415996988b15297ef7`

````markdown
# Stabilization Log

## Current stable baseline

The current stable baseline is the working v4.1 source after Cleanup Patches 1-20.

The purpose of this baseline is to keep the app clean, formalized, efficient, and ready for Debug Mode without carrying unused experimental code.

## Stable runtime capabilities

- Local Japanese EPUB loading.
- Sentence/image reader stream.
- Vertical and horizontal reading modes.
- Furigana ON/OFF rendering.
- Stable word coloring in furigana and non-furigana modes.
- Frequency-based unknown word coloring.
- Proper noun/name separation.
- Grammar/function-token exclusion.
- Numeric/counter expression grouping.
- Anki-derived known-word cache.
- Persistent manual-known word database.
- Manual Mark Known.
- Undo Known.
- Known count from Anki-known plus manual-known union.
- Latest Kiku note update through AnkiConnect.
- Nadeshiko enrichment.
- VOICEVOX fallback / forced TTS support.

## Completed stabilization steps

### Step 1.1 - Rendering/colorization stabilization

Status: passed.

Confirmed behavior:

- Furigana ON/OFF coloring works.
- Plain text coloring works.
- Existing reader navigation remains functional.

### Step 2A - Token categories

Status: passed.

Confirmed behavior:

- Proper nouns/names are separated.
- Names are excluded from comprehension.
- Names are excluded from New Words.
- Grammar and particles are excluded from New Words.

### Step 2A.1 - Numeric/counter merge

Status: passed.

Confirmed behavior:

- `二十歳` is grouped.
- `二人` is grouped.
- Similar number/counter expressions are treated as numeric.

### Step 2B - Manual Mark as Known

Status: passed.

Confirmed behavior:

- New Words can be marked known.
- Selected words can be marked known.
- The known state updates in the reader.

### Step 2B.1 / Step 2B.3 - Persistent manual-known database and undo

Status: passed.

Confirmed behavior:

- Manual-known words persist after reload.
- Manual-known words remain after Anki cache rebuild.
- Undo Known works.
- Surface/dictionary-form mismatch is handled better.

### Step 2C - Broad compound handling

Status: deferred.

Reason:

Broad compound merging caused unstable behavior and requires Token Inspector / Debug Mode before continuing.

## Cleanup patches applied

### Cleanup Patch 1

Status: passed.

Changes:

- Removed deferred composite-known runtime leftovers.
- Removed unused `isFrequencyMapLoaded` import from `Reader.jsx`.
- Removed unused `getContentWords` import from `epubParser.js`.
- Removed unused composite-known CSS.

### Cleanup Patch 2

Status: passed.

Changes:

- Simplified `tokenizer.js` responsibility.
- Removed old unused `getContentWords()` filtering logic.
- Removed unused parser helpers.

### Cleanup Patch 3

Status: documentation/formalization.

Changes:

- Updated `README.md`.
- Added `WORD_MODEL_POLICY.md`.
- Added/updated `STABILIZATION.md`.

### Cleanup Patch 4

Status: code cleanup.

Changes:

- Removed unused helper exports from Anki, enrichment, and frequency modules.

### Cleanup Patch 5

Status: word-cache cleanup.

Changes:

- Formalized known-word storage.
- Removed noisy normal-operation logs.
- Removed unused manual-known debug exports.

### Cleanup Patch 6

Status: word-model cleanup.

Changes:

- Formalized `wordModel.js` responsibility.
- Removed unused debug merge export.

### Cleanup Patch 7

Status: sentence-splitter cleanup.

Changes:

- Formalized `japaneseSentenceSplitter.js`.
- Removed unused `flattenBookSentences()`.
- Marked `readingUnitGrouper.js` as removable dead/deferred code.

### Cleanup Patch 8

Status: storage cleanup.

Changes:

- Formalized `storage.js`.
- Added safe key helper and missing-id guard.

### Cleanup Patch 9

Status: upload UI cleanup.

Changes:

- Formalized `FileLoader.jsx`.
- Removed outdated upload text and special arrow symbols.

### Cleanup Patch 10

Status: app shell cleanup.

Changes:

- Formalized `App.jsx`.
- Removed temporary `window.__book` debug exposure.
- Added state-based load-another-book callback.

### Cleanup Patch 11

Status: reader cleanup.

Changes:

- Replaced hard page reload with App-controlled book reset.

### Cleanup Patch 12

Status: stylesheet cleanup.

Changes:

- Removed unused/no-op CSS blocks.

### Cleanup Patch 13

Status: app entry cleanup.

Changes:

- Formalized `index.html` and `src/main.jsx`.

### Cleanup Patch 14

Status: Vite config cleanup.

Changes:

- Formalized server/proxy config with named constants.

### Cleanup Patch 15

Status: package metadata cleanup.

Changes:

- Set app version to `4.1.0`.
- Replaced `latest` dependency ranges with exact lockfile versions.

### Cleanup Patch 16

Status: frequency-map cleanup.

Changes:

- Formalized frequency-map responsibility.
- Split frequency loading/combining into named helpers.
- Removed normal-operation logs.

### Cleanup Patch 17

Status: enrichment-service cleanup.

Changes:

- Formalized Nadeshiko/VOICEVOX enrichment service.
- Added named constants and clearer VOICEVOX formatting.

### Cleanup Patch 18

Status: AnkiConnect cleanup.

Changes:

- Formalized AnkiConnect client.
- Added named version constant and note-query escaping helper.

### Cleanup Patch 19

Status: EPUB parser cleanup.

Changes:

- Formalized parser responsibility.
- Removed normal parser logs and misleading generated comment.

### Cleanup Patch 20

Status: tokenizer final cleanup.

Changes:

- Removed normal tokenizer-loaded log.
- Added centralized fallback token helper.

## Deferred until Debug Mode

The following are intentionally deferred until Token Inspector / Debug Mode exists:

- Broad compound-word merging.
- Composite-known judgment based on component words.
- Click-to-select token spans.
- Sentence grouping rewrite.
- EPUB parser/image-order diagnostics.
- Full debug report export.

## Next recommended phase

Phase 3A: Token Inspector / Debug Mode foundation.

Recommended first inspector fields:

- surface
- dictionary form
- POS
- POS details
- token category
- color role
- known state
- manual-known state
- frequency category
- comprehension inclusion
- New Words inclusion
````

### `novel-audio-miner/vite.config.js`

- Purpose: JavaScript/React source.
- Size: 951 bytes
- SHA-256: `b5e57218b58ac8d806da358443a5abfc5618444a59a3fcac593427fcb9024354`

````javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const HOST = '127.0.0.1';
const PORT = 5173;

const PROXY_TARGETS = {
  nadeshiko: 'https://nadeshiko.co',
  voicevox: 'http://localhost:50021',
  jpAnalyzer: 'http://127.0.0.1:8766'
};

function stripProxyPrefix(prefix) {
  return (path) => path.replace(prefix, '');
}

export default defineConfig({
  plugins: [react()],
  server: {
    host: HOST,
    port: PORT,
    proxy: {
      '/api/nadeshiko': {
        target: PROXY_TARGETS.nadeshiko,
        changeOrigin: true,
        rewrite: stripProxyPrefix(/^\/api\/nadeshiko/)
      },
      '/api/voicevox': {
        target: PROXY_TARGETS.voicevox,
        changeOrigin: true,
        rewrite: stripProxyPrefix(/^\/api\/voicevox/)
      },
      '/api/jp-analyzer': {
        target: PROXY_TARGETS.jpAnalyzer,
        changeOrigin: true,
        rewrite: stripProxyPrefix(/^\/api\/jp-analyzer/)
      }
    }
  }
});
````

### `novel-audio-miner/WORD_MODEL_POLICY.md`

- Purpose: Documentation.
- Size: 2326 bytes
- SHA-256: `52994df2185c936160789643f0887cbad5fc19e03e86c330872e81aa4a80bec5`

````markdown
# Word Model Policy

## Principle

Color broadly. Measure comprehension fairly. Mine selectively. Allow user override.

## Known-word definition

A word is known if the word exists in either:

1. the Anki-derived known-word cache, or
2. the persistent manual-known word database.

Known words are colored green and count as understood.

## Manual-known words

Manual-known words are separate from the Anki cache.

Rules:

- Rebuilding the Anki cache does not remove manual-known words.
- Clearing the Anki cache does not remove manual-known words.
- Undo Known removes only the manual-known entry.
- If a word also exists in Anki, Undo Known does not make the word unknown.

## Proper nouns and names

Proper nouns are displayed separately from normal learning words.

Examples:

- character names
- place names
- organization names

Behavior:

- color role: `name`
- comprehension: excluded
- New Words: excluded
- mining candidates: excluded

## Grammar and function tokens

Grammar/function tokens are excluded from learning calculations.

Examples:

- particles
- auxiliaries
- symbols
- suffix-like grammar tokens
- other ignored function tokens

Behavior:

- color role: `grammar`
- comprehension: excluded
- New Words: excluded
- mining candidates: excluded

## Numeric/counter expressions

Common numeric/counter expressions are grouped when Kuromoji splits them into adjacent parts.

Examples:

```text
二十 + 歳 -> 二十歳
二 + 人  -> 二人
三 + 日  -> 三日
```

Behavior:

- color role: `numeric`
- comprehension: excluded
- New Words: excluded
- mining candidates: excluded

## Learning words

Learning words are meaningful vocabulary candidates.

Behavior:

- Known words: green.
- Unknown words: colored by frequency when available.
- Comprehension: included.
- New Words: included when unknown.
- Mining candidates: included when unknown.

## Deferred compound handling

Broad compound handling is intentionally disabled/deferred until Token Inspector / Debug Mode exists.

Deferred examples:

```text
交通事故
響き渡る
現実的
精一杯
一瞬間
```

Reason:

Compound merging without diagnostics caused misclassification and over-merging. Future compound handling should be diagnostics-driven and should prefer explicit evidence from dictionaries, known-word data, or token inspection.
````


## 5. Key Architecture & Design Decisions

### Non-destructive layered analyzer

JP Analyzer uses a non-destructive evidence pipeline: morphology → protected orthography/names → predicates and structural evidence → grammar/dictionary/KWJA evidence → normalized resolver candidates → exclusive compatibility partition → reader-candidate generation → candidate-specific dictionary and structural evaluation → conservative selection/abstention → exact corrections → compact consumer contract. Earlier evidence is preserved; later layers evaluate and select rather than silently rewriting earlier facts.

The decider must explain each selection. Dictionary evidence is evidence-only, and a dictionary miss is not rejection. Generated compound evidence must be specific to the generated candidate; component evidence is not proof of the complete compound. When evidence is insufficient, the resolver abstains and preserves a safe compatibility/neutral partition.

### Tool roles

- **Sudachi/SudachiPy:** Japanese morphology and normalization support inside the analyzer stack.
- **GiNZA/spaCy:** primary morphology, POS, dependency, entity, predicate, and sentence-structure analysis.
- **KWJA:** read-only phrase/predicate/relationship evidence. It proposes or corroborates evidence but does not overwrite morphology or force reader output.
- **Kuromoji:** retired. It is no longer a dependency or production linguistic source.
- **Yomitan:** external dictionary and user-facing lookup/mining workflow.
- **AnkiConnect:** note lookup/update and media storage for mining.
- **Nadeshiko / VoiceVox:** enrichment and audio fallback services owned by the app, not the linguistic analyzer.

### Consumer contract and renderer

Novel Audio Miner validates exact analyzer source text and authoritative `readerSpans`. It preserves integer offsets, surfaces, display roles, lookup keys, grammar/correction metadata, and eligibility flags. Rendering uses exact offsets over plain text or visible XHTML text nodes while preserving ruby `rt/rp` exclusion and selectable Japanese text. There is no frontend boundary reconstruction or surface search for analyzer spans.

### Data flow

```text
EPUB upload
  -> parse package/spine/chapters/pages
  -> preserve plain text, ruby HTML, images and parser provenance
  -> select active sentence
  -> POST exact sentence to JP Analyzer /analyze
  -> validate versioned readerSpans contract
  -> resolve known state with knownLookupKey
  -> resolve frequency with frequencyLookupKey
  -> apply analyzer presentation policy to exact ranges
  -> compute comprehension and New Words from analyzer flags
  -> map exact selection to one analyzer span
  -> allow mark-known or offset-aware Anki mining when eligible
  -> export schema-v2 diagnostic report when requested
```

### Cache and corrections

Cache identity includes the exact sentence plus analyzer version, reader span schema, and correction revision. A short metadata lease allows prefetched results to activate quickly while still detecting analyzer/correction changes. Corrections are occurrence-scoped SQLite records with preview/save/list/deactivate APIs and are applied after conservative reader selection.

### Dictionary architecture

Frontend dictionaries are stored in IndexedDB as chunked minimized entries and synchronized in batches to the analyzer SQLite lexicon. The analyzer uses staging tables and a live lexicon table, exposes status and evidence endpoints, and reports readiness/counts in health. Phase 7 should make this lifecycle safer and clearer without shifting Yomitan ownership.

## 6. Known Bugs, Limitations & Test Results

### Verified tests and build

- **JP Analyzer consolidated suite:** passed, exit code 0. It covers correction revision, resolver decisions, dictionary adapter/evidence/path, engine/evidence routing, facade, health/import boundaries, KWJA adapter/timeout, reader candidates, corrections, lookup hypotheses, numeric terms, reader projection, runtime contracts/reuse, semantic snapshots, and single-pass execution.
- **Novel Audio Miner production build:** passed with Vite 8.1.3; 37 modules transformed; generated JS bundle 362.93 kB (112.41 kB gzip).
- **Snapshot regression:** not executed correctly because required `input_file` and `--reference` arguments were omitted. This must not be recorded as a product test failure.
- **Novel Audio Miner dedicated tests:** present as `test:reader-spans`, `test:color-sources`, `test:phase3`, `test:phase4`, `test:phase5-shadow`, `test:phase5`, and individual cache/prefetch/metadata/presentation/learning/mining/selection/retirement/debug-report tests. The collector only looked for a generic `test` script, so these were not executed in the captured run.

### Observed runtime validation

- Analyzer health returned HTTP 200 and `status: ok`.
- KWJA was available.
- Dictionary status returned ready with persistent counts and last sync ID.
- Two debug reports validated complete reader contracts, exact source reconstruction, zero unresolved spans in sampled scenes, analyzer-owned presentation/learning, correction-aware caches, adjacent prefetch, and full EPUB parser inventory when requested.
- The “Include all EPUB parser data” checkbox is confirmed working; empty reader selection in those reports was unrelated and is not a bug.

### Limitations requiring future work

- Exact teaching supports occurrence scope; global generalization remains deliberately offline and validation-gated.
- Full teaching UI is not yet implemented.
- Phase 7 sync integrity and restart behavior need dedicated automated tests even though persistence is currently confirmed.
- OpenAPI lacks typed response schemas for several routes.
- The large authentic-novel corpus supports future ranker tuning; existing 200-sentence corpora prove stability, not complete linguistic accuracy.
- Runtime performance needs explicit cold/warm/prefetch thresholds; the local untracked timing utility may help if formalized.

## 7. Dependencies & Environment

### Current runtimes

- Python: `3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)]`
- Node.js: `v24.18.0`
- npm: `12.0.1`
- Git: `git version 2.55.0.windows.2`
- Windows PowerShell: `5.1.22621.6133`
- OS: `Windows-10-10.0.22631-SP0`

### Python dependencies

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

### KWJA environment dependencies

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

### Frontend dependencies

- `@vitejs/plugin-react==6.0.3`
- `jszip==3.10.1`
- `react==19.2.7`
- `react-dom==19.2.7`
- `vite==8.1.3`

### External/local services

- JP Analyzer FastAPI/Uvicorn service: `http://127.0.0.1:8766`
- KWJA executable: `D:\Mining\KWJA evaluator\.venv\Scripts\kwja.exe`
- AnkiConnect for note and media operations
- Yomitan browser extension for dictionary workflow
- VoiceVox local service where configured
- Nadeshiko session/enrichment integration where configured
- Browser IndexedDB for frontend dictionary snapshots
- SQLite for analyzer lexicon and reader corrections

### Development setup

```powershell
# JP Analyzer
Set-Location "D:\Mining\JP analyzer"
$env:PYTHONPATH = "D:\Mining\JP analyzer"
$env:KWJA_EXE = "D:\Mining\KWJA evaluator\.venv\Scripts\kwja.exe"
$env:HF_HUB_OFFLINE = "1"
$env:TRANSFORMERS_OFFLINE = "1"
$env:HF_DATASETS_OFFLINE = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
& ".\.venv\Scripts\python.exe" -m uvicorn app.analyzer.service:app --host 127.0.0.1 --port 8766

# In another terminal: Novel Audio Miner
Set-Location "D:\Mining\novel-audio-miner"
npm ci
npm run dev
```

Run current tests/build:

```powershell
Set-Location "D:\Mining\JP analyzer"
& ".\run_tests.ps1"

Set-Location "D:\Mining\novel-audio-miner"
npm run test:phase5
npm run build
```

## 8. Exact Resume Instructions

Resume from **Phase 7 — Dictionary management**. Do not redo Phases 1–6 and do not reintroduce Kuromoji; it was retired in Phase 5.2E. Treat JP Analyzer `main` at `0b00fbd5ae1bdb1106a5c16199f3c9b862315fdf` and Novel Audio Miner `feature/jp-analyzer-integration` at `2d2569771cb44ba28f794a82e4e047adfc7051ac` as the current committed baselines. First run the analyzer suite, `npm run test:phase5`, and the frontend build. Then audit the existing persistent dictionary status, sync panel, IndexedDB storage, batch client, and SQLite staging/live schema. Improve Phase 7 through small commits focused on settings-driven status, safe/atomic sync, avoiding redundant resync, cancellation/retry/recovery, clear diagnostics, and automated persistence tests. Preserve the core invariants: analyzer-owned exact spans and identities, no frontend reclassification or surface fallback, dictionary miss is not rejection, ambiguity yields neutral output, exact corrections are correction-revision aware, and Yomitan remains the user-facing dictionary owner. Ask the user for any runtime-only data or expected UX behavior that is not represented in this snapshot rather than inventing it.

### Canonical update and Git procedure

After downloading this generated file, replace and commit it with:

```powershell
$Source = "D:\Downloads\PROJECT_SNAPSHOT_CURRENT.md"  # adjust to actual download location
$Target = "D:\Mining\JP analyzer\docs\PROJECT_SNAPSHOT_CURRENT.md"

Copy-Item -LiteralPath $Source -Destination $Target -Force

Set-Location "D:\Mining\JP analyzer"
git diff --check
git diff -- docs/PROJECT_SNAPSHOT_CURRENT.md
git add -- docs/PROJECT_SNAPSHOT_CURRENT.md
git commit -m "Update current Japanese novel mining project snapshot"
git status --short
```

Push only after reviewing the diff:

```powershell
Set-Location "D:\Mining\JP analyzer"
git push origin main
```
