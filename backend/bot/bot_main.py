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
from bot.bot_styles import tg_e, s_btn, EMOJIS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM States
class BotStates(StatesGroup):
    search_student_query = State()
    search_type = State()
    send_student_message = State()
    target_student_id = State()

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

        res = await db.execute(q)
        students = res.scalars().all()

        if not students:
            await safe_edit_or_reply(
                call,
                f"{tg_e('ALERT', '📭')} لا يوجد طلاب مسجلون في هذه القائمة حالياً.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")]])
            )
            return

        buttons = []
        for s in students:
            style = "success" if s.is_active else "danger"
            emoji_key = "CHECK" if s.is_active else "DANGER"
            buttons.append([s_btn(
                f"{s.full_name} ({s.student_id or 'STU'})",
                f"view_stu_{s.student_id or s.id}",
                style=style,
                emoji_key=emoji_key
            )])
        buttons.append([s_btn("رجوع لإدارة الطلاب", "menu_students", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(
            call,
            f"{tg_e('STUDENT')} <b>قائمة الطلاب ({len(students)} طالب):</b>\n"
            f"<blockquote>اضغط على اسم الطالب لعرض ملفه بالكامل والتحكم به:</blockquote>",
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
                f"{tg_e('STAR', '🌟')} <b>ممتاز! لا توجد صعوبات نطق مستمرة لدى الطلاب حالياً.</b>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[s_btn("رجوع", "menu_students", style="danger", emoji_key="DANGER")]])
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
            call.data = f"view_stu_{identifier}"
            await cb_view_student(call)

# Level Setting for Student (50 Levels Selector)
@dp.callback_query(F.data.startswith("set_lvl_"))
async def cb_set_level_menu(call: CallbackQuery):
    identifier = call.data.replace("set_lvl_", "")
    # Show stage choices or quick jumps
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
            call.data = f"view_stu_{identifier}"
            await cb_view_student(call)

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
        status_label = "تم التصحيح والاعتماد" if sub.status == "graded" else "بانتظار المراجعة"
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

# Section 5 & 6: Assignments & Submissions
@dp.callback_query(F.data.in_(["menu_assignments", "menu_submissions", "menu_grading"]))
async def cb_menu_assignments(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment)
        ).where(AssignmentSubmission.status == "submitted").order_by(AssignmentSubmission.id.desc()).limit(10)

        submissions = (await db.execute(q)).scalars().all()

        text = f"{tg_e('CAMERA', '📝')} <b>قسم الواجبات وتسليمات الدفاتر:</b>\n\n"
        buttons = []

        if submissions:
            text += f"<blockquote>🔔 <b>يوجد {len(submissions)} واجب كتابة ورقية بانتظار التصحيح:</b></blockquote>\n"
            for sub in submissions:
                s_name = sub.student.user.full_name if (sub.student and sub.student.user) else f"Student #{sub.student_id}"
                hw_title = sub.assignment.title if sub.assignment else "Homework"
                buttons.append([s_btn(
                    f"{s_name} - {hw_title[:20]}",
                    f"sub_rev_{sub.id}",
                    style="primary",
                    emoji_key="CAMERA"
                )])
        else:
            text += "<blockquote>✅ <i>جميع تسليمات الطلاب تم تصحيحها واعتمادها بالكامل!</i></blockquote>\n"

        buttons.append([s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")])

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 2 & 3: Levels Overview (50 Levels)
@dp.callback_query(F.data.in_(["menu_levels", "menu_lessons"]))
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
    buttons = [[s_btn("العودة للقائمة الرئيسية", "main_menu", style="danger", emoji_key="DANGER")]]
    await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Fallback callback handler
@dp.callback_query()
async def cb_fallback(call: CallbackQuery):
    try:
        await call.answer("تم استلام الطلب.", show_alert=False)
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
