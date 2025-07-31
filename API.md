# Let's Talk API Documentation

## Overview

Let's Talk is an offline voice-based 2FA API that generates and verifies one-time passwords (OTPs) with voice output capabilities.

## Base URL

For local development: `http://localhost:5000`

## Authentication

This API does not require authentication for basic usage. All endpoints are publicly accessible.

## Rate Limiting

Rate limiting is not implemented in the current version. Consider implementing rate limiting for production use.

## Endpoints

### 1. Send OTP

Generate and send an OTP to a user via voice.

**Endpoint:** `POST /send-otp`

**Request Body:**
```json
{
  "user_id": "user123",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "user_id": "user123"
}
```

**Error Response:**
```json
{
  "error": "User ID and phone number are required"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/send-otp \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "phone": "+1234567890"}'
```

### 2. Verify OTP

Verify an OTP provided by a user.

**Endpoint:** `POST /verify-otp`

**Request Body:**
```json
{
  "user_id": "user123",
  "otp": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Invalid or expired OTP"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "otp": "123456"}'
```

### 3. Replay OTP

Replay the last OTP for a user via voice.

**Endpoint:** `POST /replay-otp`

**Request Body:**
```json
{
  "user_id": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP replayed successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "No active OTP found for this user"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/replay-otp \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

### 4. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/health
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=false
PORT=5000

# Security Settings
OTP_EXPIRY_MINUTES=5
MAX_OTP_ATTEMPTS=3

# Voice Settings
DEFAULT_VOICE_RATE=150
DEFAULT_VOICE_VOLUME=0.9
DEFAULT_VOICE_GENDER=female

# Storage Settings
OTP_STORE_FILE=otp_store.json
ANALYTICS_FILE=analytics_data.json
USER_SETTINGS_FILE=user_settings.json

# Development
READ_ONLY=false
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Request succeeded
- `400 Bad Request`: Invalid request format or missing parameters
- `500 Internal Server Error`: Server-side error

All error responses include a JSON object with an `error` field describing the issue.

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=html
```

### Manual Testing

Use the provided cURL examples above or test with tools like Postman or Thunder Client.

## Security Considerations

1. **HTTPS**: Use HTTPS in production
2. **Rate Limiting**: Implement rate limiting to prevent brute force attacks
3. **Input Validation**: All inputs are validated on the server
4. **OTP Expiry**: OTPs expire after configurable time (default: 5 minutes)
5. **Storage**: OTPs are stored securely with SHA-256 hashing

## Troubleshooting

### Common Issues

1. **TTS Not Working**: Ensure pyttsx3 and system TTS dependencies are installed
2. **Port Already in Use**: Change the PORT in .env file
3. **Permission Errors**: Ensure proper file permissions for JSON storage files

### Debug Mode

Enable debug mode in .env:
```bash
DEBUG=true
```

This will provide more detailed error messages in responses.

## Support

For issues and questions, please check:
1. The troubleshooting section above
2. Run the test suite to verify setup
3. Check application logs for detailed error information