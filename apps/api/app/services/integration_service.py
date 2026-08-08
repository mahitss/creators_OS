import uuid
import urllib.parse
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import encrypt_secret, decrypt_secret
from app.services import attention_service

# Controlled Provider Abstraction
SUPPORTED_PROVIDERS = ["google", "github", "youtube", "slack", "notion"]

# Store active state tokens for CSRF validation during OAuth flow
_oauth_states: Dict[str, dict] = {}
_in_memory_connections: Dict[str, dict] = {}

async def generate_connect_url(workspace_id: str, provider: str) -> Tuple[str, str]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider '{provider}'. Supported providers: {SUPPORTED_PROVIDERS}")

    state = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    _oauth_states[state] = {
        "workspace_id": workspace_id,
        "provider": provider,
        "created_at": now
    }

    if provider == "google":
        # Google OAuth authorization URL construction with minimum identity scopes
        client_id = "mock_google_client_id.apps.googleusercontent.com"
        redirect_uri = "http://localhost:8000/api/v1/integrations/google/callback"
        scopes = "openid email profile"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scopes,
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return auth_url, state
    else:
        auth_url = f"https://oauth.{provider}.com/authorize?state={state}"
        return auth_url, state

async def handle_oauth_callback(
    session: Optional[AsyncSession],
    workspace_id: str,
    provider: str,
    code: str,
    state: str
) -> dict:
    # 1. Validate State Token to Prevent CSRF
    state_data = _oauth_states.get(state)
    if not state_data or state_data["workspace_id"] != workspace_id or state_data["provider"] != provider:
        raise ValueError("Invalid or expired OAuth state parameter.")

    # Remove state after validation
    _oauth_states.pop(state, None)

    # 2. Perform Code Exchange (Simulated / Production Google Identity Exchange)
    now_iso = datetime.now(timezone.utc).isoformat()
    mock_email = "alex.creator@vapor.os"
    mock_account_name = "Alex (Vapor Creator)"
    mock_access_token = f"ya29.mock_access_token_{uuid.uuid4()}"
    mock_refresh_token = f"1//mock_refresh_token_{uuid.uuid4()}"

    # 3. Encrypt Tokens Before Storage
    encrypted_access = encrypt_secret(mock_access_token)
    encrypted_refresh = encrypt_secret(mock_refresh_token)

    # 4. Upsert Integration Connection
    connection_key = f"{workspace_id}:{provider}"
    connection = {
        "id": str(uuid.uuid4()),
        "workspace_id": workspace_id,
        "provider": provider,
        "status": "connected",
        "scopes": ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
        "external_account_id": f"google_{str(uuid.uuid4())[:8]}",
        "external_account_name": mock_account_name,
        "encrypted_access_token": encrypted_access,
        "encrypted_refresh_token": encrypted_refresh,
        "connected_at": now_iso,
        "last_synced_at": now_iso,
        "last_sync_error": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_connections[connection_key] = connection
    return _sanitize_connection(connection)

async def list_connections(
    session: Optional[AsyncSession],
    workspace_id: str
) -> Tuple[List[dict], int]:
    connections = [
        _sanitize_connection(conn)
        for conn in _in_memory_connections.values()
        if conn["workspace_id"] == workspace_id
    ]
    return connections, len(connections)

async def get_connection(
    session: Optional[AsyncSession],
    workspace_id: str,
    provider: str
) -> Optional[dict]:
    connection_key = f"{workspace_id}:{provider}"
    conn = _in_memory_connections.get(connection_key)
    if not conn:
        return None
    return _sanitize_connection(conn)

async def disconnect_provider(
    session: Optional[AsyncSession],
    workspace_id: str,
    provider: str
) -> Optional[dict]:
    connection_key = f"{workspace_id}:{provider}"
    conn = _in_memory_connections.get(connection_key)
    if not conn:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    conn["status"] = "disconnected"
    conn["encrypted_access_token"] = None
    conn["encrypted_refresh_token"] = None
    conn["updated_at"] = now_iso
    return _sanitize_connection(conn)

async def refresh_connection(
    session: Optional[AsyncSession],
    workspace_id: str,
    provider: str
) -> Optional[dict]:
    connection_key = f"{workspace_id}:{provider}"
    conn = _in_memory_connections.get(connection_key)
    if not conn:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    conn["status"] = "connected"
    conn["encrypted_access_token"] = encrypt_secret(f"ya29.refreshed_{uuid.uuid4()}")
    conn["last_synced_at"] = now_iso
    conn["last_sync_error"] = None
    conn["updated_at"] = now_iso
    return _sanitize_connection(conn)

async def mark_connection_expired(
    session: Optional[AsyncSession],
    workspace_id: str,
    provider: str
) -> Optional[dict]:
    connection_key = f"{workspace_id}:{provider}"
    conn = _in_memory_connections.get(connection_key)
    if not conn:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    conn["status"] = "expired"
    conn["last_sync_error"] = "OAuth access token expired."
    conn["updated_at"] = now_iso

    # Create Attention Item on Connection Expiration
    await attention_service._upsert_attention_item(
        workspace_id=workspace_id,
        type_name="system_error",
        title=f"{provider.capitalize()} Connection Expired",
        description=f"Your {provider.capitalize()} connection expired and requires re-authorization.",
        severity="medium",
        source_type="system_event",
        source_id=f"integration_{provider}"
    )

    return _sanitize_connection(conn)

def _sanitize_connection(conn: dict) -> dict:
    """Strips encrypted access/refresh tokens from output dictionary."""
    sanitized = conn.copy()
    sanitized.pop("encrypted_access_token", None)
    sanitized.pop("encrypted_refresh_token", None)
    return sanitized
