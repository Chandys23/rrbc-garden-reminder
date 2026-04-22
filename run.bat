@echo off
echo 🌿 RRBC Garden Care Reminder App - Startup Script
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if dependencies are installed
echo Installing/updating dependencies...
pip install -r requirements.txt --quiet
echo.

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️  WARNING: .env file not found!
    echo Please create .env file with your Gmail credentials:
    echo.
    echo   1. Copy .env.example to .env
    echo   2. Add your Gmail email and app password
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Start the application
echo.
echo ✅ Starting RRBC Garden Care Reminder App...
echo.
echo 🌐 Application will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

python backend/main.py
