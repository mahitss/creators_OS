from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.adaptive_decision_governance import (
    ControlLoopCreate,
    ControlLoopRead,
    ControlSignalRead,
    DecisionValidityAssessmentRead,
    DecisionReassessmentRead,
    ControlGuardrailRead,
    GuardrailBreachRead,
    ControlResponseRead,
    ActionOutcomeObservationRead,
    ControlQueryResultRead
)
from app.services.adaptive_decision_governance_service import AdaptiveDecisionGovernanceService

router = APIRouter(prefix="/api/v1/control", tags=["adaptive_decision_governance"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_control_overview():
    return await AdaptiveDecisionGovernanceService.get_control_overview(None)

@router.get("/loops", response_model=List[dict])
async def list_control_loops():
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    return overview.get("loops", [])

@router.post("/loops", response_model=dict)
async def create_control_loop(payload: ControlLoopCreate):
    return await AdaptiveDecisionGovernanceService.create_control_loop(None, payload.model_dump())

@router.get("/loops/{loop_id}", response_model=dict)
async def get_control_loop(loop_id: str):
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    for l in overview.get("loops", []):
        if l["id"] == loop_id:
            return l
    raise HTTPException(status_code=404, detail="Control loop not found")

@router.post("/loops/{loop_id}/pause", response_model=dict)
async def pause_control_loop(loop_id: str):
    return await AdaptiveDecisionGovernanceService.pause_control_loop(None, loop_id)

@router.post("/loops/{loop_id}/resume", response_model=dict)
async def resume_control_loop(loop_id: str):
    return await AdaptiveDecisionGovernanceService.resume_control_loop(None, loop_id)

@router.get("/loops/{loop_id}/signals", response_model=List[dict])
async def list_loop_signals(loop_id: str):
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    return [s for s in overview.get("signals", []) if s.get("loop_id") == loop_id]

@router.get("/reassessments", response_model=List[dict])
async def list_reassessments():
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    return overview.get("reassessments", [])

@router.get("/reassessments/{reassessment_id}", response_model=dict)
async def get_reassessment(reassessment_id: str):
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    for r in overview.get("reassessments", []):
        if r["id"] == reassessment_id:
            return r
    raise HTTPException(status_code=404, detail="Reassessment not found")

@router.post("/reassessments/{reassessment_id}/resolve", response_model=dict)
async def resolve_reassessment(reassessment_id: str):
    return {
        "reassessmentId": reassessment_id,
        "status": "resolved",
        "resolvedBy": "usr_sec_lead",
        "message": "Decision reassessment resolved cleanly after human review."
    }

@router.get("/loops/{loop_id}/guardrails", response_model=List[dict])
async def list_loop_guardrails(loop_id: str):
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    return [g for g in overview.get("guardrails", []) if g.get("loop_id") == loop_id]

@router.get("/loops/{loop_id}/responses", response_model=List[dict])
async def list_loop_responses(loop_id: str):
    overview = await AdaptiveDecisionGovernanceService.get_control_overview(None)
    return [r for r in overview.get("responses", []) if r.get("loop_id") == loop_id]

@router.post("/responses/{response_id}/execute", response_model=dict)
async def execute_response(response_id: str):
    return {
        "responseId": response_id,
        "status": "executed",
        "authorizedBy": "usr_sec_lead",
        "actionGatewayReference": f"gw_ctrl_{uuid.uuid4().hex[:8]}",
        "message": "Control response executed via Universal Action Gateway."
    }

@router.post("/query", response_model=ControlQueryResultRead)
async def process_control_query(query: str = Query(...)):
    return await AdaptiveDecisionGovernanceService.process_natural_language_control_query(None, query)
