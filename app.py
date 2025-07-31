import os
import logging
from flask import Flask
from config import Config
from blueprints.otp import otp_blueprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(otp_blueprint)

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}, 200

if __name__ == "__main__":
    logger.info(f"Starting Let's Talk API on port {Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
