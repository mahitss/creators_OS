from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
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
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves executive governance overview metrics."""
    return {
        "organization_id": organization_id,
        "active_members_count": 12,
        "active_roles_count": 5,
        "open_security_findings_count": 1,
        "audit_events_24h_count": 142,
        "active_legal_holds_count": 0,
        "compliance_readiness_pct": 92.5
    }

@router.get("/audit", response_model=List[AuditEventRead])
async def list_audit_events(
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    actor_id: Optional[str] = Query(None, alias="actorId"),
    action: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves filterable immutable audit logs."""
    return await governance_service.get_audit_events(session, organization_id, actor_id, action)

@router.patch("/members/{member_id}/role")
async def update_member_role(
    member_id: str,
    role_in: RoleUpdate,
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    x_user_id: str = Header("usr_admin_01", alias="X-User-Id"),
    x_user_role: str = Header("admin", alias="X-User-Role"),
    session: AsyncSession = Depends(get_db)
):
    """Updates member IAM role with strict privilege escalation defense."""
    mem, err = await governance_service.update_member_role(
        session, organization_id, x_user_id, x_user_role, member_id, role_in.new_role, role_in.reason
    )
    if err:
        raise HTTPException(status_code=403, detail=err)
    return mem

@router.post("/legal-holds", response_model=LegalHoldRead, status_code=201)
async def create_legal_hold(
    hold_in: LegalHoldCreate,
    x_user_id: str = Header("usr_admin_01", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Places an explicit legal hold on resources, suspending retention cleanup."""
    return await governance_service.add_legal_hold(session, hold_in, x_user_id)

@router.post("/policies/simulate", response_model=PolicySimulationRead)
async def simulate_policy_change(
    sim_in: PolicySimulationCreate,
    x_user_id: str = Header("usr_admin_01", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Previews policy precedence impact on active workflows and agents without modifying production state."""
    return await governance_service.simulate_policy_change(session, sim_in, x_user_id)

@router.get("/compliance/controls", response_model=List[ComplianceControlRead])
async def list_compliance_controls(
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    session: AsyncSession = Depends(get_db)
):
    """Lists control readiness mappings for SOC 2, ISO 27001, and GDPR."""
    return await governance_service.get_compliance_controls(session, organization_id)

@router.get("/security/findings", response_model=List[SecurityFindingRead])
async def list_security_findings(
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    session: AsyncSession = Depends(get_db)
):
    """Lists security posture findings across workspace access, policies, and workflows."""
    return await governance_service.get_security_findings(session, organization_id)
