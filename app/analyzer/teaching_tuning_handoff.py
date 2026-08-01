from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from .teaching_tuning_corpus import build_tuning_corpus_package, verify_tuning_corpus_package
from .teaching_corpus_governance import build_corpus_governance_report, verify_corpus_governance_report

TUNING_INPUT_SCHEMA = "TeachingTuningInput.v1"
CANDIDATE_SCHEMA = "AnalyzerCandidateArtifact.v1"
EVALUATION_SCHEMA = "AnalyzerCandidateEvaluation.v1"
HANDOFF_SCHEMA = "TeachingTuningHandoff.v1"


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def _finalize(core: dict[str, Any], *, id_prefix: str, id_key: str, digest_key: str) -> dict[str, Any]:
    digest = _digest(core)
    return {**core, id_key: id_prefix + digest.split(":", 1)[1][:24], digest_key: digest}


def _verify_digest(value: dict[str, Any], *, id_prefix: str, id_key: str, digest_key: str) -> list[str]:
    core = {k: v for k, v in value.items() if k not in {id_key, digest_key}}
    expected = _digest(core)
    problems = []
    if value.get(digest_key) != expected:
        problems.append(digest_key + "-mismatch")
    if value.get(id_key) != id_prefix + expected.split(":", 1)[1][:24]:
        problems.append(id_key + "-mismatch")
    return problems


def _identity_from_corpus(corpus: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    examples = corpus.get("examples") or []
    analyzer = {}
    if examples:
        analyzer = deepcopy(((examples[0].get("baseline") or {}).get("analyzerIdentity") or {}))
    dictionary = deepcopy(corpus.get("dictionaryIdentity") or {})
    return analyzer, dictionary


def build_tuning_input_contract(*, corpus: dict[str, Any] | None = None, governance: dict[str, Any] | None = None) -> dict[str, Any]:
    corpus = corpus or build_tuning_corpus_package("private-local")
    governance = governance or build_corpus_governance_report()
    corpus_verification = verify_tuning_corpus_package(corpus)
    governance_verification = verify_corpus_governance_report(governance)
    analyzer_identity, dictionary_identity = _identity_from_corpus(corpus)
    train_fit = bool(((governance.get("maturity") or {}).get("trainFit") or {}).get("passed"))
    blockers = []
    if not corpus_verification.get("ok"):
        blockers.append("corpus-package-invalid")
    if not governance_verification.get("ok"):
        blockers.append("governance-report-invalid")
    if not ((governance.get("maturity") or {}).get("harnessValid") or {}).get("passed"):
        blockers.append("harness-not-valid")
    if not train_fit:
        blockers.append("corpus-not-train-fit")
    core = {
        "schema": TUNING_INPUT_SCHEMA,
        "mode": "handoff-contract-only",
        "status": "ready" if not blockers else "blocked",
        "tuningEnabled": False,
        "candidateDerivationEnabled": False,
        "activationEnabled": False,
        "deploymentEnabled": False,
        "corpus": {"schema": corpus.get("schema"), "packageDigest": corpus.get("packageDigest"), "corpusDigest": corpus.get("corpusDigest"), "profile": corpus.get("profile"), "splitCounts": deepcopy(corpus.get("splitCounts") or {})},
        "governance": {"schema": governance.get("schema"), "reportDigest": governance.get("reportDigest"), "harnessValid": deepcopy((governance.get("maturity") or {}).get("harnessValid") or {}), "trainFit": deepcopy((governance.get("maturity") or {}).get("trainFit") or {}), "leakageFindings": int((governance.get("counts") or {}).get("leakageFindings") or 0)},
        "analyzerIdentity": analyzer_identity,
        "dictionaryIdentity": dictionary_identity,
        "partitionPolicy": {"train": "derivation-only", "validation": "selection-only", "test": "protected-final-evaluation-only", "testMayInfluenceDerivation": False, "testMayInfluenceSelection": False},
        "provenanceRequirements": {"noCrossSplitLeakage": True, "groupCount": int((governance.get("counts") or {}).get("provenanceGroups") or 0)},
        "reproducibility": {"canonicalJson": "UTF-8, sorted keys, compact separators", "digestAlgorithm": "SHA-256", "sourceContracts": [TUNING_INPUT_SCHEMA, str(corpus.get("schema")), str(governance.get("schema"))]},
        "blockers": blockers,
    }
    return _finalize(core, id_prefix="tti-", id_key="inputId", digest_key="inputDigest")


def verify_tuning_input_contract(value: dict[str, Any]) -> dict[str, Any]:
    problems = []
    if value.get("schema") != TUNING_INPUT_SCHEMA: problems.append("unsupported-schema")
    if value.get("mode") != "handoff-contract-only": problems.append("mode-invalid")
    for k in ("tuningEnabled", "candidateDerivationEnabled", "activationEnabled", "deploymentEnabled"):
        if value.get(k) is not False: problems.append(k + "-must-be-false")
    p = value.get("partitionPolicy") or {}
    if p.get("testMayInfluenceDerivation") is not False or p.get("testMayInfluenceSelection") is not False: problems.append("protected-test-policy-invalid")
    if value.get("status") == "ready" and value.get("blockers"): problems.append("ready-input-has-blockers")
    if value.get("status") == "ready" and not ((value.get("governance") or {}).get("trainFit") or {}).get("passed"): problems.append("invalid-train-fit-claim")
    problems += _verify_digest(value,id_prefix="tti-",id_key="inputId",digest_key="inputDigest")
    return {"ok": not problems, "problems": problems, "schema": TUNING_INPUT_SCHEMA, "inputDigest": value.get("inputDigest")}


def build_candidate_artifact(*, tuning_input: dict[str, Any], candidate_payload: dict[str, Any], derivation: dict[str, Any], rollback: dict[str, Any]) -> dict[str, Any]:
    verification = verify_tuning_input_contract(tuning_input)
    if not verification["ok"]: raise ValueError("invalid tuning input")
    if tuning_input.get("status") != "ready": raise ValueError("tuning input is blocked by corpus maturity")
    core = {"schema": CANDIDATE_SCHEMA, "mode": "candidate-artifact-only", "activationEnabled": False, "deploymentEnabled": False, "parentAnalyzerIdentity": deepcopy(tuning_input.get("analyzerIdentity") or {}), "parentDictionaryIdentity": deepcopy(tuning_input.get("dictionaryIdentity") or {}), "tuningInputDigest": tuning_input.get("inputDigest"), "corpusDigest": (tuning_input.get("corpus") or {}).get("corpusDigest"), "governanceReportDigest": (tuning_input.get("governance") or {}).get("reportDigest"), "derivation": deepcopy(derivation), "candidatePayload": deepcopy(candidate_payload), "candidatePayloadDigest": _digest(candidate_payload), "compatibility": {"analyzerIdentityPinned": True, "dictionaryIdentityPinned": True}, "rollback": deepcopy(rollback)}
    return _finalize(core,id_prefix="aca-",id_key="candidateId",digest_key="artifactDigest")


def verify_candidate_artifact(value: dict[str, Any]) -> dict[str, Any]:
    problems=[]
    if value.get("schema") != CANDIDATE_SCHEMA: problems.append("unsupported-schema")
    for k in ("activationEnabled","deploymentEnabled"):
        if value.get(k) is not False: problems.append(k+"-must-be-false")
    if value.get("candidatePayloadDigest") != _digest(value.get("candidatePayload")): problems.append("candidate-payload-digest-mismatch")
    comp=value.get("compatibility") or {}
    if comp.get("analyzerIdentityPinned") is not True or comp.get("dictionaryIdentityPinned") is not True: problems.append("compatibility-not-pinned")
    rb=value.get("rollback") or {}
    if not rb.get("artifactDigest") or not rb.get("restoreProcedure"): problems.append("rollback-metadata-incomplete")
    problems += _verify_digest(value,id_prefix="aca-",id_key="candidateId",digest_key="artifactDigest")
    return {"ok":not problems,"problems":problems,"schema":CANDIDATE_SCHEMA}


def build_candidate_evaluation(*, tuning_input: dict[str, Any], candidate: dict[str, Any], metrics: dict[str, Any], leakage: list[dict[str, Any]], regressions: list[dict[str, Any]], compatibility: dict[str, Any]) -> dict[str, Any]:
    if not verify_tuning_input_contract(tuning_input)["ok"]: raise ValueError("invalid tuning input")
    if not verify_candidate_artifact(candidate)["ok"]: raise ValueError("invalid candidate artifact")
    validation = deepcopy(metrics.get("validation") or {})
    test = deepcopy(metrics.get("test") or {})
    core={"schema":EVALUATION_SCHEMA,"mode":"evaluation-artifact-only","activationEnabled":False,"deploymentEnabled":False,"tuningInputDigest":tuning_input.get("inputDigest"),"candidateArtifactDigest":candidate.get("artifactDigest"),"stages":{"train":{"purpose":"fit-observation","metrics":deepcopy(metrics.get("train") or {})},"validation":{"purpose":"candidate-selection","metrics":validation,"passed":bool(validation.get("passed"))},"test":{"purpose":"protected-final-evaluation","metrics":test,"passed":bool(test.get("passed")),"claimed":bool(test.get("claimed"))}},"leakage":deepcopy(leakage),"regressions":deepcopy(regressions),"compatibility":deepcopy(compatibility),"shadowEligible":False,"deploymentEligible":False}
    core["shadowEligible"] = bool(validation.get("passed")) and bool(test.get("claimed")) and bool(test.get("passed")) and not leakage and not regressions and bool(compatibility.get("passed"))
    return _finalize(core,id_prefix="ace-",id_key="evaluationId",digest_key="evaluationDigest")


def verify_candidate_evaluation(value: dict[str, Any]) -> dict[str, Any]:
    problems=[]
    if value.get("schema") != EVALUATION_SCHEMA: problems.append("unsupported-schema")
    for k in ("activationEnabled","deploymentEnabled","deploymentEligible"):
        if value.get(k) is not False: problems.append(k+"-must-be-false")
    stages=value.get("stages") or {}; test=(stages.get("test") or {})
    if test.get("passed") and not test.get("claimed"): problems.append("test-passed-without-claim")
    if value.get("shadowEligible") and (value.get("leakage") or value.get("regressions") or not (value.get("compatibility") or {}).get("passed")): problems.append("invalid-shadow-eligibility")
    problems += _verify_digest(value,id_prefix="ace-",id_key="evaluationId",digest_key="evaluationDigest")
    return {"ok":not problems,"problems":problems,"schema":EVALUATION_SCHEMA}


def build_handoff_manifest(*, tuning_input: dict[str, Any], candidate: dict[str, Any] | None = None, evaluation: dict[str, Any] | None = None) -> dict[str, Any]:
    input_check=verify_tuning_input_contract(tuning_input)
    candidate_check=verify_candidate_artifact(candidate) if candidate else {"ok":False}
    evaluation_check=verify_candidate_evaluation(evaluation) if evaluation else {"ok":False}
    core={"schema":HANDOFF_SCHEMA,"mode":"handoff-manifest-only","activationEnabled":False,"deploymentEnabled":False,"tuningInput":{"id":tuning_input.get("inputId"),"digest":tuning_input.get("inputDigest"),"verified":input_check["ok"]},"candidateArtifact":{"id":candidate.get("candidateId") if candidate else None,"digest":candidate.get("artifactDigest") if candidate else None,"verified":candidate_check["ok"]},"evaluation":{"id":evaluation.get("evaluationId") if evaluation else None,"digest":evaluation.get("evaluationDigest") if evaluation else None,"verified":evaluation_check["ok"]},"stages":{"inputReady":tuning_input.get("status")=="ready" and input_check["ok"],"candidateDerived":candidate is not None,"validationEvaluated":bool(evaluation and ((evaluation.get("stages") or {}).get("validation") or {}).get("metrics")),"protectedTestEvaluated":bool(evaluation and ((evaluation.get("stages") or {}).get("test") or {}).get("claimed")),"shadowObserved":False,"deploymentApproved":False},"rollbackRequired":True,"notice":"Contract handoff only. No tuning, activation, or deployment occurred."}
    return _finalize(core,id_prefix="tth-",id_key="handoffId",digest_key="handoffDigest")


def verify_handoff_manifest(value: dict[str, Any]) -> dict[str, Any]:
    problems=[]
    if value.get("schema") != HANDOFF_SCHEMA: problems.append("unsupported-schema")
    for k in ("activationEnabled","deploymentEnabled"):
        if value.get(k) is not False: problems.append(k+"-must-be-false")
    if value.get("rollbackRequired") is not True: problems.append("rollback-required")
    stages=value.get("stages") or {}
    if stages.get("deploymentApproved") is not False: problems.append("deployment-must-not-be-approved")
    if stages.get("candidateDerived") and not (value.get("candidateArtifact") or {}).get("verified"): problems.append("candidate-not-verified")
    problems += _verify_digest(value,id_prefix="tth-",id_key="handoffId",digest_key="handoffDigest")
    return {"ok":not problems,"problems":problems,"schema":HANDOFF_SCHEMA}


def build_handoff_preview() -> dict[str, Any]:
    corpus=build_tuning_corpus_package("private-local")
    governance=build_corpus_governance_report()
    tuning_input=build_tuning_input_contract(corpus=corpus,governance=governance)
    manifest=build_handoff_manifest(tuning_input=tuning_input)
    return {"tuningInput":tuning_input,"inputVerification":verify_tuning_input_contract(tuning_input),"handoff":manifest,"handoffVerification":verify_handoff_manifest(manifest),"readiness":{"corpusPackageValid":verify_tuning_corpus_package(corpus)["ok"],"governanceValid":verify_corpus_governance_report(governance)["ok"],"harnessValid":bool((governance.get("maturity") or {}).get("harnessValid",{}).get("passed")),"trainFit":bool((governance.get("maturity") or {}).get("trainFit",{}).get("passed")),"candidateDerivation":"not-performed","validation":str((governance.get("maturity") or {}).get("validationPassed",{}).get("status")),"protectedTest":"not-claimed","deployment":"disabled"},"notice":"Preview only. No training, candidate derivation, analyzer mutation, dictionary mutation, activation, or deployment occurred."}
