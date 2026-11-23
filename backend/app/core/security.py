import re
import secrets
import random
import string
import html
import base64
import os
from datetime import datetime, timedelta
from typing import Optional, Any, Tuple, Dict, Set
from jose import jwt, JWTError
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings

# ==============================================================================
# 1. Argon2id Password Hashing Engine (OWASP Recommended Parameters)
# ==============================================================================
# - Type.ID: Argon2id combines Argon2d (data-dependent) and Argon2i (data-independent)
#   providing state-of-the-art resistance to side-channel and GPU cracking attacks.
# - memory_cost=65536 (64 MiB RAM per hash)
# - time_cost=3 (3 iterations)
# - parallelism=4 (4 parallel threads)
# - salt_len=16 (128-bit cryptographically secure random salt generated per hash)
# - hash_len=32 (256-bit derived key)
# ==============================================================================
argon2_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
    type=Type.ID
)

def get_password_hash(password: str) -> str:
    """
    Generate a cryptographically secure Argon2id hash with a unique random salt.
    Never stores or logs the plain text password.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    return argon2_hasher.hash(password)

def verify_and_update_password(plain_password: str, hashed_password: str) -> Tuple[bool, Optional[str]]:
    """
    Verify password against hashed password with transparent migration support:
    1. If hash is Argon2id: verifies and checks if parameter rehash is needed.
    2. If hash is legacy bcrypt ($2b$, $2a$, $2y$): verifies with bcrypt, and on
       success automatically generates a new Argon2id hash for database upgrade.
    3. If hash is legacy plain text: checks equality, and on success generates
       a new Argon2id hash for database upgrade.
    
    Returns:
        (is_valid: bool, new_argon2_hash: Optional[str])
    """
    if not plain_password or not hashed_password:
        return False, None

    # Case 1: Argon2id Hash
    if hashed_password.startswith("$argon2"):
        try:
            argon2_hasher.verify(hashed_password, plain_password)
            # Check if hash parameters need upgrade
            if argon2_hasher.check_needs_rehash(hashed_password):
                return True, argon2_hasher.hash(plain_password)
            return True, None
        except (VerifyMismatchError, VerificationError, InvalidHash):
            return False, None
        except Exception:
            return False, None

    # Case 2: Legacy Bcrypt Hash ($2a$, $2b$, $2y$)
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            pwd_bytes = plain_password.encode("utf-8")[:72]
            hash_bytes = hashed_password.encode("utf-8")
            if bcrypt.checkpw(pwd_bytes, hash_bytes):
                # Transparent upgrade to Argon2id
                new_argon2_hash = argon2_hasher.hash(plain_password)
                return True, new_argon2_hash
            return False, None
        except Exception:
            return False, None

    # Case 3: Legacy Plain Text (Migration Fallback)
    try:
        # Constant-time comparison
        if secrets.compare_digest(plain_password, hashed_password):
            new_argon2_hash = argon2_hasher.hash(plain_password)
            return True, new_argon2_hash
    except Exception:
        pass

    return False, None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simple verification helper returning boolean."""
    is_valid, _ = verify_and_update_password(plain_password, hashed_password)
    return is_valid

# ==============================================================================
# 2. JWT Session Security & Token Revocation
# ==============================================================================
# In-memory thread-safe blacklist for revoked tokens (e.g. logout / session kill)
_REVOKED_TOKENS: Set[str] = set()

def revoke_token(jti: str) -> None:
    """Revoke a token by its unique JWT ID (JTI)."""
    if jti:
        _REVOKED_TOKENS.add(str(jti))

def is_token_revoked(jti: str) -> bool:
    """Check if token JTI has been revoked."""
    return str(jti) in _REVOKED_TOKENS

def create_access_token(
    subject: str | Any,
    role: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate JWT access token with JTI (unique identifier), IAT (issued at),
    and strict expiration.
    """
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    jti = secrets.token_hex(16)
    to_encode: Dict[str, Any] = {
        "exp": expire,
        "iat": now,
        "nbf": now,
        "sub": str(subject),
        "role": role,
        "jti": jti
    }
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT access token, enforcing revocation checks."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        jti = payload.get("jti")
        if jti and is_token_revoked(jti):
            raise JWTError("Token has been revoked")
        return payload
    except JWTError as e:
        raise e

# ==============================================================================
# 3. AES-256-GCM Symmetric Encryption (For Sensitive Secrets at Rest)
# ==============================================================================
def _derive_aes_key(secret_key: Optional[str] = None) -> bytes:
    key_str = secret_key or settings.SECRET_KEY
    import hashlib
    return hashlib.sha256(key_str.encode("utf-8")).digest()

def encrypt_sensitive_data(plain_text: str, secret_key: Optional[str] = None) -> str:
    """
    Encrypt sensitive data using authenticated AES-256-GCM.
    Returns URL-safe base64 string containing nonce + ciphertext + tag.
    """
    if not plain_text:
        return ""
    key = _derive_aes_key(secret_key)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit unique nonce
    ciphertext = aesgcm.encrypt(nonce, plain_text.encode("utf-8"), None)
    payload = nonce + ciphertext
    return base64.urlsafe_b64encode(payload).decode("utf-8")

def decrypt_sensitive_data(encrypted_data: str, secret_key: Optional[str] = None) -> str:
    """Decrypt authenticated AES-256-GCM encrypted string."""
    if not encrypted_data:
        return ""
    key = _derive_aes_key(secret_key)
    aesgcm = AESGCM(key)
    payload = base64.urlsafe_b64decode(encrypted_data.encode("utf-8"))
    nonce = payload[:12]
    ciphertext = payload[12:]
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted_bytes.decode("utf-8")

# ==============================================================================
# 4. Input Sanitization & Validation Helpers
# ==============================================================================
def sanitize_html(text: Optional[str]) -> str:
    """Sanitize user input string against XSS injection."""
    if not text:
        return ""
    return html.escape(str(text).strip(), quote=True)

def validate_tripartite_name(name: str) -> bool:
    """Ensure name has at least 3 parts (first, father, family name)"""
    if not name or not isinstance(name, str):
        return False
    parts = [p.strip() for p in name.strip().split() if len(p.strip()) > 1]
    return len(parts) >= 3

def validate_phone_number(phone: str) -> Optional[str]:
    """Validate and clean phone number (allows standard country/local formats and Arabic digits)"""
    if not phone:
        return None
    # Normalize Arabic/Eastern numerals (٠١٢٣٤٥٦٧٨٩) to standard (0123456789)
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    trans = str.maketrans(arabic_digits + persian_digits, "0123456789" * 2)
    cleaned = str(phone).translate(trans)
    cleaned = re.sub(r'[\s\-\(\)\+]', '', cleaned)
    if not cleaned.isdigit() or len(cleaned) < 8 or len(cleaned) > 15:
        return None
    return cleaned

def generate_student_id() -> str:
    """Generate cryptographically secure unique ID: STU-2026-XXXX"""
    year = datetime.now().year
    alphabet = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    rand_chars = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"STU-{year}-{rand_chars}"

def generate_telegram_link_code() -> str:
    """Generate cryptographically secure 6-digit linking code for Telegram bot"""
    return "".join(secrets.choice("0123456789") for _ in range(6))
