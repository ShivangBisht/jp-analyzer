from app.analyzer.adapters.kwja_adapter import KwjaAdapter
from app.analyzer.config import AnalyzerConfig

RAW = """# S-ID:test kwja:2.5.1
* -1D
+ -1D <体言>
検証 けんしょう 検証 名詞 6 普通名詞 1 * 0 * 0
。 。 。 特殊 1 句点 1 * 0 * 0
EOS
"""


def main():
    result = KwjaAdapter(AnalyzerConfig()).analyze("検証。", raw_knp=RAW)
    assert result["kwja_metadata_alpha1"]["source_alignment_complete"] is True
    print("Phase 10.4 KWJA adapter tests passed")


if __name__ == "__main__":
    main()
