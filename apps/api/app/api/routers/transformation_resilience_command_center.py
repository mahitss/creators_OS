from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_command_center import (
    TransformationResilienceCommandCenterRead,
    TransformationResilienceExecutiveStateRead,
    TransformationResiliencePriorityItemRead,
    TransformationResilienceSituationRead,
    TransformationResilienceSituationSnapshotRead,
    TransformationResilienceExposureMapRead,
    TransformationResilienceEvidenceSummaryRead,
    TransformationResilienceUnappliedLessonRead,
    TransformationResilienceDecisionPacketRead,
    TransformationResilienceCommandCenterQueryResultRead
)
from app.services.transformation_resilience_command_center_service import TransformationResilienceCommandCenterService

router = APIRouter(prefix="/api/v1/transformation-resilience-command-center", tags=["transformation_resilience_command_center"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_command_center_overview():
    return await TransformationResilienceCommandCenterService.get_command_center_overview(None)

@router.post("", response_model=dict)
async def create_command_center(data: dict):
    return {
        "id": "cc_res_new",
        "name": data.get("name", "New Resilience Command Center"),
        "status": "healthy"
    }

@router.post("/query", response_model=TransformationResilienceCommandCenterQueryResultRead)
async def process_command_center_query(query: str = Query(...)):
    return await TransformationResilienceCommandCenterService.process_natural_language_command_center_query(None, query)

@router.get("/{id}", response_model=dict)
async def get_command_center(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    for cc in overview.get("commandCenters", []):
        if cc.get("id") == id:
            return cc
    return {"id": id, "name": "Global Enterprise Transformation Resilience Command Center 2.0", "status": "healthy"}

@router.get("/{id}/state", response_model=List[dict])
async def list_executive_states(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    return overview.get("executiveStates", [])

@router.get("/{id}/changes", response_model=List[dict])
async def list_changes(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    situations = overview.get("situations", [])
    if situations:
        return situations[0].get("changes_json", [])
    return ["Primary OAuth SLA Drift", "IAM Senior Engineer Capacity Bottleneck"]

@router.get("/{id}/priorities", response_model=List[dict])
async def list_priorities(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    return overview.get("priorities", [])

@router.get("/{id}/exposure", response_model=List[dict])
async def list_exposure_maps(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    return overview.get("exposureMaps", [])

@router.get("/{id}/systemic-risks", response_model=List[dict])
async def list_systemic_risks(id: str):
    return [
        {
            "id": "srisk_cc_01",
            "source_dependency": "Central OAuth Gateway API",
            "affected_scope": ["Wave 2 FinOps", "Wave 3 SSO", "Wave 4 HR Migration"],
            "severity": "critical"
        }
    ]

@router.get("/{id}/dependencies", response_model=List[dict])
async def list_dependencies(id: str):
    return [
        {
            "id": "dep_cc_01",
            "dependency_name": "Central IAM OAuth Federation Gateway v2",
            "criticality": 0.96,
            "concentration": "high"
        }
    ]

@router.get("/{id}/capacity", response_model=dict)
async def get_capacity_summary(id: str):
    return {
        "capacityResource": "Senior IAM Security Engineers",
        "requiredCapacity": 45.0,
        "availableCapacity": 30.0,
        "contentionScore": 0.88,
        "margin": "-15.0 FTE"
    }

@router.get("/{id}/recovery", response_model=dict)
async def get_recovery_readiness(id: str):
    return {
        "commandCenterId": id,
        "recoveryReadinessScore": 0.95,
        "activeRecoveryPathsCount": 4,
        "primaryBottleneck": "Active-Active IAM Gateway Funding Delay"
    }

@router.get("/{id}/investment-reviews", response_model=List[dict])
async def list_investment_reviews(id: str):
    return [
        {
            "id": "inv_rev_cc_01",
            "affected_investment_id": "pinv_01",
            "reason": "Key assumption 'Primary Auth Gateway SLA >= 99.99%' drifted to degraded status.",
            "severity": "high",
            "deadline": "2026-Q3"
        }
    ]

@router.get("/{id}/decision-reviews", response_model=List[dict])
async def list_decision_reviews(id: str):
    return [
        {
            "id": "dec_rev_cc_01",
            "decision_case": "IAM Active-Active Federation Architecture Decision",
            "evidence_status": "conflict_detected",
            "assumption_status": "degraded"
        }
    ]

@router.post("/{id}/simulations", response_model=dict)
async def trigger_simulation(id: str, data: dict):
    return await TransformationResilienceCommandCenterService.trigger_simulation(None, id, data)

@router.post("/{id}/decision-packets", response_model=dict)
async def create_decision_packet(id: str, data: dict):
    return await TransformationResilienceCommandCenterService.create_decision_packet(None, id, data)

@router.get("/{id}/trends", response_model=List[dict])
async def list_trends(id: str):
    return [
        {"dimension": "recoverability", "trend": "improving", "window": "30d"},
        {"dimension": "observability", "trend": "deteriorating", "window": "30d"}
    ]

@router.get("/{id}/forecasts", response_model=List[dict])
async def list_forecasts(id: str):
    return [
        {"target_metric": "Shared Dependency Recovery Margin", "forecast_value": 0.84, "uncertainty": "±0.06"}
    ]

@router.get("/{id}/evidence", response_model=dict)
async def get_evidence_summary(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    return overview.get("evidenceSummary", {})

@router.get("/{id}/lessons", response_model=List[dict])
async def list_unapplied_lessons(id: str):
    overview = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
    return overview.get("unappliedLessons", [])

@router.get("/{id}/timeline", response_model=List[dict])
async def get_timeline(id: str):
    return [
        {"timestamp": "2026-08-13T10:00:00Z", "event_type": "signal_detected", "summary": "OAuth P99 Latency reached 142.5ms"},
        {"timestamp": "2026-08-13T10:15:00Z", "event_type": "drift_flagged", "summary": "Persistent drift flagged on Identity Gateway"},
        {"timestamp": "2026-08-13T10:30:00Z", "event_type": "priority_created", "summary": "Priority Item created: Shared IAM OAuth Gateway Bottleneck"},
        {"timestamp": "2026-08-13T11:00:00Z", "event_type": "decision_packet_generated", "summary": "Decision Packet dp_01 generated for pinv_01 funding review"}
    ]
