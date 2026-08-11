from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class WorkflowPerformanceProfileRead(BaseModel):
    id: str
    workflow_id: str
    version: int
    execution_count: int
    success_rate: float
    failure_rate: float
    average_latency: float
    p50_latency: float
    p95_latency: float
    p99_latency: float
    average_cost: float
    retry_rate: float
    timeout_rate: float
    approval_wait_time: float
    created_at: datetime
    updated_at: datetime

class WorkflowNodePerformanceRead(BaseModel):
    id: str
    workflow_id: str
    version: int
    node_id: str
    execution_count: int
    success_rate: float
    latency: float
    cost: float
    retry_rate: float
    failure_rate: float
    created_at: datetime

class WorkflowBottleneckRead(BaseModel):
    id: str
    workflow_id: str
    version: int
    bottleneck_type: str
    node_id: str
    evidence: List[Dict[str, Any]]
    severity: str
    created_at: datetime

class WorkflowOptimizationProposalRead(BaseModel):
    id: str
    workflow_id: str
    source_version: int
    changes: List[Dict[str, Any]]
    reason: str
    evidence: List[Dict[str, Any]]
    expected_impact: str
    risk: str
    status: str
    created_at: datetime

class OptimizationSimulationRead(BaseModel):
    id: str
    proposal_id: str
    simulated_latency_diff: float
    simulated_cost_diff: float
    safety_validation: Dict[str, Any]
    simulated_at: datetime

class OptimizationExperimentCreate(BaseModel):
    candidate_version: int = Field(..., alias="candidateVersion")
    traffic_split: float = Field(0.10, alias="trafficSplit")

class OptimizationExperimentRead(BaseModel):
    id: str
    workflow_id: str
    baseline_version: int
    candidate_version: int
    traffic_split: float
    status: str
    started_at: datetime
    stopped_at: Optional[datetime] = None

class WorkflowVersionComparisonRead(BaseModel):
    id: str
    workflow_id: str
    version_a: int
    version_b: int
    diff_json: Dict[str, Any]
    compared_at: datetime
