from __future__ import annotations
import hashlib, json

def _span(item):
    return {"start":item.get("start"), "end":item.get("end"), "surface":item.get("surface"), "role":item.get("role"), "headword":item.get("headword"), "grammarId":item.get("grammar_id"), "confidence":item.get("confidence"), "sourceLayer":item.get("source_layer")}

def semantic_snapshot(result):
    text = result.get("text", "")
    resolved = result.get("resolved_spans_alpha2") or []
    dictionary = result.get("dictionary_evidence_alpha34") or {}
    metadata = result.get("kwja_metadata_alpha1") or {}
    diagnostics = result.get("diagnostics_alpha2") or []
    return {"contractVersion":"1.0", "textSha256":hashlib.sha256(text.encode("utf-8")).hexdigest(), "textLength":len(text), "resolvedSpans":[_span(x) for x in resolved], "unresolvedSpans":[_span(x) for x in resolved if x.get("role") == "unresolved"], "diagnostics":[{"severity":x.get("severity"), "code":x.get("code"), "start":x.get("start"), "end":x.get("end")} for x in diagnostics], "kwjaAlignmentComplete":bool(metadata.get("source_alignment_complete")), "dictionarySummary":{"ready":dictionary.get("dictionary_ready"), "candidateCount":dictionary.get("candidate_count"), "matchedCandidateCount":dictionary.get("matched_candidate_count"), "unmatchedCandidateCount":dictionary.get("unmatched_candidate_count"), "typeEvidenceCounts":dictionary.get("dictionary_type_evidence_counts") or {}}}

def snapshot_digest(snapshot):
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
