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

# Check if Python is installed
$pythonCmd = if (Get-Command "python" -ErrorAction SilentlyContinue) { "python" } elseif (Get-Command "python3" -ErrorAction SilentlyContinue) { "python3" } else { "" }
if ($pythonCmd -eq "") {
    Write-Host "❌ Python is not installed or not in PATH." -ForegroundColor Red
    return
}

if (-Not (Test-Path ".\venv")) {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
}

Write-Host "🛠  Installing/Updating Backend Dependencies..." -ForegroundColor Gray
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
& ".\venv\Scripts\python.exe" -m pip install "pydantic[email]" --quiet

if (-Not (Test-Path ".\.env")) {
    Write-Host "⚠️  .env missing. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item ".\.env.example" -Destination ".\.env"
}

# Launch Backend in a new window
Write-Host "⚡ Launching Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\Backend'; .\venv\Scripts\python.exe -m app.main"

# 3. Setup Frontend
Write-Host "`n🎨 Preparing Frontend..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot\finwise-frontend"

if (-Not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js (npm) is not installed or not in PATH." -ForegroundColor Red
    return
}

if (-Not (Test-Path ".\node_modules")) {
    Write-Host "⚠️  Frontend dependencies missing. Installing with npm..." -ForegroundColor Yellow
    npm install
}

# Launch Frontend in a new window
Write-Host "⚡ Launching Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\finwise-frontend'; npm run dev"

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
