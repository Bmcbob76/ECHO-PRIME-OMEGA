@echo off
REM =====================================
REM MASTER MODULAR LAUNCHER V3 WITH FULL DISPLAY
REM Authority Level 11.0
REM Commander Bobby Don McWilliams II
REM =====================================

cls
color 0A
title ECHO_XV4 MASTER MODULAR LAUNCHER V3 - LIVE CONSOLE

echo.
echo ==============================================================================
echo                    ECHO_XV4 MASTER MODULAR LAUNCHER V3
echo                         AUTHORITY LEVEL 11.0
echo                    Commander Bobby Don McWilliams II
echo ==============================================================================
echo.

REM Kill any existing Python processes
echo [CLEANUP] Terminating existing Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo [OK] Clean startup environment ready
echo.

REM Set working directory
cd /d E:\ECHO_XV4\MLS
echo [INFO] Working Directory: E:\ECHO_XV4\MLS
echo.

REM Set environment variables for maximum output
set PYTHONUNBUFFERED=1
set PYTHONDONTWRITEBYTECODE=1
set ECHO_DEBUG=1
set MCP_ENABLED=1
set SHOW_SERVER_DETAILS=1

REM Display system info
echo ==============================================================================
echo                            SYSTEM INFORMATION
echo ==============================================================================
echo [TIME] %DATE% %TIME%
echo [PATH] %CD%
echo [USER] %USERNAME%
echo [AUTHORITY] Level 11.0 - Maximum Authority

REM Check Python
echo.
echo [CHECK] Python Installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

REM Count servers
echo.
echo ==============================================================================
echo                         DISCOVERING SERVERS
echo ==============================================================================
echo [SCAN] Scanning E:\ECHO_XV4\MLS\servers\...
echo.

dir /b servers\*.py 2>nul | find /c ".py" > temp_count.txt
set /p SERVER_COUNT=<temp_count.txt
del temp_count.txt

echo [FOUND] %SERVER_COUNT% Python servers detected
echo.
echo Servers found:
echo ------------------------------------------------------------------------------
for %%f in (servers\*.py) do (
    echo   - %%~nf
)
echo ------------------------------------------------------------------------------

REM Display launch configuration
echo.
echo ==============================================================================
echo                        LAUNCH CONFIGURATION
echo ==============================================================================
echo [DASHBOARD] Will be available at: http://localhost:9000
echo [BASE PORT] Starting from port 8000
echo [HEALTH CHECK] Every 30 seconds
echo [AUTO-HEAL] Enabled with Phoenix Protocol
echo [HOT RELOAD] File watcher active
echo [MCP] Model Context Protocol enabled
echo.

REM Final confirmation
echo ==============================================================================
echo                         STARTING SYSTEM
echo ==============================================================================
echo.
echo [NOTICE] The following will happen:
echo   1. Auto-discover ALL servers in servers\ directory
echo   2. Assign unique ports starting from 8000
echo   3. Launch each server in its own process
echo   4. Monitor health every 30 seconds
echo   5. Auto-restart failed servers
echo   6. Display live status at http://localhost:9000
echo.
echo [INFO] Press Ctrl+C at any time to stop all servers
echo.
echo ==============================================================================
echo                    LAUNCHING MASTER MODULAR LAUNCHER V3
echo ==============================================================================
echo.

REM Launch Python with full output
echo [LAUNCH] Starting Master Modular Launcher...
echo.

python -u master_modular_launcher_enhanced.py

REM If it exits, show error
if errorlevel 1 (
    echo.
    echo ==============================================================================
    echo                              ERROR OCCURRED
    echo ==============================================================================
    echo [ERROR] Launcher exited with error code %errorlevel%
    echo [INFO] Check logs\master.log for details
    echo.
    pause
) else (
    echo.
    echo ==============================================================================
    echo                         SHUTDOWN COMPLETE
    echo ==============================================================================
    echo [INFO] All servers stopped successfully
    echo.
    timeout /t 5
)
