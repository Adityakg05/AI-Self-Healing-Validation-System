@echo off
title Self-Healing SRE Agent - Launcher
echo ============================================================
echo  Self-Healing SRE Agent - Starting Services
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo [1/2] Starting FastAPI backend (port 8000)...
start "FastAPI Backend" cmd /k "python app.py"

REM Wait a moment for FastAPI to start
timeout /t 3 /nobreak >nul

echo [2/2] Starting Streamlit UI (port 8502)...
start "Streamlit UI" cmd /k "python -m streamlit run ui.py"

REM Wait for Streamlit to start
timeout /t 4 /nobreak >nul

echo.
echo ============================================================
echo  Both services started!
echo  - FastAPI API:    http://localhost:8000
echo  - Streamlit UI:   http://localhost:8502
echo  - API Docs:       http://localhost:8000/docs
echo ============================================================
echo.
echo Opening Streamlit UI in browser...
start http://localhost:8502

echo.
echo Press any key to stop both services...
pause >nul

REM Kill both services
taskkill /F /FI "WINDOWTITLE eq FastAPI Backend" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Streamlit UI" >nul 2>&1
echo [Done] Services stopped.
