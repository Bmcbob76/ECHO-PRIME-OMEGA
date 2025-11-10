@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM INSTALL 24/7 HARVESTER AS WINDOWS SCHEDULED TASK
REM ═══════════════════════════════════════════════════════════════════════════
REM AUTHORITY: 11.0 (Commander Bob)
REM This registers the harvester to auto-start on boot and restart on failure
REM ═══════════════════════════════════════════════════════════════════════════

title Install 24/7 Harvester Service
color 0E

echo ═══════════════════════════════════════════════════════════════════════════
echo INSTALL 24/7 AUTONOMOUS HARVESTER
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo This will:
echo   ✓ Register Windows Scheduled Task
echo   ✓ Auto-start on system boot (2 minute delay)
echo   ✓ Auto-restart on failure (999 retries)
echo   ✓ Run with highest privileges
echo   ✓ Continue even on battery power
echo.
echo Task Name: ECHO_PRIME\AI_Research_Harvester_24x7
echo.
echo ═══════════════════════════════════════════════════════════════════════════
pause

cd /d "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\AI_RESEARCH_HARVESTERS"

echo.
echo Registering task...
schtasks /Create /TN "ECHO_PRIME\AI_Research_Harvester_24x7" /XML task_scheduler_24x7.xml /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════════════════════
    echo ✅ SUCCESS - 24/7 Harvester installed!
    echo ═══════════════════════════════════════════════════════════════════════════
    echo.
    echo The harvester will:
    echo   • Start automatically on next boot
    echo   • Run continuously 24/7
    echo   • Auto-restart if crashed
    echo   • Harvest 36 AI/ML topics per cycle
    echo   • Generate EKMs with AI-ML-Mastery analysis
    echo.
    echo To start NOW: schtasks /Run /TN "ECHO_PRIME\AI_Research_Harvester_24x7"
    echo To stop:      schtasks /End /TN "ECHO_PRIME\AI_Research_Harvester_24x7"
    echo To uninstall: Run UNINSTALL_24x7.bat
    echo.
    echo Check status: H:\Tools\python.exe check_status.py
    echo View logs:    type autonomous_harvest.log
    echo.
) else (
    echo.
    echo ❌ FAILED - Error code %ERRORLEVEL%
    echo.
    echo Common issues:
    echo   • Need Administrator privileges (Run as Administrator)
    echo   • Task already exists (run UNINSTALL_24x7.bat first)
    echo.
)

echo ═══════════════════════════════════════════════════════════════════════════
pause
