import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.secops_service import SecOpsService

def test_secops_dashboard():
    async def _test():
        dash = await SecOpsService.get_operations_dashboard(None)
        assert dash is not None
        assert "activeIncidentsCount" in dash
        assert "criticalThreatsCount" in dash
        assert "activeResponsePlansCount" in dash

    asyncio.run(_test())

def test_response_plan_generation_and_simulation():
    async def _test():
        payload = {
            "riskLevel": "high",
            "actions": [
                {
                    "actionType": "quarantine",
                    "targetType": "agent",
                    "targetId": "agent_analyst_01",
                    "scope": "workspace",
                    "reason": "Test high risk response"
                }
            ]
        }
        plan = await SecOpsService.generate_response_plan(None, "inc_demo_01", payload)
        assert plan["id"] is not None
        assert plan["status"] == "draft"

        # Simulate plan
        sim = await SecOpsService.simulate_response_plan(None, plan["id"])
        assert sim["simulation_result"] == "SUCCESS"
        assert sim["production_impact"] == "NONE (Dry Run)"

    asyncio.run(_test())

def test_response_plan_approval_and_execution():
    async def _test():
        payload = {
            "riskLevel": "critical",
            "actions": [
                {
                    "actionType": "quarantine",
                    "targetType": "agent",
                    "targetId": "agent_test_exec_01",
                    "scope": "workspace",
                    "reason": "Controlled containment test"
                }
            ]
        }
        plan = await SecOpsService.generate_response_plan(None, "inc_demo_01", payload)
        
        # Approve plan
        app = await SecOpsService.approve_response_plan(None, plan["id"], "sec_admin_01")
        assert app["status"] == "approved"

        # Execute plan
        exec_res = await SecOpsService.execute_response_plan(None, plan["id"])
        assert exec_res["status"] == "completed"

    asyncio.run(_test())

def test_recovery_and_closure():
    async def _test():
        rec = await SecOpsService.verify_recovery(None, "inc_demo_01")
        assert rec["status"] == "recovering"
        assert rec["verification_result"] == "PASS"

        cls = await SecOpsService.close_incident_secops(None, "inc_demo_01")
        assert cls["status"] == "closed"

    asyncio.run(_test())

def test_detection_rule_shadow_mode():
    async def _test():
        rule_data = {
            "name": "Test Detection Shadow Rule",
            "description": "Shadow rule for testing",
            "conditionsJson": {"event_type": "tool_abuse"},
            "severity": "medium",
            "scope": "global"
        }
        rule = await SecOpsService.create_detection_rule(None, rule_data)
        assert rule["id"] is not None
        assert rule["status"] == "shadow"

        # Activate rule
        act = await SecOpsService.activate_detection_rule(None, rule["id"])
        assert act["status"] == "active"

    asyncio.run(_test())

def test_security_automations_and_runbooks():
    async def _test():
        auto_data = {
            "name": "Auto Pause Agent",
            "triggerEventType": "privilege_escalation",
            "responseActionType": "pause_agent",
            "maxActions": 3,
            "cooldownSeconds": 120,
            "approvalRequired": True
        }
        auto = await SecOpsService.create_automation_rule(None, auto_data)
        assert auto["id"] is not None
        assert auto["status"] == "active"

        rb_data = {
            "name": "Test SecOps Runbook",
            "triggerCondition": "event_type == 'privilege_escalation'",
            "investigationStepsJson": ["Step 1", "Step 2"],
            "approvedResponsesJson": ["pause_agent"],
            "verificationStepsJson": ["Verify pause"]
        }
        rb = await SecOpsService.create_runbook(None, rb_data)
        assert rb["id"] is not None
        assert rb["status"] == "active"

    asyncio.run(_test())
