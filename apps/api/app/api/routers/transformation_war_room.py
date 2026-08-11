from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_war_room import (
    TransformationWarRoomRead,
    TransformationWarRoomLiveStateRead,
    TransformationPlanVarianceRead,
    TransformationDeviationRead,
    TransformationRootCauseHypothesisRead,
    TransformationLiveImpactAssessmentRead,
    TransformationInterventionOptionRead,
    TransformationInterventionRecommendationRead,
    TransformationWarRoomEscalationRead,
    TransformationResponsePlanRead,
    TransformationResponseCheckpointRead,
    TransformationTrajectoryRead,
    TransformationEarlyWarningRead,
    TransformationSituationSummaryRead,
    TransformationWarRoomQueryResultRead
)
from app.services.transformation_war_room_service import TransformationWarRoomService

router = APIRouter(prefix="/api/v1/transformation-war-room", tags=["transformation_war_room"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_war_room_overview():
    return await TransformationWarRoomService.get_war_room_overview(None)

@router.post("", response_model=dict)
async def create_war_room(data: dict):
    return {"id": "wr_new", "name": data.get("name", "New War Room"), "status": "monitoring", "priority": "high"}

@router.get("/{id}", response_model=dict)
async def get_war_room(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    for w in overview.get("warRooms", []):
        if w.get("id") == id:
            return w
    return {"id": id, "name": "Global Operations War Room", "status": "monitoring"}

@router.patch("/{id}", response_model=dict)
async def update_war_room(id: str, data: dict):
    return {"id": id, "updated": True, "status": data.get("status", "attention")}

@router.get("/{id}/live-state", response_model=dict)
async def get_live_state(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("liveStates", [{}])[0]

@router.get("/{id}/timeline", response_model=List[dict])
async def get_war_room_timeline(id: str):
    return [
        {"event": "Signal Detected", "timestamp": "2026-08-11T18:00:00Z", "details": "14-day schedule slip in Wave 2 FinOps migration"},
        {"event": "Deviation Correlated", "timestamp": "2026-08-11T18:05:00Z", "details": "IAM capacity shortfall + CISO review backlog"},
        {"event": "Intervention Simulated", "timestamp": "2026-08-11T18:15:00Z", "details": "IO-01 simulation confirms 14-day schedule recovery"},
        {"event": "Response Plan Prepared", "timestamp": "2026-08-11T18:30:00Z", "details": "RP-01 submitted for Steering Committee Approval"}
    ]

@router.get("/{id}/deviations", response_model=List[dict])
async def list_deviations(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("deviations", [])

@router.get("/{id}/warnings", response_model=List[dict])
async def list_early_warnings(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("earlyWarnings", [])

@router.get("/{id}/impacts", response_model=List[dict])
async def list_impacts(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("impacts", [])

@router.get("/{id}/root-causes", response_model=List[dict])
async def list_root_causes(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("rootCauses", [])

@router.get("/{id}/interventions", response_model=List[dict])
async def list_interventions(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("interventions", [])

@router.post("/{id}/interventions", response_model=dict)
async def create_intervention(id: str, data: dict):
    return {"id": "io_new", "warRoomId": id, "status": "proposed", "title": data.get("title", "Proposed Intervention")}

@router.get("/{id}/interventions/{interventionId}", response_model=dict)
async def get_intervention(id: str, interventionId: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    for io in overview.get("interventions", []):
        if io.get("id") == interventionId:
            return io
    return {"id": interventionId, "status": "proposed"}

@router.post("/{id}/interventions/{interventionId}/simulate", response_model=dict)
async def simulate_intervention(id: str, interventionId: str):
    return {"interventionId": interventionId, "simulationCompleted": True, "scheduleRecoveryDays": 14, "riskScore": 0.08}

@router.post("/{id}/interventions/{interventionId}/compare", response_model=dict)
async def compare_intervention(id: str, interventionId: str):
    return {"interventionId": interventionId, "baselineScheduleSlipDays": 14, "interventionScheduleRecoveryDays": 14, "costDiff": 150000.0}

@router.post("/{id}/interventions/{interventionId}/recommend", response_model=dict)
async def recommend_intervention(id: str, interventionId: str):
    return {"interventionId": interventionId, "status": "recommended", "recommendationGenerated": True}

@router.get("/{id}/response-plans", response_model=List[dict])
async def list_response_plans(id: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    return overview.get("responsePlans", [])

@router.post("/{id}/response-plans", response_model=dict)
async def create_response_plan(id: str, data: dict):
    return {"id": "rp_new", "warRoomId": id, "status": "draft", "title": data.get("title", "New Response Plan")}

@router.get("/{id}/response-plans/{planId}", response_model=dict)
async def get_response_plan(id: str, planId: str):
    overview = await TransformationWarRoomService.get_war_room_overview(None)
    for rp in overview.get("responsePlans", []):
        if rp.get("id") == planId:
            return rp
    return {"id": planId, "status": "draft"}

@router.post("/{id}/response-plans/{planId}/submit", response_model=dict)
async def submit_response_plan(id: str, planId: str):
    return {"id": planId, "status": "awaiting_approval"}

@router.post("/{id}/response-plans/{planId}/approve", response_model=dict)
async def approve_response_plan(id: str, planId: str):
    return {"id": planId, "status": "approved", "approver": "Transformation Steering Committee"}

@router.post("/{id}/response-plans/{planId}/execute", response_model=dict)
async def execute_response_plan(id: str, planId: str):
    return {"id": planId, "status": "executing", "actionGatewayDispatched": True}

@router.post("/{id}/response-plans/{planId}/verify", response_model=dict)
async def verify_response_plan(id: str, planId: str):
    return {"id": planId, "status": "verified", "varianceVerified": True}

@router.post("/query", response_model=TransformationWarRoomQueryResultRead)
async def process_war_room_query(query: str = Query(...)):
    return await TransformationWarRoomService.process_natural_language_situation_query(None, query)
