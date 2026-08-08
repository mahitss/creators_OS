from pydantic import BaseModel
from typing import List, Optional

class IntegrationConnectionResponse(BaseModel):
    id: str
    workspace_id: str
    provider: str
    status: str
    scopes: List[str]
    external_account_id: Optional[str] = None
    external_account_name: Optional[str] = None
    connected_at: Optional[str] = None
    last_synced_at: Optional[str] = None
    last_sync_error: Optional[str] = None
    created_at: str
    updated_at: str

class IntegrationListResponse(BaseModel):
    connections: List[IntegrationConnectionResponse]
    total: int

class OAuthConnectUrlResponse(BaseModel):
    authorization_url: str
    state: str
