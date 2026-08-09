from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryListResponse,
    MemoryCandidateResponse,
    MemoryCandidateListResponse,
)
from app.services import memory_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/memories", response_model=MemoryListResponse)
async def list_memories(
    type: Optional[str] = Query(None, description="Filter by memory type"),
    importance: Optional[str] = Query(None, description="Filter by importance"),
    search: Optional[str] = Query(None, description="Text search in title or content"),
    archived: bool = Query(False, description="Include archived memories"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryListResponse:
    items, total = await memory_service.list_memories(
        db, workspace_id, type_filter=type, importance_filter=importance, search_query=search, is_archived=archived
    )
    return MemoryListResponse(
        memories=[MemoryResponse(**m) for m in items],
        total=total
    )

@router.post("/memories", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    payload: MemoryCreate,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.create_memory(db, workspace_id, payload)
    return MemoryResponse(**mem)

@router.get("/memories/{id}", response_model=MemoryResponse)
async def get_memory(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.get_memory_by_id(db, workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.patch("/memories/{id}", response_model=MemoryResponse)
async def update_memory(
    id: str,
    payload: MemoryUpdate,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.update_memory(db, workspace_id, id, payload)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memories/{id}/archive", response_model=MemoryResponse)
async def archive_memory(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.archive_memory(db, workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memories/candidates", status_code=status.HTTP_201_CREATED)
async def propose_memory_candidate(
    payload: dict,
    x_user_id: Optional[str] = Header(None),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    user_id = x_user_id or "usr_alex"
    try:
        cand = await knowledge_service.propose_memory_candidate(
            db, workspace_id=workspace_id, owner_id=user_id, statement=payload.get("statement", ""),
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
    x_user_id: Optional[str] = Header(None),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    user_id = x_user_id or "usr_alex"
    try:
        mem = await knowledge_service.approve_memory_candidate(db, workspace_id, id, user_id)
        return mem
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/memories/conflicts")
async def list_memory_conflicts(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    return await knowledge_service.list_memory_conflicts(db, workspace_id)

@router.post("/memories/conflicts/{id}/resolve")
async def resolve_memory_conflict(
    id: str,
    payload: dict,
    x_user_id: Optional[str] = Header(None),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    user_id = x_user_id or "usr_alex"
    choice = payload.get("choice", "keep_a")
    try:
        return await knowledge_service.resolve_memory_conflict(db, workspace_id, id, choice, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/memories/{id}/provenance")
async def get_memory_provenance(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    from app.services import knowledge_service
    try:
        return await knowledge_service.get_memory_provenance(db, workspace_id, id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post("/memories/{id}/stale")
async def mark_memory_stale(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
):
    mem = await memory_service.get_memory_by_id(db, workspace_id, id)
    if not mem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found.")
    mem["status"] = "stale"
    return mem


@router.post("/memories/{id}/restore", response_model=MemoryResponse)
async def restore_memory(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.restore_memory(db, workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.delete("/memories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
):
    success = await memory_service.delete_memory(db, workspace_id, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found in active workspace."
        )

# Candidates Endpoints
@router.get("/memory-candidates", response_model=MemoryCandidateListResponse)
async def list_candidates(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryCandidateListResponse:
    items, total = await memory_service.list_candidates(db, workspace_id)
    return MemoryCandidateListResponse(
        candidates=[MemoryCandidateResponse(**c) for c in items],
        total=total
    )

@router.post("/memory-candidates/{id}/approve", response_model=MemoryResponse)
async def approve_candidate(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MemoryResponse:
    mem = await memory_service.approve_candidate(db, workspace_id, id)
    if not mem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate memory not found in active workspace."
        )
    return MemoryResponse(**mem)

@router.post("/memory-candidates/{id}/reject", status_code=status.HTTP_204_NO_CONTENT)
async def reject_candidate(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
):
    success = await memory_service.reject_candidate(db, workspace_id, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate memory not found in active workspace."
        )
