from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from app.analyzer.kwja_variation import summarize
from app.analyzer.layers.kwja import run_kwja
def main():
 p=argparse.ArgumentParser();p.add_argument("--sentences",required=True);p.add_argument("--kwja-executable",required=True);p.add_argument("--output",required=True);p.add_argument("--repeats",type=int,default=3);p.add_argument("--indexes",default="0,2,6");a=p.parse_args()
 value=json.loads(Path(a.sentences).read_text(encoding="utf-8-sig")); sentences=value.get("sentences") if isinstance(value,dict) else value; rows=[]
 for i in [int(x) for x in a.indexes.split(",")]:
  outputs=[]; times=[]
  for n in range(a.repeats):
   print(f"Sentence {i}, attempt {n+1}/{a.repeats}"); raw,ms=run_kwja(str(sentences[i]),executable=a.kwja_executable);outputs.append(raw);times.append(ms)
  row=summarize(str(sentences[i]),outputs);row.update({"sentenceIndex":i,"executionMs":times});rows.append(row)
 result={"schema":"Phase12A2BVariationBenchmark.v1","productionActivated":False,"results":rows};Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n");print("Created:",a.output)
if __name__=="__main__":main()
