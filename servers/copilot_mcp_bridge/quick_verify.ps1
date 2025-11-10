# 🚀 ECHO COPILOT BRIDGE - QUICK TEST SCRIPT
# Authority Level: 11.0
# Run this in VS Code terminal to verify installation

Write-Host "🎖️ ECHO COPILOT BRIDGE - VERIFICATION" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Test 1: Check extension is installed
Write-Host "✓ Test 1: Checking extension installation..." -ForegroundColor Yellow
$extensions = code --list-extensions
if ($extensions -like "*echo-copilot-bridge*") {
    Write-Host "  ✅ Extension installed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Extension NOT found" -ForegroundColor Red
    Write-Host "  Run: code --install-extension echo-copilot-bridge-1.0.0.vsix" -ForegroundColor Yellow
}
Write-Host ""

# Test 2: Check if extension files exist
Write-Host "✓ Test 2: Checking extension files..." -ForegroundColor Yellow
$distPath = "E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\dist\extension.js"
if (Test-Path $distPath) {
    $fileSize = (Get-Item $distPath).Length
    Write-Host "  ✅ Extension compiled: extension.js ($fileSize bytes)" -ForegroundColor Green
} else {
    Write-Host "  ❌ Extension.js NOT found" -ForegroundColor Red
}
Write-Host ""

# Test 3: Check MCP server file
Write-Host "✓ Test 3: Checking MCP server..." -ForegroundColor Yellow
$mcpPath = "E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge\desktop_commander_stdio.py"
if (Test-Path $mcpPath) {
    Write-Host "  ✅ MCP server found: desktop_commander_stdio.py" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  MCP server not at expected path" -ForegroundColor Yellow
    Write-Host "  Expected: $mcpPath" -ForegroundColor Gray
}
Write-Host ""

# Test 4: Check Python
Write-Host "✓ Test 4: Checking Python..." -ForegroundColor Yellow
$pythonPath = "H:\Tools\python.exe"
if (Test-Path $pythonPath) {
    $pythonVersion = & $pythonPath --version 2>&1
    Write-Host "  ✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python NOT found at H:\Tools\python.exe" -ForegroundColor Red
}
Write-Host ""

# Test 5: Check VS Code is running
Write-Host "✓ Test 5: Checking VS Code..." -ForegroundColor Yellow
$vscodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue
if ($vscodeProcess) {
    Write-Host "  ✅ VS Code is running (PID: $($vscodeProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  VS Code not running - start it to test extension" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "1. Open VS Code if not already open" -ForegroundColor White
Write-Host "2. Press Ctrl+Shift+P" -ForegroundColor White
Write-Host "3. Type: 'ECHO: Show Connection Status'" -ForegroundColor White
Write-Host "4. Verify you see: '105+ tools registered'" -ForegroundColor White
Write-Host "5. Test with Copilot: '@echo list files in E:\ECHO_XV4'" -ForegroundColor White
Write-Host ""
Write-Host "📊 See VERIFICATION_TESTS.md for complete testing guide" -ForegroundColor Gray
Write-Host ""
Write-Host "🎖️ Commander Bobby - Authority Level 11.0" -ForegroundColor Cyan
