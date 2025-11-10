# 🔥 MASTER LAUNCHER UNIFIED - PowerShell Launcher
# Commander Bobby Don McWilliams II - Authority Level 11.0
# ECHO PRIME - Production Deployment

Write-Host "🔥 MASTER LAUNCHER UNIFIED - Starting..." -ForegroundColor Cyan
Write-Host "Authority Level: 11.0" -ForegroundColor Green
Write-Host "Target: P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS" -ForegroundColor Yellow
Write-Host ""

# Set location
Set-Location "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION"

# Check Python
$pythonPath = "H:\Tools\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Python not found at $pythonPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python found: $pythonPath" -ForegroundColor Green

# Install dependencies (if needed)
Write-Host "🔧 Checking dependencies..." -ForegroundColor Cyan
& $pythonPath -m pip install --quiet --break-system-packages watchdog flask colorama setproctitle psutil pyyaml requests 2>$null

Write-Host "✅ Dependencies ready" -ForegroundColor Green
Write-Host ""

# Launch Master Launcher
Write-Host "🚀 Launching Master Launcher Unified..." -ForegroundColor Cyan
Write-Host "   Dashboard: http://localhost:9000" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

& $pythonPath "MASTER_LAUNCHER_UNIFIED.py"
