from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class WorkflowNodeSchema(BaseModel):
    id: str
    node_key: str
    type: str  # trigger, condition, branch, agent, tool, approval, delay, transform, notification, mission, end
    title: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Optional[Dict[str, float]] = None

class WorkflowEdgeSchema(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    condition_handle: Optional[str] = None

class WorkflowDefinitionSchema(BaseModel):
    nodes: List[WorkflowNodeSchema] = Field(default_factory=list)
    edges: List[WorkflowEdgeSchema] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)

class WorkflowCreate(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None
    visibility: str = "workspace"  # private, workspace, mission
    trigger_config: Dict[str, Any] = Field(default_factory=dict)
    definition: Optional[WorkflowDefinitionSchema] = None

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    trigger_config: Optional[Dict[str, Any]] = None
    definition: Optional[WorkflowDefinitionSchema] = None

class WorkflowRead(BaseModel):
    id: str
    workspace_id: str
    created_by: str
    name: str
    description: Optional[str] = None
    status: str
    version: int
    visibility: str
    trigger_config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class WorkflowVersionRead(BaseModel):
    id: str
    workflow_id: str
    version: int
    definition: Dict[str, Any]
    compiled_graph: Dict[str, Any]
    capabilities: List[str]
    created_by: str
    status: str
    created_at: datetime
    published_at: Optional[datetime] = None

class WorkflowValidationResponse(BaseModel):
    valid: bool
    errors: List[str]
    warnings: List[str]
    capabilities: List[str]
    node_count: int
    edge_count: int

class WorkflowPublishResponse(BaseModel):
    workflow_id: str
    version: int
    workflow_version_id: str
    capabilities: List[str]
    published_at: datetime

class WorkflowRunRead(BaseModel):
    id: str
    workflow_id: str
    workflow_version_id: str
    workspace_id: str
    trigger_event_id: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_node: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class WorkflowNodeRunRead(BaseModel):
    id: str
    workflow_run_id: str
    node_id: str
    node_key: str
    node_type: str
    status: str
    attempt: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: int
    result_reference: Dict[str, Any]
    error_code: Optional[str] = None
    created_at: datetime

class WorkflowDryRunRequest(BaseModel):
    test_event_payload: Dict[str, Any] = Field(default_factory=dict)

class WorkflowDryRunResponse(BaseModel):
    simulated: bool
    workflow_id: str
    version: int
    evaluated_nodes: List[Dict[str, Any]]
    proposed_actions: List[Dict[str, Any]]
    capabilities_required: List[str]
    requires_approval: bool
    policy_decision: str
    reason: str
