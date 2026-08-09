from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentDefinitionCreate(BaseModel):
    name: str = Field(..., description="Agent definition name")
    description: str = Field("", description="Agent definition description")
    visibility: str = Field("workspace", description="Visibility: private, workspace, mission")
    default_purpose: str = Field("", description="Default agent purpose")

class AgentDefinitionResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: str
    created_by: str
    visibility: str
    default_purpose: str
    status: str
    created_at: str
    updated_at: str

class AgentDelegationCreate(BaseModel):
    agent_id: Optional[str] = Field(None, description="Target AgentDefinition ID")
    mission_id: Optional[str] = Field(None, description="Target Mission ID scope")
    scope: str = Field("mission", description="Scope: mission, workspace, resource, tool")
    permissions: Optional[List[str]] = Field(default_factory=lambda: ["read_context", "create_draft"])
    allowed_tools: Optional[List[str]] = Field(default_factory=list, description="Whitelist of allowed tools")
    allowed_resources: Optional[List[str]] = Field(default_factory=list, description="Whitelist of allowed resources")
    autonomy_level: str = Field("FULL_AUTONOMY", description="FULL_AUTONOMY, HUMAN_IN_THE_LOOP, ADVISORY_ONLY")
    expires_at: Optional[str] = Field(None, description="Expiration ISO string")

class AgentDelegationResponse(BaseModel):
    id: str
    workspace_id: str
    delegated_by: str
    agent_id: str
    mission_id: Optional[str] = None
    scope: str
    permissions: List[str]
    allowed_tools: List[str]
    allowed_resources: List[str]
    autonomy_level: str
    expires_at: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

class AgentHandoffCreate(BaseModel):
    source_agent_run_id: str = Field(..., description="Source AgentRun ID")
    target_agent_definition_id: str = Field(..., description="Target AgentDefinition ID")
    mission_id: str = Field(..., description="Mission ID")
    scope: str = Field("mission", description="Scope")
    input_reference: Dict[str, Any] = Field(default_dict={}, description="Handoff input data reference")
    current_depth: int = Field(1, description="Current handoff depth")

class AgentHandoffResponse(BaseModel):
    id: str
    source_agent_run_id: str
    target_agent_definition_id: str
    mission_id: str
    scope: str
    input_reference: Dict[str, Any]
    depth: int
    status: str
    created_at: str
    completed_at: Optional[str] = None
