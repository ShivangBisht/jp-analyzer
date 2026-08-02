from __future__ import annotations
import json
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

@dataclass(frozen=True)
class ProbeResult:
    ok: bool
    status: int | None = None
    body: dict | str | None = None
    error: str | None = None

def probe(url: str, timeout: float = 2.0, *, accept: str = "application/json") -> ProbeResult:
    try:
        with urlopen(Request(url, headers={"Accept": accept}), timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try: body = json.loads(raw)
            except json.JSONDecodeError: body = raw
            return ProbeResult(200 <= response.status < 300, response.status, body)
    except HTTPError as error:
        return ProbeResult(False, error.code, error=str(error))
    except (URLError, TimeoutError, OSError) as error:
        return ProbeResult(False, error=str(error))

def wait_for(url: str, timeout_seconds: float, process=None, *, accept: str = "application/json") -> ProbeResult:
    deadline = time.monotonic() + timeout_seconds
    last = ProbeResult(False, error="not attempted")
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            return ProbeResult(False, error=f"process exited with code {process.returncode}")
        last = probe(url, accept=accept)
        if last.ok: return last
        time.sleep(0.4)
    return ProbeResult(False, error=f"timed out waiting for {url}; {last.error}")
