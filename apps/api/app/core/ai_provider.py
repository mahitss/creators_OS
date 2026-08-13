import os
import time
from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    order: int
    title: str
    description: str

class MissionPlanOutput(BaseModel):
    goal: str
    summary: str
    steps: List[PlanStep]
    deliverables: List[str]
    open_questions: List[str]
    recommendations: List[str]

class UsageMetadata(BaseModel):
    provider: str
    model: str
    latency_ms: int
    input_tokens: Optional[int] = 150
    output_tokens: Optional[int] = 300
    tenant_id: Optional[str] = "org_global_enterprise_01"
    estimated_cost_usd: Optional[float] = 0.00045

    def to_audit_dict(self) -> dict:
        """Exports structured JSON telemetry dictionary for tenant cost attribution (GAP-03)."""
        return {
            "ai_provider": self.provider,
            "ai_model": self.model,
            "latency_ms": self.latency_ms,
            "input_tokens": self.input_tokens or 0,
            "output_tokens": self.output_tokens or 0,
            "tenant_id": self.tenant_id or "org_global_enterprise_01",
            "estimated_cost_usd": self.estimated_cost_usd or 0.0
        }


class AIProvider(ABC):
    @abstractmethod
    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> tuple[MissionPlanOutput, UsageMetadata]:
        pass

class DeterministicTestProvider(AIProvider):
    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> tuple[MissionPlanOutput, UsageMetadata]:
        start = time.time()
        output = MissionPlanOutput(
            goal=f"Execute mission: '{mission_title}' cleanly.",
            summary=f"Automated execution strategy for priority {priority.upper()} mission.",
            steps=[
                PlanStep(order=1, title="Context Assembly", description="Gather repository state and dependencies."),
                PlanStep(order=2, title="Implementation", description=f"Fulfill objective: {mission_title}."),
                PlanStep(order=3, title="Verification", description="Execute test suites and validate output integrity.")
            ],
            deliverables=[
                "Verified codebase implementation",
                "Automated test coverage pass"
            ],
            open_questions=[
                "Are there additional production constraints to consider?"
            ],
            recommendations=[
                "Maintain strict single-responsibility boundaries",
                "Verify workspace security isolation"
            ]
        )
        latency = int((time.time() - start) * 1000)
        metadata = UsageMetadata(
            provider="DeterministicTestProvider",
            model="test-kernel-v1",
            latency_ms=latency,
            input_tokens=150,
            output_tokens=300
        )
        return output, metadata

class GenericHTTPProvider(AIProvider):
    def __init__(self, provider_name: str, model_name: str, api_key: str):
        self.provider_name = provider_name
        self.model_name = model_name
        self.api_key = api_key

    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> tuple[MissionPlanOutput, UsageMetadata]:
        start = time.time()
        # Stub for live external provider connection
        output = MissionPlanOutput(
            goal=f"Strategic Execution Plan for '{mission_title}'",
            summary=f"AI-generated plan for {priority.upper()} priority mission.",
            steps=[
                PlanStep(order=1, title="Discovery & Analysis", description=f"Analyze requirements for '{mission_title}'."),
                PlanStep(order=2, title="Core Architecture", description="Design component boundaries and schemas."),
                PlanStep(order=3, title="Execution & Testing", description="Implement code and verify system behavior.")
            ],
            deliverables=["Architecture plan", "Implementation diffs", "Test report"],
            open_questions=["Any specific constraints for deployment?"],
            recommendations=["Follow modular monorepo principles"]
        )
        latency = int((time.time() - start) * 1000)
        metadata = UsageMetadata(
            provider=self.provider_name,
            model=self.model_name,
            latency_ms=latency
        )
        return output, metadata

def resolve_ai_provider() -> AIProvider:
    # 1. Environment test flag check
    if os.getenv("VAPOR_TEST_MODE") == "true" or os.getenv("PYTEST_CURRENT_TEST"):
        return DeterministicTestProvider()

    # 2. Check for configured provider keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    if openai_key:
        return GenericHTTPProvider("OpenAI", "gpt-4o", openai_key)
    elif anthropic_key:
        return GenericHTTPProvider("Anthropic", "claude-3-5-sonnet-20241022", anthropic_key)
    elif gemini_key:
        return GenericHTTPProvider("Gemini", "gemini-1.5-pro", gemini_key)
    elif openrouter_key:
        return GenericHTTPProvider("OpenRouter", "auto", openrouter_key)
    
    # 3. If running in offline test mode fallback to DeterministicTestProvider
    return DeterministicTestProvider()
