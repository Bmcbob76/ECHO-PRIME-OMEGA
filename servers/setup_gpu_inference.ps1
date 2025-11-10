# 🎖️ GPU INFERENCE AUTOMATED SETUP SCRIPT
# Authority Level: 11.0
# Commander: Bobby Don McWilliams II
# 
# Automated setup for ECHO_XV4 main computer
# Run this after completing GPU machine setup
#
# Location: E:\ECHO_XV4\MLS\servers\setup_gpu_inference.ps1

param(
    [string]$GPUServerIP = "192.168.1.100",
    [string]$Model = "mixtral:8x7b-instruct-v0.1-q4_K_M"
)

Write-Host "🎖️ GPU INFERENCE SYSTEM - AUTOMATED SETUP" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Commander: Bobby Don McWilliams II" -ForegroundColor Yellow
Write-Host "Authority Level: 11.0" -ForegroundColor Yellow
Write-Host ""

$ErrorActionPreference = "Stop"
$ScriptDir = "E:\ECHO_XV4\MLS\servers"
$PythonExe = "H:\Tools\python.exe"

# ============================================================================
# STEP 1: VERIFY PREREQUISITES
# ============================================================================

Write-Host "📋 STEP 1: Verifying Prerequisites..." -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "  Checking Python installation..." -NoNewline
if (Test-Path $PythonExe) {
    Write-Host " ✅" -ForegroundColor Green
    $version = & $PythonExe --version
    Write-Host "     Version: $version" -ForegroundColor Gray
} else {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "     Python not found at: $PythonExe" -ForegroundColor Red
    exit 1
}

# Check GS343 Foundation
Write-Host "  Checking GS343 Foundation..." -NoNewline
if (Test-Path "E:\GS343\FOUNDATION\gs343_foundation_core.py") {
    Write-Host " ✅" -ForegroundColor Green
} else {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "     GS343 Foundation not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 2: INSTALL PYTHON DEPENDENCIES
# ============================================================================

Write-Host "📦 STEP 2: Installing Python Dependencies..." -ForegroundColor Green
Write-Host ""

$packages = @("flask", "flask-cors", "requests")

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -NoNewline
    try {
        & $PythonExe -m pip install $package --break-system-packages --quiet 2>&1 | Out-Null
        Write-Host " ✅" -ForegroundColor Green
    } catch {
        Write-Host " ⚠️  Already installed or error" -ForegroundColor Yellow
    }
}

Write-Host ""

# ============================================================================
# STEP 3: UPDATE CONFIGURATION
# ============================================================================

Write-Host "⚙️  STEP 3: Updating Configuration..." -ForegroundColor Green
Write-Host ""

$configPath = Join-Path $ScriptDir "gpu_config.env"

Write-Host "  Updating GPU server IP: $GPUServerIP" -ForegroundColor Gray
Write-Host "  Updating model: $Model" -ForegroundColor Gray

# Read existing config
$configContent = Get-Content $configPath -Raw

# Update values
$configContent = $configContent -replace "GPU_SERVER_HOST=.*", "GPU_SERVER_HOST=$GPUServerIP"
$configContent = $configContent -replace "GPU_MODEL=.*", "GPU_MODEL=$Model"

# Write back
Set-Content -Path $configPath -Value $configContent -NoNewline

Write-Host "  Configuration updated ✅" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 4: TEST GPU SERVER CONNECTIVITY
# ============================================================================

Write-Host "🔗 STEP 4: Testing GPU Server Connectivity..." -ForegroundColor Green
Write-Host ""

Write-Host "  Testing connection to $GPUServerIP`:11434..." -NoNewline

try {
    $response = Invoke-WebRequest -Uri "http://${GPUServerIP}:11434/api/tags" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
        
        $json = $response.Content | ConvertFrom-Json
        $modelCount = $json.models.Count
        Write-Host "     Models available: $modelCount" -ForegroundColor Gray
        
        if ($modelCount -eq 0) {
            Write-Host ""
            Write-Host "  ⚠️  WARNING: No models found on GPU server!" -ForegroundColor Yellow
            Write-Host "     On GPU machine run: ollama pull $Model" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host ""
    Write-Host "  ⚠️  Cannot connect to GPU server!" -ForegroundColor Red
    Write-Host "     Please verify:" -ForegroundColor Yellow
    Write-Host "       1. GPU machine is powered on" -ForegroundColor Yellow
    Write-Host "       2. Ollama is installed and running" -ForegroundColor Yellow
    Write-Host "       3. IP address is correct: $GPUServerIP" -ForegroundColor Yellow
    Write-Host "       4. Firewall allows port 11434" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Run setup again after fixing connectivity" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 5: RUN TEST SUITE
# ============================================================================

Write-Host "🧪 STEP 5: Running Test Suite..." -ForegroundColor Green
Write-Host ""

$testScript = Join-Path $ScriptDir "test_gpu_inference.py"

# Load environment variables for test
$env:GPU_SERVER_HOST = $GPUServerIP
$env:GPU_MODEL = $Model

Write-Host "  Executing tests (this may take 30-60 seconds)..." -ForegroundColor Gray
Write-Host ""

try {
    & $PythonExe $testScript
    $testExitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($testExitCode -eq 0) {
        Write-Host "  ✅ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Some tests failed (exit code: $testExitCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Test execution failed: $_" -ForegroundColor Red
}

Write-Host ""

# ============================================================================
# STEP 6: SETUP COMPLETE
# ============================================================================

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Test the Python client:" -ForegroundColor White
Write-Host "     cd $ScriptDir" -ForegroundColor Gray
Write-Host "     $PythonExe" -ForegroundColor Gray
Write-Host "     >>> from gpu_inference_client import GPUInferenceClient, GPUServerConfig" -ForegroundColor Gray
Write-Host "     >>> config = GPUServerConfig(host='$GPUServerIP')" -ForegroundColor Gray
Write-Host "     >>> client = GPUInferenceClient(config)" -ForegroundColor Gray
Write-Host "     >>> result = client.generate('Hello!')" -ForegroundColor Gray
Write-Host ""

Write-Host "  2. Start the API server:" -ForegroundColor White
Write-Host "     cd $ScriptDir" -ForegroundColor Gray
Write-Host "     $PythonExe gpu_inference_server.py" -ForegroundColor Gray
Write-Host ""

Write-Host "  3. Test API endpoints:" -ForegroundColor White
Write-Host "     curl http://localhost:8070/health" -ForegroundColor Gray
Write-Host "     curl -X POST http://localhost:8070/api/generate -H 'Content-Type: application/json' -d '{""prompt"": ""Hello!""}'" -ForegroundColor Gray
Write-Host ""

Write-Host "  4. Read the documentation:" -ForegroundColor White
Write-Host "     notepad $ScriptDir\GPU_INFERENCE_SETUP.md" -ForegroundColor Gray
Write-Host ""

Write-Host "🎖️ System ready for deployment!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration saved to: $configPath" -ForegroundColor Gray
Write-Host "GPU Server: $GPUServerIP`:11434" -ForegroundColor Gray
Write-Host "Model: $Model" -ForegroundColor Gray
Write-Host ""
