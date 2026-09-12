@echo off
title AURA - Autonomous Research Intelligence

cd /d "%~dp0"

echo ==========================================
echo       AURA AUTONOMOUS RESEARCH AI
echo ==========================================
echo.

echo Closing old AURA processes...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo Starting FastAPI backend...
start "AURA Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\python.exe -m uvicorn app.main:app --port 8000"

timeout /t 3 /nobreak >nul

echo Starting React frontend...
start "AURA Frontend" cmd /k "cd /d %~dp0frontend && npm run dev -- --host localhost --strictPort"

timeout /t 5 /nobreak >nul

echo Opening AURA...
start http://localhost:5173

echo.
echo AURA is starting.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
pause