from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_assurance_interventions import (
    TransformationResilienceAssuranceInterventionDomainRead,
    TransformationResilienceAssuranceInterventionCaseRead,
    TransformationResilienceAssuranceInterventionTriggerRead,
    TransformationResilienceAssuranceInterventionOptionRead,
    TransformationResilienceAssuranceRollbackPlanRead,
    TransformationResilienceAssuranceContingencyPlanRead,
    TransformationResilienceAssuranceContingencyReadinessRead,
    TransformationResilienceAssuranceInterventionRecommendationRead,
    TransformationResilienceAssuranceInterventionDecisionPacketRead,
    TransformationResilienceAssuranceInterventionPlanRead,
    TransformationResilienceAssuranceInterventionActionRead,
    TransformationResilienceAssuranceInterventionExpirationRead,
    TransformationResilienceAssuranceInterventionConflictRead,
    TransformationResilienceAssuranceInterventionCascadeRead,
    TransformationResilienceAssuranceInterventionImpactRead,
    TransformationResilienceAssuranceInterventionEffectivenessRead,
    TransformationResilienceAssuranceInterventionFailureRead,
    TransformationResilienceAssuranceInterventionLessonRead,
    TransformationResilienceAssuranceInterventionQueryResultRead
)
from app.services.transformation_resilience_assurance_interventions_service import TransformationResilienceAssuranceInterventionsService

router = APIRouter(prefix="/api/v1/transformation-resilience-assurance-interventions", tags=["transformation_resilience_assurance_interventions"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_assurance_interventions_overview():
    return await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)

@router.post("", response_model=dict)
async def create_assurance_intervention_domain(data: dict):
    return {
        "id": "idom_new",
        "name": data.get("name", "New Assurance Intervention Domain"),
        "scope": data.get("scope", "enterprise"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceAssuranceInterventionQueryResultRead)
async def process_assurance_intervention_query(query: str = Query(...)):
    return await TransformationResilienceAssuranceInterventionsService.process_natural_language_assurance_intervention_query(None, query)

@router.get("/triggers", response_model=List[dict])
async def list_triggers():
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    return overview.get("triggers", [])

@router.get("/triggers/{id}", response_model=dict)
async def get_trigger(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    for trig in overview.get("triggers", []):
        if trig.get("id") == id:
            return trig
    return {"id": id, "type": "early_warning", "validation_status": "validated"}

@router.get("/conflicts", response_model=List[dict])
async def list_conflicts():
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    return overview.get("conflicts", [])

@router.get("/effectiveness", response_model=List[dict])
async def list_effectiveness():
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    return overview.get("effectivenesses", [])

@router.get("/{id}", response_model=dict)
async def get_assurance_intervention_case(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    for case in overview.get("cases", []):
        if case.get("id") == id:
            return case
    return {"id": id, "status": "options_ready", "severity": "high"}

@router.get("/{id}/options", response_model=List[dict])
async def list_case_options(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    return [opt for opt in overview.get("options", []) if opt.get("case_id") == id]

@router.post("/{id}/options", response_model=dict)
async def create_case_option(id: str, data: dict):
    return {
        "id": "iopt_new",
        "case_id": id,
        "option_type": data.get("option_type", "resequence"),
        "title": data.get("title", "New Intervention Option")
    }

@router.post("/{id}/simulate", response_model=dict)
async def simulate_case_scenario(id: str, data: dict):
    return await TransformationResilienceAssuranceInterventionsService.simulate_intervention_scenario(None, id, data)

@router.get("/{id}/scenarios", response_model=List[dict])
async def list_case_scenarios(id: str):
    return [
        {"id": "iscen_01", "case_id": id, "scenario_type": "continue_current_state", "risk_reduction": 0.0},
        {"id": "iscen_02", "case_id": id, "scenario_type": "resequence", "risk_reduction": 0.90}
    ]

@router.get("/{id}/decision-packet", response_model=dict)
async def get_decision_packet(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    for dpack in overview.get("decisionPackets", []):
        if dpack.get("case_id") == id:
            return dpack
    return {"id": "dpack_01", "case_id": id, "governance_requirement": "Requires Governance Board sign-off prior to week 2 close."}

@router.post("/{id}/submit-decision", response_model=dict)
async def submit_decision(id: str, data: dict):
    return {"case_id": id, "decision": data.get("decision", "approved"), "status": "approved"}

@router.get("/{id}/approval", response_model=dict)
async def get_approval_status(id: str):
    return {"case_id": id, "approval_status": "approved", "approver": "Governance Board"}

@router.post("/{id}/request-approval", response_model=dict)
async def request_approval(id: str):
    return await TransformationResilienceAssuranceInterventionsService.request_intervention_approval(None, id)

@router.get("/{id}/plan", response_model=dict)
async def get_intervention_plan(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    for plan in overview.get("plans", []):
        if plan.get("case_id") == id:
            return plan
    return {"id": "iplan_01", "case_id": id, "objective": "Eliminate compute bottleneck", "status": "approved"}

@router.post("/{id}/plan", response_model=dict)
async def create_intervention_plan(id: str, data: dict):
    return {
        "id": "iplan_new",
        "case_id": id,
        "objective": data.get("objective", "New Intervention Objective"),
        "status": "approved"
    }

@router.get("/{id}/execution", response_model=List[dict])
async def get_execution_status(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    return overview.get("actions", [])

@router.post("/{id}/execute", response_model=dict)
async def execute_action(id: str, data: dict):
    action_id = data.get("action_id", "iact_01")
    return await TransformationResilienceAssuranceInterventionsService.execute_intervention_action(None, action_id)

@router.get("/{id}/readiness", response_model=dict)
async def get_case_readiness(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    readinesses = overview.get("readinesses", [])
    if readinesses:
        return readinesses[0]
    return {"id": "cread_01", "overall_status": "partially_ready"}

@router.get("/{id}/rollback", response_model=dict)
async def get_rollback_plan(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    rollbacks = overview.get("rollbackPlans", [])
    if rollbacks:
        return rollbacks[0]
    return {"id": "rplan_01", "authorization_required": "Governance Board Authorization"}

@router.post("/{id}/rollback", response_model=dict)
async def trigger_rollback(id: str):
    return {"case_id": id, "status": "rolled_back", "message": "Rollback plan initiated safely via ActionGateway."}

@router.get("/{id}/contingency", response_model=dict)
async def get_contingency_plan(id: str):
    overview = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
    contingencies = overview.get("contingencyPlans", [])
    if contingencies:
        return contingencies[0]
    return {"id": "cplan_01", "status": "ready"}

@router.post("/{id}/contingency", response_model=dict)
async def activate_contingency(id: str):
    return {"case_id": id, "status": "contingency_activated", "message": "Contingency plan activated."}
