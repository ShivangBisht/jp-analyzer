from copy import deepcopy

from app.analyzer.analyzer_decision_snapshot import (
    build_analyzer_decision_snapshot,
    validate_analyzer_decision_snapshot,
)
from app.analyzer.compact_output import compact_analysis


def fixture():
    text = "電子書籍。"
    candidates = [
        {"candidate_id":"c1","start":0,"end":2,"surface":"電子","proposed_role":"term","candidate_family":"term","headword":"電子","grammar_id":None,"confidence":.8,"protected":False,"source_layer":"lexical","source_annotation_id":"l1","morpheme_ids":["m1"],"dictionary_evidence":{"matched":True,"dictionary_type_counts":{"term":1},"independent_source_count":1},"evidence":[],"utility_dimensions":[100,60,70,59,30,80],"utility_score":121503082},
        {"candidate_id":"c2","start":2,"end":4,"surface":"書籍","proposed_role":"term","candidate_family":"term","headword":"書籍","grammar_id":None,"confidence":.8,"protected":False,"source_layer":"lexical","source_annotation_id":"l2","morpheme_ids":["m2"],"dictionary_evidence":{"matched":True,"dictionary_type_counts":{"term":1},"independent_source_count":1},"evidence":[],"utility_dimensions":[100,60,70,59,30,80],"utility_score":121503082},
        {"candidate_id":"c3","start":4,"end":5,"surface":"。","proposed_role":"punctuation","candidate_family":"punctuation","headword":None,"grammar_id":None,"confidence":1.0,"protected":True,"source_layer":"orthography","source_annotation_id":"o1","morpheme_ids":["m3"],"dictionary_evidence":{"matched":False},"evidence":[],"utility_dimensions":[100,100,85,73,0,100],"utility_score":10085073101},
    ]
    spans = [
        {"start":0,"end":2,"surface":"電子","role":"term","headword":"電子","grammar_id":None,"confidence":.8,"selected_candidate_id":"c1","source_layer":"lexical"},
        {"start":2,"end":4,"surface":"書籍","role":"term","headword":"書籍","grammar_id":None,"confidence":.8,"selected_candidate_id":"c2","source_layer":"lexical"},
        {"start":4,"end":5,"surface":"。","role":"punctuation","headword":None,"grammar_id":None,"confidence":1.0,"selected_candidate_id":"c3","source_layer":"orthography"},
    ]
    return {"version":"9.0.0-alpha2.2-evidence-gated-decision","text":text,"morphemes":[],"resolver_candidates_alpha2":candidates,"resolver_decisions_alpha2":[],"resolver_conflicts_alpha2":[],"resolved_spans_alpha2":spans,"diagnostics_alpha2":[],"kwja_metadata_alpha1":{"source_alignment_complete":True},"alpha2_change_summary":{}}


def dictionary_status():
    return {"ready":True,"snapshotIdentity":"dict-a","lastSyncId":"sync-a","entryCount":10,"dictionaryCount":2,"typeCounts":{"term":10},"registryEntryCount":10,"registryConsistent":True}


def test_snapshot_is_correction_free_deterministic_and_valid():
    full = fixture()
    snapshot = build_analyzer_decision_snapshot(full, captured_at="2026-07-30T00:00:00+00:00", dictionary_status_fn=dictionary_status, analyzer_version="test")
    validate_analyzer_decision_snapshot(snapshot)
    assert snapshot["snapshotId"].startswith("ads-")
    assert snapshot["readerDecision"]["selection"]["appliedCorrectionCount"] == 0
    assert snapshot["correctionContext"]["operationalCorrectionApplication"] == "disabled-for-snapshot"
    assert snapshot["coreDecision"]["selectedPartition"]["totalUtilityScore"] == sum(x["utility_score"] for x in full["resolver_candidates_alpha2"])
    assert all(x["candidateFingerprint"].startswith("sha256:") for x in snapshot["coreDecision"]["candidates"])
    again = build_analyzer_decision_snapshot(full, captured_at="later", dictionary_status_fn=dictionary_status, analyzer_version="test")
    assert again["snapshotId"] == snapshot["snapshotId"]
    assert again["contentDigest"] == snapshot["contentDigest"]


def test_default_compact_output_is_unchanged_by_snapshot_option():
    full = fixture()
    before = compact_analysis(full, analyzer_version="test")
    after = compact_analysis(full, analyzer_version="test", apply_corrections=True)
    assert before == after
    raw = compact_analysis(full, analyzer_version="test", apply_corrections=False)
    assert raw["readerSpans"] == before["readerSpans"]
    assert raw["readerSelection"]["correctionApplication"] == "disabled-for-snapshot"
    assert "compatibilityReaderSpans" in raw


def test_validation_detects_mutation():
    snapshot = build_analyzer_decision_snapshot(fixture(), captured_at="x", dictionary_status_fn=dictionary_status, analyzer_version="test")
    broken = deepcopy(snapshot)
    broken["readerDecision"]["selectedSpans"][0]["surface"] = "壊"
    try:
        validate_analyzer_decision_snapshot(broken)
    except ValueError:
        pass
    else:
        raise AssertionError("mutated snapshot accepted")
