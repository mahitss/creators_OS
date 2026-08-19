from pydantic import BaseModel
from typing import Dict, Any, Optional, Union

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

class WebVitalsPayload(BaseModel):
    name: str
    value: Union[float, int]
    rating: Optional[str] = "good"
    delta: Optional[Union[float, int]] = None
    id: Optional[str] = None
    timestamp: Optional[Union[float, int]] = None
    url: Optional[str] = None
