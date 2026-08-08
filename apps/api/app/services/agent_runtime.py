import uuid
import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.tool_registry import ToolRegistry, ToolRiskLevel
from app.services.context_engine import ContextEngine, ContextRequest, ContextPurpose, SourceType
from app.services import mission_service, attention_service

_in_memory_runs: Dict[str, dict] = {}
_in_memory_steps: Dict[str, List[dict]] = {}
_in_memory_approvals: Dict[str, dict] = {}

MAX_DEFAULT_ITERATIONS = 20

def _compute_input_hash(input_data: dict) -> str:
    serialized = json.dumps(input_data or {}, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

async def create_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    goal: str,
    max_iterations: int = MAX_DEFAULT_ITERATIONS,
    initial_tool: Optional[str] = None,
    initial_input: Optional[dict] = None
) -> dict:
    mission = await mission_service.get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        raise ValueError("Mission not found.")

    run_id = f"run_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    run = {
        "id": run_id,
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "status": "running",
        "goal": goal,
        "current_step_id": None,
        "iteration_count": 0,
        "max_iterations": min(max_iterations, MAX_DEFAULT_ITERATIONS),
        "started_at": now_iso,
        "completed_at": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_runs[run_id] = run
    _in_memory_steps[run_id] = []

    # Execute Initial Agent Step Loop
    await step_agent_run(session, workspace_id, run_id, requested_tool=initial_tool, tool_input=initial_input)

    return _in_memory_runs[run_id]

async def get_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> Optional[dict]:
    run = _in_memory_runs.get(run_id)
    if not run or run["workspace_id"] != workspace_id:
        return None
    return run

async def list_agent_steps(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> List[dict]:
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        return []
    return _in_memory_steps.get(run_id, [])

async def step_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str,
    requested_tool: Optional[str] = None,
    tool_input: Optional[dict] = None
) -> dict:
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        raise ValueError("Agent run not found.")

    # Allow step execution if requested_tool is explicitly provided even if status was completed
    if requested_tool:
        run["status"] = "running"
    elif run["status"] in ["completed", "failed", "cancelled", "paused", "waiting_for_approval"]:
        return run

    if run["iteration_count"] >= run["max_iterations"]:
        run["status"] = "failed"
        run["completed_at"] = datetime.now(timezone.utc).isoformat()
        _record_step(run_id, "failure", "Max iteration limit reached.", error_code="MAX_ITERATIONS_EXCEEDED")
        return run

    run["iteration_count"] += 1
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Retrieve Bounded Context via Unified Context Engine
    ctx_req = ContextRequest(
        workspace_id=workspace_id,
        user_id="usr_alex",
        purpose=ContextPurpose.MISSION_EXECUTION,
        allowed_sources=[SourceType.MISSION, SourceType.MEMORY, SourceType.DRIVE, SourceType.CALENDAR, SourceType.GMAIL],
        mission_id=run["mission_id"]
    )
    ctx_res = await ContextEngine.retrieve(session, ctx_req)

    # 2. Determine Action
    target_tool_name = requested_tool or "search_drive_files"
    target_tool_input = tool_input or {"query": "Proposal"}

    tool = ToolRegistry.get_tool(target_tool_name)
    if not tool:
        run["status"] = "failed"
        run["completed_at"] = now_iso
        _record_step(run_id, "failure", f"Requested tool '{target_tool_name}' does not exist.", error_code="INVALID_TOOL")
        return run

    input_hash = _compute_input_hash(target_tool_input)

    # 3. Check Risk Policy Matrix
    if tool.risk_level in [ToolRiskLevel.WRITE, ToolRiskLevel.EXTERNAL_SIDE_EFFECT]:
        # Check if an approval already exists and is approved for this exact input_hash
        existing_app = None
        for app in _in_memory_approvals.values():
            if app["agent_run_id"] == run_id and app["tool_name"] == tool.name and app["input_hash"] == input_hash:
                existing_app = app
                break

        if not existing_app or existing_app["status"] != "approved":
            # Require User Approval Gate
            app_id = f"app_{uuid.uuid4().hex[:8]}"
            app_req = {
                "id": app_id,
                "agent_run_id": run_id,
                "workspace_id": workspace_id,
                "action": f"Execute {tool.name}",
                "tool_name": tool.name,
                "description": f"Agent requests permission to execute '{tool.name}' with input: {target_tool_input}",
                "risk_level": tool.risk_level.value,
                "status": "pending",
                "input_hash": input_hash,
                "input_data": target_tool_input,
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
                "created_at": now_iso
            }
            _in_memory_approvals[app_id] = app_req
            run["status"] = "waiting_for_approval"

            # Create Attention Item
            await attention_service._upsert_attention_item(
                workspace_id=workspace_id,
                type_name="approval_required",
                title=f"Approval Required: {tool.name}",
                description=app_req["description"],
                severity="high",
                source_type="system_event",
                source_id=f"app_{app_id}"
            )

            _record_step(run_id, "approval", f"Approval requested for tool '{tool.name}'.", tool_name=tool.name, input_data=target_tool_input)
            return run

    elif tool.risk_level == ToolRiskLevel.DESTRUCTIVE:
        run["status"] = "failed"
        run["completed_at"] = now_iso
        _record_step(run_id, "failure", f"Tool '{tool.name}' is destructive and blocked by runtime policy.", error_code="DESTRUCTIVE_ACTION_BLOCKED")
        return run

    # 4. Tool Execution
    _record_step(run_id, "tool_call", f"Executing tool '{tool.name}'.", tool_name=tool.name, input_data=target_tool_input)
    exec_res = await tool.execute(session, workspace_id, target_tool_input)

    if exec_res.success:
        _record_step(run_id, "result", f"Tool '{tool.name}' completed successfully.", tool_name=tool.name, result_data=exec_res.to_dict())
        run["status"] = "completed"
        run["completed_at"] = datetime.now(timezone.utc).isoformat()
        _record_step(run_id, "completion", "Agent run completed goal criteria.")
    else:
        run["status"] = "failed"
        run["completed_at"] = datetime.now(timezone.utc).isoformat()
        _record_step(run_id, "failure", f"Tool execution failed: {exec_res.error}", error_code=exec_res.error_code or "TOOL_EXECUTION_FAILED")

    run["updated_at"] = datetime.now(timezone.utc).isoformat()
    _in_memory_runs[run_id] = run
    return run

def _record_step(
    run_id: str,
    step_type: str,
    summary: str,
    tool_name: Optional[str] = None,
    input_data: Optional[dict] = None,
    result_data: Optional[dict] = None,
    error_code: Optional[str] = None
):
    steps = _in_memory_steps.get(run_id, [])
    now_iso = datetime.now(timezone.utc).isoformat()
    step = {
        "id": f"step_{len(steps)+1}_{run_id}",
        "agent_run_id": run_id,
        "sequence": len(steps) + 1,
        "type": step_type,
        "status": "completed" if not error_code else "failed",
        "tool_name": tool_name,
        "input": input_data or {},
        "result": result_data or {"summary": summary},
        "error_code": error_code,
        "started_at": now_iso,
        "completed_at": now_iso,
        "created_at": now_iso
    }
    steps.append(step)
    _in_memory_steps[run_id] = steps

async def pause_agent_run(session: Optional[AsyncSession], workspace_id: str, run_id: str) -> Optional[dict]:
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        return None
    run["status"] = "paused"
    run["updated_at"] = datetime.now(timezone.utc).isoformat()
    return run

async def resume_agent_run(session: Optional[AsyncSession], workspace_id: str, run_id: str) -> Optional[dict]:
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        return None
    run["status"] = "running"
    run["updated_at"] = datetime.now(timezone.utc).isoformat()
    return await step_agent_run(session, workspace_id, run_id)

async def cancel_agent_run(session: Optional[AsyncSession], workspace_id: str, run_id: str) -> Optional[dict]:
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        return None
    run["status"] = "cancelled"
    run["completed_at"] = datetime.now(timezone.utc).isoformat()
    run["updated_at"] = datetime.now(timezone.utc).isoformat()
    return run

async def approve_approval_request(session: Optional[AsyncSession], workspace_id: str, run_id: str, approval_id: str) -> dict:
    app_req = _in_memory_approvals.get(approval_id)
    if not app_req or app_req["workspace_id"] != workspace_id:
        raise ValueError("Approval request not found.")

    # Idempotency: Double approval check
    if app_req["status"] == "approved":
        return app_req

    if app_req["status"] != "pending":
        raise ValueError(f"Approval request is already {app_req['status']}.")

    app_req["status"] = "approved"
    run = await get_agent_run(session, workspace_id, run_id)
    if run:
        run["status"] = "running"
        tool_input = app_req.get("input_data", {})
        await step_agent_run(session, workspace_id, run_id, requested_tool=app_req["tool_name"], tool_input=tool_input)

    return app_req

async def reject_approval_request(session: Optional[AsyncSession], workspace_id: str, run_id: str, approval_id: str) -> dict:
    app_req = _in_memory_approvals.get(approval_id)
    if not app_req or app_req["workspace_id"] != workspace_id:
        raise ValueError("Approval request not found.")

    app_req["status"] = "rejected"
    run = await get_agent_run(session, workspace_id, run_id)
    if run:
        run["status"] = "cancelled"
        run["completed_at"] = datetime.now(timezone.utc).isoformat()
        _record_step(run_id, "failure", "Approval request rejected by user.", error_code="APPROVAL_REJECTED")

    return app_req
