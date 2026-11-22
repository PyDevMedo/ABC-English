from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Auth & User Schemas
class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=5, description="Full tripartite name, e.g. محمد أحمد علي")
    phone_number: str = Field(..., min_length=8, max_length=20, description="Valid mobile phone")
    password: str = Field(..., min_length=6)
    role: Optional[str] = "student"
    avatar: Optional[str] = "lion"

class UserLogin(BaseModel):
    phone_number: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    student_id: Optional[str] = None
    full_name: str

class UserResponse(BaseModel):
    id: int
    student_id: Optional[str]
    full_name: str
    phone_number: str
    role: str
    is_active: bool
    created_at: datetime
    avatar: Optional[str] = "lion"
    xp: Optional[int] = 0
    stars: Optional[int] = 0
    streak_days: Optional[int] = 1
    current_level_id: Optional[int] = 1

    class Config:
        from_attributes = True

# Telegram Linking
class TelegramLinkTokenResponse(BaseModel):
    code: str
    expires_at: datetime
    bot_username: Optional[str] = None

class TelegramLinkVerify(BaseModel):
    code: str
    telegram_user_id: str
    telegram_chat_id: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = "parent"

# Curriculum Schemas
class WordSchema(BaseModel):
    id: int
    word: str
    phonemes_breakdown: str
    translation_ar: str
    image_url: Optional[str]
    audio_url: Optional[str]
    is_sight_word: bool

    class Config:
        from_attributes = True

class LessonSectionSchema(BaseModel):
    id: int
    section_type: str
    title_ar: str
    title_en: str
    content_json: Any
    audio_url: Optional[str]
    order_index: int

    class Config:
        from_attributes = True

class LessonSchema(BaseModel):
    id: int
    level_id: int
    lesson_number: int
    title: str
    description: Optional[str]
    order_index: int
    sections: List[LessonSectionSchema] = []

    class Config:
        from_attributes = True

class LevelSchema(BaseModel):
    id: int
    level_number: int
    title: str
    subtitle: str
    description: Optional[str]
    icon: str
    is_unlocked: bool = False
    progress_percentage: int = 0
    min_passing_score: int = 80
    lessons: List[LessonSchema] = []

    class Config:
        from_attributes = True

# Pronunciation & AI Teacher Schemas
class PronunciationAssessmentResponse(BaseModel):
    attempt_id: int
    overall_score: int
    phoneme_accuracy: int
    clarity_score: int
    recognized_text: str
    target_text: str
    correct_phonemes: List[str]
    error_phonemes: List[str]
    feedback_text: str
    audio_quality: str # "clear", "noisy", "silent"
    needs_retry: bool
    adaptive_triggered: bool
    weakness_detected: Optional[str] = None
    xp_earned: int = 0
    stars_earned: int = 0

class AdaptiveExerciseStep(BaseModel):
    step_number: int
    title_ar: str
    instruction_en: str
    instruction_ar: str
    target_sound: str
    target_words: List[str]
    sample_sentence: Optional[str]
    audio_url: Optional[str]

class AdaptivePlanResponse(BaseModel):
    id: int
    student_id: int
    current_focus: str
    weakness_summary: Dict[str, Any]
    exercises_count: int
    status: str
    exercises: List[Dict[str, Any]] = []

# Assignment Schemas
class AssignmentCreate(BaseModel):
    level_id: int
    title: str
    description: Optional[str]
    instructions_ar: str
    assignment_type: str = "audio_recording"
    target_words: List[str] = []
    target_sentences: List[str] = []
    due_date: Optional[datetime] = None

class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    submission_type: str = "audio"
    text_content: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None

class AssignmentFeedbackCreate(BaseModel):
    score: int
    comments: str
    retry_requested: bool = False

# Quiz Schemas
class QuizSubmitRequest(BaseModel):
    quiz_id: int
    answers: Dict[str, Any] # question_id -> child answer

class QuizResultResponse(BaseModel):
    quiz_id: int
    score: int
    passed: bool
    passing_score: int
    correct_count: int
    total_count: int
    level_unlocked: bool = False
    details: Dict[str, Any]

# Gamification Schemas
class GamificationStats(BaseModel):
    xp: int
    stars: int
    streak_days: int
    current_level_id: int
    completed_lessons_count: int
    total_pronunciation_attempts: int
    mastered_skills: List[str]
    needs_review_skills: List[str]
    badges: List[Dict[str, Any]]
    certificates: List[Dict[str, Any]]
