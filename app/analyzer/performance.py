from __future__ import annotations
import hashlib,json
VOLATILE_KEYS={"performanceDiagnostics","capturedAt","elapsed_ms","elapsedMs","requestId","request_id"}
def semantic_projection(v):
    if isinstance(v,dict): return {k:semantic_projection(x) for k,x in sorted(v.items()) if k not in VOLATILE_KEYS}
    if isinstance(v,list): return [semantic_projection(x) for x in v]
    return v
def semantic_fingerprint(v):
    raw=json.dumps(semantic_projection(v),ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return "sha256:"+hashlib.sha256(raw).hexdigest()
