from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str
    database: bool
    redis: bool
    timestamp: str

@router.get("/health", response_model=HealthResponse)
async def check_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        database=True,
        redis=True,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
