from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_assurance_command import (
    TransformationResilienceAssuranceCommandDomainRead,
    TransformationResilienceAssuranceOperationalPictureRead,
    TransformationResilienceAssuranceCommandEventRead,
    TransformationResilienceAssuranceCommandPriorityRead,
    TransformationResilienceAssuranceCriticalObjectRead,
    TransformationResilienceAssuranceCommandAttentionRead,
    TransformationResilienceAssuranceExecutiveDecisionQueueRead,
    TransformationResilienceAssuranceDecisionBottleneckRead,
    TransformationResilienceAssuranceApprovalBottleneckRead,
    TransformationResilienceAssuranceInterventionBottleneckRead,
    TransformationResilienceAssuranceDependencyHotspotRead,
    TransformationResilienceAssuranceResourcePressureRead,
    TransformationResilienceAssuranceKnowledgeHealthProjectionRead,
    TransformationResilienceAssurancePlanHealthProjectionRead,
    TransformationResilienceAssuranceTransformationHealthProjectionRead,
    TransformationResilienceAssuranceCrossDomainHeatmapRead,
    TransformationResilienceAssuranceOperationalSceneRead,
    TransformationResilienceAssuranceSceneTimelineRead,
    TransformationResilienceAssuranceSceneRelationshipRead,
    TransformationResilienceAssuranceCommandSnapshotRead,
    TransformationResilienceAssuranceCommandSnapshotDiffRead,
    TransformationResilienceAssuranceCommandEscalationRead,
    TransformationResilienceAssuranceOperationsHandoffRead,
    TransformationResilienceAssuranceCommandProjectionHealthRead,
    TransformationResilienceAssuranceCommandQueryResultRead
)
from app.services.transformation_resilience_assurance_command_service import TransformationResilienceAssuranceCommandService

router = APIRouter(prefix="/api/v1/transformation-resilience-assurance-command", tags=["transformation_resilience_assurance_command"])

@router.get("", response_model=dict)
@router.get("/status", response_model=dict)
async def get_assurance_command_status():
    return await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)

@router.post("/query", response_model=TransformationResilienceAssuranceCommandQueryResultRead)
async def process_assurance_command_query(query: str = Query(...)):
    return await TransformationResilienceAssuranceCommandService.process_natural_language_assurance_command_query(None, query)

@router.get("/critical", response_model=List[dict])
async def list_critical_objects():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("criticalObjects", [])

@router.get("/decisions", response_model=List[dict])
async def list_executive_decisions():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("executiveDecisionQueues", [])

@router.get("/interventions", response_model=List[dict])
async def list_command_interventions():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("interventionBottlenecks", [])

@router.get("/warnings", response_model=List[dict])
async def list_command_warnings():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("commandEvents", [])

@router.get("/dependencies", response_model=List[dict])
async def list_dependency_hotspots():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("dependencyHotspots", [])

@router.get("/scenes", response_model=List[dict])
async def list_operational_scenes():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("operationalScenes", [])

@router.get("/snapshots", response_model=List[dict])
async def list_command_snapshots():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("snapshots", [])

@router.post("/snapshots", response_model=dict)
async def create_command_snapshot(data: dict):
    label = data.get("label", "Manual Operations Center Snapshot")
    return await TransformationResilienceAssuranceCommandService.create_command_snapshot(None, label)

@router.get("/snapshots/{id}", response_model=dict)
async def get_command_snapshot(id: str):
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    for snap in overview.get("snapshots", []):
        if snap.get("id") == id:
            return snap
    return {"id": id, "label": "Point-in-Time Snapshot", "state_data_json": {}}

@router.get("/snapshots/{id}/diff", response_model=dict)
async def get_snapshot_diff(id: str):
    return await TransformationResilienceAssuranceCommandService.diff_command_snapshots(None, "csnap_01", id)

@router.get("/escalations", response_model=List[dict])
async def list_escalations():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("escalations", [])

@router.post("/escalations/{id}/acknowledge", response_model=dict)
async def acknowledge_escalation(id: str):
    return {"id": id, "status": "acknowledged", "message": "Escalation acknowledged by Assurance Operations Controller."}

@router.get("/handoffs", response_model=List[dict])
async def list_handoffs():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    return overview.get("handoffs", [])

@router.post("/handoffs", response_model=dict)
async def create_handoff(data: dict):
    return {
        "id": "ohand_new",
        "outgoing_owner": data.get("outgoing_owner", "Outgoing Controller"),
        "incoming_owner": data.get("incoming_owner", "Incoming Controller"),
        "current_state_summary": data.get("current_state_summary", "Operational handoff recorded."),
        "status": "completed"
    }

@router.get("/projection-health", response_model=dict)
async def get_projection_health():
    overview = await TransformationResilienceAssuranceCommandService.get_assurance_command_overview(None)
    phealths = overview.get("projectionHealths", [])
    if phealths:
        return phealths[0]
    return {"id": "phealth_01", "rebuild_status": "idle", "lag_seconds": 0.0}

@router.post("/projection-health/rebuild", response_model=dict)
async def rebuild_projection():
    return await TransformationResilienceAssuranceCommandService.rebuild_projections(None)
