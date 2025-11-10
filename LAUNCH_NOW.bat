@echo off
REM =============================================
REM ECHO_XV4 MASTER LAUNCHER - IMMEDIATE LAUNCH
REM =============================================

title ECHO_XV4 MASTER LAUNCHER - LIVE STATUS
color 0A
mode con: cols=85 lines=50

echo ======================================================================
echo                    ECHO_XV4 MASTER LAUNCHER V3                      
echo                    Authority Level: 11.0 ACTIVE                     
echo ======================================================================
echo.
echo [INIT] Preparing system...

REM Kill Python processes
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 >nul

REM Navigate to directory
cd /d E:\ECHO_XV4\MLS

echo [READY] Launching server orchestration system...
echo.

REM Run the launcher
python simple_launcher.py

REM If error, keep window open
if errorlevel 1 (
    echo.
    echo [ERROR] Launcher encountered an error.
    pause
)

pause
