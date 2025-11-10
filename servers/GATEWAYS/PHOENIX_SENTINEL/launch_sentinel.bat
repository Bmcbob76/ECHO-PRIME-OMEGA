@echo off
REM Phoenix Sentinel Launcher
REM Authority Level: 11.0

echo.
echo ========================================
echo    PHOENIX SENTINEL LAUNCHER
echo    Authority Level: 11.0
echo ========================================
echo.

REM Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Administrator privileges required!
    echo Right-click and "Run as Administrator"
    pause
    exit /b 1
)

echo [OK] Running with Administrator privileges
echo.

REM Check Python installation
H:\Tools\python.exe --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found at H:\Tools\python.exe
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Launch Phoenix Sentinel
echo [LAUNCH] Starting Phoenix Sentinel...
echo.
cd /d P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\PHOENIX_SENTINEL
H:\Tools\python.exe phoenix_sentinel_core.py

pause
