# ABC English Telegram Management Bot Runner
$Host.UI.RawUI.WindowTitle = "ABC English - Telegram Bot"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   🚀 تشغيل بوت تليجرام لإدارة منصة ABC لتعليم الأطفال" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
$env:PYTHONPATH = "backend"
& .\backend\venv\Scripts\python.exe -m bot.bot_main
