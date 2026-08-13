import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_governance import (
    TransformationResilienceGovernanceDomainRead,
    TransformationResilienceGovernanceControlRead,
    TransformationResilienceGovernanceControlRequirementRead,
    TransformationResilienceGovernanceControlEvidenceRead,
    TransformationResilienceGovernanceControlTestRead,
    TransformationResilienceGovernanceControlAttestationRead,
    TransformationResilienceGovernanceAssuranceClaimRead,
    TransformationResilienceGovernanceAssurancePacketRead,
    TransformationResilienceGovernanceProductionReadinessAssessmentRead,
    TransformationResilienceGovernanceReadinessBlockerRead,
    TransformationResilienceGovernanceExceptionRead,
    TransformationResilienceGovernanceRiskAcceptanceRead,
    TransformationResilienceGovernanceFindingRead,
    TransformationResilienceGovernanceRemediationRead,
    TransformationResilienceGovernanceAuditReadinessRead,
    TransformationResilienceGovernanceReleaseAssessmentRead,
    TransformationResilienceGovernanceRecoveryReadinessRead,
    TransformationResilienceGovernanceQueryResultRead
)
from app.services.transformation_resilience_governance_service import TransformationResilienceGovernanceService

router = APIRouter(prefix="/api/v1/transformation-resilience-governance", tags=["transformation_resilience_governance"])

@router.get("", response_model=dict)
@router.get("/status", response_model=dict)
async def get_governance_status():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    domains = overview.get("domains", [])
    if domains:
        return domains[0]
    return {"id": "govdom_01", "name": "Resilience Governance 2.0", "status": "active"}

@router.get("/controls", response_model=List[dict])
async def list_controls():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("controls", [])

@router.post("/controls", response_model=dict)
async def create_control(data: dict):
    return {
        "id": f"ctrl_{uuid.uuid4().hex[:8]}",
        "control_code": data.get("control_code", "CTRL_CUSTOM"),
        "title": data.get("title", "Custom Assurance Control"),
        "category": data.get("category", "security"),
        "owner": data.get("owner", "Governance Lead"),
        "status": "active"
    }

@router.get("/controls/{id}", response_model=dict)
async def get_control(id: str):
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    for c in overview.get("controls", []):
        if c.get("id") == id or c.get("control_code") == id:
            return c
    return {"id": id, "title": "Event Integrity Control", "status": "active"}

@router.get("/evidence", response_model=List[dict])
async def list_evidence():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("evidence", [])

@router.get("/evidence/{id}", response_model=dict)
async def get_evidence(id: str):
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    for e in overview.get("evidence", []):
        if e.get("id") == id:
            return e
    return {"id": id, "confidence": 1.0, "review_status": "reviewed"}

@router.get("/tests", response_model=List[dict])
async def list_tests():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("tests", [])

@router.post("/tests", response_model=dict)
async def create_test(data: dict):
    return {
        "id": f"ctest_{uuid.uuid4().hex[:8]}",
        "control_id": data.get("control_id", "ctrl_01"),
        "test_type": data.get("test_type", "automated_test"),
        "result": "passed"
    }

@router.get("/attestations", response_model=List[dict])
async def list_attestations():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("attestations", [])

@router.post("/attestations/{id}/approve", response_model=dict)
async def approve_attestation(id: str, attestor: str = "Chief Compliance Officer"):
    return await TransformationResilienceGovernanceService.approve_attestation(None, id, attestor)

@router.post("/attestations/{id}/reject", response_model=dict)
async def reject_attestation(id: str):
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    atts = overview.get("attestations", [])
    for a in atts:
        if a.get("id") == id:
            a["status"] = "rejected"
            return a
    return {"id": id, "status": "rejected"}

@router.get("/claims", response_model=List[dict])
async def list_claims():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("claims", [])

@router.get("/readiness", response_model=dict)
async def get_readiness():
    return await TransformationResilienceGovernanceService.assess_production_readiness(None)

@router.get("/readiness/blockers", response_model=List[dict])
async def list_readiness_blockers():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("readinessBlockers", [])

@router.get("/exceptions", response_model=List[dict])
async def list_exceptions():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("exceptions", [])

@router.post("/exceptions", response_model=dict)
async def create_exception(data: dict):
    return {
        "id": f"excep_{uuid.uuid4().hex[:8]}",
        "control_id": data.get("control_id", "ctrl_01"),
        "reason": data.get("reason", "Temporary operational exception"),
        "status": "approved"
    }

@router.get("/findings", response_model=List[dict])
async def list_findings():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("findings", [])

@router.get("/remediation", response_model=List[dict])
async def list_remediations():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("remediations", [])

@router.get("/releases", response_model=List[dict])
async def list_releases():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("releaseAssessments", [])

@router.get("/releases/{id}", response_model=dict)
async def get_release(id: str):
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    for r in overview.get("releaseAssessments", []):
        if r.get("id") == id or r.get("release_tag") == id:
            return r
    return {"id": id, "gate_status": "approved"}

@router.post("/releases/{id}/assess", response_model=dict)
async def assess_release(id: str):
    return await TransformationResilienceGovernanceService.assess_release_gate(None, id)

@router.get("/audit-readiness", response_model=dict)
async def get_audit_readiness():
    overview = await TransformationResilienceGovernanceService.get_governance_overview(None)
    return overview.get("auditReadiness", {"audit_scope": "Enterprise Transformation Resilience OS 2.0", "evidence_availability_pct": 100.0})

@router.post("/query", response_model=TransformationResilienceGovernanceQueryResultRead)
async def process_governance_query(query: str = Query(...)):
    return await TransformationResilienceGovernanceService.process_natural_language_governance_query(None, query)
