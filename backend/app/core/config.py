import os
from typing import List, Optional, Union, Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_ROOT_DIR = _BASE_DIR.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[str(_ROOT_DIR / ".env"), str(_BASE_DIR / ".env"), ".env"],
        extra="ignore",
        case_sensitive=False
    )

    PROJECT_NAME: str = "ABC English"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "abc-super-secret-key-children-2026-xyz123")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Database: Supports SQLite (for easy local dev) and PostgreSQL (for production/VPS)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./english_journey.db")
    
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN: Optional[str] = ""
    TELEGRAM_ADMIN_IDS: Any = []

    @field_validator("TELEGRAM_ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any) -> List[int]:
        if isinstance(v, list):
            return [int(x) for x in v if str(x).strip().isdigit()]
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            res = []
            for part in v.split(","):
                part = part.strip()
                if part.isdigit():
                    res.append(int(part))
            return res
        return []
    
    # Storage & Uploads
    UPLOAD_DIR: str = os.path.abspath(os.getenv("UPLOAD_DIR", "./uploads"))
    STATIC_AUDIO_DIR: str = os.path.abspath(os.getenv("STATIC_AUDIO_DIR", "./static/audio"))

    # AI & Pronunciation Evaluation Config
    MIN_PRONUNCIATION_CONFIDENCE: float = 0.40
    NOISY_AUDIO_RMS_THRESHOLD: float = 0.015
    PASSING_SCORE_DEFAULT: int = 80
    WEAKNESS_DETECTION_THRESHOLD: int = 3  # Errors on same phoneme to trigger adaptive path

    # AI External Provider (Optional, defaults to local acoustic + phoneme analysis engine)
    OPENAI_API_KEY: Optional[str] = ""
    ELEVENLABS_API_KEY: Optional[str] = ""

settings = Settings()
