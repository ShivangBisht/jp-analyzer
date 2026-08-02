from __future__ import annotations
import os
import webbrowser
from pathlib import Path

def local_app_data_dir() -> Path:
    return Path(os.environ.get("LOCALAPPDATA", Path.home())) / "JapaneseNovelMiner"

def open_application(url: str) -> bool:
    return webbrowser.open(url, new=1, autoraise=True)
