from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration"""

    # App Info
    APP_NAME: str = "Care Companion API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI Services
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None

    # Google APIs
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Plaid
    PLAID_CLIENT_ID: str
    PLAID_SECRET: str
    PLAID_ENV: str = "sandbox"

    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # URLs
    FRONTEND_URL: str = "http://localhost:3000"

    # Caregiver
    CAREGIVER_EMAIL: Optional[str] = None
    CAREGIVER_PHONE: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
