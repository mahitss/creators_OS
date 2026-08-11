import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.governance import LegalHoldCreate, PolicySimulationCreate
from app.services import governance_service

client = TestClient(app)

def test_immutable_audit_logging_and_search():
    async def _test():
        org_id = "org_audit_test"
        evt = await governance_service.record_audit_event(
            None, org_id, "usr_admin_01", "role_change", "member", "usr_member_02", result="SUCCESS"
        )
        assert evt["organization_id"] == org_id
        assert evt["action"] == "role_change"

        logs = await governance_service.get_audit_events(None, org_id, actor_id="usr_admin_01")
        assert len(logs) >= 1
        assert logs[0]["action"] == "role_change"

    asyncio.run(_test())

def test_iam_privilege_escalation_protection_and_offboarding():
    async def _test():
        org_id = "org_iam_test"

        # 1. Member attempts to elevate self to admin -> DENIED
        mem, err = await governance_service.update_member_role(
            None, org_id, actor_id="usr_member_99", actor_role="member", target_user_id="usr_member_99", new_role="admin"
        )
        assert mem == {}
        assert "Privilege Escalation Denied" in err

        # 2. Admin elevates member to admin -> ALLOWED
        mem2, err2 = await governance_service.update_member_role(
            None, org_id, actor_id="usr_admin_01", actor_role="admin", target_user_id="usr_member_05", new_role="security_admin"
        )
        assert err2 is None
        assert mem2["role"] == "security_admin"

        # 3. Offboard user
        off_res = await governance_service.offboard_user(None, org_id, "usr_admin_01", "usr_member_05")
        assert off_res["status"] == "offboarded"
        assert off_res["sessions_revoked"] is True

    asyncio.run(_test())

def test_legal_hold_retention_suspension():
    async def _test():
        org_id = "org_legal_hold_test"

        # 1. Active Legal Hold suspends retention cleanup
        hold_in = LegalHoldCreate(organizationId=org_id, resourceType="audit", reason="Pending Litigation #1042")
        hold = await governance_service.add_legal_hold(None, hold_in, "usr_sec_01")
        assert hold["id"] is not None

        ret_res = await governance_service.enforce_retention_policy(None, org_id, "audit")
        assert ret_res["status"] == "SUSPENDED"
        assert "suspended due to active LegalHold" in ret_res["reason"]

    asyncio.run(_test())

def test_policy_simulation_and_compliance_evidence():
    async def _test():
        org_id = "org_sim_test"

        # 1. Policy Simulation (previews impact without production state mutation)
        sim_in = PolicySimulationCreate(
            organizationId=org_id,
            policyDefinition={"rule": "deny_external_email", "target": "gmail"}
        )
        sim = await governance_service.simulate_policy_change(None, sim_in, "usr_sec_01")
        assert len(sim["affected_workflows"]) >= 1
        assert len(sim["affected_agents"]) >= 1

        # 2. Compliance Controls & Readiness
        controls = await governance_service.get_compliance_controls(None, org_id)
        assert len(controls) >= 3
        frameworks = [c["framework"] for c in controls]
        assert "SOC_2" in frameworks
        assert "ISO_27001" in frameworks
        assert "GDPR" in frameworks

    asyncio.run(_test())

def test_governance_rest_api():
    # 1. Overview API
    res = client.get("/api/v1/admin/overview?organizationId=org_default_creator")
    assert res.status_code == 200
    assert "compliance_readiness_pct" in res.json()

    # 2. Audit API
    audit_res = client.get("/api/v1/admin/audit?organizationId=org_default_creator")
    assert audit_res.status_code == 200

    # 3. Compliance Controls API
    ctrl_res = client.get("/api/v1/admin/compliance/controls?organizationId=org_default_creator")
    assert ctrl_res.status_code == 200
    assert len(ctrl_res.json()) >= 3

    # 4. Security Findings API
    sec_res = client.get("/api/v1/admin/security/findings?organizationId=org_default_creator")
    assert sec_res.status_code == 200
