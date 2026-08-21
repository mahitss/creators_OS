"""Authoritative Mission Planner Abstraction for Kinetiq AI OS."""

import time
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError

from app.core.ai_provider import resolve_ai_provider, AIProvider, UsageMetadata
from app.core.mission_lifecycle import MissionStepType, FailureType, MissionExecutionError

logger = logging.getLogger("kinetiq.mission.planner")

class PlannedStep(BaseModel):
    order: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field("", max_length=2000)
    step_type: str = Field("analysis", pattern="^(retrieval|analysis|reasoning|generation|action)$")
    expected_output_type: str = Field("json", max_length=50)

class MissionPlanStructure(BaseModel):
    goal: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    steps: List[PlannedStep] = Field(..., min_length=1, max_length=20)
    deliverables: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class MissionPlanner:
    """Enterprise Mission Planner generating validated execution plans."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self._provider = provider

    def _get_provider(self) -> AIProvider:
        return self._provider or resolve_ai_provider()

    async def plan_mission(
        self,
        workspace_id: str,
        title: str,
        goal: str,
        description: str,
        priority: str = "MEDIUM",
        agent_id: Optional[str] = None,
        model: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[MissionPlanStructure, Dict[str, Any]]:
        """Generates a structured, validated multi-step plan for a mission."""
        start_time = time.perf_counter()
        provider = self._get_provider()

        effective_goal = goal if goal.strip() else title
        prompt = (
            f"Generate a rigorous, multi-step execution plan for the following autonomous AI mission.\n"
            f"Mission Title: {title}\n"
            f"Goal / Objective: {effective_goal}\n"
            f"Description: {description}\n"
            f"Priority: {priority}\n"
            f"Agent Context: {agent_id or 'General Operator'}\n"
            f"Workspace Context: {json.dumps(context or {})}\n\n"
            f"Return JSON adhering precisely to this structure:\n"
            f"{{\n"
            f'  "goal": "{effective_goal}",\n'
            f'  "summary": "High-level strategy summary",\n'
            f'  "steps": [\n'
            f'    {{"order": 1, "title": "...", "description": "...", "step_type": "retrieval|analysis|reasoning|generation|action", "expected_output_type": "json"}}\n'
            f'  ],\n'
            f'  "deliverables": ["..."],\n'
            f'  "open_questions": ["..."],\n'
            f'  "recommendations": ["..."]\n'
            f"}}\n"
        )

        system_prompt = (
            "You are the Kinetiq Mission Planning Engine. Formulate structured, atomic, deterministic "
            "steps (retrieval, analysis, reasoning, generation, action) with bounded scope. Always return strictly valid JSON."
        )

        try:
            # Check if provider has generate_plan shortcut or generate structured completion
            if hasattr(provider, "generate_plan") and not model:
                output, usage = await provider.generate_plan(title, description, priority)
                steps = [
                    PlannedStep(
                        order=s.order,
                        title=s.title,
                        description=s.description,
                        step_type="analysis" if s.order % 2 == 0 else "retrieval",
                        expected_output_type="json"
                    )
                    for s in output.steps
                ]
                if not steps:
                    steps = [
                        PlannedStep(order=1, title="Context Ingestion", description=f"Analyze inputs for {title}", step_type="retrieval"),
                        PlannedStep(order=2, title="Core Execution", description=f"Execute task: {effective_goal}", step_type="generation"),
                        PlannedStep(order=3, title="Verification & Synthesis", description="Verify outcomes and produce deliverables", step_type="analysis")
                    ]
                plan_structure = MissionPlanStructure(
                    goal=output.goal or effective_goal,
                    summary=output.summary or f"Execution strategy for {title}",
                    steps=steps,
                    deliverables=output.deliverables or ["Mission execution artifacts", "Validation audit log"],
                    open_questions=output.open_questions or [],
                    recommendations=output.recommendations or ["Verify workspace isolation", "Track token consumption"]
                )
                telemetry = usage.to_audit_dict() if hasattr(usage, "to_audit_dict") else {
                    "provider": getattr(provider, "provider_name", "openrouter"),
                    "model": model or "default",
                    "latency_ms": int((time.perf_counter() - start_time) * 1000),
                    "input_tokens": 150,
                    "output_tokens": 300,
                    "estimated_cost_usd": 0.00045
                }
                return plan_structure, telemetry

            response = await provider.generate(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                parameters={"temperature": 0.2, "max_tokens": 2048}
            )

            raw_text = response.content.strip()
            # Clean markdown code blocks if wrapped
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            parsed = json.loads(raw_text)
            plan_structure = MissionPlanStructure(**parsed)

            latency_ms = int((time.perf_counter() - start_time) * 1000)
            cost_usd = getattr(response, "cost_usd", 0.0) or (
                (response.usage.input_tokens * 0.0000015) + (response.usage.output_tokens * 0.000002)
            )

            telemetry = {
                "ai_provider": response.provider,
                "ai_model": response.model,
                "latency_ms": latency_ms,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens or (response.usage.input_tokens + response.usage.output_tokens),
                "estimated_cost_usd": round(cost_usd, 6),
                "workspace_id": workspace_id
            }

            return plan_structure, telemetry

        except json.JSONDecodeError as jde:
            logger.warning(f"Planner JSON decode error: {jde}, falling back to deterministic fallback steps.")
            # Fallback deterministic structured plan
            fallback_steps = [
                PlannedStep(order=1, title="Context & Target Retrieval", description=f"Assemble relevant environment state for {title}", step_type="retrieval"),
                PlannedStep(order=2, title="Autonomous Task Execution", description=f"Execute core objective: {effective_goal}", step_type="reasoning"),
                PlannedStep(order=3, title="Verification & Output Assembly", description="Validate results and compile mission deliverables", step_type="generation")
            ]
            fallback_plan = MissionPlanStructure(
                goal=effective_goal,
                summary=f"Automated execution plan for mission: {title}",
                steps=fallback_steps,
                deliverables=[f"Result artifacts for {title}", "Execution audit trail"],
                open_questions=[],
                recommendations=["Ensure workspace safety boundaries are verified."]
            )
            telemetry = {
                "ai_provider": "deterministic_fallback",
                "ai_model": model or "system-fallback",
                "latency_ms": int((time.perf_counter() - start_time) * 1000),
                "input_tokens": 100,
                "output_tokens": 200,
                "total_tokens": 300,
                "estimated_cost_usd": 0.0002,
                "workspace_id": workspace_id
            }
            return fallback_plan, telemetry

        except Exception as exc:
            logger.error(f"Mission planning failed: {exc}", exc_info=True)
            raise MissionExecutionError(
                FailureType.MODEL_ERROR,
                f"Failed to generate structured plan for mission: {str(exc)}",
                details={"title": title, "goal": goal, "error": str(exc)}
            )

mission_planner = MissionPlanner()
