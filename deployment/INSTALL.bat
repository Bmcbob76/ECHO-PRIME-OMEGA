@echo off
REM MASTER LAUNCHER ULTIMATE - Installation Script
REM Commander Bobby Don McWilliams II - Authority Level 11.0

echo.
echo ================================================================================
echo    MASTER LAUNCHER ULTIMATE - INSTALLATION
echo    Commander Bobby Don McWilliams II - Authority Level 11.0
echo ================================================================================
echo.

cd /d "%~dp0"

REM Check Python
if not exist "H:\Tools\python.exe" (
    echo ERROR: Python not found at H:\Tools\python.exe
    echo Please install Python 3.10+ at H:\Tools\python.exe
    pause
    exit /b 1
)

echo [1/3] Checking Python...
H:\Tools\python.exe --version
if errorlevel 1 (
    echo ERROR: Python check failed
    pause
    exit /b 1
)
echo OK
echo.

echo [2/3] Installing dependencies...
H:\Tools\python.exe -m pip install --upgrade pip
H:\Tools\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Dependency installation failed
    pause
    exit /b 1
)
echo OK
echo.

echo [3/3] Installing optional dependencies...
H:\Tools\python.exe -m pip install GPUtil
echo (GPU monitoring - optional)
echo.

echo.
echo ================================================================================
echo    INSTALLATION COMPLETE!
echo ================================================================================
echo.
echo To launch: Double-click LAUNCH.bat
echo       Or: H:\Tools\python.exe launch.py
echo.
pause
