from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.workflows import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowRead,
    WorkflowValidationResponse,
    WorkflowPublishResponse,
    WorkflowRunRead,
    WorkflowDryRunRequest,
    WorkflowDryRunResponse
)
from app.services import workflow_engine

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.get("", response_model=List[WorkflowRead])
async def list_workflows(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists workspace workflows."""
    workflows = await workflow_engine.list_workspace_workflows(session, ws_ctx.workspace_id)
    return workflows

@router.post("", response_model=WorkflowRead, status_code=201)
async def create_workflow(
    workflow_in: WorkflowCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Creates a new draft workflow."""
    workflow_in.workspace_id = ws_ctx.workspace_id
    workflow = await workflow_engine.create_workflow(session, workflow_in, created_by=ws_ctx.user_id)
    return workflow

@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(
    workflow_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves a workflow by ID."""
    workflow = await workflow_engine.get_workflow(session, workflow_id)
    if not workflow or workflow.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    return workflow

@router.patch("/{workflow_id}", response_model=WorkflowRead)
async def update_workflow(
    workflow_id: str,
    update_in: WorkflowUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Updates workflow definition, metadata, or status."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    workflow = await workflow_engine.update_workflow(session, workflow_id, update_in)
    return workflow

@router.post("/{workflow_id}/validate", response_model=WorkflowValidationResponse)
async def validate_workflow(
    workflow_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Validates workflow graph structure, cycle prevention, and capability requirements."""
    workflow = await workflow_engine.get_workflow(session, workflow_id)
    if not workflow or workflow.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")

    vkey = f"{workflow_id}_v{workflow['version']}"
    ver_def = {}
    if hasattr(workflow_engine, "_in_memory_versions") and vkey in workflow_engine._in_memory_versions:
        ver_def = workflow_engine._in_memory_versions[vkey].get("definition", {})

    valid, errors, warnings, caps = workflow_engine.validate_workflow_definition(ver_def)
    nodes = ver_def.get("nodes", [])
    edges = ver_def.get("edges", [])

    return WorkflowValidationResponse(
        valid=valid,
        errors=errors,
        warnings=warnings,
        capabilities=caps,
        node_count=len(nodes),
        edge_count=len(edges)
    )

@router.post("/{workflow_id}/publish", response_model=WorkflowPublishResponse)
async def publish_workflow(
    workflow_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Validates, performs PolicyEngine capability review, and publishes immutable WorkflowVersion."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    try:
        res = await workflow_engine.publish_workflow(session, workflow_id, user_id=ws_ctx.user_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{workflow_id}/test", response_model=WorkflowDryRunResponse)
async def test_workflow(
    workflow_id: str,
    dry_run_in: WorkflowDryRunRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Performs dry-run simulation of workflow execution using synthetic payload."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    res = await workflow_engine.dry_run_workflow(session, workflow_id, dry_run_in.test_event_payload)
    return res

@router.post("/{workflow_id}/run", response_model=WorkflowRunRead, status_code=202)
async def trigger_workflow_run(
    workflow_id: str,
    trigger_event_id: Optional[str] = Query(None, alias="triggerEventId"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Triggers an asynchronous workflow execution through the authoritative DAG Scheduler."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    try:
        run = await workflow_engine.run_workflow(session, workflow_id, trigger_event_id=trigger_event_id)
        return run
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workflow_id}/runs", response_model=List[WorkflowRunRead])
async def list_workflow_runs(
    workflow_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves execution run history for a workflow."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    runs = await workflow_engine.list_workflow_runs(session, workflow_id)
    return runs

@router.get("/runs/{run_id}", response_model=WorkflowRunRead)
async def get_workflow_run_detail(
    run_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves detailed status for a specific workflow run."""
    run = await workflow_engine.get_workflow_run(session, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    return run

@router.post("/{workflow_id}/archive", response_model=WorkflowRead)
async def archive_workflow(
    workflow_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Archives a workflow."""
    existing = await workflow_engine.get_workflow(session, workflow_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    update_in = WorkflowUpdate(status="archived")
    workflow = await workflow_engine.update_workflow(session, workflow_id, update_in)
    return workflow
