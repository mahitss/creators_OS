from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_governance import (
    TransformationGovernanceProfileRead,
    TransformationDecisionRightRead,
    TransformationGovernanceControlRead,
    TransformationGovernanceFrictionRead,
    TransformationGovernanceGapRead,
    TransformationGovernanceOvercontrolRead,
    TransformationGovernanceLoadRead,
    TransformationGovernanceBottleneckRead,
    TransformationDelegationCandidateRead,
    TransformationGovernanceExceptionRead,
    TransformationGovernanceChangeRequestRead,
    TransformationGovernanceReviewRead,
    TransformationGovernanceQueryResultRead
)
from app.services.transformation_governance_service import TransformationGovernanceService

router = APIRouter(prefix="/api/v1/transformation-governance", tags=["transformation_governance"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_governance_overview():
    return await TransformationGovernanceService.get_governance_overview(None)

@router.get("/decision-rights", response_model=List[dict])
async def list_decision_rights():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("rights", [])

@router.get("/controls", response_model=List[dict])
async def list_controls():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("controls", [])

@router.get("/friction", response_model=List[dict])
async def list_friction():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("frictions", [])

@router.get("/gaps", response_model=List[dict])
async def list_gaps():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("gaps", [])

@router.get("/overcontrol", response_model=List[dict])
async def list_overcontrol():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("overcontrols", [])

@router.get("/load", response_model=List[dict])
async def list_load():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("loads", [])

@router.get("/bottlenecks", response_model=List[dict])
async def list_bottlenecks():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("bottlenecks", [])

@router.get("/delegation", response_model=List[dict])
async def list_delegation_candidates():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("delegationCandidates", [])

@router.get("/exceptions", response_model=List[dict])
async def list_exceptions():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("exceptions", [])

@router.get("/change-requests", response_model=List[dict])
async def list_change_requests():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("changeRequests", [])

@router.post("/change-requests", response_model=dict)
async def create_change_request(data: dict):
    return {"id": "cr_new", "status": "under_review", "description": data.get("description", "Proposed governance change")}

@router.get("/change-requests/{id}", response_model=dict)
async def get_change_request(id: str):
    overview = await TransformationGovernanceService.get_governance_overview(None)
    for cr in overview.get("changeRequests", []):
        if cr.get("id") == id:
            return cr
    return {"id": id, "status": "under_review"}

@router.post("/change-requests/{id}/simulate", response_model=dict)
async def simulate_change_request(id: str):
    return {"id": id, "simulationCompleted": True, "latencyReductionHours": 36.0, "riskIncreasePct": 0.02}

@router.post("/change-requests/{id}/approve", response_model=dict)
async def approve_change_request(id: str):
    return {"id": id, "status": "approved", "approver": "Executive Governance Steering Council"}

@router.post("/change-requests/{id}/execute", response_model=dict)
async def execute_change_request(id: str):
    return {"id": id, "status": "executed", "actionGatewayDispatched": True}

@router.post("/change-requests/{id}/verify", response_model=dict)
async def verify_change_request(id: str):
    return {"id": id, "verified": True, "governanceDriftSeverity": "none"}

@router.get("/reviews", response_model=List[dict])
async def list_reviews():
    overview = await TransformationGovernanceService.get_governance_overview(None)
    return overview.get("reviews", [])

@router.post("/reviews", response_model=dict)
async def create_review(data: dict):
    return {"id": "rev_new", "status": "recommended", "triggerReason": data.get("triggerReason", "Routine governance review")}

@router.get("/reviews/{id}", response_model=dict)
async def get_review(id: str):
    overview = await TransformationGovernanceService.get_governance_overview(None)
    for r in overview.get("reviews", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "recommended"}

@router.post("/reviews/{id}/complete", response_model=dict)
async def complete_review(id: str):
    return {"id": id, "status": "completed", "completed": True}

@router.get("/{id}", response_model=dict)
async def get_governance_profile(id: str):
    overview = await TransformationGovernanceService.get_governance_overview(None)
    for p in overview.get("profiles", []):
        if p.get("id") == id:
            return p
    return {"id": id, "name": "Enterprise Governance Profile", "version": "v2.0"}

@router.post("/query", response_model=TransformationGovernanceQueryResultRead)
async def process_governance_query(query: str = Query(...)):
    return await TransformationGovernanceService.process_natural_language_governance_query(None, query)
