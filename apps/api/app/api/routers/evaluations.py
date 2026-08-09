from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.evaluations import (
    EvaluationSuiteResponse,
    EvaluationCaseResponse,
    EvaluationRunCreate,
    EvaluationRunResponse,
    EvaluationResultResponse
)
from app.services import evaluation_runner

router = APIRouter()

DEFAULT_ADMIN_USER_ID = "usr_admin_01"

def enforce_admin_authorization(x_user_id: Optional[str] = Header(None)) -> str:
    # In production, verify admin role in JWT / Session.
    return x_user_id or DEFAULT_ADMIN_USER_ID

@router.get("/evaluations/suites", response_model=List[EvaluationSuiteResponse])
async def list_suites(
    user_id: str = Depends(enforce_admin_authorization)
) -> List[EvaluationSuiteResponse]:
    suites = await evaluation_runner.list_suites()
    return [EvaluationSuiteResponse(**s) for s in suites]

@router.get("/evaluations/cases/{id}", response_model=EvaluationCaseResponse)
async def get_case(
    id: str,
    user_id: str = Depends(enforce_admin_authorization)
) -> EvaluationCaseResponse:
    c = await evaluation_runner.get_case(id)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation case not found.")
    return EvaluationCaseResponse(**c)

@router.post("/evaluations/runs", response_model=EvaluationRunResponse, status_code=status.HTTP_201_CREATED)
async def create_run(
    payload: EvaluationRunCreate,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(enforce_admin_authorization)
) -> EvaluationRunResponse:
    try:
        run = await evaluation_runner.create_evaluation_run(payload.suite_id)
        background_tasks.add_task(evaluation_runner.run_evaluation_suite, run["id"], payload.model_name or "fake")
        return EvaluationRunResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/evaluations/suites/{id}/run", response_model=EvaluationRunResponse, status_code=status.HTTP_201_CREATED)
async def trigger_suite_run(
    id: str,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(enforce_admin_authorization)
) -> EvaluationRunResponse:
    try:
        run = await evaluation_runner.create_evaluation_run(id)
        background_tasks.add_task(evaluation_runner.run_evaluation_suite, run["id"], "fake")
        return EvaluationRunResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/evaluations/runs/{id}", response_model=EvaluationRunResponse)
async def get_run(
    id: str,
    user_id: str = Depends(enforce_admin_authorization)
) -> EvaluationRunResponse:
    r = await evaluation_runner.get_run(id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation run not found.")
    return EvaluationRunResponse(**r)

@router.get("/evaluations/runs/{id}/results", response_model=List[EvaluationResultResponse])
async def get_run_results(
    id: str,
    user_id: str = Depends(enforce_admin_authorization)
) -> List[EvaluationResultResponse]:
    res = await evaluation_runner.get_run_results(id)
    return [EvaluationResultResponse(**r) for r in res]
