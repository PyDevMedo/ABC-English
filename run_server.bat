@echo off
chcp 65001 >nul
title ABC English - سيرفر المنصة التعليمية
echo ========================================================
echo    🚀 تشغيل سيرفر منصة ABC لتعليم الأطفال (FastAPI)
echo    الرابط: http://localhost:8000
echo ========================================================

:: إغلاق أي عملية قديمة حاجبة للمنفذ 8000 تلقائياً
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

set PYTHONPATH=backend
backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
