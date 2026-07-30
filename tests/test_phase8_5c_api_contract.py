from pathlib import Path
from app.analyzer.reader_corrections_api import TeachingResultResponse, DeactivateResponse

def test_typed_lifecycle_fields():
 fields=TeachingResultResponse.model_fields
 for name in ('annotationId','rawBaselineSnapshotId','effectiveBaselineSnapshotId','postCorrectionSnapshotId','derivedOutcome'): assert name in fields
 assert 'annotationId' in DeactivateResponse.model_fields

def test_preflight_precedes_save_and_integrity_route_exists():
 text=Path('app/analyzer/reader_corrections_api.py').read_text(encoding='utf-8')
 assert text.index('preflight_correction_range') < text.index('result = save(')
 assert '@router.get("/integrity")' in text
 assert 'update_derived_outcome' in text and 'kind="post-correction"' in text
