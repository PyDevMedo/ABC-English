import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.config import settings
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, TelegramLinkToken, TelegramAccount, ParentAccount
)
from app.core.security import generate_telegram_link_code
from app.schemas.schemas import TelegramLinkTokenResponse, TelegramLinkVerify

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["Telegram Integration"])

# Bot instance & Dispatcher initialized lazily for Webhook
_bot = None
_dp = None

def get_bot_and_dp():
    global _bot, _dp
    if _bot is None or _dp is None:
        from aiogram import Bot
        from bot.bot_main import dp, bot as main_bot
        _bot = main_bot if main_bot else Bot(token=settings.TELEGRAM_BOT_TOKEN)
        _dp = dp
    return _bot, _dp

@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Vercel Serverless Webhook Endpoint:
    Receives Telegram updates instantly without polling daemon!
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=400, detail="Telegram bot token not configured")

    try:
        from aiogram.types import Update
        bot, dp = get_bot_and_dp()
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot=bot, update=update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing telegram webhook update: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}

@router.get("/set-webhook")
async def set_telegram_webhook(webhook_url: str):
    """
    Convenient helper to register the Vercel URL with Telegram Bot API:
    Example: GET /api/v1/telegram/set-webhook?webhook_url=https://your-site.vercel.app/api/v1/telegram/webhook
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=400, detail="TELEGRAM_BOT_TOKEN is missing")
    
    import aiohttp
    clean_url = webhook_url.strip()
    tg_api = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook?url={clean_url}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(tg_api) as resp:
            res_data = await resp.json()
            return {
                "configured_url": clean_url,
                "telegram_response": res_data
            }

@router.get("/webhook-info")
async def get_telegram_webhook_info():
    """Check current webhook registration status with Telegram"""
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=400, detail="TELEGRAM_BOT_TOKEN is missing")
    
    import aiohttp
    tg_api = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    async with aiohttp.ClientSession() as session:
        async with session.get(tg_api) as resp:
            return await resp.json()

@router.post("/generate-link-code", response_model=TelegramLinkTokenResponse)
async def generate_link_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate 6-digit temporary linking code valid for 15 minutes"""
    # Invalidate old unused tokens
    old_tokens_q = select(TelegramLinkToken).where(
        and_(TelegramLinkToken.user_id == current_user.id, TelegramLinkToken.is_used == False)
    )
    res = await db.execute(old_tokens_q)
    for t in res.scalars().all():
        t.is_used = True

    # Generate new code
    code = generate_telegram_link_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    token_obj = TelegramLinkToken(
        user_id=current_user.id,
        token=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(token_obj)
    await db.commit()

    return TelegramLinkTokenResponse(
        code=code,
        expires_at=expires_at,
        bot_username=os.getenv("TELEGRAM_BOT_USERNAME", "EnglishJourneyBot")
    )

@router.post("/verify-code")
async def verify_telegram_code(
    payload: TelegramLinkVerify,
    db: AsyncSession = Depends(get_db)
):
    """Used by Telegram Bot when user sends `/link <code>`"""
    now = datetime.utcnow()
    q = select(TelegramLinkToken).where(
        and_(
            TelegramLinkToken.token == payload.code.strip(),
            TelegramLinkToken.is_used == False,
            TelegramLinkToken.expires_at > now
        )
    )
    res = await db.execute(q)
    token_obj = res.scalar_one_or_none()

    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز الربط غير صحيح أو منتهي الصلاحية. يرجى توليد رمز جديد من الموقع."
        )

    # Invalidate token
    token_obj.is_used = True

    # Link Telegram Account
    tg_acc_q = select(TelegramAccount).where(TelegramAccount.telegram_user_id == payload.telegram_user_id)
    tg_acc = (await db.execute(tg_acc_q)).scalar_one_or_none()

    if not tg_acc:
        tg_acc = TelegramAccount(
            telegram_user_id=payload.telegram_user_id,
            telegram_chat_id=payload.telegram_chat_id,
            role=payload.role or "parent",
            username=payload.username,
            full_name=payload.full_name,
            linked_user_id=token_obj.user_id
        )
        db.add(tg_acc)
    else:
        tg_acc.telegram_chat_id = payload.telegram_chat_id
        tg_acc.linked_user_id = token_obj.user_id

    # Update ParentAccount if applicable
    parent_q = select(ParentAccount).where(ParentAccount.user_id == token_obj.user_id)
    parent_acc = (await db.execute(parent_q)).scalar_one_or_none()
    if parent_acc:
        parent_acc.telegram_chat_id = payload.telegram_chat_id

    # Fetch user details
    user_q = select(User).where(User.id == token_obj.user_id)
    user = (await db.execute(user_q)).scalar_one()

    await db.commit()

    return {
        "status": "success",
        "message": f"تم بنجاح ربط حساب Telegram بالطالب: {user.full_name} ({user.student_id})",
        "student_name": user.full_name,
        "student_id": user.student_id
    }
