import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
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

router = APIRouter(prefix="/telegram", tags=["Telegram Integration"])

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
