from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_BRANCH = "consolidation/single-layered-analyzer"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Updated: {relative}")


def replace(relative: str, old: str, new: str, *, required: bool = True) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8-sig")
    if old not in text:
        if new in text:
            print(f"Already updated: {relative}")
            return
        if required:
            raise RuntimeError(f"Expected text not found in {relative}: {old!r}")
        return
    write(relative, text.replace(old, new))


def main() -> None:
    branch = git("branch", "--show-current").stdout.strip()
    require(branch == EXPECTED_BRANCH, f"Expected branch {EXPECTED_BRANCH!r}, found {branch!r}")
    status = git("status", "--porcelain").stdout.strip()
    require(not status, "Working tree must be clean before streamlining.\n" + status)

    # Runtime analysis must be deterministic and independent of Hub availability.
    kwja_path = "app/analyzer/layers/kwja.py"
    replace(
        kwja_path,
        '    env = os.environ.copy()\n    env["PYTHONUTF8"] = "1"\n',
        '    env = os.environ.copy()\n'
        '    env["PYTHONUTF8"] = "1"\n'
        '    # Analysis is cache-only by default. Set any variable to "0" explicitly\n'
        '    # when installing or refreshing models in a controlled online session.\n'
        '    env.setdefault("HF_HUB_OFFLINE", "1")\n'
        '    env.setdefault("TRANSFORMERS_OFFLINE", "1")\n'
        '    env.setdefault("HF_DATASETS_OFFLINE", "1")\n',
    )

    # Remove an unused runtime wrapper; all execution is owned by KwjaAdapter -> analyze_kwja.
    runtime_path = ROOT / "app/analyzer/kwja_runtime.py"
    runtime_text = runtime_path.read_text(encoding="utf-8-sig")
    runtime_text = runtime_text.replace(
        "from .layers.kwja import analyze_kwja_alpha1, run_kwja\n",
        "from .layers.kwja import analyze_kwja_alpha1\n",
    )
    unused = '''\ndef run_kwja_base(text, *, executable=None):\n    return run_kwja(text, executable=str(resolve_kwja_executable(executable)), model_size="base")\n'''
    runtime_text = runtime_text.replace(unused, "")
    write("app/analyzer/kwja_runtime.py", runtime_text)

    # Remove unused historical convenience aliases from internal layers.
    alias_files = {
        "app/analyzer/layers/morphology.py": "analyze = analyze_layered",
        "app/analyzer/layers/protected.py": "analyze = analyze_layered_alpha3",
        "app/analyzer/layers/structure.py": "analyze = analyze_layered_alpha31",
        "app/analyzer/layers/candidates.py": "analyze = analyze_layered_alpha32",
        "app/analyzer/layers/stabilization.py": "analyze = analyze_layered_alpha321",
        "app/analyzer/layers/decision.py": "analyze = analyze_layered_alpha34",
        "app/analyzer/layers/kwja.py": "analyze = analyze_kwja_alpha1",
        "app/analyzer/layers/evidence_gate.py": "analyze = analyze_integrated_alpha2",
    }
    for relative, alias in alias_files.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8-sig")
        text = text.replace("\n\n" + alias + "\n", "\n")
        write(relative, text)

    # Remove a local diagnostic artifact that was accidentally included in the archive.
    raw_fixture = ROOT / "s0023_raw.knp"
    if raw_fixture.exists():
        raw_fixture.unlink()
        print("Removed: s0023_raw.knp")

    # Replace stale prototype documentation with the current supported architecture.
    write(
        "README.md",
        '''# JP Analyzer\n\nJP Analyzer is the single supported Japanese linguistic-analysis service in this repository.\n\n## Production entry points\n\n- Python: `app.analyzer.analyze` and `app.analyzer.analyze_full`\n- FastAPI: `app.analyzer.service:app`\n- Health: `GET /health`\n- Analysis: `POST /analyze`\n\nThe implementation is organized under `app/analyzer/layers` and owns morphology, structure, candidate generation, dictionary evidence, KWJA evidence, evidence gating, final resolution, diagnostics, and compact/full output.\n\n## Test suite\n\n```powershell\nSet-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass\n& .\\run_tests.ps1\n```\n\nRegression corpora are versioned under `tests/corpora`. Generated snapshots and reports remain local.\n\n## KWJA runtime\n\nRoutine analysis is cache-only by default and does not contact Hugging Face. Install or refresh the isolated KWJA environment with `scripts/setup_kwja_windows.ps1` during a controlled online session, then set `KWJA_EXE` to that environment's executable. See `docs/KWJA_SETUP_WINDOWS.md`.\n''',
    )

    write(
        "docs/KWJA_SETUP_WINDOWS.md",
        '''# KWJA setup on Windows\n\nKWJA is an internal JP Analyzer layer. Its Python 3.11 environment is isolated in `.kwja-venv`; it is not a separate application or repository.\n\n## Install or refresh models online\n\n```powershell\n$env:HF_HUB_OFFLINE = "0"\n$env:TRANSFORMERS_OFFLINE = "0"\n$env:HF_DATASETS_OFFLINE = "0"\npowershell.exe -ExecutionPolicy Bypass -File .\\scripts\\setup_kwja_windows.ps1\n$env:KWJA_EXE = "$PWD\\.kwja-venv\\Scripts\\kwja.exe"\n```\n\nNever disable TLS certificate verification. The pure-Python `pure-cdb` installation avoids requiring Microsoft C++ Build Tools.\n\n## Routine analysis\n\nThe analyzer's KWJA subprocess defaults to cache-only mode by setting `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_DATASETS_OFFLINE=1` when those variables are absent. This prevents runtime stalls caused by model-metadata requests.\n\nTo deliberately allow Hub access for a controlled refresh, set the variables to `0` before starting the analyzer. Explicit caller values are preserved.\n''',
    )

    # Strengthen the existing KWJA test to verify timeout and offline subprocess policy.
    write(
        "tests/test_kwja_timeout.py",
        '''import inspect\nimport os\nimport tempfile\nfrom pathlib import Path\nfrom unittest.mock import patch\n\nfrom app.analyzer.layers import kwja\n\n\nclass Completed:\n    stdout = b"KNP"\n    stderr = b""\n\n\ndef main():\n    timeout = inspect.signature(kwja.run_kwja).parameters["timeout_seconds"].default\n    assert timeout == 300, timeout\n\n    captured = {}\n\n    def fake_run(*args, **kwargs):\n        captured.update(kwargs)\n        return Completed()\n\n    with tempfile.TemporaryDirectory() as tmp:\n        executable = Path(tmp) / "kwja.exe"\n        executable.write_bytes(b"")\n        with patch.object(kwja.os, "environ", {}), patch.object(kwja.subprocess, "run", fake_run):\n            output, _ = kwja.run_kwja("検証。", executable=str(executable))\n\n    assert output == "KNP"\n    env = captured["env"]\n    assert env["PYTHONUTF8"] == "1"\n    assert env["HF_HUB_OFFLINE"] == "1"\n    assert env["TRANSFORMERS_OFFLINE"] == "1"\n    assert env["HF_DATASETS_OFFLINE"] == "1"\n    assert captured["timeout"] == 300\n\n    explicit = {"HF_HUB_OFFLINE": "0", "TRANSFORMERS_OFFLINE": "0", "HF_DATASETS_OFFLINE": "0"}\n    with tempfile.TemporaryDirectory() as tmp:\n        executable = Path(tmp) / "kwja.exe"\n        executable.write_bytes(b"")\n        captured.clear()\n        with patch.object(kwja.os, "environ", explicit), patch.object(kwja.subprocess, "run", fake_run):\n            kwja.run_kwja("検証。", executable=str(executable))\n    assert captured["env"]["HF_HUB_OFFLINE"] == "0"\n    assert captured["env"]["TRANSFORMERS_OFFLINE"] == "0"\n    assert captured["env"]["HF_DATASETS_OFFLINE"] == "0"\n    print("KWJA runtime policy test passed")\n\n\nif __name__ == "__main__":\n    main()\n''',
    )

    # Ensure local KNP/debug artifacts never return to Git.
    ignore_path = ROOT / ".gitignore"
    ignore = ignore_path.read_text(encoding="utf-8-sig")
    for entry in ("s*.knp", "*_raw.knp"):
        if entry not in ignore.splitlines():
            ignore += ("" if ignore.endswith("\n") else "\n") + entry + "\n"
    write(".gitignore", ignore)

    # Static sanity checks.
    for relative, alias in alias_files.items():
        require(alias not in (ROOT / relative).read_text(encoding="utf-8-sig"), f"Alias remains: {alias}")
    require("def run_kwja_base" not in runtime_path.read_text(encoding="utf-8-sig"), "Unused KWJA wrapper remains")
    print("\nStreamlining patch applied. Run the full test suite and both frozen regressions before committing.")


if __name__ == "__main__":
    main()
