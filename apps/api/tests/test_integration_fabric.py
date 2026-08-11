import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import action_gateway_service, integration_fabric_service
from app.schemas.integration_fabric import ActionExecuteRequest, WebhookIngestRequest

client = TestClient(app)

def test_catalog_and_capabilities():
    async def _test():
        catalog = await integration_fabric_service.list_catalog(None)
        assert len(catalog) >= 3

        caps = await integration_fabric_service.list_capabilities(None, "google")
        assert len(caps) >= 1

        health = await integration_fabric_service.get_health_metrics(None, "conn_google_01")
        assert health["status"] == "healthy"

    asyncio.run(_test())

def test_ssrf_protection():
    # 1. Block Localhost
    safe, err = action_gateway_service.validate_ssrf_and_url("http://localhost:8000/internal")
    assert safe is False
    assert "SSRF Protection" in err

    # 2. Block 127.0.0.1
    safe, err = action_gateway_service.validate_ssrf_and_url("http://127.0.0.1/admin")
    assert safe is False

    # 3. Block Cloud Metadata IP 169.254.169.254
    safe, err = action_gateway_service.validate_ssrf_and_url("http://169.254.169.254/latest/meta-data")
    assert safe is False

    # 4. Allow Valid Public HTTPS
    safe, msg = action_gateway_service.validate_ssrf_and_url("https://api.github.com/repos")
    assert safe is True

def test_action_gateway_execution_and_idempotency():
    async def _test():
        # Simulation Execution
        req_sim = ActionExecuteRequest(
            capabilityId="gmail.search",
            connectionId="conn_google_01",
            inputData={"query": "urgent invoice"},
            simulateOnly=True
        )
        res_sim = await action_gateway_service.execute_action(None, req_sim)
        assert res_sim["status"] == "simulated"
        assert res_sim["result_reference"]["simulated"] is True

        # High-Risk Approval Required Execution
        req_high = ActionExecuteRequest(
            capabilityId="gmail.send",
            connectionId="conn_google_01",
            inputData={"recipient": "external@domain.com", "subject": "Contract"},
            idempotencyKey="idem_key_01"
        )
        res_high = await action_gateway_service.execute_action(None, req_high)
        assert res_high["status"] == "approval_required"

        # Idempotent Retry Returns Same Record
        res_idem = await action_gateway_service.execute_action(None, req_high)
        assert res_idem["id"] == res_high["id"]

    asyncio.run(_test())

def test_webhook_security_and_deduplication():
    async def _test():
        payload = {"event": "push", "ref": "refs/heads/main"}
        sig = integration_fabric_service.hmac.new("whsec_vapor_default".encode("utf-8"), str(payload).encode("utf-8"), integration_fabric_service.hashlib.sha256).hexdigest()

        wh_req = WebhookIngestRequest(
            eventId="evt_9901",
            eventType="push",
            payload=payload,
            signature=f"sha256={sig}",
            timestamp="2026-08-11T00:00:00Z"
        )

        # 1. Valid Signature & Processing
        res, code = await integration_fabric_service.handle_webhook(None, "github", wh_req)
        assert code == 200
        assert res["status"] == "processed"

        # 2. Replay Protection & Deduplication
        res_dup, code_dup = await integration_fabric_service.handle_webhook(None, "github", wh_req)
        assert code_dup == 200
        assert res_dup["status"] == "deduplicated"

        # 3. Invalid Signature Rejection
        wh_bad = WebhookIngestRequest(
            eventId="evt_9902",
            eventType="push",
            payload=payload,
            signature="sha256=invalid_signature",
            timestamp="2026-08-11T00:00:00Z"
        )
        res_bad, code_bad = await integration_fabric_service.handle_webhook(None, "github", wh_bad)
        assert code_bad == 401

    asyncio.run(_test())

def test_integration_fabric_rest_api():
    # 1. List Catalog API
    c_res = client.get("/api/v1/integrations/catalog")
    assert c_res.status_code == 200

    # 2. Capabilities API
    cap_res = client.get("/api/v1/integrations/google/capabilities")
    assert cap_res.status_code == 200

    # 3. Health API
    h_res = client.get("/api/v1/integrations/google/health")
    assert h_res.status_code == 200

    # 4. Action Gateway Execute API
    act_req = {
        "capabilityId": "gmail.search",
        "connectionId": "conn_google_01",
        "inputData": {"query": "test"},
        "simulateOnly": True
    }
    a_res = client.post("/api/v1/integrations/actions/execute", json=act_req)
    assert a_res.status_code == 200
    assert a_res.json()["status"] == "simulated"

    # 5. Action Gateway Actions List API
    acts_res = client.get("/api/v1/integrations/actions")
    assert acts_res.status_code == 200
