from __future__ import annotations

import tempfile
from pathlib import Path

import app.analyzer.reader_corrections as rc


def base_run():
    return [
        {
            "start": 0, "end": 2, "surface": "少年",
            "displayRole": "lexical", "knownLookupKey": "少年",
            "frequencyLookupKey": "少年", "headword": "少年",
        },
        {"start": 2, "end": 3, "surface": "が", "displayRole": "function"},
        {
            "start": 3, "end": 5, "surface": "走っ",
            "displayRole": "lexical", "knownLookupKey": "走る",
            "frequencyLookupKey": "走る", "headword": "走る",
        },
        {
            "start": 5, "end": 8, "surface": "てきた",
            "displayRole": "learnable-grammar", "grammarId": "TE_KURU",
        },
        {"start": 8, "end": 9, "surface": "。", "displayRole": "punctuation"},
    ]


def main():
    with tempfile.TemporaryDirectory() as directory:
        rc.DB_PATH = Path(directory) / "corrections.sqlite3"
        data = {
            "sentence": "少年が走ってきた。",
            "start": 3,
            "end": 8,
            "surface": "走ってきた",
            "action": "show-as-one-unit",
            "scope": "occurrence",
        }
        baseline = base_run()

        preview = rc.preview(data, baseline)
        assert preview["saved"] is False
        assert not rc.DB_PATH.exists()
        taught = preview["previewReaderSpans"][2]
        assert taught["surface"] == "走ってきた"
        assert taught["displayRole"] == "learnable-grammar"
        assert taught["grammarId"] == "TE_KURU"
        assert taught["hostLookupKey"] == "走る"
        assert taught["grammarFocusRanges"] == [
            {"start": 5, "end": 8, "surface": "てきた", "grammarId": "TE_KURU"}
        ]
        assert taught["knownLookupKey"] is None

        saved = rc.save(data, baseline, "test", "1.1")
        correction_id = saved["correctionId"]
        assert saved["saved"] is True
        rows = rc.list_corrections()
        assert len(rows) == 1
        assert rows[0]["known_lookup_key"] is None
        assert rows[0]["grammar_id"] == "TE_KURU"

        applied, provenance = rc.apply_active_corrections(data["sentence"], baseline)
        assert [item["surface"] for item in applied] == ["少年", "が", "走ってきた", "。"]
        assert applied[2]["projectionStatus"] == "user-corrected"
        assert applied[2]["correctionId"] == correction_id
        assert provenance[0]["action"] == "show-as-one-unit"

        other, other_provenance = rc.apply_active_corrections(
            "彼が走ってきた。",
            [
                {"start": 0, "end": 1, "surface": "彼", "displayRole": "lexical"},
                {"start": 1, "end": 2, "surface": "が", "displayRole": "function"},
                {"start": 2, "end": 4, "surface": "走っ", "displayRole": "lexical"},
                {"start": 4, "end": 7, "surface": "てきた", "displayRole": "learnable-grammar"},
                {"start": 7, "end": 8, "surface": "。", "displayRole": "punctuation"},
            ],
        )
        assert [item["surface"] for item in other] == ["彼", "が", "走っ", "てきた", "。"]
        assert other_provenance == []

        neutral = rc.preview(
            {
                "sentence": "少年が走ってきた。",
                "start": 3,
                "end": 8,
                "surface": "走ってきた",
                "action": "mark-unresolved",
                "scope": "occurrence",
            },
            baseline,
        )
        assert neutral["previewReaderSpans"][2]["displayRole"] == "unresolved"
        assert neutral["previewReaderSpans"][2]["colorPolicy"] == "neutral"

        rc.deactivate(correction_id)
        restored, restored_provenance = rc.apply_active_corrections(data["sentence"], baseline)
        assert [item["surface"] for item in restored] == ["少年", "が", "走っ", "てきた", "。"]
        assert restored_provenance == []
        assert rc.list_corrections() == []
        assert len(rc.list_corrections(True)) == 1

    print("reader structural teaching backend tests passed")


if __name__ == "__main__":
    main()
