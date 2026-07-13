from __future__ import annotations
import json
from pathlib import Path
import spacy
from app.phase9.enrichment_alpha2 import analyze_integrated_alpha2

TESTS = [
    "『寝坊った』という動詞が娘の造語なのか",
    "私は、へなへなとその場にへたり込んでしまう。",
    "誰かに代わってもらえるように自分からお願いしたの",
    "毎日が寂しくてつまらないから、美羽ちゃんと一緒に暮らしたいの。",
    "恋愛とかそういうの、遠慮してた感じではあったんでしょ？",
]

def load_ginza():
    cfg={"components":{"compound_splitter":{"split_mode":"A"}}}
    for name in ("ja_ginza_electra","ja_ginza"):
        try: return spacy.load(name,config=cfg),name
        except Exception: pass
    raise RuntimeError("GiNZA unavailable")

def main():
    nlp,model=load_ginza(); rows=[]
    for i,text in enumerate(TESTS,1):
        result=analyze_integrated_alpha2(text,nlp)
        row={
            "id":f"A2F-{i:02d}","text":text,
            "baseline_spans":result["resolved_spans_alpha34"],
            "alpha2_spans":result["resolved_spans_alpha2"],
            "kwja_candidates":result["kwja_candidates_alpha2"],
            "change_summary":result["alpha2_change_summary"],
            "diagnostics":result["diagnostics_alpha2"],
        }
        rows.append(row)
        print(row["id"], "proposals=",len(row["kwja_candidates"]),"selected=",row["change_summary"]["kwja_selected_count"],"unresolved=",row["change_summary"]["alpha2_unresolved_count"])
    output={"version":"9.0.0-alpha2.1-controlled-cross-phrase","ginza_model":model,"results":rows}
    Path("phase9_alpha2_focused_results.json").write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Wrote phase9_alpha2_focused_results.json")

if __name__=="__main__": main()
