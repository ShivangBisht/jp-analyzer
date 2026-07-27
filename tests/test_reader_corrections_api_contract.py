from __future__ import annotations

from app.analyzer.reader_corrections_api import (
    CorrectionListResponse,
    CorrectionRequest,
    DeactivateResponse,
    TeachingResultResponse,
)


def main():
    request = CorrectionRequest(
        sentence="少年が", start=0, end=3, surface="少年が",
        action="split", splitOffsets=[2],
    )
    assert request.splitOffsets == [2]
    for model in (TeachingResultResponse, CorrectionListResponse, DeactivateResponse):
        assert model.model_json_schema()["type"] == "object"
    print("reader correction API contract tests passed")


if __name__ == "__main__":
    main()
