from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import require_admin, WorkspaceContext
from app.schemas.identity import SCIMUserCreate, SCIMUserRead, SCIMGroupCreate, SCIMGroupRead
from app.services import identity_service

router = APIRouter(prefix="/scim/v2", tags=["scim"])

@router.get("/Users")
async def list_scim_users(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 GET /Users endpoint."""
    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 1,
        "startIndex": 1,
        "itemsPerPage": 50,
        "Resources": [
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
                "id": "scim_usr_01",
                "userName": "executive@company.com",
                "active": True,
                "emails": [{"value": "executive@company.com", "primary": True}]
            }
        ]
    }

@router.post("/Users", status_code=201)
async def create_scim_user(
    scim_in: SCIMUserCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 POST /Users endpoint for user provisioning."""
    return await identity_service.scim_create_user(session, ws_ctx.workspace_id, scim_in)

@router.delete("/Users/{user_id}", status_code=200)
async def delete_scim_user(
    user_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 DELETE/Deactivation endpoint. Revokes sessions and pauses automations."""
    return await identity_service.scim_deprovision_user(session, ws_ctx.workspace_id, user_id)

@router.get("/Groups")
async def list_scim_groups(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 GET /Groups endpoint."""
    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": 1,
        "startIndex": 1,
        "itemsPerPage": 50,
        "Resources": [
            {
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
                "id": "scim_grp_01",
                "displayName": "vapor-security-admins",
                "members": []
            }
        ]
    }
