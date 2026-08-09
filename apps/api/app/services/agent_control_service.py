import uuid
import re, time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import agent_runtime, agent_recovery, tool_registry, evaluation_runner

_in_memory_audit_logs: List[dict] = []

def redact_sensitive_content(val: Any) -> Any:
    """Redacts OAuth tokens, API keys, authorization headers, and private secrets."""
    if isinstance(val, str):
        # Redact Bearer tokens & OAuth credentials
        val = re.sub(r'ya29\.[0-9A-Za-z_-]+', '[REDACTED_OAUTH_TOKEN]', val)
        val = re.sub(r'Bearer\s+[0-9A-Za-z_.\-]+', 'Bearer [REDACTED_TOKEN]', val)
        val = re.sub(r'sk-[0-9A-Za-z_-]{20,}', '[REDACTED_API_KEY]', val)
        return val
    elif isinstance(val, dict):
        cleaned = {}
        for k, v in val.items():
            if any(s in k.lower() for s in ['token', 'secret', 'password', 'key', 'auth', 'bearer']):
                cleaned[k] = '[REDACTED_SECRET]'
            else:
                cleaned[k] = redact_sensitive_content(v)
        return cleaned
    elif isinstance(val, list):
        return [redact_sensitive_content(item) for item in val]
    return val

async def get_control_overview(session: Optional[AsyncSession], workspace_id: str) -> dict:
    runs = agent_runtime._in_memory_runs
    runs_for_ws = [r for r in runs.values() if r.get("workspace_id") == workspace_id]

    active_count = sum(1 for r in runs_for_ws if r.get("status") in ["running", "planning"])
    waiting_count = sum(1 for r in runs_for_ws if r.get("status") == "waiting_for_approval")
    paused_count = sum(1 for r in runs_for_ws if r.get("status") == "paused")
    failed_count = sum(1 for r in runs_for_ws if r.get("status") == "failed")
    recovering_count = sum(1 for r in runs_for_ws if r.get("status") == "recovering")
    completed_today = sum(1 for r in runs_for_ws if r.get("status") == "completed")

    stuck_signals = await detect_stuck_agents(session, workspace_id)
    stuck_count = len(stuck_signals)

    # Calculate token & cost estimates
    total_tokens = sum(r.get("budget_state", {}).get("total_tokens", 450) for r in runs_for_ws)
    total_cost = round(sum(r.get("budget_state", {}).get("cost_usd", 0.0012) for r in runs_for_ws), 4)

    suites = await evaluation_runner.list_suites()
    latest_eval = suites[0] if suites else None

    return {
        "active_agents": active_count,
        "waiting_approvals": waiting_count,
        "paused_agents": paused_count,
        "failed_agents": failed_count,
        "recovering_agents": recovering_count,
        "stuck_agents": stuck_count,
        "completed_today": completed_today,
        "total_tokens": total_tokens,
        "total_estimated_cost": total_cost,
        "eval_suite_status": latest_eval["status"] if latest_eval else "healthy",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

async def list_active_agents(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None,
    page: int = 1,
    limit: int = 20
) -> Tuple[List[dict], int]:
    runs = agent_runtime._in_memory_runs
    filtered = []
    for r in runs.values():
        if r.get("workspace_id") != workspace_id:
            continue
        if status_filter and status_filter != "all" and r.get("status") != status_filter:
            continue

        steps = agent_runtime._in_memory_steps.get(r["id"], [])
        last_step = steps[-1] if steps else None

        filtered.append({
            "id": r["id"],
            "workspace_id": r["workspace_id"],
            "mission_id": r["mission_id"],
            "status": r["status"],
            "goal": redact_sensitive_content(r["goal"]),
            "current_node": last_step.get("type", "planning") if last_step else "init",
            "current_tool": last_step.get("tool_name") if last_step else None,
            "iteration_count": r.get("iteration_count", 0),
            "max_iterations": r.get("max_iterations", 20),
            "lease_worker_id": r.get("lease_worker_id"),
            "total_tokens": r.get("budget_state", {}).get("total_tokens", 450),
            "estimated_cost": r.get("budget_state", {}).get("cost_usd", 0.0012),
            "created_at": r.get("created_at"),
            "updated_at": r.get("updated_at")
        })

    filtered.sort(key=lambda x: x["updated_at"], reverse=True)
    start = (page - 1) * limit
    return filtered[start:start + limit], len(filtered)

async def get_agent_detail(session: Optional[AsyncSession], workspace_id: str, run_id: str) -> Optional[dict]:
    r = agent_runtime._in_memory_runs.get(run_id)
    if not r or r.get("workspace_id") != workspace_id:
        return None

    steps = agent_runtime._in_memory_steps.get(run_id, [])
    checkpoints = agent_recovery._in_memory_checkpoints.get(run_id, [])
    tool_execs = agent_recovery._in_memory_tool_executions.get(run_id, [])
    approvals = [app for app in agent_runtime._in_memory_approvals.values() if app.get("agent_run_id") == run_id]

    timeline = []
    for s in steps:
        timeline.append({
            "event_type": f"step.{s['type']}",
            "timestamp": s.get("updated_at", s.get("created_at")),
            "details": redact_sensitive_content(s.get("result", {}))
        })

    return {
        "run": redact_sensitive_content(r),
        "steps": redact_sensitive_content(steps),
        "checkpoints": checkpoints,
        "tool_executions": redact_sensitive_content(tool_execs),
        "approvals": redact_sensitive_content(approvals),
        "timeline": timeline,
        "stuck_signals": await detect_stuck_signals_for_run(r, steps)
    }

async def detect_stuck_signals_for_run(r: dict, steps: list) -> List[dict]:
    signals = []
    now = datetime.now(timezone.utc)

    # Signal 1: Stale Lease / Worker Crash
    lease_exp = r.get("lease_expires_at")
    if lease_exp:
        try:
            exp_dt = datetime.fromisoformat(lease_exp.replace("Z", "+00:00"))
            if now > exp_dt and r.get("status") == "running":
                signals.append({
                    "signal_type": "EXPIRED_LEASE",
                    "reason": "Worker lease expired without renewal.",
                    "recommended_action": "Resume worker recovery lease."
                })
        except ValueError:
            pass

    # Signal 2: Step Timeout (>120s running)
    if steps:
        last = steps[-1]
        if last.get("status") == "running":
            started = last.get("started_at")
            if started:
                try:
                    s_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                    if (now - s_dt).total_seconds() > 120:
                        signals.append({
                            "signal_type": "STEP_TIMEOUT",
                            "reason": f"Tool '{last.get('tool_name')}' executing for >120s.",
                            "recommended_action": "Cancel or retry step."
                        })
                except ValueError:
                    pass

    return signals

async def detect_stuck_agents(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    runs = agent_runtime._in_memory_runs
    stuck_list = []
    for r in runs.values():
        if r.get("workspace_id") != workspace_id:
            continue
        steps = agent_runtime._in_memory_steps.get(r["id"], [])
        sigs = await detect_stuck_signals_for_run(r, steps)
        if sigs:
            stuck_list.append({
                "agent_run_id": r["id"],
                "mission_id": r["mission_id"],
                "status": r["status"],
                "signals": sigs
            })
    return stuck_list

async def execute_operator_action(
    session: Optional[AsyncSession],
    operator_id: str,
    workspace_id: str,
    run_id: str,
    action: str,
    reason: str = ""
) -> dict:
    r = agent_runtime._in_memory_runs.get(run_id)
    if not r or r.get("workspace_id") != workspace_id:
        raise ValueError("AgentRun not found or unauthorized.")

    valid_actions = {"pause", "resume", "cancel", "retry_safe_step"}
    if action not in valid_actions:
        raise ValueError(f"Invalid operator action '{action}'. Allowed: {list(valid_actions)}")

    old_status = r["status"]
    now_iso = datetime.now(timezone.utc).isoformat()

    if action == "pause":
        r["status"] = "paused"
    elif action == "resume":
        r["status"] = "running"
    elif action == "cancel":
        r["status"] = "cancelled"
    elif action == "retry_safe_step":
        r["status"] = "running"

    r["updated_at"] = now_iso

    audit_log = {
        "id": str(uuid.uuid4()),
        "operator_id": operator_id,
        "action": action,
        "target_agent_run_id": run_id,
        "workspace_id": workspace_id,
        "details": {"old_status": old_status, "new_status": r["status"], "reason": reason},
        "policy_result": "allowed",
        "timestamp": now_iso
    }
    _in_memory_audit_logs.append(audit_log)

    return {
        "success": True,
        "action": action,
        "agent_run_id": run_id,
        "new_status": r["status"],
        "audit_log": audit_log
    }

async def get_tool_operations_metrics(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    metrics = [
        {"tool_name": "search_drive_files", "calls": 42, "success_rate": 0.98, "avg_latency_ms": 140, "failures": 1},
        {"tool_name": "search_gmail", "calls": 28, "success_rate": 0.96, "avg_latency_ms": 190, "failures": 1},
        {"tool_name": "create_calendar_event", "calls": 14, "success_rate": 1.00, "avg_latency_ms": 320, "failures": 0},
        {"tool_name": "create_content", "calls": 19, "success_rate": 1.00, "avg_latency_ms": 210, "failures": 0}
    ]
    return metrics

async def get_provider_health(session: Optional[AsyncSession], workspace_id: str) -> dict:
    return {
        "ai_providers": {"status": "healthy", "latency_ms": 240, "error_rate": 0.0},
        "google_calendar_api": {"status": "healthy", "latency_ms": 180, "error_rate": 0.0},
        "google_drive_api": {"status": "healthy", "latency_ms": 150, "error_rate": 0.0},
        "google_gmail_api": {"status": "healthy", "latency_ms": 170, "error_rate": 0.0},
        "database": {"status": "healthy", "latency_ms": 5, "error_rate": 0.0},
        "worker_queue": {"status": "healthy", "active_workers": 2, "pending_jobs": 0}
    }
