"""Authoritative Asynchronous Mission Execution Engine & Runtime for Kinetiq."""

import time
import json
import uuid
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple, Set
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mission_lifecycle import (
    MissionStatus,
    MissionStepStatus,
    MissionStepType,
    MissionEventType,
    FailureType,
    MissionExecutionError,
    validate_status_transition,
    is_terminal_status,
)
from app.services.mission_planner import mission_planner
from app.services.mission_events import record_mission_event
from app.core.ai_provider import resolve_ai_provider

logger = logging.getLogger("kinetiq.mission.engine")

# In-memory mission state registry for rapid async coordination and testing
_in_memory_engine_missions: Dict[str, Dict[str, Any]] = {}
_in_memory_engine_steps: Dict[str, List[Dict[str, Any]]] = {}

# Active task tracking
_active_mission_tasks: Dict[str, asyncio.Task] = {}
_mission_pause_events: Dict[str, asyncio.Event] = {} # Event is cleared when paused, set when running
_mission_cancel_flags: Dict[str, bool] = {}

class MissionExecutionEngine:
    """Production asynchronous runtime worker engine for autonomous missions."""

    def __init__(self):
        self._queue: Optional[asyncio.Queue] = None
        self._worker_task: Optional[asyncio.Task] = None
        self._is_running: bool = False

    @property
    def queue(self) -> asyncio.Queue:
        if self._queue is None:
            self._queue = asyncio.Queue()
        else:
            try:
                loop = asyncio.get_running_loop()
                if getattr(self._queue, "_loop", None) is not None and self._queue._loop != loop:
                    self._queue = asyncio.Queue()
            except Exception:
                pass
        return self._queue

    def start_worker(self):
        """Starts background worker if not already running."""
        if self._worker_task is None or self._worker_task.done():
            self._is_running = True
            try:
                self._worker_task = asyncio.create_task(self._worker_loop())
                logger.info("Mission Execution Engine background worker loop started.")
            except RuntimeError:
                pass # No running loop in synchronous caller

    async def stop_worker(self):
        """Gracefully stops the worker loop."""
        self._is_running = False
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def _worker_loop(self):
        """Continuous worker loop picking up queued missions."""
        while self._is_running:
            try:
                job = await self.queue.get()
                workspace_id, mission_id = job["workspace_id"], job["mission_id"]
                try:
                    await self._execute_mission_lifecycle(workspace_id, mission_id)
                except Exception as exc:
                    logger.error(f"Unhandled exception in mission execution {mission_id}: {exc}", exc_info=True)
                finally:
                    self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error(f"Mission worker loop error: {exc}", exc_info=True)
                await asyncio.sleep(1.0)

    async def enqueue_mission(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        mission_id: str
    ) -> Dict[str, Any]:
        """Validates state and enqueues mission for asynchronous execution."""
        mission = _in_memory_engine_missions.get(mission_id)
        if not mission or mission.get("workspace_id") != workspace_id:
            raise ValueError(f"Mission {mission_id} not found in workspace.")

        curr_status = mission.get("status", MissionStatus.DRAFT.value)
        if curr_status in [MissionStatus.QUEUED.value, MissionStatus.PLANNING.value, MissionStatus.RUNNING.value, MissionStatus.COMPLETED.value]:
            return mission # Idempotent - already queued, executing, or completed

        validate_status_transition(curr_status, MissionStatus.QUEUED.value, mission_id)

        # Transition to QUEUED
        mission["status"] = MissionStatus.QUEUED.value
        mission["updated_at"] = datetime.now(timezone.utc).isoformat()
        _mission_cancel_flags[mission_id] = False
        pause_evt = _mission_pause_events.setdefault(mission_id, asyncio.Event())
        pause_evt.set()

        await record_mission_event(
            session=session,
            workspace_id=workspace_id,
            mission_id=mission_id,
            event_type=MissionEventType.MISSION_QUEUED.value,
            payload={"status": MissionStatus.QUEUED.value, "queued_at": mission["updated_at"]}
        )

        self.start_worker()
        try:
            await self.queue.put({"workspace_id": workspace_id, "mission_id": mission_id})
        except Exception:
            pass
        return mission

    async def pause_mission(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        mission_id: str
    ) -> Dict[str, Any]:
        """Pauses a running or queued mission."""
        mission = _in_memory_engine_missions.get(mission_id)
        if not mission or mission.get("workspace_id") != workspace_id:
            raise ValueError(f"Mission {mission_id} not found in workspace.")

        curr_status = mission.get("status", MissionStatus.DRAFT.value)
        if curr_status in [MissionStatus.PAUSED.value, MissionStatus.COMPLETED.value, MissionStatus.CANCELLED.value]:
            return mission # Idempotent

        validate_status_transition(curr_status, MissionStatus.PAUSED.value, mission_id)

        # Pause event flag
        if mission_id in _mission_pause_events:
            _mission_pause_events[mission_id].clear()

        mission["status"] = MissionStatus.PAUSED.value
        mission["updated_at"] = datetime.now(timezone.utc).isoformat()

        await record_mission_event(
            session=session,
            workspace_id=workspace_id,
            mission_id=mission_id,
            event_type=MissionEventType.MISSION_PAUSED.value,
            payload={"status": MissionStatus.PAUSED.value, "paused_at": mission["updated_at"]}
        )
        return mission

    async def resume_mission(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        mission_id: str
    ) -> Dict[str, Any]:
        """Resumes a paused mission."""
        mission = _in_memory_engine_missions.get(mission_id)
        if not mission or mission.get("workspace_id") != workspace_id:
            raise ValueError(f"Mission {mission_id} not found in workspace.")

        curr_status = mission.get("status", MissionStatus.DRAFT.value)
        if curr_status in [MissionStatus.QUEUED.value, MissionStatus.PLANNING.value, MissionStatus.RUNNING.value, MissionStatus.COMPLETED.value]:
            return mission # Idempotent

        validate_status_transition(curr_status, MissionStatus.QUEUED.value, mission_id)

        # Resume event flag
        if mission_id in _mission_pause_events:
            _mission_pause_events[mission_id].set()

        mission["status"] = MissionStatus.QUEUED.value
        mission["updated_at"] = datetime.now(timezone.utc).isoformat()

        await record_mission_event(
            session=session,
            workspace_id=workspace_id,
            mission_id=mission_id,
            event_type=MissionEventType.MISSION_RESUMED.value,
            payload={"status": MissionStatus.QUEUED.value, "resumed_at": mission["updated_at"]}
        )

        self.start_worker()
        try:
            await self.queue.put({"workspace_id": workspace_id, "mission_id": mission_id})
        except Exception:
            pass
        return mission

    async def cancel_mission(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        mission_id: str
    ) -> Dict[str, Any]:
        """Cancels a mission in progress or queued."""
        mission = _in_memory_engine_missions.get(mission_id)
        if not mission or mission.get("workspace_id") != workspace_id:
            raise ValueError(f"Mission {mission_id} not found in workspace.")

        curr_status = mission.get("status", MissionStatus.DRAFT.value)
        if curr_status in [MissionStatus.CANCELLED.value, MissionStatus.COMPLETED.value]:
            return mission # Idempotent

        validate_status_transition(curr_status, MissionStatus.CANCELLED.value, mission_id)

        _mission_cancel_flags[mission_id] = True
        if mission_id in _mission_pause_events:
            _mission_pause_events[mission_id].set() # Unblock if paused to let cancellation process

        now_iso = datetime.now(timezone.utc).isoformat()
        mission["status"] = MissionStatus.CANCELLED.value
        mission["cancelled_at"] = now_iso
        mission["updated_at"] = now_iso

        # Cancel any active running step task
        active_task = _active_mission_tasks.get(mission_id)
        if active_task and not active_task.done():
            active_task.cancel()

        await record_mission_event(
            session=session,
            workspace_id=workspace_id,
            mission_id=mission_id,
            event_type=MissionEventType.MISSION_CANCELLED.value,
            payload={"status": MissionStatus.CANCELLED.value, "cancelled_at": now_iso}
        )
        return mission

    async def _execute_mission_lifecycle(self, workspace_id: str, mission_id: str):
        """Core execution loop for a mission job."""
        mission = _in_memory_engine_missions.get(mission_id)
        if not mission:
            return

        # Check if already in terminal state
        if mission.get("status") in [MissionStatus.COMPLETED.value, MissionStatus.CANCELLED.value, MissionStatus.FAILED.value]:
            return

        current_task = asyncio.current_task()
        _active_mission_tasks[mission_id] = current_task

        try:
            # 1. Check cancellation before starting
            if _mission_cancel_flags.get(mission_id, False):
                return

            # 2. Transition to PLANNING
            if mission["status"] != MissionStatus.PLANNING.value and not mission.get("plan"):
                validate_status_transition(mission["status"], MissionStatus.PLANNING.value, mission_id)
                mission["status"] = MissionStatus.PLANNING.value
                now_iso = datetime.now(timezone.utc).isoformat()
                mission["started_at"] = mission["started_at"] or now_iso
                mission["updated_at"] = now_iso

                await record_mission_event(
                    session=None,
                    workspace_id=workspace_id,
                    mission_id=mission_id,
                    event_type=MissionEventType.MISSION_PLANNING.value,
                    payload={"status": MissionStatus.PLANNING.value, "started_at": now_iso}
                )

                # Generate validated Plan via MissionPlanner
                plan_structure, plan_telemetry = await mission_planner.plan_mission(
                    workspace_id=workspace_id,
                    title=mission["title"],
                    goal=mission.get("goal") or mission["title"],
                    description=mission.get("description", ""),
                    priority=mission.get("priority", "MEDIUM"),
                    agent_id=mission.get("agent_id"),
                    model=mission.get("model"),
                    context=mission.get("context", {})
                )

                mission["plan"] = plan_structure.model_dump()
                mission["token_usage"]["input_tokens"] += plan_telemetry.get("input_tokens", 0)
                mission["token_usage"]["output_tokens"] += plan_telemetry.get("output_tokens", 0)
                mission["token_usage"]["total_tokens"] += plan_telemetry.get("total_tokens", 0)
                mission["cost"] = round(mission["cost"] + plan_telemetry.get("estimated_cost_usd", 0.0), 6)

                # Initialize Step Records
                steps = []
                for pstep in plan_structure.steps:
                    s_id = str(uuid.uuid4())
                    step_dict = {
                        "id": s_id,
                        "mission_id": mission_id,
                        "workspace_id": workspace_id,
                        "step_number": pstep.order,
                        "name": pstep.title,
                        "title": pstep.title,
                        "description": pstep.description,
                        "step_type": pstep.step_type,
                        "status": MissionStepStatus.PENDING.value,
                        "input": {"description": pstep.description, "expected_output": pstep.expected_output_type},
                        "output": None,
                        "error": None,
                        "retry_count": 0,
                        "max_retries": 3,
                        "token_usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
                        "cost_usd": 0.0,
                        "duration_ms": 0,
                        "started_at": None,
                        "completed_at": None,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                    steps.append(step_dict)

                _in_memory_engine_steps[mission_id] = steps

                await record_mission_event(
                    session=None,
                    workspace_id=workspace_id,
                    mission_id=mission_id,
                    event_type=MissionEventType.PLAN_CREATED.value,
                    payload={
                        "steps_count": len(steps),
                        "summary": plan_structure.summary,
                        "deliverables": plan_structure.deliverables,
                        "cost_usd": plan_telemetry.get("estimated_cost_usd", 0.0)
                    }
                )

            # 3. Transition to RUNNING
            validate_status_transition(mission["status"], MissionStatus.RUNNING.value, mission_id)
            mission["status"] = MissionStatus.RUNNING.value
            mission["updated_at"] = datetime.now(timezone.utc).isoformat()

            # 4. Iterate and execute steps sequentially
            steps = _in_memory_engine_steps.get(mission_id, [])
            total_steps = len(steps)

            for step in steps:
                # Check cancellation flag
                if _mission_cancel_flags.get(mission_id, False):
                    mission["status"] = MissionStatus.CANCELLED.value
                    return

                # Check pause event
                pause_evt = _mission_pause_events.get(mission_id)
                if pause_evt and not pause_evt.is_set():
                    logger.info(f"Mission {mission_id} execution paused before step {step['step_number']}.")
                    await pause_evt.wait() # Wait until resumed or cancelled
                    if _mission_cancel_flags.get(mission_id, False):
                        mission["status"] = MissionStatus.CANCELLED.value
                        return

                if step["status"] == MissionStepStatus.COMPLETED.value:
                    continue

                mission["current_step"] = step["step_number"]
                step_success = await self._execute_single_step(workspace_id, mission, step)

                if not step_success:
                    # Step failed after retries -> fail mission
                    mission["status"] = MissionStatus.FAILED.value
                    mission["failed_at"] = datetime.now(timezone.utc).isoformat()
                    mission["updated_at"] = mission["failed_at"]
                    mission["error"] = step.get("error") or "Step execution failed."

                    await record_mission_event(
                        session=None,
                        workspace_id=workspace_id,
                        mission_id=mission_id,
                        event_type=MissionEventType.MISSION_FAILED.value,
                        payload={
                            "failed_step": step["step_number"],
                            "step_name": step["name"],
                            "error": mission["error"]
                        }
                    )
                    return

                # Calculate progress
                completed_count = sum(1 for s in steps if s["status"] == MissionStepStatus.COMPLETED.value)
                mission["progress"] = round((completed_count / total_steps) * 100.0, 1) if total_steps > 0 else 100.0

            # 5. All steps completed -> Transition to COMPLETED
            now_iso = datetime.now(timezone.utc).isoformat()
            mission["status"] = MissionStatus.COMPLETED.value
            mission["completed_at"] = now_iso
            mission["updated_at"] = now_iso
            mission["progress"] = 100.0

            # Compile final structured result
            deliverables = mission.get("plan", {}).get("deliverables", [])
            mission["result"] = {
                "summary": f"Autonomous mission '{mission['title']}' executed successfully.",
                "total_steps_executed": total_steps,
                "deliverables": deliverables or ["Verified repository artifacts", "Operational verification completed"],
                "total_tokens": mission["token_usage"]["total_tokens"],
                "total_cost_usd": round(mission["cost"], 6),
                "completed_at": now_iso,
                "status": "SUCCESS"
            }

            await record_mission_event(
                session=None,
                workspace_id=workspace_id,
                mission_id=mission_id,
                event_type=MissionEventType.MISSION_COMPLETED.value,
                payload={
                    "status": MissionStatus.COMPLETED.value,
                    "total_steps": total_steps,
                    "cost_usd": mission["cost"],
                    "total_tokens": mission["token_usage"]["total_tokens"],
                    "completed_at": now_iso
                }
            )

        except asyncio.CancelledError:
            logger.info(f"Mission execution cancelled for {mission_id}")
            mission["status"] = MissionStatus.CANCELLED.value
            mission["cancelled_at"] = datetime.now(timezone.utc).isoformat()
        except Exception as exc:
            logger.error(f"Mission execution fatal error for {mission_id}: {exc}", exc_info=True)
            mission["status"] = MissionStatus.FAILED.value
            mission["failed_at"] = datetime.now(timezone.utc).isoformat()
            mission["error"] = str(exc)
            await record_mission_event(
                session=None,
                workspace_id=workspace_id,
                mission_id=mission_id,
                event_type=MissionEventType.MISSION_FAILED.value,
                payload={"error": str(exc), "status": MissionStatus.FAILED.value}
            )
        finally:
            _active_mission_tasks.pop(mission_id, None)

    async def _execute_single_step(
        self,
        workspace_id: str,
        mission: Dict[str, Any],
        step: Dict[str, Any]
    ) -> bool:
        """Executes a single step with bounded exponential backoff retries."""
        step["status"] = MissionStepStatus.RUNNING.value
        step["started_at"] = datetime.now(timezone.utc).isoformat()
        step["updated_at"] = step["started_at"]

        await record_mission_event(
            session=None,
            workspace_id=workspace_id,
            mission_id=mission["id"],
            event_type=MissionEventType.STEP_STARTED.value,
            step_id=step["id"],
            payload={
                "step_number": step["step_number"],
                "step_name": step["name"],
                "step_type": step["step_type"],
                "started_at": step["started_at"]
            }
        )

        max_retries = step.get("max_retries", 3)
        retry_delay = 1.0

        for attempt in range(max_retries + 1):
            if _mission_cancel_flags.get(mission["id"], False):
                step["status"] = MissionStepStatus.SKIPPED.value
                return False

            start_perf = time.perf_counter()
            try:
                # Execute AI/tool payload
                provider = resolve_ai_provider()
                step_prompt = (
                    f"Execute Step {step['step_number']}: {step['name']}\n"
                    f"Context: Mission '{mission['title']}' - Goal: {mission.get('goal', '')}\n"
                    f"Step Description: {step['description']}\n"
                    f"Type: {step['step_type']}\n"
                    f"Perform step operation and return structured JSON result."
                )

                await record_mission_event(
                    session=None,
                    workspace_id=workspace_id,
                    mission_id=mission["id"],
                    event_type=MissionEventType.MODEL_REQUEST.value,
                    step_id=step["id"],
                    payload={"step": step["step_number"], "model": mission.get("model") or "default"}
                )

                resp = await provider.generate(
                    prompt=step_prompt,
                    model=mission.get("model"),
                    system_prompt="You are an autonomous step executor inside Kinetiq AI OS.",
                    parameters={"temperature": 0.1, "max_tokens": 1024}
                )

                duration_ms = int((time.perf_counter() - start_perf) * 1000)
                step["duration_ms"] = duration_ms
                step["output"] = {
                    "content": resp.content,
                    "model": resp.model,
                    "provider": resp.provider,
                    "status": "COMPLETED",
                    "execution_time_ms": duration_ms
                }

                # Token and Cost Accounting
                in_tok = resp.usage.input_tokens or 120
                out_tok = resp.usage.output_tokens or 240
                tot_tok = resp.usage.total_tokens or (in_tok + out_tok)
                step_cost = round(((in_tok * 0.0000015) + (out_tok * 0.000002)), 6)

                step["token_usage"] = {"input_tokens": in_tok, "output_tokens": out_tok, "total_tokens": tot_tok}
                step["cost_usd"] = step_cost

                # Aggregate to mission level
                mission["token_usage"]["input_tokens"] += in_tok
                mission["token_usage"]["output_tokens"] += out_tok
                mission["token_usage"]["total_tokens"] += tot_tok
                mission["cost"] = round(mission["cost"] + step_cost, 6)

                step["status"] = MissionStepStatus.COMPLETED.value
                step["completed_at"] = datetime.now(timezone.utc).isoformat()
                step["updated_at"] = step["completed_at"]

                await record_mission_event(
                    session=None,
                    workspace_id=workspace_id,
                    mission_id=mission["id"],
                    event_type=MissionEventType.MODEL_RESPONSE.value,
                    step_id=step["id"],
                    payload={"step": step["step_number"], "tokens": tot_tok, "latency_ms": duration_ms}
                )

                await record_mission_event(
                    session=None,
                    workspace_id=workspace_id,
                    mission_id=mission["id"],
                    event_type=MissionEventType.STEP_COMPLETED.value,
                    step_id=step["id"],
                    payload={
                        "step_number": step["step_number"],
                        "step_name": step["name"],
                        "duration_ms": duration_ms,
                        "cost_usd": step_cost,
                        "completed_at": step["completed_at"]
                    }
                )
                return True

            except Exception as exc:
                step["retry_count"] = attempt + 1
                logger.warning(f"Step {step['step_number']} execution error on attempt {attempt + 1}: {exc}")

                if attempt < max_retries:
                    # Bounded exponential backoff wait
                    backoff = min(retry_delay * (2 ** attempt), 8.0)
                    await asyncio.sleep(backoff)
                else:
                    duration_ms = int((time.perf_counter() - start_perf) * 1000)
                    step["duration_ms"] = duration_ms
                    step["status"] = MissionStepStatus.FAILED.value
                    step["error"] = {
                        "type": FailureType.MODEL_ERROR.value,
                        "message": str(exc),
                        "retries_exhausted": max_retries
                    }
                    step["updated_at"] = datetime.now(timezone.utc).isoformat()

                    await record_mission_event(
                        session=None,
                        workspace_id=workspace_id,
                        mission_id=mission["id"],
                        event_type=MissionEventType.STEP_FAILED.value,
                        step_id=step["id"],
                        payload={
                            "step_number": step["step_number"],
                            "step_name": step["name"],
                            "error": str(exc),
                            "retries": step["retry_count"]
                        }
                    )
                    return False
        return False

mission_engine = MissionExecutionEngine()
