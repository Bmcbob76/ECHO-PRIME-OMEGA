#!/usr/bin/env pwsh
# ECHO MCP Tool Registration Diagnostic
# Authority Level: 11.0

Write-Host "🎖️ ECHO MCP TOOL DIAGNOSTIC" -ForegroundColor Cyan
Write-Host "=" * 50

# Step 1: Check if extension is installed
Write-Host "`n[1] Checking Extension Status..." -ForegroundColor Yellow
$extensionPath = "E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge"
if (Test-Path $extensionPath) {
    Write-Host "✅ Extension found at: $extensionPath" -ForegroundColor Green
} else {
    Write-Host "❌ Extension not found!" -ForegroundColor Red
    exit 1
}

# Step 2: Check if VSIX is installed
Write-Host "`n[2] Checking VSIX Installation..." -ForegroundColor Yellow
$vsixPath = "$extensionPath\echo-copilot-bridge-2.1.0.vsix"
if (Test-Path $vsixPath) {
    Write-Host "✅ VSIX exists: $vsixPath" -ForegroundColor Green
} else {
    Write-Host "❌ VSIX not found!" -ForegroundColor Red
}

# Step 3: Check VS Code extensions
Write-Host "`n[3] Checking VS Code Extensions..." -ForegroundColor Yellow
$installedExtensions = code --list-extensions 2>$null
if ($installedExtensions -match "echo-copilot-bridge") {
    Write-Host "✅ ECHO MCP Bridge is installed in VS Code" -ForegroundColor Green
} else {
    Write-Host "⚠️  Extension may not be installed. Installing now..." -ForegroundColor Yellow
    code --install-extension "$vsixPath" --force
    Write-Host "✅ Extension installed. Please reload VS Code." -ForegroundColor Green
}

# Step 4: Verify settings
Write-Host "`n[4] Checking VS Code Settings..." -ForegroundColor Yellow
$settingsPath = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
    
    if ($settings."echo.mcp.autoStart" -eq $true) {
        Write-Host "✅ Auto-start enabled" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Auto-start disabled" -ForegroundColor Yellow
    }
    
    if ($settings."github.copilot.chat.executableTools.enabled" -eq $true) {
        Write-Host "✅ Copilot executable tools enabled" -ForegroundColor Green
    } else {
        Write-Host "❌ Copilot executable tools DISABLED - FIX THIS!" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Settings file not found!" -ForegroundColor Red
}

# Step 5: Test MCP server directly
Write-Host "`n[5] Testing MCP Server..." -ForegroundColor Yellow
$pythonPath = "H:\Tools\python.exe"
$serverPath = "$extensionPath\desktop_commander_stdio.py"

if (Test-Path $pythonPath) {
    Write-Host "✅ Python found: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found at: $pythonPath" -ForegroundColor Red
    exit 1
}

Write-Host "Testing MCP protocol..." -ForegroundColor Cyan
$testRequest = '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
$result = $testRequest | & $pythonPath $serverPath 2>$null | Select-Object -First 1

if ($result) {
    $tools = ($result | ConvertFrom-Json).result.tools
    Write-Host "✅ Server responding! Found $($tools.Count) tools:" -ForegroundColor Green
    foreach ($tool in $tools) {
        Write-Host "   • $($tool.name)" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ Server not responding!" -ForegroundColor Red
}

# Step 6: Instructions
Write-Host "`n" + "=" * 50
Write-Host "📋 NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Reload VS Code Window:" -ForegroundColor Yellow
Write-Host "   Ctrl+Shift+P → 'Developer: Reload Window'" -ForegroundColor White
Write-Host ""
Write-Host "2. Open Command Palette:" -ForegroundColor Yellow
Write-Host "   Ctrl+Shift+P → 'ECHO: Check Server Health'" -ForegroundColor White
Write-Host ""
Write-Host "3. Verify Tools in Copilot:" -ForegroundColor Yellow
Write-Host "   • Open Copilot Chat (Ctrl+Alt+I)" -ForegroundColor White
Write-Host "   • Type: '@workspace /tools'" -ForegroundColor White
Write-Host "   • Should see: read_file, write_file, list_directory, execute_command" -ForegroundColor White
Write-Host ""
Write-Host "4. If still not working:" -ForegroundColor Yellow
Write-Host "   • Check VS Code > Settings > Extensions > GitHub Copilot" -ForegroundColor White
Write-Host "   • Ensure 'Chat: Executable Tools' is ENABLED" -ForegroundColor White
Write-Host ""
Write-Host "=" * 50

Write-Host "`n✅ Diagnostic complete!" -ForegroundColor Green
