from __future__ import annotations

from unittest.mock import patch

from app.analyzer import reader_corrections as corrections


def main() -> None:
    records = [
        {
            "correctionId": "b",
            "sentenceFingerprint": "sentence-2",
            "start": 1,
            "end": 2,
            "surface": "乙",
            "action": "mark-unresolved",
            "displayRole": "unresolved",
            "scope": "occurrence",
            "replacementReaderSpans": [],
        },
        {
            "correctionId": "a",
            "sentenceFingerprint": "sentence-1",
            "start": 0,
            "end": 1,
            "surface": "甲",
            "action": "show-as-one-unit",
            "displayRole": "lexical",
            "scope": "occurrence",
            "replacementReaderSpans": [
                {"start": 0, "end": 1, "surface": "甲"}
            ],
        },
    ]

    with patch.object(
        corrections,
        "list_corrections",
        return_value=records,
    ):
        first = corrections.correction_revision()

    with patch.object(
        corrections,
        "list_corrections",
        return_value=list(reversed(records)),
    ):
        assert corrections.correction_revision() == first

    changed = [dict(record) for record in records]
    changed[0]["displayRole"] = "function"

    with patch.object(
        corrections,
        "list_corrections",
        return_value=changed,
    ):
        assert corrections.correction_revision() != first

    assert len(first) == 64
    print("correction revision tests passed")


if __name__ == "__main__":
    main()
