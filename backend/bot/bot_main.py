import asyncio
import logging
import os
import sys
from datetime import datetime

# Fix for Python 3.11 / pydantic FailFast unhashable issue with typing.Union
from pydantic.types import FailFast
FailFast.__hash__ = lambda self: hash(('FailFast', self.fail_fast))

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.entities import (
    User, StudentProfile, Level, Lesson, Assignment, AssignmentSubmission,
    AssignmentFeedback, QuizResult, StudentWeakness, PersonalizedLearningPlan,
    AdaptiveExercise, TeacherReport, TelegramAccount, TelegramLinkToken,
    PronunciationAttempt, Notification
)
from app.services.xp_service import get_xp_required_for_level, get_level_stage_info
from app.services.curriculum_50 import generate_50_levels
from bot.bot_styles import tg_e, s_btn, EMOJIS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cached curriculum metadata
CURRICULUM_50_DATA = generate_50_levels()

# FSM States
class BotStates(StatesGroup):
    search_student_query = State()
    search_type = State()
    send_student_message = State()
    target_student_id = State()
    broadcast_message = State()

async def safe_edit_or_reply(call: CallbackQuery, text: str, reply_markup=None):
    """Safely edit text or caption for photo messages, with graceful fallback to answering."""
    try:
        if call.message.photo:
            await call.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=reply_markup)
        else:
            await call.message.edit_text(text=text, parse_mode="HTML", reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            pass
        else:
            try:
                await call.message.answer(text=text, parse_mode="HTML", reply_markup=reply_markup)
            except Exception:
                pass
    except Exception as e:
        logger.warning(f"Safe edit fallback: {e}")
        try:
            await call.message.answer(text=text, parse_mode="HTML", reply_markup=reply_markup)
        except Exception:
            pass

def get_main_menu_keyboard():
    """15 Main Management Sections with Custom Emojis and Colored Styles"""
    keyboard = [
        [
            s_btn("إدارة الطلاب", "menu_students", style="primary", emoji_key="STUDENT"),
            s_btn("إدارة المستويات (50 لفل)", "menu_levels", style="primary", emoji_key="SPARKLES")
        ],
        [
            s_btn("إدارة الدروس", "menu_lessons", style="primary", emoji_key="PIN"),
            s_btn("إدارة الواجبات", "menu_assignments", style="primary", emoji_key="STAR")
        ],
        [
            s_btn("تسليمات الطلاب (دفاتر الخط)", "menu_submissions", style="primary", emoji_key="CAMERA"),
            s_btn("تصحيح الواجبات", "menu_grading", style="success", emoji_key="CHECK")
        ],
        [
            s_btn("الاختبارات والنتائج", "menu_quizzes", style="primary", emoji_key="STAR"),
            s_btn("مدرس الذكاء الاصطناعي", "menu_ai_teacher", style="primary", emoji_key="BRAIN")
        ],
        [
            s_btn("تقارير الطلاب", "menu_student_reports", style="primary", emoji_key="STATS"),
            s_btn("إدارة المدرسين", "menu_teachers", style="primary", emoji_key="STUDENT")
        ],
        [
            s_btn("إدارة أولياء الأمور", "menu_parents", style="primary", emoji_key="CHAT"),
            s_btn("الإشعارات والرسائل", "menu_notifications", style="primary", emoji_key="BELL")
        ],
        [
            s_btn("الشهادات والمكافآت", "menu_certificates", style="success", emoji_key="TROPHY"),
            s_btn("الإعدادات العامة", "menu_settings", style="primary", emoji_key="GEAR")
        ],
        [
            s_btn("الإحصائيات والتقارير الشاملة", "menu_stats", style="primary", emoji_key="STATS")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_students_menu_keyboard():
    keyboard = [
        [
            s_btn("جميع الطلاب", "stu_list_all", style="primary", emoji_key="STUDENT"),
            s_btn("الطلاب الجدد", "stu_list_new", style="success", emoji_key="SPARKLES")
        ],
        [
            s_btn("الطلاب النشطون", "stu_list_active", style="success", emoji_key="CHECK"),
            s_btn("الطلاب الموقوفون", "stu_list_suspended", style="danger", emoji_key="DANGER")
        ],
        [
            s_btn("بحث بالاسم", "stu_search_name", style="primary", emoji_key="PIN"),
            s_btn("بحث برقم الهاتف", "stu_search_phone", style="primary", emoji_key="PIN")
        ],
        [
            s_btn("بحث بـ Student ID", "stu_search_id", style="primary", emoji_key="PIN"),
            s_btn("طلاب بحاجة لمتابعة", "stu_list_weakness", style="danger", emoji_key="ALERT")
        ],
        [
            s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

dp = Dispatcher(storage=MemoryStorage())

# Outer middleware to guarantee callback queries are always answered
@dp.callback_query.outer_middleware()
async def callback_answer_middleware(handler, event: CallbackQuery, data: dict):
    try:
        return await handler(event, data)
    finally:
        try:
            await event.answer()
        except Exception:
            pass

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        f"{tg_e('WAVE', '👋')} <b>مرحباً بك في مركز إدارة منصة ABC لتعليم الإنجليزية!</b>\n\n"
        f"<blockquote>"
        f"✨ <i>نظام تعليمي متكامل يتدرج عبر <b>50 مستوى احترافي</b></i>\n"
        f"🎯 <b>المستوى 15:</b> التحدث مع الأشخاص والمحادثات اليومية\n"
        f"👑 <b>المستوى 50:</b> الطلاقة المطلقة والتحدث كمتحدث أصلي (Native Fluency)\n"
        f"</blockquote>\n\n"
        f"اختر القسم المطلوب للتحكم الكامل في المنصة:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())

@dp.message(Command("link"))
async def cmd_link_telegram(message: Message):
    """Link parent Telegram account using 6-digit code: /link 123456"""
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            f"{tg_e('ALERT', '⚠️')} <b>طريقة ربط الحساب:</b>\n"
            f"<blockquote>"
            f"يرجى تسجيل الدخول إلى الموقع والضغط على زر <b>(ربط Telegram)</b>، "
            f"ثم إرسال الأمر هنا هكذا:\n<code>/link 123456</code>"
            f"</blockquote>",
            parse_mode="HTML"
        )
        return

    code = args[1].strip()
    now = datetime.utcnow()

    async with AsyncSessionLocal() as db:
        q = select(TelegramLinkToken).where(
            and_(
                TelegramLinkToken.token == code,
                TelegramLinkToken.is_used == False,
                TelegramLinkToken.expires_at > now
            )
        )
        res = await db.execute(q)
        token_obj = res.scalar_one_or_none()

        if not token_obj:
            await message.answer(f"{tg_e('DANGER', '❌')} <b>رمز الربط غير صحيح أو انتهت صلاحيته.</b> يرجى طلب رمز جديد من الموقع.")
            return

        token_obj.is_used = True

        tg_q = select(TelegramAccount).where(TelegramAccount.telegram_user_id == str(message.from_user.id))
        tg_acc = (await db.execute(tg_q)).scalar_one_or_none()

        if not tg_acc:
            tg_acc = TelegramAccount(
                telegram_user_id=str(message.from_user.id),
                telegram_chat_id=str(message.chat.id),
                role="parent",
                username=message.from_user.username,
                full_name=message.from_user.full_name,
                linked_user_id=token_obj.user_id
            )
            db.add(tg_acc)
        else:
            tg_acc.telegram_chat_id = str(message.chat.id)
            tg_acc.linked_user_id = token_obj.user_id

        user_q = select(User).where(User.id == token_obj.user_id)
        user = (await db.execute(user_q)).scalar_one()
        await db.commit()

        await message.answer(
            f"{tg_e('CHECK', '🎉')} <b>تم ربط الحساب بنجاح!</b>\n\n"
            f"<blockquote>"
            f"{tg_e('STUDENT')} الطالب المرتبط: <b>{user.full_name}</b>\n"
            f"🆔 معرف الطالب: <code>{user.student_id}</code>\n"
            f"📱 ستصلك الآن تقارير الأداء، إشعارات تصحيح الواجبات، وتنبيهات المستوى مباشرة هنا."
            f"</blockquote>",
            parse_mode="HTML"
        )

# Main Menu Callback
@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_reply(
        call,
        f"{tg_e('GEAR', '🎛️')} <b>القائمة الرئيسية لإدارة منصة ABC (50 مستوى):</b>\n"
        f"<blockquote>اختر من الأقسام التالية للتحكم الكامل والوصول السريع:</blockquote>",
        reply_markup=get_main_menu_keyboard()
    )

# Section 1: Students Management
@dp.callback_query(F.data == "menu_students")
async def cb_menu_students(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_reply(
        call,
        f"{tg_e('STUDENT', '👥')} <b>قسم إدارة الطلاب:</b>\n"
        f"<blockquote>اختر العملية المطلوبة لعرض الطلاب وتعديل مستوياتهم وتصحيح واجباتهم:</blockquote>",
        reply_markup=get_students_menu_keyboard()
    )

@dp.callback_query(F.data.in_(["stu_list_all", "stu_list_new", "stu_list_active", "stu_list_suspended"]))
async def cb_list_students(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(User).where(User.role == "student")
        if call.data == "stu_list_active":
            q = q.where(User.is_active == True)
        elif call.data == "stu_list_suspended":
            q = q.where(User.is_active == False)
        elif call.data == "stu_list_new":
            q = q.order_by(User.id.desc()).limit(10)
        else:
            q = q.order_by(User.id.desc()).limit(20)

        students = (await db.execute(q)).scalars().all()

        if not students:
            await safe_edit_or_reply(
                call,
                f"{tg_e('STUDENT')} <b>لا يوجد طلاب مسجلون حالياً في هذا القسم.</b>\n\n"
                f"<blockquote>يمكنك تسجيل طالب جديد من الموقع ليظهر هنا فوراً.</blockquote>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")]])
            )
            return

        buttons = []
        for s in students:
            status_icon = "CHECK" if s.is_active else "DANGER"
            buttons.append([s_btn(
                f"{s.full_name} ({s.student_id})",
                f"view_stu_{s.student_id}",
                style="primary" if s.is_active else "danger",
                emoji_key=status_icon
            )])

        buttons.append([s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(
            call,
            f"{tg_e('STUDENT')} <b>قائمة الطلاب ({len(students)} طالب):</b>\n"
            f"<blockquote>اضغط على اسم الطالب لعرض ملفه بالكامل والتحكم به:</blockquote>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Student Search Prompts
@dp.callback_query(F.data.in_(["stu_search_name", "stu_search_phone", "stu_search_id"]))
async def cb_search_student_prompt(call: CallbackQuery, state: FSMContext):
    search_type = call.data.replace("stu_search_", "")
    await state.update_data(search_type=search_type)
    await state.set_state(BotStates.search_student_query)

    type_labels = {
        "name": "الاسم الثلاثي أو جزء منه",
        "phone": "رقم الهاتف المحمول",
        "id": "Student ID (مثال: STU-12345)"
    }

    buttons = [[s_btn("إلغاء والعودة", "menu_students", style="danger", emoji_key="DANGER")]]
    await safe_edit_or_reply(
        call,
        f"{tg_e('PIN')} <b>بحث عن طالب:</b>\n\n"
        f"<blockquote>يرجى إرسال <b>{type_labels.get(search_type, 'بيانات البحث')}</b> في رسالة نصية الآن:</blockquote>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

# Handle Search Query Input
@dp.message(BotStates.search_student_query)
async def handle_search_query(message: Message, state: FSMContext):
    query = message.text.strip()
    data = await state.get_data()
    search_type = data.get("search_type", "name")
    await state.clear()

    async with AsyncSessionLocal() as db:
        q = select(User).where(User.role == "student")
        if search_type == "name":
            q = q.where(User.full_name.ilike(f"%{query}%"))
        elif search_type == "phone":
            q = q.where(User.phone_number.ilike(f"%{query}%"))
        elif search_type == "id":
            q = q.where(User.student_id.ilike(f"%{query}%"))

        students = (await db.execute(q)).scalars().all()

        if not students:
            buttons = [
                [s_btn("إعادة البحث", f"stu_search_{search_type}", style="primary", emoji_key="PIN")],
                [s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")]
            ]
            await message.answer(
                f"{tg_e('ALERT', '⚠️')} <b>لم يتم العثور على أي طالب يطابق:</b> <code>{query}</code>\n"
                f"<blockquote>تأكد من صحة البيانات المدخلة وحاول مجدداً.</blockquote>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
            return

        if len(students) == 1:
            # Single match: jump directly to student profile
            fake_call = types.CallbackQuery(
                id="0",
                from_user=message.from_user,
                chat_instance="",
                message=message,
                data=f"view_stu_{students[0].student_id}"
            )
            await cb_view_student(fake_call)
            return

        # Multiple matches
        buttons = []
        for s in students:
            buttons.append([s_btn(
                f"{s.full_name} ({s.student_id})",
                f"view_stu_{s.student_id}",
                style="primary",
                emoji_key="STUDENT"
            )])
        buttons.append([s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")])

        await message.answer(
            f"{tg_e('CHECK', '✅')} <b>نتائج البحث ({len(students)} طالب):</b>\n"
            f"<blockquote>اختر الطالب لعرض ملفه بالكامل:</blockquote>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Weakness List
@dp.callback_query(F.data == "stu_list_weakness")
async def cb_list_weaknesses(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(StudentWeakness).options(
            selectinload(StudentWeakness.student).selectinload(StudentProfile.user)
        ).where(StudentWeakness.is_resolved == False).order_by(StudentWeakness.error_count.desc()).limit(15)
        weaknesses = (await db.execute(q)).scalars().all()

        if not weaknesses:
            await safe_edit_or_reply(
                call,
                f"{tg_e('STAR', '🌟')} <b>ممتاز! لا توجد صعوبات نطق مستمرة لدى الطلاب حالياً.</b>\n\n"
                f"<blockquote>جميع الطلاب يجتازون اختبارات النطق بنجاح.</blockquote>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")]])
            )
            return

        buttons = []
        for w in weaknesses:
            s_name = w.student.user.full_name if (w.student and w.student.user) else f"Student #{w.student_id}"
            stu_id = w.student.user.student_id if (w.student and w.student.user) else str(w.student_id)
            buttons.append([s_btn(
                f"{s_name} - {w.phoneme_or_skill} ({w.error_count} أخطاء)",
                f"ai_plan_{stu_id}",
                style="primary",
                emoji_key="ALERT"
            )])
        buttons.append([s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(
            call,
            f"{tg_e('ALERT', '⚠️')} <b>الطلاب الذين يواجهون صعوبات نطق phonemes:</b>\n"
            f"<blockquote>اضغط على اسم الطالب لعرض خطة التدريب التكيفية:</blockquote>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# View Specific Student Profile
@dp.callback_query(F.data.startswith("view_stu_"))
async def cb_view_student(call: CallbackQuery):
    identifier = call.data.replace("view_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile)
        ).where(or_(User.student_id == identifier, User.id == int(identifier) if identifier.isdigit() else False))
        res = await db.execute(q)
        user = res.scalar_one_or_none()

        if not user:
            await call.answer("لم يتم العثور على الطالب", show_alert=True)
            return

        prof = user.student_profile
        lvl_num = prof.current_level_id if prof else 1
        xp = prof.xp if prof else 0
        stars = prof.stars if prof else 0
        stage_info = get_level_stage_info(lvl_num)
        xp_next = get_xp_required_for_level(min(50, lvl_num + 1))

        # Fetch weaknesses
        weaknesses = []
        if prof:
            w_q = select(StudentWeakness).where(and_(StudentWeakness.student_id == prof.id, StudentWeakness.is_resolved == False))
            weaknesses = (await db.execute(w_q)).scalars().all()
        weakness_str = ", ".join([f"{w.phoneme_or_skill} ({w.error_count} أخطاء)" for w in weaknesses]) if weaknesses else "لا توجد نقاط ضعف مسجلة ✨"

        text = (
            f"{tg_e('STUDENT', '👤')} <b>ملف الطالب:</b> <code>{user.full_name}</code>\n\n"
            f"<blockquote>"
            f"🆔 <b>Student ID:</b> <code>{user.student_id}</code>\n"
            f"📱 <b>رقم الهاتف:</b> <code>{user.phone_number}</code>\n"
            f"📚 <b>المستوى الحالي:</b> <b>Level {lvl_num}/50</b> ({stage_info['badge']})\n"
            f"🎯 <b>المرحلة:</b> <i>{stage_info['stage_name']}</i>\n"
            f"⭐ <b>النجوم:</b> {stars} ⭐ | <b>XP:</b> {xp} / {xp_next} XP\n"
            f"🔥 <b>Streak:</b> {prof.streak_days if prof else 1} أيام متتالية\n"
            f"⚡ <b>حالة الحساب:</b> {'نشط ومفعل ✅' if user.is_active else 'موقوف مؤقتاً ⛔'}\n"
            f"⚠️ <b>نقاط تحتاج مراجعة:</b> <i>{weakness_str}</i>\n"
            f"</blockquote>"
        )

        buttons = [
            [
                s_btn("تحديد المستوى (1-50)", f"set_lvl_{user.student_id}", style="primary", emoji_key="SPARKLES"),
                s_btn("إيقاف الحساب" if user.is_active else "تفعيل الحساب", f"toggle_stu_{user.student_id}", style="danger" if user.is_active else "success", emoji_key="DANGER" if user.is_active else "CHECK")
            ],
            [
                s_btn("تقرير التقدم والـ XP", f"prog_stu_{user.student_id}", style="primary", emoji_key="STATS"),
                s_btn("واجبات الدفتر والخط", f"hw_stu_{user.student_id}", style="primary", emoji_key="CAMERA")
            ],
            [
                s_btn("المحاولات الصوتية", f"ai_listen_{user.student_id}", style="primary", emoji_key="BRAIN"),
                s_btn("إرسال رسالة للطالب", f"msg_stu_{user.student_id}", style="primary", emoji_key="CHAT")
            ],
            [
                s_btn("العودة لقائمة الطلاب", "menu_students", style="danger", emoji_key="DANGER")
            ]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Student Sub-view: Progress & XP
@dp.callback_query(F.data.startswith("prog_stu_"))
async def cb_student_progress(call: CallbackQuery):
    identifier = call.data.replace("prog_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if not user or not user.student_profile:
            await call.answer("بيانات الطالب غير متوفرة", show_alert=True)
            return

        prof = user.student_profile
        lvl_num = prof.current_level_id
        quizzes_passed = await db.scalar(select(func.count(QuizResult.id)).where(and_(QuizResult.student_id == prof.id, QuizResult.passed == True))) or 0
        hw_graded = await db.scalar(select(func.count(AssignmentSubmission.id)).where(and_(AssignmentSubmission.student_id == prof.id, AssignmentSubmission.status == "graded"))) or 0
        voice_attempts = await db.scalar(select(func.count(PronunciationAttempt.id)).where(PronunciationAttempt.student_id == prof.id)) or 0

        text = (
            f"{tg_e('STATS', '📊')} <b>تقرير تقدم الطالب:</b> <code>{user.full_name}</code>\n\n"
            f"<blockquote>"
            f"📚 <b>المستوى الحالي:</b> Level {lvl_num} من 50\n"
            f"⭐ <b>مجموع النجوم:</b> {prof.stars} نجوم\n"
            f"⚡ <b>نقاط الخبرة (XP):</b> {prof.xp} XP\n"
            f"📝 <b>الاختبارات المجتازة:</b> {quizzes_passed} اختبار بنجاح\n"
            f"✍️ <b>واجبات الخط المعتمدة:</b> {hw_graded} واجب دفتري\n"
            f"🎙️ <b>جلسات نطق الذكاء الاصطناعي:</b> {voice_attempts} تسجيل صوتي\n"
            f"🔥 <b>أيام الالتزام المستمرة:</b> {prof.streak_days} أيام متتالية\n"
            f"</blockquote>"
        )
        buttons = [
            [s_btn("تعديل المستوى", f"set_lvl_{identifier}", style="primary", emoji_key="SPARKLES")],
            [s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Student Sub-view: Homework Submissions
@dp.callback_query(F.data.startswith("hw_stu_"))
async def cb_student_homework_list(call: CallbackQuery):
    identifier = call.data.replace("hw_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if not user or not user.student_profile:
            await call.answer("بيانات الطالب غير متوفرة", show_alert=True)
            return

        sub_q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.assignment),
            selectinload(AssignmentSubmission.feedback)
        ).where(AssignmentSubmission.student_id == user.student_profile.id).order_by(AssignmentSubmission.id.desc()).limit(10)
        subs = (await db.execute(sub_q)).scalars().all()

        if not subs:
            await safe_edit_or_reply(
                call,
                f"{tg_e('CAMERA')} <b>لا توجد واجبات دفترية مسلمة من الطالب:</b> <code>{user.full_name}</code> حتى الآن.\n\n"
                f"<blockquote>يقوم الطالب بكتابة الواجب وتصويره من صفحة الدرس بالموقع.</blockquote>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]])
            )
            return

        buttons = []
        for s in subs:
            status_text = "معتمد ✅" if s.status == "graded" else "بانتظار التصحيح ⏳"
            score_text = f"({s.feedback.score}%)" if (s.feedback and s.feedback.score is not None) else ""
            hw_title = s.assignment.title if s.assignment else "Homework"
            buttons.append([s_btn(
                f"{hw_title} - {status_text} {score_text}",
                f"sub_rev_{s.id}",
                style="success" if s.status == "graded" else "primary",
                emoji_key="CAMERA"
            )])
        buttons.append([s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(
            call,
            f"{tg_e('CAMERA')} <b>سجل واجبات الدفتر للطالب:</b> <code>{user.full_name}</code>\n"
            f"<blockquote>اضغط على أي واجب لمراجعته أو تعديل درجته:</blockquote>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Student Sub-view: Voice AI Attempts
@dp.callback_query(F.data.startswith("ai_listen_"))
async def cb_student_voice_attempts(call: CallbackQuery):
    identifier = call.data.replace("ai_listen_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if not user or not user.student_profile:
            await call.answer("بيانات الطالب غير متوفرة", show_alert=True)
            return

        att_q = select(PronunciationAttempt).where(PronunciationAttempt.student_id == user.student_profile.id).order_by(PronunciationAttempt.id.desc()).limit(8)
        attempts = (await db.execute(att_q)).scalars().all()

        if not attempts:
            await safe_edit_or_reply(
                call,
                f"{tg_e('BRAIN')} <b>لا توجد محاولات نطق مسجلة للطالب:</b> <code>{user.full_name}</code> حتى الآن.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]])
            )
            return

        text = f"{tg_e('BRAIN', '🎙️')} <b>آخر جلسات نطق الذكاء الاصطناعي للطالب:</b> <code>{user.full_name}</code>\n\n<blockquote>"
        for a in attempts:
            status = "✅ ممتاز" if (a.overall_score or 0) >= 80 else ("⚠️ مقبول" if (a.overall_score or 0) >= 60 else "❌ يحتاج إعادة")
            text += f"• الكلمة: <b>{a.target_text}</b> | الدرجة: <b>{a.overall_score}%</b> ({status})\n"
        text += "</blockquote>"

        buttons = [[s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Student Sub-view: Send Message to Student/Parent
@dp.callback_query(F.data.startswith("msg_stu_"))
async def cb_prompt_student_message(call: CallbackQuery, state: FSMContext):
    identifier = call.data.replace("msg_stu_", "")
    await state.update_data(target_student_id=identifier)
    await state.set_state(BotStates.send_student_message)

    buttons = [[s_btn("إلغاء والعودة", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]]
    await safe_edit_or_reply(
        call,
        f"{tg_e('CHAT', '✉️')} <b>إرسال رسالة للطالب / ولي الأمر:</b>\n\n"
        f"<blockquote>اكتب نص الرسالة التي تريد إرسالها للطالب (<code>{identifier}</code>) الآن في الشات:</blockquote>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.message(BotStates.send_student_message)
async def handle_send_student_message(message: Message, state: FSMContext):
    data = await state.get_data()
    identifier = data.get("target_student_id")
    msg_text = message.text.strip()
    await state.clear()

    async with AsyncSessionLocal() as db:
        q = select(User).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user:
            await message.answer("لم يتم العثور على الطالب.")
            return

        # 1. Save in system notifications table
        notif = Notification(
            user_id=user.id,
            title="رسالة خاصة من المعلم الإداري 👨‍🏫",
            message=msg_text,
            type="admin_message",
            is_read=False
        )
        db.add(notif)

        # 2. Check if parent Telegram is linked and forward
        tg_q = select(TelegramAccount).where(TelegramAccount.linked_user_id == user.id)
        tg_acc = (await db.execute(tg_q)).scalar_one_or_none()
        forwarded = False
        if tg_acc and tg_acc.telegram_chat_id:
            try:
                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                await bot.send_message(
                    chat_id=int(tg_acc.telegram_chat_id),
                    text=f"👨‍🏫 <b>رسالة خاصة من إدارة منصة ABC لولي أمر الطالب ({user.full_name}):</b>\n\n<blockquote>{msg_text}</blockquote>",
                    parse_mode="HTML"
                )
                await bot.session.close()
                forwarded = True
            except Exception as e:
                logger.warning(f"Could not forward to Telegram parent: {e}")

        await db.commit()

        status_msg = "وتم تسليمها أيضاً مباشرة لحساب ولي الأمر في Telegram 📱" if forwarded else "وستظهر في صندوق إشعارات الطالب عند دخوله الموقع 💻"
        buttons = [[s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="primary", emoji_key="STUDENT")]]
        await message.answer(
            f"{tg_e('CHECK', '✅')} <b>تم إرسال الرسالة بنجاح!</b>\n\n"
            f"<blockquote>👤 الطالب: <b>{user.full_name}</b>\n{status_msg}</blockquote>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Adaptive Plan Details
@dp.callback_query(F.data.startswith("ai_plan_"))
async def cb_view_ai_plan(call: CallbackQuery):
    identifier = call.data.replace("ai_plan_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if not user or not user.student_profile:
            await call.answer("بيانات الطالب غير متوفرة", show_alert=True)
            return

        w_q = select(StudentWeakness).where(and_(StudentWeakness.student_id == user.student_profile.id, StudentWeakness.is_resolved == False))
        weaknesses = (await db.execute(w_q)).scalars().all()

        text = (
            f"{tg_e('BRAIN', '🧠')} <b>خطة التدريب التكيفية للذكاء الاصطناعي:</b>\n\n"
            f"<blockquote>"
            f"👤 <b>الطالب:</b> <code>{user.full_name}</code>\n"
            f"🎯 <b>الهدف:</b> علاج التعثر في نطق المقاطع الصوتية وإتقان مخارج الحروف.\n\n"
        )
        if weaknesses:
            text += "<b>المقاطع التي تحتاج إلى تكرار وتدريب:</b>\n"
            for w in weaknesses:
                text += f"• <code>/{w.phoneme_or_skill}/</code> - تم رصد {w.error_count} أخطاء نطق غير دقيقة.\n"
            text += "\n💡 <i>يقوم الموقع تلقائياً بزيادة تكرار هذه الكلمات للطالب حتى يتقنها بنسبة 100%.</i>"
        else:
            text += "🌟 <b>لا توجد صعوبات حالية! نطق الطالب سليم ومتقن.</b>"
        text += "</blockquote>"

        buttons = [
            [s_btn("تحديد مستوى إضافي", f"set_lvl_{identifier}", style="primary", emoji_key="SPARKLES")],
            [s_btn("العودة لملف الطالب", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Toggle Account Active / Inactive
@dp.callback_query(F.data.startswith("toggle_stu_"))
async def cb_toggle_student(call: CallbackQuery):
    identifier = call.data.replace("toggle_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if user:
            user.is_active = not user.is_active
            await db.commit()
            status_text = "تفعيل" if user.is_active else "إيقاف"
            await call.answer(f"تم {status_text} حساب الطالب بنجاح!", show_alert=True)
            new_call = call.model_copy(update={"data": f"view_stu_{identifier}"})
            await cb_view_student(new_call)

# Level Setting for Student (50 Levels Selector)
@dp.callback_query(F.data.startswith("set_lvl_"))
async def cb_set_level_menu(call: CallbackQuery):
    identifier = call.data.replace("set_lvl_", "")
    buttons = [
        [
            s_btn("Stage 1 (L1-10 Phonics)", f"lvl_stage_{identifier}_1", style="primary", emoji_key="SPARKLES"),
            s_btn("Stage 2 (L11-20 Talk)", f"lvl_stage_{identifier}_11", style="primary", emoji_key="CHAT")
        ],
        [
            s_btn("Stage 3 (L21-35 Fluency)", f"lvl_stage_{identifier}_21", style="primary", emoji_key="STAR"),
            s_btn("Stage 4 (L36-45 Pro)", f"lvl_stage_{identifier}_36", style="primary", emoji_key="TROPHY")
        ],
        [
            s_btn("Stage 5 (L46-50 Native)", f"lvl_stage_{identifier}_46", style="success", emoji_key="TROPHY")
        ],
        [
            s_btn("إلغاء والعودة", f"view_stu_{identifier}", style="danger", emoji_key="DANGER")
        ]
    ]

    await safe_edit_or_reply(
        call,
        f"{tg_e('SPARKLES', '🎯')} <b>تحديد المستوى للطالب ({identifier}):</b>\n"
        f"<blockquote>اختر المرحلة اللغوية من الـ 50 مستوى:</blockquote>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data.startswith("lvl_stage_"))
async def cb_lvl_stage_selector(call: CallbackQuery):
    parts = call.data.replace("lvl_stage_", "").split("_")
    identifier = parts[0]
    start_lvl = int(parts[1])
    end_lvl = min(50, start_lvl + 9 if start_lvl != 21 else 35)

    buttons = []
    row = []
    for i in range(start_lvl, end_lvl + 1):
        row.append(s_btn(f"L{i}", f"apply_lvl_{identifier}_{i}", style="primary", emoji_key="STAR"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([s_btn("رجوع لاختيار المرحلة", f"set_lvl_{identifier}", style="danger", emoji_key="DANGER")])

    await safe_edit_or_reply(
        call,
        f"{tg_e('PIN')} <b>اختر المستوى الدقيق للطالب ({start_lvl} إلى {end_lvl}):</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data.startswith("apply_lvl_"))
async def cb_apply_level(call: CallbackQuery):
    parts = call.data.replace("apply_lvl_", "").split("_")
    identifier = parts[0]
    lvl_num = int(parts[1])

    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()
        if user and user.student_profile:
            user.student_profile.current_level_id = lvl_num
            await db.commit()
            await call.answer(f"تم تغيير مستوى الطالب إلى Level {lvl_num} بنجاح!", show_alert=True)
            new_call = call.model_copy(update={"data": f"view_stu_{identifier}"})
            await cb_view_student(new_call)

# Review & Grade Homework Submissions
@dp.callback_query(F.data.startswith("sub_rev_"))
async def cb_review_submission(call: CallbackQuery):
    sub_id = int(call.data.replace("sub_rev_", ""))
    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment),
            selectinload(AssignmentSubmission.feedback)
        ).where(AssignmentSubmission.id == sub_id)
        sub = (await db.execute(q)).scalar_one_or_none()

        if not sub:
            await call.answer("لم يتم العثور على هذا الواجب", show_alert=True)
            return

        s_name = sub.student.user.full_name if (sub.student and sub.student.user) else "Student"
        s_id = sub.student.user.student_id if (sub.student and sub.student.user) else "STU"
        hw_title = sub.assignment.title if sub.assignment else "Homework"
        status_label = "تم التصحيح والاعتماد ✅" if sub.status == "graded" else ("يحتاج إعادة ⚠️" if sub.status == "needs_retry" else "بانتظار المراجعة ⏳")
        current_score = f"{sub.feedback.score}%" if (sub.feedback and sub.feedback.score is not None) else "لم ترصد بعد"

        text = (
            f"{tg_e('CAMERA', '📝')} <b>مراجعة تسليم واجب الدفتر:</b>\n\n"
            f"<blockquote>"
            f"👤 <b>الطالب:</b> <code>{s_name}</code> (<code>{s_id}</code>)\n"
            f"📖 <b>الواجب:</b> <i>{hw_title}</i>\n"
            f"✍️ <b>النوع:</b> كتابة ورقية بخط اليد وتصوير الكراسة\n"
            f"📅 <b>تاريخ التسليم:</b> <code>{sub.submitted_at.strftime('%Y-%m-%d %H:%M') if sub.submitted_at else 'الآن'}</code>\n"
            f"📊 <b>الحالة:</b> <b>{status_label}</b>\n"
            f"⭐ <b>الدرجة الحالية:</b> <b>{current_score}</b>\n"
            f"</blockquote>"
        )

        buttons = [
            [
                s_btn("رصد الدرجة (تصحيح فوري)", f"sub_grade_{sub.id}", style="success", emoji_key="CHECK"),
                s_btn("طلب إعادة الواجب بخط أوضح", f"sub_retry_{sub.id}", style="danger", emoji_key="ALERT")
            ],
            [
                s_btn("العودة لقائمة التسليمات", "menu_submissions", style="danger", emoji_key="DANGER")
            ]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("sub_retry_"))
async def cb_sub_retry(call: CallbackQuery):
    sub_id = int(call.data.replace("sub_retry_", ""))
    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.feedback)
        ).where(AssignmentSubmission.id == sub_id)
        sub = (await db.execute(q)).scalar_one_or_none()

        if not sub:
            await call.answer("لم يتم العثور على التسليم", show_alert=True)
            return

        sub.status = "needs_retry"
        comment = "يرجى إعادة كتابة الواجب بخط أجمل وأوضح بين الأسطر الأربعة وإعادة تصوير الصفحة ✍️"

        if sub.feedback:
            sub.feedback.score = 40
            sub.feedback.comments = comment
            sub.feedback.retry_requested = True
            sub.feedback.reviewed_at = datetime.utcnow()
        else:
            fb = AssignmentFeedback(
                submission_id=sub.id,
                score=40,
                comments=comment,
                retry_requested=True,
                reviewed_at=datetime.utcnow()
            )
            db.add(fb)

        await db.commit()
        await call.answer("تم إشعار الطالب بإعادة كتابة الواجب بخط أفضل ✍️", show_alert=True)
        new_call = call.model_copy(update={"data": f"sub_rev_{sub_id}"})
        await cb_review_submission(new_call)

@dp.callback_query(F.data.startswith("sub_grade_"))
async def cb_grade_options(call: CallbackQuery):
    sub_id = int(call.data.replace("sub_grade_", ""))
    buttons = [
        [
            s_btn("100% ممتاز جداً", f"apply_grade_{sub_id}_100", style="success", emoji_key="STAR"),
            s_btn("90% رائع", f"apply_grade_{sub_id}_90", style="success", emoji_key="CHECK")
        ],
        [
            s_btn("80% جيد جداً", f"apply_grade_{sub_id}_80", style="primary", emoji_key="THUMB_UP"),
            s_btn("70% مقبول", f"apply_grade_{sub_id}_70", style="primary", emoji_key="THUMB_UP")
        ],
        [
            s_btn("إلغاء", f"sub_rev_{sub_id}", style="danger", emoji_key="DANGER")
        ]
    ]

    await safe_edit_or_reply(
        call,
        f"{tg_e('STAR')} <b>رصد درجة الواجب رقم #{sub_id}:</b>\n"
        f"<blockquote>اختر التقييم لرصده فوراً ومكافأة الطالب بالنجوم ونقاط الخبرة XP:</blockquote>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data.startswith("apply_grade_"))
async def cb_apply_grade(call: CallbackQuery):
    parts = call.data.replace("apply_grade_", "").split("_")
    sub_id = int(parts[0])
    score = int(parts[1])

    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment),
            selectinload(AssignmentSubmission.feedback)
        ).where(AssignmentSubmission.id == sub_id)
        sub = (await db.execute(q)).scalar_one_or_none()

        if not sub:
            await call.answer("لم يتم العثور على التسليم", show_alert=True)
            return

        sub.status = "graded"
        comment = "خط ممتاز ومجهود رائع جداً! بارك الله فيك وحقق المزيد من التقدم 🌟"

        if sub.feedback:
            sub.feedback.score = score
            sub.feedback.comments = comment
            sub.feedback.retry_requested = False
            sub.feedback.reviewed_at = datetime.utcnow()
        else:
            fb = AssignmentFeedback(
                submission_id=sub.id,
                score=score,
                comments=comment,
                retry_requested=False,
                reviewed_at=datetime.utcnow()
            )
            db.add(fb)

        # Award student XP and Stars
        if sub.student:
            sub.student.xp = (sub.student.xp or 0) + 50
            sub.student.stars = (sub.student.stars or 0) + 3

            # Also ensure next level is unlocked and active for the student
            if sub.assignment:
                next_lvl_num = sub.assignment.level_id + 1
                if next_lvl_num <= 50:
                    acc_q = select(StudentLevelAccess).where(
                        and_(StudentLevelAccess.student_id == sub.student.id, StudentLevelAccess.level_id == next_lvl_num)
                    )
                    acc = (await db.execute(acc_q)).scalar_one_or_none()
                    if not acc:
                        acc = StudentLevelAccess(
                            student_id=sub.student.id,
                            level_id=next_lvl_num,
                            is_unlocked=True,
                            unlocked_by="teacher_grading"
                        )
                        db.add(acc)
                    else:
                        acc.is_unlocked = True

                    if (sub.student.current_level_id or 1) <= sub.assignment.level_id:
                        sub.student.current_level_id = next_lvl_num

        await db.commit()

        await call.answer(f"تم رصد درجة {score}% ومنح الطالب +50 XP و+3 نجوم!", show_alert=True)

        buttons = [
            [s_btn("العودة للتسليمات", "menu_submissions", style="primary", emoji_key="CAMERA")],
            [s_btn("القائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]

        await safe_edit_or_reply(
            call,
            f"{tg_e('CHECK', '✅')} <b>تم تصحيح الواجب بنجاح!</b>\n\n"
            f"<blockquote>"
            f"👤 الطالب: <b>{sub.student.user.full_name if sub.student and sub.student.user else ''}</b>\n"
            f"⭐ الدرجة المرصودة: <b>{score}%</b>\n"
            f"🎁 تمت مكافأة الطالب بـ <b>+50 XP</b> و <b>+3 نجوم</b> وتم اعتماد الواجب في حسابه."
            f"</blockquote>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Section 4: Assignments Overview
@dp.callback_query(F.data == "menu_assignments")
async def cb_menu_assignments(call: CallbackQuery):
    text = (
        f"{tg_e('STAR', '📖')} <b>نظام الواجبات المنزلية وكراسة الخط:</b>\n\n"
        f"<blockquote>"
        f"✍️ <b>إلزامية الواجبات:</b> كل مستوى من الـ 50 له واجب كتابة دفتري مستقل بين الأسطر الأربعة.\n"
        f"📸 <b>طريقة التسليم:</b> يلتقط الطالب صورة لصفحة الكراسة ويرفعها قبل فتح المستوى التالي.\n"
        f"🔁 <b>شرط التكرار:</b> تكرار نطق وكتابة كل كلمة 3 مرات لتثبيت الحروف والأصوات بالذاكرة.\n"
        f"⭐ <b>المكافآت:</b> يحصل الطالب على <b>+50 XP</b> و <b>+3 نجوم</b> عند اعتماد الواجب.\n"
        f"</blockquote>\n"
        f"اختر المرحلة لعرض تفاصيل واجباتها:"
    )
    buttons = [
        [
            s_btn("واجبات المرحلة 1 (L1-10)", "hw_stage_1", style="primary", emoji_key="SPARKLES"),
            s_btn("واجبات المرحلة 2 (L11-20)", "hw_stage_11", style="primary", emoji_key="CHAT")
        ],
        [
            s_btn("تسليمات الطلاب المعلقة", "menu_submissions", style="success", emoji_key="CAMERA"),
            s_btn("التصحيح السريع", "menu_grading", style="success", emoji_key="CHECK")
        ],
        [
            s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")
        ]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("hw_stage_"))
async def cb_hw_stage_view(call: CallbackQuery):
    stage_start = int(call.data.replace("hw_stage_", ""))
    stage_end = stage_start + 9

    text = f"{tg_e('STAR')} <b>واجبات المستويات من Level {stage_start} إلى Level {stage_end}:</b>\n\n<blockquote>"
    for lvl in CURRICULUM_50_DATA[stage_start - 1 : stage_end]:
        num = lvl["level_number"]
        prompt = lvl.get("homework_prompt", "كتابة وتطبيق عملي")
        text += f"• <b>L{num} ({lvl['title'].split('–')[-1].strip()}):</b>\n  <i>{prompt}</i>\n\n"
    text += "</blockquote>"

    buttons = [
        [s_btn("العودة لقسم الواجبات", "menu_assignments", style="primary", emoji_key="STAR")],
        [s_btn("القائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 5: Submissions Management (Pending by default, Graded in separate Archive)
@dp.callback_query(F.data.in_(["menu_submissions", "sub_filter_pending", "sub_filter_graded"]))
async def cb_menu_submissions(call: CallbackQuery):
    show_graded = call.data == "sub_filter_graded"

    async with AsyncSessionLocal() as db:
        if show_graded:
            # Graded archive
            q = select(AssignmentSubmission).options(
                selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
                selectinload(AssignmentSubmission.assignment),
                selectinload(AssignmentSubmission.feedback)
            ).where(AssignmentSubmission.status == "graded").order_by(AssignmentSubmission.id.desc()).limit(15)
        else:
            # Pending & Needs Retry queue (Unresolved homework that needs teacher action)
            q = select(AssignmentSubmission).options(
                selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
                selectinload(AssignmentSubmission.assignment),
                selectinload(AssignmentSubmission.feedback)
            ).where(AssignmentSubmission.status.in_(["submitted", "needs_retry"])).order_by(AssignmentSubmission.id.desc()).limit(20)

        submissions = (await db.execute(q)).scalars().all()

        # Count stats
        pending_total_q = select(AssignmentSubmission).where(AssignmentSubmission.status == "submitted")
        pending_total = len((await db.execute(pending_total_q)).scalars().all())

        retry_total_q = select(AssignmentSubmission).where(AssignmentSubmission.status == "needs_retry")
        retry_total = len((await db.execute(retry_total_q)).scalars().all())

        graded_total_q = select(AssignmentSubmission).where(AssignmentSubmission.status == "graded")
        graded_total = len((await db.execute(graded_total_q)).scalars().all())

        text = f"{tg_e('CAMERA', '📝')} <b>إدارة تسليمات دفاتر الواجبات:</b>\n\n"
        buttons = []

        # Tabs row to switch between Pending Queue and Graded Archive
        tabs_row = [
            s_btn(
                f"📥 بانتظار التصحيح ({pending_total + retry_total})",
                "sub_filter_pending",
                style="success" if not show_graded else "primary",
                emoji_key="BELL"
            ),
            s_btn(
                f"🗄️ الأرشيف المصحح ({graded_total})",
                "sub_filter_graded",
                style="success" if show_graded else "primary",
                emoji_key="CHECK"
            )
        ]
        buttons.append(tabs_row)

        if not show_graded:
            if submissions:
                text += (
                    f"<blockquote>"
                    f"⏳ <b>قائمة الواجبات النشطة المطلوب تصحيحها:</b>\n"
                    f"• جديدة بانتظار الدرجة: <b>{pending_total}</b>\n"
                    f"• مطلوب إعادة كتابتها: <b>{retry_total}</b>\n"
                    f"<i>(الواجب يختفي تلقائياً من هنا فور تصحيحه ورصد درجته)</i>"
                    f"</blockquote>\n"
                )
                for sub in submissions:
                    s_name = sub.student.user.full_name if (sub.student and sub.student.user) else f"Student #{sub.student_id}"
                    hw_title = sub.assignment.title if sub.assignment else "Homework"
                    is_new = sub.status == "submitted"
                    status_icon = "BELL" if is_new else "ALERT"
                    status_desc = "جديد" if is_new else "طلب إعادة"
                    buttons.append([s_btn(
                        f"📝 {s_name} - {status_desc} (L{sub.assignment.level_id if sub.assignment else 1})",
                        f"sub_rev_{sub.id}",
                        style="primary" if is_new else "danger",
                        emoji_key=status_icon
                    )])
            else:
                text += (
                    f"<blockquote>"
                    f"🎉 <b>رائع جداً! لا توجد أي واجبات معلقة حالياً.</b>\n"
                    f"تم تصحيح واعتماد جميع الواجبات المسلمة بالكامل ونقلها للأرشيف."
                    f"</blockquote>\n"
                )
        else:
            # Viewing Graded Archive
            if submissions:
                text += f"<blockquote>🗄️ <b>أرشيف الواجبات المصححة والمعتمدة مؤخراً ({len(submissions)}):</b></blockquote>\n"
                for sub in submissions:
                    s_name = sub.student.user.full_name if (sub.student and sub.student.user) else f"Student #{sub.student_id}"
                    hw_title = sub.assignment.title if sub.assignment else "Homework"
                    score_str = f"{sub.feedback.score}%" if (sub.feedback and sub.feedback.score is not None) else "100%"
                    buttons.append([s_btn(
                        f"✅ {s_name} - {score_str} (L{sub.assignment.level_id if sub.assignment else 1})",
                        f"sub_rev_{sub.id}",
                        style="success",
                        emoji_key="CHECK"
                    )])
            else:
                text += "<blockquote><i>لا توجد واجبات معتمدة في الأرشيف بعد.</i></blockquote>\n"

        if not show_graded and submissions:
            buttons.append([s_btn("⚡ التصحيح الفوري المتتالي", "menu_grading", style="success", emoji_key="CHECK")])

        buttons.append([s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 6: Direct Grading Queue
@dp.callback_query(F.data == "menu_grading")
async def cb_menu_grading(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        # Find first pending submission
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment)
        ).where(AssignmentSubmission.status == "submitted").order_by(AssignmentSubmission.id.asc()).limit(1)

        pending = (await db.execute(q)).scalar_one_or_none()

        if pending:
            # Jump directly to review
            new_call = call.model_copy(update={"data": f"sub_rev_{pending.id}"})
            await cb_review_submission(new_call)
            return

        # No pending homework!
        text = (
            f"{tg_e('CHECK', '🎉')} <b>طابور تصحيح الواجبات الورقية:</b>\n\n"
            f"<blockquote>"
            f"✅ <b>لا توجد واجبات معلقة تنتظر التصحيح حالياً!</b>\n"
            f"جميع دفاتر وواجبات الطلاب تم تصحيحها واعتمادها بنجاح.\n"
            f"</blockquote>"
        )
        buttons = [
            [s_btn("عرض سجل جميع التسليمات", "menu_submissions", style="primary", emoji_key="CAMERA")],
            [s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 2: Levels Overview (50 Levels)
@dp.callback_query(F.data == "menu_levels")
async def cb_menu_levels(call: CallbackQuery):
    text = (
        f"{tg_e('SPARKLES', '📚')} <b>خريطة المستويات الـ 50 الكاملة لمنصة ABC:</b>\n\n"
        f"<blockquote>"
        f"🔤 <b>المرحلة 1 (L1 - L10):</b> التأسيس، أصوات الحروف، CVC، ودمج المقاطع الصوتية.\n"
        f"🗣️ <b>المرحلة 2 (L11 - L20):</b> المحادثة اليومية والتواصل الاجتماعي (المستوى 15 يتيح التحدث مع الأشخاص بثقة).\n"
        f"🌟 <b>المرحلة 3 (L21 - L35):</b> الطلاقة التعبيرية والأزمنة وسرد القصص المعبرة.\n"
        f"💼 <b>المرحلة 4 (L36 - L45):</b> الإنجليزية الاحترافية، المقابلات، والتعبيرات الاصطلاحية Idioms.\n"
        f"👑 <b>المرحلة 5 (L46 - L50):</b> الطلاقة المطلقة والتحدث بالإنجليزية كأنها لغتك الأم (Native Mastery)."
        f"</blockquote>"
    )
    buttons = [
        [
            s_btn("المرحلة 1 (L1-10)", "lvl_view_1", style="primary", emoji_key="SPARKLES"),
            s_btn("المرحلة 2 (L11-20)", "lvl_view_11", style="primary", emoji_key="CHAT")
        ],
        [
            s_btn("المرحلة 3 (L21-35)", "lvl_view_21", style="primary", emoji_key="STAR"),
            s_btn("المرحلة 4 (L36-45)", "lvl_view_36", style="primary", emoji_key="TROPHY")
        ],
        [
            s_btn("المرحلة 5 (L46-50)", "lvl_view_46", style="success", emoji_key="TROPHY")
        ],
        [
            s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")
        ]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("lvl_view_"))
async def cb_levels_stage_detail(call: CallbackQuery):
    stage_start = int(call.data.replace("lvl_view_", ""))
    stage_end = min(50, stage_start + (9 if stage_start != 21 else 14))

    text = f"{tg_e('SPARKLES')} <b>مستويات المرحلة من Level {stage_start} إلى Level {stage_end}:</b>\n\n<blockquote>"
    for lvl in CURRICULUM_50_DATA[stage_start - 1 : stage_end]:
        num = lvl["level_number"]
        title = lvl["title"]
        sub = lvl["subtitle"]
        text += f"• <b>L{num}:</b> {title} ({sub})\n"
    text += "</blockquote>"

    buttons = [
        [s_btn("عرض تفاصيل الدروس", "menu_lessons", style="primary", emoji_key="PIN")],
        [s_btn("رجوع لخريطة المستويات", "menu_levels", style="danger", emoji_key="DANGER")]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 3: Lessons Management
@dp.callback_query(F.data == "menu_lessons")
async def cb_menu_lessons(call: CallbackQuery):
    text = (
        f"{tg_e('PIN', '📑')} <b>قسم إدارة واستعراض الدروس التعليمية (50 درساً):</b>\n\n"
        f"<blockquote>"
        f"يحتوي كل درس على:\n"
        f"1. أصوات الحروف والمقاطع الصوتية Phonics\n"
        f"2. الكلمات الثلاثية والمفردات مع النطق الصوتي\n"
        f"3. جمل القراءة السريعة والطلاقة\n"
        f"4. تدريبات النطق الصوتي التفاعلي للطفل بالذكاء الاصطناعي\n"
        f"5. كراسة الواجب الكتابي الإلزامي\n"
        f"</blockquote>\n"
        f"اختر المرحلة لاستعراض محتويات دروسها:"
    )
    buttons = [
        [
            s_btn("دروس التأسيس (L1-10)", "les_stage_1", style="primary", emoji_key="SPARKLES"),
            s_btn("دروس المحادثة (L11-20)", "les_stage_11", style="primary", emoji_key="CHAT")
        ],
        [
            s_btn("دروس الطلاقة (L21-35)", "les_stage_21", style="primary", emoji_key="STAR"),
            s_btn("دروس الإتقان (L36-50)", "les_stage_36", style="success", emoji_key="TROPHY")
        ],
        [
            s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")
        ]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("les_stage_"))
async def cb_lessons_stage_list(call: CallbackQuery):
    stage_start = int(call.data.replace("les_stage_", ""))
    stage_end = min(50, stage_start + (9 if stage_start != 21 else 14))

    buttons = []
    row = []
    for i in range(stage_start, stage_end + 1):
        row.append(s_btn(f"درس L{i}", f"les_detail_{i}", style="primary", emoji_key="PIN"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([s_btn("رجوع لإدارة الدروس", "menu_lessons", style="danger", emoji_key="DANGER")])

    await safe_edit_or_reply(
        call,
        f"{tg_e('PIN')} <b>اختر الدرس لعرض محتوياته (المستويات {stage_start} - {stage_end}):</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data.startswith("les_detail_"))
async def cb_lesson_detail(call: CallbackQuery):
    lvl_num = int(call.data.replace("les_detail_", ""))
    lvl = CURRICULUM_50_DATA[lvl_num - 1]

    letters_str = ", ".join([l["symbol"] for l in lvl.get("letters", [])]) or "محادثة وطلاقة"
    words_str = ", ".join([w["word"] for w in lvl.get("words", [])[:6]])
    sentences = lvl.get("sentences", [])
    sentence_sample = sentences[0]["text"] if sentences else "Everyday speech"

    text = (
        f"{tg_e('PIN', '📖')} <b>تفاصيل محتوى الدرس: Level {lvl_num}</b>\n\n"
        f"<blockquote>"
        f"🏷️ <b>العنوان:</b> {lvl['title']}\n"
        f"📌 <b>الموضوع:</b> <i>{lvl['subtitle']}</i>\n"
        f"🔤 <b>الأصوات والحروف:</b> <code>{letters_str}</code>\n"
        f"📚 <b>الكلمات المستهدفة:</b> <code>{words_str}</code>\n"
        f"💬 <b>نموذج جمل القراءة:</b> <i>\"{sentence_sample}\"</i>\n"
        f"✍️ <b>الواجب المنزلي:</b> {lvl.get('homework_prompt', '')}\n"
        f"</blockquote>"
    )

    stage_start = 1 if lvl_num <= 10 else (11 if lvl_num <= 20 else (21 if lvl_num <= 35 else 36))
    buttons = [
        [s_btn("العودة لقائمة الدروس", f"les_stage_{stage_start}", style="primary", emoji_key="PIN")],
        [s_btn("القائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
    ]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 7: Quizzes & Results
@dp.callback_query(F.data == "menu_quizzes")
async def cb_menu_quizzes(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        total_quizzes = 50
        total_attempts = await db.scalar(select(func.count(QuizResult.id))) or 0
        passed_attempts = await db.scalar(select(func.count(QuizResult.id)).where(QuizResult.passed == True)) or 0
        pass_rate = round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 100.0

        q_recent = select(QuizResult).options(
            selectinload(QuizResult.student).selectinload(StudentProfile.user)
        ).order_by(QuizResult.id.desc()).limit(5)
        recent_results = (await db.execute(q_recent)).scalars().all()

        text = (
            f"{tg_e('STAR', '🎯')} <b>قسم الاختبارات والتقييمات (50 كويز):</b>\n\n"
            f"<blockquote>"
            f"📚 <b>عدد الاختبارات:</b> <code>50</code> اختبار (اختبار لكل مستوى)\n"
            f"📝 <b>الأسئلة:</b> 4 خيارات لكل سؤال دون تسريب للإجابة\n"
            f"🎯 <b>شرط الاجتياز:</b> <b>80% على الأقل</b> + بلوغ الـ XP المطلوب\n"
            f"📊 <b>إجمالي محاولات الاختبارات:</b> <code>{total_attempts}</code> محاولة\n"
            f"🏆 <b>نسبة النجاح العامة:</b> <b>{pass_rate}%</b>\n"
            f"</blockquote>\n"
        )

        if recent_results:
            text += "<b>آخر نتائج الاختبارات:</b>\n<blockquote>"
            for r in recent_results:
                s_name = r.student.user.full_name if (r.student and r.student.user) else "طالب"
                status = "ناجح ✅" if r.passed else "إعادة ❌"
                text += f"• {s_name} - Level {r.quiz_id}: <b>{r.score}%</b> ({status})\n"
            text += "</blockquote>"

        buttons = [
            [s_btn("تحديث النتائج", "menu_quizzes", style="primary", emoji_key="SPARKLES")],
            [s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 8: AI Teacher & Pronunciation
@dp.callback_query(F.data == "menu_ai_teacher")
async def cb_menu_ai_teacher(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        total_attempts = await db.scalar(select(func.count(PronunciationAttempt.id))) or 0
        avg_score = await db.scalar(select(func.avg(PronunciationAttempt.overall_score))) or 85.0
        active_weaknesses = await db.scalar(select(func.count(StudentWeakness.id)).where(StudentWeakness.is_resolved == False)) or 0

        text = (
            f"{tg_e('BRAIN', '🧠')} <b>مدرس الذكاء الاصطناعي ومحلل النطق الصوتي:</b>\n\n"
            f"<blockquote>"
            f"🎙️ <b>إجمالي جلسات النطق المحللة:</b> <code>{total_attempts}</code> جلسة صوتية\n"
            f"⭐ <b>متوسط درجات النطق الدقيقة:</b> <b>{round(float(avg_score), 1)}/100</b>\n"
            f"⚠️ <b>المقاطع الصوتية الجاري تصحيحها:</b> <code>{active_weaknesses}</code> صوت\n"
            f"🧩 <b>خوارزمية التحليل:</b> مطابقة الفونيمات الصوتية مع التسجيل الصوتي للطفل بدقة وتحديد مواضع الخطأ.\n"
            f"</blockquote>"
        )
        buttons = [
            [s_btn("قائمة الطلاب ذوي صعوبات النطق", "stu_list_weakness", style="danger", emoji_key="ALERT")],
            [s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 9: Student Reports
@dp.callback_query(F.data == "menu_student_reports")
async def cb_menu_student_reports(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        total_students = await db.scalar(select(func.count(User.id)).where(User.role == "student")) or 0
        stage1_count = await db.scalar(select(func.count(StudentProfile.id)).where(StudentProfile.current_level_id <= 10)) or 0
        stage2_count = await db.scalar(select(func.count(StudentProfile.id)).where(and_(StudentProfile.current_level_id >= 11, StudentProfile.current_level_id <= 20))) or 0
        advanced_count = await db.scalar(select(func.count(StudentProfile.id)).where(StudentProfile.current_level_id >= 21)) or 0

        text = (
            f"{tg_e('STATS', '📈')} <b>تقارير أداء الطلاب الشاملة:</b>\n\n"
            f"<blockquote>"
            f"👥 <b>إجمالي الطلاب:</b> <code>{total_students}</code> طالب\n\n"
            f"<b>توزيع الطلاب على المراحل التعليمية:</b>\n"
            f"• المرحلة 1 (التأسيس الصوتي L1-10): <b>{stage1_count}</b> طالب\n"
            f"• المرحلة 2 (المحادثة والتحدث L11-20): <b>{stage2_count}</b> طالب\n"
            f"• المرحلة 3 فأعلى (الطلاقة والإتقان): <b>{advanced_count}</b> طالب\n"
            f"</blockquote>"
        )
        buttons = [
            [s_btn("عرض جميع الطلاب", "stu_list_all", style="primary", emoji_key="STUDENT")],
            [s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 10: Teachers Management
@dp.callback_query(F.data == "menu_teachers")
async def cb_menu_teachers(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(User).where(User.role == "teacher")
        teachers = (await db.execute(q)).scalars().all()

        text = (
            f"{tg_e('STUDENT', '👨‍🏫')} <b>قسم إدارة المدرسين والمعلمين:</b>\n\n"
            f"<blockquote>"
            f"المعلمون لديهم صلاحية متابعة الطلاب، تصحيح الواجبات الورقية، ورصد الملاحظات الصوتية.\n\n"
            f"<b>المعلمون المسجلون ({len(teachers)}):</b>\n"
        )
        if teachers:
            for t in teachers:
                text += f"• <b>{t.full_name}</b> (هاتف: <code>{t.phone_number}</code>)\n"
        else:
            text += "• <i>لا يوجد مدرسون إضافيون مسجلون حالياً (أنت المدير العام للمنصة).</i>\n"
        text += "</blockquote>"

        buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 11: Parents Management
@dp.callback_query(F.data == "menu_parents")
async def cb_menu_parents(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(TelegramAccount).where(TelegramAccount.role == "parent")
        linked_parents = (await db.execute(q)).scalars().all()

        text = (
            f"{tg_e('CHAT', '👨‍👩‍👧‍👦')} <b>إدارة أولياء الأمور وحسابات Telegram:</b>\n\n"
            f"<blockquote>"
            f"📱 <b>أولياء الأمور المرتبطون بالبوت:</b> <code>{len(linked_parents)}</code> ولي أمر\n\n"
            f"<b>طريقة ربط ولي الأمر بحسابه:</b>\n"
            f"1. يسجل الطالب دخوله في المنصة عبر الموقع.\n"
            f"2. يضغط على زر <b>(ربط Telegram)</b> للحصول على رمز 6 أرقام.\n"
            f"3. يرسل الأمر هنا في البوت: <code>/link 123456</code>\n"
            f"يتم ربطه فوراً وتصله إشعارات تصحيح الواجبات وتنبيهات المستوى.\n"
            f"</blockquote>"
        )
        buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 12: Notifications
@dp.callback_query(F.data == "menu_notifications")
async def cb_menu_notifications(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(Notification).order_by(Notification.id.desc()).limit(8)
        notifs = (await db.execute(q)).scalars().all()

        text = (
            f"{tg_e('BELL', '🔔')} <b>قسم الإشعارات والتنبيهات:</b>\n\n"
            f"<blockquote>"
            f"سجل الإشعارات المرسلة للطلاب وأولياء الأمور عبر الموقع والبوت:\n\n"
        )
        if notifs:
            for n in notifs:
                text += f"• <b>{n.title}:</b> {n.message[:45]}...\n"
        else:
            text += "• <i>لا توجد إشعارات سابقة مسجلة.</i>\n"
        text += "</blockquote>"

        buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 13: Certificates & Rewards
@dp.callback_query(F.data == "menu_certificates")
async def cb_menu_certificates(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q_top = select(User).join(StudentProfile).where(User.role == "student").order_by(StudentProfile.xp.desc()).limit(5)
        top_students = (await db.execute(q_top)).scalars().all()

        text = (
            f"{tg_e('TROPHY', '🏆')} <b>لوحة الشرف والمكافآت والشهادات:</b>\n\n"
            f"<blockquote>"
            f"📜 <b>شهادات المنصة المعتمدة:</b>\n"
            f"1. شهادة إتقان القراءة والصوتيات (المستوى 10)\n"
            f"2. شهادة التحدث والمحادثات الاجتماعية (المستوى 15)\n"
            f"3. شهادة الطلاقة المطلقة كمتحدث أصلي (المستوى 50)\n\n"
            f"<b>أفضل الطلاب حسب نقاط الـ XP:</b>\n"
        )
        if top_students:
            for idx, s in enumerate(top_students, 1):
                prof = s.student_profile
                text += f"{idx}. <b>{s.full_name}</b> - {prof.xp} XP | {prof.stars} ⭐ (L{prof.current_level_id})\n"
        else:
            text += "• <i>سيظهر المتصدرون بمجرد بدء الطلاب بحل الدروس.</i>\n"
        text += "</blockquote>"

        buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 14: General Settings
@dp.callback_query(F.data == "menu_settings")
async def cb_menu_settings(call: CallbackQuery):
    text = (
        f"{tg_e('GEAR', '⚙️')} <b>الإعدادات العامة لمنصة ABC:</b>\n\n"
        f"<blockquote>"
        f"🎯 <b>نسبة اجتياز الاختبارات:</b> <code>80%</code>\n"
        f"✍️ <b>تسليم الواجب الدفتري:</b> <code>إلزامي قبل فتح المستوى التالي</code>\n"
        f"🔁 <b>مرات التكرار الصوتي:</b> <code>3 مرات (1/3, 2/3, 3/3)</code>\n"
        f"📈 <b>معادلة نقاط التقدم:</b> <code>50 * (Level - 1)^2 XP</code>\n"
        f"🤖 <b>محرك الذكاء الاصطناعي:</b> <code>Acoustic & Phoneme Assessment Ready</code>\n"
        f"🌐 <b>نطاق المنصة:</b> <code>Live Production Mode</code>\n"
        f"</blockquote>"
    )
    buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 15: Comprehensive Statistics
@dp.callback_query(F.data == "menu_stats")
async def cb_menu_stats(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        total_students = await db.scalar(select(func.count(User.id)).where(User.role == "student")) or 0
        active_students = await db.scalar(select(func.count(User.id)).where(and_(User.role == "student", User.is_active == True))) or 0
        total_attempts = await db.scalar(select(func.count(PronunciationAttempt.id))) or 0
        avg_score = await db.scalar(select(func.avg(PronunciationAttempt.overall_score))) or 85.0
        total_submissions = await db.scalar(select(func.count(AssignmentSubmission.id))) or 0
        pending_submissions = await db.scalar(select(func.count(AssignmentSubmission.id)).where(AssignmentSubmission.status == "submitted")) or 0

        text = (
            f"{tg_e('STATS', '📈')} <b>التقرير والإحصائيات الشاملة لمنصة ABC:</b>\n\n"
            f"<blockquote>"
            f"👥 <b>إجمالي الطلاب:</b> <code>{total_students}</code> طالب\n"
            f"✅ <b>الطلاب النشطون:</b> <code>{active_students}</code> طالب\n"
            f"⛔ <b>الطلاب الموقوفون:</b> <code>{total_students - active_students}</code> طالب\n"
            f"📝 <b>واجبات الخط الورقية:</b> <code>{total_submissions}</code> تسليم (<b>{pending_submissions}</b> بانتظار المراجعة)\n"
            f"🎙️ <b>محاولات النطق الصوتي:</b> <code>{total_attempts}</code> محاولة\n"
            f"⭐ <b>متوسط درجات النطق AI:</b> <b>{round(float(avg_score), 1)}/100</b>\n"
            f"📚 <b>إجمالي مستويات المنهج:</b> <b>50 مستوى لغوي كامل</b>\n"
            f"</blockquote>"
        )

        buttons = [
            [s_btn("تحديث الإحصائيات", "menu_stats", style="primary", emoji_key="SPARKLES")],
            [s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Fallback callback handler
@dp.callback_query()
async def cb_fallback(call: CallbackQuery):
    try:
        await call.answer("⚡ جاري تحديث البيانات...", show_alert=False)
    except Exception:
        pass

async def start_bot():
    """Bot runner loop"""
    if not settings.TELEGRAM_BOT_TOKEN:
        print("[Telegram Bot] Bot token not provided in TELEGRAM_BOT_TOKEN environment variable. Bot polling paused.")
        return

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    print("Starting Telegram Bot Polling (aiogram 3) with styled buttons and custom emojis...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Telegram Bot Polling error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_bot())
