import copy
import pytest
from app.analyzer.teaching_tuning_handoff import (
    build_tuning_input_contract, verify_tuning_input_contract,
    build_candidate_artifact, verify_candidate_artifact,
    build_candidate_evaluation, verify_candidate_evaluation,
    build_handoff_manifest, verify_handoff_manifest,
)

def corpus():
    return {"schema":"TeachingTuningCorpus.v1","profile":"private-local","packageDigest":"sha256:"+"a"*64,"corpusDigest":"sha256:"+"b"*64,"splitCounts":{"train":8,"validation":2,"test":2},"dictionaryIdentity":{"identityDigest":"sha256:"+"c"*64},"examples":[{"baseline":{"analyzerIdentity":{"analyzerVersion":"test"}}}]}

def governance(train_fit=True):
    return {"schema":"TeachingCorpusGovernance.v1","reportDigest":"sha256:"+"d"*64,"maturity":{"harnessValid":{"passed":True},"trainFit":{"passed":train_fit}},"counts":{"leakageFindings":0,"provenanceGroups":3}}

def test_current_insufficient_corpus_is_blocked(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_tuning_corpus_package", lambda value: {"ok": True})
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_corpus_governance_report", lambda value: {"ok": True})
    value=build_tuning_input_contract(corpus=corpus(),governance=governance(False))
    assert value["status"]=="blocked"
    assert "corpus-not-train-fit" in value["blockers"]
    assert value["candidateDerivationEnabled"] is False
    assert verify_tuning_input_contract(value)["ok"]

def test_ready_input_candidate_evaluation_and_handoff_are_deterministic(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_tuning_corpus_package", lambda value: {"ok": True})
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_corpus_governance_report", lambda value: {"ok": True})
    t=build_tuning_input_contract(corpus=corpus(),governance=governance(True))
    c=build_candidate_artifact(tuning_input=t,candidate_payload={"weights":[1,2]},derivation={"seed":7},rollback={"artifactDigest":"sha256:"+"e"*64,"restoreProcedure":"restore baseline"})
    e=build_candidate_evaluation(tuning_input=t,candidate=c,metrics={"train":{},"validation":{"passed":True},"test":{"claimed":True,"passed":True}},leakage=[],regressions=[],compatibility={"passed":True})
    h=build_handoff_manifest(tuning_input=t,candidate=c,evaluation=e)
    assert verify_candidate_artifact(c)["ok"]
    assert verify_candidate_evaluation(e)["ok"]
    assert verify_handoff_manifest(h)["ok"]
    assert h["deploymentEnabled"] is False and h["stages"]["deploymentApproved"] is False
    assert h["handoffDigest"]==build_handoff_manifest(tuning_input=t,candidate=c,evaluation=e)["handoffDigest"]

def test_blocked_input_cannot_derive_candidate(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_tuning_corpus_package", lambda value: {"ok": True})
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_corpus_governance_report", lambda value: {"ok": True})
    t=build_tuning_input_contract(corpus=corpus(),governance=governance(False))
    with pytest.raises(ValueError):
        build_candidate_artifact(tuning_input=t,candidate_payload={},derivation={},rollback={})

def test_tampering_and_invalid_claims_are_rejected(monkeypatch):
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_tuning_corpus_package", lambda value: {"ok": True})
    monkeypatch.setattr("app.analyzer.teaching_tuning_handoff.verify_corpus_governance_report", lambda value: {"ok": True})
    t=build_tuning_input_contract(corpus=corpus(),governance=governance(True))
    bad=copy.deepcopy(t); bad["deploymentEnabled"]=True
    assert not verify_tuning_input_contract(bad)["ok"]
    c=build_candidate_artifact(tuning_input=t,candidate_payload={"x":1},derivation={},rollback={"artifactDigest":"sha256:"+"f"*64,"restoreProcedure":"restore"})
    c["candidatePayload"]["x"]=2
    assert not verify_candidate_artifact(c)["ok"]
