import logging
import os
import ssl
import aiohttp
from typing import Optional, Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

# Custom Emoji IDs from D:\bots\ايموجي مميز\id الإيموجي .txt
EMOJI_CHECK = "6039356946031582644"
EMOJI_STAR = "6039367245363161212"
EMOJI_ALERT = "6039409709704814287"
EMOJI_STUDENT = "6039640735995666163"
EMOJI_CAMERA = "6039643566379114876"
EMOJI_SPARKLES = "6039709764710047914"

def get_strict_ssl_context() -> ssl.SSLContext:
    """Enforce strict TLS 1.2+ and mandatory certificate validation."""
    ctx = ssl.create_default_context()
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx

async def send_telegram_message(
    chat_id: str | int,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> bool:
    """Send message to a telegram chat with optional inline keyboard buttons over secure HTTPS"""
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
        connector = aiohttp.TCPConnector(ssl=get_strict_ssl_context())
        async with aiohttp.ClientSession(connector=connector) as session:
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

async def send_telegram_photo(
    chat_id: str | int,
    photo_path: str,
    caption: str,
    reply_markup: Optional[Dict[str, Any]] = None
) -> bool:
    """Send child notebook photo to telegram admin chat over secure HTTPS"""
    if not settings.TELEGRAM_BOT_TOKEN or not os.path.exists(photo_path):
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        import json
        data = aiohttp.FormData()
        data.add_field("chat_id", str(chat_id))
        data.add_field("caption", caption)
        data.add_field("parse_mode", "HTML")
        if reply_markup:
            data.add_field("reply_markup", json.dumps(reply_markup))

        with open(photo_path, "rb") as f:
            data.add_field(
                "photo",
                f.read(),
                filename=os.path.basename(photo_path),
                content_type="image/jpeg"
            )

        connector = aiohttp.TCPConnector(ssl=get_strict_ssl_context())
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(url, data=data, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                return resp.status == 200
    except Exception as e:
        logger.warning(f"Failed to send Telegram photo: {e}")
        return False

async def notify_admins_new_student(
    student_id_str: str,
    full_name: str,
    phone_number: str,
    registration_date: str,
    level_num: int = 1,
    is_active: bool = True
):
    """Notify all configured Telegram Admins when a new student registers with rich formatting"""
    text = (
        f"<tg-emoji emoji-id=\"{EMOJI_SPARKLES}\">✨</tg-emoji> <b>تسجيل طالب جديد على منصة ABC!</b>\n\n"
        f"<blockquote>"
        f"👤 <b>الاسم الثلاثي:</b> <code>{full_name}</code>\n"
        f"📱 <b>رقم الهاتف:</b> <code>{phone_number}</code>\n"
        f"🆔 <b>Student ID:</b> <code>{student_id_str}</code>\n"
        f"📅 <b>تاريخ التسجيل:</b> <code>{registration_date}</code>\n"
        f"📚 <b>المستوى الأولي:</b> <b>Level {level_num}/50</b>\n"
        f"⚡ <b>حالة الحساب:</b> {'نشط ومفعل ✅' if is_active else 'قيد المراجعة ⏳'}\n"
        f"</blockquote>"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "عرض ملف الطالب", "callback_data": f"view_stu_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_STUDENT},
                {"text": "تحديد المستوى", "callback_data": f"set_lvl_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_SPARKLES}
            ],
            [
                {"text": "إيقاف الحساب" if is_active else "تفعيل الحساب", "callback_data": f"toggle_stu_{student_id_str}", "style": "danger" if is_active else "success", "icon_custom_emoji_id": EMOJI_CHECK},
                {"text": "تقرير التقدم والـ XP", "callback_data": f"prog_stu_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_STAR}
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
    """Notify Admins & Teachers about AI Teacher diagnostic alert with rich styling"""
    success_rate = int(((total_trials - error_count) / max(1, total_trials)) * 100)
    text = (
        f"<tg-emoji emoji-id=\"{EMOJI_ALERT}\">⚠️</tg-emoji> <b>تقرير وملاحظة المدرس الذكي (AI Pronunciation Alert):</b>\n\n"
        f"<blockquote>"
        f"👤 <b>الطالب:</b> <code>{student_name}</code> (<code>{student_id_str}</code>)\n"
        f"📚 <b>المستوى:</b> <b>{level_name}</b>\n"
        f"🎯 <b>المهارة الصوتية:</b> <code>{skill}</code>\n"
        f"❌ <b>الأخطاء المتكررة:</b> {error_count} من أصل {total_trials} محاولات ({success_rate}% إتقان)\n"
        f"💡 <b>توجيه الذكاء الاصطناعي:</b> <i>{notes}</i>\n"
        f"</blockquote>"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "الاستماع للمحاولات الصوتية", "callback_data": f"ai_listen_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_STAR},
                {"text": "عرض وتعديل الخطة", "callback_data": f"ai_plan_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_SPARKLES}
            ],
            [
                {"text": "اعتماد الخطة التكيفية", "callback_data": f"ai_approve_{student_id_str}", "style": "success", "icon_custom_emoji_id": EMOJI_CHECK},
                {"text": "إرسال رسالة تشجيعية", "callback_data": f"msg_stu_{student_id_str}", "style": "primary", "icon_custom_emoji_id": EMOJI_STUDENT}
            ]
        ]
    }

    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        await send_telegram_message(admin_id, text, reply_markup=reply_markup)

async def notify_assignment_submission(
    student_name: str,
    student_id_str: str,
    assignment_title: str,
    submission_id: int,
    photo_path: Optional[str] = None
):
    """Notify Telegram admin when a homework notebook photo is submitted"""
    caption = (
        f"<tg-emoji emoji-id=\"{EMOJI_CAMERA}\">📷</tg-emoji> <b>تسليم واجب كتابة ورقية جديد! ✍️</b>\n\n"
        f"<blockquote>"
        f"👤 <b>الطالب:</b> <code>{student_name}</code> (<code>{student_id_str}</code>)\n"
        f"📖 <b>الواجب:</b> <i>{assignment_title}</i>\n"
        f"📸 <b>المرفق:</b> صورة كراسة تحسين الخط (4 أسطر)\n"
        f"⏰ <b>الحالة:</b> بانتظار تصحيح ورصد الدرجة\n"
        f"</blockquote>"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "مراجعة وتصحيح الواجب", "callback_data": f"sub_rev_{submission_id}", "style": "primary", "icon_custom_emoji_id": EMOJI_CAMERA},
                {"text": "رصد الدرجة فوراً", "callback_data": f"sub_grade_{submission_id}", "style": "success", "icon_custom_emoji_id": EMOJI_CHECK}
            ]
        ]
    }

    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        if photo_path and os.path.exists(photo_path):
            sent = await send_telegram_photo(admin_id, photo_path, caption, reply_markup=reply_markup)
            if not sent:
                await send_telegram_message(admin_id, caption, reply_markup=reply_markup)
        else:
            await send_telegram_message(admin_id, caption, reply_markup=reply_markup)
