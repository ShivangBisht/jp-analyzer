from __future__ import annotations
import tempfile
from pathlib import Path
import app.analyzer.reader_corrections as rc

def base():
    return [
      {"start":0,"end":2,"surface":"頷い","displayRole":"lexical","knownLookupKey":"頷く","frequencyLookupKey":"頷く"},
      {"start":2,"end":3,"surface":"て","displayRole":"function"},
      {"start":3,"end":4,"surface":"。","displayRole":"punctuation"},
    ]
def main():
    with tempfile.TemporaryDirectory() as d:
      rc.DB_PATH=Path(d)/"corrections.sqlite3"
      data={"sentence":"頷いて。","start":0,"end":3,"surface":"頷いて","displayRole":"lexical","headword":"頷く","knownLookupKey":"頷く","frequencyLookupKey":"頷く","scope":"occurrence"}
      before=base(); p=rc.preview(data,before)
      assert p["saved"] is False and len(p["previewReaderSpans"])==2
      assert not rc.DB_PATH.exists()
      s=rc.save(data,before,"test","1.0"); assert s["saved"] is True
      rows=rc.list_corrections(); assert len(rows)==1 and rows[0]["surface"]=="頷いて"
      rc.deactivate(s["correctionId"]); assert rc.list_corrections()==[]
      assert len(rc.list_corrections(True))==1
      bad=dict(data,start=1,surface="いて")
      try: rc.preview(bad,before)
      except ValueError: pass
      else: raise AssertionError("partial-span correction accepted")
    print("reader correction backend tests passed")
if __name__=="__main__": main()
