from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class EvaluationRunCreate(BaseModel):
    evaluation_type: str = Field(..., alias="evaluationType") # offline, online, regression, benchmark, human_review, simulation, production_sample
    target_type: str = Field(..., alias="targetType") # response, agent, mission, workflow, retrieval, decision, recommendation, tool_call, memory
    target_id: str = Field(..., alias="targetId")
    model: str = "gemini-1.5-pro"
    model_version: str = Field("1.0", alias="modelVersion")
    prompt_version: str = Field("v1.0", alias="promptVersion")
    context_version: str = Field("v1.0", alias="contextVersion")

class EvaluationRunRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    evaluation_type: str = Field(..., alias="evaluationType")
    target_type: str = Field(..., alias="targetType")
    target_id: str = Field(..., alias="targetId")
    model: str
    model_version: str = Field(..., alias="modelVersion")
    prompt_version: str = Field(..., alias="promptVersion")
    context_version: str = Field(..., alias="contextVersion")
    status: str
    started_at: str = Field(..., alias="startedAt")
    completed_at: Optional[str] = Field(None, alias="completedAt")

    class Config:
        populate_by_name = True

class EvaluationDatasetCreate(BaseModel):
    name: str
    version: str = "1.0"
    description: Optional[str] = None
    scope: str = "workspace"
    is_golden: bool = Field(False, alias="isGolden")

class EvaluationDatasetRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    name: str
    version: str
    description: Optional[str] = None
    scope: str
    is_golden: bool = Field(..., alias="isGolden")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class EvaluationCaseRead(BaseModel):
    id: str
    dataset_id: str = Field(..., alias="datasetId")
    input_data: Dict[str, Any] = Field(..., alias="inputData")
    expected_output_reference: Optional[Dict[str, Any]] = Field(None, alias="expectedOutputReference")
    expected_evidence_references: List[Dict[str, Any]] = Field(default_factory=list, alias="expectedEvidenceReferences")
    metadata_info: Dict[str, Any] = Field(default_factory=dict, alias="metadataInfo")
    classification: str

    class Config:
        populate_by_name = True

class EvaluationResultRead(BaseModel):
    id: str
    evaluation_run_id: str = Field(..., alias="evaluationRunId")
    case_id: str = Field(..., alias="caseId")
    metric: str
    score: float
    status: str # pass, fail, warning
    evidence: Dict[str, Any]
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class HumanEvaluationCreate(BaseModel):
    case_id: str = Field(..., alias="caseId")
    evaluation_run_id: Optional[str] = Field(None, alias="evaluationRunId")
    criteria: str
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None

class HumanEvaluationRead(BaseModel):
    id: str
    evaluator_id: str = Field(..., alias="evaluatorId")
    case_id: str = Field(..., alias="caseId")
    evaluation_run_id: Optional[str] = Field(None, alias="evaluationRunId")
    criteria: str
    rating: float
    comment: Optional[str] = None
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class EvaluationExperimentCreate(BaseModel):
    name: str
    baseline_config: Dict[str, Any] = Field(..., alias="baselineConfig")
    candidate_config: Dict[str, Any] = Field(..., alias="candidateConfig")

class EvaluationExperimentRead(BaseModel):
    id: str
    name: str
    baseline_config: Dict[str, Any] = Field(..., alias="baselineConfig")
    candidate_config: Dict[str, Any] = Field(..., alias="candidateConfig")
    status: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class EvaluationRegressionRead(BaseModel):
    id: str
    target_id: str = Field(..., alias="targetId")
    target_type: str = Field(..., alias="targetType")
    baseline_run_id: str = Field(..., alias="baselineRunId")
    candidate_run_id: str = Field(..., alias="candidateRunId")
    metric: str
    delta: float
    status: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class AIEvaluationOverviewRead(BaseModel):
    total_runs: int = Field(..., alias="totalRuns")
    grounding_rate: float = Field(..., alias="groundingRate")
    citation_accuracy: float = Field(..., alias="citationAccuracy")
    task_success_rate: float = Field(..., alias="taskSuccessRate")
    judge_calibration_score: float = Field(..., alias="judgeCalibrationScore")
    active_regressions_count: int = Field(..., alias="activeRegressionsCount")
    total_datasets_count: int = Field(..., alias="totalDatasetsCount")
    last_evaluated_at: str = Field(..., alias="lastEvaluatedAt")

    class Config:
        populate_by_name = True
