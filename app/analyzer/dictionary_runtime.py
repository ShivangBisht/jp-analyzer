from .layers.dictionary import dictionary_ready, evaluate_analysis_candidates, evaluate_candidate
from .layers.dictionary_store import DB_PATH, status

def get_dictionary_status():
    result = dict(status())
    result["database"] = str(DB_PATH)
    return result

__all__ = ["DB_PATH", "dictionary_ready", "evaluate_analysis_candidates", "evaluate_candidate", "get_dictionary_status"]
