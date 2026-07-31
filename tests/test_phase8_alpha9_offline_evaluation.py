from app.analyzer.teaching_offline_evaluation import build_offline_experiment, verify_offline_experiment


def _corpus():
    records=[]
    for record_id, split, judgment, failure in [
        ("test-a", "test", "corrected", "boundary-error"),
        ("train-a", "train", "accepted-current", "accepted-current"),
        ("validation-a", "validation", "corrected", "role-error"),
    ]:
        records.append({
            "recordId": record_id,
            "recordDigest": "sha256:" + "a" * 64,
            "snapshotId": "ads-" + record_id,
            "judgment": judgment,
            "assertions": {"boundary": {"start": 0, "end": 1, "surface": "猫"}, "classification": {"assertedRole": "lexical"}},
            "approvedTarget": None,
            "failureClassification": failure,
            "split": split,
        })
    core={"schema":"TeachingCorpusExport.v1","mode":"dry-run","exportEnabled":False,"activationEnabled":False,"splitPolicy":{"train":80,"validation":10,"test":10},"eligibleRecords":records,"excludedRecords":[]}
    import hashlib,json
    core["eligibleCount"]=3;core["excludedCount"]=0;core["splitCounts"]={"train":1,"validation":1,"test":1}
    digest_payload={k:core[k] for k in ["schema","mode","exportEnabled","activationEnabled","splitPolicy","eligibleRecords","excludedRecords"]}
    core["corpusDigest"]="sha256:"+hashlib.sha256(json.dumps(digest_payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return core


def test_experiment_is_deterministic_and_nonactivating():
    first=build_offline_experiment(corpus=_corpus())
    second=build_offline_experiment(corpus=_corpus())
    assert first["artifactDigest"]==second["artifactDigest"]
    assert first["liveAnalyzerMutationEnabled"] is False
    assert first["dictionaryMutationEnabled"] is False
    assert first["deploymentEnabled"] is False
    assert verify_offline_experiment(first)["ok"] is True


def test_candidate_predictions_improve_validation_without_touching_test():
    prediction={"candidatePresent":True,"boundary":[0,1],"classification":"lexical","identity":None,"abstained":False,"partitionCorrect":True}
    result=build_offline_experiment(corpus=_corpus(),candidate_predictions={"validation-a":prediction})
    assert result["deltas"]["validation"]["classificationAccuracy"]==1.0
    assert result["deltas"]["test"]["boundaryAccuracy"]==0.0
    assert result["passed"] is True


def test_verifier_rejects_tampering():
    result=build_offline_experiment(corpus=_corpus())
    result["mode"]="live"
    assert verify_offline_experiment(result)["ok"] is False
