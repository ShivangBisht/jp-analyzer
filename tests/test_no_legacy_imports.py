from pathlib import Path


FORBIDDEN_IMPORT_PREFIXES = (
    "app." + "phase" + "8",
    "app." + "phase" + "9",
)


def main():
    repository = Path(__file__).resolve().parents[1]
    offenders = []
    for directory in (repository / "app" / "analyzer", repository / "tests"):
        for path in directory.rglob("*.py"):
            text = path.read_text(encoding="utf-8-sig")
            if any(prefix in text for prefix in FORBIDDEN_IMPORT_PREFIXES):
                offenders.append(str(path.relative_to(repository)))
    assert not offenders, f"Historical package imports remain: {offenders}"
    print("No-legacy-import test passed")


if __name__ == "__main__":
    main()
