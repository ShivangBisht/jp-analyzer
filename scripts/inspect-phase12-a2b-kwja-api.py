from __future__ import annotations
import argparse,importlib,inspect,json,pkgutil
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);a=p.parse_args();import kwja
 modules=sorted(x.name for x in pkgutil.walk_packages(kwja.__path__,kwja.__name__+".")); rows=[]
 for name in modules:
  if not any(x in name for x in ("cli","module","reader")):continue
  try:m=importlib.import_module(name)
  except Exception as e: rows.append({"module":name,"importError":f"{type(e).__name__}: {e}"});continue
  symbols=[]
  for n in sorted(dir(m)):
   v=getattr(m,n)
   if n.startswith("_") or not (inspect.isclass(v) or inspect.isfunction(v)):continue
   if any(x in n.casefold() for x in ("module","writer","reader","predict","cli")):
    try:s=str(inspect.signature(v))
    except Exception:s=None
    symbols.append({"name":n,"kind":"class" if inspect.isclass(v) else "function","signature":s})
  if symbols:rows.append({"module":name,"symbols":symbols})
 out={"schema":"Phase12A2BKwjaApiInventory.v1","version":getattr(kwja,"__version__","unknown"),"modules":modules,"candidates":rows,"productionActivated":False};Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8",newline="\n");print("Created:",a.output)
if __name__=="__main__":main()
