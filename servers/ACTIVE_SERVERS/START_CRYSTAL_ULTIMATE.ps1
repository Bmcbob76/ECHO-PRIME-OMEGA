#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Launch Crystal Memory Ultimate Master Server

.DESCRIPTION
    Starts the ULTIMATE MASTER crystal memory server with all features
    compiled from 7 different server versions.

.PARAMETER Port
    Port number to run the server on (default: 8002)

.PARAMETER Background
    Run in background mode (no console window)

.EXAMPLE
    .\START_CRYSTAL_ULTIMATE.ps1
    Start server on default port 8002

.EXAMPLE
    .\START_CRYSTAL_ULTIMATE.ps1 -Port 8003
    Start server on custom port 8003

.EXAMPLE
    .\START_CRYSTAL_ULTIMATE.ps1 -Background
    Start server in background mode
#>

param(
    [int]$Port = 8002,
    [switch]$Background
)

# Colors for output
$ErrorActionPreference = "Continue"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "💎🔮 " -NoNewline -ForegroundColor Yellow
Write-Host "CRYSTAL MEMORY ULTIMATE MASTER - LAUNCHER" -ForegroundColor White
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Server path
$ServerPath = "E:\ECHO_XV4\MLS\servers\ACTIVE_SERVERS\CRYSTAL_MEMORY_ULTIMATE_MASTER.py"

# Check if server file exists
if (-not (Test-Path $ServerPath)) {
    Write-Host "❌ ERROR: Server file not found!" -ForegroundColor Red
    Write-Host "   Expected: $ServerPath" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Server file found" -ForegroundColor Green
Write-Host "📁 Location: $ServerPath" -ForegroundColor Gray
Write-Host ""

# Check Python
Write-Host "🐍 Checking Python..." -NoNewline
try {
    $PythonVersion = python --version 2>&1
    Write-Host " $PythonVersion" -ForegroundColor Green
}
catch {
    Write-Host " ❌ Python not found!" -ForegroundColor Red
    Write-Host "   Install Python 3.8+ and add to PATH" -ForegroundColor Yellow
    exit 1
}

# Check if port is available
Write-Host "🔌 Checking port $Port..." -NoNewline
$PortCheck = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
if ($PortCheck) {
    Write-Host " ⚠️  Port already in use!" -ForegroundColor Yellow
    Write-Host "   Another service is using port $Port" -ForegroundColor Gray
    $Continue = Read-Host "   Continue anyway? (y/n)"
    if ($Continue -ne "y") {
        exit 0
    }
}
else {
    Write-Host " Available ✅" -ForegroundColor Green
}

# Check dependencies
Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan

$RequiredPackages = @("flask")
$OptionalPackages = @(
    "psutil",
    "PIL",
    "pywin32",
    "pytesseract",
    "cv2",
    "numpy",
    "easyocr",
    "torch",
    "watchdog"
)

$MissingRequired = @()
$MissingOptional = @()

foreach ($pkg in $RequiredPackages) {
    $check = python -c "import $pkg" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $MissingRequired += $pkg
        Write-Host "   ❌ $pkg (REQUIRED)" -ForegroundColor Red
    }
    else {
        Write-Host "   ✅ $pkg" -ForegroundColor Green
    }
}

foreach ($pkg in $OptionalPackages) {
    # Handle special package names
    $importName = $pkg
    if ($pkg -eq "PIL") { $importName = "PIL" }
    if ($pkg -eq "cv2") { $importName = "cv2" }
    if ($pkg -eq "pywin32") { $importName = "win32api" }

    $check = python -c "import $importName" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $MissingOptional += $pkg
        Write-Host "   ⚠️  $pkg (optional, feature disabled)" -ForegroundColor Yellow
    }
    else {
        Write-Host "   ✅ $pkg" -ForegroundColor Green
    }
}

if ($MissingRequired.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Missing REQUIRED packages!" -ForegroundColor Red
    Write-Host "   Install with: pip install $($MissingRequired -join ' ')" -ForegroundColor Yellow
    exit 1
}

if ($MissingOptional.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Missing optional packages (server will work with reduced features)" -ForegroundColor Yellow
    Write-Host "   Install with: pip install $($MissingOptional -join ' ')" -ForegroundColor Gray
}

# Check disk space
Write-Host ""
Write-Host "💾 Checking disk space..." -NoNewline
$Drive = Get-PSDrive -Name E
$FreeGB = [math]::Round($Drive.Free / 1GB, 2)
if ($FreeGB -lt 1) {
    Write-Host " ⚠️  Low disk space: $FreeGB GB" -ForegroundColor Yellow
}
else {
    Write-Host " $FreeGB GB available ✅" -ForegroundColor Green
}

# Create directories if needed
Write-Host ""
Write-Host "📁 Preparing directories..." -ForegroundColor Cyan

$Directories = @(
    "E:\ECHO_XV4\DATA\CRYSTAL_MEMORIES\live_capture",
    "E:\ECHO_XV4\DATA\CRYSTAL_MEMORIES\compressed_archive",
    "E:\ECHO_XV4\DATA\CRYSTAL_MEMORIES\recovery_scraping",
    "E:\ECHO_XV4\DATA\CRYSTAL_MEMORIES\temp_processing",
    "E:\ECHO_XV4\DATA\CRYSTAL_MEMORIES\captured_artifacts",
    "E:\ECHO_XV4\BACKUPS\CRYSTAL",
    "E:\ECHO_XV4\logs",
    "M:\MASTER_EKM"
)

foreach ($dir in $Directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✅ Created: $dir" -ForegroundColor Green
    }
    else {
        Write-Host "   ✅ Exists: $dir" -ForegroundColor Gray
    }
}

# Voice announcement
Write-Host ""
Write-Host "🎤 Voice announcement..." -ForegroundColor Cyan
try {
    python -c "import asyncio; from epcp3o_voice_integrated import EPCP3OVoiceSystem; voice = EPCP3OVoiceSystem(); voice.initialize(); voice.play_r2d2_sound('excited'); asyncio.run(voice.speak_c3po('Launching Ultimate Crystal Memory Server on port $Port! All systems ready Commander!', voice_id='0UTDtgGGkpqERQn1s0YK', emotion='excited'))" 2>$null
}
catch {
    # Silent fail if voice system not available
}

# Launch server
Write-Host ""
Write-Host "🚀 LAUNCHING ULTIMATE CRYSTAL MEMORY SERVER" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Server Information:" -ForegroundColor Cyan
Write-Host "   Port: $Port" -ForegroundColor White
Write-Host "   Health Check: http://localhost:$Port/health" -ForegroundColor White
Write-Host "   MCP Tools: http://localhost:$Port/mcp/tools" -ForegroundColor White
Write-Host "   Statistics: http://localhost:$Port/memory/stats" -ForegroundColor White
Write-Host ""
Write-Host "💡 Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Launch
if ($Background) {
    Write-Host "🔇 Starting in background mode..." -ForegroundColor Yellow
    $ProcessArgs = @{
        FilePath     = "pythonw"
        ArgumentList = @($ServerPath, "--port=$Port")
        WindowStyle  = "Hidden"
    }
    Start-Process @ProcessArgs
    Write-Host "✅ Server started in background" -ForegroundColor Green
    Write-Host "   Check logs: E:\ECHO_XV4\logs\crystal_memory_ultimate.log" -ForegroundColor Gray
}
else {
    # Run in foreground
    python $ServerPath --port=$Port
}

Write-Host ""
Write-Host "🛑 Server stopped" -ForegroundColor Yellow
