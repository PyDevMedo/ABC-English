from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, JSON, Table
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=True) # STU-2026-XXXX
    full_name = Column(String(200), nullable=False) # Tripartite verified
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student", nullable=False) # student, parent, teacher, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent_account = relationship("ParentAccount", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_account = relationship("TeacherAccount", back_populates="user", uselist=False, cascade="all, delete-orphan")
    telegram_link_tokens = relationship("TelegramLinkToken", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    current_level_id = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    stars = Column(Integer, default=0)
    streak_days = Column(Integer, default=1)
    last_active_date = Column(DateTime, default=datetime.utcnow)
    avatar = Column(String(100), default="lion") # cute animal avatar: lion, monkey, panda, bunny, fox
    bio = Column(String(255), nullable=True)

    user = relationship("User", back_populates="student_profile")
    level_accesses = relationship("StudentLevelAccess", back_populates="student", cascade="all, delete-orphan")
    lesson_progresses = relationship("LessonProgress", back_populates="student", cascade="all, delete-orphan")
    skill_progresses = relationship("SkillProgress", back_populates="student", cascade="all, delete-orphan")
    assignment_submissions = relationship("AssignmentSubmission", back_populates="student", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="student", cascade="all, delete-orphan")
    pronunciation_attempts = relationship("PronunciationAttempt", back_populates="student", cascade="all, delete-orphan")
    weaknesses = relationship("StudentWeakness", back_populates="student", cascade="all, delete-orphan")
    learning_plans = relationship("PersonalizedLearningPlan", back_populates="student", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="student", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="student", cascade="all, delete-orphan")

class ParentAccount(Base):
    __tablename__ = "parent_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="SET NULL"), nullable=True)
    telegram_chat_id = Column(String(50), nullable=True)
    notifications_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="parent_account")

class TeacherAccount(Base):
    __tablename__ = "teacher_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialization = Column(String(100), default="Phonics Specialist")
    telegram_chat_id = Column(String(50), nullable=True)

    user = relationship("User", back_populates="teacher_account")

class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String(50), unique=True, index=True, nullable=False)
    telegram_chat_id = Column(String(50), index=True, nullable=False)
    role = Column(String(20), default="admin") # admin, teacher, parent
    username = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=True)
    is_approved = Column(Boolean, default=True)
    linked_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TelegramLinkToken(Base):
    __tablename__ = "telegram_link_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(10), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="telegram_link_tokens")

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    level_number = Column(Integer, unique=True, index=True, nullable=False) # 1 to 8
    title = Column(String(100), nullable=False)
    subtitle = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="star")
    min_passing_score = Column(Integer, default=80)
    is_active = Column(Boolean, default=True)

    lessons = relationship("Lesson", back_populates="level", cascade="all, delete-orphan")
    words = relationship("Word", back_populates="level", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="level", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="level", cascade="all, delete-orphan")

class StudentLevelAccess(Base):
    __tablename__ = "student_level_accesses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    is_unlocked = Column(Boolean, default=False)
    unlocked_by = Column(String(50), default="system") # system or teacher_telegram
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="level_accesses")
    level = relationship("Level")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    level = relationship("Level", back_populates="lessons")
    sections = relationship("LessonSection", back_populates="lesson", cascade="all, delete-orphan")
    progresses = relationship("LessonProgress", back_populates="lesson", cascade="all, delete-orphan")

class LessonSection(Base):
    __tablename__ = "lesson_sections"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    section_type = Column(String(50), nullable=False) # intro, phonics, words, sentences, listening, pronunciation, writing, quiz
    title_ar = Column(String(150), nullable=False)
    title_en = Column(String(150), nullable=False)
    content_json = Column(JSON, nullable=False)
    audio_url = Column(String(255), nullable=True)
    order_index = Column(Integer, default=0)

    lesson = relationship("Lesson", back_populates="sections")

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    word = Column(String(50), index=True, nullable=False)
    phonemes_breakdown = Column(String(100), nullable=False) # e.g. "S-A-T" or "SH-I-P"
    translation_ar = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=True)
    audio_url = Column(String(255), nullable=True)
    is_sight_word = Column(Boolean, default=False)

    level = relationship("Level", back_populates="words")

class Phoneme(Base):
    __tablename__ = "phonemes"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False) # e.g. "S", "SH", "AI"
    name_letter = Column(String(50), nullable=False)
    sound_audio_url = Column(String(255), nullable=True)
    sample_words_json = Column(JSON, default=list)
    description_ar = Column(String(255), nullable=True)

class LessonProgress(Base):
    __tablename__ = "lesson_progresses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    is_completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="lesson_progresses")
    lesson = relationship("Lesson", back_populates="progresses")

class SkillProgress(Base):
    __tablename__ = "skill_progresses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), index=True, nullable=False) # e.g. "SH Digraph", "CVC Words", "Short A"
    mastery_percentage = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    last_assessed_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="skill_progresses")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    created_by_teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    instructions_ar = Column(Text, nullable=False)
    assignment_type = Column(String(50), default="reading") # writing, reading, audio_recording, quiz, matching, file_upload
    target_words_json = Column(JSON, default=list)
    target_sentences_json = Column(JSON, default=list)
    media_url = Column(String(255), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    level = relationship("Level", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    submission_type = Column(String(50), default="audio")
    text_content = Column(Text, nullable=True)
    audio_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    status = Column(String(30), default="submitted") # submitted, under_review, graded, retry_needed, late
    submitted_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("StudentProfile", back_populates="assignment_submissions")
    feedback = relationship("AssignmentFeedback", back_populates="submission", uselist=False, cascade="all, delete-orphan")

class AssignmentFeedback(Base):
    __tablename__ = "assignment_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("assignment_submissions.id", ondelete="CASCADE"), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    score = Column(Integer, default=100) # 0-100
    comments = Column(Text, nullable=True)
    retry_requested = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("AssignmentSubmission", back_populates="feedback")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    passing_score = Column(Integer, default=80)
    time_limit_minutes = Column(Integer, default=15)

    level = relationship("Level", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_type = Column(String(50), nullable=False) # multiple_choice, listen_select, phoneme_id, word_match, word_scramble, pronunciation, fill_blank
    question_text = Column(String(255), nullable=False)
    audio_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    options_json = Column(JSON, default=list) # List of options
    correct_answer = Column(String(255), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    passed = Column(Boolean, default=False)
    details_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    quiz = relationship("Quiz", back_populates="results")
    student = relationship("StudentProfile", back_populates="quiz_results")

class PronunciationAttempt(Base):
    __tablename__ = "pronunciation_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    target_text = Column(String(255), nullable=False)
    target_phonemes = Column(String(255), nullable=True)
    audio_path = Column(String(255), nullable=True)
    duration_seconds = Column(Float, default=0.0)
    overall_score = Column(Integer, default=0) # 0-100
    phoneme_accuracy = Column(Integer, default=0)
    clarity_score = Column(Integer, default=0)
    recognized_text = Column(String(255), nullable=True)
    recognized_phonemes = Column(String(255), nullable=True)
    correct_phonemes_json = Column(JSON, default=list)
    error_phonemes_json = Column(JSON, default=list)
    feedback_text = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="pronunciation_attempts")

class StudentWeakness(Base):
    __tablename__ = "student_weaknesses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    phoneme_or_skill = Column(String(50), index=True, nullable=False) # e.g. "SH", "TH", "Short A"
    error_count = Column(Integer, default=1)
    total_trials = Column(Integer, default=1)
    severity = Column(String(20), default="medium") # low, medium, high
    last_detected_at = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)

    student = relationship("StudentProfile", back_populates="weaknesses")

class PersonalizedLearningPlan(Base):
    __tablename__ = "personalized_learning_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    current_focus = Column(String(100), nullable=False) # e.g. "Mastering Digraph SH"
    weakness_summary_json = Column(JSON, default=dict)
    exercises_count = Column(Integer, default=3)
    status = Column(String(30), default="active") # active, completed, teacher_reviewed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="learning_plans")
    exercises = relationship("AdaptiveExercise", back_populates="plan", cascade="all, delete-orphan")

class AdaptiveExercise(Base):
    __tablename__ = "adaptive_exercises"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("personalized_learning_plans.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="easy") # easy, medium, hard, retest
    exercise_data_json = Column(JSON, nullable=False) # steps, audio, target words
    is_completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    plan = relationship("PersonalizedLearningPlan", back_populates="exercises")

class TeacherReport(Base):
    __tablename__ = "teacher_reports"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    report_type = Column(String(50), default="weakness_alert") # weakness_alert, milestone, weekly_summary
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=True)
    status = Column(String(30), default="sent") # sent, reviewed, action_taken, closed
    telegram_message_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="general")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    badge_key = Column(String(50), nullable=False)
    badge_title = Column(String(100), nullable=False)
    badge_icon = Column(String(50), default="trophy")
    earned_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="achievements")

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)
    certificate_number = Column(String(100), unique=True, index=True, nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow)
    pdf_url = Column(String(255), nullable=True)

    student = relationship("StudentProfile", back_populates="certificates")
    level = relationship("Level")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    details_json = Column(JSON, default=dict)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activity_logs")

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
