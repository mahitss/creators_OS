from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class ModelGatewayRequest(BaseModel):
    request_type: str = Field(..., alias="requestType") # chat, reasoning, classification, extraction, summarization, generation, code, embedding, reranking, vision, structured_output
    capability: str # text_generation, reasoning, tool_calling, structured_output, vision, long_context, code_generation, embedding, reranking
    prompt: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict, alias="inputData")
    classification: str = "internal" # public, internal, confidential, restricted
    required_context_window: int = Field(4096, alias="requiredContextWindow")
    max_tokens: Optional[int] = Field(1024, alias="maxTokens")
    temperature: Optional[float] = 0.7
    preferred_provider: Optional[str] = Field(None, alias="preferredProvider")

class ModelGatewayResponse(BaseModel):
    id: str
    selected_provider: str = Field(..., alias="selectedProvider")
    selected_model: str = Field(..., alias="selectedModel")
    content: str
    usage: Dict[str, int]
    latency_ms: float = Field(..., alias="latencyMs")
    estimated_cost: float = Field(..., alias="estimatedCost")
    finish_reason: str = Field(..., alias="finishReason")
    routing_decision_id: str = Field(..., alias="routingDecisionId")
    fallback_used: bool = Field(False, alias="fallbackUsed")

    model_config = ConfigDict(populate_by_name=True)

class ModelRegistryRead(BaseModel):
    id: str
    provider_id: str = Field(..., alias="providerId")
    name: str
    model_key: str = Field(..., alias="modelKey")
    version: str
    capabilities: List[str]
    context_window: int = Field(..., alias="contextWindow")
    supported_inputs: List[str] = Field(..., alias="supportedInputs")
    supported_outputs: List[str] = Field(..., alias="supportedOutputs")
    status: str
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class ModelProviderRead(BaseModel):
    id: str
    name: str
    provider_key: str = Field(..., alias="providerKey")
    status: str
    region: Optional[str] = None
    capabilities: List[str]
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class ModelRoutingDecisionRead(BaseModel):
    id: str
    request_id: str = Field(..., alias="requestId")
    selected_provider: str = Field(..., alias="selectedProvider")
    selected_model: str = Field(..., alias="selectedModel")
    candidates: List[str]
    rejected_candidates: List[Dict[str, Any]] = Field(..., alias="rejectedCandidates")
    reason_codes: List[str] = Field(..., alias="reasonCodes")
    policy_result: Dict[str, Any] = Field(..., alias="policyResult")
    routing_policy_version: str = Field(..., alias="routingPolicyVersion")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class ModelHealthRead(BaseModel):
    id: str
    model_key: str = Field(..., alias="modelKey")
    provider_key: str = Field(..., alias="providerKey")
    latency_p95_ms: float = Field(..., alias="latencyP95Ms")
    error_rate: float = Field(..., alias="errorRate")
    availability: float
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)

class ModelExperimentCreate(BaseModel):
    name: str
    candidate_model: str = Field(..., alias="candidateModel")
    traffic_percentage: float = Field(5.0, alias="trafficPercentage")

class ModelExperimentRead(BaseModel):
    id: str
    name: str
    candidate_model: str = Field(..., alias="candidateModel")
    traffic_percentage: float = Field(..., alias="trafficPercentage")
    status: str
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class ModelAdminActionRequest(BaseModel):
    reason: Optional[str] = None
