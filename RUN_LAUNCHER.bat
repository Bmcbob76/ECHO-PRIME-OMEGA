@echo off
REM ========================================
REM ECHO_XV4 MASTER LAUNCHER - DISPLAY MODE
REM ========================================

title ECHO_XV4 MASTER LAUNCHER - LIVE DISPLAY
mode con: cols=80 lines=50
color 0A

echo Killing existing Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

cls
cd /d E:\ECHO_XV4\MLS

echo Starting ECHO_XV4 Master Launcher...
echo.

python simple_launcher.py

pause
