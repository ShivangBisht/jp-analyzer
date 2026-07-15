from pathlib import Path

root = Path(__file__).resolve().parent
patch = root / "06_harden_corpus_parity_runner.py"
test = root / "test_consolidated_kwja_timeout.py"

patch_text = patch.read_text(encoding="utf-8-sig")
replacements = (
    ('timeout: int = 120', 'timeout_seconds: int = 120'),
    ('timeout: int = 300', 'timeout_seconds: int = 300'),
)
for old, new in replacements:
    patch_text = patch_text.replace(old, new)
patch.write_text(patch_text, encoding="utf-8", newline="\n")
print(f"Updated: {patch.name}")

if test.exists():
    test_text = test.read_text(encoding="utf-8-sig")
    test_text = test_text.replace('parameters["timeout"]', 'parameters["timeout_seconds"]')
    test.write_text(test_text, encoding="utf-8", newline="\n")
    print(f"Updated: {test.name}")
