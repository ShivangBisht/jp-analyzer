from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_BRANCH = "consolidation/single-layered-analyzer"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        print(f"Removed directory: {path.relative_to(ROOT)}")
    elif path.exists():
        path.unlink()
        print(f"Removed file: {path.relative_to(ROOT)}")


def replace(path: Path, old: str, new: str, *, required: bool = False) -> None:
    if not path.exists():
        if required:
            raise RuntimeError(f"Required file is missing: {path}")
        return
    text = path.read_text(encoding="utf-8-sig")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
        print(f"Updated: {path.relative_to(ROOT)}")
    elif required and new not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Wrote: {path.relative_to(ROOT)}")


def move_test(source_name: str, target_name: str) -> None:
    source = ROOT / source_name
    target = ROOT / "tests" / target_name
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.unlink()
        shutil.move(str(source), str(target))
        print(f"Moved: {source_name} -> tests/{target_name}")


def main() -> None:
    branch = git("branch", "--show-current").stdout.strip()
    require(
        branch == EXPECTED_BRANCH,
        f"Expected branch {EXPECTED_BRANCH!r}, found {branch!r}.",
    )
    status = git("status", "--porcelain").stdout.strip()
    require(
        not status,
        "Working tree must be clean before final cleanup. Commit and push the "
        "400/400 validated checkpoint first.\n" + status,
    )
    require((ROOT / "app/analyzer/layers/evidence_gate.py").is_file(),
            "Consolidated analyzer layers are missing.")
    require((ROOT / "app/phase8").is_dir() and (ROOT / "app/phase9").is_dir(),
            "Legacy phase packages are already absent or incomplete.")

    # Production naming: one analyzer function, one engine contract, no legacy seam.
    engine = ROOT / "app/analyzer/engine.py"
    replace(engine, "LegacyEngine = Callable", "AnalyzerFunction = Callable")
    replace(engine, "legacy_engine: LegacyEngine", "analyzer_fn: AnalyzerFunction")
    replace(engine, "legacy_engine: AnalyzerFunction", "analyzer_fn: AnalyzerFunction")
    replace(engine, "self.legacy_engine = legacy_engine or analyze_layers",
            "self.analyzer_fn = analyzer_fn or analyze_layers", required=True)
    replace(engine, "signature(self.legacy_engine)", "signature(self.analyzer_fn)")
    replace(engine, "result = self.legacy_engine(", "result = self.analyzer_fn(")
    replace(engine, "LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")
    replace(engine, "Expected legacy engine", "Expected engine contract")

    pipeline = ROOT / "app/analyzer/pipeline.py"
    replace(pipeline, "LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")
    replace(pipeline, "Expected legacy engine", "Expected engine contract")
    replace(pipeline, "legacy_engine=analyze_integrated_alpha2",
            "analyzer_fn=analyze_layers")
    replace(pipeline, "legacy_engine=analyze_layers", "analyzer_fn=analyze_layers")
    # Remove the temporary facade alias and its explanatory comment.
    text = pipeline.read_text(encoding="utf-8-sig")
    text = text.replace(
        "\n# Temporary compatibility alias for the established facade test and callers\n"
        "# that patch this module-level seam. Production still resolves to the\n"
        "# consolidated layer engine.\n"
        "analyze_integrated_alpha2 = analyze_layers\n",
        "",
    )
    text = text.replace(
        "# Pass the module-level alias deliberately. Existing façade tests can replace\n"
        "# it with a sentinel, while production still routes through AnalyzerEngine.\n",
        "# The public facade routes through the single consolidated analyzer function.\n",
    )
    pipeline.write_text(text, encoding="utf-8", newline="\n")
    print("Updated: app/analyzer/pipeline.py")

    version = ROOT / "app/analyzer/version.py"
    replace(version, "LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")
    health = ROOT / "app/analyzer/health.py"
    replace(health, "LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")
    service = ROOT / "app/analyzer/service.py"
    replace(service, "LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")

    # Tests become stable responsibility tests instead of phase-number tests.
    write(ROOT / "tests/__init__.py", "")
    test_moves = {
        "test_phase10_kwja_adapter.py": "test_kwja_adapter.py",
        "test_phase10_dictionary_adapter.py": "test_dictionary_adapter.py",
        "test_phase10_evidence_routing.py": "test_evidence_routing.py",
        "test_phase10_runtime_reuse.py": "test_runtime_reuse.py",
        "test_phase10_health_contract.py": "test_health_contract.py",
        "test_phase10_semantic_snapshot.py": "test_semantic_snapshot.py",
        "test_phase10_runtime_contracts.py": "test_runtime_contracts.py",
        "test_phase10_facade.py": "test_facade.py",
        "test_phase10_engine_routing.py": "test_engine_routing.py",
        "test_consolidated_import_boundary.py": "test_import_boundary.py",
        "test_consolidated_single_pass.py": "test_single_pass.py",
        "test_consolidated_dictionary_path.py": "test_dictionary_path.py",
        "test_consolidated_kwja_timeout.py": "test_kwja_timeout.py",
        "test_dictionary_evidence.py": "test_dictionary_evidence.py",
        "test_resolver_alpha34.py": "test_decision.py",
    }
    for old, new in test_moves.items():
        move_test(old, new)

    for path in (ROOT / "tests").glob("test_*.py"):
        text = path.read_text(encoding="utf-8-sig")
        text = text.replace("app.phase8.dictionary_evidence", "app.analyzer.layers.dictionary")
        text = text.replace("app.phase8.resolver_alpha34", "app.analyzer.layers.decision")
        text = text.replace("LEGACY_ENGINE_VERSION", "ENGINE_CONTRACT_VERSION")
        text = text.replace("legacy_engine=", "analyzer_fn=")
        text = text.replace("pipeline.analyze_integrated_alpha2", "pipeline.analyze_layers")
        text = text.replace("Phase 10.4 ", "")
        text = text.replace("Phase 10.3 ", "")
        text = text.replace("Phase 10.2 ", "")
        text = text.replace("Phase 10.1 ", "")
        path.write_text(text, encoding="utf-8", newline="\n")

    # The timeout test now validates only the current analyzer.
    timeout_test = ROOT / "tests/test_kwja_timeout.py"
    if timeout_test.exists():
        write(timeout_test, '''import inspect\n\nfrom app.analyzer.layers.kwja import run_kwja\n\n\ndef main():\n    timeout = inspect.signature(run_kwja).parameters["timeout_seconds"].default\n    assert timeout == 300, timeout\n    print("KWJA timeout test passed")\n\n\nif __name__ == "__main__":\n    main()\n''')

    # Facade test patches the current layer seam, not a historical alias.
    facade_test = ROOT / "tests/test_facade.py"
    if facade_test.exists():
        replace(facade_test, "pipeline.analyze_integrated_alpha2", "pipeline.analyze_layers")

    # Current-only snapshot regression runner. It never imports legacy code.
    write(ROOT / "run_snapshot_regression.py", '''from __future__ import annotations\n\nimport argparse\nimport json\nimport time\nfrom pathlib import Path\n\nfrom app.analyzer.pipeline import analyze_full\nfrom app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest\n\n\ndef read_sentences(path: Path) -> list[str]:\n    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]\n\n\ndef write_json(path: Path | None, value) -> None:\n    if path is not None:\n        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser()\n    parser.add_argument("input_file", type=Path)\n    parser.add_argument("--reference", type=Path, required=True)\n    parser.add_argument("--output", type=Path)\n    parser.add_argument("--report", type=Path, default=Path("snapshot_regression_report.json"))\n    parser.add_argument("--resume", action="store_true")\n    parser.add_argument("--retries", type=int, default=1)\n    args = parser.parse_args()\n\n    sentences = read_sentences(args.input_file)\n    references = json.loads(args.reference.read_text(encoding="utf-8-sig"))\n    if len(references) != len(sentences):\n        raise RuntimeError("Reference count mismatch")\n\n    actuals = []\n    if args.resume and args.output and args.output.exists():\n        actuals = json.loads(args.output.read_text(encoding="utf-8-sig"))\n        print(f"Resuming after {len(actuals)} sentence(s).")\n\n    mismatches = []\n    timings = []\n    for index in range(len(actuals), len(sentences)):\n        sentence_id = f"S{index + 1:04d}"\n        started = time.perf_counter()\n        last_error = None\n        for attempt in range(args.retries + 1):\n            try:\n                actual = semantic_snapshot(analyze_full(sentences[index]))\n                last_error = None\n                break\n            except Exception as error:\n                last_error = error\n                print(f"{sentence_id} attempt={attempt + 1} ERROR {type(error).__name__}: {error}")\n        if last_error is not None:\n            raise last_error\n        elapsed = (time.perf_counter() - started) * 1000\n        timings.append(elapsed)\n        actuals.append(actual)\n        write_json(args.output, actuals)\n        expected = references[index]\n        passed = actual == expected\n        if not passed:\n            mismatches.append({\n                "sentenceId": sentence_id,\n                "expectedDigest": snapshot_digest(expected),\n                "actualDigest": snapshot_digest(actual),\n                "text": sentences[index],\n            })\n        report = {\n            "sentences": len(sentences),\n            "completed": len(actuals),\n            "passed": len(actuals) - len(mismatches),\n            "failed": len(mismatches),\n            "semanticParity": len(actuals) == len(sentences) and not mismatches,\n            "meanRuntimeMs": sum(timings) / len(timings) if timings else None,\n            "mismatches": mismatches,\n        }\n        write_json(args.report, report)\n        print(f"{sentence_id} {'PASS' if passed else 'FAIL'} elapsed_ms={elapsed:.2f} checkpoint={len(actuals)}/{len(sentences)}")\n\n    raise SystemExit(0 if not mismatches else 1)\n\n\nif __name__ == "__main__":\n    main()\n''')

    # Integrate KWJA environment ownership into the analyzer repository.
    kwja_requirements = ROOT / "requirements-kwja-py311.txt"
    if not kwja_requirements.exists():
        write(kwja_requirements, '''kwja==2.5.1\npure-cdb==4.0.0\ntorch==2.7.1\ntransformers==4.50.3\ntokenizers==0.21.4\nsafetensors==0.8.0\nsentencepiece==0.2.1\nprotobuf==7.35.1\n''')
    write(ROOT / "scripts/setup_kwja_windows.ps1", '''$ErrorActionPreference = "Stop"\nSet-Location (Split-Path -Parent $PSScriptRoot)\npy -3.11 -m venv .kwja-venv\n$Python = ".\\.kwja-venv\\Scripts\\python.exe"\n& $Python -m pip install --upgrade pip wheel\n$env:ENABLE_DJB_HASH_CEXT = "0"\n$env:SETUPTOOLS_USE_DISTUTILS = "stdlib"\n& $Python -m pip install --no-build-isolation --no-binary pure-cdb "pure-cdb==4.0.0"\n& $Python -m pip install -r ".\\requirements-kwja-py311.txt"\nWrite-Host "KWJA executable: $PWD\\.kwja-venv\\Scripts\\kwja.exe" -ForegroundColor Green\n''')
    write(ROOT / "docs/KWJA_SETUP_WINDOWS.md", '''# KWJA setup on Windows\n\nKWJA is an internal analyzer layer. Its heavy Python 3.11 environment is isolated in `.kwja-venv`; it is not a separate application or repository.\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\scripts\\setup_kwja_windows.ps1\n$env:KWJA_EXE = "$PWD\\.kwja-venv\\Scripts\\kwja.exe"\n```\n\nNever disable TLS certificate verification. The pure-Python `pure-cdb` installation avoids requiring Microsoft C++ Build Tools.\n''')

    # Stable test runner.
    write(ROOT / "run_tests.ps1", '''$ErrorActionPreference = "Stop"\nSet-Location $PSScriptRoot\n$Python = ".\\.venv\\Scripts\\python.exe"\nif (-not (Test-Path $Python)) { throw "Python not found: $Python" }\n$Tests = Get-ChildItem ".\\tests\\test_*.py" | Sort-Object Name\nforeach ($Test in $Tests) {\n    Write-Host "Running $($Test.Name)" -ForegroundColor Cyan\n    & $Python $Test.FullName\n    if ($LASTEXITCODE -ne 0) { throw "Test failed: $($Test.Name)" }\n}\n& $Python -m compileall -q ".\\app\\analyzer"\nif ($LASTEXITCODE -ne 0) { throw "Analyzer compilation failed" }\nWrite-Host "All consolidated analyzer tests passed." -ForegroundColor Green\n''')

    write(ROOT / "CONSOLIDATED_ANALYZER.md", '''# Consolidated JP Analyzer\n\nThe supported production implementation is `app.analyzer.analyze`. The analyzer owns morphology, protected ranges, structure, candidates, dictionary evidence, KWJA evidence, evidence gating, the final decision, diagnostics, and compact/full output.\n\nHistorical Phase 8, Phase 9, and Phase 10 wrapper implementations were removed after exact semantic parity on 200 development and 200 fresh unseen sentences. Existing phase-named debug fields remain temporarily for response-schema compatibility; they are not separate runtime implementations.\n\n## Run tests\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\run_tests.ps1\n```\n\n## Run frozen snapshot regression\n\n```powershell\n& .\\.venv\\Scripts\\python.exe .\\run_snapshot_regression.py .\\random_sentences.txt --reference .\\consolidation_dev_reference_200.json --output .\\post_cleanup_dev_actual.json --report .\\post_cleanup_dev_report.json\n```\n''')

    # Remove legacy implementation and compatibility-only modules.
    remove(ROOT / "app/phase8")
    remove(ROOT / "app/phase9")
    remove(ROOT / "app/analyzer/legacy_reference.py")
    remove(ROOT / "app/analyzer/dictionary_runtime.py")
    remove(ROOT / "run_consolidated_parity.py")

    # Delete phase tests/runners, generated snapshots, migrations and backups.
    obsolete_exact = [
        "README_PHASE10.md", "README_PHASE10_2.md", "README_PHASE10_3.md", "README_PHASE10_4.md",
        "apply_phase10_2_infrastructure.py", "apply_phase10_3_routing.py",
        "apply_phase10_4_evidence_routing.py", "fix_phase10_4_signature_import.py",
        "run_phase10_parity.py", "run_phase10_snapshot_parity.py",
        "run_phase9_alpha111_s0198.py", "run_phase9_alpha21_corpus.py", "run_phase9_alpha2_focused.py",
        "test_phase9_alpha22.py", "01_apply_consolidated_analyzer.py",
        "02_run_fast_consolidation_tests.ps1", "03_CONSOLIDATION_CHECKPOINT.md",
        "04_fix_facade_compatibility.py", "05_fix_consolidated_dictionary_path.py",
        "06_harden_corpus_parity_runner.py", "06a_fix_hardening_patch_signature.py",
        "build_consolidation_package.py", "jp_analyzer_current_inventory.txt", "-LiteralPath",
        "phase10_3_api_check.json", "phase10_parity_mismatches.json", "phase10_parity_summary.json",
        "phase10_reference_development20.json", "phase10_snapshot_mismatches.json",
        "phase10_snapshot_summary.json", "phase9_alpha111_s0198_result.json",
        "phase9_alpha2_focused_results.json",
    ]
    for relative in obsolete_exact:
        remove(ROOT / relative)
    remove(ROOT / "frozen_phase9_alpha22")

    for path in (ROOT / "app/analyzer").rglob("*.bak"):
        remove(path)
    for path in ROOT.rglob("__pycache__"):
        remove(path)

    # Preserve a committed single-case snapshot as a neutral fixture if present.
    for candidate in (ROOT / "phase10_semantic_reference_1.json", ROOT / "phase10_speed_reference_1.json"):
        if candidate.exists():
            target = ROOT / "tests/fixtures/single_case_semantic_reference.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                target.unlink()
            shutil.move(str(candidate), str(target))
            print(f"Moved: {candidate.name} -> tests/fixtures/{target.name}")
            break

    # Repository hygiene.
    ignore = ROOT / ".gitignore"
    current = ignore.read_text(encoding="utf-8-sig") if ignore.exists() else ""
    additions = [
        ".kwja-venv/",
        "consolidation_*_reference*.json",
        "consolidation_*_actual*.json",
        "consolidation_*_report*.json",
        "fresh_unseen_*.json",
        "post_cleanup_*.json",
    ]
    for entry in additions:
        if entry not in current.splitlines():
            current += ("" if current.endswith("\n") or not current else "\n") + entry + "\n"
    ignore.write_text(current, encoding="utf-8", newline="\n")

    # Final static checks before returning control to the user.
    offenders = []
    for path in (ROOT / "app/analyzer").rglob("*.py"):
        text = path.read_text(encoding="utf-8-sig")
        if "app.phase8" in text or "app.phase9" in text:
            offenders.append(str(path.relative_to(ROOT)))
    require(not offenders, f"Active phase imports remain: {offenders}")

    print("\nFinal cleanup applied.")
    print("Run: powershell.exe -ExecutionPolicy Bypass -File .\\run_tests.ps1")
    print("Then run both frozen 200-sentence snapshot regressions before committing.")


if __name__ == "__main__":
    main()
