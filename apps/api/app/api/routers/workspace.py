from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, require_admin, WorkspaceContext, AuthenticatedUser, get_current_user
from app.services import workspace_service

router = APIRouter()

class WorkspaceSummary(BaseModel):
    id: str
    name: str
    root_path: str

class InviteMemberPayload(BaseModel):
    email: str = Field(..., description="Email address to invite")
    role: str = Field("member", description="Role: owner, admin, member, viewer")

class AcceptInvitationPayload(BaseModel):
    token: str = Field(..., description="Invitation token string")

class UpdateRolePayload(BaseModel):
    role: str = Field(..., description="New role: owner, admin, member, viewer")

@router.get("/workspaces", response_model=List[WorkspaceSummary])
async def list_workspaces(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[WorkspaceSummary]:
    from app.services import identity_service
    user_workspaces = await identity_service.get_user_workspaces(db, user.id)
    if user_workspaces:
        return [
            WorkspaceSummary(
                id=w["id"],
                name=w["name"],
                root_path="c:\\Users\\pc\\OneDrive\\Desktop\\Hack vibe"
            ) for w in user_workspaces
        ]
    return [
        WorkspaceSummary(
            id=user.workspace_id,
            name="Vapor Core Engine",
            root_path="c:\\Users\\pc\\OneDrive\\Desktop\\Hack vibe"
        )
    ]

@router.get("/workspaces/{id}/members")
async def list_workspace_members(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    if ws_ctx.workspace_id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-workspace access denied.")
    return await workspace_service.list_workspace_members(db, id)

@router.post("/workspaces/{id}/invitations", status_code=status.HTTP_201_CREATED)
async def invite_member(
    id: str,
    payload: InviteMemberPayload,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    if ws_ctx.workspace_id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-workspace access denied.")
    try:
        inv = await workspace_service.invite_workspace_member(db, id, email=payload.email, role=payload.role, invited_by=ws_ctx.user_id)
        return inv
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/workspaces/{id}/invitations/accept")
async def accept_invitation(
    id: str,
    payload: AcceptInvitationPayload,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    try:
        member = await workspace_service.accept_workspace_invitation(db, id, token=payload.token, user_id=user.id)
        return member
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch("/workspaces/{id}/members/{member_user_id}/role")
async def update_member_role(
    id: str,
    member_user_id: str,
    payload: UpdateRolePayload,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    if ws_ctx.workspace_id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-workspace access denied.")

    # Self-role escalation prevention
    if member_user_id == ws_ctx.user_id and ws_ctx.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users cannot escalate their own role.")

    try:
        return await workspace_service.update_member_role(db, id, member_user_id, payload.role, actor_id=ws_ctx.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/workspaces/{id}/members/{member_user_id}/suspend")
async def suspend_member(
    id: str,
    member_user_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    if ws_ctx.workspace_id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-workspace access denied.")
    try:
        return await workspace_service.suspend_workspace_member(db, id, member_user_id, actor_id=ws_ctx.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete("/workspaces/{id}/members/{member_user_id}")
async def remove_member(
    id: str,
    member_user_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    if ws_ctx.workspace_id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-workspace access denied.")
    try:
        return await workspace_service.remove_workspace_member(db, id, member_user_id, actor_id=ws_ctx.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
