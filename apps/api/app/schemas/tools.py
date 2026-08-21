from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ToolCategoryEnum(str, Enum):
    READ = "READ"
    SEARCH = "SEARCH"
    DATA = "DATA"
    CONTENT = "CONTENT"
    COMMUNICATION = "COMMUNICATION"
    WORKFLOW = "WORKFLOW"
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"


class ToolRiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ToolDefinitionRead(BaseModel):
    id: str
    name: str
    description: str
    version: int = 1
    category: ToolCategoryEnum
    input_schema: Dict[str, Any] = Field(default_factory=dict, alias="inputSchema")
    output_schema: Dict[str, Any] = Field(default_factory=dict, alias="outputSchema")
    required_permissions: List[str] = Field(default_factory=list, alias="requiredPermissions")
    risk_level: ToolRiskLevelEnum = Field(default=ToolRiskLevelEnum.LOW, alias="riskLevel")
    timeout_ms: int = Field(default=30000, alias="timeoutMs")
    timeout_seconds: Optional[int] = Field(default=30, alias="timeoutSeconds")
    enabled: bool = True

    class Config:
        populate_by_name = True


class ToolListResponse(BaseModel):
    tools: List[ToolDefinitionRead]
    total: int


class AgentToolDiscoveryResponse(BaseModel):
    agent_id: str
    workspace_id: str
    authorized_tools: List[ToolDefinitionRead]
    denied_tools: List[Dict[str, Any]]
    total_authorized: int
    total_denied: int


class ToolCallAuditLogRead(BaseModel):
    id: str
    tool_id: str
    tool_name: str
    agent_run_id: Optional[str] = None
    mission_id: Optional[str] = None
    workspace_id: str
    user_id: str
    timestamp: str
    authorization_result: str
    policy_result: Dict[str, Any] = Field(default_factory=dict)
    duration_ms: int
    status: str
    error_code: Optional[str] = None
    idempotency_key: Optional[str] = None
    truncated: bool = False
    input_sanitized: Dict[str, Any] = Field(default_factory=dict)
    output_sanitized: Dict[str, Any] = Field(default_factory=dict)


class ToolAuditLogListResponse(BaseModel):
    logs: List[ToolCallAuditLogRead]
    total: int
