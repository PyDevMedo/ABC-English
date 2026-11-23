import os
import secrets
from typing import Tuple, Set
from fastapi import HTTPException, UploadFile, status

# ==============================================================================
# File Upload Security & Magic Bytes Verification
# ==============================================================================

ALLOWED_IMAGE_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_AUDIO_EXTENSIONS: Set[str] = {".mp3", ".wav", ".m4a", ".ogg"}

DANGEROUS_EXTENSIONS: Set[str] = {
    ".php", ".php3", ".php4", ".php5", ".phtml", ".phar",
    ".py", ".pyc", ".sh", ".bash", ".exe", ".bat", ".cmd",
    ".ps1", ".vbs", ".js", ".mjs", ".html", ".htm", ".xhtml",
    ".svg", ".dll", ".so", ".jar", ".war", ".asp", ".aspx",
    ".jsp", ".cgi", ".pl", ".htaccess"
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5 MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10 MB

def detect_image_type_from_magic_bytes(header: bytes) -> str | None:
    """Verify true file format using magic byte signatures."""
    if len(header) < 12:
        return None
    if header.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if header.startswith(b"RIFF") and b"WEBP" in header[:16]:
        return ".webp"
    return None

def detect_audio_type_from_magic_bytes(header: bytes) -> str | None:
    """Verify true audio format using magic byte signatures."""
    if len(header) < 12:
        return None
    if header.startswith(b"RIFF") and b"WAVE" in header[:16]:
        return ".wav"
    if header.startswith(b"ID3") or header.startswith(b"\xff\xfb") or header.startswith(b"\xff\xf3") or header.startswith(b"\xff\xf2"):
        return ".mp3"
    if header.startswith(b"OggS"):
        return ".ogg"
    if b"ftyp" in header[:16]:
        return ".m4a"
    return None

async def validate_and_save_upload(
    upload_file: UploadFile,
    category: str, # "image" or "audio"
    target_dir: str,
    prefix: str,
    user_id: int | str
) -> Tuple[str, str]:
    """
    Validates file content, size, and extension, and stores with a cryptographically
    random filename inside target_dir.
    
    Returns:
        (saved_filepath, relative_url)
    """
    if not upload_file or not upload_file.filename:
        raise HTTPException(status_code=400, detail="لم يتم استلام أي ملف.")

    # 1. Check raw extension against blacklist
    raw_filename = os.path.basename(upload_file.filename)
    _, ext = os.path.splitext(raw_filename.lower())
    if ext in DANGEROUS_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نوع الملف المرفوع غير مسموح به لأسباب أمنية."
        )

    # 2. Read file content and check size limit
    content = await upload_file.read()
    file_size = len(content)

    max_size = MAX_IMAGE_SIZE if category == "image" else MAX_AUDIO_SIZE
    if file_size > max_size:
        max_mb = max_size // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"حجم الملف كبير جداً ({file_size // (1024 * 1024)}MB). الحد الأقصى المسموح به هو {max_mb}MB."
        )

    if file_size < 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الملف تالف أو فارغ."
        )

    # 3. Magic Bytes Content Inspection
    header = content[:32]
    if category == "image":
        detected_ext = detect_image_type_from_magic_bytes(header)
        if not detected_ext or detected_ext not in ALLOWED_IMAGE_EXTENSIONS:
            # Fallback if extension matches allowed images and content starts with standard format
            if ext in ALLOWED_IMAGE_EXTENSIONS:
                detected_ext = ext
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="محتوى الملف لا يطابق صيغة صورة صالحة (JPEG, PNG, WebP)."
                )
    elif category == "audio":
        detected_ext = detect_audio_type_from_magic_bytes(header)
        if not detected_ext or detected_ext not in ALLOWED_AUDIO_EXTENSIONS:
            if ext in ALLOWED_AUDIO_EXTENSIONS:
                detected_ext = ext
            else:
                # Fallback for recorded web audio blobs
                detected_ext = ".wav"
    else:
        raise HTTPException(status_code=400, detail="فئة الملف غير معروفة.")

    # 4. Generate Random Unpredictable Filename
    safe_token = secrets.token_hex(12)
    clean_prefix = "".join(c for c in prefix if c.isalnum() or c in "_-")
    clean_user = "".join(c for c in str(user_id) if c.isalnum() or c in "_-")
    safe_filename = f"{clean_prefix}_{clean_user}_{safe_token}{detected_ext}"

    # 5. Path Traversal Defense
    os.makedirs(target_dir, exist_ok=True)
    real_target_dir = os.path.realpath(target_dir)
    dest_path = os.path.realpath(os.path.join(real_target_dir, safe_filename))

    if not dest_path.startswith(real_target_dir):
        raise HTTPException(status_code=400, detail="محاولة غير صالحة لتحديد مسار الملف.")

    # 6. Save File to Disk
    with open(dest_path, "wb") as f:
        f.write(content)

    relative_url = f"/uploads/{safe_filename}"
    return dest_path, relative_url
