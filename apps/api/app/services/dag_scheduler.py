import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dag_validator import validate_dag_plan
from app.services.tool_registry import ToolRegistry, ToolRiskLevel
from app.services import agent_runtime, agent_recovery

_in_memory_plans: Dict[str, dict] = {}
_in_memory_nodes: Dict[str, List[dict]] = {}

MAX_PARALLELISM = 5
MAX_REPLANS = 3

async def create_dag_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    goal: str,
    nodes: List[Dict[str, Any]]
) -> dict:
    valid, errors = validate_dag_plan(nodes)
    if not valid:
        raise ValueError(f"Invalid DAG plan: {'; '.join(errors)}")

    plan_id = f"plan_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    plan = {
        "id": plan_id,
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "version": 1,
        "status": "validated",
        "goal": goal,
        "summary": f"DAG Plan with {len(nodes)} nodes.",
        "replan_count": 0,
        "approved_at": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    formatted_nodes = []
    for n in nodes:
        node_id = f"node_{uuid.uuid4().hex[:8]}"
        tool_name = n.get("tool_name")
        risk_level = "read"
        if tool_name:
            t = ToolRegistry.get_tool(tool_name)
            if t:
                risk_level = t.risk_level.value

        fn = {
            "id": node_id,
            "plan_id": plan_id,
            "node_key": n["node_key"],
            "title": n.get("title", n["node_key"]),
            "description": n.get("description", ""),
            "type": n.get("type", "tool_call"),
            "status": "pending",
            "dependencies": n.get("dependencies", []),
            "tool_name": tool_name,
            "input_schema": n.get("input_schema", {}),
            "risk_level": risk_level,
            "approval_required": n.get("approval_required", risk_level in ["write", "external_side_effect"]),
            "estimated_cost": n.get("estimated_cost", 0.0),
            "created_at": now_iso,
            "updated_at": now_iso
        }
        formatted_nodes.append(fn)

    _in_memory_plans[plan_id] = plan
    _in_memory_nodes[plan_id] = formatted_nodes
    return plan

async def get_plan_nodes(plan_id: str) -> List[dict]:
    return _in_memory_nodes.get(plan_id, [])

async def execute_dag_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str,
    plan_id: str
) -> dict:
    plan = _in_memory_plans.get(plan_id)
    if not plan:
        raise ValueError("Plan not found.")

    nodes = _in_memory_nodes.get(plan_id, [])
    completed_keys: Set[str] = {n["node_key"] for n in nodes if n["status"] == "completed"}

    # Find Ready Nodes (Dependencies all completed)
    ready_nodes = []
    for n in nodes:
        if n["status"] == "pending":
            deps_met = all(dep in completed_keys for dep in n.get("dependencies", []))
            if deps_met:
                ready_nodes.append(n)

    if not ready_nodes and len(completed_keys) == len(nodes):
        plan["status"] = "completed"
        return plan

    # Limit Parallelism to MAX_PARALLELISM (5)
    nodes_to_execute = ready_nodes[:MAX_PARALLELISM]

    # Execute Safe Concurrent READ / Approval Nodes
    for n in nodes_to_execute:
        if n["type"] == "approval" or n["approval_required"]:
            n["status"] = "waiting_for_approval"
            plan["status"] = "running"
            await agent_runtime.step_agent_run(session, workspace_id, run_id, requested_tool=n["tool_name"], tool_input=n.get("input_schema", {}))
            return plan

        n["status"] = "running"
        tool_name = n.get("tool_name") or "search_drive_files"
        tool_input = n.get("input_schema") or {"query": "Proposal"}

        # Execute Tool via AgentRuntime
        run_res = await agent_runtime.step_agent_run(session, workspace_id, run_id, requested_tool=tool_name, tool_input=tool_input)
        if run_res["status"] in ["completed", "running"]:
            n["status"] = "completed"
            completed_keys.add(n["node_key"])
        else:
            n["status"] = "failed"

    if len(completed_keys) == len(nodes):
        plan["status"] = "completed"
    else:
        plan["status"] = "running"

    return plan

async def replan_dag(
    session: Optional[AsyncSession],
    workspace_id: str,
    plan_id: str,
    new_nodes: List[dict]
) -> dict:
    plan = _in_memory_plans.get(plan_id)
    if not plan:
        raise ValueError("Plan not found.")

    if plan["replan_count"] >= MAX_REPLANS:
        raise ValueError(f"Maximum replan limit reached ({MAX_REPLANS}).")

    valid, errors = validate_dag_plan(new_nodes)
    if not valid:
        raise ValueError(f"Invalid replan DAG: {'; '.join(errors)}")

    plan["version"] += 1
    plan["replan_count"] += 1
    plan["updated_at"] = datetime.now(timezone.utc).isoformat()
    return plan
