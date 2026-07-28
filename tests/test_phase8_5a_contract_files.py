from pathlib import Path


def test_contract_document_exists():
    assert Path("docs/TEACHING_ANNOTATION_CONTRACT.md").is_file()


def test_audit_document_exists():
    assert Path("docs/PHASE8_5A_CURRENT_DATA_AUDIT.md").is_file()
