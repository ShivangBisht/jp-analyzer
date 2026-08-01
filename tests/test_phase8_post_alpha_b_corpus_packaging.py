import json
from app.analyzer.teaching_tuning_corpus import build_tuning_corpus_package, verify_tuning_corpus_package

def test_profiles_are_deterministic_and_safe(monkeypatch):
    preview={"corpusDigest":"sha256:"+"a"*64,"splitPolicy":{"train":80,"validation":10,"test":10},"splitCounts":{"train":1,"validation":0,"test":0},"eligibleRecords":[{"recordId":"tdr-a","snapshotId":"ads-a","split":"train"}]}
    record={"recordId":"tdr-a","contentDigest":"sha256:"+"b"*64,"sourceSentence":"example sentence","reviewCoverage":[],"judgment":"corrected","assertions":{"boundary":{"start":0,"end":7,"surface":"example"},"classification":{"assertedRole":"lexical"}},"approvedTarget":{"targetSpans":[]},"failureClassification":"boundary-error","confidence":"confident"}
    snapshot={"snapshotId":"ads-a","contentDigest":"sha256:"+"c"*64,"schemaVersion":"1.0","source":{"sentence":"example sentence"},"analyzerIdentity":{},"dictionaryIdentity":{},"readerDecision":{"selectedSpans":[{"start":0,"end":7,"surface":"example","displayRole":"lexical"}],"candidates":[]},"coreDecision":{"candidates":[],"resolvedSpans":[]},"correctionContext":{}}
    quality={"quality_status":"approved","reviewer":"tester","quality_note":"private note","updated_at":"now"}
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.build_export_preview",lambda **k:preview)
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.get_record",lambda *a,**k:record)
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.get_snapshot",lambda *a,**k:snapshot)
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.get_quality",lambda *a,**k:quality)
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.dictionary_status",lambda:{"ready":True,"entryCount":1,"dictionaryCount":1,"registryConsistent":True,"installedDictionaries":[]})
    private=build_tuning_corpus_package("private-local")
    share=build_tuning_corpus_package("redacted-shareable")
    assert verify_tuning_corpus_package(private)["ok"]
    assert verify_tuning_corpus_package(share)["ok"]
    assert private["tuningEnabled"] is False and private["activationEnabled"] is False
    assert private["examples"][0]["sourceSentence"] == "example sentence"
    assert "sourceSentence" not in json.dumps(share)
    assert "reviewer" not in share["examples"][0]["qualityApproval"]
    assert "qualityNote" not in share["examples"][0]["qualityApproval"]

def test_tamper_rejected(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.build_export_preview",lambda **k:{"corpusDigest":"x","splitPolicy":{},"splitCounts":{},"eligibleRecords":[]})
    monkeypatch.setattr("app.analyzer.teaching_tuning_corpus.dictionary_status",lambda:{"ready":True,"entryCount":0,"dictionaryCount":0,"registryConsistent":True,"installedDictionaries":[]})
    package=build_tuning_corpus_package()
    package["deploymentEnabled"]=True
    assert not verify_tuning_corpus_package(package)["ok"]


def test_redacted_profile_removes_nested_private_metadata(monkeypatch):
    preview = {
        "corpusDigest": "sha256:" + "d" * 64,
        "splitPolicy": {
            "train": 80,
            "validation": 10,
            "test": 10,
        },
        "splitCounts": {
            "train": 1,
            "validation": 0,
            "test": 0,
        },
        "eligibleRecords": [
            {
                "recordId": "tdr-private",
                "snapshotId": "ads-private",
                "split": "train",
            }
        ],
    }

    record = {
        "recordId": "tdr-private",
        "contentDigest": "sha256:" + "e" * 64,
        "sourceSentence": "PRIVATE_SENTENCE_TEXT",
        "reviewCoverage": [],
        "judgment": "corrected",
        "assertions": {
            "boundary": {
                "start": 0,
                "end": 7,
                "surface": "PRIVATE_SURFACE",
            },
            "classification": {
                "assertedRole": "lexical",
            },
        },
        "approvedTarget": {
            "targetSpans": [],
            "provenance": {
                "bookTitle": "PRIVATE_BOOK_TITLE",
                "bookId": "PRIVATE_BOOK_ID",
                "chapterTitle": "PRIVATE_CHAPTER_TITLE",
                "sceneTitle": "PRIVATE_SCENE_TITLE",
                "leftContext": "PRIVATE_LEFT_CONTEXT",
                "rightContext": "PRIVATE_RIGHT_CONTEXT",
            },
        },
        "failureClassification": "boundary-error",
        "confidence": "confident",
        "note": "PRIVATE_RECORD_NOTE",
    }

    snapshot = {
        "snapshotId": "ads-private",
        "contentDigest": "sha256:" + "f" * 64,
        "schemaVersion": "1.0",
        "source": {
            "sentence": "PRIVATE_SENTENCE_TEXT",
            "bookTitle": "PRIVATE_BOOK_TITLE",
            "bookId": "PRIVATE_BOOK_ID",
            "leftContext": "PRIVATE_LEFT_CONTEXT",
            "rightContext": "PRIVATE_RIGHT_CONTEXT",
        },
        "analyzerIdentity": {},
        "dictionaryIdentity": {
            "database": "D:/PRIVATE/phase8_analysis_lexicon.sqlite3",
            "databasePath": "D:/PRIVATE/database-path.sqlite3",
            "lastSyncId": "PRIVATE_SYNC_ID",
        },
        "readerDecision": {
            "selectedSpans": [
                {
                    "start": 0,
                    "end": 7,
                    "surface": "PRIVATE_SURFACE",
                    "displayRole": "lexical",
                    "headword": "PRIVATE_HEADWORD",
                }
            ],
            "candidates": [],
        },
        "coreDecision": {
            "candidates": [],
            "resolvedSpans": [],
        },
        "correctionContext": {},
        "nestedPrivateMetadata": {
            "localPath": "D:/PRIVATE/local-path",
            "sourceStorePath": "D:/PRIVATE/source-store",
            "readerLibraryId": "PRIVATE_LIBRARY_ID",
        },
    }

    quality = {
        "quality_status": "approved",
        "reviewer": "PRIVATE_REVIEWER",
        "quality_note": "PRIVATE_QUALITY_NOTE",
        "updated_at": "now",
    }

    dictionary = {
        "ready": True,
        "entryCount": 1,
        "dictionaryCount": 1,
        "registryConsistent": True,
        "database": "D:/PRIVATE/dictionary.sqlite3",
        "databasePath": "D:/PRIVATE/dictionary-path.sqlite3",
        "lastSyncId": "PRIVATE_SYNC_ID",
        "installedDictionaries": [],
    }

    monkeypatch.setattr(
        "app.analyzer.teaching_tuning_corpus.build_export_preview",
        lambda **kwargs: preview,
    )

    monkeypatch.setattr(
        "app.analyzer.teaching_tuning_corpus.get_record",
        lambda *args, **kwargs: record,
    )

    monkeypatch.setattr(
        "app.analyzer.teaching_tuning_corpus.get_snapshot",
        lambda *args, **kwargs: snapshot,
    )

    monkeypatch.setattr(
        "app.analyzer.teaching_tuning_corpus.get_quality",
        lambda *args, **kwargs: quality,
    )

    monkeypatch.setattr(
        "app.analyzer.teaching_tuning_corpus.dictionary_status",
        lambda: dictionary,
    )

    private_first = build_tuning_corpus_package("private-local")
    private_second = build_tuning_corpus_package("private-local")

    redacted_first = build_tuning_corpus_package(
        "redacted-shareable"
    )
    redacted_second = build_tuning_corpus_package(
        "redacted-shareable"
    )

    assert verify_tuning_corpus_package(private_first)["ok"]
    assert verify_tuning_corpus_package(redacted_first)["ok"]

    assert (
        private_first["packageDigest"]
        == private_second["packageDigest"]
    )

    assert (
        redacted_first["packageDigest"]
        == redacted_second["packageDigest"]
    )

    prohibited_keys = {
        "sourceSentence",
        "bookTitle",
        "bookId",
        "chapterTitle",
        "sceneTitle",
        "leftContext",
        "rightContext",
        "reviewer",
        "qualityNote",
        "quality_note",
        "database",
        "databasePath",
        "localPath",
        "sourceStorePath",
        "readerLibraryId",
        "lastSyncId",
    }

    def find_prohibited_keys(value):
        found = set()

        if isinstance(value, dict):
            found.update(
                key
                for key in value
                if key in prohibited_keys
            )

            for item in value.values():
                found.update(find_prohibited_keys(item))

        elif isinstance(value, list):
            for item in value:
                found.update(find_prohibited_keys(item))

        return found

    assert find_prohibited_keys(redacted_first) == set()

    encoded = json.dumps(
        redacted_first,
        ensure_ascii=False,
    )

    prohibited_values = {
        "PRIVATE_SENTENCE_TEXT",
        "PRIVATE_SURFACE",
        "PRIVATE_BOOK_TITLE",
        "PRIVATE_BOOK_ID",
        "PRIVATE_CHAPTER_TITLE",
        "PRIVATE_SCENE_TITLE",
        "PRIVATE_LEFT_CONTEXT",
        "PRIVATE_RIGHT_CONTEXT",
        "PRIVATE_RECORD_NOTE",
        "PRIVATE_REVIEWER",
        "PRIVATE_QUALITY_NOTE",
        "PRIVATE_HEADWORD",
        "PRIVATE_SYNC_ID",
        "PRIVATE_LIBRARY_ID",
        "D:/PRIVATE",
    }

    for value in prohibited_values:
        assert value not in encoded

    assert redacted_first["tuningEnabled"] is False
    assert redacted_first["activationEnabled"] is False
    assert redacted_first["deploymentEnabled"] is False
    assert redacted_first["includesSqliteBytes"] is False

    assert (
        redacted_first["includesOperationalCorrections"]
        is False
    )
