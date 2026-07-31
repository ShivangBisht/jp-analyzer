from __future__ import annotations
import hashlib, json
from typing import Any

ACTIVATION_SCHEMA = "TeachingControlledActivation.v1"
ALLOWED_MODE = "shadow"

def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()

def build_activation_plan(experiment: dict[str, Any]) -> dict[str, Any]:
    if experiment.get("schema") != "TeachingOfflineExperiment.v1":
        raise ValueError("verified TeachingOfflineExperiment.v1 is required")
    if experiment.get("passed") is not True:
        raise ValueError("only a passing offline experiment can create a shadow plan")
    if experiment.get("deploymentEnabled") is not False:
        raise ValueError("source experiment must have deployment disabled")
    core = {
        "schema": ACTIVATION_SCHEMA,
        "mode": ALLOWED_MODE,
        "enabled": False,
        "liveMutationEnabled": False,
        "automaticDeploymentEnabled": False,
        "rollbackRequired": True,
        "experimentId": experiment.get("experimentId"),
        "experimentDigest": experiment.get("artifactDigest"),
        "corpusDigest": experiment.get("corpusDigest"),
        "compatibility": {
            "experimentVerified": True,
            "dictionaryIdentityPinned": True,
            "analyzerIdentityPinned": True,
            "rollbackArtifactPresent": True,
        },
        "featureFlag": "TEACHING_SHADOW_ACTIVATION",
        "featureFlagRequiredValue": "enabled",
        "shadowPolicy": {
            "observeOnly": True,
            "readerOutputUnchanged": True,
            "operationalCorrectionsUnchanged": True,
            "metricsOnly": True,
        },
        "rollback": {
            "action": "discard-shadow-plan",
            "restoresAnalyzerState": "unchanged",
            "restoresDictionaryState": "unchanged",
        },
    }
    digest = _digest(core)
    return {**core, "planId": "tca-" + digest.split(":",1)[1][:24], "planDigest": digest}

def verify_activation_plan(plan: dict[str, Any]) -> dict[str, Any]:
    problems=[]
    if plan.get("schema") != ACTIVATION_SCHEMA: problems.append("unsupported-schema")
    if plan.get("mode") != ALLOWED_MODE: problems.append("mode-must-be-shadow")
    for key in ("enabled","liveMutationEnabled","automaticDeploymentEnabled"):
        if plan.get(key) is not False: problems.append(key+"-must-remain-false")
    if plan.get("rollbackRequired") is not True: problems.append("rollback-required")
    policy=plan.get("shadowPolicy") or {}
    if policy.get("observeOnly") is not True or policy.get("readerOutputUnchanged") is not True: problems.append("shadow-policy-invalid")
    compatibility=plan.get("compatibility") or {}
    for key in ("experimentVerified","dictionaryIdentityPinned","analyzerIdentityPinned","rollbackArtifactPresent"):
        if compatibility.get(key) is not True: problems.append("compatibility:"+key)
    core={k:v for k,v in plan.items() if k not in {"planId","planDigest"}}
    expected=_digest(core)
    if plan.get("planDigest") != expected: problems.append("plan-digest-mismatch")
    if plan.get("planId") != "tca-"+expected.split(":",1)[1][:24]: problems.append("plan-id-mismatch")
    return {"ok":not problems,"problems":problems,"schema":ACTIVATION_SCHEMA}

def simulate_shadow_observation(plan: dict[str, Any], *, baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    verification=verify_activation_plan(plan)
    if not verification["ok"]: raise ValueError("invalid shadow plan: "+", ".join(verification["problems"]))
    observation={
        "planId":plan["planId"],
        "mode":"shadow",
        "baselineDigest":_digest(baseline),
        "candidateDigest":_digest(candidate),
        "different":baseline != candidate,
        "readerOutput":baseline,
        "candidateOutputApplied":False,
        "liveAnalyzerChanged":False,
        "dictionaryChanged":False,
    }
    return {**observation,"observationDigest":_digest(observation)}
