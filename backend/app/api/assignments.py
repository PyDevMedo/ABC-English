import os
import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import (
    User, StudentProfile, Assignment, AssignmentSubmission, AssignmentFeedback
)
from app.schemas.schemas import AssignmentCreate, AssignmentFeedbackCreate
from app.services.telegram_notifier import notify_assignment_submission

router = APIRouter(prefix="/assignments", tags=["Assignments & Homework"])

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
    if image_file:
        ext = image_file.filename.split(".")[-1] if "." in image_file.filename else "jpg"
        fname = f"hw_img_{student.id}_{uuid.uuid4().hex[:8]}.{ext}"
        fpath = os.path.join(settings.UPLOAD_DIR, fname)
        content = await image_file.read()
        with open(fpath, "wb") as f:
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

    student.xp += 15
    student.stars += 1
    await db.commit()

    # Get assignment title
    asg_q = select(Assignment).where(Assignment.id == assignment_id)
    asg = (await db.execute(asg_q)).scalar_one_or_none()
    title = asg.title if asg else "Homework"

    # Notify Telegram bot admins
    await notify_assignment_submission(
        student_name=current_user.full_name,
        student_id_str=current_user.student_id or str(current_user.id),
        assignment_title=title,
        submission_id=sub_id
    )

    return {
        "status": "success",
        "message": "تم تسليم الواجب بنجاح وإشعار المعلم! أحسنت يا بطل 🌟",
        "xp_earned": 15,
        "submission_id": sub_id
    }
