# PowerShell script to test Let's Talk API endpoints
Write-Host "🎯 Testing Let's Talk API Endpoints" -ForegroundColor Green
Write-Host "=" * 50

# Ensure we're in the right directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Yellow

# Test Health Endpoint
Write-Host "`n🔍 Testing /health endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
    Write-Host "✅ Health endpoint working!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"
} catch {
    Write-Host "❌ Health endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test OTP Generation
Write-Host "`n🔍 Testing /calls/otp endpoint..." -ForegroundColor Cyan
try {
    $body = @{phone_number = "+256700123456"} | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/calls/otp" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ OTP generation working!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"
} catch {
    Write-Host "❌ OTP endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test API Token Creation
Write-Host "`n🔍 Testing /api/tokens endpoint..." -ForegroundColor Cyan
try {
    $body = @{user_id = "test_user"; scopes = @("read", "write")} | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/tokens" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Token creation working!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 10)"
} catch {
    Write-Host "❌ Token endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + "=" * 50 -ForegroundColor Green
Write-Host "🎉 Testing complete!" -ForegroundColor Green