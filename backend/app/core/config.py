from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "SEO Analyzer Tool"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./seo_analyzer.db"

    # API Keys
    GOOGLE_API_KEY: str = ""
    PAGESPEED_API_KEY: str = ""
    GEMINI_API_KEY: str = ""  # Google Gemini API for LLM analysis

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS - Will be split by comma if provided as string
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost,http://localhost:80")

    class Config:
        case_sensitive = True

    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list"""
        # Force read from environment variable
        origins = os.getenv("ALLOWED_ORIGINS", self.ALLOWED_ORIGINS)
        if isinstance(origins, str):
            return [origin.strip() for origin in origins.split(',')]
        return origins


settings = Settings()
