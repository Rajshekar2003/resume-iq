# Day 10 — Market Analysis endpoint test
# Run from backend/test_files/ or any directory: .\test_market.ps1
# Requires: Flask server running on localhost:5000

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BackendDir = Split-Path -Parent $ScriptDir
$ResumeFile = Join-Path $ScriptDir "Rajshekar_RC_Resume.pdf"
$ChromaDir = Join-Path $BackendDir "rag\data\chroma_db"

# Check ChromaDB index exists
if (-not (Test-Path $ChromaDir)) {
    Write-Host "ERROR: ChromaDB index not found at $ChromaDir" -ForegroundColor Red
    Write-Host "Run this first (from backend/):" -ForegroundColor Yellow
    Write-Host "  python -m rag.build_index" -ForegroundColor Cyan
    exit 1
}

# Check resume file exists
if (-not (Test-Path $ResumeFile)) {
    Write-Host "ERROR: Resume not found at $ResumeFile" -ForegroundColor Red
    exit 1
}

Write-Host "Calling /api/market-analysis with $ResumeFile ..." -ForegroundColor Cyan
Write-Host ""

$response = curl.exe -s -X POST http://localhost:5000/api/market-analysis `
    -F "resume=@$ResumeFile" | ConvertFrom-Json

$response | ConvertTo-Json -Depth 10
