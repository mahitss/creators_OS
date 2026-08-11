from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_recovery import (
    TransformationRecoveryDomainRead,
    TransformationDisruptionRead,
    TransformationRecoveryImpactRead,
    TransformationRecoveryCriticalityRead,
    TransformationRecoveryPriorityRead,
    TransformationProtectionTargetRead,
    TransformationRecoveryObjectiveRead,
    TransformationRecoveryPathRead,
    TransformationRecoveryOptionRead,
    TransformationRecoveryBottleneckRead,
    TransformationRecoveryTrajectoryRead,
    TransformationRecoveryComparisonRead,
    TransformationRecoveryCheckpointRead,
    TransformationRecoveryGateRead,
    TransformationReturnToNormalPlanRead,
    TransformationRecoveryDriftRead,
    TransformationRecoveryEscalationRead,
    TransformationRecoveryCommunicationRead,
    TransformationResilienceGapRead,
    TransformationResilienceImprovementRead,
    TransformationRecoveryReadinessRead,
    TransformationRecoveryDrillRead,
    TransformationRecoveryQueryResultRead
)
from app.services.transformation_recovery_service import TransformationRecoveryService

router = APIRouter(prefix="/api/v1/transformation-recovery", tags=["transformation_recovery"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_recovery_overview():
    return await TransformationRecoveryService.get_recovery_overview(None)

@router.post("", response_model=dict)
async def create_recovery_domain(data: dict):
    return {"id": "rd_new", "name": data.get("name", "New Recovery Domain"), "status": "prepared", "version": "v2.0"}

@router.get("/drills", response_model=List[dict])
async def list_drills():
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("drills", [])

@router.post("/drills", response_model=dict)
async def create_drill(data: dict):
    return {"id": "drill_new", "drillName": data.get("drillName", "New Drill"), "noProductionMutation": True}

@router.get("/drills/{id}", response_model=dict)
async def get_drill(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    for d in overview.get("drills", []):
        if d.get("id") == id:
            return d
    return {"id": id, "noProductionMutation": True}

@router.post("/drills/{id}/run", response_model=dict)
async def run_drill(id: str):
    return {"drillId": id, "status": "completed", "noProductionMutation": True, "simulatedRecoveryHours": 42.0}

@router.get("/drills/{id}/results", response_model=dict)
async def get_drill_results(id: str):
    return {"drillId": id, "results": {"simulated_recovery_time_hours": 42.0, "zero_production_mutation": True}}

@router.get("/{id}", response_model=dict)
async def get_recovery_domain(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    for d in overview.get("domains", []):
        if d.get("id") == id:
            return d
    return {"id": id, "name": "Enterprise Core IAM & FinOps Resilience Domain", "status": "recovery_active"}

@router.get("/{id}/status", response_model=dict)
async def get_domain_status(id: str):
    return {"domainId": id, "status": "recovery_active", "version": "v2.0"}

@router.get("/{id}/disruptions", response_model=List[dict])
async def list_disruptions(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("disruptions", [])

@router.get("/{id}/impact", response_model=List[dict])
async def list_impacts(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("impacts", [])

@router.get("/{id}/paths", response_model=List[dict])
async def list_recovery_paths(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("paths", [])

@router.post("/{id}/paths", response_model=dict)
async def create_recovery_path(id: str, data: dict):
    return {"id": "path_new", "domainId": id, "pathName": data.get("pathName", "New Recovery Path"), "status": "proposed"}

@router.get("/{id}/paths/{pathId}", response_model=dict)
async def get_recovery_path(id: str, pathId: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    for p in overview.get("paths", []):
        if p.get("id") == pathId:
            return p
    return {"id": pathId, "status": "proposed"}

@router.post("/{id}/paths/{pathId}/simulate", response_model=dict)
async def simulate_recovery_path(id: str, pathId: str):
    return {"pathId": pathId, "simulationCompleted": True, "estimatedRecoveryHours": 48.0, "riskScore": 0.08}

@router.get("/{id}/paths/{pathId}/compare", response_model=dict)
async def compare_recovery_path(id: str, pathId: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("comparisons", [{}])[0]

@router.get("/{id}/checkpoints", response_model=List[dict])
async def list_checkpoints(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("checkpoints", [])

@router.get("/{id}/gates", response_model=List[dict])
async def list_gates(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("gates", [])

@router.get("/{id}/trajectory", response_model=List[dict])
async def list_trajectories(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("trajectories", [])

@router.get("/{id}/bottlenecks", response_model=List[dict])
async def list_bottlenecks(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("bottlenecks", [])

@router.get("/{id}/readiness", response_model=dict)
async def get_readiness(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("readinesses", [{}])[0]

@router.get("/{id}/return-to-normal", response_model=dict)
async def get_return_to_normal(id: str):
    overview = await TransformationRecoveryService.get_recovery_overview(None)
    return overview.get("returnPlans", [{}])[0]

@router.post("/{id}/return-to-normal/verify", response_model=dict)
async def verify_return_to_normal(id: str):
    return {"domainId": id, "verified": True, "status": "verified"}

@router.post("/{id}/close", response_model=dict)
async def close_recovery(id: str):
    return {"domainId": id, "status": "closed", "closedAt": "2026-08-11T20:30:00Z"}

@router.post("/query", response_model=TransformationRecoveryQueryResultRead)
async def process_recovery_query(query: str = Query(...)):
    return await TransformationRecoveryService.process_natural_language_recovery_query(None, query)
