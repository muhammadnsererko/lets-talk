# API Token Generation Guide

Your voice API now has the ability to generate and manage API tokens for secure authentication.

## Available Endpoints

### 1. Create API Token
**Endpoint:** `POST /api/tokens`

**Request:**
```json
{
  "name": "my-app-token"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "name": "my-app-token",
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Validate API Token
**Endpoint:** `POST /api/tokens/validate`

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "valid": true,
  "name": "my-app-token",
  "created_at": "2024-01-15T10:30:00",
  "last_used": "2024-01-15T14:45:00",
  "usage_count": 5
}
```

### 3. List All Tokens
**Endpoint:** `GET /api/tokens`

**Headers:**
```
Authorization: Bearer <your-api-token>
```

**Response:**
```json
{
  "tokens": [
    {
      "name": "my-app-token",
      "created_at": "2024-01-15T10:30:00",
      "last_used": "2024-01-15T14:45:00",
      "usage_count": 5
    }
  ]
}
```

## Usage Examples

### Using curl:
```bash
# Create a new token
curl -X POST http://localhost:5000/api/tokens \
  -H "Content-Type: application/json" \
  -d '{"name": "my-mobile-app"}'

# Validate a token
curl -X POST http://localhost:5000/api/tokens/validate \
  -H "Content-Type: application/json" \
  -d '{"token": "your-token-here"}'

# List all tokens (requires authentication)
curl -X GET http://localhost:5000/api/tokens \
  -H "Authorization: Bearer your-token-here"
```

### Using Python:
```python
import requests

# Create a token
response = requests.post('http://localhost:5000/api/tokens', 
                        json={'name': 'my-app'})
token = response.json()['token']

# Use the token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/tokens', 
                       headers=headers)
```

## Security Features

- **Secure Token Generation:** Uses cryptographically secure random tokens
- **Token Hashing:** Tokens are stored as SHA-256 hashes, never in plain text
- **Usage Tracking:** Each token tracks creation time, last used time, and usage count
- **Bearer Authentication:** Uses standard Bearer token authentication
- **File-based Storage:** Tokens are stored in `data/api_tokens.json` for persistence

## Testing

Run the API token test suite:
```bash
python test_api_tokens.py
```

This will test:
- ✅ Token creation
- ✅ Token validation
- ✅ Token listing
- ✅ Invalid token handling
- ✅ Health check integration

Your API is now fully equipped with secure API token generation capabilities!