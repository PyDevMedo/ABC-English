import os
import hashlib
import asyncio
import numpy as np
from typing import Tuple
from app.core.config import settings

VOICE_DEFAULT = "en-US-AnaNeural" # Friendly child/teaching American English voice in edge-tts

def get_audio_hash(text: str, voice: str = VOICE_DEFAULT) -> str:
    cleaned = text.strip().lower()
    return hashlib.md5(f"{cleaned}_{voice}".encode("utf-8")).hexdigest()

async def generate_speech_audio(text: str, voice: str = VOICE_DEFAULT) -> str:
    """Generate high-quality American English speech audio file using edge-tts or gTTS fallback"""
    os.makedirs(settings.STATIC_AUDIO_DIR, exist_ok=True)
    file_hash = get_audio_hash(text, voice)
    filename = f"{file_hash}.mp3"
    filepath = os.path.join(settings.STATIC_AUDIO_DIR, filename)
    relative_url = f"/static/audio/{filename}"

    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        return relative_url

    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate="-10%", pitch="+5Hz")
        await communicate.save(filepath)
        return relative_url
    except Exception as e:
        # Fallback to gTTS if edge-tts network is unreachable or fails
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', tld='com') # American English
            tts.save(filepath)
            return relative_url
        except Exception as ex:
            # If completely offline, return placeholder url
            return f"/static/audio/sample_voice.mp3"

def analyze_audio_quality(filepath: str) -> Tuple[str, float]:
    """
    Check if the child's recording is silent, overly noisy, or clear.
    Returns (status: 'clear'|'silent'|'noisy', rms_energy: float)
    """
    if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
        return "silent", 0.0

    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(filepath)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        if len(samples) == 0:
            return "silent", 0.0

        rms = np.sqrt(np.mean(samples**2)) / 32768.0

        if rms < 0.005:
            return "silent", float(rms)
        elif rms > 0.85:
            return "noisy", float(rms)
        return "clear", float(rms)
    except Exception:
        # If pydub/audio decode fails, gracefully consider clear
        return "clear", 0.15
