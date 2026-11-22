import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["levels"] == 8

@pytest.mark.asyncio
async def test_student_registration_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Reject incomplete name (< 3 parts)
        bad_name_res = await ac.post("/api/v1/auth/register", json={
            "full_name": "محمد أحمد",
            "phone_number": "01099887766",
            "password": "password123"
        })
        assert bad_name_res.status_code == 400
        assert "الاسم الثلاثي" in bad_name_res.json()["detail"]

        # 2. Reject invalid phone number
        bad_phone_res = await ac.post("/api/v1/auth/register", json={
            "full_name": "محمد أحمد علي",
            "phone_number": "invalid_phone",
            "password": "password123"
        })
        assert bad_phone_res.status_code == 400

        # 3. Successful registration with 3-part name and dynamic unique phone
        unique_phone = f"010{uuid.uuid4().int % 100000000:08d}"
        reg_res = await ac.post("/api/v1/auth/register", json={
            "full_name": "يوسف محمود إبراهيم",
            "phone_number": unique_phone,
            "password": "password123",
            "avatar": "panda"
        })
        assert reg_res.status_code == 200
        student_data = reg_res.json()
        assert student_data["full_name"] == "يوسف محمود إبراهيم"
        assert student_data["student_id"].startswith("STU-")
        assert student_data["is_active"] is True
        assert student_data["current_level_id"] == 1

        # 4. Prevent duplicate registration with same phone
        dup_res = await ac.post("/api/v1/auth/register", json={
            "full_name": "يوسف محمود إبراهيم",
            "phone_number": unique_phone,
            "password": "password123"
        })
        assert dup_res.status_code == 400
        assert "مسجل بالفعل" in dup_res.json()["detail"]

        # 5. Login
        login_res = await ac.post("/api/v1/auth/login", json={
            "phone_number": unique_phone,
            "password": "password123"
        })
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 6. Access /me profile
        me_res = await ac.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["phone_number"] == unique_phone

        # 7. Access curriculum levels
        levels_res = await ac.get("/api/v1/curriculum/levels", headers=headers)
        assert levels_res.status_code == 200
        levels = levels_res.json()
        assert len(levels) == 8
        assert levels[0]["is_unlocked"] is True # Level 1 unlocked

        # 8. Test AI Pronunciation Evaluation
        eval_res = await ac.post(
            "/api/v1/pronunciation/evaluate",
            headers=headers,
            data={
                "target_text": "Ship",
                "simulated_speech": "Ship"
            }
        )
        assert eval_res.status_code == 200
        eval_data = eval_res.json()
        assert eval_data["overall_score"] >= 70
        assert "SH" in eval_data["correct_phonemes"]
        assert eval_data["needs_retry"] is False

        # 9. Test Telegram Link Code generation
        tg_res = await ac.post("/api/v1/telegram/generate-link-code", headers=headers)
        assert tg_res.status_code == 200
        tg_data = tg_res.json()
        assert len(tg_data["code"]) == 6
