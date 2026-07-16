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
