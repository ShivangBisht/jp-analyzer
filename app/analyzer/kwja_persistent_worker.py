from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WorkerResult:
    request_id: str
    output: str
    elapsed_ms: float
    process_id: int


class InteractiveKwjaWorker:
    """Benchmark-only wrapper around KWJA's documented interactive CLI mode."""

    def __init__(self, executable: str, *, model_size: str = "base"):
        self.executable = str(Path(executable))
        self.model_size = model_size
        self.process: subprocess.Popen[str] | None = None
        self._stdout: queue.Queue[str | None] = queue.Queue()
        self._stderr: queue.Queue[str | None] = queue.Queue()
        self._stdout_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None

    def start(self) -> float:
        if self.process is not None and self.process.poll() is None:
            return 0.0
        env = os.environ.copy()
        env.update({
            "PYTHONUTF8": "1",
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_DATASETS_OFFLINE": "1",
        })
        started = time.perf_counter()
        self.process = subprocess.Popen(
            [self.executable, "--model-size", self.model_size],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=env,
        )
        self._stdout_thread = threading.Thread(
            target=self._pump, args=(self.process.stdout, self._stdout), daemon=True
        )
        self._stderr_thread = threading.Thread(
            target=self._pump, args=(self.process.stderr, self._stderr), daemon=True
        )
        self._stdout_thread.start()
        self._stderr_thread.start()
        return (time.perf_counter() - started) * 1000

    @staticmethod
    def _pump(stream, output: queue.Queue[str | None]) -> None:
        try:
            for line in iter(stream.readline, ""):
                output.put(line)
        finally:
            output.put(None)

    def analyze(self, text: str, *, timeout_seconds: float = 180.0) -> WorkerResult:
        if self.process is None or self.process.poll() is not None:
            raise RuntimeError("KWJA worker is not running.")
        if self.process.stdin is None:
            raise RuntimeError("KWJA worker stdin is unavailable.")
        request_id = uuid.uuid4().hex
        while not self._stdout.empty():
            self._stdout.get_nowait()
        started = time.perf_counter()
        self.process.stdin.write(text.rstrip("\n") + "\nEOD\n")
        self.process.stdin.flush()
        lines: list[str] = []
        deadline = time.monotonic() + timeout_seconds
        saw_eos = False
        last_output_at = None
        while time.monotonic() < deadline:
            wait = min(0.25, max(0.01, deadline - time.monotonic()))
            try:
                line = self._stdout.get(timeout=wait)
            except queue.Empty:
                if saw_eos and last_output_at is not None and time.monotonic() - last_output_at >= 0.20:
                    break
                if self.process.poll() is not None:
                    raise RuntimeError("KWJA worker exited before completing the request.")
                continue
            if line is None:
                raise RuntimeError("KWJA worker stdout closed before completing the request.")
            lines.append(line)
            last_output_at = time.monotonic()
            if line.rstrip("\r\n") == "EOS":
                saw_eos = True
        if not saw_eos:
            raise TimeoutError(f"KWJA worker request exceeded {timeout_seconds} seconds.")
        return WorkerResult(
            request_id=request_id,
            output="".join(lines),
            elapsed_ms=(time.perf_counter() - started) * 1000,
            process_id=self.process.pid,
        )

    def diagnostics(self) -> dict:
        errors = []
        while not self._stderr.empty():
            value = self._stderr.get_nowait()
            if value is not None:
                errors.append(value.rstrip())
        return {
            "running": self.process is not None and self.process.poll() is None,
            "processId": self.process.pid if self.process is not None else None,
            "stderrTail": errors[-20:],
        }

    def stop(self) -> None:
        process = self.process
        self.process = None
        if process is None:
            return
        if process.stdin is not None:
            try:
                process.stdin.close()
            except OSError:
                pass
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
