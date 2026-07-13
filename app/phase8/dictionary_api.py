from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .dictionary_store import start_sync, add_batch, finish_sync, status, clear
router = APIRouter(prefix="/dictionary-sync", tags=["dictionary-sync"])
class StartRequest(BaseModel):
    expectedEntries: int = 0
    dictionaryCount: int = 0
class Entry(BaseModel):
    term: str
    reading: str = ""
    dictionaryId: str = ""
    dictionaryTitle: str = "unknown"
    dictionaryType: str = "term"
    dictionaryPriority: int = 9999
    tags: list[str] = Field(default_factory=list)
    rules: list[str] | str = Field(default_factory=list)
    score: float = 0
    sequence: str | int | None = None
    nameType: str = ""
    grammarType: str = ""
    expressionType: str = ""
class BatchRequest(BaseModel):
    syncId: str
    entries: list[Entry]
class FinishRequest(BaseModel):
    syncId: str
@router.post("/start")
def start(req: StartRequest): return start_sync(req.expectedEntries, req.dictionaryCount)
@router.post("/batch")
def batch(req: BatchRequest):
    try: return add_batch(req.syncId, [e.model_dump() for e in req.entries])
    except ValueError as exc: raise HTTPException(409, str(exc))
@router.post("/finish")
def finish(req: FinishRequest):
    try: return finish_sync(req.syncId)
    except ValueError as exc: raise HTTPException(409, str(exc))
@router.get("/status")
def get_status(): return status()
@router.delete("/cache")
def delete_cache(): return clear()
