import pytest

from app.analyzer.teaching_annotation_contract import (
    AnalyzerIdentity, AnalyzerSnapshot, AnnotationHistoryEvent, DerivedOutcome,
    SourceProvenance, SourceRange, TeachingAnnotation, TeachingTarget,
    build_partial_coverage, stable_dataset_assignment,
)

SENTENCE = "本電子書籍を示す。"


def spans():
    return [
        {"start": 0, "end": 1, "surface": "本"},
        {"start": 1, "end": 3, "surface": "電子"},
        {"start": 3, "end": 5, "surface": "書籍"},
        {"start": 5, "end": 6, "surface": "を"},
        {"start": 6, "end": 8, "surface": "示す"},
        {"start": 8, "end": 9, "surface": "。"},
    ]


def test_partial_annotation_marks_only_selected_range():
    selected = SourceRange(start=1, end=5, surface="電子書籍")
    coverage = build_partial_coverage(SENTENCE, selected)
    assert [item.state for item in coverage.regions] == ["unreviewed", "reviewed-corrected", "unreviewed"]
    assert coverage.wholeSentenceReviewed is False


def test_snapshot_requires_exact_reader_partition():
    identity = AnalyzerIdentity(
        analyzerVersion="test", readerSpanSchemaVersion="1.1", correctionRevision="r0"
    )
    snapshot = AnalyzerSnapshot(
        snapshotId="snap-1", identity=identity, sentence=SENTENCE,
        snapshotKind="raw-baseline", readerSpans=spans(),
        readerCandidates=[], readerSelection={},
    )
    assert snapshot.readerSpans[1]["surface"] == "電子"


def test_vocabulary_annotation_is_local_and_role_explicit():
    selected = SourceRange(start=1, end=5, surface="電子書籍")
    annotation = TeachingAnnotation(
        annotationId="ann-1", correctionId="corr-1",
        source=SourceProvenance(
            sentence=SENTENCE, sentenceFingerprint="fp", bookId="book-1",
        ),
        rawBaselineSnapshotId="snap-raw", effectiveBaselineSnapshotId="snap-effective",
        target=TeachingTarget(
            selectedRange=selected, action="mark-vocabulary", displayRole="lexical",
            targetReaderSpans=[{"start": 1, "end": 5, "surface": "電子書籍", "displayRole": "lexical"}],
        ),
        coverage=build_partial_coverage(SENTENCE, selected),
        derivedOutcome=DerivedOutcome(derivationStatus="pending"),
        history=[AnnotationHistoryEvent(eventId="evt-1", event="saved")],
        dataset=stable_dataset_assignment(SENTENCE, selected, "mark-vocabulary"),
    )
    assert annotation.coverage.regions[0].state == "unreviewed"
    assert annotation.target.displayRole == "lexical"


def test_vocabulary_requires_lexical_role():
    selected = SourceRange(start=1, end=5, surface="電子書籍")
    with pytest.raises(ValueError):
        TeachingTarget(
            selectedRange=selected, action="mark-vocabulary", displayRole="function",
            targetReaderSpans=[],
        )


def test_dataset_assignment_is_stable():
    selected = SourceRange(start=1, end=5, surface="電子書籍")
    first = stable_dataset_assignment(SENTENCE, selected, "mark-vocabulary")
    second = stable_dataset_assignment("別の電子書籍。", SourceRange(start=2, end=6, surface="電子書籍"), "mark-vocabulary")
    assert first.groupId == second.groupId
    assert first.partition == second.partition
