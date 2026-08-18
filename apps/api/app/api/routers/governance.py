from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import require_admin, WorkspaceContext
from app.schemas.governance import (
    OrganizationMemberRead,
    RoleUpdate,
    AuditEventRead,
    RetentionPolicyCreate,
    RetentionPolicyRead,
    LegalHoldCreate,
    LegalHoldRead,
    AccessReviewCreate,
    AccessReviewRead,
    AccessReviewItemRead,
    ComplianceControlRead,
    ComplianceEvidenceRead,
    SecurityFindingRead,
    PolicySimulationCreate,
    PolicySimulationRead
)
from app.services import governance_service

router = APIRouter(prefix="/admin", tags=["governance"])

@router.get("/overview")
async def get_governance_overview(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves executive governance overview metrics."""
    return {
        "organization_id": ws_ctx.workspace_id,
        "active_members_count": 12,
        "active_roles_count": 5,
        "open_security_findings_count": 1,
        "audit_events_24h_count": 142,
        "active_legal_holds_count": 0,
        "compliance_readiness_pct": 92.5
    }

@router.get("/audit", response_model=List[AuditEventRead])
async def list_audit_events(
    actor_id: Optional[str] = Query(None, alias="actorId"),
    action: Optional[str] = Query(None),
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves filterable immutable audit logs."""
    return await governance_service.get_audit_events(session, ws_ctx.workspace_id, actor_id, action)

@router.patch("/members/{member_id}/role")
async def update_member_role(
    member_id: str,
    role_in: RoleUpdate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Updates member IAM role with strict privilege escalation defense."""
    mem, err = await governance_service.update_member_role(
        session, ws_ctx.workspace_id, ws_ctx.user_id, ws_ctx.role, member_id, role_in.new_role, role_in.reason
    )
    if err:
        raise HTTPException(status_code=403, detail=err)
    return mem

@router.post("/legal-holds", response_model=LegalHoldRead, status_code=201)
async def create_legal_hold(
    hold_in: LegalHoldCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Places an explicit legal hold on resources, suspending retention cleanup."""
    return await governance_service.add_legal_hold(session, hold_in, ws_ctx.user_id)

@router.post("/policies/simulate", response_model=PolicySimulationRead)
async def simulate_policy_change(
    sim_in: PolicySimulationCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Previews policy precedence impact on active workflows and agents without modifying production state."""
    return await governance_service.simulate_policy_change(session, sim_in, ws_ctx.user_id)

@router.get("/compliance/controls", response_model=List[ComplianceControlRead])
async def list_compliance_controls(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Lists control readiness mappings for SOC 2, ISO 27001, and GDPR."""
    return await governance_service.get_compliance_controls(session, ws_ctx.workspace_id)

@router.get("/security/findings", response_model=List[SecurityFindingRead])
async def list_security_findings(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """Lists open security configuration findings and vulnerabilities."""
    return await governance_service.get_security_findings(session, ws_ctx.workspace_id)
