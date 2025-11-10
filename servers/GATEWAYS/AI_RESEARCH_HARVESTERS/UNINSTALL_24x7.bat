@echo off
REM UNINSTALL 24/7 HARVESTER FROM WINDOWS SCHEDULED TASKS
title Uninstall 24/7 Harvester

echo ═══════════════════════════════════════════════════════════════════════════
echo UNINSTALL 24/7 AUTONOMOUS HARVESTER
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo This will remove the Windows Scheduled Task.
echo The harvester files will NOT be deleted.
echo.
pause

schtasks /Delete /TN "ECHO_PRIME\AI_Research_Harvester_24x7" /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Task uninstalled successfully
) else (
    echo.
    echo ❌ Failed to uninstall (task may not exist)
)

echo.
pause
