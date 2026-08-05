from app.analyzer.health import liveness_report
from app.analyzer.performance import semantic_fingerprint
from app.startup.ownership import service_ok
def test_liveness_minimal():assert liveness_report()=={"status":"alive","service":"jp-analyzer"}
def test_liveness_no_runtime(monkeypatch):
 monkeypatch.setattr("app.analyzer.health.get_runtime",lambda:(_ for _ in ()).throw(AssertionError()))
 assert liveness_report()["status"]=="alive"
def test_liveness_identity(monkeypatch):
 v=type("R",(),{"ok":True,"body":{"status":"alive","service":"jp-analyzer"}})();monkeypatch.setattr("app.startup.ownership.probe",lambda *a,**k:v);assert service_ok("analyzer-liveness","x")
def test_fingerprint_ignores_timings_not_semantics():
 a={"readerSpans":[{"surface":"猫"}],"performanceDiagnostics":{"x":1}};b={"readerSpans":[{"surface":"猫"}],"performanceDiagnostics":{"x":2}};assert semantic_fingerprint(a)==semantic_fingerprint(b);b["readerSpans"][0]["surface"]="犬";assert semantic_fingerprint(a)!=semantic_fingerprint(b)
