@echo off
echo ===================================================================
echo ECHO COPILOT BRIDGE - WINDOWS DIAGNOSTIC SCRIPT
echo Commander Bobby Don McWilliams II - Authority Level 11.0
echo ===================================================================
echo.

echo [1/8] Checking Node.js installation...
node --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found or not in PATH
    echo Install from: https://nodejs.org/
) else (
    echo ✅ Node.js found
)
echo.

echo [2/8] Checking Python installation...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found or not in PATH
) else (
    echo ✅ Python found
)
echo.

echo [3/8] Checking extension installation...
code --list-extensions | findstr echo-copilot-bridge >NUL
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ECHO Copilot Bridge extension not installed
) else (
    echo ✅ Extension installed
)
echo.

echo [4/8] Checking Desktop Commander server...
if exist "E:\ECHO_XV4\MLS\servers\desktop_commander_server.py" (
    echo ✅ Desktop Commander Python server found
) else (
    echo ❌ Desktop Commander Python server NOT found
)
echo.

echo [5/8] Checking Node.js MCP backup server...
if exist "E:\ECHO_XV4\CLAUDE_EXT_BACKUP\ant.dir.gh.wonderwhy-er.desktopcommandermcp\dist\index.js" (
    echo ✅ Node.js MCP backup server found
    set NODE_MCP_AVAILABLE=1
) else (
    echo ❌ Node.js MCP backup server NOT found
    set NODE_MCP_AVAILABLE=0
)
echo.

echo [6/8] Checking Windows API Ultimate server...
if exist "E:\ECHO_XV4\MLS\servers\WINDOWS_API_ULTIMATE.py" (
    echo ✅ Windows API Ultimate server found
) else (
    echo ❌ Windows API Ultimate server NOT found
)
echo.

echo [7/8] Checking port availability...
netstat -ano | findstr :8000 >NUL
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 8000 is in use
) else (
    echo ✅ Port 8000 available
)

netstat -ano | findstr :8343 >NUL
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 8343 is in use
) else (
    echo ✅ Port 8343 available
)
echo.

echo [8/8] Testing simple commands...
echo Listing MLS servers directory...
dir "E:\ECHO_XV4\MLS\servers\*.py" 2>NUL
echo.

echo ===================================================================
echo DIAGNOSTIC COMPLETE
echo ===================================================================
echo.
echo RECOMMENDED ACTIONS:
echo.
if %NODE_MCP_AVAILABLE% EQU 1 (
    echo ✅ Use Node.js MCP server (preferred)
    echo    Run: node "E:\ECHO_XV4\CLAUDE_EXT_BACKUP\ant.dir.gh.wonderwhy-er.desktopcommandermcp\dist\index.js"
) else (
    echo ⚠️  Node.js MCP server missing - use Python fallback
    echo    Run: python "E:\ECHO_XV4\MLS\servers\desktop_commander_server.py"
)
echo.
echo 📋 Next Steps:
echo    1. Start the MCP server (see above)
echo    2. Reload VS Code: Ctrl+Shift+P → "Developer: Reload Window"
echo    3. Test connection: Ctrl+Shift+P → "ECHO: Connect to ECHO Servers"
echo.
echo 🎖️ Authority Level 11.0 - Commander Bobby Don McWilliams II
echo ===================================================================
pause