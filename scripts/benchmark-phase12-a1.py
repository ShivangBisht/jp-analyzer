from __future__ import annotations

from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import argparse,json,statistics,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from app.analyzer.performance import semantic_fingerprint
def req(url,body=None,timeout=180):
 data=None if body is None else json.dumps(body,ensure_ascii=False).encode("utf-8")
 q=urllib.request.Request(url,data=data,headers={"Accept":"application/json","Content-Type":"application/json"},method="GET" if body is None else "POST")
 with urllib.request.urlopen(q,timeout=timeout) as r:return json.loads(r.read().decode("utf-8"))
def main():
 a=argparse.ArgumentParser();a.add_argument("--sentences",required=True);a.add_argument("--repeats",type=int,default=3);a.add_argument("--base-url",default="http://127.0.0.1:8766");a.add_argument("--output",default="phase12_a1_benchmark_results.json");x=a.parse_args()
 ss=json.loads(Path(x.sentences).read_text(encoding="utf-8-sig"))["sentences"];rows=[]
 for i,s in enumerate(ss):
  fps=[]
  for n in range(1,x.repeats+1):
   before=req(x.base_url+"/liveness",timeout=30);t=time.perf_counter();r=req(x.base_url+"/analyze",{"text":s,"performanceDiagnostics":True});secs=time.perf_counter()-t;after=req(x.base_url+"/liveness",timeout=30);fp=semantic_fingerprint(r);fps.append(fp);rows.append({"sentenceIndex":i,"attempt":n,"seconds":secs,"fingerprint":fp,"livenessBefore":before,"livenessAfter":after,"performanceDiagnostics":r.get("performanceDiagnostics")})
  if len(set(fps))!=1:raise SystemExit(f"Semantic drift for sentence {i}")
 ds=[z["seconds"] for z in rows];out={"schema":"Phase12A1Benchmark.v1","capturedAt":datetime.now(timezone.utc).isoformat(),"sentenceCount":len(ss),"repeats":x.repeats,"requestCount":len(rows),"summary":{"minimumSeconds":min(ds),"medianSeconds":statistics.median(ds),"meanSeconds":statistics.mean(ds),"maximumSeconds":max(ds)},"rows":rows}
 Path(x.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n");print("Created:",Path(x.output).resolve());print("Requests:",len(rows));print("Semantic drift: none")
if __name__=="__main__":main()
