from __future__ import annotations
from app.analyzer.layers.dictionary_update_proxy import _validate_url

def reject(url):
    try: _validate_url(url)
    except ValueError: return
    raise AssertionError(f"Expected URL rejection: {url}")

def run():
    reject("http://github.com/example")
    reject("https://localhost/test")
    reject("https://127.0.0.1/test")
    checked = _validate_url("https://github.com/yomidevs/jmdict-yomitan")
    assert checked.startswith("https://github.com/")
    print("dictionary update proxy safety tests passed")
if __name__ == "__main__": run()
