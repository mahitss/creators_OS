import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.portfolio_intelligence_service import PortfolioIntelligenceService

def test_portfolio_overview_telemetry():
    async def _test():
        ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
        assert ov is not None
        assert "programsCount" in ov
        assert "resourceConflictsCount" in ov
        assert "overlapsCount" in ov
        assert "variancesCount" in ov
        assert ov["portfolioHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_portfolio_in_draft_status():
    async def _test():
        p_data = {
            "name": "Q4 Cloud Modernization Portfolio",
            "description": "Consolidate multi-cloud workloads into enterprise agent mesh.",
            "owner": "usr_exec_01",
            "workspaceId": "ws_default"
        }
        portfolio = await PortfolioIntelligenceService.create_portfolio(None, p_data)
        assert portfolio["id"] is not None
        assert portfolio["status"] == "draft"

    asyncio.run(_test())

def test_resource_conflict_and_overlap_detection():
    async def _test():
        ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
        assert len(ov["conflicts"]) > 0
        c = ov["conflicts"][0]
        assert c["resource_type"] == "agent_capacity"
        assert len(c["competing_initiatives_json"]) >= 2

        assert len(ov["overlaps"]) > 0
        o = ov["overlaps"][0]
        assert o["overlap_type"] == "capability"

    asyncio.run(_test())

def test_recommendation_approval_gating_and_no_auto_capital_movement():
    async def _test():
        ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
        rec = ov["recommendations"][0]
        assert rec["approval_status"] == "pending"
        # Verify explicit reversibility ratings
        assert "reversibility" in rec
        for alt in rec["alternatives_json"]:
            assert "reversibility" in alt

    asyncio.run(_test())

def test_natural_language_portfolio_query_and_dlp():
    async def _test():
        # Valid portfolio query
        res = await PortfolioIntelligenceService.process_natural_language_portfolio_query(None, "Which initiatives compete for capacity?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Secret query -> blocked by DLP
        secret_q = "Which initiatives compete for capacity? sk_live_888877776666"
        blocked = await PortfolioIntelligenceService.process_natural_language_portfolio_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

    asyncio.run(_test())
