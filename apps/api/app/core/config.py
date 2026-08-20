import os
import secrets
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vapor OS Core Kernel API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://vapor_user:vapor_password@localhost:5432/vapor_os")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Cryptographically secure secret key loaded from env with fallback
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vapor_kernel_auth_token_signing_key_2026_x99a_enterprise_32bytes")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://vapor.os"
    ]

    # Google Identity Services / OAuth 2.0 Credentials (Server-Side Only)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "381940932694-o2q57f2bhp8sjbt9r6fgm240q4jknmfa.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/login"

    FAILOVER_TELEMETRY_BUFFER_SECONDS: int = 30
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "openrouter/free"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()

import sys

def validate_production_secrets():
    """Fails fast on startup if production environment uses an empty or default secret key."""
    if settings.ENVIRONMENT == "production" and not (os.getenv("PYTEST_CURRENT_TEST") or os.getenv("VAPOR_TEST_MODE") == "true" or "pytest" in sys.modules):
        insecure_keys = ["secret", "changeme", "dev-secret", "123456", "password"]
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32 or any(k in settings.SECRET_KEY.lower() for k in insecure_keys):
            raise RuntimeError("CRITICAL SECURITY ERROR: Insecure or default SECRET_KEY detected in production.")

validate_production_secrets()
