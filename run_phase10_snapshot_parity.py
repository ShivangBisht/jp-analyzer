from __future__ import annotations
import argparse, json, time
from pathlib import Path
from app.analyzer.pipeline import analyze_full
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest
from app.analyzer.ginza_runtime import get_ginza, ginza_model_name

def run(input_path, limit, reference_path):
    sentences = [x.strip() for x in input_path.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    if limit is not None: sentences = sentences[:limit]
    references = json.loads(reference_path.read_text(encoding="utf-8-sig")) if reference_path else None
    if references is not None and len(references) != len(sentences): raise RuntimeError("Reference count mismatch")
    nlp = get_ginza(); snapshots=[]; mismatches=[]; timings=[]
    for i, text in enumerate(sentences, 1):
        started=time.perf_counter(); snapshot=semantic_snapshot(analyze_full(text,nlp)); elapsed=(time.perf_counter()-started)*1000
        snapshots.append(snapshot); timings.append(elapsed); passed=references is None or snapshot == references[i-1]
        if not passed: mismatches.append({"sentenceId":f"S{i:04d}","expectedDigest":snapshot_digest(references[i-1]),"actualDigest":snapshot_digest(snapshot)})
        print(f"S{i:04d} snapshot={'CREATED' if references is None else ('PASS' if passed else 'FAIL')} elapsed_ms={elapsed:.2f}")
    if references is None: Path("phase10_semantic_snapshots.json").write_text(json.dumps(snapshots,ensure_ascii=False,indent=2),encoding="utf-8")
    Path("phase10_snapshot_mismatches.json").write_text(json.dumps(mismatches,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={"phase":"10.2-infrastructure","inputFile":str(input_path),"ginzaModel":ginza_model_name(),"requestedSentences":len(sentences),"mode":"create-reference" if references is None else "compare-reference","parityPassedSentences":len(sentences)-len(mismatches),"parityFailedSentences":len(mismatches),"semanticParity":not mismatches,"meanRuntimeMs":sum(timings)/len(timings) if timings else None}
    Path("phase10_snapshot_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2)); return 0 if not mismatches else 1

def main():
    p=argparse.ArgumentParser(); p.add_argument("input_file",type=Path); p.add_argument("--limit",type=int); p.add_argument("--reference",type=Path); a=p.parse_args(); raise SystemExit(run(a.input_file,a.limit,a.reference))
if __name__ == "__main__": main()
