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
