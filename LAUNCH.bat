@echo off
REM MASTER LAUNCHER ULTIMATE - Windows Launch Script
REM Commander Bobby Don McWilliams II - Authority Level 11.0

echo.
echo ================================================================================
echo    MASTER LAUNCHER ULTIMATE - QUICK LAUNCH
echo    Commander Bobby Don McWilliams II - Authority Level 11.0
echo ================================================================================
echo.

cd /d "%~dp0"

REM Check if Python exists
if not exist "H:\Tools\python.exe" (
    echo ERROR: Python not found at H:\Tools\python.exe
    echo.
    pause
    exit /b 1
)

REM Launch
echo Launching Master Launcher Ultimate...
echo.
H:\Tools\python.exe launch.py

pause
