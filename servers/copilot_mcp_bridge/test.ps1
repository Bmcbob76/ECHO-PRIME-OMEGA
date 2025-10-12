# Quick test script to verify ECHO tools are available

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ECHO TOOLSET VERIFICATION TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking VS Code extension status..." -ForegroundColor Yellow
code --list-extensions | Select-String "echo-copilot-bridge"

Write-Host ""
Write-Host "Extension should appear above if installed." -ForegroundColor White
Write-Host ""
Write-Host "To test tools in VS Code:" -ForegroundColor Cyan
Write-Host "1. Open any file in VS Code" -ForegroundColor White
Write-Host "2. Open Copilot Chat" -ForegroundColor White
Write-Host "3. Type: @workspace /tools" -ForegroundColor White
Write-Host "4. You should see 105+ ECHO tools listed" -ForegroundColor White
Write-Host ""
