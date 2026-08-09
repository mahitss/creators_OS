from typing import Optional, List, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.services import workspace_service

router = APIRouter()

DEFAULT_USER_ID = "usr_alex"
DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_auth_headers(
    x_user_id: Optional[str] = Header(None),
    x_workspace_id: Optional[str] = Header(None)
) -> Tuple[str, str]:
    user_id = x_user_id or DEFAULT_USER_ID
    workspace_id = x_workspace_id or DEFAULT_WORKSPACE_ID
    return user_id, workspace_id

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
async def list_workspaces() -> List[WorkspaceSummary]:
    return [
        WorkspaceSummary(
            id="ws_default_01",
            name="Vapor Core Engine",
            root_path="c:\\Users\\pc\\OneDrive\\Desktop\\Hack vibe"
        )
    ]

@router.get("/workspaces/{id}/members")
async def list_workspace_members(
    id: str,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    return await workspace_service.list_workspace_members(db, id)

@router.post("/workspaces/{id}/invitations", status_code=status.HTTP_201_CREATED)
async def invite_member(
    id: str,
    payload: InviteMemberPayload,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    user_id, _ = auth
    # Verify actor is owner or admin
    actor = await workspace_service.get_workspace_member(db, id, user_id)
    if not actor or actor.get("role") not in ["owner", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners and admins can invite new members.")

    try:
        inv = await workspace_service.invite_workspace_member(db, id, email=payload.email, role=payload.role, invited_by=user_id)
        return inv
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/workspaces/{id}/invitations/accept")
async def accept_invitation(
    id: str,
    payload: AcceptInvitationPayload,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    user_id, _ = auth
    try:
        member = await workspace_service.accept_workspace_invitation(db, id, token=payload.token, user_id=user_id)
        return member
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch("/workspaces/{id}/members/{member_user_id}/role")
async def update_member_role(
    id: str,
    member_user_id: str,
    payload: UpdateRolePayload,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    user_id, _ = auth
    actor = await workspace_service.get_workspace_member(db, id, user_id)
    if not actor or actor.get("role") not in ["owner", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners and admins can modify member roles.")

    # Self-role escalation prevention
    if member_user_id == user_id and actor.get("role") != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users cannot escalate their own role.")

    try:
        return await workspace_service.update_member_role(db, id, member_user_id, payload.role, actor_id=user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/workspaces/{id}/members/{member_user_id}/suspend")
async def suspend_member(
    id: str,
    member_user_id: str,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    user_id, _ = auth
    actor = await workspace_service.get_workspace_member(db, id, user_id)
    if not actor or actor.get("role") not in ["owner", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners and admins can suspend members.")

    try:
        return await workspace_service.suspend_workspace_member(db, id, member_user_id, actor_id=user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete("/workspaces/{id}/members/{member_user_id}")
async def remove_member(
    id: str,
    member_user_id: str,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> dict:
    user_id, _ = auth
    actor = await workspace_service.get_workspace_member(db, id, user_id)
    if not actor or actor.get("role") not in ["owner", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners and admins can remove members.")

    try:
        return await workspace_service.remove_workspace_member(db, id, member_user_id, actor_id=user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
