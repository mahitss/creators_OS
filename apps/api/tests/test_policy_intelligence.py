import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
api_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import policy_intelligence_service, policy_engine
from app.schemas.policy_intelligence import (
    PolicyCreate,
    PolicyEvaluateRequest,
    BreakGlassGrantCreate
)
from app.services.policy_engine import PolicyContext

def test_allow_request():
    async def _test():
        req = PolicyEvaluateRequest(
            actorId="usr_member_01",
            action="read",
            resourceId="doc_public_01",
            resourceType="document"
        )
        res = await policy_intelligence_service.evaluate_request(None, req=req)
        assert res["decision"] == "allow"
    asyncio.run(_test())

def test_deny_and_precedence_conflict():
    async def _test():
        req = PolicyEvaluateRequest(
            actorId="usr_member_01",
            action="export",
            resourceId="db_customer_data",
            resourceType="database"
        )
        res = await policy_intelligence_service.evaluate_request(None, req=req)
        assert res["decision"] == "deny"
        assert "Explicit DENY" in res["reason"]
    asyncio.run(_test())

def test_approval_required():
    async def _test():
        req = PolicyEvaluateRequest(
            actorId="usr_member_01",
            action="write",
            resourceId="tool_email_sender",
            resourceType="tool"
        )
        res = await policy_intelligence_service.evaluate_request(None, req=req)
        assert res["decision"] == "approval_required"
        assert len(res["controls"]) >= 1
    asyncio.run(_test())

def test_breakglass_emergency_grant():
    async def _test():
        bg_req = BreakGlassGrantCreate(
            actorId="usr_emergency_01",
            reason="P0 Outage Remediation",
            durationMinutes=30
        )
        bg = await policy_intelligence_service.create_breakglass_grant(None, req=bg_req, authorized_by="usr_admin_01")
        assert bg["status"] == "active"

        # Evaluate request for actor with breakglass active
        req = PolicyEvaluateRequest(
            actorId="usr_emergency_01",
            action="execute",
            resourceId="tool_db_repair",
            resourceType="tool"
        )
        res = await policy_intelligence_service.evaluate_request(None, req=req)
        assert res["decision"] == "allow"
        assert "Emergency Break-Glass Grant active" in res["reason"]
    asyncio.run(_test())

def test_legacy_policy_engine_wrapper():
    async def _test():
        ctx = PolicyContext(
            workspace_id="ws_default_01",
            user_id="usr_member_01",
            tool_name="get_weather",
            risk_level="READ"
        )
        p_dec = await policy_engine.evaluate_policy(None, ctx)
        assert p_dec.decision == "ALLOW"
    asyncio.run(_test())
