# Master Modular Launcher V3 - Installation Script
# ECHO_XV4 Production System

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "     MASTER MODULAR LAUNCHER V3 - INSTALLATION" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[CHECK] Verifying Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip
Write-Host "[CHECK] Verifying pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "[OK] Found pip" -ForegroundColor Green
} catch {
    Write-Host "[WARN] pip not found, attempting to install..." -ForegroundColor Yellow
    python -m ensurepip --default-pip
}

# Install requirements
Write-Host ""
Write-Host "[INSTALL] Installing required packages..." -ForegroundColor Yellow

$packages = @(
    "pyyaml",
    "psutil",
    "requests",
    "aiohttp",
    "watchdog",
    "flask",
    "flask-cors",
    "numpy",
    "python-dotenv"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet --upgrade
}

# Try to install MCP (optional)
Write-Host ""
Write-Host "[OPTIONAL] Checking MCP for Claude integration..." -ForegroundColor Yellow
try {
    pip show mcp | Out-Null
    Write-Host "[OK] MCP already installed" -ForegroundColor Green
} catch {
    Write-Host "[INFO] MCP not installed. This is optional for Claude Desktop integration." -ForegroundColor Cyan
    $installMCP = Read-Host "Would you like to install MCP? (y/n)"
    if ($installMCP -eq 'y') {
        pip install mcp
        Write-Host "[OK] MCP installed" -ForegroundColor Green
    }
}

# Check Docker (optional)
Write-Host ""
Write-Host "[OPTIONAL] Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "[OK] Found $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Docker not found. This is optional for container support." -ForegroundColor Cyan
}

# Create directories
Write-Host ""
Write-Host "[SETUP] Creating directory structure..." -ForegroundColor Yellow

$directories = @(
    "E:\ECHO_XV4\MLS\servers",
    "E:\ECHO_XV4\MLS\logs",
    "E:\ECHO_XV4\MLS\static"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}

# Check GS343 Foundation
Write-Host ""
Write-Host "[CHECK] Checking GS343 Foundation..." -ForegroundColor Yellow
if (Test-Path "E:\GS343\FOUNDATION\gs343_foundation_core.py") {
    Write-Host "[OK] GS343 Foundation found" -ForegroundColor Green
} else {
    Write-Host "[WARN] GS343 Foundation not found. Some features will be limited." -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "     INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review configuration: config.yaml" -ForegroundColor White
Write-Host "2. Add servers to: E:\ECHO_XV4\MLS\servers\" -ForegroundColor White
Write-Host "3. Launch system: .\launch_v3.bat" -ForegroundColor White
Write-Host "4. Access dashboard: http://localhost:9000" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: DOCUMENTATION.md" -ForegroundColor Gray
Write-Host ""

$launch = Read-Host "Would you like to launch the system now? (y/n)"
if ($launch -eq 'y') {
    Write-Host ""
    Write-Host "[LAUNCH] Starting Master Modular Launcher V3..." -ForegroundColor Green
    Set-Location "E:\ECHO_XV4\MLS"
    python master_modular_launcher_enhanced.py
}
