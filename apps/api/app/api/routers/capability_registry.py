from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.capability_registry import (
    CapabilityCreate,
    CapabilityRead,
    CapabilityVersionRead,
    CapabilityInstallationRead,
    CapabilityRequestCreate,
    CapabilityRequestRead,
    CapabilityHealthRead,
    CapabilityInvokeRequest,
    CapabilityInvokeResponse,
    CapabilityPackageRead
)
from app.services import capability_registry_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, require_admin, WorkspaceContext

router = APIRouter(prefix="", tags=["Enterprise Agent Capability Registry & Skill Marketplace Foundation"])

@router.get("/capabilities", response_model=List[CapabilityRead])
async def list_capabilities(
    query: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Discovers enterprise capabilities in the registry catalog."""
    return await capability_registry_service.discover_capabilities(
        db, workspace_id=ws_ctx.workspace_id, query=query, cap_type=type, category=category
    )

@router.post("/capabilities", response_model=CapabilityRead)
async def register_capability(
    req: CapabilityCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Registers a new capability in the Enterprise Capability Registry."""
    cap, _ = await capability_registry_service.register_capability(
        db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id
    )
    return cap

@router.get("/capabilities/installations", response_model=List[CapabilityInstallationRead])
async def list_installations(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists installed capabilities in the current workspace."""
    return await capability_registry_service.list_installations(db, workspace_id=ws_ctx.workspace_id)

@router.get("/capabilities/requests", response_model=List[CapabilityRequestRead])
async def list_requests(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists pending installation and access requests."""
    return await capability_registry_service.list_requests(db, workspace_id=ws_ctx.workspace_id)

@router.post("/capabilities/requests", response_model=CapabilityRequestRead)
async def create_request(
    req: CapabilityRequestCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Submits an installation or access request for a high-risk capability."""
    return await capability_registry_service.request_installation(
        db, workspace_id=ws_ctx.workspace_id, req=req
    )

@router.post("/capabilities/requests/{request_id}/approve", response_model=CapabilityRequestRead)
async def approve_request(
    request_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Approves a pending capability installation request."""
    return await capability_registry_service.approve_request(db, request_id=request_id, reviewed_by=ws_ctx.user_id)

@router.get("/capabilities/{capability_id}", response_model=CapabilityRead)
async def get_capability(
    capability_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Fetches details of a specific capability."""
    cap = await capability_registry_service.get_capability(db, capability_id=capability_id)
    if not cap:
        raise HTTPException(status_code=404, detail="Capability not found")
    return cap

@router.get("/capabilities/{capability_id}/versions", response_model=List[CapabilityVersionRead])
async def get_versions(
    capability_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns version history of a capability."""
    return await capability_registry_service.get_versions(db, capability_id=capability_id)

@router.get("/capabilities/{capability_id}/health", response_model=CapabilityHealthRead)
async def get_health(
    capability_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns availability and latency health telemetry for a capability."""
    health = await capability_registry_service.get_health(db, capability_id=capability_id)
    if not health:
        raise HTTPException(status_code=404, detail="Capability health telemetry not found")
    return health

@router.post("/capabilities/{capability_id}/invoke", response_model=CapabilityInvokeResponse)
async def invoke_capability(
    capability_id: str,
    req: CapabilityInvokeRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Invokes a capability through the Unified Capability Invocation Router."""
    return await capability_registry_service.invoke_capability(
        db, workspace_id=ws_ctx.workspace_id, capability_id=capability_id, req=req, organization_id=ws_ctx.workspace_id
    )
