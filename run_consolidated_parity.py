from __future__ import annotations
import argparse, json, time
from pathlib import Path
from app.analyzer.ginza_runtime import get_ginza
from app.analyzer.layers import analyze_layers
from app.analyzer.legacy_reference import analyze_legacy
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest

def load(path): return [x.strip() for x in path.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
def run(args):
    sentences = load(args.input_file)
    if args.limit: sentences = sentences[:args.limit]
    nlp = get_ginza(); mismatches=[]; snapshots=[]; times=[]
    references = json.loads(args.reference.read_text(encoding="utf-8-sig")) if args.reference else None
    if references is not None and len(references) != len(sentences): raise RuntimeError("Reference count mismatch")
    for i,text in enumerate(sentences,1):
        started=time.perf_counter()
        if args.create_reference:
            actual=semantic_snapshot(analyze_legacy(text,nlp))
        else:
            actual=semantic_snapshot(analyze_layers(text,nlp))
        times.append((time.perf_counter()-started)*1000); snapshots.append(actual)
        expected = references[i-1] if references is not None else actual
        if actual != expected: mismatches.append({"sentenceId":f"S{i:04d}","expectedDigest":snapshot_digest(expected),"actualDigest":snapshot_digest(actual),"text":text})
        print(f"S{i:04d} {'PASS' if actual == expected else 'FAIL'} elapsed_ms={times[-1]:.2f}")
    if args.output: args.output.write_text(json.dumps(snapshots,ensure_ascii=False,indent=2),encoding="utf-8")
    report={"inputFile":str(args.input_file),"sentences":len(sentences),"passed":len(sentences)-len(mismatches),"failed":len(mismatches),"semanticParity":not mismatches,"meanRuntimeMs":sum(times)/len(times) if times else None,"mismatches":mismatches}
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "mismatches"},ensure_ascii=False,indent=2))
    return 0 if not mismatches else 1
def main():
    p=argparse.ArgumentParser(); p.add_argument("input_file",type=Path); p.add_argument("--limit",type=int); p.add_argument("--create-reference",action="store_true"); p.add_argument("--reference",type=Path); p.add_argument("--output",type=Path); p.add_argument("--report",type=Path,default=Path("consolidated_parity_report.json")); a=p.parse_args()
    if a.create_reference and a.reference: p.error("choose --create-reference or --reference")
    if not a.create_reference and a.reference is None: p.error("comparison mode requires --reference")
    raise SystemExit(run(a))
if __name__ == "__main__": main()
