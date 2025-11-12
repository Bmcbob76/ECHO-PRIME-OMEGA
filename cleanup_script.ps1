# Production Reorganization Script
$removePatterns = @(
    'test_*.py',
    'TEST_DC_ALIVE.txt',
    'DEBUG_*.md',
    'omega_debug_brain.py',
    'LAUNCH*.py',
    'LAUNCH*.bat',
    'LAUNCH*.ps1',
    'START_*.bat',
    'RUN_*.bat',
    'BENCHMARK.bat',
    'STATUS.bat',
    'run_stt.bat',
    '*integrator*.py',
    'b_drive_crystal_analysis.py',
    'quick_mdrive_test.py',
    'quick_status.py',
    '*_emotions.py',
    'fix_launcher.py',
    'dual_model_orchestrator.py',
    'csv_diagnostic.py',
    'crystal_timestamp_query.py',
    'temp_db_query.py',
    '*_backup*.py',
    '*_temp*.py'
)

$count = 0
foreach($pattern in $removePatterns) {
    $files = Get-ChildItem -Path . -Recurse -Filter $pattern -File -ErrorAction SilentlyContinue
    foreach($file in $files) {
        if($file.FullName -notlike '*venv*' -and $file.FullName -notlike '*site-packages*') {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
            $count++
        }
    }
}
Write-Host "Removed $count redundant files"
