@echo off
chcp 65001 >nul
title ABC English - سيرفر المنصة التعليمية
echo ========================================================
echo    🚀 تشغيل سيرفر منصة ABC لتعليم الأطفال (FastAPI)
echo    الرابط: http://localhost:8000
echo ========================================================
set PYTHONPATH=backend
backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
