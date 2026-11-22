@echo off
chcp 65001 >nul
title ABC English - تشغيل بوت تليجرام للإدارة
echo ========================================================
echo    🚀 تشغيل بوت تليجرام لإدارة منصة ABC لتعليم الأطفال
echo ========================================================
set PYTHONPATH=backend
backend\venv\Scripts\python.exe -m bot.bot_main
pause
