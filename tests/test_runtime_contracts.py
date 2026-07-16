from pathlib import Path
from app.analyzer.config import AnalyzerConfig
from app.analyzer.kwja_runtime import kwja_status
from app.analyzer.source_contract import validate_analysis_source

def main():
    cfg = AnalyzerConfig(kwja_executable=Path("missing-kwja.exe"))
    assert not cfg.kwja_available() and not kwja_status(cfg)["available"]
    valid = {"text":"検証。", "morphemes":[{"start":0,"end":2,"surface":"検証"},{"start":2,"end":3,"surface":"。"}], "resolved_spans_alpha2":[{"start":0,"end":2,"surface":"検証"},{"start":2,"end":3,"surface":"。"}]}
    assert validate_analysis_source(valid) == []
    invalid = dict(valid); invalid["resolved_spans_alpha2"] = [{"start":0,"end":2,"surface":"誤り"}]
    codes = {x["code"] for x in validate_analysis_source(invalid)}
    assert {"SOURCE_SURFACE_MISMATCH", "SOURCE_PARTITION_INCOMPLETE"} <= codes
    print("runtime contract tests passed")
if __name__ == "__main__": main()
