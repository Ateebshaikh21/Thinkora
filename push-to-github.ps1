# Thinkora - Push to GitHub Script
# Run this in PowerShell to push your changes

Write-Host "🚀 Pushing Thinkora to GitHub..." -ForegroundColor Cyan
Write-Host ""

# Check if git is available
$gitPath = "C:\Program Files\Git\cmd\git.exe"
if (-not (Test-Path $gitPath)) {
    Write-Host "❌ Git not found at $gitPath" -ForegroundColor Red
    Write-Host "Please install Git or use GitHub Desktop" -ForegroundColor Yellow
    exit 1
}

# Show current status
Write-Host "📊 Current status:" -ForegroundColor Yellow
& $gitPath status --short

Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Cyan

# Push to GitHub
& $gitPath push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Render will auto-deploy backend (or click 'Manual Deploy')" -ForegroundColor White
    Write-Host "  2. Vercel will auto-deploy frontend" -ForegroundColor White
    Write-Host "  3. Wait 5 minutes for deployment" -ForegroundColor White
    Write-Host "  4. Test your live app!" -ForegroundColor White
    Write-Host ""
    Write-Host "📍 Check deployment status:" -ForegroundColor Cyan
    Write-Host "  Render: https://dashboard.render.com" -ForegroundColor White
    Write-Host "  Vercel: https://vercel.com/dashboard" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Common solutions:" -ForegroundColor Yellow
    Write-Host "  1. Make sure you're signed in to GitHub" -ForegroundColor White
    Write-Host "  2. Use GitHub Desktop (easier)" -ForegroundColor White
    Write-Host "  3. Check PUSH_MANUALLY.txt for help" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"
