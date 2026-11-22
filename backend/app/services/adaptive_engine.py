import json
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.entities import (
    StudentProfile, StudentWeakness, PersonalizedLearningPlan,
    AdaptiveExercise, TeacherReport, PronunciationAttempt, User
)

SKILL_EXERCISE_TEMPLATES = {
    "SH": {
        "title": "إتقان الصوت السحري SH",
        "description": "تدريبات مخصصة لعلاج صعوبة نطق صوت /ʃ/ والتمييز بينه وبين الأصوات المشابهة",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "الاستماع لصوت SH الهادئ",
                "instruction_en": "Listen to the quiet sound: shhhhh",
                "instruction_ar": "ضع إصبعك على شفتيك واستمع إلى صوت الهدوء shhhhh",
                "target_sound": "SH",
                "target_words": ["Ship", "Shop", "Fish"],
                "audio_text": "shhhhh, like in ship, shop, and fish"
            },
            {
                "step_number": 2,
                "title_ar": "التمييز بين SH و S",
                "instruction_en": "Listen and spot the difference between /s/ and /sh/",
                "instruction_ar": "اسمع الفرق بين صوت الثعبان ssss وصوت الهدوء shhhh",
                "target_sound": "SH vs S",
                "target_words": ["Sit", "Ship", "Sun", "Shop"],
                "audio_text": "Sit starts with sss, Ship starts with shhh"
            },
            {
                "step_number": 3,
                "title_ar": "نطق وتكرار كلمات مميزة",
                "instruction_en": "Repeat after the teacher: Ship, Shop, Fish",
                "instruction_ar": "ردد وراء المعلم وسجل صوتك بوضوح",
                "target_sound": "SH",
                "target_words": ["Ship", "Shop", "Fish"],
                "sample_sentence": "The ship is big.",
                "audio_text": "Ship, Shop, Fish. The ship is big."
            },
            {
                "step_number": 4,
                "title_ar": "اختبار التحدي وإعادة التقييم",
                "instruction_en": "Pronounce the sentence: I see a ship in the shop.",
                "instruction_ar": "اقرأ الجملة كاملة وسجل صوتك لتحصل على نجمتك الذهبية!",
                "target_sound": "SH",
                "target_words": ["Ship", "Shop"],
                "sample_sentence": "I see a ship in the shop.",
                "audio_text": "I see a ship in the shop."
            }
        ]
    },
    "CH": {
        "title": "إتقان صوت القطار CH",
        "description": "تدريبات مكثفة على صوت /tʃ/ والفرق بينه وبين صوت SH",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "الاستماع لصوت قطار البخار تش تش",
                "instruction_en": "Listen to the train sound: ch-ch-choo",
                "instruction_ar": "اسمع صوت قطار البخار تش تش ch-ch",
                "target_sound": "CH",
                "target_words": ["Chip", "Chat", "Chin"],
                "audio_text": "ch-ch-choo, chip, chat"
            },
            {
                "step_number": 2,
                "title_ar": "نطق وتكرار كلمات CH",
                "instruction_en": "Say: Chip and Chat",
                "instruction_ar": "ردد وسجل صوتك: Chip ثم Chat",
                "target_sound": "CH",
                "target_words": ["Chip", "Chat"],
                "sample_sentence": "I chat with mom.",
                "audio_text": "I chat with mom."
            }
        ]
    },
    "TH": {
        "title": "إتقان إخراج اللسان مع صوت TH",
        "description": "تدريب على وضع اللسان بين الأسنان لصوت /θ/ و /ð/",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "إخراج طرف اللسان مع TH",
                "instruction_en": "Put your tongue between your teeth: th-th-thin",
                "instruction_ar": "أخرج طرف لسانك الصغير وانطق th-th-thin",
                "target_sound": "TH",
                "target_words": ["Thin", "This", "That"],
                "audio_text": "th-th-thin, this is a thin cat"
            }
        ]
    },
    "SHORT_VOWELS": {
        "title": "التمييز بين الحركات القصيرة A, E, I, O, U",
        "description": "تدريبات لضبط الحركات القصيرة ومنع الخلط بينها في الكلمات الثلاثية",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "الاستماع ومقارنة الكلمات",
                "instruction_en": "Compare: Bat, Bed, Bit, Bug",
                "instruction_ar": "اسمع الفرق بين الحركات القصيرة المختلفة",
                "target_sound": "Vowels",
                "target_words": ["Pan", "Pen", "Pin"],
                "audio_text": "Pan, Pen, Pin. Listen closely!"
            }
        ]
    }
}

async def process_adaptive_learning(
    db: AsyncSession,
    student_id: int,
    error_phonemes: List[str]
) -> Tuple[bool, Optional[str], Optional[PersonalizedLearningPlan]]:
    """
    Checks student history for recurring phoneme errors.
    If recurrence threshold (>= 3 errors) is reached:
    1. Updates StudentWeakness record
    2. Automatically generates a Personalized Learning Plan
    3. Creates progressive Adaptive Exercises
    4. Queues a Teacher Report for Telegram notification
    """
    if not error_phonemes:
        return False, None, None

    # Track target phoneme
    target_phoneme = error_phonemes[0].upper()
    if target_phoneme in ["SH", "CH", "TH"]:
        skill_key = target_phoneme
    elif target_phoneme in ["AE", "EH", "IH", "AA", "AH", "A", "E", "I", "O", "U"]:
        skill_key = "SHORT_VOWELS"
    else:
        skill_key = target_phoneme

    # Check weakness in database
    q = select(StudentWeakness).where(
        and_(
            StudentWeakness.student_id == student_id,
            StudentWeakness.phoneme_or_skill == skill_key,
            StudentWeakness.is_resolved == False
        )
    )
    result = await db.execute(q)
    weakness = result.scalar_one_or_none()

    if weakness:
        weakness.error_count += 1
        weakness.total_trials += 1
        weakness.last_detected_at = datetime.utcnow()
        if weakness.error_count >= 5:
            weakness.severity = "high"
        elif weakness.error_count >= 3:
            weakness.severity = "medium"
    else:
        weakness = StudentWeakness(
            student_id=student_id,
            phoneme_or_skill=skill_key,
            error_count=1,
            total_trials=1,
            severity="low"
        )
        db.add(weakness)

    await db.flush()

    # Trigger adaptive plan if errors >= 3
    if weakness.error_count >= 3:
        # Check if an active plan already exists for this skill
        plan_q = select(PersonalizedLearningPlan).where(
            and_(
                PersonalizedLearningPlan.student_id == student_id,
                PersonalizedLearningPlan.current_focus.like(f"%{skill_key}%"),
                PersonalizedLearningPlan.status == "active"
            )
        )
        existing_plan_res = await db.execute(plan_q)
        existing_plan = existing_plan_res.scalar_one_or_none()

        if not existing_plan:
            template = SKILL_EXERCISE_TEMPLATES.get(skill_key, SKILL_EXERCISE_TEMPLATES["SH"])
            
            new_plan = PersonalizedLearningPlan(
                student_id=student_id,
                current_focus=f"إتقان مهارة {skill_key} ({template['title']})",
                weakness_summary_json={
                    "skill": skill_key,
                    "error_count": weakness.error_count,
                    "total_trials": weakness.total_trials,
                    "severity": weakness.severity,
                    "detected_at": datetime.utcnow().isoformat()
                },
                exercises_count=len(template["steps"]),
                status="active"
            )
            db.add(new_plan)
            await db.flush()

            # Create individual adaptive exercises
            for step in template["steps"]:
                exercise = AdaptiveExercise(
                    plan_id=new_plan.id,
                    student_id=student_id,
                    skill=skill_key,
                    difficulty="easy" if step["step_number"] <= 2 else "medium",
                    exercise_data_json=step,
                    is_completed=False,
                    score=0
                )
                db.add(exercise)

            # Create Teacher Report for Telegram notification
            # Get student name
            stu_q = select(StudentProfile, User).join(User, StudentProfile.user_id == User.id).where(StudentProfile.id == student_id)
            stu_res = await db.execute(stu_q)
            row = stu_res.first()
            student_name = row[1].full_name if row else f"Student #{student_id}"

            teacher_report = TeacherReport(
                student_id=student_id,
                report_type="weakness_alert",
                title=f"⚠️ تنبيه المدرس الذكي: ضعف متكرر في نطق ({skill_key})",
                content=(
                    f"الطالب: {student_name}\n"
                    f"المهارة: {skill_key} Pronunciation\n"
                    f"عدد الأخطاء: {weakness.error_count} من آخر {weakness.total_trials} محاولات.\n"
                    f"ملاحظة المدرس الذكي: الطالب يواجه صعوبة متكررة في نطق {skill_key}، "
                    f"وتم تلقائياً إنشاء خطة تدريبية تتضمن {len(template['steps'])} تدريبات تفاعلية متدرجة."
                ),
                recommended_action=f"اعتماد الخطة التدريبية المقترحة لمراجعة صوت {skill_key}",
                status="sent"
            )
            db.add(teacher_report)
            await db.commit()
            return True, skill_key, new_plan

    await db.commit()
    return False, None, None
