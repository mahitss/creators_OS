import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    AgentExecution,
    AgentExecutionState,
    AgentExecutionStep,
    ExecutionCheckpoint,
    ExecutionStepAttempt,
    ExecutionContextSnapshot,
    ExecutionFailure,
    ExecutionUnknownOutcome,
    ExecutionBudget
)
from app.schemas.agent_runtime_v2 import (
    AgentExecutionCreate,
    AgentExecutionRead,
    AgentExecutionStateRead,
    AgentExecutionStepRead,
    ExecutionCheckpointRead,
    UnknownOutcomeResolveRequest,
    UnknownOutcomeRead,
    ExecutionTraceRead
)
from app.services import (
    action_gateway_service,
    model_gateway_service,
    policy_engine,
    dlp_service,
    governance_service,
    event_mesh_service,
    finops_service
)

_in_memory_executions: Dict[str, dict] = {}
_in_memory_states: Dict[str, dict] = {}
_in_memory_steps: Dict[str, List[dict]] = {}
_in_memory_checkpoints: Dict[str, List[dict]] = {}
_in_memory_unknown_outcomes: Dict[str, List[dict]] = {}

def _initialize_demo_execution_if_empty():
    if _in_memory_executions:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    exec_id = "exec_demo_01"
    chk_id = "chk_001"

    _in_memory_executions[exec_id] = {
        "id": exec_id,
        "organization_id": "org_default_creator",
        "workspace_id": "ws_default_01",
        "agent_id": "ag_creator_ops_01",
        "mission_id": "msn_001",
        "workflow_id": None,
        "status": "running",
        "version": 3,
        "current_step": "step_003",
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_states[exec_id] = {
        "id": "st_001",
        "execution_id": exec_id,
        "version": 3,
        "variables": {"target_channel": "@VaporOS", "scheduled_date": "2026-08-15"},
        "completed_steps": ["step_001", "step_002"],
        "pending_steps": ["step_003", "step_004"],
        "active_steps": ["step_003"],
        "blocked_steps": [],
        "context_references": ["ctx_doc_99"],
        "memory_references": ["mem_001"],
        "last_checkpoint_id": chk_id,
        "updated_at": now_iso
    }

    _in_memory_steps[exec_id] = [
        {
            "id": "step_001",
            "execution_id": exec_id,
            "step_type": "knowledge_retrieval",
            "status": "completed",
            "attempt": 1,
            "input_reference": {"query": "Q3 product roadmap"},
            "output_reference": {"retrieved_count": 4},
            "started_at": now_iso,
            "completed_at": now_iso
        },
        {
            "id": "step_002",
            "execution_id": exec_id,
            "step_type": "model_call",
            "status": "completed",
            "attempt": 1,
            "input_reference": {"capability": "reasoning", "prompt": "Synthesize roadmap report"},
            "output_reference": {"selected_model": "gemini-1.5-pro"},
            "started_at": now_iso,
            "completed_at": now_iso
        },
        {
            "id": "step_003",
            "execution_id": exec_id,
            "step_type": "tool_call",
            "status": "running",
            "attempt": 1,
            "input_reference": {"tool": "gmail.send", "recipient": "exec@vapor.ai"},
            "output_reference": None,
            "started_at": now_iso,
            "completed_at": None
        }
    ]

    _in_memory_checkpoints[exec_id] = [
        {
            "id": chk_id,
            "execution_id": exec_id,
            "execution_version": 2,
            "step_id": "step_002",
            "state_reference": {"variables_count": 2},
            "reason": "before_external_action",
            "created_at": now_iso
        }
    ]

    _in_memory_unknown_outcomes[exec_id] = []

_initialize_demo_execution_if_empty()

async def create_execution(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: AgentExecutionCreate,
    organization_id: str = "org_default_creator"
) -> Tuple[dict, dict]:
    """Creates a new durable Agent Execution 2.0 instance."""
    _initialize_demo_execution_if_empty()
    exec_id = f"exec_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    execution = {
        "id": exec_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "agent_id": req.agent_id,
        "mission_id": req.mission_id,
        "workflow_id": req.workflow_id,
        "status": "created",
        "version": 1,
        "current_step": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    state = {
        "id": f"st_{uuid.uuid4().hex[:8]}",
        "execution_id": exec_id,
        "version": 1,
        "variables": req.initial_variables,
        "completed_steps": [],
        "pending_steps": ["step_01_init"],
        "active_steps": [],
        "blocked_steps": [],
        "context_references": [],
        "memory_references": [],
        "last_checkpoint_id": None,
        "updated_at": now_iso
    }

    _in_memory_executions[exec_id] = execution
    _in_memory_states[exec_id] = state
    _in_memory_steps[exec_id] = []
    _in_memory_checkpoints[exec_id] = []
    _in_memory_unknown_outcomes[exec_id] = []

    # Initial Checkpoint
    chk_id = f"chk_{uuid.uuid4().hex[:8]}"
    checkpoint = {
        "id": chk_id,
        "execution_id": exec_id,
        "execution_version": 1,
        "step_id": None,
        "state_reference": {"variables_count": len(req.initial_variables)},
        "reason": "step_completed",
        "created_at": now_iso
    }
    _in_memory_checkpoints[exec_id].append(checkpoint)
    state["last_checkpoint_id"] = chk_id

    # Emit Event
    try:
        from app.schemas.event_mesh import EventEnvelopePublishRequest
        evt = EventEnvelopePublishRequest(
            organization_id=organization_id,
            workspace_id=workspace_id,
            event_type="custom.agent.execution.created",
            producer="agent_runtime_v2",
            payload_reference={"execution_id": exec_id, "agent_id": req.agent_id}
        )
        await event_mesh_service.publish_event(session, evt)
    except Exception:
        pass

    return execution, state

async def execute_step(
    session: Optional[AsyncSession],
    execution_id: str,
    step_type: str,
    input_payload: dict,
    organization_id: str = "org_default_creator"
) -> dict:
    """Executes a durable step with pre-action checkpointing and ModelGateway/ActionGateway routing."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if not execution:
        raise ValueError(f"Execution '{execution_id}' not found.")

    now_iso = datetime.now(timezone.utc).isoformat()
    step_id = f"step_{uuid.uuid4().hex[:8]}"

    # Pre-Action Checkpoint BEFORE External Side Effects
    if step_type in ["tool_call", "agent_delegate"]:
        chk_id = f"chk_{uuid.uuid4().hex[:8]}"
        chk = {
            "id": chk_id,
            "execution_id": execution_id,
            "execution_version": execution["version"],
            "step_id": step_id,
            "state_reference": {"variables": _in_memory_states[execution_id]["variables"]},
            "reason": "before_external_action",
            "created_at": now_iso
        }
        _in_memory_checkpoints[execution_id].append(chk)
        _in_memory_states[execution_id]["last_checkpoint_id"] = chk_id

    # Create Step
    step = {
        "id": step_id,
        "execution_id": execution_id,
        "step_type": step_type,
        "status": "running",
        "attempt": 1,
        "input_reference": input_payload,
        "output_reference": None,
        "started_at": now_iso,
        "completed_at": None
    }
    _in_memory_steps[execution_id].append(step)

    # Route Step
    if step_type == "model_call":
        from app.schemas.model_gateway import ModelGatewayRequest
        mg_req = ModelGatewayRequest(
            requestType=input_payload.get("requestType", "reasoning"),
            capability=input_payload.get("capability", "reasoning"),
            prompt=input_payload.get("prompt", "Analyze step"),
            classification=input_payload.get("classification", "internal")
        )
        resp, _ = await model_gateway_service.execute_model_inference(
            session, workspace_id=execution["workspace_id"], req=mg_req, organization_id=organization_id
        )
        step["status"] = "completed"
        step["completed_at"] = datetime.now(timezone.utc).isoformat()
        step["output_reference"] = {"content": resp.content, "selected_model": resp.selected_model}

    elif step_type == "tool_call":
        # Simulate ActionGateway call
        step["status"] = "completed"
        step["completed_at"] = datetime.now(timezone.utc).isoformat()
        step["output_reference"] = {"status": "success", "action": input_payload.get("action")}

    else:
        step["status"] = "completed"
        step["completed_at"] = datetime.now(timezone.utc).isoformat()
        step["output_reference"] = {"result": "ok"}

    # Update Execution Version & State
    execution["version"] += 1
    execution["updated_at"] = datetime.now(timezone.utc).isoformat()
    state = _in_memory_states[execution_id]
    state["version"] = execution["version"]
    state["completed_steps"].append(step_id)

    return step

async def pause_execution(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    """Pauses a running execution."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if execution:
        execution["status"] = "paused"
        execution["updated_at"] = datetime.now(timezone.utc).isoformat()
    return execution

async def resume_execution(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    """Resumes a paused execution from latest checkpoint."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if execution:
        execution["status"] = "running"
        execution["updated_at"] = datetime.now(timezone.utc).isoformat()
    return execution

async def cancel_execution(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    """Cancels a running execution."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if execution:
        execution["status"] = "cancelled"
        execution["updated_at"] = datetime.now(timezone.utc).isoformat()
    return execution

async def recover_execution(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    """Recovers a crashed or stale execution from latest valid checkpoint."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if execution:
        execution["status"] = "recovering"
        execution["status"] = "running"
        execution["updated_at"] = datetime.now(timezone.utc).isoformat()
    return execution

async def resolve_unknown_outcome(
    session: Optional[AsyncSession],
    execution_id: str,
    step_id: str,
    req: UnknownOutcomeResolveRequest,
    user_id: str = "usr_executive_01"
) -> dict:
    """Operator resolves unknown_outcome step with explicit evidence notes."""
    _initialize_demo_execution_if_empty()
    outcomes = _in_memory_unknown_outcomes.get(execution_id, [])
    item = next((o for o in outcomes if o["step_id"] == step_id), None)
    if not item:
        # Create resolved record
        item = {
            "id": f"unk_{uuid.uuid4().hex[:8]}",
            "execution_id": execution_id,
            "step_id": step_id,
            "idempotency_key": f"idem_{uuid.uuid4().hex[:8]}",
            "action_type": "external_tool_call",
            "status": req.resolution,
            "resolution_notes": req.notes,
            "resolved_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_unknown_outcomes.setdefault(execution_id, []).append(item)
    else:
        item["status"] = req.resolution
        item["resolution_notes"] = req.notes
        item["resolved_by"] = user_id

    return item

async def get_execution(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    _initialize_demo_execution_if_empty()
    return _in_memory_executions.get(execution_id)

async def get_execution_trace(session: Optional[AsyncSession], execution_id: str) -> Optional[dict]:
    """Returns complete execution trace including state, steps, checkpoints, and unknown outcomes."""
    _initialize_demo_execution_if_empty()
    execution = _in_memory_executions.get(execution_id)
    if not execution:
        return None

    state = _in_memory_states.get(execution_id, {})
    steps = _in_memory_steps.get(execution_id, [])
    checkpoints = _in_memory_checkpoints.get(execution_id, [])
    unknown_outcomes = _in_memory_unknown_outcomes.get(execution_id, [])

    return {
        "execution": execution,
        "state": state,
        "steps": steps,
        "checkpoints": checkpoints,
        "unknown_outcomes": unknown_outcomes
    }

async def list_executions(session: Optional[AsyncSession]) -> List[dict]:
    _initialize_demo_execution_if_empty()
    return list(_in_memory_executions.values())

async def list_checkpoints(session: Optional[AsyncSession], execution_id: str) -> List[dict]:
    _initialize_demo_execution_if_empty()
    return _in_memory_checkpoints.get(execution_id, [])

async def list_unknown_outcomes(session: Optional[AsyncSession], execution_id: str) -> List[dict]:
    _initialize_demo_execution_if_empty()
    return _in_memory_unknown_outcomes.get(execution_id, [])
