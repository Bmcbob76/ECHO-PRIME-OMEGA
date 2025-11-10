@echo off
REM GS343 Gateway Launcher
echo ========================================
echo GS343 DIVINE AUTHORITY GATEWAY
echo Port 9406 - 45,962 Error Patterns
echo ========================================
echo.

cd /d "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\GS343_GATEWAY"

echo Starting GS343 Gateway...
H:\Tools\python.exe gs343_gateway_http.py

pause
