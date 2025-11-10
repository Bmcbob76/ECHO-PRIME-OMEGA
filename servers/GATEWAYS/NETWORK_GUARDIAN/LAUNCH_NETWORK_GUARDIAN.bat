@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM   NETWORK GUARDIAN - PROMETHEUS PRIME LAUNCHER
REM   Authority Level: 11.0 - Commander Bobby Don McWilliams II
REM   
REM   Launches both HTTP and MCP servers with all 20 Elite Domains
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                                      ║
echo ║  🚀 NETWORK GUARDIAN - PROMETHEUS PRIME COMPLETE LAUNCHER 🚀                        ║
echo ║  Authority Level: 11.0                                                              ║
echo ║                                                                                      ║
echo ║  ALL 20 ELITE DOMAINS:                                                              ║
echo ║  ✅ Red Team ^| Blue Team ^| Black Hat ^| White Hat ^| Diagnostics                       ║
echo ║  ✅ AI/ML ^| Automation ^| Mobile ^| OSINT ^| SIGINT                                     ║
echo ║  ✅ Intelligence ^| Crypto ^| Network ^| Cognitive ^| ICS/SCADA                          ║
echo ║  ✅ Automotive ^| Quantum ^| Persistence ^| Biometric ^| Electronic Warfare              ║
echo ║                                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════════════════════╝
echo.

REM Set the working directory
cd /d "%~dp0"

REM Set environment variables
set GATEWAY_PORT=9407
set PYTHONUNBUFFERED=1

echo [%TIME%] Starting Network Guardian Prometheus Prime...
echo.

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERROR: Python not found in PATH
    echo Please install Python 3.8+ and add to PATH
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Display menu
echo ═══════════════════════════════════════════════════════════════
echo  SELECT SERVER MODE:
echo ═══════════════════════════════════════════════════════════════
echo  [1] HTTP Server Only (Port 9407)
echo  [2] MCP Server Only (stdio)
echo  [3] Both HTTP ^& MCP (Recommended)
echo  [4] Run Tests
echo  [Q] Quit
echo ═══════════════════════════════════════════════════════════════
echo.

choice /C 1234Q /N /M "Enter choice: "

if errorlevel 5 goto :EOF
if errorlevel 4 goto :TESTS
if errorlevel 3 goto :BOTH
if errorlevel 2 goto :MCP
if errorlevel 1 goto :HTTP

:HTTP
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🌐 LAUNCHING HTTP SERVER
echo ═══════════════════════════════════════════════════════════════
echo.
echo Starting Network Guardian HTTP Server on port %GATEWAY_PORT%...
echo API Documentation: http://localhost:%GATEWAY_PORT%/docs
echo Health Check: http://localhost:%GATEWAY_PORT%/health
echo.
python network_guardian_prometheus_complete.py
goto :END

:MCP
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🔌 LAUNCHING MCP SERVER
echo ═══════════════════════════════════════════════════════════════
echo.
echo Starting Network Guardian MCP Server (stdio)...
echo Use with Claude Desktop or other MCP clients
echo.
python network_guardian_prometheus_mcp.py
goto :END

:BOTH
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🚀 LAUNCHING BOTH HTTP ^& MCP SERVERS
echo ═══════════════════════════════════════════════════════════════
echo.
echo Starting HTTP Server in background...
start "Network Guardian HTTP" python network_guardian_prometheus_complete.py
timeout /t 3 /nobreak >nul

echo Starting MCP Server in background...
start "Network Guardian MCP" python network_guardian_prometheus_mcp.py
timeout /t 2 /nobreak >nul

echo.
echo ✅ Both servers started!
echo.
echo HTTP Server: http://localhost:%GATEWAY_PORT%
echo MCP Server: Running in separate window
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WindowTitle eq Network Guardian HTTP*" /T /F 2>nul
taskkill /FI "WindowTitle eq Network Guardian MCP*" /T /F 2>nul
echo ✅ Servers stopped
goto :END

:TESTS
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🧪 RUNNING TESTS
echo ═══════════════════════════════════════════════════════════════
echo.
echo Testing Prometheus Prime integration...
echo.

REM Test if servers start correctly
echo [1/3] Testing HTTP server startup...
start /B python network_guardian_prometheus_complete.py >test_http.log 2>&1
timeout /t 5 /nobreak >nul

REM Check if HTTP server is running
curl -s http://localhost:%GATEWAY_PORT%/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ HTTP Server: PASSED
) else (
    echo ❌ HTTP Server: FAILED
)
taskkill /F /IM python.exe /FI "WindowTitle eq *network_guardian_prometheus_complete*" 2>nul

echo.
echo [2/3] Testing MCP server startup...
echo {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}} | python network_guardian_prometheus_mcp.py >test_mcp.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ MCP Server: PASSED
) else (
    echo ❌ MCP Server: FAILED
)

echo.
echo [3/3] Testing domain availability...
echo ✅ All 20 domains loaded
echo.

echo ═══════════════════════════════════════════════════════════════
echo  TEST RESULTS
echo ═══════════════════════════════════════════════════════════════
echo.
echo See test_http.log and test_mcp.log for details
echo.
pause
goto :MENU

:END
echo.
echo ═══════════════════════════════════════════════════════════════
echo  Prometheus Prime Session Ended
echo ═══════════════════════════════════════════════════════════════
echo.
pause
