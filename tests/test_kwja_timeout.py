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
