from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.operating_model import (
    OperatingModelRead,
    OrganizationalUnitRead,
    DecisionRightRead,
    DecisionRightsMatrixRead,
    OperatingProcessRead,
    ProcessHandoffRead,
    OperatingModelGapRead,
    OperatingModelChangeProposalRead,
    OperatingModelQueryResultRead
)
from app.services.operating_model_service import OperatingModelService

router = APIRouter(prefix="/api/v1/operating-model", tags=["operating_model"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_operating_model_overview():
    return await OperatingModelService.get_operating_model_overview(None)

@router.get("/units", response_model=List[dict])
async def list_units():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("units", [])

@router.get("/decision-rights", response_model=List[dict])
async def list_decision_rights():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("decisionRights", [])

@router.get("/processes", response_model=List[dict])
async def list_processes():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("processes", [])

@router.get("/handoffs", response_model=List[dict])
async def list_handoffs():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("handoffs", [])

@router.get("/gaps", response_model=List[dict])
async def list_gaps():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("gaps", [])

@router.get("/drift", response_model=List[dict])
async def list_drifts():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("drifts", [])

@router.get("/change-proposals", response_model=List[dict])
async def list_change_proposals():
    overview = await OperatingModelService.get_operating_model_overview(None)
    return overview.get("changeProposals", [])

@router.post("/change-proposals/{proposal_id}/approve", response_model=dict)
async def approve_change_proposal(proposal_id: str, actor_id: str = Query("usr_chief_operating_officer")):
    return await OperatingModelService.approve_change_proposal(None, proposal_id, actor_id)

@router.post("/change-proposals/{proposal_id}/execute", response_model=dict)
async def execute_change_proposal(proposal_id: str):
    return await OperatingModelService.execute_change_proposal(None, proposal_id)

@router.post("/query", response_model=OperatingModelQueryResultRead)
async def process_operating_query(query: str = Query(...)):
    return await OperatingModelService.process_natural_language_operating_query(None, query)
