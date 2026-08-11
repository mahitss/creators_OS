from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.workflow_ai import (
    WorkflowAIRequestCreate,
    WorkflowProposalRead,
    WorkflowExplainRequest,
    WorkflowExplainResponse,
    WorkflowDebugRequest,
    WorkflowDebugResponse,
    WorkflowOptimizeRequest,
    WorkflowOptimizationResponse,
    WorkflowSimulationRequest,
    WorkflowSimulationResponse,
    WorkflowReadinessResponse,
    WorkflowTestCaseCreate,
    WorkflowTestCaseRead
)
from app.services import workflow_ai_service

router = APIRouter(prefix="/workflows", tags=["workflow_ai"])

@router.post("/ai", response_model=WorkflowProposalRead, status_code=201)
async def request_ai_workflow(
    request_in: WorkflowAIRequestCreate,
    x_user_id: str = Header("usr_default_owner", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Processes natural language request to generate a structured workflow proposal."""
    try:
        proposal = await workflow_ai_service.generate_workflow_proposal(session, request_in, user_id=x_user_id)
        return proposal
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{workflow_id}/ai/explain", response_model=WorkflowExplainResponse)
async def explain_workflow(
    workflow_id: str,
    explain_in: Optional[WorkflowExplainRequest] = None,
    session: AsyncSession = Depends(get_db)
):
    """Generates structured explanation of workflow nodes, branches, and capability access."""
    try:
        sel_id = explain_in.selected_node_id if explain_in else None
        res = await workflow_ai_service.explain_workflow(session, workflow_id, selected_node_id=sel_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{workflow_id}/ai/debug", response_model=WorkflowDebugResponse)
async def debug_workflow(
    workflow_id: str,
    debug_in: WorkflowDebugRequest,
    session: AsyncSession = Depends(get_db)
):
    """Analyzes execution run logs and PolicyEngine decisions to categorize failures and recommend remediations."""
    res = await workflow_ai_service.debug_workflow_run(session, debug_in.run_id)
    return res

@router.post("/{workflow_id}/ai/optimize", response_model=WorkflowOptimizationResponse)
async def optimize_workflow(
    workflow_id: str,
    opt_in: Optional[WorkflowOptimizeRequest] = None,
    session: AsyncSession = Depends(get_db)
):
    """Generates cost, performance, and safety optimization proposals."""
    goal = opt_in.goal if opt_in else "balanced"
    try:
        res = await workflow_ai_service.optimize_workflow(session, workflow_id, goal=goal)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{workflow_id}/ai/simulate", response_model=WorkflowSimulationResponse)
async def simulate_workflow(
    workflow_id: str,
    sim_in: Optional[WorkflowSimulationRequest] = None,
    session: AsyncSession = Depends(get_db)
):
    """Simulates workflow execution across synthetic scenarios."""
    scenarios = sim_in.scenarios if sim_in else []
    try:
        res = await workflow_ai_service.simulate_workflow_scenarios(session, workflow_id, scenarios)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/proposals/{proposal_id}/accept")
async def accept_proposal(
    proposal_id: str,
    x_user_id: str = Header("usr_default_owner", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Accepts proposal, creating a new draft WorkflowVersion. Does NOT auto-publish production."""
    try:
        res = await workflow_ai_service.accept_proposal(session, proposal_id, user_id=x_user_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Rejects workflow proposal."""
    try:
        res = await workflow_ai_service.reject_proposal(session, proposal_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
