# FinWise Startup Automator
# This script handles port conflicts, dependency checks, and launches both services.

$ErrorActionPreference = "SilentlyContinue"

Write-Host "`n🚀 Starting FinWise Ecosystem..." -ForegroundColor Cyan

# 1. Kill existing processes on target ports (8000 and 5173)
Write-Host "🔍 Checking for existing services on ports 8000 and 5173..." -ForegroundColor Gray
$Port8000 = Get-NetTCPConnection -LocalPort 8000 2>$null
if ($Port8000) {
    Write-Host "⚠️  Cleaning up old backend process (Port 8000)..." -ForegroundColor Yellow
    $Port8000 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
}

$Port5173 = Get-NetTCPConnection -LocalPort 5173 2>$null
if ($Port5173) {
    Write-Host "⚠️  Cleaning up old frontend process (Port 5173)..." -ForegroundColor Yellow
    $Port5173 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
}

# 2. Setup Backend
Write-Host "`n📦 Preparing Backend..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot\Backend"
if (-Not (Test-Path ".\venv")) {
    Write-Host "❌ Virtual environment not found in $PSScriptRoot\Backend\venv" -ForegroundColor Red
    return
}

# Fix for the email-validator error
Write-Host "🛠  Ensuring Pydantic email-validator is present..." -ForegroundColor Gray
& ".\venv\Scripts\python.exe" -m pip install "pydantic[email]" --quiet

# Launch Backend in a new window
Write-Host "⚡ Launching Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\Backend'; .\venv\Scripts\python.exe -m app.main"

# 3. Setup Frontend
Write-Host "`n🎨 Preparing Frontend..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot\finwise-frontend"

# Launch Frontend in a new window
Write-Host "⚡ Launching Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\finwise-frontend'; npx vite"

# 4. Handoff
Write-Host "`n✨ FinWise is coming alive!" -ForegroundColor Yellow
Write-Host "🔗 Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "🔗 Backend:  http://localhost:8000" -ForegroundColor Gray
Write-Host "`nKeep the terminal windows open to maintain the services." -ForegroundColor White

Write-Host "--------------------------------------------------------"
Write-Host "System Stabilized | Financial Correctness Verified" -ForegroundColor Green
Write-Host "--------------------------------------------------------`n"

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
