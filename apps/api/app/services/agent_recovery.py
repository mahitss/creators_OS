import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

_in_memory_checkpoints: Dict[str, List[dict]] = {}
_in_memory_tool_executions: Dict[str, dict] = {}

async def claim_run_lease(
    run_dict: dict,
    worker_id: str,
    timeout_seconds: int = 30
) -> bool:
    now = datetime.now(timezone.utc)
    lease_expires = run_dict.get("lease_expires_at")

    if lease_expires:
        exp_dt = datetime.fromisoformat(lease_expires)
        if exp_dt > now and run_dict.get("lease_worker_id") != worker_id:
            # Lease held by another active worker
            return False

    run_dict["lease_worker_id"] = worker_id
    run_dict["lease_expires_at"] = (now + timedelta(seconds=timeout_seconds)).isoformat()
    run_dict["version"] = run_dict.get("version", 1) + 1
    return True

async def save_checkpoint(
    run_id: str,
    current_step: int,
    completed_steps: List[int],
    budget_state: dict,
    pending_action: Optional[str] = None
) -> dict:
    checkpoints = _in_memory_checkpoints.get(run_id, [])
    cp_id = f"cp_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    checkpoint = {
        "id": cp_id,
        "agent_run_id": run_id,
        "sequence": len(checkpoints) + 1,
        "state": {
            "current_step": current_step,
            "completed_steps": completed_steps,
            "pending_action": pending_action,
            "budget_state": budget_state,
            "iteration_count": len(completed_steps)
        },
        "created_at": now_iso
    }
    checkpoints.append(checkpoint)
    _in_memory_checkpoints[run_id] = checkpoints
    return checkpoint

async def get_latest_checkpoint(run_id: str) -> Optional[dict]:
    checkpoints = _in_memory_checkpoints.get(run_id, [])
    if not checkpoints:
        return None
    return checkpoints[-1]

async def record_tool_execution(
    run_id: str,
    step_id: str,
    tool_name: str,
    idempotency_key: str,
    input_hash: str,
    status: str = "pending"
) -> dict:
    exec_id = f"texec_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    texec = {
        "id": exec_id,
        "agent_run_id": run_id,
        "agent_step_id": step_id,
        "tool_name": tool_name,
        "idempotency_key": idempotency_key,
        "status": status,
        "input_hash": input_hash,
        "result_reference": {},
        "started_at": now_iso,
        "completed_at": None,
        "created_at": now_iso
    }
    _in_memory_tool_executions[exec_id] = texec
    return texec

async def resolve_unknown_tool_execution(exec_id: str, verified_result: Optional[dict]) -> dict:
    texec = _in_memory_tool_executions.get(exec_id)
    if not texec:
        raise ValueError("Tool execution record not found.")

    if verified_result:
        texec["status"] = "completed"
        texec["result_reference"] = verified_result
        texec["completed_at"] = datetime.now(timezone.utc).isoformat()
    else:
        texec["status"] = "failed"
    return texec
