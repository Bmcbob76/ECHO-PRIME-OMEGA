@echo off
REM =====================================
REM MASTER MODULAR LAUNCHER V3 - ECHO_XV4
REM Authority Level 11.0
REM Commander Bobby Don McWilliams II
REM =====================================

cls
echo.
echo ======================================================================
echo        MASTER MODULAR LAUNCHER V3 - ECHO_XV4 PRODUCTION
echo ======================================================================
echo.
echo [INFO] Authority Level: 11.0
echo [INFO] Commander: Bobby Don McWilliams II
echo [INFO] Features: Auto-Discovery, Hot Reload, MCP Integration, Docker
echo.

REM Set working directory
cd /d E:\ECHO_XV4\MLS

REM Set environment variables
set PYTHONUNBUFFERED=1
set ECHO_DEBUG=1
set MCP_ENABLED=1
set PYTHONDONTWRITEBYTECODE=1

REM Check Python
echo [CHECK] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found

REM Install requirements if needed
echo [CHECK] Checking dependencies...
pip show pyyaml >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
)

REM Check MCP (optional)
echo [CHECK] Checking MCP for Claude integration...
python -c "import mcp" >nul 2>&1
if errorlevel 1 (
    echo [WARN] MCP not installed. Some features will be limited.
    echo [INFO] To enable Claude integration, run: pip install mcp
) else (
    echo [OK] MCP available - Claude integration enabled
)

REM Check servers directory
if not exist "servers" (
    echo [INFO] Creating servers directory...
    mkdir servers
)

REM Check logs directory
if not exist "logs" (
    echo [INFO] Creating logs directory...
    mkdir logs
)

echo.
echo ======================================================================
echo [START] Launching Master Modular Launcher V3...
echo ======================================================================
echo.
echo [INFO] Servers directory: E:\ECHO_XV4\MLS\servers
echo [INFO] Dashboard will be available at: http://localhost:9000
echo [INFO] Drop any server script in the servers folder to auto-launch
echo.
echo [INFO] Press Ctrl+C to stop all servers and exit
echo.

REM Launch the master launcher
python master_modular_launcher_enhanced.py

REM If launcher exits, pause to show any errors
if errorlevel 1 (
    echo.
    echo [ERROR] Launcher exited with error code %errorlevel%
    pause
)
