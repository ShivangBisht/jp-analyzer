from app.analyzer.kwja_persistent_worker import InteractiveKwjaWorker

def test_worker_constructs_without_starting():
    worker = InteractiveKwjaWorker("kwja.exe")
    assert worker.process is None
    assert worker.model_size == "base"

def test_diagnostics_before_start():
    worker = InteractiveKwjaWorker("kwja.exe")
    assert worker.diagnostics()["running"] is False
