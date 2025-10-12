# Start VS Code API Server
# Authority Level 11.0

Write-Host "Starting ECHO VS Code API Server..." -ForegroundColor Cyan

# Check if port is listening
$portCheck = netstat -ano | findstr :9001
if ($portCheck) {
    Write-Host "SUCCESS: API Server already running on port 9001" -ForegroundColor Green
    Write-Host $portCheck
} else {
    Write-Host "FAILED: API Server not running on port 9001" -ForegroundColor Red
    Write-Host ""
    Write-Host "MANUAL FIX REQUIRED:" -ForegroundColor Yellow
    Write-Host "1. Open VS Code"
    Write-Host "2. Press Ctrl+Shift+P"
    Write-Host "3. Type: ECHO: Start API Server"
    Write-Host "4. Press Enter"
}
