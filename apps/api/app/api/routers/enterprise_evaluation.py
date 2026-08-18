from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.enterprise_evaluation import (
    AIEvaluationOverviewRead,
    EvaluationRunCreate,
    EvaluationRunRead,
    EvaluationDatasetCreate,
    EvaluationDatasetRead,
    EvaluationResultRead,
    HumanEvaluationCreate,
    HumanEvaluationRead,
    EvaluationExperimentCreate,
    EvaluationExperimentRead,
    EvaluationRegressionRead
)
from app.services import enterprise_evaluation_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext

router = APIRouter(prefix="/ai/evaluation", tags=["Enterprise AI Evaluation & Continuous Intelligence Improvement"])

@router.get("", response_model=AIEvaluationOverviewRead)
async def get_evaluation_overview(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns high-level AI evaluation telemetry and metrics."""
    return await enterprise_evaluation_service.get_evaluation_overview(db)

@router.get("/runs", response_model=List[EvaluationRunRead])
async def list_evaluation_runs(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists evaluation runs for workspace."""
    return await enterprise_evaluation_service.list_evaluation_runs(db, workspace_id=ws_ctx.workspace_id)

@router.post("/runs", response_model=EvaluationRunRead)
async def create_evaluation_run(
    req: EvaluationRunCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Triggers a multi-dimensional evaluation run."""
    return await enterprise_evaluation_service.create_evaluation_run(db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id)

@router.get("/runs/{run_id}", response_model=EvaluationRunRead)
async def get_evaluation_run(
    run_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Fetches details for a single evaluation run."""
    run = await enterprise_evaluation_service.get_evaluation_run(db, run_id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return run

@router.get("/results", response_model=List[EvaluationResultRead])
async def list_evaluation_results(
    run_id: Optional[str] = Query(None, alias="runId"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists evaluation results."""
    return await enterprise_evaluation_service.list_evaluation_results(db, run_id=run_id)

@router.get("/datasets", response_model=List[EvaluationDatasetRead])
async def list_evaluation_datasets(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists evaluation datasets."""
    return await enterprise_evaluation_service.list_evaluation_datasets(db, workspace_id=ws_ctx.workspace_id)

@router.post("/datasets", response_model=EvaluationDatasetRead)
async def create_evaluation_dataset(
    req: EvaluationDatasetCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new evaluation dataset."""
    return await enterprise_evaluation_service.create_evaluation_dataset(db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id)

@router.get("/regressions", response_model=List[EvaluationRegressionRead])
async def list_regressions(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists quality regressions."""
    return await enterprise_evaluation_service.list_regressions(db)

@router.get("/reviews", response_model=List[HumanEvaluationRead])
async def list_human_reviews(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists human review ratings."""
    return await enterprise_evaluation_service.list_human_evaluations(db)

@router.post("/reviews", response_model=HumanEvaluationRead)
async def submit_human_review(
    req: HumanEvaluationCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Submits human rating for LLM judge calibration."""
    return await enterprise_evaluation_service.submit_human_evaluation(db, evaluator_id=ws_ctx.user_id, req=req)

@router.get("/experiments", response_model=List[EvaluationExperimentRead])
async def list_experiments(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists A/B experiments."""
    return await enterprise_evaluation_service.list_experiments(db)

@router.post("/experiments", response_model=EvaluationExperimentRead)
async def create_experiment(
    req: EvaluationExperimentCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Creates an A/B experiment."""
    return await enterprise_evaluation_service.create_experiment(db, req=req)

@router.post("/experiments/{exp_id}/stop", response_model=EvaluationExperimentRead)
async def stop_experiment(
    exp_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Stops a running experiment."""
    exp = await enterprise_evaluation_service.stop_experiment(db, experiment_id=exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp
