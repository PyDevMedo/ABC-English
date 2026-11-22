import os
import uuid
import asyncio
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

from app.core.config import settings
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, Assignment, AssignmentSubmission, AssignmentFeedback,
    StudentLevelAccess, LessonProgress, Level
)
from app.schemas.schemas import AssignmentCreate, AssignmentFeedbackCreate
from app.services.telegram_notifier import notify_assignment_submission

router = APIRouter(prefix="/assignments", tags=["Assignments & Homework"])

@router.get("/my-submissions")
async def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all handwriting homework requests/submissions made by the logged-in student"""
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can view homework submissions")

    q = select(AssignmentSubmission).options(
        selectinload(AssignmentSubmission.assignment).selectinload(Assignment.level),
        selectinload(AssignmentSubmission.feedback)
    ).where(
        AssignmentSubmission.student_id == current_user.student_profile.id
    ).order_by(AssignmentSubmission.id.desc())

    subs = (await db.execute(q)).scalars().all()

    results = []
    for s in subs:
        lvl_num = s.assignment.level.level_number if (s.assignment and s.assignment.level) else (s.assignment.level_id if s.assignment else 1)
        results.append({
            "id": s.id,
            "assignment_id": s.assignment_id,
            "level_number": lvl_num,
            "title": s.assignment.title if s.assignment else f"واجب المستوى {lvl_num}",
            "instructions_ar": s.assignment.instructions_ar if s.assignment else "",
            "submission_type": s.submission_type,
            "image_url": s.image_url,
            "audio_url": s.audio_url,
            "status": s.status, # submitted, graded, needs_retry
            "submitted_at": s.submitted_at.strftime("%Y-%m-%d %H:%M") if s.submitted_at else "الآن",
            "score": s.feedback.score if s.feedback else None,
            "comments": s.feedback.comments if s.feedback else None,
            "retry_requested": s.feedback.retry_requested if s.feedback else False,
            "reviewed_at": s.feedback.reviewed_at.strftime("%Y-%m-%d %H:%M") if (s.feedback and s.feedback.reviewed_at) else None
        })
    return results

@router.get("/by-level/{level_id}")
async def get_level_handwriting_assignment(
    level_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the mandatory handwriting assignment for a specific level"""
    q = select(Assignment).where(Assignment.level_id == level_id).order_by(Assignment.id.desc())
    res = await db.execute(q)
    assignment = res.scalars().first()

    if not assignment:
        # Fallback default assignment data if not seeded
        return {
            "id": level_id,
            "title": f"واجب كتابة وتثبيت كلمات المستوى {level_id}",
            "instructions_ar": "اكتب الكلمات والحروف في كراسة اللغة الإنجليزية بخط جميل ومرتب، ثم التقط صورة لدفترك وارفعها هنا لتفتح الدرس التالي!",
            "target_words": ["Sat", "Sit", "Pin"] if level_id == 1 else ["Cat", "Dog", "Sun"],
            "target_sentences": ["I sit.", "A pin."] if level_id == 1 else ["A cat and a dog."],
            "is_submitted": False
        }

    # Check if student submitted this assignment
    sub = None
    if current_user.student_profile:
        sub_q = select(AssignmentSubmission).where(
            and_(
                AssignmentSubmission.assignment_id == assignment.id,
                AssignmentSubmission.student_id == current_user.student_profile.id
            )
        )
        sub = (await db.execute(sub_q)).scalar_one_or_none()

    return {
        "id": assignment.id,
        "title": assignment.title,
        "instructions_ar": assignment.instructions_ar,
        "target_words": assignment.target_words_json,
        "target_sentences": assignment.target_sentences_json,
        "is_submitted": sub is not None,
        "submission_status": sub.status if sub else None,
        "image_url": sub.image_url if sub else None
    }

@router.get("/")
async def get_assignments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role == "student" and current_user.student_profile:
        level_id = current_user.student_profile.current_level_id
        q = select(Assignment).options(
            selectinload(Assignment.submissions)
        ).where(Assignment.level_id <= level_id).order_by(Assignment.id.desc())
        res = await db.execute(q)
        assignments = res.scalars().all()

        results = []
        for a in assignments:
            # Check if this student has submitted
            my_sub = next((s for s in a.submissions if s.student_id == current_user.student_profile.id), None)
            results.append({
                "id": a.id,
                "title": a.title,
                "description": a.description,
                "instructions_ar": a.instructions_ar,
                "assignment_type": a.assignment_type,
                "target_words": a.target_words_json,
                "target_sentences": a.target_sentences_json,
                "due_date": a.due_date,
                "status": my_sub.status if my_sub else "not_started",
                "score": my_sub.feedback.score if (my_sub and my_sub.feedback) else None,
                "feedback": my_sub.feedback.comments if (my_sub and my_sub.feedback) else None
            })
        return results
    else:
        # Teachers and Admins get all
        q = select(Assignment).order_by(Assignment.id.desc())
        res = await db.execute(q)
        return res.scalars().all()

@router.post("/submit")
async def submit_assignment(
    assignment_id: int = Form(...),
    submission_type: str = Form("audio"),
    text_content: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can submit homework")

    student = current_user.student_profile
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    audio_url = None
    if audio_file:
        ext = audio_file.filename.split(".")[-1] if "." in audio_file.filename else "mp3"
        fname = f"hw_aud_{student.id}_{uuid.uuid4().hex[:8]}.{ext}"
        fpath = os.path.join(settings.UPLOAD_DIR, fname)
        content = await audio_file.read()
        with open(fpath, "wb") as f:
            f.write(content)
        audio_url = f"/uploads/{fname}"

    image_url = None
    image_fpath = None
    if image_file:
        ext = image_file.filename.split(".")[-1] if "." in image_file.filename else "jpg"
        fname = f"hw_img_{student.id}_{uuid.uuid4().hex[:8]}.{ext}"
        image_fpath = os.path.join(settings.UPLOAD_DIR, fname)
        content = await image_file.read()
        with open(image_fpath, "wb") as f:
            f.write(content)
        image_url = f"/uploads/{fname}"

    # Check existing submission
    q = select(AssignmentSubmission).where(
        and_(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student.id
        )
    )
    res = await db.execute(q)
    existing_sub = res.scalar_one_or_none()

    if existing_sub:
        existing_sub.submission_type = submission_type
        existing_sub.text_content = text_content or existing_sub.text_content
        if audio_url:
            existing_sub.audio_url = audio_url
        if image_url:
            existing_sub.image_url = image_url
        existing_sub.status = "submitted"
        existing_sub.submitted_at = datetime.utcnow()
        sub_id = existing_sub.id
    else:
        new_sub = AssignmentSubmission(
            assignment_id=assignment_id,
            student_id=student.id,
            submission_type=submission_type,
            text_content=text_content,
            audio_url=audio_url,
            image_url=image_url,
            status="submitted",
            submitted_at=datetime.utcnow()
        )
        db.add(new_sub)
        await db.flush()
        sub_id = new_sub.id

    student.xp += 25
    student.stars += 2

    # Get assignment and unlock next level if needed
    asg_q = select(Assignment).where(Assignment.id == assignment_id)
    asg = (await db.execute(asg_q)).scalar_one_or_none()
    title = asg.title if asg else "Handwriting Homework"

    if asg:
        next_lvl = asg.level_id + 1
        if next_lvl <= 50:
            acc_q = select(StudentLevelAccess).where(
                and_(StudentLevelAccess.student_id == student.id, StudentLevelAccess.level_id == next_lvl)
            )
            acc = (await db.execute(acc_q)).scalar_one_or_none()
            if not acc:
                acc = StudentLevelAccess(
                    student_id=student.id,
                    level_id=next_lvl,
                    is_unlocked=True,
                    unlocked_by="homework_submission"
                )
                db.add(acc)
            else:
                acc.is_unlocked = True

    await db.commit()

    # Notify Telegram bot admins with the student's notebook photo in background!
    try:
        asyncio.create_task(notify_assignment_submission(
            student_name=current_user.full_name,
            student_id_str=current_user.student_id or str(current_user.id),
            assignment_title=title,
            submission_id=sub_id,
            photo_path=image_fpath
        ))
    except Exception as e:
        logger.warning(f"Failed to dispatch telegram assignment notification: {e}")

    return {
        "status": "success",
        "message": "تم تسليم واجب الكتابة الورقية بنجاح، ووصلت صورة الدفتر للمعلم عبر Telegram! وتم فتح المرحلة التالية 🌟",
        "xp_earned": 25,
        "submission_id": sub_id,
        "image_url": image_url,
        "next_unlocked": True
    }
