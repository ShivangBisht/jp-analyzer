# KWJA setup on Windows

KWJA is an internal analyzer layer. Its heavy Python 3.11 environment is isolated in `.kwja-venv`; it is not a separate application or repository.

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\setup_kwja_windows.ps1
$env:KWJA_EXE = "$PWD\.kwja-venv\Scripts\kwja.exe"
```

Never disable TLS certificate verification. The pure-Python `pure-cdb` installation avoids requiring Microsoft C++ Build Tools.
