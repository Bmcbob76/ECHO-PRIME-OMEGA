@echo off
echo ============================================================
echo ECHO XV4 - ELEVENLABS TTS V3 NARRATOR SETUP
echo ============================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo [INFO] Installing required packages...
pip install --break-system-packages -r E:\ECHO_XV4\MLS\servers\requirements_narrator.txt

echo.
echo [INFO] Packages installed!
echo.
echo ============================================================
echo SETUP COMPLETE - Ready to run narrator
echo ============================================================
echo.
echo NEXT STEPS:
echo 1. Set your ElevenLabs API key:
echo    set ELEVENLABS_API_KEY=your_api_key_here
echo.
echo 2. Run the narrator:
echo    python E:\ECHO_XV4\MLS\servers\elevenlabs_echo_narrator.py
echo.
pause
