from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vapor OS Core Kernel API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"

    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+asyncpg://vapor_user:vapor_password@localhost:5432/vapor_os"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "super_secret_vapor_kernel_jwt_key_change_in_production_32bytes!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    FAILOVER_TELEMETRY_BUFFER_SECONDS: int = 30
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "openrouter/free"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
