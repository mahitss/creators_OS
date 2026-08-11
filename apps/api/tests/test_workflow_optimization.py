import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import workflow_optimization_service
from app.schemas.workflow_optimization import OptimizationExperimentCreate

client = TestClient(app)

def test_performance_analysis_and_bottlenecks():
    async def _test():
        wf_id = "wf_opt_test"

        # Performance Profile
        prof = await workflow_optimization_service.analyze_workflow_performance(None, wf_id)
        assert prof["execution_count"] > 0
        assert prof["p95_latency"] > 0

        # Bottlenecks
        b_list = await workflow_optimization_service.detect_bottlenecks(None, wf_id)
        assert len(b_list) >= 1
        assert b_list[0]["bottleneck_type"] in ["latency", "sequential_dependency"]

    asyncio.run(_test())

def test_proposal_generation_and_side_effect_safety():
    async def _test():
        wf_id = "wf_opt_test"

        # Safe Proposal Generation
        prop, status = await workflow_optimization_service.generate_optimization_proposal(None, wf_id)
        assert status == "SUCCESS"
        assert len(prop["changes"]) >= 1

        # Unsafe Side Effect Parallelization Blocked
        unsafe_changes = [{
            "change_type": "parallelize",
            "before": {"nodes": ["node_send_email_01", "node_write_drive_02"]}
        }]
        safe, err_msg = await workflow_optimization_service.validate_side_effects(unsafe_changes)
        assert safe is False
        assert "Unsafe parallelization" in err_msg

    asyncio.run(_test())

def test_sandbox_simulation_and_version_publication():
    async def _test():
        wf_id = "wf_opt_test"
        prop, _ = await workflow_optimization_service.generate_optimization_proposal(None, wf_id)

        # Simulation
        sim = await workflow_optimization_service.simulate_proposal(None, prop["id"])
        assert sim["simulated_latency_diff"] < 0
        assert sim["safety_validation"]["dlp_passed"] is True

        # Publish Version 2
        ver = await workflow_optimization_service.publish_optimization(None, prop["id"], "usr_admin")
        assert ver["version"] == 2

        # Rollback to Version 1
        rb = await workflow_optimization_service.rollback_optimization(None, wf_id, target_version=1)
        assert rb["active_version"] == 1
        assert rb["status"] == "rolled_back"

    asyncio.run(_test())

def test_canary_experiments_and_version_compare():
    async def _test():
        wf_id = "wf_opt_test"

        # Start Experiment
        exp_req = OptimizationExperimentCreate(candidateVersion=2, trafficSplit=0.10)
        exp = await workflow_optimization_service.start_experiment(None, wf_id, exp_req)
        assert exp["traffic_split"] == 0.10
        assert exp["status"] == "running"

        # Version Comparison Diff
        comp = await workflow_optimization_service.compare_versions(None, wf_id, 1, 2)
        assert comp["version_a"] == 1
        assert comp["version_b"] == 2
        assert len(comp["diff_json"]["nodes_modified"]) >= 1

    asyncio.run(_test())

def test_workflow_optimization_rest_api():
    # 1. Performance API
    p_res = client.get("/api/v1/workflows/wf_default_01/performance")
    assert p_res.status_code == 200

    # 2. Bottlenecks API
    b_res = client.get("/api/v1/workflows/wf_default_01/bottlenecks")
    assert b_res.status_code == 200

    # 3. Optimization Proposals API
    prop_res = client.get("/api/v1/workflows/wf_default_01/optimization")
    assert prop_res.status_code == 200
    prop_id = prop_res.json()[0]["id"]

    # 4. Simulation API
    sim_res = client.post(f"/api/v1/workflows/wf_default_01/optimization/simulate?proposalId={prop_id}")
    assert sim_res.status_code == 200

    # 5. Publish API
    pub_res = client.post(f"/api/v1/workflows/wf_default_01/optimization/{prop_id}/publish")
    assert pub_res.status_code == 200

    # 6. Rollback API
    rb_res = client.post(f"/api/v1/workflows/wf_default_01/optimization/{prop_id}/rollback?targetVersion=1")
    assert rb_res.status_code == 200

    # 7. Versions API & Compare
    v_res = client.get("/api/v1/workflows/wf_default_01/versions")
    assert v_res.status_code == 200

    c_res = client.get("/api/v1/workflows/wf_default_01/versions/1/compare/2")
    assert c_res.status_code == 200

    # 8. Experiments API
    exp_res = client.get("/api/v1/workflows/wf_default_01/experiments")
    assert exp_res.status_code == 200
