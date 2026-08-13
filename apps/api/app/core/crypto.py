import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet
from app.core.config import settings

def _get_fernet_key() -> bytes:
    # Hash settings.SECRET_KEY to get a reliable 32-byte key for Fernet
    key_bytes = settings.SECRET_KEY.encode('utf-8')
    digest = hashlib.sha256(key_bytes).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_secret(plaintext: Optional[str]) -> Optional[str]:
    if not plaintext:
        return None
    f = Fernet(_get_fernet_key())
    encrypted = f.encrypt(plaintext.encode('utf-8'))
    return encrypted.decode('utf-8')

def decrypt_secret(ciphertext: Optional[str]) -> Optional[str]:
    if not ciphertext:
        return None
    try:
        f = Fernet(_get_fernet_key())
        decrypted = f.decrypt(ciphertext.encode('utf-8'))
        return decrypted.decode('utf-8')
    except Exception:
        return None

def sign_event_payload(payload: str) -> str:
    """Generates dual-digest HMAC-SHA512 + HMAC-SHA256 hybrid event signature (Priority #6)."""
    import hmac
    secret_bytes = settings.SECRET_KEY.encode('utf-8')
    payload_bytes = payload.encode('utf-8')
    h256 = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
    h512 = hmac.new(secret_bytes, payload_bytes, hashlib.sha512).hexdigest()
    return f"v1:hybrid:{h256[:16]}:{h512}"

def verify_event_signature(payload: str, signature: str) -> bool:
    """Verifies dual-digest hybrid event signature against payload content (Priority #6)."""
    if not signature or not signature.startswith("v1:hybrid:"):
        return False
    expected = sign_event_payload(payload)
    import hmac
    return hmac.compare_digest(expected, signature)

