# ECHO Copilot Bridge - Automated Installation & Activation
# Authority Level 11.0 - Commander Bobby Don McWilliams II

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ECHO COPILOT BRIDGE - INSTALLATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$extensionPath = "E:\ECHO_XV4\MLS\servers\copilot_mcp_bridge"

try {
    # Step 1: Navigate to extension directory
    Write-Host "[1/6] Navigating to extension directory..." -ForegroundColor Yellow
    Set-Location $extensionPath
    Write-Host "✓ Location: $extensionPath" -ForegroundColor Green
    Write-Host ""

    # Step 2: Install dependencies
    Write-Host "[2/6] Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) { throw "npm install failed" }
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
    Write-Host ""

    # Step 3: Compile TypeScript
    Write-Host "[3/6] Compiling TypeScript..." -ForegroundColor Yellow
    npm run compile
    if ($LASTEXITCODE -ne 0) { throw "TypeScript compilation failed" }
    Write-Host "✓ TypeScript compiled successfully" -ForegroundColor Green
    Write-Host ""

    # Step 4: Install VSCE if not present
    Write-Host "[4/6] Checking for VSCE..." -ForegroundColor Yellow
    $vsceInstalled = Get-Command vsce -ErrorAction SilentlyContinue
    if (-not $vsceInstalled) {
        Write-Host "Installing VSCE globally..." -ForegroundColor Yellow
        npm install -g @vscode/vsce
        if ($LASTEXITCODE -ne 0) { throw "VSCE installation failed" }
    }
    Write-Host "✓ VSCE ready" -ForegroundColor Green
    Write-Host ""

    # Step 5: Package extension
    Write-Host "[5/6] Packaging extension..." -ForegroundColor Yellow
    vsce package --allow-star-activation
    if ($LASTEXITCODE -ne 0) { throw "Extension packaging failed" }
    Write-Host "✓ Extension packaged" -ForegroundColor Green
    Write-Host ""

    # Step 6: Install in VS Code
    Write-Host "[6/6] Installing extension in VS Code..." -ForegroundColor Yellow
    $vsixFile = Get-ChildItem -Path $extensionPath -Filter "*.vsix" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if (-not $vsixFile) {
        throw "No .vsix file found"
    }
    
    code --install-extension $vsixFile.FullName --force
    if ($LASTEXITCODE -ne 0) { throw "VS Code installation failed" }
    Write-Host "✓ Extension installed: $($vsixFile.Name)" -ForegroundColor Green

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ INSTALLATION COMPLETE" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Reload VS Code (Ctrl+Shift+P > Developer: Reload Window)" -ForegroundColor White
    Write-Host "2. Verify extension is active in Extensions panel" -ForegroundColor White
    Write-Host "3. Test tools with: @workspace /tools" -ForegroundColor White
    Write-Host ""
    Write-Host "To start MCP servers, run:" -ForegroundColor Yellow
    Write-Host "cd E:\ECHO_XV4\MLS" -ForegroundColor White
    Write-Host "py master_modular_launcher_enhanced.py" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ INSTALLATION FAILED" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check that Node.js is installed: node --version" -ForegroundColor White
    Write-Host "2. Check that VS Code is in PATH: code --version" -ForegroundColor White
    Write-Host "3. Review TypeScript errors: npm run compile" -ForegroundColor White
    Write-Host ""
    exit 1
}
