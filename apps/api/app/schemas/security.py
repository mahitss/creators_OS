from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class SecurityEventCreate(BaseModel):
    organizationId: str = Field(..., description="Organization identifier")
    workspaceId: str = Field(..., description="Workspace identifier")
    eventType: str = Field(..., description="Event classification type")
    severity: str = Field("medium", description="Event severity (info, low, medium, high, critical)")
    source: str = Field(..., description="Event source component")
    actor: str = Field(..., description="User or agent actor ID")
    resource: str = Field(..., description="Target resource ID")
    missionId: Optional[str] = None
    agentId: Optional[str] = None

class SecurityEventRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    eventType: str
    severity: str
    source: str
    actor: str
    resource: str
    missionId: Optional[str] = None
    agentId: Optional[str] = None
    timestamp: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ThreatFindingRead(BaseModel):
    id: str
    securityEventId: str
    threatType: str
    severity: str
    status: str
    evidence: Dict[str, Any]
    recommendedAction: str

    model_config = ConfigDict(from_attributes=True)

class SecurityIncidentCreate(BaseModel):
    organizationId: str
    severity: str = "high"
    summary: str
    eventIds: List[str] = []

class SecurityIncidentRead(BaseModel):
    id: str
    organizationId: str
    severity: str
    status: str
    summary: str
    createdAt: str
    resolvedAt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SecurityQuarantineCreate(BaseModel):
    targetType: str = Field(..., description="agent, skill, capability, workflow, integration")
    targetId: str
    reason: str
    scope: str = "full_isolation"
    createdBy: str
    expiresAt: Optional[str] = None
    releasePolicy: str = "security_admin_approval"

class SecurityQuarantineRead(BaseModel):
    id: str
    targetType: str
    targetId: str
    reason: str
    scope: str
    createdBy: str
    expiresAt: Optional[str] = None
    releasePolicy: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class AgentBehaviorBaselineRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    agentId: str
    toolFrequencyJson: Dict[str, int]
    avgLatencyMs: float
    avgDataVolumeBytes: int
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class BehaviorAnomalyRead(BaseModel):
    id: str
    agentId: str
    anomalyType: str
    deviationScore: float
    evidence: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class ThreatIntelligenceSignalCreate(BaseModel):
    source: str
    confidence: float = 0.90
    freshness: str = "fresh"
    indicatorType: str = Field(..., description="domain, IP, URL, hash, package, capability, model, tool")
    indicatorValue: str
    context: Dict[str, Any] = {}

class ThreatIntelligenceSignalRead(BaseModel):
    id: str
    source: str
    confidence: float
    freshness: str
    indicatorType: str
    indicatorValue: str
    context: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)
