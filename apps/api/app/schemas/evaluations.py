from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class EvaluationSuiteResponse(BaseModel):
    id: str
    name: str
    description: str
    version: int
    status: str
    created_at: str
    updated_at: str

class EvaluationCaseResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    input: Dict[str, Any]
    expected: Dict[str, Any]
    constraints: Dict[str, Any]

class EvaluationRunCreate(BaseModel):
    suite_id: str
    model_name: Optional[str] = "fake"
    is_deterministic: Optional[bool] = True

class EvaluationRunResponse(BaseModel):
    id: str
    suite_id: str
    status: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    total_cases: int
    passed_cases: int
    failed_cases: int
    score: float
    release_blocked: bool = False
    regression_detected: bool = False
    created_at: str
    updated_at: str

class EvaluationResultResponse(BaseModel):
    id: str
    case_id: str
    case_name: str
    category: str
    status: str
    score: float
    metrics: Dict[str, Any]
    hard_security_failure: bool = False
    failure_category: Optional[str] = None
    duration_ms: int
    token_usage: Dict[str, Any]
    estimated_cost: float
    created_at: str
