@echo off
title ECHO_XV4 MASTER LAUNCHER - VISUAL DISPLAY
color 0A
cls

echo ========================================================================
echo                 ECHO_XV4 MASTER MODULAR LAUNCHER V3
echo                         VISUAL DISPLAY EDITION
echo ========================================================================
echo.
echo [INIT] Killing any existing Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [INIT] Setting up environment...
cd /d E:\ECHO_XV4\MLS

echo [INIT] Installing dependencies...
python -m pip install rich colorama requests pyyaml psutil -q >nul 2>&1

echo [LAUNCH] Starting Visual Master Launcher...
echo.
echo ========================================================================

REM Launch with full output visible
python visual_launcher.py

REM Keep window open if error
if errorlevel 1 (
    echo.
    echo [ERROR] Launcher exited with error
    pause
)
