from typing import Optional, List, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.policies import (
    PolicyRuleCreate,
    PolicyRuleResponse,
    PolicyEvaluationRequest,
    PolicyDecisionResponse
)
from app.services import policy_engine

router = APIRouter()

DEFAULT_USER_ID = "usr_alex"
DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_auth_headers(
    x_user_id: Optional[str] = Header(None),
    x_workspace_id: Optional[str] = Header(None)
) -> Tuple[str, str]:
    user_id = x_user_id or DEFAULT_USER_ID
    workspace_id = x_workspace_id or DEFAULT_WORKSPACE_ID
    return user_id, workspace_id

@router.get("/policies/rules", response_model=List[PolicyRuleResponse])
async def list_rules(
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[PolicyRuleResponse]:
    _, ws_id = auth
    rules = await policy_engine.list_policy_rules(db, ws_id)
    return [PolicyRuleResponse(**r) for r in rules]

@router.post("/policies/rules", response_model=PolicyRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    payload: PolicyRuleCreate,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> PolicyRuleResponse:
    _, ws_id = auth
    rule = await policy_engine.create_policy_rule(
        db, workspace_id=ws_id, name=payload.name, action=payload.action, conditions=payload.conditions, priority=payload.priority
    )
    return PolicyRuleResponse(**rule)

@router.post("/policies/evaluate", response_model=PolicyDecisionResponse)
async def evaluate_dry_run(
    payload: PolicyEvaluationRequest,
    auth: Tuple[str, str] = Depends(get_auth_headers),
    db: Optional[AsyncSession] = Depends(get_db)
) -> PolicyDecisionResponse:
    user_id, ws_id = auth
    ctx = policy_engine.PolicyContext(
        workspace_id=ws_id,
        user_id=payload.user_id or user_id,
        tool_name=payload.tool_name,
        agent_run_id=payload.agent_run_id,
        mission_id=payload.mission_id,
        tool_input=payload.tool_input,
        risk_level=payload.risk_level,
        autonomy_level=payload.autonomy_level,
        user_role=payload.user_role,
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
