# ULTIMATE AUTO-HEALING LAUNCHER - STARTUP SCRIPT
# Commander: Bobby Don McWilliams II
# Authority Level: 11.0
# Runs 24/7 with 30-minute check cycles

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🚀 ULTIMATE AUTO-HEALING LAUNCHER - GS343 PHOENIX EDITION" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Check if already running
$existingProcess = Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $cmdline = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine
    $cmdline -like "*ULTIMATE_AUTO_HEALING_LAUNCHER*"
}

if ($existingProcess) {
    Write-Host "⚠️  Launcher already running (PID: $($existingProcess.Id))" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Restart? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "🛑 Stopping existing launcher..." -ForegroundColor Red
        Stop-Process -Id $existingProcess.Id -Force
        Start-Sleep -Seconds 2
    }
    else {
        Write-Host "✅ Keeping existing launcher running" -ForegroundColor Green
        exit 0
    }
}

Write-Host "🎖️  Authority Level: 11.0" -ForegroundColor Cyan
Write-Host "👤 Commander: Bobby Don McWilliams II" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features:" -ForegroundColor White
Write-Host "  ✅ 30-minute automatic check cycles" -ForegroundColor Green
Write-Host "  ✅ Auto-detects running servers (no relaunching)" -ForegroundColor Green
Write-Host "  ✅ Phoenix auto-healing with 45,962+ error templates" -ForegroundColor Green
Write-Host "  ✅ Quarantines busted servers with diagnostics" -ForegroundColor Green
Write-Host "  ✅ GS343 Foundation integration" -ForegroundColor Green
Write-Host "  ✅ EKM training and pattern recognition" -ForegroundColor Green
Write-Host ""

# Start launcher
Write-Host "🚀 Starting Ultimate Auto-Healing Launcher..." -ForegroundColor Yellow
Write-Host ""

$pythonExe = "H:\Tools\python.exe"
$launcherScript = "E:\ECHO_XV4\MLS\ULTIMATE_AUTO_HEALING_LAUNCHER.py"

# Check files exist
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python not found: $pythonExe" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $launcherScript)) {
    Write-Host "❌ Launcher script not found: $launcherScript" -ForegroundColor Red
    exit 1
}

# Start in new window
$process = Start-Process -FilePath $pythonExe -ArgumentList $launcherScript -PassThru -WindowStyle Normal

Start-Sleep -Seconds 2

if ($process -and !$process.HasExited) {
    Write-Host "✅ Launcher started successfully!" -ForegroundColor Green
    Write-Host "   PID: $($process.Id)" -ForegroundColor Cyan
    Write-Host "   Script: $launcherScript" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📊 Check logs at: E:\ECHO_XV4\MLS\logs\" -ForegroundColor Cyan
    Write-Host "📋 Master reports generated every 6 hours" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C in launcher window to stop" -ForegroundColor Yellow
}
else {
    Write-Host "❌ Failed to start launcher" -ForegroundColor Red
    exit 1
}
