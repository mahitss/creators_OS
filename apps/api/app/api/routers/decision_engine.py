from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.decision_engine import (
    DecisionCreate,
    DecisionRead,
    DecisionClaimRead,
    DecisionEvidenceRead,
    EvidenceConflictRead,
    DecisionOptionRead,
    DecisionTradeoffRead,
    DecisionRiskRead,
    DecisionAnalyzeRequest,
    DecisionScenarioCreate,
    DecisionScenarioRead,
    DecisionApprovalRequest,
    DecisionOverrideRequest,
    DecisionOutcomeCreate,
    DecisionOutcomeRead
)
from app.services import decision_engine_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext

router = APIRouter(prefix="/decisions", tags=["Enterprise Decision Intelligence 2.0 & Evidence-Backed Agent Decision Engine"])

@router.get("", response_model=List[DecisionRead])
async def list_decisions(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists workspace decisions."""
    return await decision_engine_service.list_decisions(db, workspace_id=ws_ctx.workspace_id)

@router.post("", response_model=DecisionRead)
async def create_decision(
    req: DecisionCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new decision with evidence gathering and option generation."""
    return await decision_engine_service.create_decision(
        db, workspace_id=ws_ctx.workspace_id, user_id=ws_ctx.user_id, req=req
    )

@router.get("/{decision_id}", response_model=DecisionRead)
async def get_decision(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Gets decision details by ID."""
    dec = await decision_engine_service.get_decision_by_id(db, decision_id=decision_id)
    if not dec:
        raise HTTPException(status_code=404, detail="Decision not found")
    return dec

@router.get("/{decision_id}/evidence", response_model=List[DecisionEvidenceRead])
async def get_decision_evidence(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns supporting and contradicting evidence items."""
    return await decision_engine_service.get_evidence(db, decision_id=decision_id)

@router.get("/{decision_id}/options", response_model=List[DecisionOptionRead])
async def get_decision_options(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns generated decision options."""
    return await decision_engine_service.get_options(db, decision_id=decision_id)

@router.get("/{decision_id}/risks", response_model=List[DecisionRiskRead])
async def get_decision_risks(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns multi-dimensional risk evaluations for options."""
    return await decision_engine_service.get_risks(db, decision_id=decision_id)

@router.get("/{decision_id}/outcome", response_model=DecisionOutcomeRead)
async def get_decision_outcome(
    decision_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns expected vs actual outcome tracking."""
    out = await decision_engine_service.get_outcome(db, decision_id=decision_id)
    if not out:
        raise HTTPException(status_code=404, detail="Decision outcome tracking not found")
    return out

@router.post("/{decision_id}/analyze", response_model=DecisionRead)
async def analyze_decision(
    decision_id: str,
    req: DecisionAnalyzeRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Performs deep evidence analysis, claim classification, and trade-off evaluation."""
    return await decision_engine_service.analyze_decision(
        db, decision_id=decision_id, req=req
    )

@router.post("/{decision_id}/scenarios", response_model=DecisionScenarioRead)
async def create_scenario(
    decision_id: str,
    req: DecisionScenarioCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Performs non-destructive scenario analysis ('what-if' simulation)."""
    return await decision_engine_service.create_scenario(
        db, decision_id=decision_id, req=req
    )

@router.post("/{decision_id}/approve", response_model=DecisionRead)
async def approve_decision(
    decision_id: str,
    req: DecisionApprovalRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Approves a recommended decision option."""
    return await decision_engine_service.approve_decision(
        db, decision_id=decision_id, req=req, approver_id=ws_ctx.user_id
    )

@router.post("/{decision_id}/override", response_model=DecisionRead)
async def override_decision(
    decision_id: str,
    req: DecisionOverrideRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Performs human override of AI recommendation while preserving original state in audit trail."""
    return await decision_engine_service.override_decision(
        db, decision_id=decision_id, req=req, actor_id=ws_ctx.user_id
    )
