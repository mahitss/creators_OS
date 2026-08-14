from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PolicyRuleCreate(BaseModel):
    name: str = Field(..., description="Name of the custom policy rule")
    action: str = Field(..., description="Action: ALLOW, DENY, APPROVAL_REQUIRED")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Matching conditions e.g. tool_name, risk_level")
    priority: int = Field(10, description="Rule priority (higher priority evaluated first)")

class PolicyRuleResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    action: str
    conditions: Dict[str, Any]
    is_active: bool
    priority: int
    created_at: str
    updated_at: str

class PolicyEvaluationRequest(BaseModel):
    tool_name: str
    user_id: Optional[str] = "usr_alex"
    agent_run_id: Optional[str] = None
    mission_id: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    risk_level: Optional[str] = "READ"
    autonomy_level: Optional[str] = "FULL_AUTONOMY"
    user_role: Optional[str] = "member"
    user_status: Optional[str] = "active"
    resource_scope: Optional[str] = "workspace"

class PolicyDecisionResponse(BaseModel):
    decision: str
    risk_level: str
    reason: str
    required_approval_type: str
    rule_id: Optional[str] = None
