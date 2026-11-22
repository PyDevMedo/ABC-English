import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My English Journey"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "english-journey-super-secret-key-children-2026-xyz123")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Database: Supports SQLite (for easy local dev) and PostgreSQL (for production/VPS)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./english_journey.db")
    
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_ADMIN_IDS: List[int] = [int(x.strip()) for x in os.getenv("TELEGRAM_ADMIN_IDS", "").split(",") if x.strip().isdigit()]
    
    # Storage & Uploads
    UPLOAD_DIR: str = os.path.abspath(os.getenv("UPLOAD_DIR", "./uploads"))
    STATIC_AUDIO_DIR: str = os.path.abspath(os.getenv("STATIC_AUDIO_DIR", "./static/audio"))

    # AI & Pronunciation Evaluation Config
    MIN_PRONUNCIATION_CONFIDENCE: float = 0.40
    NOISY_AUDIO_RMS_THRESHOLD: float = 0.015
    PASSING_SCORE_DEFAULT: int = 80
    WEAKNESS_DETECTION_THRESHOLD: int = 3  # Errors on same phoneme to trigger adaptive path

    # AI External Provider (Optional, defaults to local acoustic + phoneme analysis engine)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY", "")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
