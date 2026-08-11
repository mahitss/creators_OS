from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_control import (
    TransformationControlTowerRead,
    TransformationLiveStateRead,
    TransformationControlSignalRead,
    TransformationSituationRead,
    TransformationRootCauseAssessmentRead,
    TransformationWaveReadinessRead,
    TransformationChangeRequestRead,
    TransformationIncidentRead,
    TransformationEscalationRead,
    TransformationWeeklyReviewRead,
    TransformationControlQueryResultRead
)
from app.services.transformation_control_service import TransformationControlService

router = APIRouter(prefix="/api/v1/transformation-control", tags=["transformation_control"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_control_overview():
    return await TransformationControlService.get_control_overview(None)

@router.get("/towers", response_model=List[dict])
async def list_towers():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("towers", [])

@router.get("/live-state", response_model=List[dict])
async def list_live_states():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("liveStates", [])

@router.get("/signals", response_model=List[dict])
async def list_signals():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("signals", [])

@router.get("/situations", response_model=List[dict])
async def list_situations():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("situations", [])

@router.get("/root-causes", response_model=List[dict])
async def list_root_causes():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("rootCauses", [])

@router.get("/waves", response_model=List[dict])
async def list_waves():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("waveReadinesses", [])

@router.get("/change-requests", response_model=List[dict])
async def list_change_requests():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("changeRequests", [])

@router.get("/incidents", response_model=List[dict])
async def list_incidents():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("incidents", [])

@router.get("/escalations", response_model=List[dict])
async def list_escalations():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("escalations", [])

@router.get("/reviews", response_model=List[dict])
async def list_reviews():
    overview = await TransformationControlService.get_control_overview(None)
    return overview.get("weeklyReviews", [])

@router.post("/change-requests/{request_id}/approve", response_model=dict)
async def approve_change_request(request_id: str, actor_id: str = Query("usr_chief_transformation_officer")):
    return await TransformationControlService.approve_change_request(None, request_id, actor_id)

@router.post("/change-requests/{request_id}/execute", response_model=dict)
async def execute_change_request(request_id: str):
    return await TransformationControlService.execute_change_request(None, request_id)

@router.post("/query", response_model=TransformationControlQueryResultRead)
async def process_control_query(query: str = Query(...)):
    return await TransformationControlService.process_natural_language_control_query(None, query)
