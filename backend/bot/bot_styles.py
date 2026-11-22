# Telegram Custom Emoji IDs and Button Styler
# Loaded from D:\bots\ايموجي مميز\id الإيموجي .txt
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

EMOJIS = {
    "CHECK": "6039356946031582644",      # ✅
    "STAR": "6039367245363161212",       # ⭐️
    "FIRE": "6039663022580964808",       # 🔥
    "STUDENT": "6039640735995666163",    # 👤
    "ALERT": "6039409709704814287",      # ⚠️
    "GEAR": "6039716284470402303",       # ⚙️
    "BELL": "6039810103736017240",       # 🔔
    "STATS": "6039873609122454883",      # 📶
    "SPARKLES": "6039709764710047914",   # ✨
    "LOCK": "6039774717500465122",       # 🔒
    "BRAIN": "6039623740810076123",      # 🧠
    "DANGER": "6039850532263174530",     # ⛔
    "PIN": "6041850440834885588",        # 📌
    "CHAT": "6041783877431729209",       # 💬
    "TROPHY": "6039496588303278706",     # 💰
    "WAVE": "6039876280592112521",       # 👋
    "THUMB_UP": "6039836612274167260",   # 👍
    "CAMERA": "6039643566379114876",     # 📷
}

def tg_e(name: str, fallback: str = "✨") -> str:
    """Return tg-emoji HTML tag with the custom emoji id"""
    eid = EMOJIS.get(name)
    if eid:
        return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'
    return fallback

def s_btn(text: str, callback_data: str, style: str = None, emoji_key: str = None) -> InlineKeyboardButton:
    """Create a styled InlineKeyboardButton with optional style (primary, success, danger) and custom emoji."""
    kwargs = {"text": text, "callback_data": callback_data}
    if style in ["primary", "success", "danger"]:
        kwargs["style"] = style
    if emoji_key and emoji_key in EMOJIS:
        kwargs["icon_custom_emoji_id"] = EMOJIS[emoji_key]
    return InlineKeyboardButton(**kwargs)
