from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, Achievement, Certificate, LessonProgress,
    PronunciationAttempt, StudentWeakness, Level
)

router = APIRouter(prefix="/gamification", tags=["Gamification & Achievements"])

@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students have gamification dashboards")

    student = current_user.student_profile

    # Fetch achievements
    ach_q = select(Achievement).where(Achievement.student_id == student.id)
    achievements = (await db.execute(ach_q)).scalars().all()

    # Fetch certificates
    cert_q = select(Certificate).options(selectinload(Certificate.level)).where(Certificate.student_id == student.id)
    certificates = (await db.execute(cert_q)).scalars().all()

    # Count completed lessons
    completed_lessons = await db.scalar(
        select(LessonProgress.id).where(
            and_(LessonProgress.student_id == student.id, LessonProgress.is_completed == True)
        )
    )

    # Fetch mastered & needs review skills
    weaknesses_q = select(StudentWeakness).where(StudentWeakness.student_id == student.id)
    weaknesses = (await db.execute(weaknesses_q)).scalars().all()

    mastered = [w.phoneme_or_skill for w in weaknesses if w.is_resolved]
    needs_review = [w.phoneme_or_skill for w in weaknesses if not w.is_resolved]

    # If new student, provide starter skills
    if not mastered and not needs_review:
        mastered = ["Letter Sounds S, A, T", "Listening & Recognition"]

    from app.services.xp_service import get_next_level_requirements
    xp_info = get_next_level_requirements(student.current_level_id, student.xp)

    return {
        "xp": student.xp,
        "stars": student.stars,
        "streak_days": student.streak_days,
        "current_level_id": student.current_level_id,
        "avatar": student.avatar,
        "xp_progress": xp_info,
        "completed_lessons_count": 1 if completed_lessons else 0,
        "mastered_skills": mastered,
        "needs_review_skills": needs_review,
        "achievements": [
            {
                "id": a.id,
                "key": a.badge_key,
                "title": a.badge_title,
                "icon": a.badge_icon,
                "earned_at": a.earned_at
            } for a in achievements
        ],
        "certificates": [
            {
                "id": c.id,
                "certificate_number": c.certificate_number,
                "level_title": c.level.title if c.level else "Level 8 Final",
                "issue_date": c.issue_date
            } for c in certificates
        ]
    }
