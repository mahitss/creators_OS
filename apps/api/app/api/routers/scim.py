from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.identity import SCIMUserCreate, SCIMUserRead, SCIMGroupCreate, SCIMGroupRead
from app.services import identity_service

router = APIRouter(prefix="/scim/v2", tags=["scim"])

@router.get("/Users")
async def list_scim_users(
    authorization: str = Header(..., alias="Authorization"),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 GET /Users endpoint."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized SCIM Access")
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
    authorization: str = Header(..., alias="Authorization"),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 POST /Users endpoint for user provisioning."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized SCIM Access")
    return await identity_service.scim_create_user(session, "org_default_creator", scim_in)

@router.delete("/Users/{user_id}", status_code=200)
async def delete_scim_user(
    user_id: str,
    authorization: str = Header(..., alias="Authorization"),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 DELETE/Deactivation endpoint. Revokes sessions and pauses automations."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized SCIM Access")
    return await identity_service.scim_deprovision_user(session, "org_default_creator", user_id)

@router.get("/Groups")
async def list_scim_groups(
    authorization: str = Header(..., alias="Authorization"),
    session: AsyncSession = Depends(get_db)
):
    """SCIM 2.0 GET /Groups endpoint."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized SCIM Access")
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
