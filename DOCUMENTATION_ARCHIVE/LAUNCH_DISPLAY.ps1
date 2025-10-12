# ECHO_XV4 Master Modular Launcher V3 - PowerShell Launch Script
# Full Display with Server Details

Clear-Host
$Host.UI.RawUI.WindowTitle = "ECHO_XV4 MASTER MODULAR LAUNCHER V3"
$Host.UI.RawUI.ForegroundColor = "Green"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    ECHO_XV4 MASTER MODULAR LAUNCHER V3                        " -ForegroundColor Cyan
Write-Host "                         AUTHORITY LEVEL 11.0                                  " -ForegroundColor Cyan
Write-Host "                    Commander Bobby Don McWilliams II                          " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Kill existing Python processes
Write-Host "[CLEANUP] Terminating existing Python processes..." -ForegroundColor Yellow
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "[OK] Clean startup environment ready" -ForegroundColor Green
Write-Host ""

# Change to MLS directory
Set-Location "E:\ECHO_XV4\MLS"
Write-Host "[INFO] Working Directory: $PWD" -ForegroundColor White
Write-Host ""

# Set environment variables
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:ECHO_DEBUG = "1"
$env:MCP_ENABLED = "1"
$env:SHOW_SERVER_DETAILS = "1"

# Display system info
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                            SYSTEM INFORMATION                                 " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "[TIME] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "[USER] $env:USERNAME" -ForegroundColor White
Write-Host "[COMPUTER] $env:COMPUTERNAME" -ForegroundColor White
Write-Host "[AUTHORITY] Level 11.0 - Maximum Authority" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "[CHECK] Python Installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Discover servers
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                         DISCOVERING SERVERS                                   " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "[SCAN] Scanning E:\ECHO_XV4\MLS\servers\..." -ForegroundColor Yellow
Write-Host ""

$servers = Get-ChildItem -Path "servers\*.py" -ErrorAction SilentlyContinue
$serverCount = $servers.Count

Write-Host "[FOUND] $serverCount Python servers detected" -ForegroundColor Green
Write-Host ""
Write-Host "Servers found:" -ForegroundColor White
Write-Host "───────────────────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$port = 8000
foreach ($server in $servers) {
    $serverName = $server.BaseName
    $isMCP = $serverName -like "*mcp*"
    
    if ($isMCP) {
        Write-Host "  ► $serverName (Port: $port) [MCP-ENABLED]" -ForegroundColor Cyan
    } else {
        Write-Host "  ► $serverName (Port: $port)" -ForegroundColor White
    }
    $port++
}
Write-Host "───────────────────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

# Display configuration
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                        LAUNCH CONFIGURATION                                   " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan

$config = @{
    "Dashboard" = "http://localhost:9000"
    "Base Port" = "8000"
    "Health Check" = "Every 30 seconds"
    "Auto-Heal" = "Phoenix Protocol Active"
    "Hot Reload" = "File watcher enabled"
    "MCP Integration" = "Claude Desktop ready"
    "Docker Support" = "Enabled"
}

foreach ($key in $config.Keys) {
    Write-Host ("[{0,-15}] {1}" -f $key, $config[$key]) -ForegroundColor White
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                         STARTING SYSTEM                                       " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "[NOTICE] The following will happen:" -ForegroundColor Yellow
Write-Host "  1. Auto-discover ALL servers in servers\ directory" -ForegroundColor White
Write-Host "  2. Assign unique ports starting from 8000" -ForegroundColor White
Write-Host "  3. Launch each server in its own process" -ForegroundColor White
Write-Host "  4. Monitor health every 30 seconds" -ForegroundColor White
Write-Host "  5. Auto-restart failed servers" -ForegroundColor White
Write-Host "  6. Display live status at http://localhost:9000" -ForegroundColor White
Write-Host ""
Write-Host "[INFO] Press Ctrl+C at any time to stop all servers" -ForegroundColor Yellow
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "                    LAUNCHING MASTER MODULAR LAUNCHER V3                       " -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# Function to display server launch status
function Show-ServerStatus {
    param($Line)
    
    if ($Line -match "Launching|Starting") {
        Write-Host "► $Line" -ForegroundColor Cyan
    }
    elseif ($Line -match "✅|SUCCESS|started|running") {
        Write-Host "✓ $Line" -ForegroundColor Green
    }
    elseif ($Line -match "❌|ERROR|failed") {
        Write-Host "✗ $Line" -ForegroundColor Red
    }
    elseif ($Line -match "⚠️|WARNING") {
        Write-Host "⚠ $Line" -ForegroundColor Yellow
    }
    elseif ($Line -match "Dashboard.*http") {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Green
        Write-Host "$Line" -ForegroundColor Cyan
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Green
        Write-Host ""
    }
    else {
        Write-Host "$Line" -ForegroundColor Gray
    }
}

Write-Host "[LAUNCH] Starting Master Modular Launcher with full output..." -ForegroundColor Green
Write-Host ""

# Launch Python with real-time output
try {
    $process = Start-Process python -ArgumentList "-u", "master_modular_launcher_enhanced.py" -PassThru -NoNewWindow -Wait
    
    if ($process.ExitCode -ne 0) {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Red
        Write-Host "                              ERROR OCCURRED                                   " -ForegroundColor Red
        Write-Host "═══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Red
        Write-Host "[ERROR] Launcher exited with code $($process.ExitCode)" -ForegroundColor Red
        Write-Host "[INFO] Check logs\master.log for details" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Failed to launch: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to exit..."
Read-Host
