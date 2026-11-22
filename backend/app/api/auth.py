from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from jose import jwt, JWTError

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    validate_tripartite_name, validate_phone_number, generate_student_id
)
from app.models.entities import User, StudentProfile, StudentLevelAccess, ActivityLog
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse
from app.services.telegram_notifier import notify_admins_new_student

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    q = select(User).options(selectinload(User.student_profile)).where(User.id == user_id)
    result = await db.execute(q)
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    # 1. Validate Tripartite Name (Must have at least 3 parts, e.g. "محمد أحمد علي")
    if not validate_tripartite_name(user_in.full_name):
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

    # 3. Check for duplicates
    existing = await db.execute(select(User).where(User.phone_number == clean_phone))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم الهاتف مسجل بالفعل مسبقاً، يرجى تسجيل الدخول أو استخدام رقم آخر"
        )

    # 4. Generate unique Student ID
    student_id_str = generate_student_id()
    # Ensure uniqueness
    while True:
        dup = await db.execute(select(User).where(User.student_id == student_id_str))
        if not dup.scalar_one_or_none():
            break
        student_id_str = generate_student_id()

    # 5. Create User
    new_user = User(
        student_id=student_id_str,
        full_name=user_in.full_name.strip(),
        phone_number=clean_phone,
        hashed_password=get_password_hash(user_in.password),
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

    # Log activity
    log = ActivityLog(user_id=new_user.id, action="user_registered", details_json={"role": new_user.role})
    db.add(log)
    await db.commit()

    # 7. Notify Telegram Bot Admins asynchronously
    reg_date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    await notify_admins_new_student(
        student_id_str=student_id_str,
        full_name=new_user.full_name,
        phone_number=new_user.phone_number,
        registration_date=reg_date_str,
        level_num=1,
        is_active=new_user.is_active
    )

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
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    clean_phone = validate_phone_number(credentials.phone_number)
    if not clean_phone:
        raise HTTPException(status_code=400, detail="رقم الهاتف غير صالح")

    q = select(User).where(User.phone_number == clean_phone)
    res = await db.execute(q)
    user = res.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رقم الهاتف أو كلمة المرور غير صحيحة"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا الحساب موقوف حالياً من قبل الإدارة. يرجى التواصل مع المعلم."
        )

    access_token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        student_id=user.student_id,
        full_name=user.full_name
    )

# OAuth2 standard compatibility form login
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    clean_phone = validate_phone_number(form_data.username)
    if not clean_phone:
        clean_phone = form_data.username

    q = select(User).where((User.phone_number == clean_phone) | (User.student_id == form_data.username))
    res = await db.execute(q)
    user = res.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        student_id=user.student_id,
        full_name=user.full_name
    )

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
