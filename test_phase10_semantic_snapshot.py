from copy import deepcopy
from app.analyzer.semantic_snapshot import semantic_snapshot, snapshot_digest

def main():
    base = {"text":"検証。", "resolved_spans_alpha2":[{"start":0,"end":2,"surface":"検証","role":"term","headword":"検証","confidence":.9},{"start":2,"end":3,"surface":"。","role":"punctuation","confidence":1.0}], "diagnostics_alpha2":[], "kwja_metadata_alpha1":{"source_alignment_complete":True,"elapsed_ms":123}, "dictionary_evidence_alpha34":{"dictionary_ready":True,"candidate_count":1,"matched_candidate_count":1,"unmatched_candidate_count":0}, "runtimeElapsedMs":10}
    changed = deepcopy(base); changed["runtimeElapsedMs"] = 999; changed["kwja_metadata_alpha1"]["elapsed_ms"] = 777
    assert semantic_snapshot(base) == semantic_snapshot(changed)
    assert snapshot_digest(semantic_snapshot(base)) == snapshot_digest(semantic_snapshot(changed))
    changed["resolved_spans_alpha2"][0]["role"] = "unresolved"
    assert semantic_snapshot(base) != semantic_snapshot(changed)
    print("Phase 10.2 semantic snapshot tests passed")
if __name__ == "__main__": main()
