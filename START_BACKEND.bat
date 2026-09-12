@echo off
cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
    echo Backend virtual environment not found.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000

pause