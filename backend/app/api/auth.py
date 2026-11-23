import asyncio
import logging
from datetime import datetime, timedelta
from typing import Annotated, Optional

logger = logging.getLogger(__name__)
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from jose import JWTError

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    verify_password, verify_and_update_password, get_password_hash,
    create_access_token, decode_access_token, revoke_token,
    validate_tripartite_name, validate_phone_number, generate_student_id, sanitize_html
)
from app.core.rate_limiter import limiter
from app.models.entities import User, StudentProfile, StudentLevelAccess, ActivityLog
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse
from app.services.telegram_notifier import notify_admins_new_student

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="تعذر التحقق من صحة الجلسة، يرجى تسجيل الدخول مجدداً.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    # Parameterized query with eager loading of student profile
    q = select(User).options(selectinload(User.student_profile)).where(User.id == user_id)
    result = await db.execute(q)
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserRegister,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    client_ip = limiter.get_client_ip(request)
    # 0. General Rate limit check
    await limiter.check_general_rate_limit(client_ip, limit=15, window_seconds=60)

    # 1. Validate Tripartite Name
    clean_name = sanitize_html(user_in.full_name)
    if not validate_tripartite_name(clean_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب إدخال الاسم الثلاثي كاملاً للطفل (مثال: محمد أحمد علي)"
        )

    # 2. Validate Phone Number
    clean_phone = validate_phone_number(user_in.phone_number)
    if not clean_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم الهاتف غير صالح، يرجى إدخال رقم هاتف صحيح"
        )

    # 3. Check for duplicates using parameterized query
    existing = await db.execute(select(User).where(User.phone_number == clean_phone))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم الهاتف مسجل بالفعل مسبقاً، يرجى تسجيل الدخول أو استخدام رقم آخر"
        )

    # 4. Generate unique Student ID
    student_id_str = generate_student_id()
    while True:
        dup = await db.execute(select(User).where(User.student_id == student_id_str))
        if not dup.scalar_one_or_none():
            break
        student_id_str = generate_student_id()

    # 5. Create User with Argon2id Password Hash
    argon2_hash = get_password_hash(user_in.password)
    new_user = User(
        student_id=student_id_str,
        full_name=clean_name,
        phone_number=clean_phone,
        hashed_password=argon2_hash,
        role=user_in.role or "student",
        is_active=True
    )
    db.add(new_user)
    await db.flush()

    # 6. Create Student Profile if role is student
    if new_user.role == "student":
        student_profile = StudentProfile(
            user_id=new_user.id,
            current_level_id=1,
            xp=50, # Initial welcome bonus
            stars=5,
            streak_days=1,
            avatar=user_in.avatar or "lion"
        )
        db.add(student_profile)
        await db.flush()

        # Unlock Level 1 automatically
        unlock = StudentLevelAccess(
            student_id=student_profile.id,
            level_id=1,
            is_unlocked=True,
            unlocked_by="system"
        )
        db.add(unlock)

    # 7. Audit Log
    log = ActivityLog(
        user_id=new_user.id,
        action="user_registered",
        details_json={"role": new_user.role, "student_id": student_id_str},
        ip_address=client_ip
    )
    db.add(log)
    await db.commit()

    # 8. Notify Telegram Bot Admins in background
    reg_date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    try:
        asyncio.create_task(notify_admins_new_student(
            student_id_str=student_id_str,
            full_name=new_user.full_name,
            phone_number=new_user.phone_number,
            registration_date=reg_date_str,
            level_num=1,
            is_active=new_user.is_active
        ))
    except Exception as e:
        logger.warning(f"Could not dispatch telegram notification task: {e}")

    return UserResponse(
        id=new_user.id,
        student_id=new_user.student_id,
        full_name=new_user.full_name,
        phone_number=new_user.phone_number,
        role=new_user.role,
        is_active=new_user.is_active,
        created_at=new_user.created_at,
        avatar=user_in.avatar or "lion",
        xp=50,
        stars=5,
        streak_days=1,
        current_level_id=1
    )

@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    client_ip = limiter.get_client_ip(request)
    clean_phone = validate_phone_number(credentials.phone_number)
    lookup_key = clean_phone or str(credentials.phone_number).strip()

    # 1. Enforce Rate Limiting & Brute Force Lockout with progressive delay
    await limiter.check_login_rate_limit(client_ip, lookup_key)

    if not clean_phone:
        await limiter.record_failed_login(client_ip, lookup_key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="خطأ في رقم الهاتف أو خطأ في كلمة المرور: بيانات الدخول غير صحيحة، يرجى التأكد من الرقم وكلمة المرور."
        )

    # 2. Parameterized Query for User
    q = select(User).where(User.phone_number == clean_phone)
    res = await db.execute(q)
    user = res.scalar_one_or_none()

    # 3. Password Verification with Argon2id and Transparent Migration
    is_valid = False
    new_hash_to_save: Optional[str] = None
    if user:
        is_valid, new_hash_to_save = verify_and_update_password(
            credentials.password,
            user.hashed_password
        )

    if not user or not is_valid:
        # Record failed attempt and apply lockout/delay counter
        await limiter.record_failed_login(client_ip, lookup_key)
        # Log failed attempt without leaking password
        audit_log = ActivityLog(
            user_id=user.id if user else None,
            action="login_failed",
            details_json={"phone_attempt": clean_phone[:4] + "****" if len(clean_phone) > 4 else "****"},
            ip_address=client_ip
        )
        db.add(audit_log)
        await db.commit()

        # Uniform security message protecting against User Enumeration while maintaining compatibility
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="خطأ في رقم الهاتف أو خطأ في كلمة المرور: بيانات الدخول غير صحيحة، يرجى التأكد من الرقم وكلمة المرور."
        )

    # 4. Check if Account is Active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا الحساب موقوف حالياً من قبل الإدارة. يرجى التواصل مع المعلم."
        )

    # 5. Transparent Argon2id Migration if user had older bcrypt/plain text hash
    if new_hash_to_save:
        user.hashed_password = new_hash_to_save
        user.updated_at = datetime.utcnow()
        logger.info(f"User {user.id} password hash successfully upgraded to Argon2id.")

    # 6. Reset Rate Limiter for this client
    await limiter.record_successful_login(client_ip, lookup_key)

    # 7. Generate Secure JWT Token with JTI
    access_token = create_access_token(subject=user.id, role=user.role)

    # 8. Set Secure Cookie with HttpOnly, Secure, SameSite
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True, # Enforce HTTPS transmission
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    # 9. Audit Log
    log = ActivityLog(
        user_id=user.id,
        action="login_success",
        details_json={"role": user.role},
        ip_address=client_ip
    )
    db.add(log)
    await db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        student_id=user.student_id,
        full_name=user.full_name
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    client_ip = limiter.get_client_ip(request)
    clean_phone = validate_phone_number(form_data.username) or form_data.username.strip()

    await limiter.check_login_rate_limit(client_ip, clean_phone)

    q = select(User).where((User.phone_number == clean_phone) | (User.student_id == form_data.username.strip()))
    res = await db.execute(q)
    user = res.scalar_one_or_none()

    is_valid = False
    new_hash_to_save = None
    if user:
        is_valid, new_hash_to_save = verify_and_update_password(
            form_data.password,
            user.hashed_password
        )

    if not user or not is_valid:
        await limiter.record_failed_login(client_ip, clean_phone)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is suspended."
        )

    if new_hash_to_save:
        user.hashed_password = new_hash_to_save
        user.updated_at = datetime.utcnow()

    await limiter.record_successful_login(client_ip, clean_phone)
    access_token = create_access_token(subject=user.id, role=user.role)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        student_id=user.student_id,
        full_name=user.full_name
    )

@router.post("/logout")
async def logout(
    response: Response,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """Secure logout: revokes current token and clears session cookies."""
    try:
        payload = decode_access_token(token)
        jti = payload.get("jti")
        if jti:
            revoke_token(jti)
    except Exception:
        pass

    response.delete_cookie(key="access_token")
    return {"status": "success", "message": "تم تسجيل الخروج بنجاح وإلغاء صلاحية الجلسة."}

@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    phone_number: str
):
    """
    Password reset request.
    Security: Never reveals whether the phone number is registered or not (User Enumeration Defense).
    """
    clean_phone = validate_phone_number(phone_number)
    # Generic uniform response
    return {
        "status": "success",
        "message": "إذا كان رقم الهاتف مسجلاً في المنصة، فسيتم إرسال تعليمات إعادة التعيين عبر Telegram أو رسالة خاصة."
    }

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Strict Account Data Isolation: Only accesses current authenticated user profile
    profile_q = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    prof_res = await db.execute(profile_q)
    profile = prof_res.scalar_one_or_none()

    return UserResponse(
        id=current_user.id,
        student_id=current_user.student_id,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        avatar=profile.avatar if profile else "lion",
        xp=profile.xp if profile else 0,
        stars=profile.stars if profile else 0,
        streak_days=profile.streak_days if profile else 1,
        current_level_id=profile.current_level_id if profile else 1
    )
