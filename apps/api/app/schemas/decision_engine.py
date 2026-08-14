from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class DecisionCreate(BaseModel):
    question: str
    decision_type: str = Field("operational", alias="decisionType")
    mission_id: Optional[str] = Field(None, alias="missionId")
    agent_id: Optional[str] = Field(None, alias="agentId")

class DecisionClaimRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    claim_type: str = Field(..., alias="claimType") # fact, inference, assumption, constraint, prediction, recommendation
    content: str
    uncertainty: str # known, likely, uncertain, unknown
    time_horizon: Optional[str] = Field(None, alias="timeHorizon")
    source_evidence_ids: List[str] = Field(default_factory=list, alias="sourceEvidenceIds")

    model_config = ConfigDict(populate_by_name=True)

class DecisionEvidenceRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    source_type: str = Field(..., alias="sourceType")
    source_id: str = Field(..., alias="sourceId")
    claim_summary: str = Field(..., alias="claimSummary")
    observed_at: str = Field(..., alias="observedAt")
    retrieved_at: str = Field(..., alias="retrievedAt")
    valid_until: Optional[str] = Field(None, alias="validUntil")
    authority: str
    freshness: str
    relevance: float
    status: str

    model_config = ConfigDict(populate_by_name=True)

class EvidenceConflictRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    claim_a: str = Field(..., alias="claimA")
    claim_b: str = Field(..., alias="claimB")
    source_a_id: str = Field(..., alias="sourceAId")
    source_b_id: str = Field(..., alias="sourceBId")
    authority_a: str = Field(..., alias="authorityA")
    authority_b: str = Field(..., alias="authorityB")
    resolution_status: str = Field(..., alias="resolutionStatus")

    model_config = ConfigDict(populate_by_name=True)

class DecisionOptionRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    name: str
    description: str
    generated_by: str = Field(..., alias="generatedBy")
    is_generated: bool = Field(..., alias="isGenerated")
    constraints: Dict[str, Any]
    requirements: List[str]
    risks: List[str]

    model_config = ConfigDict(populate_by_name=True)

class DecisionTradeoffRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    option_a_id: str = Field(..., alias="optionAId")
    option_b_id: str = Field(..., alias="optionBId")
    advantage_a: str = Field(..., alias="advantageA")
    advantage_b: str = Field(..., alias="advantageB")
    tradeoff_summary: str = Field(..., alias="tradeoffSummary")

    model_config = ConfigDict(populate_by_name=True)

class DecisionRiskRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    option_id: str = Field(..., alias="optionId")
    financial_risk: str = Field(..., alias="financialRisk")
    security_risk: str = Field(..., alias="securityRisk")
    operational_risk: str = Field(..., alias="operationalRisk")
    data_risk: str = Field(..., alias="dataRisk")
    compliance_risk: str = Field(..., alias="complianceRisk")
    execution_risk: str = Field(..., alias="executionRisk")
    reputational_risk: str = Field(..., alias="reputationalRisk")

    model_config = ConfigDict(populate_by_name=True)

class DecisionRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    mission_id: Optional[str] = Field(None, alias="missionId")
    agent_id: Optional[str] = Field(None, alias="agentId")
    decision_type: str = Field(..., alias="decisionType")
    question: str
    status: str
    current_version: int = Field(..., alias="currentVersion")
    superseded_by: Optional[str] = Field(None, alias="supersededBy")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class DecisionAnalyzeRequest(BaseModel):
    force_fresh_evidence: bool = Field(False, alias="forceFreshEvidence")

class DecisionScenarioCreate(BaseModel):
    name: str
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    variables: Dict[str, Any] = Field(default_factory=dict)

class DecisionScenarioRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    name: str
    assumptions: Dict[str, Any]
    variables: Dict[str, Any]
    result_summary: Dict[str, Any] = Field(..., alias="resultSummary")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class DecisionApprovalRequest(BaseModel):
    recommended_option_id: str = Field(..., alias="recommendedOptionId")

class DecisionOverrideRequest(BaseModel):
    original_option_id: str = Field(..., alias="originalOptionId")
    selected_option_id: str = Field(..., alias="selectedOptionId")
    reason: str

class DecisionOutcomeCreate(BaseModel):
    expected_outcome: str = Field(..., alias="expectedOutcome")
    actual_outcome: Optional[str] = Field(None, alias="actualOutcome")
    status: str = "pending"

class DecisionOutcomeRead(BaseModel):
    id: str
    decision_id: str = Field(..., alias="decisionId")
    expected_outcome: str = Field(..., alias="expectedOutcome")
    actual_outcome: Optional[str] = Field(None, alias="actualOutcome")
    observed_at: Optional[str] = Field(None, alias="observedAt")
    status: str

    model_config = ConfigDict(populate_by_name=True)
