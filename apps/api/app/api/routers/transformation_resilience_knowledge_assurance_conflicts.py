from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_knowledge_assurance_conflicts import (
    TransformationResilienceKnowledgeAssuranceConflictIntelligenceDomainRead,
    TransformationResilienceKnowledgeAssuranceConflictCaseRead,
    TransformationResilienceKnowledgeAssuranceConflictImpactRead,
    TransformationResilienceKnowledgeAssuranceConflictRootCauseRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionOptionRead,
    TransformationResilienceKnowledgeAssuranceConflictTradeoffRead,
    TransformationResilienceKnowledgeAssuranceConflictScenarioResultRead,
    TransformationResilienceKnowledgeAssuranceConflictRecommendationRead,
    TransformationResilienceKnowledgeAssuranceConflictDecisionPacketRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionPlanRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionActionRead,
    TransformationResilienceKnowledgeAssuranceResidualConflictRead,
    TransformationResilienceKnowledgeAssuranceConflictCascadeRead,
    TransformationResilienceKnowledgeAssuranceConflictClusterRead,
    TransformationResilienceKnowledgeAssuranceSystemicConflictRead,
    TransformationResilienceKnowledgeAssuranceConflictDriftRead,
    TransformationResilienceKnowledgeAssuranceConflictEscalationRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionEffectivenessRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionFailureRead,
    TransformationResilienceKnowledgeAssuranceConflictResolutionPatternRead,
    TransformationResilienceKnowledgeAssuranceConflictQueryResultRead
)
from app.services.transformation_resilience_knowledge_assurance_conflict_service import TransformationResilienceKnowledgeAssuranceConflictService

router = APIRouter(prefix="/api/v1/transformation-resilience-knowledge-assurance-conflicts", tags=["transformation_resilience_knowledge_assurance_conflicts"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_knowledge_assurance_conflict_overview():
    return await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)

@router.post("", response_model=dict)
async def create_conflict_case(data: dict):
    return {
        "id": "ccase_new",
        "conflict_type": data.get("conflict_type", "resource"),
        "severity": data.get("severity", "high"),
        "status": "detected"
    }

@router.post("/query", response_model=TransformationResilienceKnowledgeAssuranceConflictQueryResultRead)
async def process_conflict_query(query: str = Query(...)):
    return await TransformationResilienceKnowledgeAssuranceConflictService.process_natural_language_assurance_conflict_query(None, query)

@router.get("/queue", response_model=List[dict])
async def list_conflict_queue():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("cases", [])

@router.get("/critical", response_model=List[dict])
async def list_critical_conflicts():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return [c for c in overview.get("cases", []) if c.get("severity") in ["critical", "high"]]

@router.get("/cascades", response_model=List[dict])
async def list_conflict_cascades():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("cascades", [])

@router.get("/clusters", response_model=List[dict])
async def list_conflict_clusters():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("clusters", [])

@router.get("/systemic", response_model=List[dict])
async def list_systemic_conflicts():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("systemic", [])

@router.get("/drift", response_model=List[dict])
async def list_conflict_drift():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("drifts", [])

@router.get("/effectiveness", response_model=List[dict])
async def list_resolution_effectiveness():
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return overview.get("effectivenesses", [])

@router.get("/{id}", response_model=dict)
async def get_conflict_case(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    for c in overview.get("cases", []):
        if c.get("id") == id:
            return c
    return {"id": id, "conflict_type": "resource", "severity": "high", "status": "options_ready"}

@router.get("/{id}/impact", response_model=dict)
async def get_conflict_impact(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    for imp in overview.get("impacts", []):
        if imp.get("conflict_case_id") == id:
            return imp
    return {"conflict_case_id": id, "risk_exposure": 0.25, "coverage_loss": 0.15, "deadline_exposure_days": 7}

@router.get("/{id}/options", response_model=List[dict])
async def list_resolution_options(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return [opt for opt in overview.get("options", []) if opt.get("conflict_case_id") == id]

@router.post("/{id}/options", response_model=dict)
async def create_resolution_option(id: str, data: dict):
    return {
        "id": "ropt_new",
        "conflict_case_id": id,
        "option_type": data.get("option_type", "sequence"),
        "title": data.get("title", "New Resolution Option")
    }

@router.get("/{id}/scenarios", response_model=List[dict])
async def list_conflict_scenarios(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    return [scen for scen in overview.get("scenarios", []) if scen.get("conflict_case_id") == id]

@router.post("/{id}/simulate", response_model=dict)
async def simulate_conflict_resolution(id: str, data: dict):
    return {
        "conflict_case_id": id,
        "option_type": data.get("option_type", "sequence"),
        "simulated_coverage": 0.92,
        "simulated_risk_reduction": 0.90
    }

@router.get("/{id}/decision-packet", response_model=dict)
async def get_conflict_decision_packet(id: str):
    return await TransformationResilienceKnowledgeAssuranceConflictService.prepare_decision_packet(None, id)

@router.post("/{id}/submit-decision", response_model=dict)
async def submit_conflict_decision(id: str, data: dict):
    return await TransformationResilienceKnowledgeAssuranceConflictService.submit_decision(None, id, data)

@router.get("/{id}/approval", response_model=dict)
async def get_conflict_approval(id: str):
    return {"conflict_case_id": id, "approval_state": "approved", "approver": "Enterprise Governance Board"}

@router.post("/{id}/request-approval", response_model=dict)
async def request_conflict_approval(id: str):
    return {"conflict_case_id": id, "approval_requested": True, "approval_routed": True}

@router.get("/{id}/resolution", response_model=dict)
async def get_conflict_resolution(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
    for plan in overview.get("resolutionPlans", []):
        if plan.get("conflict_case_id") == id:
            return plan
    return {"conflict_case_id": id, "selected_option": "sequence", "status": "planned"}

@router.post("/{id}/resolve", response_model=dict)
async def resolve_conflict(id: str, data: dict):
    return await TransformationResilienceKnowledgeAssuranceConflictService.resolve_conflict(None, id, data)
