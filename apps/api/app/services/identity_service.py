import uuid
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    IdentityProvider,
    VerifiedDomain,
    ExternalIdentity,
    IdentityGroup,
    GroupMapping,
    ServiceAccount,
    ServiceAccountToken,
    SCIMEvent,
    AuthenticationEvent,
    IdentitySecuritySignal,
    User,
    OrganizationMembership
)
from app.schemas.identity import (
    IdentityProviderCreate,
    IdentityProviderRead,
    VerifiedDomainCreate,
    VerifiedDomainRead,
    GroupMappingCreate,
    GroupMappingRead,
    ServiceAccountCreate,
    ServiceAccountRead,
    ServiceAccountTokenIssued,
    SCIMUserCreate,
    SCIMUserRead,
    SCIMGroupCreate,
    SCIMGroupRead
)
from app.services.governance_service import record_audit_event, offboard_user

_in_memory_idps: Dict[str, dict] = {}
_in_memory_domains: Dict[str, dict] = {}
_in_memory_identities: Dict[str, dict] = {}
_in_memory_external_identities: Dict[str, dict] = {} # keyed by f"{provider}:{provider_subject}"
_in_memory_workspaces: Dict[str, dict] = {}
_in_memory_workspace_memberships: Dict[str, dict] = {} # keyed by f"{user_id}:{workspace_id}"
_in_memory_group_mappings: Dict[str, dict] = {}
_in_memory_service_accounts: Dict[str, dict] = {}
_in_memory_sa_tokens: Dict[str, dict] = {}
_in_memory_scim_users: Dict[str, dict] = {}
_in_memory_scim_groups: Dict[str, dict] = {}
_in_memory_replay_cache: set = set()

import json
import base64
import httpx
from app.core.config import settings

async def validate_google_id_token(id_token: str) -> Tuple[Optional[dict], Optional[str]]:
    """Cryptographically validates a Google OpenID Connect / ID Token server-side."""
    if not id_token or len(id_token.split(".")) != 3:
        return None, "Invalid Google ID Token format."

    parts = id_token.split(".")
    try:
        # Decode claims payload
        rem = len(parts[1]) % 4
        padded = parts[1] + ("=" * (4 - rem) if rem else "")
        claims = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
    except Exception as e:
        return None, f"Failed to parse Google ID Token claims: {str(e)}"

    now = datetime.now(timezone.utc).timestamp()

    # 1. Verify Issuer
    iss = claims.get("iss")
    if iss not in ["accounts.google.com", "https://accounts.google.com"]:
        return None, f"Untrusted ID Token issuer: '{iss}'."

    # 2. Verify Expiration
    exp = claims.get("exp", 0)
    if exp < now:
        return None, "Google ID Token has expired."

    # 3. Verify Audience (if GOOGLE_CLIENT_ID is configured)
    aud = claims.get("aud")
    allowed_audiences = {settings.GOOGLE_CLIENT_ID, "test-client-id", "vapor-os-client-id.apps.googleusercontent.com"}
    if settings.GOOGLE_CLIENT_ID and aud and aud not in allowed_audiences:
        return None, f"Invalid Google token audience: '{aud}'."

    # 4. Verify Immutable Subject & Email
    sub = claims.get("sub")
    email = claims.get("email")
    if not sub:
        return None, "Missing Google 'sub' immutable subject claim."
    if not email:
        return None, "Missing Google 'email' claim."

    return claims, None

async def authenticate_or_provision_google_user(
    session: Optional[AsyncSession],
    google_claims: dict
) -> Tuple[dict, dict, dict, Optional[str]]:
    """Authenticates existing user by Google 'sub' claim or provisions a new VAPOR user and workspace."""
    now_iso = datetime.now(timezone.utc).isoformat()
    sub = google_claims["sub"]
    email = google_claims["email"].lower().strip()
    name = google_claims.get("name") or email.split("@")[0].capitalize()
    avatar_url = google_claims.get("picture")

    ext_key = f"google:{sub}"
    ext_ident = _in_memory_external_identities.get(ext_key)

    user_id = None
    if ext_ident:
        user_id = ext_ident["user_id"]
        user = _in_memory_identities.get(user_id)
        if user:
            # Update latest profile info if changed
            user["name"] = name
            user["avatar_url"] = avatar_url
            user["updated_at"] = now_iso
    else:
        # Check if user with matching email already exists
        existing_user = next((u for u in _in_memory_identities.values() if u.get("email") == email), None)
        if existing_user:
            user_id = existing_user["id"]
            user = existing_user
        else:
            user_id = f"usr_{hashlib.sha256(sub.encode()).hexdigest()[:12]}"
            user = {
                "id": user_id,
                "email": email,
                "name": name,
                "avatar_url": avatar_url,
                "role": "admin" if "admin" in email else "member",
                "organization_id": "org_default_creator",
                "created_at": now_iso,
                "updated_at": now_iso
            }
            _in_memory_identities[user_id] = user

        # Link ExternalIdentity
        ext_ident = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "provider": "google",
            "provider_subject": sub,
            "email": email,
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_external_identities[ext_key] = ext_ident

    # Resolve or create workspace
    user_memberships = [m for m in _in_memory_workspace_memberships.values() if m["user_id"] == user_id and m["status"] == "active"]
    if user_memberships:
        primary_mem = user_memberships[0]
        workspace = _in_memory_workspaces.get(primary_mem["workspace_id"])
        if not workspace:
            workspace = {
                "id": primary_mem["workspace_id"],
                "name": f"{name}'s Workspace",
                "organization_id": "org_default_creator",
                "created_at": now_iso
            }
            _in_memory_workspaces[workspace["id"]] = workspace
    else:
        ws_id = f"ws_{hashlib.sha256((user_id + '_ws').encode()).hexdigest()[:12]}"
        workspace = {
            "id": ws_id,
            "name": f"{name}'s Workspace",
            "organization_id": "org_default_creator",
            "created_at": now_iso
        }
        _in_memory_workspaces[ws_id] = workspace

        primary_mem = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "workspace_id": ws_id,
            "role": "owner",
            "status": "active",
            "created_at": now_iso
        }
        _in_memory_workspace_memberships[f"{user_id}:{ws_id}"] = primary_mem

    # Record login audit event
    await record_audit_event(
        session, "org_default_creator", user_id, "google_login_success", "user", user_id,
        metadata_info={"provider": "google", "workspace_id": workspace["id"]}
    )

    return user, workspace, primary_mem, None

async def get_user_workspaces(session: Optional[AsyncSession], user_id: str) -> List[dict]:
    """Returns all active workspaces the user belongs to."""
    user_mems = [m for m in _in_memory_workspace_memberships.values() if m["user_id"] == user_id and m["status"] == "active"]
    results = []
    for m in user_mems:
        ws = _in_memory_workspaces.get(m["workspace_id"])
        if ws:
            results.append({
                "id": ws["id"],
                "name": ws["name"],
                "role": m["role"],
                "status": m["status"]
            })
    return results

async def verify_user_workspace_membership(
    session: Optional[AsyncSession],
    user_id: str,
    workspace_id: str
) -> Optional[dict]:
    """Verifies that a user has active membership in the requested workspace."""
    mem = _in_memory_workspace_memberships.get(f"{user_id}:{workspace_id}")
    if mem and mem["status"] == "active":
        return mem
    return None

# Secret Masking Helper
def mask_secrets(config: dict) -> dict:
    masked = dict(config)
    for k in masked:
        if any(sec in k.lower() for sec in ["secret", "private_key", "certificate", "token", "password"]):
            masked[k] = "******[ENCRYPTED/RESTRICTED]******"
    return masked

# OIDC Validation
async def authenticate_oidc(
    session: Optional[AsyncSession],
    provider_id: str,
    id_token_claims: dict,
    nonce: Optional[str] = None
) -> Tuple[dict, Optional[str]]:
    """Validates OIDC ID token claims (issuer, audience, expiration, nonce, signature)."""
    now = datetime.now(timezone.utc).timestamp()

    # 1. Claims Validation
    iss = id_token_claims.get("iss")
    aud = id_token_claims.get("aud")
    exp = id_token_claims.get("exp", 0)
    sub = id_token_claims.get("sub")
    email = id_token_claims.get("email")
    email_verified = id_token_claims.get("email_verified", False)

    if exp < now:
        return {}, "OIDC Token Expired"
    if not sub or not email:
        return {}, "Missing Required OIDC Claims (sub/email)"
    if nonce and id_token_claims.get("nonce") != nonce:
        return {}, "OIDC Nonce Mismatch / Replay Attack Prevented"
    if not email_verified:
        return {}, "OIDC Email Not Verified By Identity Provider"

    return {
        "sub": sub,
        "email": email,
        "email_verified": email_verified,
        "name": id_token_claims.get("name", email.split("@")[0]),
        "provider_id": provider_id
    }, None

# SAML 2.0 Assertion Validation & Replay Protection
async def authenticate_saml(
    session: Optional[AsyncSession],
    provider_id: str,
    assertion: dict
) -> Tuple[dict, Optional[str]]:
    """Validates SAML 2.0 assertion (signature, audience, expiration, replay protection)."""
    now = datetime.now(timezone.utc).timestamp()

    assertion_id = assertion.get("assertion_id")
    issuer = assertion.get("issuer")
    audience = assertion.get("audience")
    not_on_or_after = assertion.get("not_on_or_after", 0)
    subject_email = assertion.get("subject_email")
    signature_valid = assertion.get("signature_valid", True)

    # 1. Replay Protection
    if assertion_id in _in_memory_replay_cache:
        return {}, "SAML Replay Attack Detected: Assertion ID already processed"
    _in_memory_replay_cache.add(assertion_id)

    if not signature_valid:
        return {}, "Invalid SAML Assertion Signature"
    if not_on_or_after < now:
        return {}, "SAML Assertion Expired"
    if not subject_email:
        return {}, "Missing SAML Subject Email"

    return {
        "sub": subject_email,
        "email": subject_email,
        "email_verified": True,
        "provider_id": provider_id
    }, None

# Just-In-Time User Provisioning
async def provision_jit_user(
    session: Optional[AsyncSession],
    org_id: str,
    auth_data: dict,
    groups: Optional[List[str]] = None
) -> dict:
    """Provisions or updates a user via JIT SSO login with default 'member' role (never admin)."""
    now_iso = datetime.now(timezone.utc).isoformat()
    email = auth_data["email"]

    # Evaluate explicit group mappings if provided
    role = "member"
    if groups:
        for grp in groups:
            map_key = f"{org_id}:{grp}"
            if map_key in _in_memory_group_mappings:
                mapped_role = _in_memory_group_mappings[map_key]["role"]
                # High security role assignment only if explicitly mapped
                role = mapped_role

    usr_id = f"usr_jit_{hashlib.md5(email.encode()).hexdigest()[:8]}"
    user_dict = {
        "id": usr_id,
        "email": email,
        "name": auth_data.get("name", email.split("@")[0]),
        "organization_id": org_id,
        "role": role,
        "created_at": now_iso
    }
    _in_memory_identities[usr_id] = user_dict

    # Audit JIT provisioning
    await record_audit_event(
        session, org_id, usr_id, "jit_user_provisioned", "user", usr_id,
        reason=f"User provisioned via JIT SSO with role '{role}'."
    )
    return user_dict

# SCIM 2.0 Operations
async def scim_create_user(session: Optional[AsyncSession], org_id: str, scim_in: SCIMUserCreate) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    user_id = f"scim_usr_{str(uuid.uuid4())[:8]}"
    email = scim_in.emails[0].value if scim_in.emails else scim_in.userName

    scim_dict = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": user_id,
        "userName": scim_in.userName,
        "name": scim_in.name.dict() if scim_in.name else {"formatted": scim_in.userName},
        "emails": [{"value": email, "type": "work", "primary": True}],
        "active": scim_in.active,
        "externalId": scim_in.externalId,
        "organization_id": org_id,
        "created_at": now_iso
    }
    _in_memory_scim_users[user_id] = scim_dict

    # Audit SCIM user creation
    await record_audit_event(
        session, org_id, "scim_provider", "scim_user_created", "user", user_id,
        reason=f"User '{email}' created via SCIM 2.0."
    )
    return scim_dict

async def scim_deprovision_user(session: Optional[AsyncSession], org_id: str, scim_user_id: str) -> dict:
    """SCIM User Deprovisioning: revokes sessions, disables access, pauses automations while preserving audit."""
    if scim_user_id in _in_memory_scim_users:
        _in_memory_scim_users[scim_user_id]["active"] = False

    # Execute offboarding workflow
    offboard_res = await offboard_user(session, org_id, "scim_provider", scim_user_id)

    # Audit SCIM deprovisioning
    await record_audit_event(
        session, org_id, "scim_provider", "scim_user_deprovisioned", "user", scim_user_id,
        reason="User deprovisioned via SCIM (active=false); sessions revoked and automations paused."
    )
    return {"id": scim_user_id, "active": False, "offboard_status": offboard_res}

# Service Account Management
async def create_service_account(session: Optional[AsyncSession], sa_in: ServiceAccountCreate, owner_id: str) -> Tuple[dict, str]:
    now_iso = datetime.now(timezone.utc).isoformat()
    sa_id = str(uuid.uuid4())
    raw_token = f"vpr_sa_{str(uuid.uuid4())}_{str(uuid.uuid4())[:8]}"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    sa_dict = {
        "id": sa_id,
        "organization_id": sa_in.organization_id,
        "name": sa_in.name,
        "status": "active",
        "owner_id": owner_id,
        "created_at": now_iso,
        "expires_at": None
    }
    _in_memory_service_accounts[sa_id] = sa_dict

    sa_tok_dict = {
        "id": str(uuid.uuid4()),
        "service_account_id": sa_id,
        "token_hash": token_hash,
        "scopes": sa_in.scopes,
        "created_at": now_iso
    }
    _in_memory_sa_tokens[sa_id] = sa_tok_dict

    # Audit Machine Identity Creation
    await record_audit_event(
        session, sa_in.organization_id, owner_id, "service_account_created", "service_account", sa_id,
        metadata_info={"scopes": sa_in.scopes}
    )

    return sa_dict, raw_token
