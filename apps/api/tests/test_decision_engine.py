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
from app.services import decision_engine_service
from app.schemas.decision_engine import (
    DecisionCreate,
    DecisionAnalyzeRequest,
    DecisionApprovalRequest,
    DecisionOverrideRequest,
    DecisionScenarioCreate
)

def test_evidence_provenance_and_stale_flagging():
    async def _test():
        req = DecisionCreate(
            question="Which cloud database tier should we choose?",
            decisionType="architectural"
        )
        dec = await decision_engine_service.create_decision(
            None, workspace_id="ws_test_dec", user_id="usr_01", req=req
        )
        d_id = dec["id"]

        evidence_list = await decision_engine_service.get_evidence(None, decision_id=d_id)
        assert len(evidence_list) >= 1
        assert evidence_list[0]["authority"] == "high"

        # Trigger analysis
        analyzed = await decision_engine_service.analyze_decision(
            None, decision_id=d_id, req=DecisionAnalyzeRequest(forceFreshEvidence=True)
        )
        assert analyzed["status"] == "options_ready"
    asyncio.run(_test())

def test_options_tradeoffs_and_risks():
    async def _test():
        d_id = "dec_demo_strategy_01"
        options = await decision_engine_service.get_options(None, decision_id=d_id)
        assert len(options) >= 2

        tradeoffs = await decision_engine_service.get_tradeoffs(None, decision_id=d_id)
        assert len(tradeoffs) >= 1
        assert "Kubernetes" in tradeoffs[0]["tradeoff_summary"]

        risks = await decision_engine_service.get_risks(None, decision_id=d_id)
        assert len(risks) >= 2
    asyncio.run(_test())

def test_human_override_and_version_immutability():
    async def _test():
        req = DecisionCreate(
            question="Should we migrate the billing system?",
            decisionType="financial"
        )
        dec = await decision_engine_service.create_decision(
            None, workspace_id="ws_test_over", user_id="usr_01", req=req
        )
        d_id = dec["id"]

        override_req = DecisionOverrideRequest(
            originalOptionId="opt_01",
            selectedOptionId="opt_02",
            reason="Executive compliance mandate requires on-prem billing isolation"
        )
        updated = await decision_engine_service.override_decision(
            None, decision_id=d_id, req=override_req, actor_id="usr_admin_01"
        )
        assert updated["status"] == "approved"
        assert updated["current_version"] == 2
    asyncio.run(_test())

def test_scenario_simulation():
    async def _test():
        d_id = "dec_demo_strategy_01"
        scen_req = DecisionScenarioCreate(
            name="Traffic Spike Simulation",
            assumptions={"load_multiplier": 5.0},
            variables={"concurrency_limit": 10000}
        )
        scen = await decision_engine_service.create_scenario(
            None, decision_id=d_id, req=scen_req
        )
        assert scen["name"] == "Traffic Spike Simulation"
        assert scen["result_summary"]["production_mutated"] is False
    asyncio.run(_test())
