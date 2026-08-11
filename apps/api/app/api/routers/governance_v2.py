from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.policy_intelligence import (
    PolicyCreate,
    PolicyRead,
    PolicyVersionRead,
    PolicyEvaluateRequest,
    PolicyEvaluateResponse,
    PolicyRequestRead,
    PolicyConflictRead,
    PolicyGapRead,
    PolicySimulationCreate,
    PolicySimulationRead,
    PolicyOverrideCreate,
    PolicyOverrideRead,
    TemporaryAccessGrantCreate,
    TemporaryAccessGrantRead,
    BreakGlassGrantCreate,
    BreakGlassGrantRead
)
from app.services import policy_intelligence_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/governance", tags=["Enterprise Agent Governance & Policy Intelligence 2.0"])

@router.get("/policies", response_model=List[PolicyRead])
async def list_policies(
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Lists workspace and organization policies."""
    return await policy_intelligence_service.list_policies(db, workspace_id=workspace_id)

@router.post("/policies", response_model=PolicyRead)
async def create_policy(
    req: PolicyCreate,
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    user_id: str = Header("usr_default_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new policy with schema validation and broad policy detection."""
    return await policy_intelligence_service.create_policy(
        db, workspace_id=workspace_id, user_id=user_id, req=req
    )

@router.get("/policies/{policy_id}", response_model=PolicyRead)
async def get_policy(
    policy_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Gets policy details by ID."""
    pol = await policy_intelligence_service.get_policy_by_id(db, policy_id=policy_id)
    if not pol:
        raise HTTPException(status_code=404, detail="Policy not found")
    return pol

@router.post("/evaluate", response_model=PolicyEvaluateResponse)
async def evaluate_policy_request(
    req: PolicyEvaluateRequest,
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Evaluates a policy request with risk classification, control chains, and deterministic precedence."""
    return await policy_intelligence_service.evaluate_request(
        db, req=req, workspace_id=workspace_id
    )

@router.get("/gaps", response_model=List[PolicyGapRead])
async def list_policy_gaps(
    db: AsyncSession = Depends(get_db)
):
    """Surfaces uncovered non-trivial risk actions as policy gaps."""
    return await policy_intelligence_service.list_gaps(db)

@router.get("/conflicts", response_model=List[PolicyConflictRead])
async def list_policy_conflicts(
    db: AsyncSession = Depends(get_db)
):
    """Surfaces contradictory policies with deterministic precedence resolution."""
    return await policy_intelligence_service.list_conflicts(db)

@router.get("/overrides", response_model=List[PolicyOverrideRead])
async def list_policy_overrides(
    db: AsyncSession = Depends(get_db)
):
    """Lists active policy overrides."""
    return await policy_intelligence_service.list_overrides(db)

@router.post("/breakglass", response_model=BreakGlassGrantRead)
async def request_breakglass_access(
    req: BreakGlassGrantCreate,
    user_id: str = Header("usr_default_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Requests emergency Break-Glass access with explicit authorization and audit trail."""
    return await policy_intelligence_service.create_breakglass_grant(
        db, req=req, authorized_by=user_id
    )
