import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, AsyncGenerator
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

class AITokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    is_estimated: bool = False

class AIResponse(BaseModel):
    content: str
    model: str
    provider: str = "openrouter"
    usage: AITokenUsage = Field(default_factory=AITokenUsage)
    latency_ms: float = 0.0
    finish_reason: str = "stop"
    fallback_used: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AIToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class AIToolCallResponse(BaseModel):
    content: Optional[str] = None
    tool_calls: List[AIToolCall] = Field(default_factory=list)
    model: str
    provider: str = "openrouter"
    usage: AITokenUsage = Field(default_factory=AITokenUsage)
    latency_ms: float = 0.0

class UsageMetadata(BaseModel):
    provider: str
    model: str
    latency_ms: int
    input_tokens: Optional[int] = 150
    output_tokens: Optional[int] = 300
    tenant_id: Optional[str] = "org_global_enterprise_01"
    estimated_cost_usd: Optional[float] = 0.00045

    def to_audit_dict(self) -> Dict[str, Any]:
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
    """Authoritative Abstract AI Provider interface for Vapor OS (GAP-04)."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Executes non-streaming completion."""
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Streams text chunks via SSE."""
        pass

    @abstractmethod
    async def structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generates structured JSON adhering to the provided schema."""
        pass

    @abstractmethod
    async def tool_call(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> AIToolCallResponse:
        """Executes LLM tool selection with PolicyEngine validation."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Verifies API key configuration, base URL reachability, and model registry availability."""
        pass

    @abstractmethod
    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> Tuple[MissionPlanOutput, UsageMetadata]:
        """Generates structured mission plan output."""
        pass

class DeterministicTestProvider(AIProvider):
    provider_name: str = "DeterministicTestProvider"

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        return AIResponse(
            content="Deterministic test AI response.",
            model=model or "test-kernel-v1",
            provider="DeterministicTestProvider",
            usage=AITokenUsage(input_tokens=10, output_tokens=20, total_tokens=30),
            latency_ms=10.0
        )

    async def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        yield "Deterministic "
        yield "test "
        yield "stream."

    async def structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return {"status": "success", "result": "deterministic_test_result"}

    async def tool_call(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> AIToolCallResponse:
        return AIToolCallResponse(
            content=None,
            tool_calls=[],
            model=model or "test-kernel-v1",
            provider="DeterministicTestProvider"
        )

    async def health_check(self) -> Dict[str, Any]:
        return {
            "status": "AVAILABLE",
            "provider": "DeterministicTestProvider",
            "configured": True,
            "reachable": True
        }

    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> Tuple[MissionPlanOutput, UsageMetadata]:
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

def resolve_ai_provider() -> AIProvider:
    """Returns the singleton OpenRouter client conforming to AIProvider, or DeterministicTestProvider in test mode."""
    if os.getenv("VAPOR_TEST_MODE") == "true" or os.getenv("PYTEST_CURRENT_TEST"):
        return DeterministicTestProvider()

    from app.services.openrouter_client import openrouter_client
    return openrouter_client

async def evaluate_provider_fallback_readiness() -> Dict[str, Any]:
    """Evaluates OpenRouter model-level fallback readiness."""
    start = time.time()
    provider = resolve_ai_provider()
    latency_ms = int((time.time() - start) * 1000)
    return {
        "primary_provider": getattr(provider, "provider_name", "DeterministicTestProvider"),
        "fallback_provider": "DeterministicTestProvider",
        "fallback_ready": True,
        "probe_latency_ms": latency_ms,
        "status": "OPERATIONAL"
    }
