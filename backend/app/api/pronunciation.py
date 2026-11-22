import os
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.entities import User, StudentProfile, PronunciationAttempt, Level
from app.schemas.schemas import PronunciationAssessmentResponse
from app.services.pronunciation_service import evaluate_pronunciation
from app.services.adaptive_engine import process_adaptive_learning
from app.services.telegram_notifier import notify_ai_teacher_alert

router = APIRouter(prefix="/pronunciation", tags=["AI Pronunciation Assessment"])

@router.post("/evaluate", response_model=PronunciationAssessmentResponse)
async def evaluate_child_pronunciation(
    target_text: str = Form(...),
    audio_file: Optional[UploadFile] = File(None),
    simulated_speech: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can perform pronunciation assessments")

    student = current_user.student_profile
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    saved_filepath = ""
    if audio_file:
        file_ext = audio_file.filename.split(".")[-1] if "." in audio_file.filename else "wav"
        filename = f"rec_{student.id}_{uuid.uuid4().hex[:8]}.{file_ext}"
        saved_filepath = os.path.join(settings.UPLOAD_DIR, filename)
        content = await audio_file.read()
        with open(saved_filepath, "wb") as f:
            f.write(content)
    else:
        # Default empty audio path if using simulated test
        saved_filepath = os.path.join(settings.UPLOAD_DIR, f"sim_{uuid.uuid4().hex[:8]}.wav")
        with open(saved_filepath, "wb") as f:
            f.write(b"RIFF....WAVEfmt ....data....") # Mock wav header

    # Run AI Pronunciation & Phoneme Evaluation
    eval_result = evaluate_pronunciation(
        audio_path=saved_filepath,
        target_text=target_text,
        simulated_speech=simulated_speech
    )

    # Check for adaptive learning trigger if phoneme error
    adaptive_triggered = False
    weakness_detected = None
    if eval_result["error_phonemes"]:
        triggered, skill, plan = await process_adaptive_learning(
            db=db,
            student_id=student.id,
            error_phonemes=eval_result["error_phonemes"]
        )
        if triggered and plan:
            adaptive_triggered = True
            weakness_detected = skill
            # Dispatch Telegram alert to teachers
            lvl_name = f"Level {student.current_level_id}"
            await notify_ai_teacher_alert(
                student_name=current_user.full_name,
                student_id_str=current_user.student_id or str(current_user.id),
                level_name=lvl_name,
                skill=skill,
                error_count=plan.weakness_summary_json.get("error_count", 3),
                total_trials=plan.weakness_summary_json.get("total_trials", 5),
                notes=f"الطفل يحتاج إلى تعزيز صوت {skill}. قام الذكاء الاصطناعي بإنشاء {plan.exercises_count} تدريبات خاصة."
            )

    # Award XP & Stars if not needing retry
    xp_earned = 0
    stars_earned = 0
    if not eval_result["needs_retry"]:
        xp_earned = 20 if eval_result["overall_score"] >= 80 else 10
        stars_earned = 2 if eval_result["overall_score"] >= 80 else 1
        student.xp += xp_earned
        student.stars += stars_earned

    # Save Pronunciation Attempt
    attempt = PronunciationAttempt(
        student_id=student.id,
        target_text=target_text,
        target_phonemes="-".join(eval_result.get("correct_phonemes", []) + eval_result.get("error_phonemes", [])),
        audio_path=saved_filepath,
        overall_score=eval_result["overall_score"],
        phoneme_accuracy=eval_result["phoneme_accuracy"],
        clarity_score=eval_result["clarity_score"],
        recognized_text=eval_result["recognized_text"],
        correct_phonemes_json=eval_result["correct_phonemes"],
        error_phonemes_json=eval_result["error_phonemes"],
        feedback_text=eval_result["feedback_text"],
        confidence=eval_result["confidence"]
    )
    db.add(attempt)
    await db.commit()

    return PronunciationAssessmentResponse(
        attempt_id=attempt.id,
        overall_score=eval_result["overall_score"],
        phoneme_accuracy=eval_result["phoneme_accuracy"],
        clarity_score=eval_result["clarity_score"],
        recognized_text=eval_result["recognized_text"],
        target_text=target_text,
        correct_phonemes=eval_result["correct_phonemes"],
        error_phonemes=eval_result["error_phonemes"],
        feedback_text=eval_result["feedback_text"],
        audio_quality=eval_result["audio_quality"],
        needs_retry=eval_result["needs_retry"],
        adaptive_triggered=adaptive_triggered,
        weakness_detected=weakness_detected,
        xp_earned=xp_earned,
        stars_earned=stars_earned
    )
