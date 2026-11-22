import random
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
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

    all_questions = list(quiz.questions)
    if not all_questions:
        raise HTTPException(status_code=404, detail="No questions available for this quiz")

    # Group questions by pedagogical question_type / category to guarantee diverse coverage:
    # 1) listen_select (Minimal pairs audio discrimination)
    # 2) word_match (Semantic nuances)
    # 3) fill_blank (Contextual grammar & vocab in sentences)
    # 4) phoneme_or_dialogue (Conversational mastery / Phonics)
    by_type = defaultdict(list)
    for q_obj in all_questions:
        by_type[q_obj.question_type].append(q_obj)

    selected_questions: List[QuizQuestion] = []
    # Pick 1 random variant from each present category
    for q_type, q_list in by_type.items():
        if q_list:
            selected_questions.append(random.choice(q_list))

    # If fewer than 4 categories were found, fill up to 4 distinct questions
    if len(selected_questions) < 4:
        remaining = [q for q in all_questions if q not in selected_questions]
        random.shuffle(remaining)
        needed = min(4 - len(selected_questions), len(remaining))
        selected_questions.extend(remaining[:needed])

    # If total selected is more than 4, take up to 4
    if len(selected_questions) > 4:
        selected_questions = selected_questions[:4]

    # Format questions and shuffle options so options aren't in predictable order
    formatted_questions = []
    for q_item in selected_questions:
        raw_options = list(q_item.options_json) if isinstance(q_item.options_json, list) else []
        # Randomize options order on each attempt
        shuffled_options = list(raw_options)
        random.shuffle(shuffled_options)

        formatted_questions.append({
            "id": q_item.id,
            "question_type": q_item.question_type,
            "question_text": q_item.question_text,
            "audio_url": q_item.audio_url,
            "audio_text": q_item.correct_answer if (q_item.audio_url or q_item.question_type == "listen_select") else None,
            "image_url": q_item.image_url,
            "options": shuffled_options
        })

    return {
        "id": quiz.id,
        "title": quiz.title,
        "passing_score": quiz.passing_score,
        "time_limit_minutes": quiz.time_limit_minutes,
        "questions": formatted_questions
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
    # Evaluate only the questions the student actually answered in this attempt
    submitted_q_ids = set()
    for k in payload.answers.keys():
        try:
            submitted_q_ids.add(int(k))
        except (ValueError, TypeError):
            continue

    # Filter to questions that belong to this quiz and were included in the student's attempt
    attempt_questions = [q for q in quiz.questions if q.id in submitted_q_ids]
    
    # If for any reason no matching IDs were found (e.g. empty submission), default to all questions
    if not attempt_questions:
        attempt_questions = quiz.questions

    total_count = len(attempt_questions)
    details = {}

    for question in attempt_questions:
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

        # Unlock next level if currently at this level and XP requirement is fulfilled
        from app.services.xp_service import get_xp_required_for_level
        next_lvl_num = quiz.level_id + 1
        if next_lvl_num <= 50:
            xp_required_for_next = get_xp_required_for_level(next_lvl_num)
            if student.xp >= xp_required_for_next:
                next_lvl_q = select(Level).where(Level.level_number == next_lvl_num)
                next_lvl = (await db.execute(next_lvl_q)).scalar_one_or_none()
                if next_lvl:
                    acc_q = select(StudentLevelAccess).where(
                        and_(StudentLevelAccess.student_id == student.id, StudentLevelAccess.level_id == next_lvl.id)
                    )
                    acc = (await db.execute(acc_q)).scalar_one_or_none()
                    if not acc:
                        acc = StudentLevelAccess(
                            student_id=student.id,
                            level_id=next_lvl.id,
                            is_unlocked=True,
                            unlocked_by="quiz_and_xp"
                        )
                        db.add(acc)
                    else:
                        acc.is_unlocked = True
                    student.current_level_id = next_lvl_num
                    level_unlocked = True

        # Issue Certificate if completed milestone Level 15 or Level 50
        if quiz.level_id in [15, 50]:
            cert = Certificate(
                student_id=student.id,
                level_id=quiz.level_id,
                certificate_number=f"CERT-{student.id}-{quiz.level_id}-{datetime.utcnow().strftime('%Y%m%d')}"
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
