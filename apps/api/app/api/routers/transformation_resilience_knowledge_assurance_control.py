from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_knowledge_assurance_control import (
    TransformationResilienceAdaptiveKnowledgeAssuranceDomainRead,
    TransformationResilienceKnowledgeAssurancePlanBaselineRead,
    TransformationResilienceKnowledgeAssuranceChangeSignalRead,
    TransformationResilienceKnowledgeAssuranceChangeDetectionRead,
    TransformationResilienceKnowledgeAssuranceAssumptionImpactRead,
    TransformationResilienceKnowledgeAssurancePlanImpactRead,
    TransformationResilienceKnowledgeAssurancePlanHealthRead,
    TransformationResilienceKnowledgeAssurancePlanStalenessRead,
    TransformationResilienceKnowledgeAssuranceReplanTriggerRead,
    TransformationResilienceKnowledgeAssuranceReplanRecommendationRead,
    TransformationResilienceKnowledgeAssurancePlanVersionRead,
    TransformationResilienceKnowledgeAssurancePlanDiffRead,
    TransformationResilienceKnowledgeAssuranceReplanQueueRead,
    TransformationResilienceKnowledgeAssuranceEmergencyReplanRead,
    TransformationResilienceKnowledgeAssuranceCrossPlanImpactRead,
    TransformationResilienceKnowledgeAssurancePortfolioDriftRead,
    TransformationResilienceKnowledgeAssuranceControlQueryResultRead
)
from app.services.transformation_resilience_knowledge_assurance_control_service import TransformationResilienceKnowledgeAssuranceControlService

router = APIRouter(prefix="/api/v1/transformation-resilience-knowledge-assurance-control", tags=["transformation_resilience_knowledge_assurance_control"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_knowledge_assurance_control_overview():
    return await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)

@router.post("", response_model=dict)
async def create_adaptive_domain(data: dict):
    return {
        "id": "adom_new",
        "name": data.get("name", "New Adaptive Assurance Domain"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceKnowledgeAssuranceControlQueryResultRead)
async def process_control_query(query: str = Query(...)):
    return await TransformationResilienceKnowledgeAssuranceControlService.process_natural_language_assurance_control_query(None, query)

@router.get("/plans", response_model=List[dict])
async def list_baselines():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("baselines", [])

@router.get("/plans/{planId}/health", response_model=dict)
async def get_plan_health(planId: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    for h in overview.get("healths", []):
        if h.get("plan_id") == planId:
            return h
    return {"plan_id": planId, "risk_alignment": 0.92, "evidence_alignment": 0.88, "capacity_alignment": 0.75}

@router.get("/plans/{planId}/staleness", response_model=dict)
async def get_plan_staleness(planId: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    for s in overview.get("stalenesses", []):
        if s.get("plan_id") == planId:
            return s
    return {"plan_id": planId, "status": "current", "outdated_assumptions_json": []}

@router.get("/change-signals", response_model=List[dict])
async def list_change_signals():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("signals", [])

@router.post("/change-signals", response_model=dict)
async def create_change_signal(data: dict):
    return {
        "id": "csig_new",
        "source": data.get("source", "resilience_sensing"),
        "change_type": data.get("change_type", "dependency_change"),
        "significance": data.get("significance", "material")
    }

@router.get("/change-signals/{id}", response_model=dict)
async def get_change_signal(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    for s in overview.get("signals", []):
        if s.get("id") == id:
            return s
    return {"id": id, "change_type": "dependency_change", "significance": "material"}

@router.get("/replans", response_model=List[dict])
async def list_replans():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("queues", [])

@router.post("/plans/{planId}/replan", response_model=dict)
async def request_replan(planId: str, data: dict):
    return await TransformationResilienceKnowledgeAssuranceControlService.create_plan_version(None, planId, data)

@router.get("/plans/{planId}/replan-options", response_model=List[dict])
async def list_replan_options(planId: str):
    return [
        {"id": "opt_continue", "title": "Continue Current Plan V1.0", "coverage": 0.84, "baseline_comparison": "Current baseline"},
        {"id": "opt_resequence", "title": "Resequence with 2x Retry Buffer (Plan V2.0)", "coverage": 0.92, "baseline_comparison": "+8% coverage boost"}
    ]

@router.post("/plans/{planId}/simulate-replan", response_model=dict)
async def simulate_replan(planId: str, data: dict):
    return {
        "plan_id": planId,
        "option_simulated": data.get("option_id", "opt_resequence"),
        "simulated_coverage": 0.92,
        "simulated_residual_risk": 0.08
    }

@router.get("/plans/{planId}/versions", response_model=List[dict])
async def list_versions(planId: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("versions", [])

@router.get("/plans/{planId}/versions/{versionId}", response_model=dict)
async def get_version(planId: str, versionId: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    for v in overview.get("versions", []):
        if v.get("id") == versionId or v.get("version_number") == versionId:
            return v
    return {"id": versionId, "plan_id": planId, "version_number": "v2.0", "approval_state": "approved"}

@router.get("/plans/{planId}/diff", response_model=List[dict])
async def get_plan_diff(planId: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("diffs", [])

@router.get("/plans/{planId}/approval", response_model=dict)
async def get_plan_approval_state(planId: str):
    return {"plan_id": planId, "approval_state": "approved", "approver": "Enterprise Governance Board"}

@router.post("/plans/{planId}/request-approval", response_model=dict)
async def request_plan_version_approval(planId: str):
    return {"plan_id": planId, "approval_requested": True, "approval_routed": True}

@router.get("/plans/{planId}/execution", response_model=dict)
async def get_plan_execution_state(planId: str):
    return {"plan_id": planId, "version_executing": "v2.0", "execution_status": "executing", "action_gateway_routed": True}

@router.post("/plans/{planId}/execute", response_model=dict)
async def execute_plan_version(planId: str, version_id: str = Query("v2.0")):
    return await TransformationResilienceKnowledgeAssuranceControlService.execute_plan_version(None, planId, version_id)

@router.get("/cross-plan-impact", response_model=List[dict])
async def list_cross_plan_impacts():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("crossImpacts", [])

@router.get("/portfolio-drift", response_model=List[dict])
async def list_portfolio_drift():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("drifts", [])

@router.get("/emergency-replans", response_model=List[dict])
async def list_emergency_replans():
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    return overview.get("emergencies", [])

@router.post("/emergency-replans", response_model=dict)
async def create_emergency_replan(data: dict):
    plan_id = data.get("plan_id", "aplan_critical_99")
    return await TransformationResilienceKnowledgeAssuranceControlService.trigger_emergency_replan(None, plan_id, data)

@router.get("/{id}", response_model=dict)
async def get_adaptive_domain(id: str):
    overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
    for dom in overview.get("domains", []):
        if dom.get("id") == id:
            return dom
    return {"id": id, "name": "Global Enterprise Adaptive Knowledge Assurance & Continuous Replanning Control 2.0", "status": "active"}
