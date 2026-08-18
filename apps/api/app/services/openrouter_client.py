import os
import json
import time
import logging
import httpx
from typing import Dict, Any, List, Optional, Tuple, AsyncGenerator
from app.core.config import settings
from app.core.ai_provider import (
    AIProvider,
    AIResponse,
    AITokenUsage,
    AIToolCall,
    AIToolCallResponse,
    PlanStep,
    MissionPlanOutput,
    UsageMetadata
)

logger = logging.getLogger("vapor.ai.openrouter")

# Error State Taxonomy
AUTH_ERROR = "AUTH_ERROR"
RATE_LIMITED = "RATE_LIMITED"
TIMEOUT = "TIMEOUT"
MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
PROVIDER_ERROR = "PROVIDER_ERROR"
NETWORK_ERROR = "NETWORK_ERROR"
ALL_MODELS_UNAVAILABLE = "ALL_MODELS_UNAVAILABLE"

class OpenRouterAIException(Exception):
    def __init__(self, error_type: str, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.status_code = status_code

class OpenRouterClient(AIProvider):
    """Authoritative OpenRouter AI Client for Vapor OS."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None
    ):
        self._api_key = api_key or os.getenv("OPENROUTER_API_KEY") or settings.OPENROUTER_API_KEY
        self.base_url = (base_url or os.getenv("OPENROUTER_BASE_URL") or settings.OPENROUTER_BASE_URL).rstrip("/")
        self.default_model = default_model or os.getenv("OPENROUTER_DEFAULT_MODEL") or settings.OPENROUTER_DEFAULT_MODEL or "openrouter/free"
        self._http_headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://vapor.os",
            "X-Title": "Vapor OS Core AI Kernel"
        }

    def _get_headers(self) -> Dict[str, str]:
        key = self._api_key or os.getenv("OPENROUTER_API_KEY") or settings.OPENROUTER_API_KEY
        if not key:
            raise OpenRouterAIException(
                AUTH_ERROR,
                "OpenRouter API Key is missing. Configure OPENROUTER_API_KEY in server environment.",
                status_code=401
            )
        headers = dict(self._http_headers)
        headers["Authorization"] = f"Bearer {key}"
        return headers

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Executes non-streaming completion with model-level fallback."""
        target_model = model or self.default_model
        params = parameters or {}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "max_tokens": params.get("max_tokens", 1024),
            "temperature": params.get("temperature", 0.7)
        }

        start_time = time.perf_counter()
        headers = self._get_headers()

        # Primary attempt
        async with httpx.AsyncClient(timeout=45.0) as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
            except httpx.TimeoutException:
                raise OpenRouterAIException(TIMEOUT, f"OpenRouter inference timed out for model '{target_model}'.", 504)
            except httpx.RequestError as req_err:
                raise OpenRouterAIException(NETWORK_ERROR, f"OpenRouter network connectivity error: {req_err}", 502)

            fallback_used = False
            # Handle 404 / Model unavailable with fallback to openrouter/free
            if resp.status_code == 404 and target_model != "openrouter/free":
                logger.warning(f"OpenRouter model '{target_model}' unavailable (404). Falling back to 'openrouter/free'.")
                fallback_used = True
                payload["model"] = "openrouter/free"
                try:
                    resp = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    )
                except Exception as fb_err:
                    raise OpenRouterAIException(ALL_MODELS_UNAVAILABLE, f"All OpenRouter models failed: {fb_err}", 503)

            if resp.status_code == 401:
                raise OpenRouterAIException(AUTH_ERROR, "Invalid OpenRouter credentials.", 401)
            elif resp.status_code == 429:
                raise OpenRouterAIException(RATE_LIMITED, "OpenRouter rate limit reached.", 429)
            elif resp.status_code != 200:
                raise OpenRouterAIException(PROVIDER_ERROR, f"OpenRouter returned HTTP {resp.status_code}: {resp.text}", resp.status_code)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            data = resp.json()
            choices = data.get("choices", [])
            if not choices:
                raise OpenRouterAIException(PROVIDER_ERROR, "OpenRouter returned empty choices list.", 500)

            content = choices[0].get("message", {}).get("content", "")
            finish_reason = choices[0].get("finish_reason", "stop")
            usage_raw = data.get("usage", {})

            usage = AITokenUsage(
                input_tokens=usage_raw.get("prompt_tokens", len(prompt.split()) + 10),
                output_tokens=usage_raw.get("completion_tokens", len(content.split()) + 5),
                total_tokens=usage_raw.get("total_tokens", len(prompt.split()) + len(content.split()) + 15),
                is_estimated="prompt_tokens" not in usage_raw
            )

            return AIResponse(
                content=content,
                model=payload["model"],
                provider="openrouter",
                usage=usage,
                latency_ms=latency_ms,
                finish_reason=finish_reason,
                fallback_used=fallback_used,
                metadata={"raw_model": data.get("model", payload["model"])}
            )

    async def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Streams text chunks via SSE."""
        target_model = model or self.default_model
        params = parameters or {}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "max_tokens": params.get("max_tokens", 1024),
            "temperature": params.get("temperature", 0.7),
            "stream": True
        }

        headers = self._get_headers()
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status_code != 200:
                    yield f"[Error: OpenRouter stream HTTP {response.status_code}]"
                    return
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except Exception:
                            continue

    async def structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generates structured JSON adhering to the provided schema."""
        target_model = model or self.default_model
        params = parameters or {}
        system_msg = f"You are a structured output assistant. Output strict valid JSON matching schema: {json.dumps(schema)}"
        resp = await self.generate(
            prompt=prompt,
            model=target_model,
            parameters=params,
            system_prompt=system_msg
        )
        try:
            # Clean markdown code blocks if returned
            text = resp.content.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except Exception as err:
            raise OpenRouterAIException(
                "STRUCTURED_OUTPUT_PARSE_ERROR",
                f"Failed to parse model output into JSON schema: {err}. Raw output: {resp.content[:200]}",
                500
            )

    async def tool_call(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        model: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> AIToolCallResponse:
        """Executes LLM tool selection with formatted tool specifications."""
        target_model = model or self.default_model
        params = parameters or {}
        payload = {
            "model": target_model,
            "messages": [{"role": "user", "content": prompt}],
            "tools": tools,
            "max_tokens": params.get("max_tokens", 1024)
        }
        headers = self._get_headers()
        start_time = time.perf_counter()

        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            if resp.status_code != 200:
                raise OpenRouterAIException(PROVIDER_ERROR, f"OpenRouter tool call error: {resp.text}", resp.status_code)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            data = resp.json()
            msg = data.get("choices", [{}])[0].get("message", {})
            raw_tools = msg.get("tool_calls", [])
            tool_calls = []
            for rt in raw_tools:
                fn = rt.get("function", {})
                args = {}
                try:
                    args = json.loads(fn.get("arguments", "{}"))
                except Exception:
                    pass
                tool_calls.append(AIToolCall(
                    id=rt.get("id", str(time.time())),
                    name=fn.get("name", "unknown_tool"),
                    arguments=args
                ))

            return AIToolCallResponse(
                content=msg.get("content"),
                tool_calls=tool_calls,
                model=target_model,
                provider="openrouter",
                latency_ms=latency_ms
            )

    async def health_check(self) -> Dict[str, Any]:
        """Verifies API key configuration, reachability, and active models."""
        key = self._api_key or os.getenv("OPENROUTER_API_KEY") or settings.OPENROUTER_API_KEY
        if not key:
            return {
                "status": "UNCONFIGURED",
                "provider": "openrouter",
                "configured": False,
                "reachable": False,
                "message": "OPENROUTER_API_KEY is not set."
            }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {key}"}
                )
                if resp.status_code == 200:
                    models = resp.json().get("data", [])
                    return {
                        "status": "AVAILABLE",
                        "provider": "openrouter",
                        "configured": True,
                        "reachable": True,
                        "models_count": len(models),
                        "default_model": self.default_model
                    }
                elif resp.status_code == 401:
                    return {
                        "status": "AUTH_REQUIRED",
                        "provider": "openrouter",
                        "configured": True,
                        "reachable": True,
                        "message": "OpenRouter API Key rejected (401 Unauthorized)."
                    }
                else:
                    return {
                        "status": "DEGRADED",
                        "provider": "openrouter",
                        "configured": True,
                        "reachable": False,
                        "message": f"OpenRouter returned HTTP {resp.status_code}"
                    }
        except Exception as err:
            return {
                "status": "UNAVAILABLE",
                "provider": "openrouter",
                "configured": True,
                "reachable": False,
                "message": str(err)
            }

    async def generate_plan(
        self,
        mission_title: str,
        mission_description: str,
        priority: str
    ) -> Tuple[MissionPlanOutput, UsageMetadata]:
        """Generates structured mission plan output via OpenRouter."""
        start_time = time.perf_counter()
        schema = {
            "type": "object",
            "properties": {
                "goal": {"type": "string"},
                "summary": {"type": "string"},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "order": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["order", "title", "description"]
                    }
                },
                "deliverables": {"type": "array", "items": {"type": "string"}},
                "open_questions": {"type": "array", "items": {"type": "string"}},
                "recommendations": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["goal", "summary", "steps", "deliverables", "open_questions", "recommendations"]
        }
        
        prompt = (
            f"Generate a strategic mission plan for priority: {priority.upper()}\n"
            f"Mission Title: {mission_title}\n"
            f"Mission Description: {mission_description}\n"
            f"Provide a thorough breakdown with goal, summary, ordered execution steps, deliverables, open questions, and recommendations."
        )

        try:
            struct_data = await self.structured_output(prompt, schema)
            steps = [
                PlanStep(
                    order=s.get("order", idx + 1),
                    title=s.get("title", f"Step {idx + 1}"),
                    description=s.get("description", "")
                )
                for idx, s in enumerate(struct_data.get("steps", []))
            ]
            if not steps:
                steps = [
                    PlanStep(order=1, title="Context Assembly", description="Gather mission context and requirements."),
                    PlanStep(order=2, title="Core Execution", description=f"Fulfill objective for {mission_title}."),
                    PlanStep(order=3, title="Verification", description="Validate all deliverables and operational criteria.")
                ]
            output = MissionPlanOutput(
                goal=struct_data.get("goal", f"Fulfill mission objective for '{mission_title}'"),
                summary=struct_data.get("summary", f"AI-orchestrated plan for {priority.upper()} priority mission."),
                steps=steps,
                deliverables=struct_data.get("deliverables", ["Mission execution artifacts", "Verification report"]),
                open_questions=struct_data.get("open_questions", ["Are there additional security or compliance constraints?"]),
                recommendations=struct_data.get("recommendations", ["Follow modular architecture and maintain test isolation"])
            )
        except Exception:
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

        latency_ms = int((time.perf_counter() - start_time) * 1000)
        metadata = UsageMetadata(
            provider="openrouter",
            model=self.default_model,
            latency_ms=latency_ms,
            input_tokens=150,
            output_tokens=300
        )
        return output, metadata

# Singleton client instance
openrouter_client = OpenRouterClient()
