from __future__ import annotations

import ipaddress
import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

METADATA_LIMIT = 2 * 1024 * 1024
ARCHIVE_LIMIT = 512 * 1024 * 1024
TIMEOUT_SECONDS = 45
ALLOWED_SCHEMES = {"https"}


def _validate_url(url: str) -> str:
    value = str(url or "").strip()
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError("Only public HTTPS update URLs are allowed")
    host = parsed.hostname.lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise ValueError("Local update hosts are not allowed")
    try:
        addresses = socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise ValueError(f"Update host could not be resolved: {host}") from error
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise ValueError("Private or local update addresses are not allowed")
    return value


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _open(url: str, accept: str):
    checked = _validate_url(url)
    request = urllib.request.Request(
        checked,
        headers={
            "Accept": accept,
            "User-Agent": "Novel-Audio-Miner-Dictionary-Updater/7.5B",
        },
    )
    opener = urllib.request.build_opener(SafeRedirectHandler())
    return opener.open(request, timeout=TIMEOUT_SECONDS)


def _read_limited(response, limit: int) -> bytes:
    length = response.headers.get("Content-Length")
    if length and int(length) > limit:
        raise ValueError("Remote update exceeds the allowed size")
    chunks = []
    total = 0
    while True:
        chunk = response.read(min(1024 * 1024, limit - total + 1))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise ValueError("Remote update exceeds the allowed size")
    return b"".join(chunks)


def fetch_update_metadata(url: str) -> dict[str, Any]:
    try:
        with _open(url, "application/json") as response:
            raw = _read_limited(response, METADATA_LIMIT)
            final_url = response.geturl()
            status = getattr(response, "status", 200)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Update metadata returned HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Unable to reach update host: {error.reason}") from error
    try:
        payload = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Update metadata is not valid UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise ValueError("Update metadata must be a JSON object")
    return {"status": "ok", "route": "analyzer", "url": final_url, "httpStatus": status, "metadata": payload}


def fetch_update_archive(url: str) -> tuple[bytes, dict[str, Any]]:
    try:
        with _open(url, "application/zip, application/octet-stream") as response:
            raw = _read_limited(response, ARCHIVE_LIMIT)
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "application/zip")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Dictionary archive returned HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Unable to reach dictionary archive host: {error.reason}") from error
    if len(raw) < 4 or raw[:2] != b"PK":
        raise ValueError("Downloaded update is not a ZIP archive")
    return raw, {"route": "analyzer", "url": final_url, "contentType": content_type, "sizeBytes": len(raw)}
