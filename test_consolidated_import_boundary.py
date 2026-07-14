from pathlib import Path

def main():
    root = Path("app/analyzer")
    offenders = []
    for path in root.rglob("*.py"):
        if path.name == "legacy_reference.py":
            continue
        text = path.read_text(encoding="utf-8-sig")
        if "app.phase8" in text or "app.phase9" in text:
            offenders.append(str(path))
    assert not offenders, f"Consolidated analyzer still imports phase packages: {offenders}"
    print("Consolidated import-boundary test passed")

if __name__ == "__main__": main()
