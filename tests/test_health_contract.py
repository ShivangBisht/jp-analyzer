from app.analyzer.health import health_report
from app.analyzer.version import ANALYZER_VERSION, ENGINE_CONTRACT_VERSION


class FakeRuntime:
    class Status:
        ginza_model = "ja_ginza"
        kwja = {"available": True, "modelSize": "base"}
        dictionary = {"ready": True, "entryCount": 10}

    def status(self):
        return self.Status()


def main():
    result = health_report(FakeRuntime())
    assert result["status"] == "ok"
    assert result["version"] == ANALYZER_VERSION
    assert result["engineVersion"] == ENGINE_CONTRACT_VERSION
    assert result["ginzaModel"] == "ja_ginza"
    assert result["kwja"]["available"] is True
    assert result["dictionary"]["ready"] is True
    print("health contract tests passed")


if __name__ == "__main__":
    main()
