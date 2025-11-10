@echo off
REM ============================================
REM WINDOWS API MCP BRIDGE LAUNCHER
REM Commander Bobby Don McWilliams II
REM Authority Level: 11.0
REM ============================================

echo.
echo ========================================
echo   WINDOWS API MCP BRIDGE
echo   Authority Level: 11.0
echo ========================================
echo.
echo Starting Windows API MCP Bridge...
echo Backend: http://localhost:8343
echo.

REM Change to server directory
cd /d E:\ECHO_XV4\MLS\servers

REM Launch with Python (full path)
H:\Tools\python.exe windows_api_mcp_bridge.py

echo.
echo Bridge terminated.
pause
