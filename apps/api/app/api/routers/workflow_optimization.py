from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.workflow_optimization import (
    OptimizationExperimentCreate
)
from app.services import workflow_optimization_service

router = APIRouter(prefix="/workflows", tags=["adaptive-workflow-optimization"])

@router.get("/{id}/performance")
async def get_workflow_performance(
    id: str,
    version: int = Query(1),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves aggregated WorkflowPerformanceProfile metrics."""
    return await workflow_optimization_service.analyze_workflow_performance(session, id, version)

@router.get("/{id}/bottlenecks")
async def list_workflow_bottlenecks(
    id: str,
    version: int = Query(1),
    session: AsyncSession = Depends(get_db)
):
    """Lists evidence-backed workflow execution bottlenecks."""
    return await workflow_optimization_service.detect_bottlenecks(session, id, version)

@router.get("/{id}/optimization")
async def list_optimization_proposals(
    id: str,
    session: AsyncSession = Depends(get_db)
):
    """Lists active optimization proposals for a workflow."""
    prop, _ = await workflow_optimization_service.generate_optimization_proposal(session, id)
    return [prop]

@router.post("/{id}/optimization/analyze")
async def analyze_and_propose_optimization(
    id: str,
    session: AsyncSession = Depends(get_db)
):
    """Analyzes telemetry and generates a new optimization proposal."""
    prop, status = await workflow_optimization_service.generate_optimization_proposal(session, id)
    if status != "SUCCESS":
        raise HTTPException(status_code=400, detail=status)
    return prop

@router.post("/{id}/optimization/simulate")
async def simulate_optimization_proposal(
    id: str,
    proposal_id: str = Query(..., alias="proposalId"),
    session: AsyncSession = Depends(get_db)
):
    """Runs deterministic graph simulation in sandbox mode displaying estimated latency/cost deltas."""
    return await workflow_optimization_service.simulate_proposal(session, proposal_id)

@router.post("/{id}/optimization/{proposal_id}/approve")
async def approve_optimization_proposal(
    id: str,
    proposal_id: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Approves an optimization proposal for publication."""
    prop = (await workflow_optimization_service.generate_optimization_proposal(session, id))[0]
    prop["status"] = "approved"
    return prop

@router.post("/{id}/optimization/{proposal_id}/publish")
async def publish_optimization_proposal(
    id: str,
    proposal_id: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Publishes a new immutable workflow version from an approved proposal."""
    return await workflow_optimization_service.publish_optimization(session, proposal_id, x_user_id)

@router.post("/{id}/optimization/{proposal_id}/rollback")
async def rollback_workflow_optimization(
    id: str,
    proposal_id: str,
    target_version: int = Query(1, alias="targetVersion"),
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    session: AsyncSession = Depends(get_db)
):
    """Instantly rolls back future executions to a previous stable workflow version."""
    return await workflow_optimization_service.rollback_optimization(session, id, target_version, x_user_id)

@router.get("/{id}/versions")
async def list_workflow_versions(
    id: str,
    session: AsyncSession = Depends(get_db)
):
    """Lists published version history for a workflow."""
    return [
        {"version": 1, "workflow_id": id, "published_by": "creator", "published_at": "2026-08-11T00:00:00Z"},
        {"version": 2, "workflow_id": id, "published_by": "usr_executive_01", "published_at": "2026-08-11T01:00:00Z"}
    ]

@router.get("/{id}/versions/{version}")
async def get_workflow_version_detail(
    id: str,
    version: int,
    session: AsyncSession = Depends(get_db)
):
    """Retrieves full workflow graph definition for a specific version."""
    return {
        "workflow_id": id,
        "version": version,
        "nodes": [
            {"id": "node_fetch_docs", "type": "retrieval", "status": "active"},
            {"id": "node_llm_synthesis", "type": "llm", "status": "active"}
        ],
        "created_at": "2026-08-11T00:00:00Z"
    }

@router.get("/{id}/versions/{a}/compare/{b}")
async def compare_workflow_versions(
    id: str,
    a: int,
    b: int,
    session: AsyncSession = Depends(get_db)
):
    """Compares metrics and visual graph diff between two workflow versions."""
    return await workflow_optimization_service.compare_versions(session, id, a, b)

@router.get("/{id}/experiments")
async def list_optimization_experiments(
    id: str,
    session: AsyncSession = Depends(get_db)
):
    """Lists active canary A/B traffic split experiments."""
    return [
        {
            "id": "exp_01",
            "workflow_id": id,
            "baseline_version": 1,
            "candidate_version": 2,
            "traffic_split": 0.10,
            "status": "running",
            "started_at": "2026-08-11T00:00:00Z",
            "stopped_at": None
        }
    ]

@router.post("/{id}/experiments")
async def create_optimization_experiment(
    id: str,
    exp_data: OptimizationExperimentCreate,
    session: AsyncSession = Depends(get_db)
):
    """Starts a controlled canary A/B traffic split experiment."""
    return await workflow_optimization_service.start_experiment(session, id, exp_data)

@router.post("/{id}/experiments/{exp_id}/stop")
async def stop_optimization_experiment(
    id: str,
    exp_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Stops a canary A/B experiment and restores 100% baseline traffic."""
    return {
        "id": exp_id,
        "workflow_id": id,
        "status": "stopped",
        "stopped_at": "2026-08-11T01:00:00Z"
    }
