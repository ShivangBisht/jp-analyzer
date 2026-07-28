from pathlib import Path
def test_save_links_annotation_and_compensates():
 text=Path('app/analyzer/reader_corrections_api.py').read_text(encoding='utf-8')
 assert 'annotationId' in text
 assert 'save_snapshot(full, compact' in text
 assert 'deactivate(result["correctionId"])' in text
 assert 'retract_for_correction' in text
 assert '@router.get("/annotations")' in text
