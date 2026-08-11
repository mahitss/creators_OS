import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import model_gateway_service
from app.schemas.model_gateway import ModelGatewayRequest, ModelExperimentCreate

def test_model_gateway_inference_execution():
    async def _test():
        req = ModelGatewayRequest(
            requestType="reasoning",
            capability="reasoning",
            prompt="Analyze revenue trends for Q3.",
            classification="internal",
            requiredContextWindow=16384
        )
        resp, decision = await model_gateway_service.execute_model_inference(
            None, workspace_id="ws_test_01", req=req, organization_id="org_test_01"
        )
        assert resp.selected_model in ["gemini-1.5-pro", "gpt-4o", "claude-3-5-sonnet"]
        assert resp.selected_provider in ["google", "openai", "anthropic"]
        assert resp.usage["total_tokens"] > 0
        assert resp.estimated_cost >= 0.0
        assert decision["policy_result"]["status"] == "allowed"
    asyncio.run(_test())

def test_capability_matching_and_rejection():
    async def _test():
        req = ModelGatewayRequest(
            requestType="reranking",
            capability="unsupported_exotic_capability",
            prompt="Rerank document vectors.",
            classification="internal",
            requiredContextWindow=2048
        )
        with pytest.raises(ValueError, match="No available models satisfy capability"):
            await model_gateway_service.execute_model_inference(
                None, workspace_id="ws_test_01", req=req, organization_id="org_test_01"
            )
    asyncio.run(_test())

def test_context_window_filtering():
    async def _test():
        req = ModelGatewayRequest(
            requestType="long_context",
            capability="long_context",
            prompt="Analyze massive 10 million token codebase.",
            classification="internal",
            requiredContextWindow=10000000
        )
        with pytest.raises(ValueError, match="No available models satisfy capability"):
            await model_gateway_service.execute_model_inference(
                None, workspace_id="ws_test_01", req=req, organization_id="org_test_01"
            )
    asyncio.run(_test())

def test_pre_inference_dlp_and_policy_gating():
    async def _test():
        req = ModelGatewayRequest(
            requestType="reasoning",
            capability="reasoning",
            prompt="Restricted security credentials payload.",
            classification="restricted",
            requiredContextWindow=4096
        )
        with pytest.raises(ValueError, match="DLP Guardrail"):
            await model_gateway_service.execute_model_inference(
                None,
                workspace_id="ws_test_01",
                req=req,
                organization_id="org_test_01",
                user_permissions=["read_internal"]
            )
    asyncio.run(_test())

def test_model_status_admin_actions():
    async def _test():
        models = await model_gateway_service.list_models(None)
        assert len(models) >= 3

        updated, err = await model_gateway_service.set_model_status(None, "gemini-1.5-pro", "disabled")
        assert err is None
        assert updated["status"] == "disabled"

        updated, err = await model_gateway_service.set_model_status(None, "gemini-1.5-pro", "available")
        assert err is None
        assert updated["status"] == "available"
    asyncio.run(_test())

def test_model_experiment_lifecycle():
    async def _test():
        exp_req = ModelExperimentCreate(
            name="Canary Test Gemini Flash vs Pro",
            candidateModel="gemini-1.5-flash",
            trafficPercentage=10.0
        )
        exp = await model_gateway_service.create_model_experiment(None, exp_req)
        assert exp["status"] == "running"
        assert exp["traffic_percentage"] == 10.0

        stopped = await model_gateway_service.stop_model_experiment(None, exp["id"])
        assert stopped["status"] == "stopped"
    asyncio.run(_test())
