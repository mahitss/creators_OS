from pydantic import BaseModel
from typing import Dict, Any

class ServiceHealthStatus(BaseModel):
    database: bool
    redis: bool

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    services: ServiceHealthStatus
    timestamp: str
    details: Dict[str, Any] = {}
