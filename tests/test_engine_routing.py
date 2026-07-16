from __future__ import annotations

from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine


class FakeRuntime:
    def __init__(self):
        self.nlp = object()
        self.calls = 0

    def get_nlp(self):
        self.calls += 1
        return self.nlp


def main():
    runtime = FakeRuntime()
    calls = []

    def legacy(text, nlp, **kwargs):
        calls.append((text, nlp, kwargs))
        return {
            "version": "9.0.0-alpha2.2-evidence-gated-decision",
            "text": text,
            "morphemes": [
                {"start": 0, "end": 2, "surface": "検証"},
                {"start": 2, "end": 3, "surface": "。"},
            ],
            "resolved_spans_alpha2": [
                {"start": 0, "end": 2, "surface": "検証", "role": "term"},
                {"start": 2, "end": 3, "surface": "。", "role": "punctuation"},
            ],
        }

    engine = AnalyzerEngine(runtime=runtime, analyzer_fn=legacy)
    result = engine.analyze_full(
        "検証。",
        options=AnalyzeOptions(use_dictionary=False, raw_knp="RAW"),
    )
    assert result["text"] == "検証。"
    assert runtime.calls == 1
    assert calls[0][1] is runtime.nlp
    assert calls[0][2] == {
        "use_dictionary": False,
        "raw_knp": "RAW",
        "kwja_executable": None,
    }

    supplied_nlp = object()
    engine.analyze_full("検証。", supplied_nlp)
    assert runtime.calls == 1
    assert calls[1][1] is supplied_nlp
    print("engine routing tests passed")


if __name__ == "__main__":
    main()
