from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class IdentityProviderCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    type: str  # oidc, saml, google, azure_ad, okta, auth0
    name: str
    configuration: Dict[str, Any] = Field(default_factory=dict)

class IdentityProviderRead(BaseModel):
    id: str
    organization_id: str
    type: str
    name: str
    status: str  # draft, active, disabled, error, deleted
    configuration_summary: Dict[str, Any]
    created_by: str
    created_at: datetime
    updated_at: datetime

class VerifiedDomainCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    domain: str

class VerifiedDomainRead(BaseModel):
    id: str
    organization_id: str
    domain: str
    status: str  # pending, verified, failed
    verification_token: str
    verified_at: Optional[datetime] = None
    created_at: datetime

class GroupMappingCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    external_group: str = Field(..., alias="externalGroup")
    role: str = "member"
    scope: str = "organization"

class GroupMappingRead(BaseModel):
    id: str
    organization_id: str
    external_group: str
    role: str
    scope: str
    status: str
    created_at: datetime

class ServiceAccountCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    name: str
    scopes: List[str] = Field(default_factory=lambda: ["workspace.read", "workflow.run"])

class ServiceAccountRead(BaseModel):
    id: str
    organization_id: str
    name: str
    status: str
    owner_id: str
    created_at: datetime
    expires_at: Optional[datetime] = None

class ServiceAccountTokenIssued(BaseModel):
    token_id: str
    raw_token: str  # Only returned ONCE upon creation
    scopes: List[str]
    created_at: datetime

# SCIM 2.0 Schemas
class SCIMUserEmail(BaseModel):
    value: str
    type: str = "work"
    primary: bool = True

class SCIMUserName(BaseModel):
    formatted: Optional[str] = None
    familyName: Optional[str] = None
    givenName: Optional[str] = None

class SCIMUserCreate(BaseModel):
    userName: str
    name: Optional[SCIMUserName] = None
    emails: List[SCIMUserEmail]
    active: bool = True
    externalId: Optional[str] = None

class SCIMUserRead(BaseModel):
    schemas: List[str] = ["urn:ietf:params:scim:schemas:core:2.0:User"]
    id: str
    userName: str
    name: Optional[SCIMUserName] = None
    emails: List[SCIMUserEmail]
    active: bool
    externalId: Optional[str] = None

class SCIMGroupCreate(BaseModel):
    displayName: str
    externalId: Optional[str] = None
    members: List[Dict[str, Any]] = Field(default_factory=list)

class SCIMGroupRead(BaseModel):
    schemas: List[str] = ["urn:ietf:params:scim:schemas:core:2.0:Group"]
    id: str
    displayName: str
    externalId: Optional[str] = None
    members: List[Dict[str, Any]] = Field(default_factory=list)
