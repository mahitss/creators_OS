from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.agent_mesh import (
    AgentCapabilityCreate,
    AgentCapabilityRead,
    AgentRegistryRead,
    DelegationRequestCreate,
    DelegationRequestRead,
    AgentArtifactRead,
    AgentDisagreementRead,
    AgentReviewTaskRead,
    ReviewActionRequest
)
from app.services import agent_mesh_service

router = APIRouter(prefix="/agents", tags=["agent-mesh"])

@router.get("/registry")
async def list_registered_agents(
    specialization: Optional[str] = None,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists registered specialist agents in the mesh."""
    return await agent_mesh_service.discover_agents(session, ws_ctx.workspace_id, specialization=specialization)

@router.get("/capabilities")
async def list_agent_capabilities(
    agent_id: Optional[str] = None,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists capability descriptors registered in the Agent Mesh."""
    return [
        {
            "id": "cap_res_01",
            "agent_id": agent_id or "ag_research_01",
            "type": "research",
            "name": "Knowledge Synthesis & Document Retrieval",
            "description": "Retrieves authorized internal knowledge and produces structured citations.",
            "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
            "output_schema": {"type": "object", "properties": {"findings": {"type": "array"}}},
            "risk_level": "low",
            "enabled": True,
            "created_at": "2026-08-11T00:00:00Z"
        },
        {
            "id": "cap_analyst_02",
            "agent_id": agent_id or "ag_analyst_02",
            "type": "analysis",
            "name": "Data Analytics & Financial Modeling",
            "description": "Analyzes structured datasets and produces financial forecasts.",
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "risk_level": "medium",
            "enabled": True,
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.post("/delegations")
async def request_delegation(
    req: DelegationRequestCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Requests controlled agent-to-agent delegation with cycle detection and authority bounds."""
    delegation, status = await agent_mesh_service.request_delegation(session, req)
    if status != "ALLOWED":
        raise HTTPException(status_code=400, detail=status)
    return delegation

@router.get("/delegations")
async def list_delegations(
    mission_id: str = Query("msn_default_creator", alias="missionId"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists active agent delegations for a mission."""
    return [
        {
            "id": "del_01",
            "parent_agent_id": "ag_planner_01",
            "child_agent_id": "ag_research_01",
            "mission_id": mission_id,
            "task_id": "tsk_research_01",
            "scope": "read_only",
            "input_references": [{"type": "knowledge_doc", "id": "doc_specs_01"}],
            "required_output": "Research Report Artifact",
            "risk_level": "low",
            "status": "approved",
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/mesh/{mission_id}")
async def get_mesh_execution_graph(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves multi-agent orchestration execution graph (DAG nodes and dependency edges)."""
    return {
        "mission_id": mission_id,
        "nodes": [
            {"id": "n_plan", "task_id": "tsk_01", "agent_id": "ag_planner_01", "node_type": "sequential", "status": "completed"},
            {"id": "n_res", "task_id": "tsk_02", "agent_id": "ag_research_01", "node_type": "parallel", "status": "running"},
            {"id": "n_analyst", "task_id": "tsk_03", "agent_id": "ag_analyst_02", "node_type": "parallel", "status": "running"},
            {"id": "n_review", "task_id": "tsk_04", "agent_id": "ag_reviewer_03", "node_type": "review", "status": "queued"},
            {"id": "n_synth", "task_id": "tsk_05", "agent_id": "ag_synth_05", "node_type": "synthesis", "status": "queued"}
        ],
        "edges": [
            {"id": "e1", "source_node_id": "n_plan", "target_node_id": "n_res", "dependency_type": "success_required"},
            {"id": "e2", "source_node_id": "n_plan", "target_node_id": "n_analyst", "dependency_type": "success_required"},
            {"id": "e3", "source_node_id": "n_res", "target_node_id": "n_review", "dependency_type": "success_required"},
            {"id": "e4", "source_node_id": "n_analyst", "target_node_id": "n_review", "dependency_type": "success_required"},
            {"id": "e5", "source_node_id": "n_review", "target_node_id": "n_synth", "dependency_type": "success_required"}
        ]
    }

@router.get("/mesh/{mission_id}/artifacts")
async def get_mesh_artifacts(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists structured artifacts produced by specialist agents for a mission."""
    return [
        {
            "id": "art_01",
            "mission_id": mission_id,
            "task_id": "tsk_02",
            "agent_id": "ag_research_01",
            "type": "research_report",
            "schema_version": "v1.0",
            "reference_url": "https://vapor.app/artifacts/art_01",
            "content_json": {"title": "Architecture Research Report", "summary": "Full security & DLP specs evaluated."},
            "classification": "internal",
            "validation_status": "valid",
            "version": 1,
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/mesh/{mission_id}/disagreements")
async def get_mesh_disagreements(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists agent fact disagreements and evidence resolution status."""
    return [
        {
            "id": "dis_01",
            "mission_id": mission_id,
            "task_id": "tsk_03",
            "agents": ["ag_analyst_02", "ag_research_01"],
            "positions": {
                "ag_analyst_02": "Q3 Revenue Target is $5.2M",
                "ag_research_01": "Q3 Revenue Target is $4.8M"
            },
            "evidence": [{"source": "doc_specs_01", "fact": "Official Q3 target: $5.0M"}],
            "resolution": "needs_human",
            "status": "open",
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/reviews")
async def list_human_review_tasks(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists pending human escalation review tasks."""
    return [
        {
            "id": "rev_01",
            "mission_id": ws_ctx.workspace_id,
            "task_id": "tsk_03",
            "artifact_id": "art_01",
            "reason": "Agent disagreement on financial target ($5.2M vs $4.8M) requires human operator approval.",
            "risk_level": "high",
            "status": "pending",
            "assigned_to": ws_ctx.user_id,
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.post("/reviews/{review_id}/approve")
async def approve_human_review(
    review_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Approves a human escalation review task."""
    return await agent_mesh_service.resolve_review_task(session, review_id, "approved", ws_ctx.user_id)

@router.post("/reviews/{review_id}/reject")
async def reject_human_review(
    review_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Rejects a human escalation review task."""
    return await agent_mesh_service.resolve_review_task(session, review_id, "rejected", ws_ctx.user_id)
