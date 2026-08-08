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
