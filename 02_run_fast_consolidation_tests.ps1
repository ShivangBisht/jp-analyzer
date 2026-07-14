$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw "Python not found: $Python" }

$Tests = @(
  "test_phase10_kwja_adapter.py",
  "test_phase10_dictionary_adapter.py",
  "test_phase10_evidence_routing.py",
  "test_phase10_runtime_reuse.py",
  "test_phase10_health_contract.py",
  "test_phase10_semantic_snapshot.py",
  "test_phase10_runtime_contracts.py",
  "test_phase10_facade.py",
  "test_consolidated_import_boundary.py",
  "test_consolidated_single_pass.py"
)
foreach ($Test in $Tests) {
  if (Test-Path $Test) {
    Write-Host "Running $Test" -ForegroundColor Cyan
    & $Python $Test
    if ($LASTEXITCODE -ne 0) { throw "Test failed: $Test" }
  }
}
Write-Host "All fast consolidation tests passed." -ForegroundColor Green
