from pathlib import Path
from app.startup.supervisor import shutdown_requested

def test_shutdown_request_contract(tmp_path: Path):
    request = tmp_path / "shutdown.request"
    assert shutdown_requested(request) is False
    request.write_text("requested", encoding="utf-8")
    assert shutdown_requested(request) is True

def test_windows_launchers_are_hidden_and_local():
    root = Path(__file__).resolve().parents[1]
    normal = (root / "Japanese Novel Miner.vbs").read_text(encoding="utf-8-sig")
    diagnostics = (root / "Japanese Novel Miner - Diagnostics.vbs").read_text(encoding="utf-8-sig")
    stop = (root / "Japanese Novel Miner - Stop.vbs").read_text(encoding="utf-8-sig")
    assert "pythonw.exe" in normal and ", 0, False" in normal
    assert "open_japanese_novel_miner_diagnostics.pyw" in diagnostics
    assert "stop_japanese_novel_miner.pyw" in stop
    assert "Stop-Process" not in stop and "taskkill" not in stop
