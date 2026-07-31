from app.analyzer.teaching_quality_store import QUALITY_STATES

def test_quality_states_and_export_boundary():
    assert QUALITY_STATES == {"captured","needs-review","reviewed","approved","rejected-for-corpus"}
