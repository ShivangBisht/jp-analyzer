from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .dictionary_store import (
    add_batch,
    cancel_sync,
    clear,
    finish_sync,
    recover_interrupted_syncs,
    start_sync,
    status,
)


router = APIRouter(
    prefix="/dictionary-sync",
    tags=["dictionary-sync"],
)


class StartRequest(BaseModel):
    expectedEntries: int
    dictionaryCount: int
    snapshotIdentity: str | None = None


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


class CancelRequest(BaseModel):
    syncId: str


class StartResponse(BaseModel):
    syncId: str
    status: str
    expectedEntries: int
    receivedEntries: int
    stagedEntries: int
    dictionaryCount: int
    stagedDictionaryCount: int
    snapshotIdentity: str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    completedAt: str | None = None
    errorCode: str | None = None
    errorMessage: str | None = None
    progress: float
    database: str


class BatchResponse(BaseModel):
    syncId: str
    accepted: int
    received: int
    expected: int
    staged: int
    progress: float
    status: str


class FinishResponse(BaseModel):
    syncId: str
    status: str
    entryCount: int
    dictionaryCount: int
    typeCounts: dict[str, int]
    snapshotIdentity: str | None = None
    completedAt: str


class SessionResponse(BaseModel):
    syncId: str
    status: str
    expectedEntries: int
    receivedEntries: int
    stagedEntries: int
    dictionaryCount: int
    stagedDictionaryCount: int
    snapshotIdentity: str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    completedAt: str | None = None
    errorCode: str | None = None
    errorMessage: str | None = None
    progress: float


class RecoveryResponse(BaseModel):
    status: str
    recoveredCount: int
    recoveredSyncIds: list[str]
    cleanedTerminalCount: int
    cleanedTerminalSyncIds: list[str]
    database: str


class DictionaryStatusResponse(BaseModel):
    ready: bool
    entryCount: int
    dictionaryCount: int
    typeCounts: dict[str, int]
    lastSyncId: str | None = None
    snapshotIdentity: str | None = None
    lastSyncCompletedAt: str | None = None
    database: str
    activeSession: dict[str, Any] | None = None
    lastCompletedSession: dict[str, Any] | None = None
    lastProblemSession: dict[str, Any] | None = None
    stagedEntryCount: int
    recoveryRequired: bool


@router.post(
    "/start",
    response_model=StartResponse,
)
def start(req: StartRequest):
    try:
        return start_sync(
            req.expectedEntries,
            req.dictionaryCount,
            req.snapshotIdentity,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@router.post(
    "/batch",
    response_model=BatchResponse,
)
def batch(req: BatchRequest):
    try:
        return add_batch(
            req.syncId,
            [entry.model_dump() for entry in req.entries],
        )
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error


@router.post(
    "/finish",
    response_model=FinishResponse,
)
def finish(req: FinishRequest):
    try:
        return finish_sync(req.syncId)
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error


@router.post(
    "/cancel",
    response_model=SessionResponse,
)
def cancel(req: CancelRequest):
    try:
        return cancel_sync(req.syncId)
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error


@router.post(
    "/recover",
    response_model=RecoveryResponse,
)
def recover():
    return recover_interrupted_syncs()


@router.get(
    "/status",
    response_model=DictionaryStatusResponse,
)
def get_status():
    return status()


@router.delete(
    "/cache",
    response_model=DictionaryStatusResponse,
)
def delete_cache():
    return clear()
