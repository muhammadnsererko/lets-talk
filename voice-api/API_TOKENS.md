# Let's Talk API - Token Authentication Guide

## Overview

The Let's Talk API now supports secure API access tokens for programmatic access. This allows developers to integrate the voice-authentication system into their applications without manual OTP verification.

## Quick Start

### 1. Get Your API Token

#### Via Dashboard (Recommended for Developers)
1. Start the server: `python app.py`
2. Visit: http://localhost:5000/api/tokens/dashboard
3. Login with dashboard password (set `DASHBOARD_PASSWORD` in .env)
4. Click "Create New Token" and copy your token

#### Via API (Programmatic)
```bash
curl -X POST http://localhost:5000/api/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "my_app",
    "scopes": ["read", "write"]
  }'
```

Response:
```json
{
  "token_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "abc123def456...",
  "created_at": "2024-01-15T10:30:00",
  "scopes": ["read", "write"]
}
```

### 2. Use Your Token

Include your token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer abc123def456..." \
  http://localhost:5000/calls/otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "+256700123456"}'
```

## API Token Endpoints

### POST /api/tokens
Generate a new API token.

**Request:**
```json
{
  "user_id": "string",           // Optional, defaults to "default_user"
  "scopes": ["read", "write"]    // Optional, defaults to ["read", "write"]
}
```

**Response:**
```json
{
  "token_id": "uuid",
  "token": "secure_token_string",
  "created_at": "ISO8601_timestamp",
  "scopes": ["scopes_list"]
}
```

### GET /api/tokens
List all tokens for a user.

**Query Parameters:**
- `user_id`: Filter by user ID (optional)

**Response:**
```json
{
  "tokens": [
    {
      "token_id": "uuid",
      "created_at": "ISO8601_timestamp",
      "last_used": "ISO8601_timestamp",
      "scopes": ["scopes_list"]
    }
  ]
}
```

### DELETE /api/tokens/{token_id}
Revoke a specific token.

**Response:**
```json
{
  "message": "Token revoked successfully"
}
```

## Protected OTP Endpoints

All existing OTP endpoints now support token authentication:

### POST /calls/otp
Send OTP to a phone number (requires token).

**Headers:**
```
Authorization: Bearer your_token_here
```

**Request:**
```json
{
  "phone": "+256700123456",
  "message": "Optional custom message"
}
```

### POST /calls/verify
Verify OTP code (requires token).

**Headers:**
```
Authorization: Bearer your_token_here
```

**Request:**
```json
{
  "phone": "+256700123456",
  "code": "123456"
}
```

### POST /calls/replay
Replay last OTP (requires token).

**Headers:**
```
Authorization: Bearer your_token_here
```

**Request:**
```json
{
  "phone": "+256700123456"
}
```

## Web Dashboard

The API includes a web-based dashboard for easy token management:

- **URL:** http://localhost:5000/api/tokens/dashboard
- **Login:** Use dashboard password (set via `DASHBOARD_PASSWORD` environment variable)
- **Features:**
  - Create new tokens
  - View all active tokens
  - See token usage statistics
  - Revoke tokens instantly

## Environment Configuration

Add these to your `.env` file:

```bash
# Dashboard access
DASHBOARD_PASSWORD=your_secure_password_here

# Security
SECRET_KEY=your_secret_key_for_sessions

# Server settings
FLASK_ENV=production    # Use production mode with waitress
PORT=5000               # Server port
```

## Production Deployment

### Using Waitress (Recommended)
```bash
# Install waitress
pip install waitress

# Set production mode
export FLASK_ENV=production

# Start server
python app.py
```

### Using Flask Development Server
```bash
# Development mode
export FLASK_ENV=development
python app.py
```

## Security Features

- **Encrypted Storage:** All tokens are encrypted using Fernet symmetric encryption
- **Token Hashing:** Tokens are hashed before storage (never stored in plain text)
- **Revocation:** Tokens can be instantly revoked via API or dashboard
- **Usage Tracking:** Last used timestamp is updated on every request
- **Scope-based Access:** Tokens can be limited to specific scopes
- **Rate Limiting:** Built-in rate limiting per token (configurable)

## Error Handling

### Invalid Token
```json
{
  "error": "Invalid or revoked token"
}
```

### Missing Authorization Header
```json
{
  "error": "Missing or invalid authorization header"
}
```

## Examples

### Python Integration
```python
import requests

# Create token
response = requests.post('http://localhost:5000/api/tokens', json={
    'user_id': 'my_app',
    'scopes': ['read', 'write']
})
token = response.json()['token']

# Use token
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:5000/calls/otp', 
                        headers=headers,
                        json={'phone': '+256700123456'})
```

### JavaScript Integration
```javascript
// Create token
const createToken = async () => {
  const response = await fetch('http://localhost:5000/api/tokens', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 'my_app', scopes: ['read', 'write'] })
  });
  const data = await response.json();
  return data.token;
};

// Use token
const sendOTP = async (phone, token) => {
  const response = await fetch('http://localhost:5000/calls/otp', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ phone })
  });
  return response.json();
};
```

## Token Lifecycle

1. **Creation:** Token is generated and returned (shown once)
2. **Usage:** Token is validated on each request
3. **Tracking:** Last used timestamp is updated automatically
4. **Revocation:** Token can be revoked via API or dashboard
5. **Cleanup:** Revoked tokens remain in storage but are marked as inactive

## Best Practices

- **Store tokens securely** - Never commit tokens to version control
- **Use environment variables** - Store tokens in environment variables or secure vaults
- **Rotate tokens regularly** - Create new tokens and revoke old ones periodically
- **Monitor usage** - Check the dashboard for unusual activity
- **Use specific scopes** - Limit token scopes to minimum required permissions
- **Implement token refresh** - Plan for token rotation in your application