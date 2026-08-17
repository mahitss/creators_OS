from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.crypto import sign_event_payload

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900

class PasskeyRegisterRequest(BaseModel):
    email: EmailStr
    credential_id: str

@router.post("/auth/passkey/verify", response_model=TokenResponse)
async def verify_passkey(payload: PasskeyRegisterRequest) -> TokenResponse:
    if not payload.email or not payload.credential_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid passkey credential signature."
        )
    token = sign_event_payload(f"{payload.email}:{payload.credential_id}")
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=900
    )

