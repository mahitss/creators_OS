from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ComponentHealthRead(BaseModel):
    id: str
    componentId: str
    componentType: str = Field(..., description="agent, model, tool, integration, database, queue, event_stream, knowledge, memory, workflow, service")
    status: str = Field("healthy", description="healthy, degraded, unavailable, recovering, unknown")
    latencyMs: float
    errorRate: float
    availabilityPct: float
    lastHealthyAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class FailureEventRead(BaseModel):
    id: str
    componentId: str
    failureType: str = Field(..., description="timeout, provider_outage, dependency_failure, capacity_exhaustion, data_corruption, network_failure, authentication_failure, authorization_failure, schema_failure, queue_failure, unknown_failure")
    evidenceJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class DegradationModeRead(BaseModel):
    id: str
    scope: str
    mode: str = Field(..., description="read_only, limited_execution, no_external_actions, approval_required, model_fallback, queue_only, manual_operation")
    reason: str
    status: str
    expiresAt: Optional[str] = None
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CircuitBreakerStateRead(BaseModel):
    id: str
    targetName: str
    state: str = Field("closed", description="closed, open, half_open")
    failureCount: int
    lastStateChangeAt: str

    model_config = ConfigDict(from_attributes=True)

class DeadLetterEntryRead(BaseModel):
    id: str
    messageRef: str
    queueName: str
    failureReason: str
    attempts: int
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class RecoveryPlanCreate(BaseModel):
    name: str
    componentsJson: List[str] = []
    rtoSeconds: int = 300
    rpoSeconds: int = 60
    recoveryOrderJson: List[str] = []

class RecoveryPlanRead(BaseModel):
    id: str
    name: str
    componentsJson: List[str]
    rtoSeconds: int
    rpoSeconds: int
    recoveryOrderJson: List[str]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class ResilienceExperimentCreate(BaseModel):
    name: str
    experimentType: str = Field(..., description="latency_injection, error_injection, dependency_disablement, queue_saturation, model_outage_simulation, tool_outage_simulation")
    targetScope: str = "sandbox"
    blastRadiusJson: Dict[str, Any] = {}
    abortConditionsJson: Dict[str, Any] = {}

class ResilienceExperimentRead(BaseModel):
    id: str
    name: str
    experimentType: str
    targetScope: str
    blastRadiusJson: Dict[str, Any]
    abortConditionsJson: Dict[str, Any]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class ResilienceSLORead(BaseModel):
    id: str
    sloName: str
    targetAvailabilityPct: float
    currentAvailabilityPct: float
    targetLatencyMs: float
    currentLatencyMs: float
    status: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class ReliabilityBudgetRead(BaseModel):
    id: str
    organizationId: str
    allowedErrorPct: float
    currentBurnRate: float
    budgetRemainingPct: float
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class CapacitySnapshotRead(BaseModel):
    id: str
    cpuPct: float
    memoryPct: float
    queueDepth: int
    concurrencyLevel: int
    loadSheddingActive: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)
