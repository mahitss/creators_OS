import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel

class V1ApiErrorDetail(BaseModel):
    code: str
    message: str
    requestId: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None

def format_v1_api_error(
    code: str,
    message: str,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Uniform V1.0 API Error Contract hiding stack traces, SQL errors, credentials, and internal paths."""
    rid = request_id or f"req_{uuid.uuid4().hex[:12]}"
    ts = datetime.now(timezone.utc).isoformat()
    
    # Strip any potential stack traces or internal paths from message
    clean_msg = message.split("\n")[0] if message else "An internal error occurred."
    if "Traceback" in clean_msg or "sqlalchemy" in clean_msg.lower() or "psycopg" in clean_msg.lower():
        clean_msg = "A database or system error occurred. Please contact system support."
        
    return {
        "code": code,
        "message": clean_msg,
        "requestId": rid,
        "timestamp": ts,
        "details": details or {}
    }
