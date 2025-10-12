@echo off
REM ============================================================================
REM UNIFIED DEVELOPER API LAUNCHER
REM Commander Bobby Don McWilliams II - Authority Level 11.0
REM Master orchestrator for ECHO_XV4 Developer API System
REM ============================================================================

echo.
echo ========================================================================
echo ECHO UNIFIED DEVELOPER API - MASTER ORCHESTRATOR
echo Authority Level 11.0 - Commander Bobby Don McWilliams II
echo ========================================================================
echo.
echo Starting Unified Developer API Server...
echo - Port 9000 (Master Orchestrator)
echo - VS Code API integration (port 9001)
echo - Windows API integration (port 8343)
echo - Desktop Commander (MCP integrated)
echo - Multi-step workflow engine
echo.

REM Change to servers directory
cd /d E:\ECHO_XV4\MLS\servers

REM Launch with H: drive Python
echo Launching server with H:\Tools\python.exe...
H:\Tools\python.exe unified_developer_api.py

echo.
echo Server stopped.
pause
