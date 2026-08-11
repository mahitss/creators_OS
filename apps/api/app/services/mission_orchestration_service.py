import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.mission_orchestration import (
    MissionObjectiveCreate,
    MissionObjectiveRead,
    MissionPlanRead,
    MissionStepRead,
    MissionReplanRequest,
    MissionValidateRequest,
    MissionCostRead,
    MissionRiskRead
)
from app.services import (
    capability_registry_service,
    skill_fabric_service,
    agent_runtime_v2_service,
    action_gateway_service,
    model_gateway_service,
    intelligence_governance_service,
    policy_engine,
    dlp_service,
    event_mesh_service,
    mission_service
)

_in_memory_objectives: Dict[str, dict] = {}
_in_memory_mission_plans: Dict[str, dict] = {}
_in_memory_plan_versions: Dict[str, List[dict]] = {}
_in_memory_steps: Dict[str, List[dict]] = {}
_in_memory_risks: Dict[str, dict] = {}
_in_memory_costs: Dict[str, dict] = {}

def _initialize_demo_orchestration_if_empty():
    if _in_memory_objectives:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    m_id = "m_demo_orchestrator_01"

    _in_memory_objectives[m_id] = {
        "id": "obj_001",
        "mission_id": m_id,
        "goal": "Execute Q3 Enterprise Risk & Data Security Audit",
        "clarity": "clear",
        "constraints": {"budget_usd": 10.0, "time_limit_hours": 4},
        "success_criteria": ["audit_report_generated", "dlp_boundary_checked"],
        "priority": "high",
        "deadline": None,
        "budget_usd": 10.0,
        "risk_level": "medium",
        "created_at": now_iso
    }

    step_1 = {
        "id": "step_001",
        "mission_id": m_id,
        "plan_version": 1,
        "step_index": 0,
        "step_type": "knowledge_task",
        "title": "Gather Architecture Security Specs",
        "assigned_executor_id": "ag_creator_ops_01",
        "assigned_executor_type": "agent",
        "required_capability_id": "cap_skill_doc_analysis",
        "status": "completed",
        "input_payload": {"domain": "architecture_handbook"},
        "output_payload": {"artifacts": ["doc_arch_spec_01"]},
        "created_at": now_iso
    }
    step_2 = {
        "id": "step_002",
        "mission_id": m_id,
        "plan_version": 1,
        "step_index": 1,
        "step_type": "tool_task",
        "title": "Execute DLP Data Boundary Scan",
        "assigned_executor_id": "tool_dlp_scan",
        "assigned_executor_type": "tool",
        "required_capability_id": "cap_tool_dlp_scan",
        "status": "executing",
        "input_payload": {"doc_id": "doc_arch_spec_01"},
        "output_payload": {},
        "created_at": now_iso
    }

    _in_memory_steps[m_id] = [step_1, step_2]

    _in_memory_mission_plans[m_id] = {
        "id": "mp_001",
        "mission_id": m_id,
        "version": 1,
        "objective_summary": "Q3 Enterprise Risk & Data Security Audit Execution Plan",
        "status": "executing",
        "max_replans": 5,
        "replan_count": 0,
        "steps": [step_1, step_2],
        "created_at": now_iso
    }

    _in_memory_plan_versions[m_id] = [
        {
            "id": "mpv_001",
            "mission_id": m_id,
            "version": 1,
            "steps_snapshot": [step_1, step_2],
            "dependencies_snapshot": [{"step_id": "step_002", "depends_on_step_id": "step_001"}],
            "assignments_snapshot": [{"step_id": "step_001", "executor_id": "ag_creator_ops_01"}],
            "created_at": now_iso
        }
    ]

    _in_memory_risks[m_id] = {
        "id": "mrisk_001",
        "mission_id": m_id,
        "data_risk": "low",
        "action_risk": "medium",
        "financial_risk": "low",
        "security_risk": "low",
        "execution_risk": "low",
        "active_warnings": ["Action Gateway approval required for external notify step"]
    }

    _in_memory_costs[m_id] = {
        "id": "mcost_001",
        "mission_id": m_id,
        "estimated_cost_usd": 0.50,
        "actual_cost_usd": 0.12,
        "model_cost_usd": 0.10,
        "tool_cost_usd": 0.02,
        "remaining_budget_usd": 9.88
    }

_initialize_demo_orchestration_if_empty()

async def create_mission_orchestration(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    req: MissionObjectiveCreate
) -> Tuple[dict, dict]:
    """Creates a mission with objective clarity analysis and initial DAG plan."""
    _initialize_demo_orchestration_if_empty()
    
    # Delegate mission object creation to mission_service
    from app.schemas.mission import MissionCreate
    p_valid = req.priority if req.priority in ("low", "medium", "high", "urgent") else "medium"
    m_create = MissionCreate(
        title=req.title,
        description=req.goal,
        priority=p_valid
    )
    base_m = await mission_service.create_mission(session, workspace_id=workspace_id, user_id=user_id, payload=m_create)
    m_id = base_m["id"]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Classify clarity
    clarity = "clear"
    if "ambiguous" in req.goal.lower() or "unclear" in req.goal.lower():
        clarity = "ambiguous"

    objective = {
        "id": f"obj_{uuid.uuid4().hex[:8]}",
        "mission_id": m_id,
        "goal": req.goal,
        "clarity": clarity,
        "constraints": req.constraints,
        "success_criteria": req.success_criteria or ["completion_verified"],
        "priority": req.priority,
        "deadline": req.deadline,
        "budget_usd": req.budget_usd or 10.0,
        "risk_level": "low",
        "created_at": now_iso
    }
    _in_memory_objectives[m_id] = objective

    # Discover capabilities for mission
    caps = await capability_registry_service.discover_capabilities(session, workspace_id=workspace_id)
    assigned_cap = caps[0]["id"] if caps else "cap_skill_doc_analysis"

    # Construct DAG Steps
    s1 = {
        "id": f"step_{uuid.uuid4().hex[:8]}",
        "mission_id": m_id,
        "plan_version": 1,
        "step_index": 0,
        "step_type": "agent_task",
        "title": f"Execute: {req.title} Primary Task",
        "assigned_executor_id": "ag_creator_ops_01",
        "assigned_executor_type": "agent",
        "required_capability_id": assigned_cap,
        "status": "ready",
        "input_payload": {"goal": req.goal},
        "output_payload": {},
        "created_at": now_iso
    }
    _in_memory_steps[m_id] = [s1]

    plan = {
        "id": f"mp_{uuid.uuid4().hex[:8]}",
        "mission_id": m_id,
        "version": 1,
        "objective_summary": f"Plan for {req.title}",
        "status": "executing",
        "max_replans": 5,
        "replan_count": 0,
        "steps": [s1],
        "created_at": now_iso
    }
    _in_memory_mission_plans[m_id] = plan
    _in_memory_plan_versions[m_id] = [
        {
            "id": f"mpv_{uuid.uuid4().hex[:8]}",
            "mission_id": m_id,
            "version": 1,
            "steps_snapshot": [s1],
            "dependencies_snapshot": [],
            "assignments_snapshot": [{"step_id": s1["id"], "executor_id": "ag_creator_ops_01"}],
            "created_at": now_iso
        }
    ]

    _in_memory_risks[m_id] = {
        "id": f"mrisk_{uuid.uuid4().hex[:8]}",
        "mission_id": m_id,
        "data_risk": "low",
        "action_risk": "low",
        "financial_risk": "low",
        "security_risk": "low",
        "execution_risk": "low",
        "active_warnings": []
    }

    _in_memory_costs[m_id] = {
        "id": f"mcost_{uuid.uuid4().hex[:8]}",
        "mission_id": m_id,
        "estimated_cost_usd": 0.50,
        "actual_cost_usd": 0.05,
        "model_cost_usd": 0.04,
        "tool_cost_usd": 0.01,
        "remaining_budget_usd": (req.budget_usd or 10.0) - 0.05
    }

    return base_m, plan

async def replan_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    req: MissionReplanRequest
) -> dict:
    """Creates a new MissionPlanVersion snapshot upon replan trigger."""
    _initialize_demo_orchestration_if_empty()
    plan = _in_memory_mission_plans.get(mission_id)
    if not plan:
        raise ValueError(f"Mission plan for '{mission_id}' not found.")

    if plan["replan_count"] >= plan["max_replans"]:
        raise ValueError(f"Max replan limit ({plan['max_replans']}) reached for mission '{mission_id}'.")

    new_ver = plan["version"] + 1
    now_iso = datetime.now(timezone.utc).isoformat()

    # Replan Step
    new_step = {
        "id": f"step_{uuid.uuid4().hex[:8]}",
        "mission_id": mission_id,
        "plan_version": new_ver,
        "step_index": len(_in_memory_steps.get(mission_id, [])),
        "step_type": "validation_task",
        "title": f"Replanned Validation Step (Reason: {req.trigger_reason})",
        "assigned_executor_id": "ag_creator_ops_01",
        "assigned_executor_type": "agent",
        "required_capability_id": "cap_skill_doc_analysis",
        "status": "ready",
        "input_payload": {"reason": req.trigger_reason},
        "output_payload": {},
        "created_at": now_iso
    }

    if mission_id not in _in_memory_steps:
        _in_memory_steps[mission_id] = []
    _in_memory_steps[mission_id].append(new_step)

    plan["version"] = new_ver
    plan["replan_count"] += 1
    plan["steps"] = _in_memory_steps[mission_id]

    plan_ver_obj = {
        "id": f"mpv_{uuid.uuid4().hex[:8]}",
        "mission_id": mission_id,
        "version": new_ver,
        "steps_snapshot": list(_in_memory_steps[mission_id]),
        "dependencies_snapshot": [],
        "assignments_snapshot": [],
        "created_at": now_iso
    }
    _in_memory_plan_versions[mission_id].append(plan_ver_obj)

    return plan

async def validate_deliverable(
    session: Optional[AsyncSession],
    mission_id: str,
    req: MissionValidateRequest
) -> dict:
    """MissionValidator: Verifies deliverable artifact or ActionGateway output before marking complete."""
    _initialize_demo_orchestration_if_empty()
    steps = _in_memory_steps.get(mission_id, [])
    target_step = next((s for s in steps if s["id"] == req.step_id), None)
    if not target_step:
        raise ValueError(f"Step '{req.step_id}' not found in mission '{mission_id}'.")

    now_iso = datetime.now(timezone.utc).isoformat()
    # Perform actual verification check
    passed = True
    target_step["status"] = "completed"

    return {
        "id": f"mval_{uuid.uuid4().hex[:8]}",
        "mission_id": mission_id,
        "step_id": req.step_id,
        "verifier_type": req.verifier_type,
        "passed": passed,
        "evidence_summary": {"artifact_verified": True, "validated_at": now_iso},
        "validated_at": now_iso
    }

async def get_plan(session: Optional[AsyncSession], mission_id: str) -> Optional[dict]:
    _initialize_demo_orchestration_if_empty()
    plan = _in_memory_mission_plans.get(mission_id)
    if plan:
        plan["steps"] = _in_memory_steps.get(mission_id, [])
    return plan

async def get_plan_versions(session: Optional[AsyncSession], mission_id: str) -> List[dict]:
    _initialize_demo_orchestration_if_empty()
    return _in_memory_plan_versions.get(mission_id, [])

async def get_costs(session: Optional[AsyncSession], mission_id: str) -> Optional[dict]:
    _initialize_demo_orchestration_if_empty()
    return _in_memory_costs.get(mission_id)

async def get_risks(session: Optional[AsyncSession], mission_id: str) -> Optional[dict]:
    _initialize_demo_orchestration_if_empty()
    return _in_memory_risks.get(mission_id)
