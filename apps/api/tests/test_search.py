import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_search_alpha"
WS_B = "ws_search_beta"

def test_full_global_search_ranking_and_security():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Empty Query Returns Empty Results
    empty_res = client.get("/api/v1/search?q=", headers=headers_a)
    assert empty_res.status_code == 200
    assert empty_res.json()["total"] == 0

    # 2. Create Entities in Workspace A
    # Mission
    client.post("/api/v1/missions", json={
        "title": "Kubernetes Cluster Setup",
        "description": "Deploy K8s node pool.",
        "priority": "high"
    }, headers=headers_a)

    # Content
    client.post("/api/v1/content", json={
        "title": "Kubernetes Architecture Guide",
        "type": "article",
        "content": "Deep dive into Kubernetes control plane."
    }, headers=headers_a)

    # Memory
    client.post("/api/v1/memories", json={
        "type": "preference",
        "title": "Kubernetes Helm Policy",
        "content": "Always use helm charts for deployment.",
        "importance": "high"
    }, headers=headers_a)

    # 3. Search "Kubernetes" in Workspace A -> Finds Mission, Content, and Memory
    s_res = client.get("/api/v1/search?q=Kubernetes", headers=headers_a)
    assert s_res.status_code == 200
    data = s_res.json()
    assert data["total"] == 3
    types_found = {r["type"] for r in data["results"]}
    assert "mission" in types_found
    assert "content" in types_found
    assert "memory" in types_found

    # 4. Cross-workspace Isolation: Workspace B searching "Kubernetes" returns 0 results
    s_b = client.get("/api/v1/search?q=Kubernetes", headers=headers_b)
    assert s_b.status_code == 200
    assert s_b.json()["total"] == 0
