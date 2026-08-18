import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import jwt
import pytest
from starlette.testclient import TestClient

# Ensure root and apps/api are in sys.path
test_dir = Path(__file__).resolve().parent
api_dir = test_dir.parent
root_dir = api_dir.parent.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from app.core.config import settings
from app.services import identity_service

def _make_test_jwt(user_id: str, email: str, role: str, workspace_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "workspace_id": workspace_id,
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "iat": int(now.timestamp())
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Seed standard test memberships
_standard_memberships = [
    ("usr_default_01", "ws_default_01", "owner"),
    ("usr_admin_01", "ws_default_01", "admin"),
    ("usr_alex", "ws_test_alpha", "member"),
    ("usr_bob", "ws_test_beta", "member"),
    ("usr_alex_01", "ws_test_01", "member"),
    ("usr_default_owner", "ws_default_01", "owner"),
    ("usr_executive_01", "ws_default_01", "admin"),
    ("usr_member_01", "ws_default_01", "member"),
]

for uid, wid, role in _standard_memberships:
    identity_service._in_memory_workspace_memberships[f"{uid}:{wid}"] = {
        "user_id": uid,
        "workspace_id": wid,
        "role": role,
        "status": "active",
        "permissions": ["admin", "read", "write"] if role in ["owner", "admin"] else ["read", "write"]
    }

# Patch TestClient.request so legacy functional test cases supply signed test JWTs
_original_testclient_request = TestClient.request

def _auto_auth_testclient_request(self, method, url, *args, **kwargs):
    current_test = os.environ.get("PYTEST_CURRENT_TEST", "")
    # Strict security tests must NOT be auto-authenticated
    if "test_p0_" in current_test or "test_critical_security_" in current_test or "test_google_auth" in current_test:
        return _original_testclient_request(self, method, url, *args, **kwargs)

    headers = kwargs.get("headers")
    if headers is None:
        headers = {}
    else:
        headers = dict(headers)

    # If no Authorization header is provided, generate a signed test JWT
    if "Authorization" not in headers and "authorization" not in headers:
        user_id = headers.get("X-User-Id", headers.get("x-user-id", "usr_default_01"))
        ws_id = headers.get("X-Workspace-Id", headers.get("x-workspace-id", "ws_default_01"))
        role = headers.get("X-User-Role", headers.get("x-user-role", "admin"))
        
        # Ensure membership is registered
        identity_service._in_memory_workspace_memberships[f"{user_id}:{ws_id}"] = {
            "user_id": user_id,
            "workspace_id": ws_id,
            "role": role,
            "status": "active",
            "permissions": ["admin", "read", "write"] if role in ["owner", "admin"] else ["read", "write"]
        }

        token = _make_test_jwt(user_id, f"{user_id}@test.vapor.os", role, ws_id)
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

    return _original_testclient_request(self, method, url, *args, **kwargs)

TestClient.request = _auto_auth_testclient_request
