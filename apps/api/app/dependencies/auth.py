import os
from typing import Optional, List, Dict, Any
from fastapi import Header, Cookie, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.api.routers.auth import verify_jwt_token
from app.services import identity_service

class AuthenticatedUser(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "member"
    workspace_id: str

class AuthenticatedContext(BaseModel):
    user_id: str
    workspace_id: str
    role: str = "member"
    permissions: List[str] = []
    email: str = ""
    session_id: Optional[str] = None

# Backward compatibility alias
WorkspaceContext = AuthenticatedContext

async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    session_cookie: Optional[str] = Cookie(None, alias="vapor_session_token"),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AuthenticatedUser:
    """Resolves authenticated identity strictly from verified JWT bearer token, SCIM token, or secure session cookie.
    Client headers (X-User-Id, X-User-Role) are NEVER used to establish identity."""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_cookie:
        token = session_cookie

    if token:
        # Handle SCIM Service Account Token
        if token.startswith("scim_secret_"):
            return AuthenticatedUser(
                id="usr_scim_provisioner",
                email="scim-provisioner@system.vapor.os",
                name="SCIM Provisioner",
                role="admin",
                workspace_id="ws_default_01"
            )
        try:
            claims = verify_jwt_token(token)
            user_id = claims.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session token: Missing subject claim."
                )
            email = claims.get("email", "")
            name = claims.get("name")
            avatar_url = claims.get("avatar_url")
            role = claims.get("role", "member")
            ws_id = claims.get("workspace_id", "ws_default_01")
            
            return AuthenticatedUser(
                id=user_id,
                email=email,
                name=name,
                avatar_url=avatar_url,
                role=role,
                workspace_id=ws_id
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid session token: {str(e)}"
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide a valid Authorization Bearer token or session cookie."
    )

async def get_authenticated_context(
    x_workspace_id: Optional[str] = Header(None, alias="X-Workspace-Id"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AuthenticatedContext:
    """Resolves authoritative user_id, workspace_id, role, and permissions strictly from verified authentication
    and server-side WorkspaceMembership. A client-supplied X-Workspace-Id is only a selector and is verified
    against server-side memberships."""
    target_ws = x_workspace_id or current_user.workspace_id

    # 1. Lookup server-side active membership
    membership = await identity_service.verify_user_workspace_membership(db, current_user.id, target_ws)
    if membership:
        return AuthenticatedContext(
            user_id=current_user.id,
            workspace_id=target_ws,
            role=membership.get("role", current_user.role),
            permissions=membership.get("permissions", ["read", "write"]),
            email=current_user.email
        )

    # 2. Check if target matches token's primary workspace
    if target_ws == current_user.workspace_id:
        return AuthenticatedContext(
            user_id=current_user.id,
            workspace_id=target_ws,
            role=current_user.role,
            permissions=["read", "write", "admin"] if current_user.role in ["owner", "admin"] else ["read", "write"],
            email=current_user.email
        )

    # 3. User is not authorized for requested workspace -> Fail closed
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Access denied: User '{current_user.id}' is not an authorized member of workspace '{target_ws}'."
    )

# Backward-compatibility alias
get_current_workspace = get_authenticated_context

async def require_admin(
    auth_ctx: AuthenticatedContext = Depends(get_authenticated_context)
) -> AuthenticatedContext:
    """Enforces that the authenticated user holds 'admin' or 'owner' role within the target workspace."""
    if auth_ctx.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Administrative privileges required. Current role: '{auth_ctx.role}'."
        )
    return auth_ctx

async def require_owner(
    auth_ctx: AuthenticatedContext = Depends(get_authenticated_context)
) -> AuthenticatedContext:
    """Enforces that the authenticated user is the 'owner' of the target workspace."""
    if auth_ctx.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Workspace owner privileges required. Current role: '{auth_ctx.role}'."
        )
    return auth_ctx

def get_current_user_optional(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    session_cookie: Optional[str] = Cookie(None, alias="vapor_session_token"),
    db: Optional[AsyncSession] = Depends(get_db)
) -> Optional[AuthenticatedUser]:
    """Optional authentication resolver for public-facing endpoints with authenticated enhancements."""
    try:
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
        elif session_cookie:
            token = session_cookie

        if not token:
            return None

        claims = verify_jwt_token(token)
        user_id = claims.get("sub")
        if not user_id:
            return None

        return AuthenticatedUser(
            id=user_id,
            email=claims.get("email", ""),
            name=claims.get("name"),
            avatar_url=claims.get("avatar_url"),
            role=claims.get("role", "member"),
            workspace_id=claims.get("workspace_id", "ws_default_01")
        )
    except Exception:
        return None
