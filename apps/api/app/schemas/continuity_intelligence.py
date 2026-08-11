from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class CriticalCapabilityCreate(BaseModel):
    name: str
    description: str
    owner: str
    criticality: str = "critical"
    workspaceId: str = "ws_default"

class CriticalCapabilityRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    owner: str
    criticality: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class BusinessImpactProfileRead(BaseModel):
    id: str
    capabilityId: str
    financialImpact: str
    operationalImpact: str
    customerImpact: str
    regulatoryImpact: str
    reputationalImpact: str
    strategicImpact: str
    tolerableDowntime: str
    maximumTolerableDisruption: str
    recoveryObjective: str
    dataRecoveryObjective: str

    model_config = ConfigDict(from_attributes=True)

class ResilienceDependencyRiskRead(BaseModel):
    id: str
    capabilityId: str
    dependencyId: str
    dependencyType: str
    criticality: str
    isSinglePointOfFailure: bool
    hasFallback: bool
    primaryFallback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ResilienceGapRead(BaseModel):
    id: str
    capabilityId: str
    gapType: str
    severity: str
    evidence: str
    owner: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class FailureScenarioRead(BaseModel):
    id: str
    name: str
    description: str
    scenarioType: str
    trigger: str
    probabilityRange: str
    impactSummary: str
    cascadeDepth: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ContinuityPlanRead(BaseModel):
    id: str
    organizationId: str
    capabilityId: str
    name: str
    description: str
    status: str
    version: int
    lastValidatedAt: str
    nextDueAt: str

    model_config = ConfigDict(from_attributes=True)

class RecoveryProcedureRead(BaseModel):
    id: str
    planId: str
    name: str
    owner: str
    expectedDurationMin: int
    verificationCriteria: str

    model_config = ConfigDict(from_attributes=True)

class RecoveryOutcomeRead(BaseModel):
    id: str
    procedureId: str
    executionId: str
    outcomeClass: str
    expectedDurationMin: int
    actualDurationMin: int
    varianceMin: int
    verificationDetails: str

    model_config = ConfigDict(from_attributes=True)

class ResilienceTestRead(BaseModel):
    id: str
    planId: str
    testType: str
    frequency: str
    executedAt: str
    result: str
    nextDueDate: str

    model_config = ConfigDict(from_attributes=True)

class ResiliencePostureRead(BaseModel):
    id: str
    capabilityId: str
    dependencyDimension: float
    recoveryDimension: float
    testingDimension: float
    capacityDimension: float
    dataDimension: float
    governanceDimension: float
    overallReadiness: float

    model_config = ConfigDict(from_attributes=True)

class VendorResilienceProfileRead(BaseModel):
    id: str
    vendorId: str
    vendorName: str
    criticality: str
    concentrationRiskFlag: bool
    fallbackAvailable: bool

    model_config = ConfigDict(from_attributes=True)

class DataResilienceProfileRead(BaseModel):
    id: str
    dataAssetId: str
    backupStatus: str
    replicationStatus: str
    lastRestoreTestAt: str
    rpoMinutes: int
    rtoMinutes: int

    model_config = ConfigDict(from_attributes=True)

class AIResilienceProfileRead(BaseModel):
    id: str
    modelId: str
    providerName: str
    fallbackModelId: Optional[str] = None
    fallbackAgentId: Optional[str] = None
    humanEscalationEnabled: bool
    qualityScore: float

    model_config = ConfigDict(from_attributes=True)

class ResilienceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
