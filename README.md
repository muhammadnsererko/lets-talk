# voice-api

An offline-first, privacy-respecting 2FA OTP API built with Flask and pyttsx3. All functionality is local and does not rely on external APIs.

## Features

- **Offline First**: No internet connection required for core functionality.
- **Privacy-Respecting**: No data leaves your local machine.
- **2FA OTP**: Generate and verify one-time passwords.
- **Voice-based OTP**: Reads out the OTP using text-to-speech.

## Getting Started

### Prerequisites

- Python 3.10–3.13

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/muhammadnsereko/voice-api.git
    cd voice-api
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

```bash
python app.py
```

### Running Tests

```bash
python -m unittest discover
```