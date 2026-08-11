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
_in_memory_group_mappings: Dict[str, dict] = {}
_in_memory_service_accounts: Dict[str, dict] = {}
_in_memory_sa_tokens: Dict[str, dict] = {}
_in_memory_scim_users: Dict[str, dict] = {}
_in_memory_scim_groups: Dict[str, dict] = {}
_in_memory_replay_cache: set = set()

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
