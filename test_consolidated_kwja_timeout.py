import inspect
from app.analyzer.layers.kwja import run_kwja as consolidated_run_kwja
from app.phase9.kwja_alpha1 import run_kwja as legacy_run_kwja


def main():
    consolidated = inspect.signature(consolidated_run_kwja).parameters["timeout_seconds"].default
    legacy = inspect.signature(legacy_run_kwja).parameters["timeout_seconds"].default
    assert consolidated == legacy == 300, (consolidated, legacy)
    print("Consolidated KWJA timeout test passed")


if __name__ == "__main__":
    main()
