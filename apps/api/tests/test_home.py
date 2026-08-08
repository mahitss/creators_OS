import sys
from pathlib import Path

# Ensure apps/api is in Python path for test execution
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_home_executive_brief():
    response = client.get("/api/v1/home/brief?user_name=Mahit")
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_name"] == "Mahit"
    assert "Mahit" in data["greeting"]
    assert "summary_statement" in data
    assert isinstance(data["needs_attention"], list)
    assert isinstance(data["recent_activity"], list)
    assert isinstance(data["quick_actions"], list)
    assert data["is_empty_state"] is True
    assert len(data["quick_actions"]) > 0
