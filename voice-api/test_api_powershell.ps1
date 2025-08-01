# PowerShell script to test Voice API endpoints

Write-Host "Testing Voice API Endpoints..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

$baseUrl = "http://localhost:5000"

# Test Health Check
Write-Host "`n1. Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
    Write-Host "✅ Health Check: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test OTP Generation
Write-Host "`n2. Testing OTP Generation..." -ForegroundColor Yellow
$otpBody = @{
    phone_number = "+1234567890"
    message = "Your verification code is"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/calls/otp" -Method Post -Body $otpBody -ContentType "application/json"
    Write-Host "✅ OTP Generation: Success" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)"
} catch {
    Write-Host "❌ OTP Generation Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test API Token Creation
Write-Host "`n3. Testing API Token Creation..." -ForegroundColor Yellow
$tokenBody = @{
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/tokens" -Method Post -Body $tokenBody -ContentType "application/json"
    Write-Host "✅ Token Creation: Success" -ForegroundColor Green
    Write-Host "Token: $($response.token)"
    
    # Test Protected Endpoint
    Write-Host "`n4. Testing Protected Endpoint..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Bearer $($response.token)"
    }
    
    try {
        $protectedResponse = Invoke-RestMethod -Uri "$baseUrl/api/protected" -Method Get -Headers $headers
        Write-Host "✅ Protected Endpoint: $($protectedResponse.message)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Protected Endpoint Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Token Creation Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Dashboard
Write-Host "`n5. Testing Dashboard Access..." -ForegroundColor Yellow
$dashboardBody = @{
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/tokens/dashboard" -Method Post -Body $dashboardBody -ContentType "application/json"
    Write-Host "✅ Dashboard: Accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Dashboard Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Green
Write-Host "API Testing Complete!" -ForegroundColor Green