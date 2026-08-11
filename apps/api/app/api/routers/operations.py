from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.control_plane import (
    OperationsOverviewRead,
    ServiceTopologyNode,
    ControlActionRequest,
    ControlActionRead,
    ControlActionApprovalRequest,
    ControlActionApprovalRead,
    AIOperationsQueryRequest,
    AIOperationsQueryResponse
)
from app.services import control_plane_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/operations", tags=["Enterprise Control Plane & Operations Center"])

@router.get("/overview", response_model=OperationsOverviewRead)
async def get_overview(
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Returns top-level executive health summary and contributing signals."""
    return await control_plane_service.get_operations_overview(db, workspace_id=workspace_id)

@router.get("/services", response_model=List[ServiceTopologyNode])
async def get_services(
    db: AsyncSession = Depends(get_db)
):
    """Returns major Vapor subsystems topology and dependency graph."""
    return await control_plane_service.get_service_dependency_map(db)

@router.get("/actions", response_model=List[ControlActionRead])
async def list_actions(
    db: AsyncSession = Depends(get_db)
):
    """Lists control action history and pending approvals."""
    return await control_plane_service.list_control_actions(db)

@router.post("/actions", response_model=ControlActionRead)
async def request_action(
    req: ControlActionRequest,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Requests execution of a policy-governed control action."""
    action, err = await control_plane_service.request_control_action(db, req, requester_id=x_user_id, organization_id=organization_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return action

@router.get("/actions/{action_id}", response_model=ControlActionRead)
async def get_action(
    action_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches control action details by ID."""
    action = await control_plane_service.get_control_action_by_id(db, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Control action not found")
    return action

@router.post("/actions/{action_id}/approve", response_model=ControlActionRead)
async def approve_action(
    action_id: str,
    req: ControlActionApprovalRequest,
    x_user_id: str = Header("usr_approver_02", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Approves a high/critical risk control action enforcing 2-person approval."""
    action, err = await control_plane_service.approve_control_action(
        db, action_id=action_id, approver_id=x_user_id, comments=req.comments, organization_id=organization_id
    )
    if err:
        raise HTTPException(status_code=400, detail=err)
    return action

@router.post("/actions/{action_id}/reject", response_model=ControlActionRead)
async def reject_action(
    action_id: str,
    req: ControlActionApprovalRequest,
    x_user_id: str = Header("usr_approver_02", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Rejects a pending control action."""
    action, err = await control_plane_service.reject_control_action(
        db, action_id=action_id, approver_id=x_user_id, comments=req.comments, organization_id=organization_id
    )
    if err:
        raise HTTPException(status_code=400, detail=err)
    return action

@router.post("/ai-query", response_model=AIOperationsQueryResponse)
async def query_ai_operations(
    req: AIOperationsQueryRequest,
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Natural language evidence-backed operational diagnostic query engine."""
    return await control_plane_service.query_ai_operations_assistant(db, req, workspace_id=workspace_id)
