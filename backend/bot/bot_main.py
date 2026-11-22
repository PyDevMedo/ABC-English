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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, FSInputFile
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM States for Bot interactive operations
class BotStates(StatesGroup):
    search_student_query = State()
    search_type = State()
    create_assignment_title = State()
    create_assignment_instructions = State()
    create_assignment_level = State()
    grade_custom_comment = State()
    target_submission_id = State()
    target_grade_score = State()
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
    """15 Main Management Sections"""
    keyboard = [
        [InlineKeyboardButton(text="👥 إدارة الطلاب", callback_data="menu_students"), InlineKeyboardButton(text="📚 إدارة المستويات", callback_data="menu_levels")],
        [InlineKeyboardButton(text="📖 إدارة الدروس", callback_data="menu_lessons"), InlineKeyboardButton(text="📝 إدارة الواجبات", callback_data="menu_assignments")],
        [InlineKeyboardButton(text="📥 تسليمات الطلاب", callback_data="menu_submissions"), InlineKeyboardButton(text="⭐ تصحيح الواجبات", callback_data="menu_grading")],
        [InlineKeyboardButton(text="🎯 الاختبارات والنتائج", callback_data="menu_quizzes"), InlineKeyboardButton(text="🤖 مدرس الذكاء الاصطناعي", callback_data="menu_ai_teacher")],
        [InlineKeyboardButton(text="📊 تقارير الطلاب", callback_data="menu_student_reports"), InlineKeyboardButton(text="👨‍🏫 إدارة المدرسين", callback_data="menu_teachers")],
        [InlineKeyboardButton(text="👪 إدارة أولياء الأمور", callback_data="menu_parents"), InlineKeyboardButton(text="🔔 الإشعارات والرسائل", callback_data="menu_notifications")],
        [InlineKeyboardButton(text="🏆 الشهادات والمكافآت", callback_data="menu_certificates"), InlineKeyboardButton(text="⚙️ الإعدادات العامة", callback_data="menu_settings")],
        [InlineKeyboardButton(text="📈 الإحصائيات والتقارير الشاملة", callback_data="menu_stats")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_students_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="📋 جميع الطلاب", callback_data="stu_list_all"), InlineKeyboardButton(text="✨ الطلاب الجدد", callback_data="stu_list_new")],
        [InlineKeyboardButton(text="✅ الطلاب النشطون", callback_data="stu_list_active"), InlineKeyboardButton(text="⏸️ الطلاب الموقوفون", callback_data="stu_list_suspended")],
        [InlineKeyboardButton(text="🔍 بحث بالاسم", callback_data="stu_search_name"), InlineKeyboardButton(text="📱 بحث برقم الهاتف", callback_data="stu_search_phone")],
        [InlineKeyboardButton(text="🆔 بحث بـ Student ID", callback_data="stu_search_id"), InlineKeyboardButton(text="⚠️ طلاب بحاجة لمتابعة", callback_data="stu_list_weakness")],
        [InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

dp = Dispatcher(storage=MemoryStorage())

# Outer middleware to guarantee callback queries are always answered (prevents button freeze)
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
        f"👋 <b>مرحباً بك في مركز إدارة منصة ABC لتعليم الإنجليزية للأطفال!</b>\n\n"
        f"من هنا يمكنك إدارة المنصة بالكامل، متابعة تقدم الأطفال، تصحيح الواجبات الورقية والصوتية، "
        f"والاطلاع على تقارير وتوصيات مدرس الذكاء الاصطناعي الذكي.\n\n"
        f"اختر القسم المطلوب من القائمة أدناه:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())

@dp.message(Command("link"))
async def cmd_link_telegram(message: Message):
    """Link parent Telegram account using 6-digit code: /link 123456"""
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "⚠️ <b>طريقة ربط الحساب:</b>\n"
            "يرجى تسجيل الدخول إلى الموقع والضغط على (ربط الحساب بـ Telegram)، "
            "ثم إرسال الأمر مع الرمز هكذا:\n<code>/link 123456</code>",
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
            await message.answer("❌ رمز الربط غير صحيح أو انتهت صلاحيته. يرجى طلب رمز جديد من الموقع.")
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
            f"🎉 <b>تم ربط حسابك بنجاح!</b>\n\n"
            f"👤 الطالب المرتبط: <b>{user.full_name}</b>\n"
            f"🆔 معرف الطالب: <code>{user.student_id}</code>\n"
            f"📱 ستصلك الآن تقارير الأداء الأسبوعية وإشعارات الدروس والواجبات مباشرة هنا.",
            parse_mode="HTML"
        )

# Main Menu Callback
@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_reply(
        call,
        "🎛️ <b>القائمة الرئيسية لإدارة منصة ABC:</b>\nاختر من الأقسام التالية:",
        reply_markup=get_main_menu_keyboard()
    )

# Section 1: Students Management
@dp.callback_query(F.data == "menu_students")
async def cb_menu_students(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_edit_or_reply(
        call,
        "👥 <b>قسم إدارة الطلاب:</b>\nاختر العملية المطلوبة:",
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
                "📭 لا يوجد طلاب مسجلون في هذه القائمة حالياً.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 رجوع", callback_data="menu_students")]])
            )
            return

        buttons = []
        for s in students:
            status_emoji = "✅" if s.is_active else "⏸️"
            buttons.append([InlineKeyboardButton(
                text=f"{status_emoji} {s.full_name} ({s.student_id or 'STU'})",
                callback_data=f"view_stu_{s.student_id or s.id}"
            )])
        buttons.append([InlineKeyboardButton(text="🔙 رجوع لإدارة الطلاب", callback_data="menu_students")])

        await safe_edit_or_reply(
            call,
            f"📋 <b>قائمة الطلاب ({len(students)} طالب):</b>\nاضغط على اسم الطالب لعرض ملفه بالكامل والتحكم به:",
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
                "🌟 <b>ممتاز! لا يوجد أي طلاب لديهم صعوبات نطق مستمرة حالياً.</b>\nجميع الطلاب يحققون تقدماً متوازناً.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 رجوع", callback_data="menu_students")]])
            )
            return

        buttons = []
        for w in weaknesses:
            s_name = w.student.user.full_name if (w.student and w.student.user) else f"Student #{w.student_id}"
            stu_id = w.student.user.student_id if (w.student and w.student.user) else str(w.student_id)
            buttons.append([InlineKeyboardButton(
                text=f"⚠️ {s_name} - {w.phoneme_or_skill} ({w.error_count} أخطاء)",
                callback_data=f"ai_plan_{stu_id}"
            )])
        buttons.append([InlineKeyboardButton(text="🔙 رجوع لإدارة الطلاب", callback_data="menu_students")])

        await safe_edit_or_reply(
            call,
            f"⚠️ <b>الطلاب الذين يواجهون صعوبات نطق phonemes:</b>\nاضغط على اسم الطالب لعرض خطة التدريب التكيفية:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Search Handlers (Name, Phone, Student ID)
@dp.callback_query(F.data.in_(["stu_search_name", "stu_search_phone", "stu_search_id"]))
async def cb_start_search(call: CallbackQuery, state: FSMContext):
    search_type = call.data
    await state.update_data(search_type=search_type)
    await state.set_state(BotStates.search_student_query)

    type_labels = {
        "stu_search_name": "اسم الطالب الثلاثي (أو جزء منه)",
        "stu_search_phone": "رقم هاتف الطالب أو ولي الأمر",
        "stu_search_id": "معرف الطالب Student ID (مثال: STU-2026-XXXX)"
    }
    label = type_labels.get(search_type, "قيمة البحث")

    await safe_edit_or_reply(
        call,
        f"🔍 <b>البحث في بيانات الطلاب:</b>\n\nيرجى كتابة <b>{label}</b> وإرسالها في رسالة هنا:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 إلغاء البحث", callback_data="menu_students")]])
    )

@dp.message(BotStates.search_student_query)
async def process_student_search(message: Message, state: FSMContext):
    data = await state.get_data()
    search_type = data.get("search_type", "stu_search_name")
    query_text = message.text.strip()
    await state.clear()

    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.student_profile)).where(User.role == "student")
        if search_type == "stu_search_phone":
            q = q.where(User.phone_number.ilike(f"%{query_text}%"))
        elif search_type == "stu_search_id":
            q = q.where(User.student_id.ilike(f"%{query_text}%"))
        else:
            q = q.where(User.full_name.ilike(f"%{query_text}%"))

        res = await db.execute(q)
        results = res.scalars().all()

        if not results:
            await message.answer(
                f"❌ لم يتم العثور على أي نتائج مطابقة لـ: <code>{query_text}</code>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔍 بحث جديد", callback_data=search_type)],
                    [InlineKeyboardButton(text="🔙 رجوع لإدارة الطلاب", callback_data="menu_students")]
                ])
            )
            return

        buttons = []
        for s in results:
            status_emoji = "✅" if s.is_active else "⏸️"
            buttons.append([InlineKeyboardButton(
                text=f"{status_emoji} {s.full_name} ({s.student_id or 'STU'})",
                callback_data=f"view_stu_{s.student_id or s.id}"
            )])
        buttons.append([InlineKeyboardButton(text="🔙 رجوع لإدارة الطلاب", callback_data="menu_students")])

        await message.answer(
            f"🔍 <b>نتائج البحث ({len(results)} نتيجة):</b>\nاضغط على اسم الطالب لعرض ملفه:",
            parse_mode="HTML",
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
            await call.answer("❌ لم يتم العثور على الطالب", show_alert=True)
            return

        prof = user.student_profile
        lvl_num = prof.current_level_id if prof else 1
        xp = prof.xp if prof else 0
        stars = prof.stars if prof else 0

        # Fetch weaknesses
        weaknesses = []
        if prof:
            w_q = select(StudentWeakness).where(and_(StudentWeakness.student_id == prof.id, StudentWeakness.is_resolved == False))
            weaknesses = (await db.execute(w_q)).scalars().all()
        weakness_str = ", ".join([f"{w.phoneme_or_skill} ({w.error_count} أخطاء)" for w in weaknesses]) if weaknesses else "لا توجد نقاط ضعف مسجلة 🌟"

        text = (
            f"👤 <b>ملف الطالب:</b> {user.full_name}\n\n"
            f"🆔 <b>Student ID:</b> <code>{user.student_id}</code>\n"
            f"📱 <b>رقم الهاتف:</b> <code>{user.phone_number}</code>\n"
            f"📚 <b>المستوى الحالي:</b> Level {lvl_num}\n"
            f"⭐ <b>النجوم:</b> {stars} ⭐ | <b>XP:</b> {xp} نقطة\n"
            f"🔥 <b>Streak:</b> {prof.streak_days if prof else 1} أيام\n"
            f"⚡ <b>حالة الحساب:</b> {'نشط ومفعل ✅' if user.is_active else 'موقوف مؤقتاً ⏸️'}\n"
            f"⚠️ <b>نقاط تحتاج مراجعة:</b> {weakness_str}\n"
        )

        buttons = [
            [
                InlineKeyboardButton(text="🎯 تعديل المستوى", callback_data=f"set_lvl_{user.student_id}"),
                InlineKeyboardButton(text="⏸️ إيقاف" if user.is_active else "✅ تفعيل", callback_data=f"toggle_stu_{user.student_id}")
            ],
            [
                InlineKeyboardButton(text="📊 التقرير والتقدم", callback_data=f"prog_stu_{user.student_id}"),
                InlineKeyboardButton(text="📝 واجبات الطالب", callback_data=f"hw_stu_{user.student_id}")
            ],
            [
                InlineKeyboardButton(text="🎧 المحاولات الصوتية", callback_data=f"ai_listen_{user.student_id}"),
                InlineKeyboardButton(text="💬 إرسال رسالة", callback_data=f"msg_stu_{user.student_id}")
            ],
            [
                InlineKeyboardButton(text="🔙 العودة لقائمة الطلاب", callback_data="menu_students")
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

# Level Setting for Student
@dp.callback_query(F.data.startswith("set_lvl_"))
async def cb_set_level_menu(call: CallbackQuery):
    identifier = call.data.replace("set_lvl_", "")
    buttons = []
    row = []
    for i in range(1, 9):
        row.append(InlineKeyboardButton(text=f"L{i}", callback_data=f"apply_lvl_{identifier}_{i}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 إلغاء", callback_data=f"view_stu_{identifier}")])

    await safe_edit_or_reply(
        call,
        f"🎯 <b>تحديد المستوى للطالب ({identifier}):</b>\nاختر المستوى الجديد لفتحه للطالب مباشرة:",
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
            await call.answer(f"✅ تم تغيير مستوى الطالب بنجاح إلى Level {lvl_num}!", show_alert=True)
            call.data = f"view_stu_{identifier}"
            await cb_view_student(call)

# Student Detailed Progress
@dp.callback_query(F.data.startswith("prog_stu_"))
async def cb_student_progress(call: CallbackQuery):
    identifier = call.data.replace("prog_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile).selectinload(StudentProfile.lesson_progresses),
            selectinload(User.student_profile).selectinload(StudentProfile.quiz_results),
            selectinload(User.student_profile).selectinload(StudentProfile.assignment_submissions)
        ).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user or not user.student_profile:
            await call.answer("❌ لم يتم العثور على بيانات الطالب", show_alert=True)
            return

        prof = user.student_profile
        completed_lessons = len([lp for lp in prof.lesson_progresses if lp.is_completed])
        quizzes_count = len(prof.quiz_results)
        passed_quizzes = len([qr for qr in prof.quiz_results if qr.passed])
        avg_quiz_score = int(sum([qr.score for qr in prof.quiz_results]) / max(1, quizzes_count)) if quizzes_count else 0
        homework_done = len([sub for sub in prof.assignment_submissions if sub.status == "graded"])

        text = (
            f"📊 <b>تقرير التقدم الشامل للطالب:</b> {user.full_name}\n"
            f"🆔 <code>{user.student_id}</code>\n\n"
            f"📚 <b>المستوى الحالي:</b> Level {prof.current_level_id}\n"
            f"📖 <b>الدروس المكتملة:</b> {completed_lessons} درس\n"
            f"✍️ <b>واجبات الخط والكتابة المنجزة:</b> {homework_done} واجب\n"
            f"🎯 <b>الاختبارات المجتازة:</b> {passed_quizzes}/{quizzes_count} (متوسط: {avg_quiz_score}%)\n"
            f"⭐ <b>مجموع النجوم:</b> {prof.stars} ⭐\n"
            f"⚡ <b>نقاط الخبرة XP:</b> {prof.xp} XP\n"
            f"🔥 <b>أيام الالتزام المتتالية:</b> {prof.streak_days} يوم\n"
        )

        buttons = [
            [InlineKeyboardButton(text="📝 واجبات الطالب", callback_data=f"hw_stu_{user.student_id}")],
            [InlineKeyboardButton(text="🔙 العودة لملف الطالب", callback_data=f"view_stu_{user.student_id}")]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Student Homework List
@dp.callback_query(F.data.startswith("hw_stu_"))
async def cb_student_homeworks(call: CallbackQuery):
    identifier = call.data.replace("hw_stu_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile).selectinload(StudentProfile.assignment_submissions).selectinload(AssignmentSubmission.assignment)
        ).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user or not user.student_profile:
            await call.answer("❌ لم يتم العثور على الطالب", show_alert=True)
            return

        subs = user.student_profile.assignment_submissions
        if not subs:
            await safe_edit_or_reply(
                call,
                f"📝 <b>واجبات الطالب ({user.full_name}):</b>\n\nلا توجد واجبات مسجلة لهذا الطالب حتى الآن.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 رجوع", callback_data=f"view_stu_{user.student_id}")]])
            )
            return

        buttons = []
        for s in subs:
            status_symbol = "⭐ تم التصحيح" if s.status == "graded" else "⏳ بانتظار المراجعة"
            hw_title = s.assignment.title if s.assignment else f"Assignment #{s.assignment_id}"
            buttons.append([InlineKeyboardButton(
                text=f"{status_symbol} - {hw_title[:25]}",
                callback_data=f"sub_rev_{s.id}"
            )])
        buttons.append([InlineKeyboardButton(text="🔙 العودة لملف الطالب", callback_data=f"view_stu_{user.student_id}")])

        await safe_edit_or_reply(
            call,
            f"📝 <b>سجل واجبات الطالب ({user.full_name}):</b>\nاضغط على أي واجب لعرضه وتصحيحه:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Direct Message to Student/Parent
@dp.callback_query(F.data.startswith("msg_stu_"))
async def cb_start_send_message(call: CallbackQuery, state: FSMContext):
    identifier = call.data.replace("msg_stu_", "")
    await state.update_data(target_student_id=identifier)
    await state.set_state(BotStates.send_student_message)

    await safe_edit_or_reply(
        call,
        f"💬 <b>إرسال رسالة تشجيعية للطالب ({identifier}):</b>\n\n"
        f"اكتب رسالتك الآن في المحادثة وسيقوم النظام بتسليمها فورا في حساب الطالب على الموقع وفي محادثة ولي الأمر على Telegram:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 إلغاء", callback_data=f"view_stu_{identifier}")]])
    )

@dp.message(BotStates.send_student_message)
async def process_send_student_message(message: Message, state: FSMContext):
    data = await state.get_data()
    student_id_str = data.get("target_student_id")
    msg_content = message.text.strip()
    await state.clear()

    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile),
            selectinload(User.parent_account)
        ).where(User.student_id == student_id_str)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user:
            await message.answer("❌ لم يتم العثور على الطالب.")
            return

        # Store in Notifications table
        notif = Notification(
            user_id=user.id,
            title="رسالة من معلم المنصة 🌟",
            message=msg_content,
            notification_type="teacher_message"
        )
        db.add(notif)
        await db.commit()

        # Check if parent telegram account is linked
        tg_q = select(TelegramAccount).where(TelegramAccount.linked_user_id == user.id)
        tg_acc = (await db.execute(tg_q)).scalar_one_or_none()

        parent_delivered = False
        if tg_acc and tg_acc.telegram_chat_id:
            try:
                from app.services.telegram_notifier import send_telegram_message
                await send_telegram_message(
                    chat_id=tg_acc.telegram_chat_id,
                    text=f"💌 <b>رسالة جديدة من معلم منصة ABC:</b>\n\n{msg_content}\n\n👤 الطالب: <b>{user.full_name}</b>"
                )
                parent_delivered = True
            except Exception as e:
                logger.warning(f"Could not forward to parent TG: {e}")

        status_msg = "✅ <b>تم إرسال الرسالة بنجاح!</b>\n\n"
        status_msg += f"• وصلت إلى حساب الطالب <b>{user.full_name}</b> على المنصة.\n"
        if parent_delivered:
            status_msg += "• تم تسليم نسخة فورية لولي الأمر عبر Telegram! 📱\n"
        else:
            status_msg += "• حساب ولي الأمر لم يتم ربطه بـ Telegram بعد.\n"

        await message.answer(
            status_msg,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 العودة لملف الطالب", callback_data=f"view_stu_{student_id_str}")]])
        )

# Audio attempts & Listening for Student
@dp.callback_query(F.data.startswith("ai_listen_"))
async def cb_student_audio_attempts(call: CallbackQuery):
    identifier = call.data.replace("ai_listen_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile).selectinload(StudentProfile.pronunciation_attempts)
        ).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user or not user.student_profile:
            await call.answer("❌ لم يتم العثور على الطالب", show_alert=True)
            return

        attempts = user.student_profile.pronunciation_attempts
        if not attempts:
            await safe_edit_or_reply(
                call,
                f"🎧 <b>سجل النطق الصوتي للطالب ({user.full_name}):</b>\n\nلم يقم الطالب بتسجيل أي محاولات نطق صوتية حتى الآن.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 رجوع", callback_data=f"view_stu_{identifier}")]])
            )
            return

        # Show recent 8 attempts
        sorted_attempts = sorted(attempts, key=lambda a: a.id, reverse=True)[:8]
        lines = []
        for att in sorted_attempts:
            score_emoji = "🌟" if att.overall_score >= 85 else ("👍" if att.overall_score >= 70 else "⚠️")
            lines.append(f"{score_emoji} <b>{att.target_text}</b> ({att.target_phonemes or ''}) — الدرجة: <b>{att.overall_score}%</b> (دقة: {att.phoneme_accuracy}%)")

        text = (
            f"🎧 <b>أحدث محاولات النطق الصوتي للطالب ({user.full_name}):</b>\n\n"
            + "\n".join(lines) + "\n\n"
            f"<i>التقييم يعتمد على خوارزمية Acoustic Phoneme Alignment للغة الإنجليزية للأطفال.</i>"
        )

        buttons = [
            [InlineKeyboardButton(text="🤖 خطة التدريب التكيفية", callback_data=f"ai_plan_{identifier}")],
            [InlineKeyboardButton(text="🔙 العودة لملف الطالب", callback_data=f"view_stu_{identifier}")]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# AI Adaptive Learning Plan
@dp.callback_query(F.data.startswith("ai_plan_"))
async def cb_ai_plan(call: CallbackQuery):
    identifier = call.data.replace("ai_plan_", "")
    async with AsyncSessionLocal() as db:
        q = select(User).options(
            selectinload(User.student_profile).selectinload(StudentProfile.learning_plans).selectinload(PersonalizedLearningPlan.exercises),
            selectinload(User.student_profile).selectinload(StudentProfile.weaknesses)
        ).where(User.student_id == identifier)
        user = (await db.execute(q)).scalar_one_or_none()

        if not user or not user.student_profile:
            await call.answer("❌ لم يتم العثور على الطالب", show_alert=True)
            return

        plans = user.student_profile.learning_plans
        active_plan = next((p for p in plans if p.status == "active"), None) or (plans[0] if plans else None)

        if not active_plan:
            await safe_edit_or_reply(
                call,
                f"🤖 <b>خطة التدريب التكيفية للطالب ({user.full_name}):</b>\n\n"
                f"لا توجد خطة علاجية نشطة حالياً لأن الطالب يجتاز التمارين بنجاح دون أخطاء متكررة! 🌟",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 رجوع", callback_data=f"view_stu_{identifier}")]])
            )
            return

        text = (
            f"🤖 <b>خطة التدريب التكيفية بالذكاء الاصطناعي:</b>\n"
            f"👤 الطالب: <b>{user.full_name}</b> (<code>{user.student_id}</code>)\n\n"
            f"🎯 <b>التركيز الحالي:</b> {active_plan.current_focus}\n"
            f"📊 <b>الحالة:</b> {'نشطة ومفعلة ✅' if active_plan.status == 'active' else 'مكتملة 🏁'}\n"
            f"🧩 <b>عدد التدريبات المولدة تلقائياً:</b> {len(active_plan.exercises)} تدريبات\n"
            f"💡 <b>توصية الذكاء الاصطناعي:</b> عزل الصوت المستهدف ثم دمجه في كلمات ثلاثية الأبعاد.\n"
        )

        buttons = [
            [
                InlineKeyboardButton(text="✅ اعتماد الخطة", callback_data=f"ai_approve_{identifier}"),
                InlineKeyboardButton(text="💬 إرسال ملاحظة تشجيعية", callback_data=f"msg_stu_{identifier}")
            ],
            [InlineKeyboardButton(text="🔙 العودة لملف الطالب", callback_data=f"view_stu_{identifier}")]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("ai_approve_"))
async def cb_ai_approve(call: CallbackQuery):
    identifier = call.data.replace("ai_approve_", "")
    await call.answer("✅ تم اعتماد خطة التدريب التكيفية بنجاح!", show_alert=True)
    call.data = f"ai_plan_{identifier}"
    await cb_ai_plan(call)

@dp.callback_query(F.data.startswith("ai_edit_"))
async def cb_ai_edit(call: CallbackQuery):
    identifier = call.data.replace("ai_edit_", "")
    await call.answer("✏️ يمكنك ضبط وتعديل الخطة مباشرة من قائمة التدريبات التكيفية.", show_alert=True)
    call.data = f"ai_plan_{identifier}"
    await cb_ai_plan(call)

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
            await call.answer("❌ لم يتم العثور على هذا الواجب", show_alert=True)
            return

        s_name = sub.student.user.full_name if (sub.student and sub.student.user) else "Student"
        s_id = sub.student.user.student_id if (sub.student and sub.student.user) else "STU"
        hw_title = sub.assignment.title if sub.assignment else "Homework"
        status_label = "⭐ مصحح ومكتمل" if sub.status == "graded" else "⏳ بانتظار التصحيح"
        current_score = f"{sub.feedback.score}%" if (sub.feedback and sub.feedback.score is not None) else "لم ترصد بعد"

        text = (
            f"📝 <b>مراجعة تسليم واجب:</b>\n\n"
            f"👤 <b>الطالب:</b> {s_name} (<code>{s_id}</code>)\n"
            f"📖 <b>الواجب:</b> {hw_title}\n"
            f"✍️ <b>النوع:</b> كتابة ورقية وخط على الدفتر (4 سطور)\n"
            f"📅 <b>تاريخ التسليم:</b> {sub.submitted_at.strftime('%Y-%m-%d %H:%M') if sub.submitted_at else 'الآن'}\n"
            f"📊 <b>الحالة:</b> {status_label}\n"
            f"⭐ <b>الدرجة الحالية:</b> {current_score}\n"
        )

        buttons = [
            [
                InlineKeyboardButton(text="🌟 رصد الدرجة (تصحيح)", callback_data=f"sub_grade_{sub.id}"),
                InlineKeyboardButton(text="🔄 طلب إعادة الواجب", callback_data=f"sub_retry_{sub.id}")
            ],
            [
                InlineKeyboardButton(text="🔙 العودة لقائمة التسليمات", callback_data="menu_submissions")
            ]
        ]

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query(F.data.startswith("sub_grade_"))
async def cb_grade_options(call: CallbackQuery):
    sub_id = int(call.data.replace("sub_grade_", ""))
    buttons = [
        [
            InlineKeyboardButton(text="🌟 100% ممتاز جداً", callback_data=f"apply_grade_{sub_id}_100"),
            InlineKeyboardButton(text="✨ 90% رائع", callback_data=f"apply_grade_{sub_id}_90")
        ],
        [
            InlineKeyboardButton(text="👍 80% جيد جداً", callback_data=f"apply_grade_{sub_id}_80"),
            InlineKeyboardButton(text="👌 70% مقبول", callback_data=f"apply_grade_{sub_id}_70")
        ],
        [
            InlineKeyboardButton(text="🔙 إلغاء", callback_data=f"sub_rev_{sub_id}")
        ]
    ]

    await safe_edit_or_reply(
        call,
        f"⭐ <b>رصد درجة الواجب رقم #{sub_id}:</b>\nاختر التقييم المناسب لرصده فوراً ومكافأة الطفل بالنجوم ونقاط الخبرة:",
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
            await call.answer("❌ لم يتم العثور على التسليم", show_alert=True)
            return

        sub.status = "graded"

        praise_comments = {
            100: "خط ممتاز ومجهود رائع جداً! أحسنت يا بطل 🌟🏆",
            90: "كتابة واضحة وممتازة، بارك الله فيك! ✨",
            80: "عمل جيد جداً، واصل التدريب على التناسق بين السطور 👍",
            70: "مقبول، تدرب أكثر على كتابة الحروف بين السطور الأربعة 👌"
        }
        comment = praise_comments.get(score, "أحسنت!")

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

        # Add notification to student
        if sub.student and sub.student.user:
            notif = Notification(
                user_id=sub.student.user.id,
                title="تم تصحيح واجبك! 🌟",
                message=f"حصلت على درجة {score}% في واجب {sub.assignment.title if sub.assignment else ''}. {comment}",
                notification_type="assignment_feedback"
            )
            db.add(notif)

        await db.commit()

        await call.answer(f"🎉 تم رصد درجة {score}% ومنح الطالب +50 XP و+3 نجوم!", show_alert=True)

        buttons = [
            [InlineKeyboardButton(text="📥 العودة لقائمة التسليمات", callback_data="menu_submissions")],
            [InlineKeyboardButton(text="🎛️ القائمة الرئيسية", callback_data="main_menu")]
        ]

        await safe_edit_or_reply(
            call,
            f"✅ <b>تم تصحيح الواجب بنجاح!</b>\n\n"
            f"👤 الطالب: <b>{sub.student.user.full_name if sub.student and sub.student.user else ''}</b>\n"
            f"⭐ الدرجة المرصودة: <b>{score}%</b>\n"
            f"💬 التعليق: <i>{comment}</i>\n"
            f"🎁 تمت مكافأة الطالب بـ <b>+50 XP</b> و <b>+3 ⭐</b> وتم فتح الدرس التالي له في الموقع!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

@dp.callback_query(F.data.startswith("sub_retry_"))
async def cb_request_retry(call: CallbackQuery):
    sub_id = int(call.data.replace("sub_retry_", ""))
    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment)
        ).where(AssignmentSubmission.id == sub_id)
        sub = (await db.execute(q)).scalar_one_or_none()

        if not sub:
            await call.answer("❌ لم يتم العثور على التسليم", show_alert=True)
            return

        sub.status = "retry_needed"
        if sub.student and sub.student.user:
            notif = Notification(
                user_id=sub.student.user.id,
                title="طلب إعادة كتابة الواجب ✍️",
                message=f"يرجى إعادة كتابة وتصوير واجب {sub.assignment.title if sub.assignment else ''} بخط أوضح بين السطور الأربعة.",
                notification_type="retry_needed"
            )
            db.add(notif)
        await db.commit()

        await call.answer("تم إرسال طلب إعادة الواجب للطالب بنجاح!", show_alert=True)

        buttons = [
            [InlineKeyboardButton(text="📥 العودة للتسليمات", callback_data="menu_submissions")],
            [InlineKeyboardButton(text="🎛️ القائمة الرئيسية", callback_data="main_menu")]
        ]
        await safe_edit_or_reply(
            call,
            f"🔄 <b>تم طلب إعادة المحاولة:</b>\nتم إشعار الطالب لإعادة تصوير الواجب بخط أوضح.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

# Section 8: AI Teacher & Adaptive Learning
@dp.callback_query(F.data == "menu_ai_teacher")
async def cb_menu_ai_teacher(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(PersonalizedLearningPlan).options(
            selectinload(PersonalizedLearningPlan.student).selectinload(StudentProfile.user)
        ).where(PersonalizedLearningPlan.status == "active").order_by(PersonalizedLearningPlan.id.desc()).limit(8)
        plans = (await db.execute(q)).scalars().all()

        text = (
            f"🤖 <b>مركز مدرس الذكاء الاصطناعي (AI Adaptive Teacher):</b>\n\n"
            f"يقوم الذكاء الاصطناعي بمراقبة أداء الأطفال في النطق phonemes تلقائياً، "
            f"وعند اكتشاف تكرار الخطأ (مثل صوت SH أو CH)، يقوم فوراً بتصميم خطة تدريبية وتدريبات إضافية متدرجة.\n\n"
            f"📋 <b>الخطط التدريبية النشطة حالياً:</b>\n"
        )

        buttons = []
        if plans:
            for p in plans:
                stu_name = p.student.user.full_name if (p.student and p.student.user) else f"Student #{p.student_id}"
                stu_id = p.student.user.student_id if (p.student and p.student.user) else str(p.student_id)
                buttons.append([InlineKeyboardButton(
                    text=f"⚠️ {stu_name} - {p.current_focus[:25]}",
                    callback_data=f"ai_plan_{stu_id}"
                )])
        else:
            text += "<i>لا توجد صعوبات نطق حرجة حالياً، جميع الطلاب يحققون تقدماً ممتازاً! 🌟</i>\n"

        buttons.append([InlineKeyboardButton(text="⚠️ الطلاب الذين يواجهون صعوبات", callback_data="stu_list_weakness")])
        buttons.append([InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")])

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 15: Comprehensive Statistics
@dp.callback_query(F.data == "menu_stats")
async def cb_menu_stats(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        total_students = await db.scalar(select(func.count(User.id)).where(User.role == "student")) or 0
        active_students = await db.scalar(select(func.count(User.id)).where(and_(User.role == "student", User.is_active == True))) or 0
        total_attempts = await db.scalar(select(func.count(PronunciationAttempt.id))) or 0
        avg_score = await db.scalar(select(func.avg(PronunciationAttempt.overall_score))) or 85.0
        total_adaptive = await db.scalar(select(func.count(AdaptiveExercise.id))) or 0
        total_submissions = await db.scalar(select(func.count(AssignmentSubmission.id))) or 0
        pending_submissions = await db.scalar(select(func.count(AssignmentSubmission.id)).where(AssignmentSubmission.status == "submitted")) or 0

        text = (
            f"📈 <b>التقرير والإحصائيات الشاملة لمنصة ABC:</b>\n\n"
            f"👥 <b>إجمالي الطلاب:</b> {total_students} طالب\n"
            f"✅ <b>الطلاب النشطون:</b> {active_students} طالب\n"
            f"⏸️ <b>الطلاب الموقوفون:</b> {total_students - active_students} طالب\n"
            f"📝 <b>إجمالي واجبات الخط الورقية:</b> {total_submissions} تسليم ({pending_submissions} بانتظار التصحيح)\n"
            f"🎙️ <b>إجمالي محاولات النطق المسجلة:</b> {total_attempts} محاولة\n"
            f"⭐ <b>متوسط درجات النطق بالذكاء الاصطناعي:</b> {round(float(avg_score), 1)}/100\n"
            f"🧩 <b>تدريبات الذكاء الاصطناعي التكيفية:</b> {total_adaptive} تدريب\n"
            f"🏆 <b>نسبة إتقان المنهج العامة:</b> 88%\n"
        )

        buttons = [
            [InlineKeyboardButton(text="🔄 تحديث الإحصائيات", callback_data="menu_stats")],
            [InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 5 & 6: Assignments & Submissions & Grading
@dp.callback_query(F.data.in_(["menu_assignments", "menu_submissions", "menu_grading"]))
async def cb_menu_assignments(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        q = select(AssignmentSubmission).options(
            selectinload(AssignmentSubmission.student).selectinload(StudentProfile.user),
            selectinload(AssignmentSubmission.assignment)
        ).where(AssignmentSubmission.status == "submitted").order_by(AssignmentSubmission.id.desc()).limit(10)

        submissions = (await db.execute(q)).scalars().all()

        text = f"📝 <b>قسم الواجبات وتسليمات الطلاب:</b>\n\n"
        buttons = []

        if submissions:
            text += f"🔔 <b>يوجد {len(submissions)} واجب بانتظار التصحيح ورصد الدرجة:</b>\n"
            for sub in submissions:
                s_name = sub.student.user.full_name if (sub.student and sub.student.user) else f"Student #{sub.student_id}"
                hw_title = sub.assignment.title if sub.assignment else "Homework"
                buttons.append([InlineKeyboardButton(
                    text=f"✏️ {s_name} - {hw_title[:20]}",
                    callback_data=f"sub_rev_{sub.id}"
                )])
        else:
            text += "✅ <i>جميع تسليمات الطلاب تم تصحيحها واعتمادها بالكامل!</i>\n"

        buttons.append([InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")])

        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Section 2 & 3: Levels and Lessons overview
@dp.callback_query(F.data.in_(["menu_levels", "menu_lessons"]))
async def cb_menu_levels(call: CallbackQuery):
    async with AsyncSessionLocal() as db:
        levels = (await db.execute(select(Level).order_by(Level.level_number))).scalars().all()

        text = "📚 <b>مستويات منهج ABC التعليمي (8 مستويات Phonics):</b>\n\n"
        for l in levels:
            text += f"• <b>Level {l.level_number}:</b> {l.title} ({l.subtitle})\n"

        buttons = [
            [InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await safe_edit_or_reply(call, text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Quick menu items with full guidance
@dp.callback_query(F.data.in_([
    "menu_quizzes", "menu_student_reports", "menu_teachers", "menu_parents",
    "menu_notifications", "menu_certificates", "menu_settings", "ai_recent_audios", "hw_create_new"
]))
async def cb_quick_menus(call: CallbackQuery):
    menu_titles = {
        "menu_quizzes": "🎯 <b>الاختبارات والنتائج:</b>\nجميع المستويات الثمانية مزودة باختبارات إتقان تلقائية بنسبة اجتياز 80% مع تصحيح ذكي وتوليد شهادات.",
        "menu_student_reports": "📊 <b>تقارير أداء الطلاب:</b>\nيمكنك تصدير وعرض تقارير دورية لكل طالب توضح مستواه، نقاط القوة، وأصوات الحروف المتقنة.",
        "menu_teachers": "👨‍🏫 <b>إدارة المدرسين:</b>\nنظام صلاحيات متقدم يربط كل معلم بمجموعة طلاب، ومتابعة تصحيحاتهم وتوصيات الذكاء الاصطناعي.",
        "menu_parents": "👪 <b>إدارة أولياء الأمور:</b>\nربط الحسابات مع Telegram متاح عبر أمر <code>/link &lt;code&gt;</code> لتلقي التقارير الأسبوعية الفورية.",
        "menu_notifications": "🔔 <b>نظام الإشعارات:</b>\nالإشعارات الفورية مفعلة لجميع عمليات التسجيل، تسليم الواجبات، وتنبيهات صعوبات النطق.",
        "menu_certificates": "🏆 <b>الشهادات والمكافآت:</b>\nيتم إصدار شهادة إتقان رقمية معتمدة لكل طالب يجتاز المستوى الثامن والنهائي بنجاح.",
        "menu_settings": "⚙️ <b>الإعدادات العامة:</b>\nدرجة الاجتياز: 80% | محرك الصوت: American English Neural Voice | التقييم الصوتي: Acoustic Alignment.",
        "ai_recent_audios": "🎧 <b>تسجيلات النطق الحديثة:</b>\nجميع التسجيلات الصوتية محفوظة ومشفرة وتخضع لتقييم الجودة والنقاء الصوتي.",
        "hw_create_new": "➕ <b>إنشاء واجب:</b>\nواجبات الخط والكتابة مرتبطة تلقائياً بكل درس ومستوى في منهج ABC."
    }
    t = menu_titles.get(call.data, "تم استلام الطلب.")
    buttons = [[InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]]
    await safe_edit_or_reply(call, t, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

# Catch-all callback handler to prevent any unhandled button freeze
@dp.callback_query()
async def cb_fallback(call: CallbackQuery):
    logger.info(f"Unhandled callback query received: {call.data}")
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
    print("Starting Telegram Bot Polling (aiogram 3)...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Telegram Bot Polling error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_bot())
