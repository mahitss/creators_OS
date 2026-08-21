from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryListResponse,
    MemorySearchRequest,
    MemorySearchResponse,
    MemoryCandidateResponse,
    MemoryCandidateListResponse,
)
from app.services import memory_service

router = APIRouter()

@router.post("/memory/search", response_model=MemorySearchResponse)
@router.post("/memories/search", response_model=MemorySearchResponse)
async def search_memories(
    payload: MemorySearchRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemorySearchResponse:
    items = await memory_service.retrieve_relevant_memories(
        session=db,
        workspace_id=ws_ctx.workspace_id,
        query_context=payload.query,
        limit=payload.limit or 5,
        type_filter=payload.type_filter
    )
    return MemorySearchResponse(
        memories=[MemoryResponse(**m) for m in items],
        count=len(items),
        query=payload.query
    )

@router.post("/memory", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
@router.post("/memories", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    payload: MemoryCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.create_memory(db, ws_ctx.workspace_id, payload, created_by=ws_ctx.user_id)
    return MemoryResponse(**mem)

@router.get("/memory/{id}", response_model=MemoryResponse)
@router.get("/memories/{id}", response_model=MemoryResponse)
async def get_memory(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.get_memory_by_id(db, ws_ctx.workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.delete("/memory/{id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/memories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory_singular(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
):
    success = await memory_service.delete_memory(db, ws_ctx.workspace_id, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )

@router.patch("/memories/{id}", response_model=MemoryResponse)
async def update_memory(
    id: str,
    payload: MemoryUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.update_memory(db, ws_ctx.workspace_id, id, payload)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memories/{id}/archive", response_model=MemoryResponse)
async def archive_memory(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.archive_memory(db, ws_ctx.workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memories/candidates", status_code=status.HTTP_201_CREATED)
async def propose_memory_candidate(
    payload: dict,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    try:
        cand = await knowledge_service.propose_memory_candidate(
            db, workspace_id=ws_ctx.workspace_id, owner_id=ws_ctx.user_id, statement=payload.get("statement", ""),
            type_name=payload.get("type_name", "fact"), scope=payload.get("scope", "workspace"),
            source_references=payload.get("source_references", []), confidence=payload.get("confidence", 1.0),
            reason=payload.get("reason", ""), mission_id=payload.get("mission_id")
        )
        return cand
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/memories/candidates/{id}/approve")
async def approve_memory_candidate(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    try:
        mem = await knowledge_service.approve_memory_candidate(db, ws_ctx.workspace_id, id, ws_ctx.user_id)
        return mem
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/memories/conflicts")
async def list_memory_conflicts(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    return await knowledge_service.list_memory_conflicts(db, ws_ctx.workspace_id)

@router.post("/memories/conflicts/{id}/resolve")
async def resolve_memory_conflict(
    id: str,
    payload: dict,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    choice = payload.get("choice", "keep_a")
    try:
        return await knowledge_service.resolve_memory_conflict(db, ws_ctx.workspace_id, id, choice, ws_ctx.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/memories/{id}/provenance")
async def get_memory_provenance(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    try:
        return await knowledge_service.get_memory_provenance(db, ws_ctx.workspace_id, id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post("/memories/{id}/stale")
async def mark_memory_stale(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    mem = await memory_service.get_memory_by_id(db, ws_ctx.workspace_id, id)
    if not mem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found.")
    mem["status"] = "stale"
    return mem

@router.post("/memories/{id}/restore", response_model=MemoryResponse)
async def restore_memory(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.restore_memory(db, ws_ctx.workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.delete("/memories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
):
    success = await memory_service.delete_memory(db, ws_ctx.workspace_id, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )

# Candidates Endpoints
@router.get("/memory-candidates", response_model=MemoryCandidateListResponse)
async def list_candidates(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryCandidateListResponse:
    items, total = await memory_service.list_candidates(db, ws_ctx.workspace_id)
    return MemoryCandidateListResponse(
        candidates=[MemoryCandidateResponse(**c) for c in items],
        total=total
    )

@router.post("/memory-candidates/{id}/approve", response_model=MemoryResponse)
async def approve_candidate(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.approve_candidate(db, ws_ctx.workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memory-candidates/{id}/reject", status_code=status.HTTP_204_NO_CONTENT)
async def reject_candidate(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
):
    success = await memory_service.reject_candidate(db, ws_ctx.workspace_id, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate memory not found in active workspace."
        )
