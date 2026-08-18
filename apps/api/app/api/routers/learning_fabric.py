from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.learning_fabric import (
    AgentMemoryCreate,
    AgentMemoryRead,
    MemoryVersionRead,
    MemoryProvenanceRead,
    MemoryCandidateRead,
    MemoryConflictRead,
    MemoryCorrectRequest,
    MemoryConflictResolveRequest
)
from app.services import learning_fabric_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext

router = APIRouter(prefix="/memory", tags=["Enterprise Agent Memory & Learning Fabric"])

@router.get("/search", response_model=List[AgentMemoryRead])
async def search_memories(
    query: Optional[str] = Query(None),
    type: Optional[str] = Query(None, alias="type"),
    scope: Optional[str] = Query(None, alias="scope"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Searches and ranks memories for context retrieval."""
    return await learning_fabric_service.search_memories(
        db, workspace_id=ws_ctx.workspace_id, query=query, memory_type=type, scope=scope
    )

@router.get("/review", response_model=List[MemoryCandidateRead])
async def list_candidates(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists unvalidated memory candidates in review queue."""
    return await learning_fabric_service.list_candidates(db, workspace_id=ws_ctx.workspace_id)

@router.get("/conflicts", response_model=List[MemoryConflictRead])
async def list_conflicts(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists unresolved memory conflicts."""
    return await learning_fabric_service.list_conflicts(db, workspace_id=ws_ctx.workspace_id)

@router.post("/conflicts/{conflict_id}/resolve", response_model=MemoryConflictRead)
async def resolve_conflict(
    conflict_id: str,
    req: MemoryConflictResolveRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Operator resolves a memory conflict."""
    return await learning_fabric_service.resolve_conflict(
        db, workspace_id=ws_ctx.workspace_id, conflict_id=conflict_id, req=req, user_id=ws_ctx.user_id
    )

@router.get("", response_model=List[AgentMemoryRead])
async def list_memories(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists active workspace memories."""
    return await learning_fabric_service.search_memories(db, workspace_id=ws_ctx.workspace_id)

@router.post("", response_model=AgentMemoryRead)
async def create_memory(
    req: AgentMemoryCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Creates a governed memory object."""
    mem, _ = await learning_fabric_service.create_memory(
        db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id
    )
    return mem

@router.get("/{memory_id}", response_model=AgentMemoryRead)
async def get_memory(
    memory_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Fetches memory details."""
    mem = await learning_fabric_service.get_memory(db, memory_id=memory_id)
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
    return mem

@router.get("/{memory_id}/history", response_model=List[MemoryVersionRead])
async def get_memory_history(
    memory_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns memory version history."""
    return await learning_fabric_service.get_history(db, memory_id=memory_id)

@router.get("/{memory_id}/evidence", response_model=MemoryProvenanceRead)
async def get_memory_evidence(
    memory_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns memory provenance and ground-truth evidence."""
    prov = await learning_fabric_service.get_provenance(db, memory_id=memory_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Provenance not found")
    return prov

@router.post("/{memory_id}/correct", response_model=AgentMemoryRead)
async def correct_memory(
    memory_id: str,
    req: MemoryCorrectRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Human correction updates memory and creates new version snapshot."""
    return await learning_fabric_service.correct_memory(
        db, memory_id=memory_id, req=req, user_id=ws_ctx.user_id
    )

@router.post("/{memory_id}/invalidate", response_model=AgentMemoryRead)
async def invalidate_memory(
    memory_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Marks memory as deprecated/invalidated."""
    return await learning_fabric_service.invalidate_memory(db, memory_id=memory_id)
