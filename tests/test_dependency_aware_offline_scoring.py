from app.analyzer.teaching_offline_evaluation import _aggregate, _baseline, _score


def record():
    return {"judgment":"corrected","failureClassification":"candidate-generation-miss","assertions":{"boundary":{"start":18,"end":21,"surface":"ã ã£ãŸ"},"classification":{"assertedRole":"function"},"identity":None}}


def expected():
    return {"candidatePresent":True,"boundary":[18,21],"classification":"function","identity":None,"abstained":False,"partitionCorrect":True}


def test_missing_candidate_clears_dependent_predictions():
    value=_baseline(record())
    assert value=={"candidatePresent":False,"boundary":None,"classification":None,"identity":None,"abstained":False,"partitionCorrect":False}


def test_missing_candidate_scores_dependencies_as_not_applicable():
    scores=_score(expected(),_baseline(record()))
    assert scores=={"candidateGenerationRecall":0,"boundaryAccuracy":None,"classificationAccuracy":None,"identityAccuracy":None,"abstentionAccuracy":1,"partitionAccuracy":0}


def test_present_candidate_scores_all_dimensions():
    assert all(value==1 for value in _score(expected(),expected()).values())


def test_aggregate_excludes_not_applicable_values():
    empty={name:None for name in ("candidateGenerationRecall","boundaryAccuracy","classificationAccuracy","identityAccuracy","abstentionAccuracy","partitionAccuracy")}
    full={"candidateGenerationRecall":1,"boundaryAccuracy":1,"classificationAccuracy":0,"identityAccuracy":1,"abstentionAccuracy":1,"partitionAccuracy":1}
    result=_aggregate([{"scores":empty},{"scores":full}])
    assert result["recordCount"]==2
    assert result["metricCounts"]["boundaryAccuracy"]==1
    assert result["metrics"]["boundaryAccuracy"]==1.0
    assert result["metrics"]["classificationAccuracy"]==0.0
