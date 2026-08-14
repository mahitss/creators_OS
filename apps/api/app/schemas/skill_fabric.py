from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class AgentSkillCreate(BaseModel):
    owner_type: str = Field("workspace", alias="ownerType")
    owner_id: str = Field("ws_default_01", alias="ownerId")
    name: str
    description: str
    skill_type: str = Field("workflow_execution", alias="skillType")
    side_effect_contract: str = Field("read-only", alias="sideEffectContract")
    required_capabilities: List[str] = Field(default_factory=list, alias="requiredCapabilities")
    required_tools: List[str] = Field(default_factory=list, alias="requiredTools")
    required_knowledge: List[str] = Field(default_factory=list, alias="requiredKnowledge")
    input_schema: Dict[str, Any] = Field(default_factory=dict, alias="inputSchema")
    output_schema: Dict[str, Any] = Field(default_factory=dict, alias="outputSchema")

class AgentSkillRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    owner_type: str = Field(..., alias="ownerType")
    owner_id: str = Field(..., alias="ownerId")
    name: str
    description: str
    skill_type: str = Field(..., alias="skillType")
    status: str
    current_version_id: Optional[str] = Field(None, alias="currentVersionId")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class AgentSkillVersionRead(BaseModel):
    id: str
    skill_id: str = Field(..., alias="skillId")
    version: int
    definition_reference: Dict[str, Any] = Field(..., alias="definitionReference")
    input_schema: Dict[str, Any] = Field(..., alias="inputSchema")
    output_schema: Dict[str, Any] = Field(..., alias="outputSchema")
    side_effect_contract: str = Field(..., alias="sideEffectContract")
    required_capabilities: List[str] = Field(..., alias="requiredCapabilities")
    required_tools: List[str] = Field(..., alias="requiredTools")
    required_knowledge: List[str] = Field(..., alias="requiredKnowledge")
    status: str
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class SkillCandidateRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    proposed_by_agent_id: str = Field(..., alias="proposedByAgentId")
    skill_type: str = Field(..., alias="skillType")
    suggested_definition: Dict[str, Any] = Field(..., alias="suggestedDefinition")
    evidence_summary: Dict[str, Any] = Field(..., alias="evidenceSummary")
    success_rate: float = Field(..., alias="successRate")
    status: str
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class SkillEvaluationRead(BaseModel):
    id: str
    skill_version_id: str = Field(..., alias="skillVersionId")
    evaluation_run_id: str = Field(..., alias="evaluationRunId")
    correctness_score: float = Field(..., alias="correctnessScore")
    grounding_score: float = Field(..., alias="groundingScore")
    safety_score: float = Field(..., alias="safetyScore")
    cost_usd: float = Field(..., alias="costUsd")
    latency_ms: int = Field(..., alias="latencyMs")
    passed: bool
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class SkillHealthRead(BaseModel):
    id: str
    skill_version_id: str = Field(..., alias="skillVersionId")
    quality_score: float = Field(..., alias="qualityScore")
    reliability_score: float = Field(..., alias="reliabilityScore")
    cost_per_1k: float = Field(..., alias="costPer1k")
    latency_p95_ms: int = Field(..., alias="latencyP95Ms")
    safety_score: float = Field(..., alias="safetyScore")
    freshness_status: str = Field(..., alias="freshnessStatus")

    model_config = ConfigDict(populate_by_name=True)

class SkillInvokeRequest(BaseModel):
    input_payload: Dict[str, Any] = Field(default_factory=dict, alias="inputPayload")
    calling_skill_ids: List[str] = Field(default_factory=list, alias="callingSkillIds")
    max_depth: int = Field(5, alias="maxDepth")

class SkillInvokeResponse(BaseModel):
    skill_id: str = Field(..., alias="skillId")
    version_id: str = Field(..., alias="versionId")
    status: str
    output_payload: Dict[str, Any] = Field(..., alias="outputPayload")
    execution_id: str = Field(..., alias="executionId")
    duration_ms: int = Field(..., alias="durationMs")

class SkillDeployRequest(BaseModel):
    mode: str = "active" # sandbox, canary, active
    traffic_percentage: float = 100.0

class SkillFeedbackRequest(BaseModel):
    feedback_type: str = Field(..., alias="feedbackType") # useful, incorrect, outdated, unsafe, too_expensive, too_slow
    notes: Optional[str] = None
