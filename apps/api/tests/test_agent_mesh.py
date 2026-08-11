import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import agent_mesh_service
from app.schemas.agent_mesh import DelegationRequestCreate

client = TestClient(app)

def test_agent_discovery_and_capability_registration():
    async def _test():
        ws_id = "ws_mesh_test"

        # 1. Register Capability
        cap = await agent_mesh_service.register_agent_capability(
            None, "ag_research_01", "research", "Knowledge Discovery", "Retrieves indexed docs"
        )
        assert cap["type"] == "research"

        # 2. Discover Agents
        agents = await agent_mesh_service.discover_agents(None, ws_id, capability_type="research")
        assert len(agents) >= 1
        assert agents[0]["specialization"] == "Researcher"

    asyncio.run(_test())

def test_delegation_authority_and_cycle_detection():
    async def _test():
        # 1. Valid Delegation
        del_req = DelegationRequestCreate(
            parentAgentId="ag_planner_01",
            childAgentId="ag_research_01",
            missionId="msn_01",
            taskId="tsk_01",
            scope="read_only",
            requiredOutput="Research Report"
        )
        del_res, status = await agent_mesh_service.request_delegation(None, del_req)
        assert status == "ALLOWED"
        assert del_res["status"] == "approved"

        # 2. Cycle Detection A -> B -> C -> A
        cycle_chain = ["ag_planner_01", "ag_research_01", "ag_analyst_02"]
        cycle_req = DelegationRequestCreate(
            parentAgentId="ag_analyst_02",
            childAgentId="ag_planner_01",
            missionId="msn_01",
            taskId="tsk_02",
            scope="read_only",
            requiredOutput="Cyclic Delegation"
        )
        _, cycle_status = await agent_mesh_service.request_delegation(None, cycle_req, delegation_chain=cycle_chain)
        assert "Circular delegation loop detected" in cycle_status

        # 3. Max Depth Violation
        depth_chain = ["ag_1", "ag_2", "ag_3"]
        depth_req = DelegationRequestCreate(
            parentAgentId="ag_3",
            childAgentId="ag_4",
            missionId="msn_01",
            taskId="tsk_03",
            scope="read_only",
            requiredOutput="Deep Delegation"
        )
        _, depth_status = await agent_mesh_service.request_delegation(None, depth_req, delegation_chain=depth_chain)
        assert "Maximum delegation depth" in depth_status

    asyncio.run(_test())

def test_artifact_exchange_and_disagreements():
    async def _test():
        msn_id = "msn_art_test"
        tsk_id = "tsk_art_01"

        # 1. Artifact Exchange
        art = await agent_mesh_service.exchange_artifact(
            None, msn_id, tsk_id, "ag_research_01", "research_report",
            {"summary": "Evaluated architecture options."}, classification="internal"
        )
        assert art["validation_status"] == "valid"

        # 2. Record Fact Disagreement
        dis = await agent_mesh_service.record_disagreement(
            None, msn_id, tsk_id, ["ag_analyst_02", "ag_research_01"],
            {"ag_analyst_02": "$5.2M", "ag_research_01": "$4.8M"},
            [{"source": "doc_specs_01", "fact": "Official Q3 target: $5.0M"}]
        )
        assert dis["resolution"] == "unresolved"

        # 3. Human Escalation Review
        rev = await agent_mesh_service.create_review_task(
            None, msn_id, tsk_id, art["id"], "Fact conflict on financial target requires operator decision"
        )
        assert rev["status"] == "pending"

        # 4. Resolve Human Review
        resolved = await agent_mesh_service.resolve_review_task(None, rev["id"], "approved", "usr_admin")
        assert resolved["status"] == "approved"

    asyncio.run(_test())

def test_agent_mesh_rest_api():
    # 1. Registry API
    reg_res = client.get("/api/v1/agents/registry?workspaceId=ws_default_creator")
    assert reg_res.status_code == 200
    assert len(reg_res.json()) >= 5

    # 2. Capabilities API
    cap_res = client.get("/api/v1/agents/capabilities")
    assert cap_res.status_code == 200

    # 3. Delegations API
    del_res = client.get("/api/v1/agents/delegations?missionId=msn_default_creator")
    assert del_res.status_code == 200

    # 4. Execution Mesh Graph API
    mesh_res = client.get("/api/v1/agents/mesh/msn_default_creator")
    assert mesh_res.status_code == 200
    assert "nodes" in mesh_res.json()

    # 5. Artifacts API
    art_res = client.get("/api/v1/agents/mesh/msn_default_creator/artifacts")
    assert art_res.status_code == 200

    # 6. Disagreements API
    dis_res = client.get("/api/v1/agents/mesh/msn_default_creator/disagreements")
    assert dis_res.status_code == 200

    # 7. Reviews API & Approval
    rev_res = client.get("/api/v1/agents/reviews")
    assert rev_res.status_code == 200
    review_id = rev_res.json()[0]["id"]

    app_res = client.post(f"/api/v1/agents/reviews/{review_id}/approve")
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "approved"
