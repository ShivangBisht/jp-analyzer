from copy import deepcopy
import hashlib
from app.analyzer.teaching_decision_record import build_teaching_decision_record
from app.analyzer.teaching_decision_store import persist_record,get_record,list_records,retract_record,supersede_record,integrity_report

S="黒い服を着た。"
def snap(seed="a"):
    import json
    from app.analyzer.analyzer_decision_snapshot import _digest
    # construct using real canonical rules
    content={"schemaVersion":"1.0","source":{"sentence":S,"sentenceSha256":hashlib.sha256(S.encode()).hexdigest(),"textLength":len(S)},"analyzerIdentity":{},"dictionaryIdentity":{},"fullAnalysis":{},"coreDecision":{"candidates":[],"decisions":[],"conflicts":[],"resolvedSpans":[],"selectedPartition":{}},"readerDecision":{"compatibilitySpans":[],"candidates":[],"selection":{},"selectedSpans":[{"start":0,"end":2,"surface":"黒い","displayRole":"lexical"},{"start":2,"end":len(S),"surface":S[2:],"displayRole":"unresolved"}]},"generationObservability":{},"correctionContext":{},"replayability":{}}
    d="sha256:"+_digest(content);return {"snapshotId":"ads-"+d.split(':')[1][:24],"capturedAt":"2026-07-30T00:00:00+00:00","contentDigest":d,**content}
def rec(snapshot,judgment="accepted-current",role="lexical",failure="accepted-current"):
    return build_teaching_decision_record(snapshot,boundary={"start":0,"end":2,"surface":"黒い"},judgment=judgment,classification={"assertedRole":role},approved_target={"displayRole":role} if judgment=="corrected" else None,failure_classification=failure)
def test_persist_get_dedupe_and_filters(tmp_path):
    db=tmp_path/'tdr.sqlite3';s=snap();r=rec(s);a=persist_record(r,snapshot=s,db_path=db);b=persist_record(r,db_path=db)
    assert a['recordId']==b['recordId']==get_record(r['recordId'],db_path=db)['recordId'];assert len(list_records(judgment='accepted-current',db_path=db))==1
    assert integrity_report(db)['ok']
def test_missing_snapshot_rejected(tmp_path):
    import pytest
    r=rec(snap())
    with pytest.raises(ValueError,match='not stored'):persist_record(r,db_path=tmp_path/'x.db')
def test_retract(tmp_path):
    db=tmp_path/'x.db';s=snap();r=rec(s);persist_record(r,snapshot=s,db_path=db)
    assert retract_record(r['recordId'],db_path=db)['lifecycle']['status']=='retracted'
def test_supersede(tmp_path):
    db=tmp_path/'x.db';s=snap();old=rec(s);persist_record(old,snapshot=s,db_path=db)
    new=rec(s,'corrected','grammar','role-error');res=supersede_record(old['recordId'],new,db_path=db)
    assert res['superseded']['lifecycle']['status']=='superseded';assert res['replacement']['lifecycle']['status']=='active'
