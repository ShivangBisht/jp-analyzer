import inspect

from app.analyzer.layers.kwja import run_kwja


def main():
    timeout = inspect.signature(run_kwja).parameters["timeout_seconds"].default
    assert timeout == 300, timeout
    print("KWJA timeout test passed")


if __name__ == "__main__":
    main()
