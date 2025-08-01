"""
Let's Talk API - Main Application
Production-ready Flask app with API token support and web dashboard
"""
import os
import sys
from flask import Flask, request, jsonify
from blueprints.api_tokens import api_tokens_bp, validate_api_token
from blueprints.otp import otp_bp
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Register blueprints
app.register_blueprint(otp_bp)
app.register_blueprint(api_tokens_bp)

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': logging.Formatter().formatTime(logging.LogRecord(
            name='health', level=logging.INFO, pathname='', lineno=0,
            msg='', args=(), exc_info=None
        ))
    })

# Protected routes with token validation
@app.route('/api/protected')
@validate_api_token
def protected_route():
    """Example protected route requiring API token"""
    return jsonify({
        'message': 'This is a protected route',
        'user': request.api_token['user_id'],
        'scopes': request.api_token['scopes']
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check for production mode
    is_production = os.getenv('FLASK_ENV') == 'production'
    port = int(os.getenv('PORT', 5000))
    
    if is_production:
        try:
            from waitress import serve
            logging.info(f"Starting production server on port {port}")
            serve(app, host='0.0.0.0', port=port)
        except ImportError:
            logging.warning("waitress not installed, falling back to Flask dev server")
            app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logging.info(f"Starting development server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)