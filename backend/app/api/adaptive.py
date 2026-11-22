from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, PersonalizedLearningPlan, AdaptiveExercise,
    StudentWeakness, Achievement
)

router = APIRouter(prefix="/adaptive", tags=["Adaptive Learning Engine"])

@router.get("/plan")
async def get_my_learning_plan(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students have adaptive learning plans")

    student_id = current_user.student_profile.id
    q = select(PersonalizedLearningPlan).options(
        selectinload(PersonalizedLearningPlan.exercises)
    ).where(
        and_(
            PersonalizedLearningPlan.student_id == student_id,
            PersonalizedLearningPlan.status == "active"
        )
    ).order_by(PersonalizedLearningPlan.id.desc())

    res = await db.execute(q)
    plan = res.scalar_one_or_none()

    if not plan:
        return {"has_plan": False, "message": "أنت متألق يا بطل! لا توجد نقاط ضعف تتطلب تدريبات إضافية حالياً."}

    return {
        "has_plan": True,
        "plan_id": plan.id,
        "current_focus": plan.current_focus,
        "weakness_summary": plan.weakness_summary_json,
        "exercises_count": plan.exercises_count,
        "status": plan.status,
        "exercises": [
            {
                "id": ex.id,
                "skill": ex.skill,
                "difficulty": ex.difficulty,
                "data": ex.exercise_data_json,
                "is_completed": ex.is_completed,
                "score": ex.score
            } for ex in plan.exercises
        ]
    }

@router.post("/exercises/{exercise_id}/complete")
async def complete_adaptive_exercise(
    exercise_id: int,
    score: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can complete exercises")

    student = current_user.student_profile
    ex_q = select(AdaptiveExercise).where(
        and_(AdaptiveExercise.id == exercise_id, AdaptiveExercise.student_id == student.id)
    )
    ex = (await db.execute(ex_q)).scalar_one_or_none()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    ex.is_completed = True
    ex.score = score
    student.xp += 25
    student.stars += 2

    # Check if all exercises in plan completed
    plan_q = select(PersonalizedLearningPlan).options(
        selectinload(PersonalizedLearningPlan.exercises)
    ).where(PersonalizedLearningPlan.id == ex.plan_id)
    plan = (await db.execute(plan_q)).scalar_one()

    all_done = all(e.is_completed for e in plan.exercises)
    plan_completed = False
    if all_done:
        plan.status = "completed"
        plan_completed = True
        # Mark weakness as resolved
        skill = ex.skill
        w_q = select(StudentWeakness).where(
            and_(StudentWeakness.student_id == student.id, StudentWeakness.phoneme_or_skill == skill)
        )
        w_res = await db.execute(w_q)
        weakness = w_res.scalar_one_or_none()
        if weakness:
            weakness.is_resolved = True

        # Award badge
        badge = Achievement(
            student_id=student.id,
            badge_key=f"master_{skill.lower()}",
            badge_title=f"بطل إتقان صوت {skill}",
            badge_icon="award"
        )
        db.add(badge)

    await db.commit()
    return {
        "status": "success",
        "exercise_completed": True,
        "plan_completed": plan_completed,
        "xp_earned": 25,
        "stars_earned": 2,
        "new_total_xp": student.xp
    }
