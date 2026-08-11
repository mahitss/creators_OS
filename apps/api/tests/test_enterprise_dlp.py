import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import dlp_service

client = TestClient(app)

def test_pattern_detection_and_redaction():
    # 1. API Key Detection
    sample_text = "Here is my secret API key: vpr_live_secret_key_891429814"
    findings = dlp_service.detect_sensitive_patterns(sample_text)
    assert len(findings) >= 1
    assert findings[0]["detector"] == "api_key"
    assert findings[0]["classification"] == "secret"

    # 2. Secret Redaction (never stores secret value)
    redacted, count = dlp_service.redact_sensitive_content(sample_text)
    assert count >= 1
    assert "vpr_live_secret_key_891429814" not in redacted
    assert "[REDACTED_SECRET]" in redacted

def test_model_input_gate_and_boundary_enforcement():
    async def _test():
        ws_id = "ws_dlp_test"
        org_id = "org_dlp_test"

        # 1. Secret in prompt context -> REDACTED before external model call
        secret_prompt = "Contact user john@company.com with key sk_live_secret_key_99999"
        clean_text, action, dec = await dlp_service.evaluate_model_input(
            None, ws_id, org_id, "openai", "gpt-4o", secret_prompt
        )
        assert action == "REDACTED"
        assert "[REDACTED_SECRET]" in clean_text
        assert "sk_live_secret_key_99999" not in clean_text

        # 2. Restricted classification sent to unapproved model -> BLOCKED
        res_text, action_block, dec_block = await dlp_service.evaluate_model_input(
            None, ws_id, org_id, "unapproved_provider", "random-model", "Restricted document", classification="restricted"
        )
        assert action_block == "BLOCKED"

    asyncio.run(_test())

def test_memory_gate_secret_prevention():
    async def _test():
        ws_id = "ws_mem_test"

        # 1. Attempt to store secret in memory -> DENIED
        secret_mem = "User password is super_secret_pass_123 with key sk_test_12345678901234567890"
        allowed, msg = await dlp_service.evaluate_memory_gate(None, ws_id, secret_mem, operation="write")
        assert allowed is False
        assert "Memory Write Denied" in msg

        # 2. Safe memory write -> ALLOWED
        safe_mem = "Weekly market research summary for executive review."
        safe_allowed, safe_msg = await dlp_service.evaluate_memory_gate(None, ws_id, safe_mem, operation="write")
        assert safe_allowed is True
        assert safe_msg == "ALLOWED"

    asyncio.run(_test())

def test_lineage_tracing_and_quarantine():
    async def _test():
        ws_id = "ws_lineage_test"

        # 1. Lineage DAG Tracing
        lin_res = await dlp_service.record_lineage(
            None, "msg_104", "gmail_source", "doc_summary", "drive_destination", "context_retrieval"
        )
        assert lin_res["edge_id"] is not None

        # 2. Quarantine Asset
        q_res = await dlp_service.quarantine_asset(
            None, ws_id, "workflow_run", "run_9912", "Suspicious external transfer of confidential document", "usr_sec_01"
        )
        assert q_res["status"] == "quarantined"

    asyncio.run(_test())

def test_data_security_rest_api():
    # 1. Data Assets API
    assets_res = client.get("/api/v1/admin/data/assets?workspaceId=ws_default_creator")
    assert assets_res.status_code == 200
    assert len(assets_res.json()) >= 2

    # 2. Sensitive Findings API
    findings_res = client.get("/api/v1/admin/data/findings?workspaceId=ws_default_creator")
    assert findings_res.status_code == 200

    # 3. DLP Policies API
    policies_res = client.get("/api/v1/admin/data/policies?organizationId=org_default_creator")
    assert policies_res.status_code == 200

    # 4. Data Lineage API
    lineage_res = client.get("/api/v1/admin/data/lineage?workspaceId=ws_default_creator")
    assert lineage_res.status_code == 200
    assert "nodes" in lineage_res.json()

    # 5. Policy Simulation API
    sim_res = client.post("/api/v1/admin/data/policies/simulate", json={
        "organizationId": "org_default_creator",
        "contentSample": "Secret API Key: vpr_live_secret_key_89142",
        "destination": "external_model"
    })
    assert sim_res.status_code == 200
    assert sim_res.json()["action"] == "REDACTED"
