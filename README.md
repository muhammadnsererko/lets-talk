# Voice API

A secure voice communication API with OTP authentication and AWS Polly integration for text-to-speech synthesis.

## Features

- OTP (One-Time Password) authentication for secure access
- Voice synthesis using AWS Polly
- Security and recovery mechanisms
- Backup management
- Tamper detection

## Project Structure

```
voice-api/
├── app.py                  # Main Flask application entry point
├── config.py               # Configuration settings
├── src/
│   └── voice_api/
│       ├── blueprints/     # Flask blueprints
│       │   ├── otp.py      # OTP authentication routes
│       │   └── polly.py    # AWS Polly integration routes
│       ├── plugins/        # Plugin modules
│       │   ├── analytics.py
│       │   ├── backup_manager.py
│       │   └── tamper_detection.py
│       └── utils/          # Utility functions
│           └── security.py  # Security utilities
├── tests/                  # Test suite
│   ├── test_api.py
│   └── test_security_and_recovery.py
├── docs/                   # Documentation
│   └── ENCRYPTION_PROTOCOLS.md
├── .github/workflows/      # CI/CD pipelines
└── scripts/                # Test and utility scripts
```

### Repository Contents Summary

#### 📁 **Core Application**
- `app.py` - Main Flask application
- `config/` - Configuration and requirements
- `blueprints/` - Modular API endpoints
- `utils/` - Utility functions

#### 🧪 **Testing**
- `tests/` - Complete test suite
- `scripts/` - Test and utility scripts

#### 📚 **Documentation**
- `docs/` - Complete documentation
- `README.md` - Project overview

#### 🔧 **Configuration**
- `.github/workflows/` - CI/CD pipelines
- `requirements.txt` - Dependencies
- `config.py` - Application settings

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests to verify your setup:

```bash
python -m unittest discover
```

## Usage

### Configuration

Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

### Running the Server

Start the Flask development server:

```bash
python app.py
```

The server will start on port 5000 by default.

## API Endpoints

### OTP Authentication

- `POST /calls/otp` - Send OTP to a user
- `POST /calls/otp/verify` - Verify OTP
- `POST /calls/otp/replay` - Replay OTP

### AWS Polly Integration

- `POST /api/polly/synthesize` - Synthesize text to speech

## Testing

Run the test suite:

```bash
python -m unittest discover
```

## Security

This project implements several security measures:

- AES-256 encryption for sensitive data
- SHA-256 hashing for file integrity
- Tamper detection for critical files
- Backup and recovery mechanisms
- Key rotation process for Fernet keys
- Emergency revocation protocol

For more details, see [ENCRYPTION_PROTOCOLS.md](docs/ENCRYPTION_PROTOCOLS.md).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE)