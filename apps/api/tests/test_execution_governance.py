import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.execution_governance_service import ExecutionGovernanceService

def test_execution_overview_telemetry():
    async def _test():
        ov = await ExecutionGovernanceService.get_execution_overview(None)
        assert ov is not None
        assert "benefitsCount" in ov
        assert "achievedRatePct" in ov
        assert "milestonesCount" in ov
        assert "variancesCount" in ov
        assert ov["executionHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_benefit_in_planned_status():
    async def _test():
        b_data = {
            "name": "Customer Onboarding Time Reduction",
            "description": "Reduce partner onboarding timeline from 14 days to 4 hours.",
            "owner": "usr_exec_01",
            "benefitType": "operational",
            "baseline": 14.0,
            "target": 0.16,
            "unit": "days",
            "measurementMethod": "Audit timestamp log analysis"
        }
        benefit = await ExecutionGovernanceService.create_benefit(None, b_data)
        assert benefit["id"] is not None
        assert benefit["status"] == "planned"
        assert benefit["baseline"] == 14.0

    asyncio.run(_test())

def test_evidence_verification_and_variances():
    async def _test():
        ov = await ExecutionGovernanceService.get_execution_overview(None)
        assert len(ov["evidences"]) > 0
        ev = ov["evidences"][0]
        assert ev["verification_status"] == "verified"
        assert ev["confidence"] >= 90.0

        assert len(ov["variances"]) > 0
        v = ov["variances"][0]
        assert v["variance_type"] == "schedule"
        assert "timeline slip" in v["delta"]

    asyncio.run(_test())

def test_governance_gates_and_forecasts():
    async def _test():
        ov = await ExecutionGovernanceService.get_execution_overview(None)
        assert len(ov["gates"]) > 0
        gate = ov["gates"][0]
        assert gate["gate_type"] == "security"

        assert len(ov["forecasts"]) > 0
        fc = ov["forecasts"][0]
        assert fc["confidence_pct"] >= 80.0
        assert fc["upper_bound"] >= fc["lower_bound"]

    asyncio.run(_test())

def test_natural_language_execution_query_and_dlp():
    async def _test():
        # Valid execution query
        res = await ExecutionGovernanceService.process_natural_language_execution_query(None, "Which initiatives are actually delivering benefits?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Secret query -> blocked by DLP
        secret_q = "Which initiatives are delivering benefits? sk_live_777766665555"
        blocked = await ExecutionGovernanceService.process_natural_language_execution_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

    asyncio.run(_test())
