from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, Level, Lesson, LessonSection, Word,
    StudentLevelAccess, LessonProgress
)
from app.schemas.schemas import LevelSchema, LessonSchema, WordSchema

router = APIRouter(prefix="/curriculum", tags=["Curriculum & Levels"])

@router.get("/levels", response_model=List[LevelSchema])
async def get_levels(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Fetch all 8 levels
    levels_q = select(Level).order_by(Level.level_number)
    levels_res = await db.execute(levels_q)
    all_levels = levels_res.scalars().all()

    # Get student accesses if student
    unlocked_level_ids = set()
    completed_lesson_ids = set()

    if current_user.role == "student" and current_user.student_profile:
        student_id = current_user.student_profile.id
        access_q = select(StudentLevelAccess).where(
            and_(StudentLevelAccess.student_id == student_id, StudentLevelAccess.is_unlocked == True)
        )
        access_res = await db.execute(access_q)
        unlocked_level_ids = {a.level_id for a in access_res.scalars().all()}

        # Level 1 always unlocked by default
        unlocked_level_ids.add(1)

        prog_q = select(LessonProgress.lesson_id).where(
            and_(LessonProgress.student_id == student_id, LessonProgress.is_completed == True)
        )
        prog_res = await db.execute(prog_q)
        completed_lesson_ids = set(prog_res.scalars().all())
    else:
        # Teachers / Admins see all levels unlocked
        unlocked_level_ids = {lvl.id for lvl in all_levels}

    result = []
    for lvl in all_levels:
        is_unlocked = (lvl.id in unlocked_level_ids) or (lvl.level_number == 1)
        result.append(LevelSchema(
            id=lvl.id,
            level_number=lvl.level_number,
            title=lvl.title,
            subtitle=lvl.subtitle,
            description=lvl.description,
            icon=lvl.icon,
            is_unlocked=is_unlocked,
            progress_percentage=100 if is_unlocked and lvl.level_number < 2 else (25 if is_unlocked else 0),
            min_passing_score=lvl.min_passing_score,
            lessons=[]
        ))

    return result

@router.get("/levels/{level_id}", response_model=LevelSchema)
async def get_level_detail(
    level_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    level_q = select(Level).options(
        selectinload(Level.lessons).selectinload(Lesson.sections)
    ).where(Level.id == level_id)
    level_res = await db.execute(level_q)
    level = level_res.scalar_one_or_none()

    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    is_unlocked = True
    if current_user.role == "student" and current_user.student_profile:
        student_id = current_user.student_profile.id
        if level.level_number > 1:
            access_q = select(StudentLevelAccess).where(
                and_(StudentLevelAccess.student_id == student_id, StudentLevelAccess.level_id == level_id, StudentLevelAccess.is_unlocked == True)
            )
            access = (await db.execute(access_q)).scalar_one_or_none()
            if not access:
                is_unlocked = False

    if not is_unlocked and current_user.role == "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا المستوى مقفول حالياً. يرجى إتمام متطلبات واختبار المستوى السابق أولاً."
        )

    return LevelSchema(
        id=level.id,
        level_number=level.level_number,
        title=level.title,
        subtitle=level.subtitle,
        description=level.description,
        icon=level.icon,
        is_unlocked=True,
        progress_percentage=0,
        min_passing_score=level.min_passing_score,
        lessons=[
            LessonSchema(
                id=l.id,
                level_id=l.level_id,
                lesson_number=l.lesson_number,
                title=l.title,
                description=l.description,
                order_index=l.order_index,
                sections=[
                    {
                        "id": s.id,
                        "section_type": s.section_type,
                        "title_ar": s.title_ar,
                        "title_en": s.title_en,
                        "content_json": s.content_json,
                        "audio_url": s.audio_url,
                        "order_index": s.order_index
                    } for s in l.sections
                ]
            ) for l in level.lessons
        ]
    )

@router.get("/words/{level_id}", response_model=List[WordSchema])
async def get_level_words(
    level_id: int,
    db: AsyncSession = Depends(get_db)
):
    words_q = select(Word).where(Word.level_id == level_id)
    res = await db.execute(words_q)
    return res.scalars().all()

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can track progress")

    student = current_user.student_profile
    prog_q = select(LessonProgress).where(
        and_(LessonProgress.student_id == student.id, LessonProgress.lesson_id == lesson_id)
    )
    prog = (await db.execute(prog_q)).scalar_one_or_none()

    if not prog:
        prog = LessonProgress(
            student_id=student.id,
            lesson_id=lesson_id,
            is_completed=True,
            score=100
        )
        db.add(prog)
        # Award XP & Stars
        student.xp += 30
        student.stars += 3
        await db.commit()

    return {"status": "success", "xp_earned": 30, "stars_earned": 3, "total_xp": student.xp, "total_stars": student.stars}
