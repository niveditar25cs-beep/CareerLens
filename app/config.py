import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "CareerLens")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./careerlens.db")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # External APIs
    SCRAPER_BASE_URL: str = os.getenv("SCRAPER_BASE_URL", "")
    NOTIFICATION_API_KEY: str = os.getenv("NOTIFICATION_API_KEY", "")


settings = Settings()
