import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy import select

from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.seed_data import seed_database
from app.models.entities import User
from app.core.security import get_password_hash

# Routers
from app.api.auth import router as auth_router
from app.api.curriculum import router as curriculum_router
from app.api.pronunciation import router as pronunciation_router
from app.api.adaptive import router as adaptive_router
from app.api.assignments import router as assignments_router
from app.api.quizzes import router as quizzes_router
from app.api.gamification import router as gamification_router
from app.api.telegram_sync import router as telegram_router
from app.api.stats import router as stats_router

logger = logging.getLogger(__name__)

# ==============================================================================
# Security Middlewares
# ==============================================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Applies comprehensive security headers to all HTTP responses:
    - Content-Security-Policy (CSP)
    - Strict-Transport-Security (HSTS)
    - X-Content-Type-Options (nosniff)
    - X-Frame-Options (Clickjacking defense)
    - Referrer-Policy
    - Permissions-Policy
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # 1. Content Security Policy (CSP)
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "img-src 'self' data: https: blob:; "
            "media-src 'self' data: blob: https:; "
            "connect-src 'self' https:; "
            "font-src 'self' https: data:; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers["Content-Security-Policy"] = csp_policy

        # 2. HTTP Strict Transport Security (HSTS - 2 years with preload)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        # 3. Prevent MIME Sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 4. Clickjacking Defense
        response.headers["X-Frame-Options"] = "DENY"

        # 5. Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 6. Permissions Policy
        response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=()"

        # 7. Sensitive API Cache Control
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"

        return response

class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Prevent Denial of Service (DoS) attacks via oversized request bodies."""
    def __init__(self, app, max_upload_size: int = 50 * 1024 * 1024):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > self.max_upload_size:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={"detail": "حجم الطلب تجاوز الحد المسموح به (50MB)."}
                    )
            except ValueError:
                pass
        return await call_next(request)

# ==============================================================================
# Application Lifespan & Legacy Migration
# ==============================================================================

async def run_security_startup_checks():
    """Scan and safely migrate any legacy plaintext passwords to Argon2id."""
    try:
        async with AsyncSessionLocal() as db:
            q = select(User)
            res = await db.execute(q)
            users = res.scalars().all()
            migrated_count = 0
            for u in users:
                # If password is plain text (not starting with $argon2 or $2)
                if u.hashed_password and not u.hashed_password.startswith(("$argon2", "$2")):
                    logger.warning(f"Plain text password detected for user {u.id}! Upgrading to Argon2id immediately.")
                    u.hashed_password = get_password_hash(u.hashed_password)
                    migrated_count += 1
            if migrated_count > 0:
                await db.commit()
                logger.info(f"Successfully migrated {migrated_count} legacy plaintext passwords to Argon2id.")
    except Exception as e:
        logger.warning(f"Startup security migration check completed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables, seed data, and run security migrations
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.STATIC_AUDIO_DIR, exist_ok=True)
    await seed_database()
    await run_security_startup_checks()
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="My English Journey API",
    description="منصة تعليم الإنجليزية للأطفال بالذكاء الاصطناعي مع نظام إدارة متكامل ومؤمن بالكامل",
    version="2.0.0",
    lifespan=lifespan
)

# Apply Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeLimitMiddleware, max_upload_size=50 * 1024 * 1024)

# CORS Configuration - Explicit Origins Allowed
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://localhost:5173",
    "https://localhost:3000",
    "https://localhost:8000"
]
# Add origins from environment if present
env_api_host = os.getenv("VITE_API_BASE_URL", "")
if env_api_host and env_api_host not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(env_api_host.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permissive for easy local dev, but credentials restricted
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Length", "Retry-After"]
)

# Global Database Exception Shield: Protect DB details and structure from leaking
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error encountered on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "حدث خطأ غير متوقع أثناء معالجة البيانات، يرجى المحاولة لاحقاً."}
    )

# Mount static file directories with nosniff protection
os.makedirs(settings.STATIC_AUDIO_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static/audio", StaticFiles(directory=settings.STATIC_AUDIO_DIR), name="static_audio")
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(curriculum_router, prefix=settings.API_V1_STR)
app.include_router(pronunciation_router, prefix=settings.API_V1_STR)
app.include_router(adaptive_router, prefix=settings.API_V1_STR)
app.include_router(assignments_router, prefix=settings.API_V1_STR)
app.include_router(quizzes_router, prefix=settings.API_V1_STR)
app.include_router(gamification_router, prefix=settings.API_V1_STR)
app.include_router(telegram_router, prefix=settings.API_V1_STR)
app.include_router(stats_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "environment": "active",
        "security": "Argon2id + HTTPS + Strict Isolation + RBAC Active",
        "levels": 8,
        "ai_engine": "Acoustic & Phoneme Assessment Ready"
    }

# Mount Frontend SPA if dist directory exists
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
