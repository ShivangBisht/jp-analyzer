# Phase 7A.1 - Sudachi/GiNZA Evaluation Service

This is an isolated prototype. It does not modify the working Novel Audio Miner app.

## Purpose

Compare modern Japanese linguistic analysis before changing production word coloring:

- Sudachi modes A, B and C
- dictionary forms
- normalized forms
- POS and conjugation information
- GiNZA dependencies and named entities
- original character offsets and coverage

## Windows setup

Use Python 3.11 if possible.

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

Start the service:

```powershell
.\start.ps1
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
```

Analyze one sentence:

```powershell
$body = @{
  text = "ほら、さっさと食べちゃいなさい。"
  include_ginza = $true
  sudachi_modes = @("A", "B", "C")
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8765/analyze `
  -ContentType "application/json; charset=utf-8" `
  -Body $body | ConvertTo-Json -Depth 12
```

Interactive command-line comparison:

```powershell
.\.venv\Scripts\python.exe compare.py "一息つきつつ、私は四角いフライパンで卵を焼いていく。"
```

Run the known-problem QA set:

```powershell
.\.venv\Scripts\python.exe run_qa.py
```

This writes `qa_results.json`.

## API contract

`POST /analyze` accepts:

```json
{
  "text": "微妙だった。",
  "include_ginza": true,
  "sudachi_modes": ["A", "B", "C"]
}
```

The response preserves original offsets and includes Sudachi and GiNZA outputs separately. No mining-word decision is made yet. This is intentional: first evaluate which analyzer output is reliable, then design the structural adapter.

## Next checkpoint

Review the QA output for:

- `食べちゃいなさい`
- `なんで`
- `起こしてくれなかった`
- `一息つき`
- `膝を折り`
- `働き始めた`
- `完っ全`
- copula structures such as `微妙だった`

Only after comparison should this service be connected to the React app.
