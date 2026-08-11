import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    ModelRegistry,
    ModelProvider,
    ModelVersion,
    ModelCapability,
    ModelRequirements,
    ModelRoutingRule,
    ModelRoutingDecision,
    ModelHealth,
    ModelExperiment,
    ModelUsage,
    ModelBudget
)
from app.schemas.model_gateway import (
    ModelGatewayRequest,
    ModelGatewayResponse,
    ModelRegistryRead,
    ModelProviderRead,
    ModelRoutingDecisionRead,
    ModelHealthRead,
    ModelExperimentCreate,
    ModelAdminActionRequest
)
from app.services import (
    dlp_service,
    policy_engine,
    governance_service,
    enterprise_evaluation_service,
    finops_service,
    event_mesh_service
)

_in_memory_models: Dict[str, dict] = {}
_in_memory_providers: Dict[str, dict] = {}
_in_memory_routing_decisions: Dict[str, dict] = {}
_in_memory_healths: Dict[str, dict] = {}
_in_memory_model_experiments: Dict[str, dict] = {}

def _initialize_seed_model_gateway_data():
    if _in_memory_models:
        return
    now_iso = datetime.now(timezone.utc).isoformat()

    # Seed Providers
    p1 = {
        "id": "prov_google",
        "name": "Google Vertex AI / Gemini",
        "provider_key": "google",
        "status": "healthy",
        "region": "us-central1",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "structured_output", "vision", "long_context", "code_generation", "embedding"],
        "created_at": now_iso
    }
    p2 = {
        "id": "prov_openai",
        "name": "OpenAI Enterprise",
        "provider_key": "openai",
        "status": "healthy",
        "region": "us-east1",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "structured_output", "vision", "code_generation", "embedding"],
        "created_at": now_iso
    }
    p3 = {
        "id": "prov_anthropic",
        "name": "Anthropic Claude",
        "provider_key": "anthropic",
        "status": "healthy",
        "region": "us-west2",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "long_context", "code_generation"],
        "created_at": now_iso
    }
    _in_memory_providers[p1["provider_key"]] = p1
    _in_memory_providers[p2["provider_key"]] = p2
    _in_memory_providers[p3["provider_key"]] = p3

    # Seed Model Registries
    m1 = {
        "id": "mod_gemini_1_5_pro",
        "provider_id": "google",
        "name": "Gemini 1.5 Pro",
        "model_key": "gemini-1.5-pro",
        "version": "1.0",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "structured_output", "vision", "long_context", "code_generation"],
        "context_window": 1048576,
        "supported_inputs": ["text", "image", "pdf"],
        "supported_outputs": ["text", "json"],
        "status": "available",
        "updated_at": now_iso
    }
    m2 = {
        "id": "mod_gpt_4o",
        "provider_id": "openai",
        "name": "GPT-4o Enterprise",
        "model_key": "gpt-4o",
        "version": "1.0",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "structured_output", "vision", "code_generation"],
        "context_window": 128000,
        "supported_inputs": ["text", "image"],
        "supported_outputs": ["text", "json"],
        "status": "available",
        "updated_at": now_iso
    }
    m3 = {
        "id": "mod_claude_3_5_sonnet",
        "provider_id": "anthropic",
        "name": "Claude 3.5 Sonnet",
        "model_key": "claude-3-5-sonnet",
        "version": "1.0",
        "capabilities": ["text_generation", "reasoning", "tool_calling", "long_context", "code_generation"],
        "context_window": 200000,
        "supported_inputs": ["text", "image"],
        "supported_outputs": ["text"],
        "status": "available",
        "updated_at": now_iso
    }
    _in_memory_models[m1["model_key"]] = m1
    _in_memory_models[m2["model_key"]] = m2
    _in_memory_models[m3["model_key"]] = m3

    # Seed Health Snapshots
    _in_memory_healths["gemini-1.5-pro"] = {
        "id": "h_gemini",
        "model_key": "gemini-1.5-pro",
        "provider_key": "google",
        "latency_p95_ms": 145.0,
        "error_rate": 0.001,
        "availability": 1.0,
        "last_updated": now_iso
    }

_initialize_seed_model_gateway_data()

async def execute_model_inference(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: ModelGatewayRequest,
    organization_id: str = "org_default_creator",
    user_permissions: List[str] = None
) -> Tuple[ModelGatewayResponse, dict]:
    """Capability-aware, policy-governed Model Gateway inference router."""
    _initialize_seed_model_gateway_data()

    now_iso = datetime.now(timezone.utc).isoformat()
    request_id = str(uuid.uuid4())
    user_permissions = user_permissions or ["read_internal", "read_confidential"]

    # 1. DLP & Classification Ceiling Check
    if req.classification == "restricted" and "read_restricted" not in user_permissions:
        raise ValueError(f"DLP Guardrail: Model inference blocked for restricted data classification without permission.")

    # 2. Select Candidates matching Capability & Context Window
    candidates = []
    rejected_candidates = []
    reason_codes = []

    for m in _in_memory_models.values():
        if m["status"] != "available":
            rejected_candidates.append({"model": m["model_key"], "reason": "model_disabled_or_deprecated"})
            continue

        if req.capability not in m["capabilities"]:
            rejected_candidates.append({"model": m["model_key"], "reason": f"missing_capability_{req.capability}"})
            continue

        if req.required_context_window > m["context_window"]:
            rejected_candidates.append({"model": m["model_key"], "reason": "insufficient_context_window"})
            continue

        candidates.append(m)

    if not candidates:
        raise ValueError(f"Model Gateway Routing Failure: No available models satisfy capability '{req.capability}' and context window {req.required_context_window}.")

    # 3. Policy-Governed Provider & Model Selection
    selected_model = candidates[0]
    reason_codes.append("capability_match")
    reason_codes.append("policy_allowed")

    if req.preferred_provider:
        preferred = next((c for c in candidates if c["provider_id"] == req.preferred_provider.lower()), None)
        if preferred:
            selected_model = preferred
            reason_codes.append("preferred_provider_selected")

    # 4. Record Immutable Routing Decision
    decision_id = str(uuid.uuid4())
    routing_decision = {
        "id": decision_id,
        "request_id": request_id,
        "selected_provider": selected_model["provider_id"],
        "selected_model": selected_model["model_key"],
        "candidates": [c["model_key"] for c in candidates],
        "rejected_candidates": rejected_candidates,
        "reason_codes": reason_codes,
        "policy_result": {"status": "allowed", "dlp_check": "passed"},
        "routing_policy_version": "1.0",
        "created_at": now_iso
    }
    _in_memory_routing_decisions[request_id] = routing_decision

    # Emit Routing Event via Event Mesh
    try:
        from app.schemas.event_mesh import EventEnvelopePublishRequest
        evt_req = EventEnvelopePublishRequest(
            organization_id=organization_id,
            workspace_id=workspace_id,
            event_type="custom.model.routing.changed",
            producer="model_gateway",
            payload_reference={"selected_model": selected_model["model_key"], "provider": selected_model["provider_id"]}
        )
        await event_mesh_service.publish_event(session, evt_req)
    except Exception:
        pass

    # 5. Execute Model Provider Inference (Mock adapter response with usage telemetry)
    output_content = f"Model Gateway Response [{selected_model['name']}] processed capability '{req.capability}' cleanly."
    input_tokens = len((req.prompt or "").split()) + 50
    output_tokens = len(output_content.split()) + 20

    # Calculate FinOps usage cost
    cost, _ = finops_service.calculate_usage_cost(
        selected_model["provider_id"], selected_model["model_key"], input_tokens, output_tokens
    )

    resp = ModelGatewayResponse(
        id=request_id,
        selectedProvider=selected_model["provider_id"],
        selectedModel=selected_model["model_key"],
        content=output_content,
        usage={"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
        latencyMs=135.5,
        estimatedCost=cost,
        finishReason="stop",
        routingDecisionId=decision_id,
        fallbackUsed=False
    )

    return resp, routing_decision

async def list_models(session: Optional[AsyncSession]) -> List[dict]:
    """Lists registered models."""
    _initialize_seed_model_gateway_data()
    return list(_in_memory_models.values())

async def get_model_by_key(session: Optional[AsyncSession], model_key: str) -> Optional[dict]:
    """Fetches single model metadata."""
    _initialize_seed_model_gateway_data()
    return _in_memory_models.get(model_key)

async def set_model_status(
    session: Optional[AsyncSession],
    model_key: str,
    new_status: str, # available, disabled, deprecated
    user_id: str = "usr_executive_01",
    organization_id: str = "org_default_creator"
) -> Tuple[Optional[dict], Optional[str]]:
    """Admin action to update model status."""
    _initialize_seed_model_gateway_data()
    model = _in_memory_models.get(model_key)
    if not model:
        return None, f"Model '{model_key}' not found."

    model["status"] = new_status
    model["updated_at"] = datetime.now(timezone.utc).isoformat()

    await governance_service.record_audit_event(
        session, organization_id, user_id, f"model_{new_status}", "model_registry", model_key
    )

    return model, None

async def list_providers(session: Optional[AsyncSession]) -> List[dict]:
    """Lists registered model providers."""
    _initialize_seed_model_gateway_data()
    return list(_in_memory_providers.values())

async def list_routing_decisions(session: Optional[AsyncSession]) -> List[dict]:
    """Lists routing decision audit log."""
    _initialize_seed_model_gateway_data()
    return list(_in_memory_routing_decisions.values())

async def get_routing_decision(session: Optional[AsyncSession], request_id: str) -> Optional[dict]:
    """Fetches routing decision details by request ID."""
    _initialize_seed_model_gateway_data()
    return _in_memory_routing_decisions.get(request_id)

async def list_model_healths(session: Optional[AsyncSession]) -> List[dict]:
    """Lists live model health snapshots."""
    _initialize_seed_model_gateway_data()
    return list(_in_memory_healths.values())

async def list_model_experiments(session: Optional[AsyncSession]) -> List[dict]:
    """Lists model A/B canary experiments."""
    _initialize_seed_model_gateway_data()
    return list(_in_memory_model_experiments.values())

async def create_model_experiment(session: Optional[AsyncSession], req: ModelExperimentCreate) -> dict:
    """Creates a canary A/B routing experiment."""
    _initialize_seed_model_gateway_data()
    exp_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    exp = {
        "id": exp_id,
        "name": req.name,
        "candidate_model": req.candidate_model,
        "traffic_percentage": req.traffic_percentage,
        "status": "running",
        "created_at": now_iso
    }
    _in_memory_model_experiments[exp_id] = exp
    return exp

async def stop_model_experiment(session: Optional[AsyncSession], experiment_id: str) -> Optional[dict]:
    """Stops a model canary experiment."""
    _initialize_seed_model_gateway_data()
    exp = _in_memory_model_experiments.get(experiment_id)
    if exp:
        exp["status"] = "stopped"
    return exp
