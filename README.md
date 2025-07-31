# Let's Talk: Offline Voice-Based 2FA API

**Let's Talk** is a secure, offline-first API for voice-based two-factor authentication (2FA). It leverages Flask for the web framework and `pyttsx3` for local text-to-speech, ensuring all authentication and voice delivery happens without internet dependency. This makes it ideal for Ugandan organizations or any environment where privacy, reliability, and local control are critical.

## 🚀 Core Features

- **Voice OTP Delivery:** OTPs are generated and spoken to the user using local TTS (pyttsx3), no cloud or external APIs.
- **Offline-First:** All logic, storage, and analytics are local. No internet required for any authentication or voice flow.
- **Token-Based Security:** Endpoints are protected with secure tokens and OTPs are generated using cryptographically sound methods.
- **Modular Flask Blueprints:** Each API module (like OTP) is a Flask blueprint, making the system easy to extend.
- **Local Analytics:** All logs and analytics are stored as JSON files for compliance and auditability.
- **Comprehensive Testing:** Includes `unittest` and `pytest`-compatible tests, plus integration scripts and batch runners for CI/CD.
- **Security Auditing:** Integrates with `bandit`, `safety`, and `pip-audit` for vulnerability checks.

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/otp/send` | POST | Generate and speak an OTP for a user |
| `/calls/otp/verify` | POST | Verify a submitted OTP |
| `/calls/otp/replay` | POST | Replay the OTP via voice |

### Request Examples

**Send OTP:**
```bash
curl -X POST http://localhost:5000/api/otp/send \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}'
```

**Verify OTP:**
```bash
curl -X POST http://localhost:5000/calls/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser", "otp": "123456"}'
```

**Replay OTP:**
```bash
curl -X POST http://localhost:5000/calls/otp/replay \
  -H "Content-Type: application/json" \
  -d '{"user_id": "testuser"}'
```

## 📁 Project Structure

```
voice-api/
├── app.py                 # Main Flask app, registers all blueprints
├── blueprints/
│   └── otp.py            # OTP API endpoints
├── utils/
│   └── otp_logic.py      # Core OTP generation, storage, and voice logic
├── tests/                # Unit and integration tests
├── run_integration_test.py # Standalone integration test runner
├── run_test.bat          # Batch script for running tests on Windows
├── requirements.txt      # Python dependencies
└── .github/workflows/    # CI/CD automation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10–3.13
- Windows, Linux, or macOS

### 1. Clone the Repository

```bash
git clone https://github.com/muhammadnsererko/lets-talk.git
cd lets-talk
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Server

```bash
python app.py
```

The API will be available at [http://localhost:5000](http://localhost:5000).

### 5. Run Tests

**Using the batch runner (Windows):**
```bash
.\run_test.bat
```

**Using unittest:**
```bash
python -m unittest discover tests
```

**Using pytest:**
```bash
python -m pytest tests/ -v
```

**Integration test script:**
```bash
python run_integration_test.py
```

### 6. Security Checks

**Bandit (security linter):**
```bash
bandit -r .
```

**Safety (dependency vulnerabilities):**
```bash
safety check -r requirements.txt
```

**Pip-audit (package vulnerabilities):**
```bash
pip-audit
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## 🌍 Local Ugandan Analogy

Just like a boda boda rider who knows every shortcut in Kampala and delivers your message even when the network is down, Let's Talk ensures your OTPs are delivered securely and reliably, no matter the connectivity.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email nserekomuhammad20@gmail.com or create an issue in the GitHub repository.

---

**Built with ❤️ in Uganda for the world**