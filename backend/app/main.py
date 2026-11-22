import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base
from app.seed_data import seed_database

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables and seed initial data
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.STATIC_AUDIO_DIR, exist_ok=True)
    await seed_database()
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="My English Journey API",
    description="منصة تعليم الإنجليزية للأطفال بالذكاء الاصطناعي مع نظام إدارة متكامل عبر Telegram",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories
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
