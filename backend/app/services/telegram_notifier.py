import logging
import aiohttp
from typing import Optional, Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_telegram_message(
    chat_id: str | int,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> bool:
    """Send message to a telegram chat with optional inline keyboard buttons"""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.info(f"[Telegram Not Configured] Would have sent to {chat_id}:\n{text}")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    return True
                else:
                    err = await resp.text()
                    logger.warning(f"Telegram API error ({resp.status}): {err}")
                    return False
    except Exception as e:
        logger.warning(f"Failed to send Telegram message: {e}")
        return False

async def notify_admins_new_student(
    student_id_str: str,
    full_name: str,
    phone_number: str,
    registration_date: str,
    level_num: int = 1,
    is_active: bool = True
):
    """Notify all configured Telegram Admins when a new child registers"""
    text = (
        f"🌟 <b>تسجيل طالب جديد على المنصة!</b>\n\n"
        f"👤 <b>الاسم الثلاثي:</b> {full_name}\n"
        f"📱 <b>رقم الهاتف:</b> <code>{phone_number}</code>\n"
        f"🆔 <b>Student ID:</b> <code>{student_id_str}</code>\n"
        f"📅 <b>تاريخ التسجيل:</b> {registration_date}\n"
        f"📚 <b>المستوى الأولي:</b> Level {level_num}\n"
        f"⚡ <b>حالة الحساب:</b> {'نشط ✅' if is_active else 'قيد المراجعة ⏳'}\n"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "📋 عرض ملف الطالب", "callback_data": f"view_stu_{student_id_str}"},
                {"text": "🎯 تحديد المستوى", "callback_data": f"set_lvl_{student_id_str}"}
            ],
            [
                {"text": "⏸️ إيقاف الحساب" if is_active else "✅ تفعيل الحساب", "callback_data": f"toggle_stu_{student_id_str}"},
                {"text": "📊 تقدم الطالب", "callback_data": f"prog_stu_{student_id_str}"}
            ],
            [
                {"text": "💬 إرسال رسالة لولي الأمر", "callback_data": f"msg_stu_{student_id_str}"}
            ]
        ]
    }

    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        await send_telegram_message(admin_id, text, reply_markup=reply_markup)

async def notify_ai_teacher_alert(
    student_name: str,
    student_id_str: str,
    level_name: str,
    skill: str,
    error_count: int,
    total_trials: int,
    notes: str
):
    """Notify Admins & Teachers about AI Teacher diagnostic alert & auto-generated plan"""
    success_rate = int(((total_trials - error_count) / max(1, total_trials)) * 100)
    text = (
        f"🤖 <b>تقرير المدرس الذكي (AI Pronunciation Alert)</b>\n\n"
        f"👤 <b>الطالب:</b> {student_name} (<code>{student_id_str}</code>)\n"
        f"📚 <b>المستوى:</b> {level_name}\n"
        f"🎯 <b>المهارة:</b> {skill} Pronunciation\n"
        f"❌ <b>عدد الأخطاء:</b> {error_count} من آخر {total_trials} محاولات\n"
        f"📊 <b>نسبة النجاح:</b> {success_rate}%\n\n"
        f"💡 <b>ملاحظة المدرس الذكي:</b>\n{notes}\n\n"
        f"⚡ <b>الإجراء التلقائي:</b>\nتم إنشاء تدريبات إضافية مخصصة وعزل الصوت للتدريب المكثف."
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🎧 الاستماع للمحاولات", "callback_data": f"ai_listen_{student_id_str}"},
                {"text": "📋 عرض التدريبات", "callback_data": f"ai_plan_{student_id_str}"}
            ],
            [
                {"text": "✅ اعتماد الخطة", "callback_data": f"ai_approve_{student_id_str}"},
                {"text": "✏️ تعديل الخطة", "callback_data": f"ai_edit_{student_id_str}"}
            ],
            [
                {"text": "💬 إرسال ملاحظة تشجيعية", "callback_data": f"msg_stu_{student_id_str}"}
            ]
        ]
    }

    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        await send_telegram_message(admin_id, text, reply_markup=reply_markup)

async def notify_assignment_submission(
    student_name: str,
    student_id_str: str,
    assignment_title: str,
    submission_id: int
):
    """Notify Telegram admin when a homework assignment is handed in"""
    text = (
        f"📝 <b>تسليم واجب مدرسي جديد!</b>\n\n"
        f"👤 <b>الطالب:</b> {student_name} (<code>{student_id_str}</code>)\n"
        f"📖 <b>الواجب:</b> {assignment_title}\n"
        f"⏰ <b>الحالة:</b> بانتظار تصحيح المعلم"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🔍 مراجعة الإجابة والتسجيل", "callback_data": f"sub_rev_{submission_id}"},
                {"text": "⭐ رصد الدرجة", "callback_data": f"sub_grade_{submission_id}"}
            ]
        ]
    }

    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        await send_telegram_message(admin_id, text, reply_markup=reply_markup)
