"""Production-Grade Bounded Agent Runtime Engine with Model Gateway, Structured Output & Governed Tool Execution."""

import os
import uuid
import json
import re
import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.agent_lifecycle import (
    AgentStatus,
    AgentRunStatus,
    AgentEventType,
    AgentFailureType,
    ToolRiskLevel,
    validate_agent_status_transition,
    validate_agent_run_status_transition,
    validate_agent_executable,
    is_retryable_agent_failure,
    InvalidAgentRunStateTransitionError,
)
from app.services.agent_context import ContextAssembler
from app.services.tool_registry import ToolRegistry, authorize_and_execute_tool, ToolExecutionResult
from app.services import model_gateway_service
from app.schemas.model_gateway import ModelGatewayRequest
from packages.database.models import AgentRun, AgentObservation, AgentEvent

logger = logging.getLogger("kinetiq.agent.runtime")

# In-memory fast stores for local / test execution
_in_memory_agents: Dict[str, Dict[str, Any]] = {}
_in_memory_agent_versions: Dict[str, List[Dict[str, Any]]] = {}
_in_memory_agent_runs: Dict[str, Dict[str, Any]] = {}
_in_memory_agent_observations: Dict[str, List[Dict[str, Any]]] = {}
_in_memory_agent_events: Dict[str, List[Dict[str, Any]]] = {}

# Active SSE listener queues per agent_run_id
_active_agent_subscribers: Dict[str, Set[asyncio.Queue]] = {}

# Active task tracking, cancellation flags, and pause events
_active_run_tasks: Dict[str, asyncio.Task] = {}
_run_cancel_flags: Dict[str, bool] = {}
_run_pause_events: Dict[str, asyncio.Event] = {}


class StructuredModelAction(BaseModel):
    action: str = Field(..., pattern="^(RESPOND|TOOL_CALL|WAIT|COMPLETE|FAIL)$")
    tool: Optional[str] = None
    arguments: Dict[str, Any] = Field(default_factory=dict)
    reason: Optional[str] = ""
    response: Optional[str] = None


def _get_or_create_subscriber_set(run_id: str) -> Set[asyncio.Queue]:
    if run_id not in _active_agent_subscribers:
        _active_agent_subscribers[run_id] = set()
    return _active_agent_subscribers[run_id]


async def record_agent_event(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_run_id: str,
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    mission_id: Optional[str] = None,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """Appends event to immutable agent event store and broadcasts to active SSE subscribers."""
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    evt_id = str(uuid.uuid4())
    corr_id = correlation_id or str(uuid.uuid4())

    event_record = {
        "id": evt_id,
        "agent_run_id": agent_run_id,
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "event_type": event_type,
        "correlation_id": corr_id,
        "timestamp": now_iso,
        "payload": payload or {}
    }

    if agent_run_id not in _in_memory_agent_events:
        _in_memory_agent_events[agent_run_id] = []
    _in_memory_agent_events[agent_run_id].append(event_record)

    # Persist to database if in production Postgres
    if session is not None:
        db_url = os.getenv("DATABASE_URL", "")
        if "postgres" in db_url or "neon.tech" in db_url:
            try:
                db_event = AgentEvent(
                    id=uuid.UUID(evt_id),
                    agent_run_id=uuid.UUID(agent_run_id) if len(agent_run_id) == 36 else uuid.uuid4(),
                    workspace_id=uuid.UUID(workspace_id) if len(workspace_id) == 36 else uuid.uuid4(),
                    mission_id=uuid.UUID(mission_id) if mission_id and len(mission_id) == 36 else None,
                    event_type=event_type,
                    correlation_id=corr_id,
                    timestamp=now_dt,
                    payload=payload or {}
                )
                if hasattr(session, "is_active") and session.is_active:
                    session.add(db_event)
            except Exception as exc:
                logger.debug(f"Could not persist AgentEvent to DB: {exc}")

    # Broadcast to SSE subscribers
    subscribers = _active_agent_subscribers.get(agent_run_id, set())
    for q in list(subscribers):
        try:
            q.put_nowait(event_record)
        except Exception:
            pass

    return event_record


async def record_agent_observation(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_run_id: str,
    step_number: int,
    observation_type: str,
    tool_name: Optional[str],
    status: str,
    summary: str,
    raw_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Records a step observation for execution trace and replay."""
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    obs_id = str(uuid.uuid4())

    obs_record = {
        "id": obs_id,
        "agent_run_id": agent_run_id,
        "workspace_id": workspace_id,
        "step_number": step_number,
        "observation_type": observation_type,
        "tool_name": tool_name,
        "status": status,
        "summary": summary,
        "raw_data": raw_data or {},
        "timestamp": now_iso
    }

    if agent_run_id not in _in_memory_agent_observations:
        _in_memory_agent_observations[agent_run_id] = []
    _in_memory_agent_observations[agent_run_id].append(obs_record)

    await record_agent_event(
        session=session,
        workspace_id=workspace_id,
        agent_run_id=agent_run_id,
        event_type=AgentEventType.OBSERVATION_RECORDED.value,
        payload=obs_record
    )
    return obs_record


class AgentRuntimeEngine:
    """Core Asynchronous Runtime Loop for Autonomous Agent Execution."""

    def parse_structured_output(self, content: str) -> StructuredModelAction:
        """Parses model response into validated StructuredModelAction, stripping markdown blocks if present."""
        if not content:
            return StructuredModelAction(action="RESPOND", response="Empty model response.", reason="No output produced.")

        clean_text = content.strip()

        # Extract JSON from markdown backticks if present
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean_text, re.DOTALL)
        if json_match:
            clean_text = json_match.group(1).strip()
        elif clean_text.startswith("```") and clean_text.endswith("```"):
            clean_text = clean_text.strip("`").strip()

        try:
            parsed = json.loads(clean_text)
            action_str = str(parsed.get("action", "")).upper()
            return StructuredModelAction(
                action=action_str if action_str in ["RESPOND", "TOOL_CALL", "WAIT", "COMPLETE", "FAIL"] else "RESPOND",
                tool=parsed.get("tool"),
                arguments=parsed.get("arguments") or {},
                reason=parsed.get("reason", ""),
                response=parsed.get("response") or parsed.get("result") or clean_text
            )
        except Exception:
            # Fallback: model returned natural language text -> map to RESPOND action
            return StructuredModelAction(
                action="RESPOND",
                response=content,
                reason="Natural language response parsed."
            )

    async def execute_agent_run(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        run_id: str,
        user_id: str = "usr_agent_runner",
        user_role: str = "ADMIN"
    ) -> Dict[str, Any]:
        """Executes the full bounded runtime execution loop for an AgentRun."""
        run = _in_memory_agent_runs.get(run_id)
        if not run:
            raise ValueError(f"AgentRun {run_id} not found.")

        if run.get("workspace_id") != workspace_id:
            raise PermissionError("Cross-workspace AgentRun execution rejected.")

        agent_id = run["agent_id"]
        agent = _in_memory_agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found.")

        agent_version_id = run["agent_version_id"]
        versions = _in_memory_agent_versions.get(agent_id, [])
        agent_version = next((v for v in versions if v["id"] == agent_version_id), None)
        if not agent_version:
            # Fallback to agent default version spec
            agent_version = {
                "id": agent_version_id,
                "agent_id": agent_id,
                "version": 1,
                "instructions": agent.get("system_instructions", ""),
                "capabilities": agent.get("capabilities", []),
                "tool_policy": {"allowed_tools": agent.get("allowed_tools", [])},
                "model_policy": {"allowed_models": agent.get("allowed_models", [])},
                "limits": {
                    "max_steps": agent.get("max_steps", 20),
                    "max_runtime_seconds": agent.get("max_runtime_seconds", 300),
                    "max_token_budget": agent.get("max_token_budget", 100000)
                }
            }

        # 1. Enforce executable status guard (DISABLED and ARCHIVED agents cannot execute)
        validate_agent_executable(agent_id, agent.get("status", "ACTIVE"))

        # Setup cancellation and pause tracking
        _run_cancel_flags[run_id] = False
        pause_evt = _run_pause_events.setdefault(run_id, asyncio.Event())
        pause_evt.set()

        # Hard Ceilings
        limits = agent_version.get("limits", {})
        max_steps = min(limits.get("max_steps") or agent.get("max_steps", 20), 50)
        max_runtime = limits.get("max_runtime_seconds") or agent.get("max_runtime_seconds", 300)
        max_token_budget = limits.get("max_token_budget") or agent.get("max_token_budget", 100000)

        start_time = time.time()
        now_iso = datetime.now(timezone.utc).isoformat()
        run["started_at"] = run["started_at"] or now_iso
        run["status"] = AgentRunStatus.INITIALIZING.value

        await record_agent_event(
            session=None,
            workspace_id=workspace_id,
            agent_run_id=run_id,
            mission_id=run.get("mission_id"),
            event_type=AgentEventType.AGENT_INITIALIZED.value,
            payload={"status": AgentRunStatus.INITIALIZING.value, "started_at": run["started_at"]}
        )

        assembler = ContextAssembler(workspace_id=workspace_id)
        current_step = run.get("current_step", 0)

        try:
            while current_step < max_steps:
                # 1. Cancellation Guard
                if _run_cancel_flags.get(run_id, False):
                    run["status"] = AgentRunStatus.CANCELLED.value
                    run["completed_at"] = datetime.now(timezone.utc).isoformat()
                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_COMPLETED.value,
                        payload={"status": AgentRunStatus.CANCELLED.value, "reason": "Cancelled by user."}
                    )
                    return run

                # 2. Pause Guard (at safe step boundary)
                if not pause_evt.is_set():
                    run["status"] = AgentRunStatus.WAITING_TOOL.value # paused marker
                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_PAUSED.value,
                        payload={"status": "PAUSED", "step": current_step}
                    )
                    await pause_evt.wait()

                # 3. Runtime Watchdog Limit
                elapsed = time.time() - start_time
                if elapsed > max_runtime:
                    run["status"] = AgentRunStatus.TIMED_OUT.value
                    run["completed_at"] = datetime.now(timezone.utc).isoformat()
                    run["error_info"] = {"code": AgentFailureType.RUNTIME_TIMEOUT.value, "message": f"Execution exceeded max runtime of {max_runtime}s."}
                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_FAILED.value,
                        payload=run["error_info"]
                    )
                    return run

                # 4. Token Budget Limit
                if run.get("total_tokens", 0) >= max_token_budget:
                    run["status"] = AgentRunStatus.FAILED.value
                    run["completed_at"] = datetime.now(timezone.utc).isoformat()
                    run["error_info"] = {"code": AgentFailureType.TOKEN_LIMIT.value, "message": f"Token budget of {max_token_budget} exceeded."}
                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_FAILED.value,
                        payload=run["error_info"]
                    )
                    return run

                current_step += 1
                run["current_step"] = current_step
                run["status"] = AgentRunStatus.EXECUTING.value

                await record_agent_event(
                    session=None,
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    mission_id=run.get("mission_id"),
                    event_type=AgentEventType.AGENT_STEP_STARTED.value,
                    payload={"step_number": current_step}
                )

                # 5. Assemble Context
                observations = _in_memory_agent_observations.get(run_id, [])
                context_result = await assembler.assemble_context(
                    session=session,
                    agent=agent,
                    agent_version=agent_version,
                    mission_id=run.get("mission_id"),
                    goal=run.get("goal", ""),
                    user_context=run.get("context"),
                    observations=observations,
                    max_context_tokens=16384
                )

                await record_agent_event(
                    session=None,
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    mission_id=run.get("mission_id"),
                    event_type=AgentEventType.CONTEXT_ASSEMBLED.value,
                    payload={"sources_count": len(context_result["sources_used"]), "estimated_tokens": context_result["estimated_tokens"]}
                )

                # 6. Format Model Gateway Request
                available_tools = ToolRegistry.list_tools()
                tools_prompt = json.dumps([{"name": t["name"], "description": t["description"], "input_schema": t["input_schema"]} for t in available_tools], indent=2)

                prompt_with_tools = (
                    f"{context_result['assembled_prompt']}\n\n"
                    f"### AVAILABLE TOOLS\n{tools_prompt}\n\n"
                    f"### ACTION REQUIREMENT\n"
                    f"Emit your decision as a valid JSON object matching this schema:\n"
                    f'{{"action": "TOOL_CALL" | "RESPOND" | "COMPLETE" | "FAIL", "tool": "tool_name", "arguments": {{}}, "reason": "...", "response": "..."}}'
                )

                model_req = ModelGatewayRequest(
                    requestType="reasoning",
                    capability="reasoning",
                    prompt=prompt_with_tools,
                    classification="internal",
                    parameters={"temperature": 0.2, "response_format": {"type": "json_object"}}
                )

                await record_agent_event(
                    session=None,
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    mission_id=run.get("mission_id"),
                    event_type=AgentEventType.MODEL_REQUESTED.value,
                    payload={"step": current_step}
                )

                # 7. Model Gateway Inference
                gateway_res, decision = await model_gateway_service.execute_model_inference(
                    session=session,
                    workspace_id=workspace_id,
                    req=model_req
                )

                # Update token and cost usage
                in_tok = gateway_res.usage.get("input_tokens", 0)
                out_tok = gateway_res.usage.get("output_tokens", 0)
                tot_tok = in_tok + out_tok
                cost_usd = gateway_res.estimated_cost or 0.0

                run["input_tokens"] = run.get("input_tokens", 0) + in_tok
                run["output_tokens"] = run.get("output_tokens", 0) + out_tok
                run["total_tokens"] = run.get("total_tokens", 0) + tot_tok
                run["cost_usd"] = run.get("cost_usd", 0.0) + cost_usd

                await record_agent_event(
                    session=None,
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    mission_id=run.get("mission_id"),
                    event_type=AgentEventType.MODEL_RESPONDED.value,
                    payload={"model": gateway_res.selected_model, "tokens": tot_tok, "cost_usd": cost_usd}
                )

                # 8. Parse Structured Model Action
                action_struct = self.parse_structured_output(gateway_res.content)

                # Handle Termination Actions
                if action_struct.action in ["RESPOND", "COMPLETE"]:
                    run["status"] = AgentRunStatus.COMPLETED.value
                    run["completed_at"] = datetime.now(timezone.utc).isoformat()
                    run["duration_ms"] = int((time.time() - start_time) * 1000)
                    run["result_data"] = {
                        "final_response": action_struct.response or action_struct.reason,
                        "total_steps": current_step,
                        "status": "success"
                    }

                    await record_agent_observation(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        step_number=current_step,
                        observation_type="final_result",
                        tool_name=None,
                        status="success",
                        summary=action_struct.reason or "Agent completed goal.",
                        raw_data=run["result_data"]
                    )

                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_COMPLETED.value,
                        payload=run["result_data"]
                    )
                    return run

                if action_struct.action == "FAIL":
                    run["status"] = AgentRunStatus.FAILED.value
                    run["completed_at"] = datetime.now(timezone.utc).isoformat()
                    run["error_info"] = {"code": AgentFailureType.UNKNOWN.value, "message": action_struct.reason or "Model failed execution."}
                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.AGENT_FAILED.value,
                        payload=run["error_info"]
                    )
                    return run

                # 9. Governed Tool Execution
                if action_struct.action == "TOOL_CALL" and action_struct.tool:
                    run["status"] = AgentRunStatus.WAITING_TOOL.value
                    t_name = action_struct.tool
                    t_args = action_struct.arguments or {}

                    await record_agent_event(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        mission_id=run.get("mission_id"),
                        event_type=AgentEventType.TOOL_REQUESTED.value,
                        payload={"tool": t_name, "args": t_args, "reason": action_struct.reason}
                    )

                    # Authorize & Execute with bounded backoff
                    idempotency_key = f"{run_id}_step_{current_step}_{t_name}"
                    tool_result: Optional[ToolExecutionResult] = None
                    retry_count = 0
                    max_retries = 3

                    while retry_count <= max_retries:
                        tool_result = await authorize_and_execute_tool(
                            session=session,
                            workspace_id=workspace_id,
                            user_id=user_id,
                            user_role=user_role,
                            agent=agent,
                            agent_version=agent_version,
                            tool_name=t_name,
                            input_data=t_args,
                            idempotency_key=idempotency_key
                        )

                        if tool_result.success:
                            await record_agent_event(
                                session=None,
                                workspace_id=workspace_id,
                                agent_run_id=run_id,
                                mission_id=run.get("mission_id"),
                                event_type=AgentEventType.TOOL_EXECUTED.value,
                                payload={"tool": t_name, "status": "success"}
                            )
                            break

                        # Check if failure is retryable
                        if is_retryable_agent_failure(tool_result.error_code or "TOOL_ERROR") and retry_count < max_retries:
                            retry_count += 1
                            backoff_sec = (2 ** retry_count) * 0.5
                            logger.info(f"Retrying tool '{t_name}' in {backoff_sec}s (attempt {retry_count}/{max_retries})")
                            await asyncio.sleep(backoff_sec)
                        else:
                            # Denied or unretryable error
                            event_type = AgentEventType.TOOL_DENIED.value if tool_result.error_code in ["POLICY_DENIED", "AUTH_ERROR"] else AgentEventType.TOOL_EXECUTED.value
                            await record_agent_event(
                                session=None,
                                workspace_id=workspace_id,
                                agent_run_id=run_id,
                                mission_id=run.get("mission_id"),
                                event_type=event_type,
                                payload={"tool": t_name, "status": "error", "error": tool_result.error, "error_code": tool_result.error_code}
                            )
                            break

                    # 10. Record Step Observation
                    run["status"] = AgentRunStatus.OBSERVING.value
                    obs_status = "success" if tool_result.success else ("denied" if tool_result.error_code in ["POLICY_DENIED", "AUTH_ERROR"] else "failed")
                    obs_summary = f"Executed {t_name}: {action_struct.reason}" if tool_result.success else f"Failed {t_name}: {tool_result.error}"

                    await record_agent_observation(
                        session=None,
                        workspace_id=workspace_id,
                        agent_run_id=run_id,
                        step_number=current_step,
                        observation_type="tool_result",
                        tool_name=t_name,
                        status=obs_status,
                        summary=obs_summary,
                        raw_data=tool_result.data if tool_result.success else {"error": tool_result.error, "code": tool_result.error_code}
                    )

                await record_agent_event(
                    session=None,
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    mission_id=run.get("mission_id"),
                    event_type=AgentEventType.AGENT_STEP_COMPLETED.value,
                    payload={"step_number": current_step}
                )

            # Reached max steps without final respond
            run["status"] = AgentRunStatus.COMPLETED.value
            run["completed_at"] = datetime.now(timezone.utc).isoformat()
            run["duration_ms"] = int((time.time() - start_time) * 1000)
            run["result_data"] = {"total_steps": current_step, "summary": f"Completed execution budget of {max_steps} steps."}

            await record_agent_event(
                session=None,
                workspace_id=workspace_id,
                agent_run_id=run_id,
                mission_id=run.get("mission_id"),
                event_type=AgentEventType.AGENT_COMPLETED.value,
                payload=run["result_data"]
            )
            return run

        except Exception as exc:
            logger.error(f"Fatal error in agent run {run_id}: {exc}", exc_info=True)
            run["status"] = AgentRunStatus.FAILED.value
            run["completed_at"] = datetime.now(timezone.utc).isoformat()
            run["error_info"] = {"code": AgentFailureType.UNKNOWN.value, "message": str(exc)}

            await record_agent_event(
                session=None,
                workspace_id=workspace_id,
                agent_run_id=run_id,
                mission_id=run.get("mission_id"),
                event_type=AgentEventType.AGENT_FAILED.value,
                payload=run["error_info"]
            )
            return run


# Singleton engine instance
agent_runtime_engine = AgentRuntimeEngine()
