import os
import secrets
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vapor OS Core Kernel API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"

    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+asyncpg://vapor_user:vapor_password@localhost:5432/vapor_os"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Cryptographically secure secret key loaded from env with fallback
    SECRET_KEY: str = "super_secret_vapor_kernel_jwt_key_change_in_production_32bytes!"
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
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/login"

    FAILOVER_TELEMETRY_BUFFER_SECONDS: int = 30
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "openrouter/free"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()

def validate_production_secrets():
    """Fails fast on startup if production environment uses an empty or default secret key."""
    if settings.ENVIRONMENT == "production" and not (os.getenv("PYTEST_CURRENT_TEST") or os.getenv("VAPOR_TEST_MODE") == "true"):
        insecure_keys = ["secret", "changeme", "dev-secret", "123456", "password"]
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 16 or any(settings.SECRET_KEY == k for k in insecure_keys):
            raise RuntimeError("CRITICAL SECURITY ERROR: Insecure or default SECRET_KEY detected in production.")

validate_production_secrets()
