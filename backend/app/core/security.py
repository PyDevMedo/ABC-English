import re
import secrets
import random
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def create_access_token(subject: str | Any, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def validate_tripartite_name(name: str) -> bool:
    """Ensure name has at least 3 parts (first, father, family name)"""
    if not name or not isinstance(name, str):
        return False
    parts = [p.strip() for p in name.strip().split() if len(p.strip()) > 1]
    return len(parts) >= 3

def validate_phone_number(phone: str) -> Optional[str]:
    """Validate and clean phone number (allows standard country/local formats)"""
    if not phone:
        return None
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    if not cleaned.isdigit() or len(cleaned) < 8 or len(cleaned) > 15:
        return None
    return cleaned

def generate_student_id() -> str:
    """Generate professional unique ID: STU-2026-XXXX"""
    year = datetime.now().year
    rand_chars = "".join(random.choices("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ", k=4))
    return f"STU-{year}-{rand_chars}"

def generate_telegram_link_code() -> str:
    """Generate 6-digit linking code for Telegram bot"""
    return "".join(random.choices("0123456789", k=6))
