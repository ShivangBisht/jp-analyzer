from app.analyzer.contracts import AnalyzeOptions
from app.analyzer.engine import AnalyzerEngine

class Runtime:
    config = None
    services = None
    def get_nlp(self): return object()

def main():
    calls = {"engine": 0}
    def layer_engine(text, nlp, **kwargs):
        calls["engine"] += 1
        return {"version":"9.0.0-alpha2.2-evidence-gated-decision","text":text,"morphemes":[{"start":0,"end":1,"surface":text}],"resolved_spans_alpha2":[{"start":0,"end":1,"surface":text,"role":"term"}]}
    engine = AnalyzerEngine(runtime=Runtime(), legacy_engine=layer_engine)
    engine.analyze_full("検", options=AnalyzeOptions())
    assert calls["engine"] == 1
    print("Consolidated single-pass test passed")

if __name__ == "__main__": main()
