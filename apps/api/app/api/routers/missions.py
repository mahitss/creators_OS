from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.mission import (
    MissionCreate,
    MissionUpdate,
    MissionResponse,
    MissionListResponse,
)
from app.services import mission_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"
DEFAULT_USER_ID = "usr_alex_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> str:
    return x_user_id or DEFAULT_USER_ID

@router.get("/missions", response_model=MissionListResponse)
async def list_missions(
    status: Optional[str] = Query(None, description="Filter by status (active, draft, completed, archived)"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high, urgent)"),
    search: Optional[str] = Query(None, description="Text search in title or description"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionListResponse:
    items, total = await mission_service.list_workspace_missions(
        db, workspace_id, status_filter=status, priority_filter=priority, search_query=search
    )
    return MissionListResponse(
        missions=[MissionResponse(**m) for m in items],
        total=total
    )

@router.post("/missions", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission(
    payload: MissionCreate,
    workspace_id: str = Depends(get_current_workspace_id),
    user_id: str = Depends(get_current_user_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.create_mission(db, workspace_id, user_id, payload)
    return MissionResponse(**m)

@router.get("/missions/{id}", response_model=MissionResponse)
async def get_mission(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.get_mission_by_id(db, workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.patch("/missions/{id}", response_model=MissionResponse)
async def update_mission(
    id: str,
    payload: MissionUpdate,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.update_mission(db, workspace_id, id, payload)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.post("/missions/{id}/complete", response_model=MissionResponse)
async def complete_mission(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.complete_mission(db, workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.post("/missions/{id}/archive", response_model=MissionResponse)
async def archive_mission(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.archive_mission(db, workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)
