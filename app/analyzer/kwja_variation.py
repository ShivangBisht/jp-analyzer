from __future__ import annotations
import hashlib, unicodedata
from typing import Any
from .layers.kwja import normalize_kwja
from .performance import semantic_fingerprint

def sha(value): return "sha256:"+hashlib.sha256(value.encode("utf-8")).hexdigest()
def stable_lines(raw): return [x.rstrip() for x in raw.replace("\r\n","\n").replace("\r","\n").split("\n") if x.rstrip() and not x.startswith("#")]
def line_type(line):
    if line is None:return "missing"
    if line.startswith("*"):return "bunsetsu"
    if line.startswith("+"):return "basic-phrase"
    return "eos" if line=="EOS" else "morpheme"
def line_diff(a,b):
    left,right=stable_lines(a),stable_lines(b); changed=[]
    for i in range(max(len(left),len(right))):
        x=left[i] if i<len(left) else None; y=right[i] if i<len(right) else None
        if x!=y: changed.append({"lineIndex":i,"leftType":line_type(x),"rightType":line_type(y),"leftSha256":sha(x or ""),"rightSha256":sha(y or "")})
    return {"changedLineCount":len(changed),"changed":changed}
def first_mismatch(a,b):
    for i in range(max(len(a),len(b))):
        x=a[i] if i<len(a) else None; y=b[i] if i<len(b) else None
        if x!=y:return {"offset":i,"leftCodePoint":f"U+{ord(x):04X}" if x else None,"rightCodePoint":f"U+{ord(y):04X}" if y else None,"leftName":unicodedata.name(x,"UNKNOWN") if x else None,"rightName":unicodedata.name(y,"UNKNOWN") if y else None}
    return None
def alignment(source,item):
    rebuilt="".join(str(x.get("surface") or "") for x in item.get("kwja_morphemes_alpha1") or [])
    ds=item.get("kwja_alignment_diagnostics_alpha1") or []
    return {"complete":bool((item.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete")),"sourceLength":len(source),"reconstructedLength":len(rebuilt),"firstMismatch":first_mismatch(source,rebuilt),"diagnosticCodes":[x.get("code") for x in ds]}
def summarize(source,outputs):
    items=[normalize_kwja(source,x,elapsed_ms=None) for x in outputs]; groups={}
    for i,x in enumerate(items):groups.setdefault(semantic_fingerprint(x),[]).append(i+1)
    reps=[v[0]-1 for v in groups.values()]; comparisons=[]
    for a,b in zip(reps,reps[1:]): comparisons.append({"leftAttempt":a+1,"rightAttempt":b+1,"rawLineDiff":line_diff(outputs[a],outputs[b]),"changedTopLevelFields":[k for k in sorted(set(items[a])|set(items[b])) if semantic_fingerprint(items[a].get(k))!=semantic_fingerprint(items[b].get(k))]})
    return {"sentenceSha256":sha(source),"variantCount":len(groups),"variants":[{"fingerprint":k,"attempts":v} for k,v in groups.items()],"comparisons":comparisons,"alignments":[alignment(source,x) for x in items]}
