from flask import Flask
from routes.otp_route import otp_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(otp_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)