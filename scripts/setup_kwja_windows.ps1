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
