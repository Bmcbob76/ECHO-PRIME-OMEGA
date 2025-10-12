@echo off
REM ========================================
REM PHOENIX VOICE - GUILTY SPARK LAUNCHER
REM Authority Level: 11.0
REM ========================================

echo.
echo ========================================
echo   PHOENIX VOICE - GUILTY SPARK
echo   343 - Monitor of Installation 04
echo ========================================
echo.

cd /d "E:\ECHO_XV4\MLS\servers"

echo [*] Checking Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo [!] ERROR: Python not found
    pause
    exit /b 1
)

echo.
echo [*] Checking CUDA availability...
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"

echo.
echo [*] Starting Phoenix Voice server on port 7343...
echo [*] Log file: E:\ECHO_XV4\logs\phoenix_guilty_spark.log
echo.
echo ========================================
echo   Press Ctrl+C to stop server
echo ========================================
echo.

python phoenix_voice_guilty_spark.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] SERVER CRASHED - Check logs
    pause
)
