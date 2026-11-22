from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, Quiz, QuizQuestion, QuizResult,
    StudentLevelAccess, Achievement, Certificate, Level
)
from app.schemas.schemas import QuizSubmitRequest, QuizResultResponse

router = APIRouter(prefix="/quizzes", tags=["Quizzes & Exams"])

@router.get("/{level_id}")
async def get_level_quiz(
    level_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    q = select(Quiz).options(
        selectinload(Quiz.questions)
    ).where(Quiz.level_id == level_id)
    res = await db.execute(q)
    quiz = res.scalar_one_or_none()

    if not quiz:
        raise HTTPException(status_code=404, detail="No quiz configured for this level")

    return {
        "id": quiz.id,
        "title": quiz.title,
        "passing_score": quiz.passing_score,
        "time_limit_minutes": quiz.time_limit_minutes,
        "questions": [
            {
                "id": q.id,
                "question_type": q.question_type,
                "question_text": q.question_text,
                "audio_url": q.audio_url,
                "image_url": q.image_url,
                "options": q.options_json
            } for q in quiz.questions
        ]
    }

@router.post("/submit", response_model=QuizResultResponse)
async def submit_quiz(
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can submit quizzes")

    student = current_user.student_profile
    q = select(Quiz).options(
        selectinload(Quiz.questions)
    ).where(Quiz.id == payload.quiz_id)
    res = await db.execute(q)
    quiz = res.scalar_one_or_none()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct_count = 0
    total_count = len(quiz.questions)
    details = {}

    for question in quiz.questions:
        q_id_str = str(question.id)
        child_ans = payload.answers.get(q_id_str, "")
        is_corr = str(child_ans).strip().lower() == str(question.correct_answer).strip().lower()
        if is_corr:
            correct_count += 1
        details[q_id_str] = {
            "question": question.question_text,
            "child_answer": child_ans,
            "correct_answer": question.correct_answer,
            "is_correct": is_corr
        }

    score = int((correct_count / max(1, total_count)) * 100)
    passed = score >= quiz.passing_score
    level_unlocked = False

    # Save quiz result
    result = QuizResult(
        quiz_id=quiz.id,
        student_id=student.id,
        score=score,
        passed=passed,
        details_json=details
    )
    db.add(result)

    if passed:
        student.xp += 50
        student.stars += 5

        # Unlock next level if currently at this level
        next_lvl_num = quiz.level_id + 1
        if next_lvl_num <= 8:
            next_lvl_q = select(Level).where(Level.level_number == next_lvl_num)
            next_lvl = (await db.execute(next_lvl_q)).scalar_one_or_none()
            if next_lvl:
                # Check if access exists
                acc_q = select(StudentLevelAccess).where(
                    and_(StudentLevelAccess.student_id == student.id, StudentLevelAccess.level_id == next_lvl.id)
                )
                acc = (await db.execute(acc_q)).scalar_one_or_none()
                if not acc:
                    acc = StudentLevelAccess(
                        student_id=student.id,
                        level_id=next_lvl.id,
                        is_unlocked=True,
                        unlocked_by="quiz_pass"
                    )
                    db.add(acc)
                else:
                    acc.is_unlocked = True
                student.current_level_id = next_lvl_num
                level_unlocked = True

        # Issue Certificate if completed Level 8
        if quiz.level_id == 8:
            cert = Certificate(
                student_id=student.id,
                level_id=8,
                certificate_number=f"CERT-{student.id}-8-{datetime.utcnow().strftime('%Y%m%d')}"
            )
            db.add(cert)

        # Issue achievement
        badge = Achievement(
            student_id=student.id,
            badge_key=f"passed_level_{quiz.level_id}",
            badge_title=f"خريج المستوى {quiz.level_id}",
            badge_icon="trophy"
        )
        db.add(badge)

    await db.commit()

    return QuizResultResponse(
        quiz_id=quiz.id,
        score=score,
        passed=passed,
        passing_score=quiz.passing_score,
        correct_count=correct_count,
        total_count=total_count,
        level_unlocked=level_unlocked,
        details=details
    )
