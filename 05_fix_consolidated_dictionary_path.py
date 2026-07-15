from pathlib import Path

root = Path(__file__).resolve().parent
path = root / "app" / "analyzer" / "layers" / "dictionary_store.py"
text = path.read_text(encoding="utf-8-sig")
old = 'DB_PATH = Path(__file__).resolve().parents[2] / "data" / "phase8_analysis_lexicon.sqlite3"'
new = 'DB_PATH = Path(__file__).resolve().parents[3] / "data" / "phase8_analysis_lexicon.sqlite3"'

if new in text:
    print(f"Already correct: {path}")
elif old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print(f"Updated: {path}")
else:
    raise RuntimeError("Expected dictionary database path declaration was not found")
