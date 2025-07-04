import os
from flask import Flask
from config import Config
from src.voice_api.blueprints.otp import otp_bp
from src.voice_api.blueprints.polly import polly_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(otp_bp)
app.register_blueprint(polly_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
