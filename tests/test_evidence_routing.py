from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine


class FakeRuntime:
    config = object()
    nlp = object()

    def get_nlp(self):
        return self.nlp


class FakeKwja:
    def analyze(self, text, *, raw_knp=None, executable=None):
        return {"source": "stable-kwja"}


class FakeDictionary:
    def evaluate_analysis(self, analysis):
        return {"source": "stable-dictionary-analysis"}

    def evaluate_candidate(self, candidate, parser_pos=None):
        return {"source": "stable-dictionary-candidate"}


def main():
    calls = []

    def legacy(
        text, nlp, *, use_dictionary=True, raw_knp=None, kwja_executable=None,
        analyze_kwja_fn=None, evaluate_analysis_fn=None, evaluate_candidate_fn=None,
    ):
        kwargs = {
            "analyze_kwja_fn": analyze_kwja_fn,
            "evaluate_analysis_fn": evaluate_analysis_fn,
            "evaluate_candidate_fn": evaluate_candidate_fn,
        }
        calls.append(kwargs)
        assert kwargs["analyze_kwja_fn"]("x", raw_knp="RAW")["source"] == "stable-kwja"
        assert kwargs["evaluate_analysis_fn"]({})["source"] == "stable-dictionary-analysis"
        assert kwargs["evaluate_candidate_fn"]({})["source"] == "stable-dictionary-candidate"
        return {
            "version": "9.0.0-alpha2.2-evidence-gated-decision",
            "text": text,
            "morphemes": [{"start": 0, "end": 3, "surface": text}],
            "resolved_spans_alpha2": [
                {"start": 0, "end": 3, "surface": text, "role": "term"}
            ],
        }

    engine = AnalyzerEngine(
        runtime=FakeRuntime(),
        analyzer_fn=legacy,
        kwja_adapter=FakeKwja(),
        dictionary_adapter=FakeDictionary(),
    )
    engine.analyze_full("検証。", options=AnalyzeOptions(raw_knp="RAW"))
    assert len(calls) == 1
    print("evidence routing tests passed")


if __name__ == "__main__":
    main()
