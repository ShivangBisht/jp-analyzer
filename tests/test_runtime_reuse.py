from app.analyzer.config import AnalyzerConfig
from app.analyzer.runtime import get_runtime, reset_runtime_for_tests


def main():
    reset_runtime_for_tests()
    config = AnalyzerConfig()
    first = get_runtime(config)
    second = get_runtime()
    assert first is second
    try:
        get_runtime(AnalyzerConfig(ginza_split_mode="C"))
    except RuntimeError:
        pass
    else:
        raise AssertionError("Runtime accepted a conflicting configuration")
    reset_runtime_for_tests()
    print("runtime reuse tests passed")


if __name__ == "__main__":
    main()
