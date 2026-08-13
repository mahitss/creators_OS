from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_knowledge_operations import (
    TransformationResilienceKnowledgeOperationsDomainRead,
    TransformationResilienceKnowledgeRiskCaseRead,
    TransformationResilienceKnowledgeRiskQueueRead,
    TransformationResilienceKnowledgeRiskAssignmentRead,
    TransformationResilienceKnowledgeRemediationPlanRead,
    TransformationResilienceKnowledgeRemediationActionRead,
    TransformationResilienceKnowledgeEvidenceTaskRead,
    TransformationResilienceKnowledgeReviewTaskRead,
    TransformationResilienceKnowledgeRemediationVerificationRead,
    TransformationResilienceKnowledgeRemediationEffectivenessRead,
    TransformationResilienceKnowledgeRiskEscalationRead,
    TransformationResilienceKnowledgeRemediationFailureRead,
    TransformationResilienceKnowledgeRecurringRiskPatternRead,
    TransformationResilienceKnowledgeRemediationQualityRead,
    TransformationResilienceKnowledgeOperatingPatternRead,
    TransformationResilienceKnowledgeOperationsQueryResultRead
)
from app.services.transformation_resilience_knowledge_operations_service import TransformationResilienceKnowledgeOperationsService

router = APIRouter(prefix="/api/v1/transformation-resilience-knowledge-operations", tags=["transformation_resilience_knowledge_operations"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_knowledge_operations_overview():
    return await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)

@router.post("", response_model=dict)
async def create_operations_domain(data: dict):
    return {
        "id": "opdom_new",
        "name": data.get("name", "New Knowledge Operations Domain"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceKnowledgeOperationsQueryResultRead)
async def process_operations_query(query: str = Query(...)):
    return await TransformationResilienceKnowledgeOperationsService.process_natural_language_operations_query(None, query)

@router.get("/risks", response_model=List[dict])
async def list_risk_cases():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("cases", [])

@router.post("/risks", response_model=dict)
async def create_risk_case(data: dict):
    return {
        "id": "rcase_new",
        "knowledge_object_id": data.get("knowledge_object_id", "kobj_01"),
        "risk_type": data.get("risk_type", "stale_evidence"),
        "severity": data.get("severity", "medium"),
        "status": "detected"
    }

@router.get("/risks/{riskId}", response_model=dict)
async def get_risk_case(riskId: str):
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    for c in overview.get("cases", []):
        if c.get("id") == riskId:
            return c
    return {"id": riskId, "risk_type": "high_influence_low_quality", "severity": "high", "status": "in_remediation"}

@router.post("/risks/{riskId}/assign", response_model=dict)
async def assign_risk_owner(riskId: str, data: dict):
    return await TransformationResilienceKnowledgeOperationsService.assign_risk(
        None, riskId, data.get("owner", "Unassigned"), data.get("assigned_by", "Architect"), data.get("reason", "Assignment")
    )

@router.get("/risks/{riskId}/remediation", response_model=dict)
async def get_remediation_plan(riskId: str):
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    for p in overview.get("plans", []):
        if p.get("risk_case_id") == riskId:
            return p
    return {"id": "rplan_01", "risk_case_id": riskId, "status": "in_progress"}

@router.post("/risks/{riskId}/remediation", response_model=dict)
async def create_remediation_plan(riskId: str, data: dict):
    return {
        "id": "rplan_new",
        "risk_case_id": riskId,
        "objective": data.get("objective", "Remediate knowledge risk"),
        "status": "planned"
    }

@router.post("/remediation/{id}/start", response_model=dict)
async def start_remediation(id: str):
    return {"id": id, "status": "in_progress"}

@router.post("/remediation/{id}/complete", response_model=dict)
async def complete_remediation(id: str):
    return {"id": id, "status": "completed"}

@router.get("/evidence-tasks", response_model=List[dict])
async def list_evidence_tasks():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("evidenceTasks", [])

@router.post("/evidence-tasks", response_model=dict)
async def create_evidence_task(data: dict):
    return {
        "id": "etask_new",
        "requested_evidence": data.get("requested_evidence", "Evidence trace"),
        "status": "assigned"
    }

@router.post("/evidence-tasks/{id}/complete", response_model=dict)
async def complete_evidence_task(id: str):
    return {"id": id, "status": "completed"}

@router.get("/review-tasks", response_model=List[dict])
async def list_review_tasks():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("reviewTasks", [])

@router.post("/review-tasks", response_model=dict)
async def create_review_task(data: dict):
    return {
        "id": "rtask_new",
        "review_question": data.get("review_question", "Review question"),
        "status": "assigned"
    }

@router.post("/review-tasks/{id}/complete", response_model=dict)
async def complete_review_task(id: str):
    return {"id": id, "status": "completed"}

@router.get("/escalations", response_model=List[dict])
async def list_escalations():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("escalations", [])

@router.post("/risks/{riskId}/escalate", response_model=dict)
async def escalate_risk(riskId: str, data: dict):
    return {
        "id": "resc_new",
        "risk_case_id": riskId,
        "trigger": data.get("trigger", "manual_escalation"),
        "status": "escalated"
    }

@router.get("/recurring-risks", response_model=List[dict])
async def list_recurring_risks():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("recurring", [])

@router.get("/operating-patterns", response_model=List[dict])
async def list_operating_patterns():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("operatingPatterns", [])

@router.get("/risk-concentration", response_model=List[dict])
async def list_risk_concentration():
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("riskConcentration", [])

@router.get("/{id}", response_model=dict)
async def get_operations_domain(id: str):
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    for dom in overview.get("domains", []):
        if dom.get("id") == id:
            return dom
    return {"id": id, "name": "Global Enterprise Knowledge Operations & Remediation Operating System 2.0", "status": "active"}

@router.get("/{id}/verification", response_model=List[dict])
async def get_remediation_verification(id: str):
    overview = await TransformationResilienceKnowledgeOperationsService.get_knowledge_operations_overview(None)
    return overview.get("verifications", [])

@router.post("/{id}/verify", response_model=dict)
async def verify_remediation(id: str, data: dict):
    return await TransformationResilienceKnowledgeOperationsService.verify_remediation(None, id, data)
