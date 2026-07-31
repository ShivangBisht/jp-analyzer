from app.analyzer.teaching_controlled_activation import build_activation_plan,verify_activation_plan,simulate_shadow_observation

def experiment(passed=True):
 return {"schema":"TeachingOfflineExperiment.v1","passed":passed,"deploymentEnabled":False,"experimentId":"toe-test","artifactDigest":"sha256:"+"a"*64,"corpusDigest":"sha256:"+"b"*64}

def test_plan_is_shadow_only_and_deterministic():
 a=build_activation_plan(experiment());b=build_activation_plan(experiment())
 assert a["planDigest"]==b["planDigest"]
 assert a["mode"]=="shadow" and a["enabled"] is False
 assert a["liveMutationEnabled"] is False and a["automaticDeploymentEnabled"] is False
 assert verify_activation_plan(a)["ok"] is True

def test_nonpassing_experiment_is_rejected():
 import pytest
 with pytest.raises(ValueError): build_activation_plan(experiment(False))

def test_shadow_observation_never_applies_candidate():
 plan=build_activation_plan(experiment())
 baseline={"role":"term"};candidate={"role":"grammar"}
 result=simulate_shadow_observation(plan,baseline=baseline,candidate=candidate)
 assert result["different"] is True
 assert result["readerOutput"]==baseline
 assert result["candidateOutputApplied"] is False
 assert result["liveAnalyzerChanged"] is False
 assert result["dictionaryChanged"] is False

def test_verifier_rejects_live_mode_tampering():
 plan=build_activation_plan(experiment());plan["mode"]="live"
 assert verify_activation_plan(plan)["ok"] is False
