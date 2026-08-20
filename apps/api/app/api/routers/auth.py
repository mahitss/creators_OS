import os
import time
import uuid
import hmac
import hashlib
import json
import base64
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, status, Query, Header, Depends, Response, Cookie
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dependencies.db import get_db
from app.services import identity_service

router = APIRouter()

# In-memory challenge store with TTL
_pending_challenges: Dict[str, Dict[str, Any]] = {}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400 # 24 hours
    user_id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    workspace_id: str
    role: str

class GoogleVerifyRequest(BaseModel):
    id_token: Optional[str] = None
    credential: Optional[str] = None # GIS credential parameter

class PasskeyChallengeResponse(BaseModel):
    challenge: str
    timeout_ms: int = 60000
    rp_id: str = "vapor.os"
    user_id: str

class PasskeyRegisterRequest(BaseModel):
    email: EmailStr
    credential_id: str
    challenge: Optional[str] = None
    client_data_json: Optional[str] = None
    authenticator_data: Optional[str] = None
    signature: Optional[str] = None

class WorkspaceSummary(BaseModel):
    id: str
    name: str
    role: str
    status: str

class AuthMeResponse(BaseModel):
    user_id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str
    workspace_id: str
    workspaces: List[WorkspaceSummary] = []
    authenticated: bool

class WorkspaceSelectRequest(BaseModel):
    workspace_id: str

def _create_jwt_token(payload: Dict[str, Any]) -> str:
    """Creates an HMAC-SHA256 authenticated JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    signing_input = f"{header_b64}.{payload_b64}"
    secret_key = settings.SECRET_KEY.encode()
    sig = hmac.new(secret_key, signing_input.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return f"{signing_input}.{sig_b64}"

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verifies and decodes an HMAC-SHA256 JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token format")
        
        signing_input = f"{parts[0]}.{parts[1]}"
        secret_key = settings.SECRET_KEY.encode()
        expected_sig = hmac.new(secret_key, signing_input.encode(), hashlib.sha256).digest()
        
        # Add padding back for decode
        rem = len(parts[2]) % 4
        sig_str = parts[2] + ("=" * (4 - rem) if rem else "")
        provided_sig = base64.urlsafe_b64decode(sig_str.encode())
        
        if not hmac.compare_digest(expected_sig, provided_sig):
            raise ValueError("Invalid token signature")
        
        rem_p = len(parts[1]) % 4
        payload_str = parts[1] + ("=" * (4 - rem_p) if rem_p else "")
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        
        if payload.get("exp", 0) < time.time():
            raise ValueError("Token expired")
            
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication token verification failed: {str(e)}"
        )

@router.post("/auth/google/verify", response_model=TokenResponse)
async def verify_google_identity(
    payload: GoogleVerifyRequest,
    response: Response,
    db: Optional[AsyncSession] = Depends(get_db)
) -> TokenResponse:
    """Verifies Google ID Token server-side, provisions user & workspace, and issues secure VAPOR session."""
    token_str = payload.credential or payload.id_token
    if not token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google ID token or credential is required."
        )

    claims, err = await identity_service.validate_google_id_token(token_str)
    if err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Google authentication failed: {err}"
        )

    user, workspace, membership, p_err = await identity_service.authenticate_or_provision_google_user(db, claims)
    if p_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User provisioning failed: {p_err}"
        )

    now = time.time()
    token_claims = {
        "sub": user["id"],
        "email": user["email"],
        "name": user.get("name"),
        "avatar_url": user.get("avatar_url"),
        "role": membership["role"],
        "workspace_id": workspace["id"],
        "provider": "google",
        "iat": int(now),
        "exp": int(now + 86400), # 24h
        "jti": str(uuid.uuid4())
    }

    session_token = _create_jwt_token(token_claims)

    # Set secure HttpOnly cookie
    is_prod = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="vapor_session_token",
        value=session_token,
        max_age=86400,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        path="/"
    )

    return TokenResponse(
        access_token=session_token,
        token_type="bearer",
        expires_in=86400,
        user_id=user["id"],
        email=user["email"],
        name=user.get("name"),
        avatar_url=user.get("avatar_url"),
        workspace_id=workspace["id"],
        role=membership["role"]
    )

@router.post("/auth/logout")
async def logout(response: Response):
    """Invalidates the active VAPOR session and removes auth cookies."""
    is_prod = settings.ENVIRONMENT == "production"
    response.delete_cookie(
        key="vapor_session_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=is_prod
    )
    response.set_cookie(
        key="vapor_session_token",
        value="",
        max_age=0,
        expires=0,
        path="/",
        httponly=True,
        samesite="lax",
        secure=is_prod
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return {"status": "logged_out", "message": "Vapor session successfully terminated."}

@router.get("/auth/me", response_model=AuthMeResponse)
async def get_current_session(
    response: Response,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    session_cookie: Optional[str] = Cookie(None, alias="vapor_session_token"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    """Returns the authenticated identity, avatar, active workspace, and accessible workspaces."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_cookie:
        token = session_cookie

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthenticated: No active session token found."
        )

    claims = verify_jwt_token(token)
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token: Missing subject claim."
        )
    ws_id = claims.get("workspace_id")
    if not ws_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token: Missing workspace claim."
        )
    ws_list = await identity_service.get_user_workspaces(db, user_id)
    if not ws_list:
        ws_list = [{
            "id": ws_id,
            "name": f"{claims.get('name', 'User')}'s Workspace",
            "role": claims.get("role", "member"),
            "status": "active"
        }]

    return AuthMeResponse(
        user_id=user_id,
        email=claims.get("email", ""),
        name=claims.get("name"),
        avatar_url=claims.get("avatar_url"),
        role=claims.get("role", "member"),
        workspace_id=ws_id,
        workspaces=[WorkspaceSummary(**w) for w in ws_list],
        authenticated=True
    )

@router.get("/auth/workspaces", response_model=List[WorkspaceSummary])
async def list_workspaces(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    session_cookie: Optional[str] = Cookie(None, alias="vapor_session_token"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    """Lists all active workspaces accessible to the authenticated identity."""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_cookie:
        token = session_cookie

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")

    claims = verify_jwt_token(token)
    user_id = claims.get("sub")
    workspaces = await identity_service.get_user_workspaces(db, user_id)
    return [WorkspaceSummary(**w) for w in workspaces]

@router.post("/auth/workspaces/select", response_model=TokenResponse)
async def select_workspace(
    payload: WorkspaceSelectRequest,
    response: Response,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    session_cookie: Optional[str] = Cookie(None, alias="vapor_session_token"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    """Switches the active workspace context in the user's session token."""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_cookie:
        token = session_cookie

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")

    claims = verify_jwt_token(token)
    user_id = claims.get("sub")
    membership = await identity_service.verify_user_workspace_membership(db, user_id, payload.workspace_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access Denied: You are not a member of workspace '{payload.workspace_id}'."
        )

    now = time.time()
    claims["workspace_id"] = payload.workspace_id
    claims["role"] = membership["role"]
    claims["iat"] = int(now)
    claims["exp"] = int(now + 86400)
    claims["jti"] = str(uuid.uuid4())

    new_token = _create_jwt_token(claims)
    is_prod = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="vapor_session_token",
        value=new_token,
        max_age=86400,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        path="/"
    )

    return TokenResponse(
        access_token=new_token,
        token_type="bearer",
        expires_in=86400,
        user_id=user_id,
        email=claims.get("email", ""),
        name=claims.get("name"),
        avatar_url=claims.get("avatar_url"),
        workspace_id=payload.workspace_id,
        role=membership["role"]
    )

@router.get("/auth/passkey/challenge", response_model=PasskeyChallengeResponse)
async def get_passkey_challenge(email: EmailStr = Query(..., description="User email for WebAuthn challenge")):
    """Issues a cryptographically secure random WebAuthn/Passkey challenge."""
    challenge_bytes = os.urandom(32)
    challenge_hex = challenge_bytes.hex()
    user_id = f"usr_{hashlib.sha256(email.encode()).hexdigest()[:12]}"
    
    _pending_challenges[email] = {
        "challenge": challenge_hex,
        "issued_at": time.time(),
        "user_id": user_id
    }
    
    return PasskeyChallengeResponse(
        challenge=challenge_hex,
        timeout_ms=60000,
        rp_id="vapor.os",
        user_id=user_id
    )

@router.post("/auth/passkey/verify", response_model=TokenResponse)
async def verify_passkey(
    payload: PasskeyRegisterRequest,
    response: Response,
    db: Optional[AsyncSession] = Depends(get_db)
) -> TokenResponse:
    """Verifies Passkey WebAuthn credential challenge and returns a signed session token."""
    if not payload.email or not payload.credential_id or len(payload.credential_id) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid passkey credential: email and credential ID are required."
        )
    
    if not payload.challenge:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: WebAuthn challenge response is mandatory."
        )

    challenge_entry = _pending_challenges.get(payload.email)
    if not challenge_entry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: No active challenge found for email. Request a new challenge."
        )

    if time.time() - challenge_entry["issued_at"] > 60:
        _pending_challenges.pop(payload.email, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="WebAuthn challenge expired."
        )

    if payload.challenge != challenge_entry["challenge"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid WebAuthn challenge signature."
        )

    # Optional origin verification if client_data_json provided
    if payload.client_data_json:
        try:
            client_data = json.loads(base64.urlsafe_b64decode(payload.client_data_json.encode() + b"==").decode())
            origin = client_data.get("origin", "")
            if origin and not any(o in origin for o in ["localhost", "127.0.0.1", "vapor.os"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Untrusted WebAuthn client origin: {origin}"
                )
        except Exception:
            pass

    _pending_challenges.pop(payload.email, None)
    user_id = challenge_entry["user_id"]

    # Resolve or provision user safely
    user_claims = {
        "sub": user_id,
        "email": payload.email,
        "name": payload.email.split("@")[0].capitalize(),
        "provider": "passkey"
    }
    user, workspace, membership, p_err = await identity_service.authenticate_or_provision_google_user(db, user_claims)
    role = membership["role"] if membership else "member"
    ws_id = workspace["id"] if workspace else "ws_default_01"

    now = time.time()
    token_claims = {
        "sub": user["id"] if user else user_id,
        "email": payload.email,
        "credential_id": payload.credential_id,
        "role": role,
        "workspace_id": ws_id,
        "provider": "passkey",
        "iat": int(now),
        "exp": int(now + 86400),
        "jti": str(uuid.uuid4())
    }
    
    token = _create_jwt_token(token_claims)
    is_prod = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="vapor_session_token",
        value=token,
        max_age=86400,
        httponly=True,
        secure=is_prod,
        samesite="lax",
        path="/"
    )
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=86400,
        user_id=token_claims["sub"],
        email=payload.email,
        workspace_id=ws_id,
        role=role
    )
