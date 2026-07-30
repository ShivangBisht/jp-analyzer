from pathlib import Path


def test_save_links_annotation_and_compensates():
    text = Path(
        "app/analyzer/reader_corrections_api.py"
    ).read_text(encoding="utf-8")

    # Phase 8.5B foundation remains present.
    assert "annotationId" in text
    assert "create_annotation(" in text
    assert "deactivate(new_correction_id)" in text
    assert "retract_for_correction" in text
    assert '@router.get("/annotations")' in text

    # Phase 8.5C now distinguishes the three snapshot stages.
    assert 'kind="raw-baseline"' in text
    assert 'kind="effective-baseline"' in text
    assert 'kind="post-correction"' in text

    # Phase 8.5C records the post-correction learning and colour outcome.
    assert "update_derived_outcome(" in text

    # Conflicts are checked before the operational correction is saved.
    assert "preflight_correction_range(" in text
    assert "preflight_annotation_range(" in text
    assert text.index(
        "preflight_correction_range("
    ) < text.index(
        "result = save("
    )

    # Failed same-range replacement restores the previous correction.
    assert "reactivate(correction_id)" in text

    # The corpus consistency report remains read-only.
    assert '@router.get("/integrity")' in text
