import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_dag_alpha"
HEADERS_A = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}

def test_full_dag_validation_and_parallel_execution():
    # 1. Create Mission
    m_res = client.post("/api/v1/missions", json={"title": "Client Proposal DAG Mission", "description": "Complex proposal orchestration"}, headers=HEADERS_A)
    assert m_res.status_code == 201
    m_id = m_res.json()["id"]

    # 2. Create Valid Parallel DAG Plan (A & B parallel -> C synthesis -> D proposal)
    nodes = [
        {"node_key": "research_docs", "title": "Research Docs", "type": "context_retrieval", "dependencies": [], "tool_name": "search_drive_files"},
        {"node_key": "research_email", "title": "Research Gmail", "type": "context_retrieval", "dependencies": [], "tool_name": "search_gmail"},
        {"node_key": "synthesize", "title": "Synthesize Research", "type": "analysis", "dependencies": ["research_docs", "research_email"]},
        {"node_key": "generate_proposal", "title": "Generate Proposal", "type": "content_generation", "dependencies": ["synthesize"], "tool_name": "create_content"}
    ]

    dag_res = client.post(f"/api/v1/missions/{m_id}/dag-plans", json={"goal": "Prepare proposal", "nodes": nodes}, headers=HEADERS_A)
    assert dag_res.status_code == 201
    plan_data = dag_res.json()
    plan_id = plan_data["id"]
    assert plan_data["status"] == "validated"

    # 3. Retrieve Nodes
    nodes_res = client.get(f"/api/v1/missions/{m_id}/dag-plans/{plan_id}/nodes", headers=HEADERS_A)
    assert nodes_res.status_code == 200
    plan_nodes = nodes_res.json()
    assert len(plan_nodes) == 4

    # 4. Create Agent Run & Execute DAG Plan
    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Execute DAG"}, headers=HEADERS_A)
    assert run_res.status_code == 201
    run_id = run_res.json()["id"]

    exec_res = client.post(f"/api/v1/missions/{m_id}/dag-plans/{plan_id}/execute?run_id={run_id}", headers=HEADERS_A)
    assert exec_res.status_code == 200
    assert exec_res.json()["status"] in ["running", "completed"]

def test_dag_cycle_rejection():
    m_res = client.post("/api/v1/missions", json={"title": "Cycle Test Mission", "description": "Test cycle rejection"}, headers=HEADERS_A)
    m_id = m_res.json()["id"]

    # Cyclic Nodes: A -> B -> A
    nodes = [
        {"node_key": "node_a", "title": "Node A", "type": "tool_call", "dependencies": ["node_b"]},
        {"node_key": "node_b", "title": "Node B", "type": "tool_call", "dependencies": ["node_a"]}
    ]

    dag_res = client.post(f"/api/v1/missions/{m_id}/dag-plans", json={"goal": "Cyclic Goal", "nodes": nodes}, headers=HEADERS_A)
    assert dag_res.status_code == 400
    assert "Cycle detected" in dag_res.json()["detail"]
