import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.skill_fabric import (
    AgentSkillCreate,
    AgentSkillRead,
    AgentSkillVersionRead,
    SkillCandidateRead,
    SkillEvaluationRead,
    SkillHealthRead,
    SkillInvokeRequest,
    SkillInvokeResponse,
    SkillDeployRequest,
    SkillFeedbackRequest
)
from app.services import (
    agent_runtime_v2_service,
    model_gateway_service,
    action_gateway_service,
    policy_engine,
    dlp_service,
    event_mesh_service,
    enterprise_evaluation_service
)

_in_memory_skills: Dict[str, dict] = {}
_in_memory_versions: Dict[str, List[dict]] = {}
_in_memory_candidates: Dict[str, List[dict]] = {}
_in_memory_evaluations: Dict[str, List[dict]] = {}
_in_memory_healths: Dict[str, dict] = {}
_in_memory_deployments: Dict[str, List[dict]] = {}

def _initialize_demo_skill_fabric_if_empty():
    if _in_memory_skills:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    org_id = "org_default_creator"

    skill_01 = "sk_doc_analysis_01"
    ver_01 = "skv_doc_analysis_01_v1"

    _in_memory_skills[skill_01] = {
        "id": skill_01,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "owner_type": "workspace",
        "owner_id": ws_id,
        "name": "Automated Document Analysis & Summarization",
        "description": "Extracts key evidence, synthesizes executive summaries, and runs DLP scan.",
        "skill_type": "analysis",
        "status": "active",
        "current_version_id": ver_01,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_versions[skill_01] = [
        {
            "id": ver_01,
            "skill_id": skill_01,
            "version": 1,
            "definition_reference": {"steps": ["retrieval", "grounding", "summarization"]},
            "input_schema": {"type": "object", "properties": {"doc_id": {"type": "string"}}},
            "output_schema": {"type": "object", "properties": {"summary": {"type": "string"}}},
            "side_effect_contract": "read-only",
            "required_capabilities": ["reasoning", "long_context"],
            "required_tools": ["drive.read"],
            "required_knowledge": ["architecture_handbook"],
            "status": "active",
            "created_at": now_iso
        }
    ]

    _in_memory_healths[ver_01] = {
        "id": "hlth_001",
        "skill_version_id": ver_01,
        "quality_score": 0.96,
        "reliability_score": 0.99,
        "cost_per_1k": 0.02,
        "latency_p95_ms": 280,
        "safety_score": 1.0,
        "freshness_status": "fresh"
    }

    _in_memory_candidates[ws_id] = [
        {
            "id": "skc_pattern_001",
            "workspace_id": ws_id,
            "proposed_by_agent_id": "ag_creator_ops_01",
            "skill_type": "workflow_execution",
            "suggested_definition": {"name": "Q3 Financial Report Triage", "steps": ["fetch_drive", "run_dlp", "email_notify"]},
            "evidence_summary": {"successful_execution_count": 8, "evaluation_score": 0.95},
            "success_rate": 0.95,
            "status": "pending",
            "created_at": now_iso
        }
    ]

_initialize_demo_skill_fabric_if_empty()

async def create_skill(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: AgentSkillCreate,
    organization_id: str = "org_default_creator"
) -> Tuple[dict, dict]:
    """Creates a versioned agent skill."""
    _initialize_demo_skill_fabric_if_empty()
    skill_id = f"sk_{uuid.uuid4().hex[:10]}"
    ver_id = f"skv_{uuid.uuid4().hex[:8]}_v1"
    now_iso = datetime.now(timezone.utc).isoformat()

    skill = {
        "id": skill_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "owner_type": req.owner_type,
        "owner_id": req.owner_id,
        "name": req.name,
        "description": req.description,
        "skill_type": req.skill_type,
        "status": "active",
        "current_version_id": ver_id,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    version = {
        "id": ver_id,
        "skill_id": skill_id,
        "version": 1,
        "definition_reference": {"steps": ["init", "execute", "validate"]},
        "input_schema": req.input_schema,
        "output_schema": req.output_schema,
        "side_effect_contract": req.side_effect_contract,
        "required_capabilities": req.required_capabilities,
        "required_tools": req.required_tools,
        "required_knowledge": req.required_knowledge,
        "status": "active",
        "created_at": now_iso
    }

    _in_memory_skills[skill_id] = skill
    _in_memory_versions[skill_id] = [version]
    _in_memory_healths[ver_id] = {
        "id": f"hlth_{uuid.uuid4().hex[:8]}",
        "skill_version_id": ver_id,
        "quality_score": 0.95,
        "reliability_score": 0.99,
        "cost_per_1k": 0.01,
        "latency_p95_ms": 250,
        "safety_score": 1.0,
        "freshness_status": "fresh"
    }

    return skill, version

async def invoke_skill(
    session: Optional[AsyncSession],
    workspace_id: str,
    skill_id: str,
    req: SkillInvokeRequest,
    organization_id: str = "org_default_creator"
) -> dict:
    """Invokes a versioned skill with circular dependency detection and max depth checks."""
    _initialize_demo_skill_fabric_if_empty()
    skill = _in_memory_skills.get(skill_id)
    if not skill:
        raise ValueError(f"Skill '{skill_id}' not found.")

    # Circular Dependency & Max Depth Checks
    if skill_id in req.calling_skill_ids:
        raise ValueError(f"Circular skill dependency detected: Skill '{skill_id}' is already in active call stack.")
    if len(req.calling_skill_ids) >= req.max_depth:
        raise ValueError(f"Max skill recursion depth ({req.max_depth}) exceeded.")

    ver_id = skill["current_version_id"]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Route through Agent Runtime V2
    from app.schemas.agent_runtime_v2 import AgentExecutionCreate
    exec_req = AgentExecutionCreate(
        agentId=f"ag_skill_{skill_id[:8]}",
        initialVariables=req.input_payload
    )
    exec_inst, _ = await agent_runtime_v2_service.create_execution(
        session, workspace_id=workspace_id, req=exec_req, organization_id=organization_id
    )

    # Execute model step
    await agent_runtime_v2_service.execute_step(
        session,
        execution_id=exec_inst["id"],
        step_type="model_call",
        input_payload={"prompt": f"Execute skill {skill['name']}", "capability": "reasoning"},
        organization_id=organization_id
    )

    return {
        "skill_id": skill_id,
        "version_id": ver_id,
        "status": "completed",
        "output_payload": {"result": "success", "skill_name": skill["name"]},
        "execution_id": exec_inst["id"],
        "duration_ms": 240
    }

async def list_skills(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_skill_fabric_if_empty()
    return [s for s in _in_memory_skills.values() if s["workspace_id"] == workspace_id]

async def list_candidates(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_skill_fabric_if_empty()
    return _in_memory_candidates.get(workspace_id, [])

async def get_skill(session: Optional[AsyncSession], skill_id: str) -> Optional[dict]:
    _initialize_demo_skill_fabric_if_empty()
    return _in_memory_skills.get(skill_id)

async def get_versions(session: Optional[AsyncSession], skill_id: str) -> List[dict]:
    _initialize_demo_skill_fabric_if_empty()
    return _in_memory_versions.get(skill_id, [])

async def get_health(session: Optional[AsyncSession], version_id: str) -> Optional[dict]:
    _initialize_demo_skill_fabric_if_empty()
    return _in_memory_healths.get(version_id)
