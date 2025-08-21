import os
import logging
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from config import Config
from blueprints.otp import otp_blueprint
from blueprints.api_tokens import api_tokens_bp

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
app.register_blueprint(otp_blueprint, url_prefix='')
app.register_blueprint(api_tokens_bp, url_prefix='')

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}, 200

if __name__ == "__main__":
    logger.info(f"Starting Let's Talk API on port {Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
