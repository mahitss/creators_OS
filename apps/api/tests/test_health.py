import sys
import os
from pathlib import Path

# Add apps/api to python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.dependencies.db import get_db

# Override get_db for testing environment
async def mock_get_db():
    yield None

app.dependency_overrides[get_db] = mock_get_db

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data
    assert "services" in data
