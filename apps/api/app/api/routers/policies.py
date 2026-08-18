from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, require_admin, WorkspaceContext
from app.schemas.policies import (
    PolicyRuleCreate,
    PolicyRuleResponse,
    PolicyEvaluationRequest,
    PolicyDecisionResponse
)
from app.services import policy_engine

router = APIRouter()

@router.get("/policies/rules", response_model=List[PolicyRuleResponse])
async def list_rules(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[PolicyRuleResponse]:
    rules = await policy_engine.list_policy_rules(db, ws_ctx.workspace_id)
    return [PolicyRuleResponse(**r) for r in rules]

@router.post("/policies/rules", response_model=PolicyRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    payload: PolicyRuleCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> PolicyRuleResponse:
    rule = await policy_engine.create_policy_rule(
        db, workspace_id=ws_ctx.workspace_id, name=payload.name, action=payload.action, conditions=payload.conditions, priority=payload.priority
    )
    return PolicyRuleResponse(**rule)

@router.post("/policies/evaluate", response_model=PolicyDecisionResponse)
async def evaluate_dry_run(
    payload: PolicyEvaluationRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> PolicyDecisionResponse:
    ctx = policy_engine.PolicyContext(
        workspace_id=ws_ctx.workspace_id,
        user_id=ws_ctx.user_id,
        tool_name=payload.tool_name,
        agent_run_id=payload.agent_run_id,
        mission_id=payload.mission_id,
        tool_input=payload.tool_input,
        risk_level=payload.risk_level,
        autonomy_level=payload.autonomy_level,
        user_role=ws_ctx.role,
        user_status=payload.user_status,
        resource_scope=payload.resource_scope
    )
    decision = await policy_engine.evaluate_policy(db, ctx)
    return PolicyDecisionResponse(
        decision=decision.decision,
        risk_level=decision.risk_level,
        reason=decision.reason,
        required_approval_type=decision.required_approval_type,
        rule_id=decision.rule_id
    )
