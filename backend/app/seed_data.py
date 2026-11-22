import asyncio
from datetime import datetime
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import get_password_hash, generate_student_id
from app.models.entities import (
    User, StudentProfile, TeacherAccount, Level, Lesson, LessonSection,
    Word, Phoneme, Quiz, QuizQuestion, StudentLevelAccess, SystemSetting, Assignment
)
from app.services.phonics_curriculum import CURRICULUM_DATA

async def seed_database():
    print("Initializing Database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        levels_count = await db.scalar(select(Level.id))
        if levels_count is not None:
            print("Database already seeded with curriculum.")
            return

        print("Seeding 8 Levels and Phonics Curriculum...")
        # 1. Seed Levels and Lessons
        for item in CURRICULUM_DATA:
            level = Level(
                level_number=item["level_number"],
                title=item["title"],
                subtitle=item["subtitle"],
                description=item["description"],
                icon=item["icon"],
                min_passing_score=80,
                is_active=True
            )
            db.add(level)
            await db.flush()

            # Add Primary Lesson for this level
            lesson = Lesson(
                level_id=level.id,
                lesson_number=1,
                title=f"Lesson 1: {item['subtitle']}",
                description=item["description"],
                order_index=1
            )
            db.add(lesson)
            await db.flush()

            # Add Lesson Sections:
            # Section 1: Intro in Arabic
            s_intro = LessonSection(
                lesson_id=lesson.id,
                section_type="intro",
                title_ar="المقدمة والقصة المشوقة",
                title_en="Welcome & Introduction",
                content_json={"text_ar": item["intro_ar"]},
                order_index=1
            )
            # Section 2: Letters & Phonics Exploration
            s_phonics = LessonSection(
                lesson_id=lesson.id,
                section_type="phonics",
                title_ar="أصوات الحروف السحرية",
                title_en="Letters & Sounds Exploration",
                content_json={"letters": item["letters"]},
                order_index=2
            )
            # Section 3: Word Blending
            s_words = LessonSection(
                lesson_id=lesson.id,
                section_type="words",
                title_ar="دمج وقراءة الكلمات",
                title_en="Word Blending & Reading",
                content_json={"words": item["words"]},
                order_index=3
            )
            # Section 4: Sentences & Sight Words
            s_sentences = LessonSection(
                lesson_id=lesson.id,
                section_type="sentences",
                title_ar="قراءة الجمل والكلمات البصرية",
                title_en="Sentences & Sight Words",
                content_json={
                    "sentences": item["sentences"],
                    "sight_words": item["sight_words"]
                },
                order_index=4
            )
            # Section 5: AI Pronunciation Practice
            s_pronunciation = LessonSection(
                lesson_id=lesson.id,
                section_type="pronunciation",
                title_ar="مختبر النطق مع المدرس الذكي",
                title_en="AI Pronunciation Lab",
                content_json={
                    "practice_words": [w["word"] for w in item["words"]],
                    "practice_sentences": [s["text"] for s in item["sentences"]]
                },
                order_index=5
            )

            db.add_all([s_intro, s_phonics, s_words, s_sentences, s_pronunciation])

            # Seed Words table
            for w in item["words"]:
                word_obj = Word(
                    level_id=level.id,
                    lesson_id=lesson.id,
                    word=w["word"],
                    phonemes_breakdown=w["phonemes"],
                    translation_ar=w["translation_ar"],
                    image_url=w.get("image"),
                    audio_url=f"/static/audio/{w['word'].lower()}.mp3",
                    is_sight_word=False
                )
                db.add(word_obj)

            # Seed Sight Words
            for sw in item["sight_words"]:
                sw_obj = Word(
                    level_id=level.id,
                    lesson_id=lesson.id,
                    word=sw,
                    phonemes_breakdown=sw,
                    translation_ar="كلمة بصرية",
                    is_sight_word=True
                )
                db.add(sw_obj)

            # Seed Mandatory Handwriting Assignment
            hw_words = [w["word"] for w in item["words"][:4]]
            hw_sentences = [s["text"] for s in item["sentences"][:2]]
            hw_instructions = (
                f"اكتب في كراسة اللغة الإنجليزية الكلمات التالية بخط جميل ومرتب: "
                f"({', '.join(hw_words)}) وجملة: ({hw_sentences[0] if hw_sentences else ''})، "
                f"ثم التقط صورة واضحة للدفتر وارفعها هنا لاعتماد الواجب وفتح المرحلة التالية!"
            )
            assignment = Assignment(
                level_id=level.id,
                title=f"واجب كتابة وتثبيت كلمات {item['title']}",
                description=f"كتابة حروف وكلمات {item['subtitle']} في كراسة الإنجليزية وتصوير الصفحة.",
                instructions_ar=hw_instructions,
                assignment_type="handwriting_photo",
                target_words_json=hw_words,
                target_sentences_json=hw_sentences
            )
            db.add(assignment)

            # Seed Level Quiz
            quiz = Quiz(
                level_id=level.id,
                lesson_id=lesson.id,
                title=f"اختبار إتقان {item['title']}",
                passing_score=80,
                time_limit_minutes=15
            )
            db.add(quiz)
            await db.flush()

            # Seed Quiz Questions
            if item["words"]:
                w1 = item["words"][0]["word"]
                w2 = item["words"][1]["word"] if len(item["words"]) > 1 else w1
                # Question 1: Listen and choose the word
                q1 = QuizQuestion(
                    quiz_id=quiz.id,
                    question_type="listen_select",
                    question_text=f"استمع جيداً واختر الكلمة الصحيحة ({w1})",
                    audio_url=f"/static/audio/{w1.lower()}.mp3",
                    options_json=[w1, w2, "Car", "Sun"],
                    correct_answer=w1
                )
                # Question 2: Word meaning / Picture matching
                q2 = QuizQuestion(
                    quiz_id=quiz.id,
                    question_type="word_match",
                    question_text=f"ما معنى كلمة ({item['words'][0]['word']}) بالعربية؟",
                    options_json=[item['words'][0]['translation_ar'], "قمر", "طائرة", "ماء"],
                    correct_answer=item['words'][0]['translation_ar']
                )
                # Question 3: Phonics breakdown
                q3 = QuizQuestion(
                    quiz_id=quiz.id,
                    question_type="phoneme_id",
                    question_text=f"كم عدد أصوات كلمة {w1}؟",
                    options_json=["3 أصوات", "5 أصوات", "صوت واحد"],
                    correct_answer="3 أصوات"
                )
                db.add_all([q1, q2, q3])

        # Seed System Settings
        settings_rows = [
            SystemSetting(key="passing_grade", value="80", description="نسبة النجاح الافتراضية لاجتياز المستويات"),
            SystemSetting(key="min_phoneme_confidence", value="0.4", description="الحد الأدنى لثقة التحليل الصوتي"),
            SystemSetting(key="allow_parent_registration", value="true", description="السماح بإنشاء حسابات أولياء الأمور"),
            SystemSetting(key="telegram_notifications", value="true", description="تفعيل الإشعارات الفورية إلى Telegram")
        ]
        db.add_all(settings_rows)

        # 2. Seed Default Admin User
        admin_user = User(
            student_id="ADMIN-001",
            full_name="المدير العام للمنصة",
            phone_number="01000000000",
            hashed_password=get_password_hash("admin123456"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)

        # 3. Seed Default Teacher
        teacher_user = User(
            student_id="TCH-001",
            full_name="ميس سارة أحمد خليل",
            phone_number="01011111111",
            hashed_password=get_password_hash("teacher123"),
            role="teacher",
            is_active=True
        )
        db.add(teacher_user)
        await db.flush()

        teacher_profile = TeacherAccount(
            user_id=teacher_user.id,
            specialization="Early Literacy & Jolly Phonics Expert"
        )
        db.add(teacher_profile)

        # 4. Seed Demo Student User
        student_user = User(
            student_id="STU-2026-DEMO",
            full_name="محمد أحمد علي",
            phone_number="01022222222",
            hashed_password=get_password_hash("student123"),
            role="student",
            is_active=True
        )
        db.add(student_user)
        await db.flush()

        student_prof = StudentProfile(
            user_id=student_user.id,
            current_level_id=1,
            xp=150,
            stars=12,
            streak_days=3,
            avatar="lion"
        )
        db.add(student_prof)
        await db.flush()

        # Unlock Level 1 for student
        unlock = StudentLevelAccess(
            student_id=student_prof.id,
            level_id=1,
            is_unlocked=True,
            unlocked_by="system"
        )
        db.add(unlock)

        await db.commit()
        print("Curriculum, Admin, Teacher, and Student seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
