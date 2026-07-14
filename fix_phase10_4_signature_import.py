from pathlib import Path

path = Path("app/analyzer/engine.py")
text = path.read_text(encoding="utf-8")

required = "from inspect import signature"

if required in text:
    print("Import already present.")
else:
    target = "from typing import Any"

    if target not in text:
        raise RuntimeError(
            "Could not find the expected typing import."
        )

    text = text.replace(
        target,
        required + "\n" + target,
        1,
    )

    path.write_text(
        text,
        encoding="utf-8",
    )

    print("Added: from inspect import signature")
