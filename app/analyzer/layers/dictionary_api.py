from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from .dictionary_update_proxy import fetch_update_archive, fetch_update_metadata

from .dictionary_items import (
    add_batch as add_dictionary_item_batch,
    cancel_operation,
    finish_operation,
    management_status,
    remove_dictionary,
    start_operation,
    update_dictionary_metadata,
)

from .dictionary_store import (
    add_batch,
    cancel_sync,
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
    installedDictionaryCount: int
    registryEntryCount: int
    registryConsistent: bool
    installedDictionaries: list[dict[str, Any]]


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


@router.delete("/cache", status_code=410)
def delete_cache():
    raise HTTPException(
        status_code=410,
        detail={
            "code": "DICTIONARY_CLEAR_DISABLED",
            "message": (
                "Deleting the authoritative analyzer lexicon is disabled. "
                "Use dictionary-management install, update, replace, or remove operations instead."
            ),
        },
    )


class DictionaryItemStartRequest(BaseModel):
    mode: str
    dictionaryId: str
    stableIdentity: str
    displayTitle: str
    dictionaryType: str = "term"
    priority: int = 9999
    expectedEntries: int
    revision: str | None = None
    version: str | None = None
    contentDigest: str | None = None
    sourceUrl: str | None = None
    updateManifestUrl: str | None = None


class DictionaryItemBatchRequest(BaseModel):
    operationId: str
    entries: list[Entry]


class DictionaryItemOperationRequest(BaseModel):
    operationId: str


class DictionaryRemoveRequest(BaseModel):
    dictionaryId: str


@router.post("/item/start")
def start_dictionary_item(req: DictionaryItemStartRequest):
    try:
        return start_operation(req.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/item/batch")
def batch_dictionary_item(req: DictionaryItemBatchRequest):
    try:
        return add_dictionary_item_batch(
            req.operationId,
            [entry.model_dump() for entry in req.entries],
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/item/finish")
def finish_dictionary_item(req: DictionaryItemOperationRequest):
    try:
        return finish_operation(req.operationId)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/item/cancel")
def cancel_dictionary_item(req: DictionaryItemOperationRequest):
    try:
        return cancel_operation(req.operationId)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.delete("/item")
def delete_dictionary_item(req: DictionaryRemoveRequest):
    try:
        return remove_dictionary(req.dictionaryId)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/management/status")
def get_dictionary_management_status():
    return management_status()


class DictionaryMetadataUpdateRequest(BaseModel):
    dictionaryId: str
    stableIdentity: str | None = None
    displayTitle: str | None = None
    revision: str | None = None
    version: str | None = None
    contentDigest: str | None = None
    sourceUrl: str | None = None
    updateManifestUrl: str | None = None
    lastUpdateCheckAt: str | None = None
    lastUpdateStatus: str | None = None


@router.patch("/item/metadata")
def patch_dictionary_metadata(req: DictionaryMetadataUpdateRequest):
    try:
        payload = req.model_dump(exclude={"dictionaryId"}, exclude_unset=True)
        return update_dictionary_metadata(req.dictionaryId, payload)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


class DictionaryUpdateUrlRequest(BaseModel):
    url: str


@router.post("/update/check")
def analyzer_update_check(req: DictionaryUpdateUrlRequest):
    try:
        return fetch_update_metadata(req.url)
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/update/archive")
def analyzer_update_archive(req: DictionaryUpdateUrlRequest):
    try:
        content, metadata = fetch_update_archive(req.url)
        return Response(
            content=content,
            media_type="application/zip",
            headers={
                "X-Dictionary-Update-Route": metadata["route"],
                "X-Dictionary-Update-Size": str(metadata["sizeBytes"]),
                "Access-Control-Expose-Headers": "X-Dictionary-Update-Route,X-Dictionary-Update-Size",
            },
        )
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
