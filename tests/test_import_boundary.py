from pathlib import Path


FORBIDDEN_IMPORT_PREFIXES = (
    "app." + "phase" + "8",
    "app." + "phase" + "9",
)


def main():
    package = Path(__file__).resolve().parents[1] / "app" / "analyzer"
    offenders = []
    for path in package.rglob("*.py"):
        text = path.read_text(encoding="utf-8-sig")
        if any(prefix in text for prefix in FORBIDDEN_IMPORT_PREFIXES):
            offenders.append(str(path.relative_to(package.parent.parent)))
    assert not offenders, f"Consolidated analyzer imports historical packages: {offenders}"
    print("Consolidated import-boundary test passed")


if __name__ == "__main__":
    main()
