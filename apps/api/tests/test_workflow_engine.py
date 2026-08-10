import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.workflows import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowDefinitionSchema,
    WorkflowNodeSchema,
    WorkflowEdgeSchema
)
from app.services import workflow_engine

client = TestClient(app)

def test_workflow_definition_validation_and_cycle_prevention():
    # Valid Graph
    valid_def = {
        "nodes": [
            {"id": "n1", "node_key": "trig", "type": "trigger", "title": "Trigger"},
            {"id": "n2", "node_key": "agent", "type": "agent", "title": "Agent Node"},
            {"id": "n3", "node_key": "end", "type": "end", "title": "End Node"}
        ],
        "edges": [
            {"id": "e1", "source_node_id": "n1", "target_node_id": "n2"},
            {"id": "e2", "source_node_id": "n2", "target_node_id": "n3"}
        ]
    }
    valid, errors, warnings, caps = workflow_engine.validate_workflow_definition(valid_def)
    assert valid is True
    assert len(errors) == 0
    assert "ingress_event" in caps
    assert "agent_execution" in caps

    # Graph with Cycle: n1 -> n2 -> n3 -> n1
    cycle_def = {
        "nodes": [
            {"id": "n1", "node_key": "trig", "type": "trigger", "title": "Trigger"},
            {"id": "n2", "node_key": "agent", "type": "agent", "title": "Agent Node"},
            {"id": "n3", "node_key": "end", "type": "end", "title": "End Node"}
        ],
        "edges": [
            {"id": "e1", "source_node_id": "n1", "target_node_id": "n2"},
            {"id": "e2", "source_node_id": "n2", "target_node_id": "n3"},
            {"id": "e3", "source_node_id": "n3", "target_node_id": "n1"}
        ]
    }
    valid_cycle, errors_cycle, _, _ = workflow_engine.validate_workflow_definition(cycle_def)
    assert valid_cycle is False
    assert any("cycle detected" in err.lower() for err in errors_cycle)

def test_workflow_compilation_to_dag():
    definition = {
        "nodes": [
            {"id": "n1", "node_key": "t1", "type": "trigger"},
            {"id": "n2", "node_key": "tool1", "type": "tool", "config": {"tool_name": "create_content"}},
            {"id": "n3", "node_key": "e1", "type": "end"}
        ],
        "edges": [
            {"id": "e1", "source_node_id": "n1", "target_node_id": "n2"},
            {"id": "e2", "source_node_id": "n2", "target_node_id": "n3"}
        ]
    }
    compiled = workflow_engine.compile_workflow_to_dag(definition, "wf_test_comp", version=1)
    assert compiled["workflow_id"] == "wf_test_comp"
    assert len(compiled["nodes"]) == 3
    # n2 depends on n1
    n2_compiled = next(cn for cn in compiled["nodes"] if cn["node_key"] == "n2")
    assert "n1" in n2_compiled["dependencies"]
    assert n2_compiled["tool_name"] == "create_content"

def test_workflow_creation_dry_run_and_publishing():
    async def _test():
        wf_in = WorkflowCreate(
            workspace_id="ws_wf_test",
            name="Executive Brief Workflow",
            description="Automates executive brief synthesis",
            definition=WorkflowDefinitionSchema(
                nodes=[
                    WorkflowNodeSchema(id="n1", node_key="t1", type="trigger", title="Schedule"),
                    WorkflowNodeSchema(id="n2", node_key="a1", type="agent", title="AI Synthesizer"),
                    WorkflowNodeSchema(id="n3", node_key="e1", type="end", title="Done")
                ],
                edges=[
                    WorkflowEdgeSchema(id="e1", source_node_id="n1", target_node_id="n2"),
                    WorkflowEdgeSchema(id="e2", source_node_id="n2", target_node_id="n3")
                ]
            )
        )
        wf = await workflow_engine.create_workflow(None, wf_in, created_by="usr_owner")
        assert wf["name"] == "Executive Brief Workflow"
        assert wf["status"] == "draft"

        # Dry run simulation
        dry_run = await workflow_engine.dry_run_workflow(None, wf["id"], {})
        assert dry_run.simulated is True
        assert dry_run.policy_decision == "ALLOW"

        # Publish workflow
        pub_res = await workflow_engine.publish_workflow(None, wf["id"], user_id="usr_owner")
        assert pub_res.workflow_id == wf["id"]
        assert pub_res.version == 1

        # Check published workflow status
        wf_updated = await workflow_engine.get_workflow(None, wf["id"])
        assert wf_updated["status"] == "active"

    asyncio.run(_test())

def test_workflow_rest_api_endpoints():
    # 1. Create workflow via REST API
    payload = {
        "workspace_id": "ws_api_wf",
        "name": "REST API Workflow",
        "description": "Created via API test",
        "definition": {
            "nodes": [
                {"id": "n1", "node_key": "trig", "type": "trigger", "title": "Trigger"},
                {"id": "n2", "node_key": "appr", "type": "approval", "title": "Human Gate"},
                {"id": "n3", "node_key": "end", "type": "end", "title": "End"}
            ],
            "edges": [
                {"id": "e1", "source_node_id": "n1", "target_node_id": "n2"},
                {"id": "e2", "source_node_id": "n2", "target_node_id": "n3"}
            ]
        }
    }
    create_res = client.post("/api/v1/workflows", json=payload)
    assert create_res.status_code == 201
    wf_data = create_res.json()
    wf_id = wf_data["id"]

    # 2. Validate workflow via API
    val_res = client.post(f"/api/v1/workflows/{wf_id}/validate")
    assert val_res.status_code == 200
    assert val_res.json()["valid"] is True

    # 3. Publish workflow via API
    pub_res = client.post(f"/api/v1/workflows/{wf_id}/publish")
    assert pub_res.status_code == 200
    assert pub_res.json()["version"] == 1

    # 4. Trigger workflow run via API
    run_res = client.post(f"/api/v1/workflows/{wf_id}/run")
    assert run_res.status_code == 202
    assert run_res.json()["status"] == "running"

    # 5. List runs via API
    runs_res = client.get(f"/api/v1/workflows/{wf_id}/runs")
    assert runs_res.status_code == 200
    assert len(runs_res.json()) >= 1
