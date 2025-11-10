@echo off
echo ===================================================================
echo ECHO COPILOT BRIDGE - EMERGENCY BYPASS COMPILATION
echo Commander Bobby Don McWilliams II - Authority Level 11.0  
echo ===================================================================
echo.

echo [1/4] Creating dist directory...
if not exist "dist" mkdir dist
echo ✅ dist/ directory ready

echo.
echo [2/4] Copying pre-compiled extension...
copy /Y "COMPILED_EXTENSION.js" "dist\extension.js"
if %ERRORLEVEL% EQU 0 (
    echo ✅ extension.js copied to dist/
) else (
    echo ❌ Failed to copy extension.js
    pause
    exit /b 1
)

echo.
echo [3/4] Packaging extension...
npx vsce package --allow-missing-repository --no-yarn 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo ✅ Extension packaged successfully
) else (
    echo ❌ Packaging failed - trying alternative...
    echo Installing vsce globally...
    npm install -g @vscode/vsce
    vsce package --allow-missing-repository --no-yarn
)

echo.
echo [4/4] Installing extension...
for %%f in (*.vsix) do (
    echo Installing: %%f
    code --install-extension "%%f" --force
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Extension installed successfully
    ) else (
        echo ❌ Installation failed
    )
)

echo.
echo ===================================================================
echo BYPASS COMPILATION COMPLETE
echo ===================================================================
echo.
echo Next Steps:
echo 1. Start MCP server: node "E:\ECHO_XV4\CLAUDE_EXT_BACKUP\ant.dir.gh.wonderwhy-er.desktopcommandermcp\dist\index.js"
echo 2. Reload VS Code: Ctrl+Shift+P → "Developer: Reload Window"  
echo 3. Connect: Ctrl+Shift+P → "ECHO: Connect to ECHO Servers"
echo 4. Check status bar for: ⚡ ECHO Connected (XX tools)
echo.
echo 🎖️ Authority Level 11.0 - Emergency Deployment Complete
echo ===================================================================
pause