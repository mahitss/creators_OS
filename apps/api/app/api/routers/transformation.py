from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation import (
    TransformationProgramRead,
    TransformationDriverRead,
    OperatingModelCurrentStateRead,
    OperatingModelTargetStateRead,
    OperatingModelDeltaRead,
    FutureOperatingModelRead,
    OperatingModelDesignOptionRead,
    OperatingModelComparisonRead,
    TransformationScenarioRead,
    TransformationRoadmapRead,
    TransformationDecisionGateRead,
    TransformationPilotRead,
    TransformationChangeProposalRead,
    TransformationQueryResultRead
)
from app.services.transformation_service import TransformationService

router = APIRouter(prefix="/api/v1/transformation", tags=["transformation"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_transformation_overview():
    return await TransformationService.get_transformation_overview(None)

@router.get("/programs", response_model=List[dict])
async def list_programs():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("programs", [])

@router.get("/drivers", response_model=List[dict])
async def list_drivers():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("drivers", [])

@router.get("/deltas", response_model=List[dict])
async def list_deltas():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("deltas", [])

@router.get("/design-options", response_model=List[dict])
async def list_design_options():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("designOptions", [])

@router.get("/future-models", response_model=List[dict])
async def list_future_models():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("futureModels", [])

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("scenarios", [])

@router.get("/roadmaps", response_model=List[dict])
async def list_roadmaps():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("roadmaps", [])

@router.get("/gates", response_model=List[dict])
async def list_gates():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("gates", [])

@router.get("/pilots", response_model=List[dict])
async def list_pilots():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("pilots", [])

@router.get("/change-proposals", response_model=List[dict])
async def list_change_proposals():
    overview = await TransformationService.get_transformation_overview(None)
    return overview.get("changeProposals", [])

@router.post("/change-proposals/{proposal_id}/approve", response_model=dict)
async def approve_change_proposal(proposal_id: str, actor_id: str = Query("usr_chief_transformation_officer")):
    return await TransformationService.approve_change_proposal(None, proposal_id, actor_id)

@router.post("/change-proposals/{proposal_id}/execute", response_model=dict)
async def execute_change_proposal(proposal_id: str):
    return await TransformationService.execute_change_proposal(None, proposal_id)

@router.post("/query", response_model=TransformationQueryResultRead)
async def process_transformation_query(query: str = Query(...)):
    return await TransformationService.process_natural_language_transformation_query(None, query)
