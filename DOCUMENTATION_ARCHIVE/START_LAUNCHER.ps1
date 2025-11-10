# PowerShell Launcher for ECHO_XV4 MLS

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   ECHO_XV4 MASTER LAUNCHER" -ForegroundColor Yellow
Write-Host "   LAUNCHING WITH DISPLAY" -ForegroundColor Yellow  
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Kill existing Python
Write-Host "Stopping existing Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Change to MLS directory
Set-Location "E:\ECHO_XV4\MLS"

# Check if simple_launcher.py exists
if (Test-Path "simple_launcher.py") {
    Write-Host "Found launcher script" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting launcher..." -ForegroundColor Cyan
    Write-Host ""
    
    # Run Python script
    python simple_launcher.py
    
} else {
    Write-Host "ERROR: simple_launcher.py not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
