@echo off
REM ECHO PRIME SENTINEL Launcher
REM Authority Level: 11.0
REM 19 Skills Unified

echo.
echo ========================================
echo    ECHO PRIME SENTINEL LAUNCHER
echo    Authority Level: 11.0
echo    19 Skills Integrated
echo ========================================
echo.

REM Check Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Administrator privileges required!
    echo Right-click and "Run as Administrator"
    pause
    exit /b 1
)

echo [OK] Running with Administrator privileges
echo.

REM Check Python
H:\Tools\python.exe --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found at H:\Tools\python.exe
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Launch ECHO PRIME SENTINEL
echo [LAUNCH] Starting ECHO PRIME SENTINEL...
echo          Initializing 19 skill modules...
echo.
cd /d P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\PHOENIX_SENTINEL
H:\Tools\python.exe echo_prime_sentinel.py

pause
