@echo off
REM VS Code Gateway Server - MLS Gateway
REM Integrates with VS Code extension API

echo Starting VS Code Gateway...
echo.
echo Prerequisites:
echo - VS Code extension installed and running
echo - Extension listening on localhost:3000
echo.

H:\Tools\python.exe "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\VSCODE_GATEWAY\vscode_gateway_http.py"
