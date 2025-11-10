@echo off
REM OMEGA SWARM BRAIN LAUNCHER
REM Starts OMEGA as both HTTP (5200) and MCP Gateway

echo ============================================
echo OMEGA SWARM BRAIN GATEWAY LAUNCHER
echo ============================================
echo.
echo HTTP Port: 5200
echo MCP Gateway: Available
echo.

cd /d "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\OMEGA_SWARM_BRAIN"

echo Starting OMEGA Swarm Brain HTTP Gateway...
start "OMEGA_HTTP_5200" /MIN H:\Tools\python.exe omega_swarm_brain_http.py

echo.
echo ✅ OMEGA Swarm Brain started
echo    HTTP: http://localhost:5200
echo    Status: http://localhost:5200/status
echo    Health: http://localhost:5200/health
echo.
echo MCP Gateway available via MLS
echo.
pause
