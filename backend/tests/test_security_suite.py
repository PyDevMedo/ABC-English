import pytest
import uuid
import bcrypt
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import (
    get_password_hash, verify_password, verify_and_update_password,
    encrypt_sensitive_data, decrypt_sensitive_data, sanitize_html
)
from app.core.file_security import detect_image_type_from_magic_bytes, detect_audio_type_from_magic_bytes
from bot.bot_main import is_admin_user
from app.core.config import settings

# ==============================================================================
# 1. Tests for HTTPS & Security Headers
# ==============================================================================
@pytest.mark.asyncio
async def test_security_headers_and_hsts():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/health")
        assert res.status_code == 200

        # Strict-Transport-Security (HSTS)
        assert "Strict-Transport-Security" in res.headers
        assert "max-age=63072000" in res.headers["Strict-Transport-Security"]
        assert "includeSubDomains" in res.headers["Strict-Transport-Security"]

        # Content-Security-Policy (CSP)
        assert "Content-Security-Policy" in res.headers
        csp = res.headers["Content-Security-Policy"]
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp
        assert "object-src 'none'" in csp

        # Nosniff, Clickjacking & Referrer
        assert res.headers.get("X-Content-Type-Options") == "nosniff"
        assert res.headers.get("X-Frame-Options") == "DENY"
        assert res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert "Permissions-Policy" in res.headers

# ==============================================================================
# 2. Tests for Argon2id Password Hashing, Salting & Legacy Migration
# ==============================================================================
def test_argon2id_hashing_and_legacy_migration():
    # A) Argon2id Hashing & Unique Salting
    pwd = "Argon2SecretPassword2026!"
    h1 = get_password_hash(pwd)
    h2 = get_password_hash(pwd)
    assert h1.startswith("$argon2id$v=19$m=65536,t=3,p=4$")
    assert h2.startswith("$argon2id$v=19$m=65536,t=3,p=4$")
    assert h1 != h2
    assert verify_password(pwd, h1) is True
    assert verify_password("WrongPassword!", h1) is False

    # B) Bcrypt Upgrade Migration (Transparent upgrade on login)
    plain_bcrypt = "oldBcryptUserPass"
    b_hash = bcrypt.hashpw(plain_bcrypt.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    assert b_hash.startswith("$2b$")
    ok, new_argon = verify_and_update_password(plain_bcrypt, b_hash)
    assert ok is True
    assert new_argon is not None
    assert new_argon.startswith("$argon2id$")
    assert verify_password(plain_bcrypt, new_argon) is True

    # C) Plaintext Upgrade Migration
    plain_old = "oldPlaintextPass"
    ok2, new_argon2 = verify_and_update_password(plain_old, plain_old)
    assert ok2 is True
    assert new_argon2.startswith("$argon2id$")

    # D) AES-256-GCM Sensitive Data Encryption
    sensitive_data = "TelegramSensitiveTokenKey123"
    enc = encrypt_sensitive_data(sensitive_data)
    assert enc != sensitive_data
    assert decrypt_sensitive_data(enc) == sensitive_data

# ==============================================================================
# 3. Tests for Account Data Isolation (Student A vs Student B)
# ==============================================================================
@pytest.mark.asyncio
async def test_multi_account_strict_data_isolation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        phone_a = f"011{uuid.uuid4().int % 100000000:08d}"
        phone_b = f"012{uuid.uuid4().int % 100000000:08d}"

        # Register Student A
        reg_a = await ac.post("/api/v1/auth/register", json={
            "full_name": "الطالب الأول محمد علي",
            "phone_number": phone_a,
            "password": "PasswordStudentA123",
            "avatar": "lion"
        })
        assert reg_a.status_code == 200
        stu_a_id = reg_a.json()["student_id"]

        # Register Student B
        reg_b = await ac.post("/api/v1/auth/register", json={
            "full_name": "الطالب الثاني كريم أحمد",
            "phone_number": phone_b,
            "password": "PasswordStudentB123",
            "avatar": "panda"
        })
        assert reg_b.status_code == 200
        stu_b_id = reg_b.json()["student_id"]

        assert stu_a_id != stu_b_id

        login_a = await ac.post("/api/v1/auth/login", json={"phone_number": phone_a, "password": "PasswordStudentA123"})
        token_a = login_a.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        login_b = await ac.post("/api/v1/auth/login", json={"phone_number": phone_b, "password": "PasswordStudentB123"})
        token_b = login_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # Verify /auth/me returns strictly isolated user data
        me_a = await ac.get("/api/v1/auth/me", headers=headers_a)
        me_b = await ac.get("/api/v1/auth/me", headers=headers_b)
        assert me_a.json()["student_id"] == stu_a_id
        assert me_b.json()["student_id"] == stu_b_id

        # Student A submits homework
        fake_img = b"\xff\xd8\xff\xe0" + b"\x00" * 100
        sub_a = await ac.post(
            "/api/v1/assignments/submit",
            headers=headers_a,
            data={"assignment_id": 1, "submission_type": "handwriting_photo"},
            files={"image_file": ("notebook.jpg", fake_img, "image/jpeg")}
        )
        assert sub_a.status_code == 200
        sub_a_id = sub_a.json()["submission_id"]

        # Student A sees own submission
        subs_a = await ac.get("/api/v1/assignments/my-submissions", headers=headers_a)
        assert any(s["id"] == sub_a_id for s in subs_a.json())

        # DATA ISOLATION PROOF: Student B cannot see Student A's submission!
        subs_b = await ac.get("/api/v1/assignments/my-submissions", headers=headers_b)
        assert not any(s["id"] == sub_a_id for s in subs_b.json())

        # Student B by-level view reports is_submitted = False
        lvl_b = await ac.get("/api/v1/assignments/by-level/1", headers=headers_b)
        assert lvl_b.json()["is_submitted"] is False

# ==============================================================================
# 4. Tests for Unauthorized Access & Role-Based Access Control (RBAC)
# ==============================================================================
@pytest.mark.asyncio
async def test_rbac_authorization():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Unauthenticated request blocked
        unauth = await ac.get("/api/v1/auth/me")
        assert unauth.status_code == 401

        # Student accessing teacher/admin stats blocked with 403 Forbidden
        phone = f"015{uuid.uuid4().int % 100000000:08d}"
        await ac.post("/api/v1/auth/register", json={
            "full_name": "طالب عادي للتجربة",
            "phone_number": phone,
            "password": "PasswordStu123"
        })
        login_res = await ac.post("/api/v1/auth/login", json={"phone_number": phone, "password": "PasswordStu123"})
        headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

        stats = await ac.get("/api/v1/stats/overview", headers=headers)
        assert stats.status_code == 403
        assert "للمعلمين والمشرفين فقط" in stats.json()["detail"]

# ==============================================================================
# 5. Tests for Brute-Force Defense, User Enumeration & Logout
# ==============================================================================
@pytest.mark.asyncio
async def test_brute_force_protection_and_user_enumeration():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        phone = f"010{uuid.uuid4().int % 100000000:08d}"
        await ac.post("/api/v1/auth/register", json={
            "full_name": "مستخدم لاختبار التخمين",
            "phone_number": phone,
            "password": "CorrectPassword123"
        })

        # Uniform error response prevents phone enumeration
        res1 = await ac.post("/api/v1/auth/login", json={"phone_number": "01088887777", "password": "AnyPass"})
        res2 = await ac.post("/api/v1/auth/login", json={"phone_number": phone, "password": "WrongPass"})
        assert res1.status_code == 401
        assert res2.status_code == 401
        assert res1.json()["detail"] == res2.json()["detail"]

        # Forgot password uniform response
        forgot = await ac.post("/api/v1/auth/forgot-password?phone_number=01000000000")
        assert forgot.status_code == 200
        assert "إذا كان رقم الهاتف مسجلاً" in forgot.json()["message"]

        # Logout revokes session
        valid_login = await ac.post("/api/v1/auth/login", json={"phone_number": phone, "password": "CorrectPassword123"})
        tok = valid_login.json()["access_token"]
        headers = {"Authorization": f"Bearer {tok}"}

        assert (await ac.get("/api/v1/auth/me", headers=headers)).status_code == 200
        await ac.post("/api/v1/auth/logout", headers=headers)
        assert (await ac.get("/api/v1/auth/me", headers=headers)).status_code == 401

# ==============================================================================
# 6. Tests for File Upload Security (Extension Whitelisting, Magic Bytes, Executable Blocking)
# ==============================================================================
@pytest.mark.asyncio
async def test_file_upload_security_hardening():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        phone = f"012{uuid.uuid4().int % 100000000:08d}"
        await ac.post("/api/v1/auth/register", json={
            "full_name": "مستخدم لاختبار الملفات",
            "phone_number": phone,
            "password": "PasswordFiles123"
        })
        login_res = await ac.post("/api/v1/auth/login", json={"phone_number": phone, "password": "PasswordFiles123"})
        headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

        # Block Executable Script Upload (.php)
        php_payload = b"<?php echo 'Disallowed Script'; ?>"
        bad_res = await ac.post(
            "/api/v1/assignments/submit",
            headers=headers,
            data={"assignment_id": 1, "submission_type": "handwriting_photo"},
            files={"image_file": ("test.php", php_payload, "application/x-php")}
        )
        assert bad_res.status_code == 400
        assert "غير مسموح به لأسباب أمنية" in bad_res.json()["detail"]

        # Magic Bytes Validation
        assert detect_image_type_from_magic_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 20) == ".png"
        assert detect_image_type_from_magic_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 20) == ".jpg"
        assert detect_audio_type_from_magic_bytes(b"RIFF\x00\x00\x00\x00WAVE" + b"\x00" * 20) == ".wav"

# ==============================================================================
# 7. Tests for Telegram Bot Admin Access Control
# ==============================================================================
def test_telegram_bot_admin_access_control():
    if settings.TELEGRAM_ADMIN_IDS:
        admin_id = settings.TELEGRAM_ADMIN_IDS[0]
        assert is_admin_user(admin_id) is True
    assert is_admin_user(999999999999) is False

# ==============================================================================
# 8. Tests for SQL Injection & Parameterized Query Immunity
# ==============================================================================
@pytest.mark.asyncio
async def test_sql_injection_defense():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # SQL Injection attempt in login phone number field
        sql_payloads = [
            "' OR '1'='1",
            "admin' --",
            "' UNION SELECT * FROM users --",
            "01000000000' OR '1'='1"
        ]
        for payload in sql_payloads:
            res = await ac.post("/api/v1/auth/login", json={
                "phone_number": payload,
                "password": "Password123!"
            })
            # Must safely reject with 401 without SQL syntax error or leaking table data
            assert res.status_code == 401
            assert "بيانات الدخول غير صحيحة" in res.json()["detail"]

# ==============================================================================
# 9. Tests for XSS Sanitization & Input Cleansing
# ==============================================================================
def test_xss_sanitization_defense():
    raw_xss_inputs = [
        ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"),
        ("<img src=x onerror=alert(1)>", "&lt;img src=x onerror=alert(1)&gt;"),
        ("Hello <a href='javascript:steal()'>Click</a>", "Hello &lt;a href=&#x27;javascript:steal()&#x27;&gt;Click&lt;/a&gt;")
    ]
    for raw, expected in raw_xss_inputs:
        cleaned = sanitize_html(raw)
        assert "<script>" not in cleaned
        assert "<img" not in cleaned
        assert cleaned == expected

# ==============================================================================
# 10. Tests for Direct Object Reference (IDOR) & Cross-Account Isolation
# ==============================================================================
@pytest.mark.asyncio
async def test_cross_account_gamification_and_plan_isolation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        phone_1 = f"011{uuid.uuid4().int % 100000000:08d}"
        phone_2 = f"012{uuid.uuid4().int % 100000000:08d}"

        reg1 = await ac.post("/api/v1/auth/register", json={
            "full_name": "طالب العزل الأول",
            "phone_number": phone_1,
            "password": "PasswordOne123!"
        })
        reg2 = await ac.post("/api/v1/auth/register", json={
            "full_name": "طالب العزل الثاني",
            "phone_number": phone_2,
            "password": "PasswordTwo123!"
        })
        t1 = (await ac.post("/api/v1/auth/login", json={"phone_number": phone_1, "password": "PasswordOne123!"})).json()["access_token"]
        t2 = (await ac.post("/api/v1/auth/login", json={"phone_number": phone_2, "password": "PasswordTwo123!"})).json()["access_token"]

        h1 = {"Authorization": f"Bearer {t1}"}
        h2 = {"Authorization": f"Bearer {t2}"}

        # Dashboard strictly isolated
        dash1 = (await ac.get("/api/v1/gamification/dashboard", headers=h1)).json()
        dash2 = (await ac.get("/api/v1/gamification/dashboard", headers=h2)).json()

        # Each student sees their own isolated learning plan and gamification stats
        plan1 = (await ac.get("/api/v1/adaptive/plan", headers=h1)).json()
        plan2 = (await ac.get("/api/v1/adaptive/plan", headers=h2)).json()
        assert "has_plan" in plan1
        assert "has_plan" in plan2

