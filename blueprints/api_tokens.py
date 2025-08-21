import secrets
import hashlib
import json
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from functools import wraps

api_tokens_bp = Blueprint('api_tokens', __name__)

# Simple file-based storage for API tokens
TOKENS_FILE = 'data/api_tokens.json'

def ensure_tokens_file():
    """Ensure the tokens file exists"""
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'w') as f:
            json.dump({}, f)

def hash_token(token):
    """Hash a token using SHA-256"""
    return hashlib.sha256(token.encode()).hexdigest()

def generate_token():
    """Generate a secure API token"""
    return secrets.token_urlsafe(32)

def store_token(name, token):
    """Store a token with its hash"""
    ensure_tokens_file()
    
    with open(TOKENS_FILE, 'r') as f:
        tokens = json.load(f)
    
    token_hash = hash_token(token)
    tokens[token_hash] = {
        'name': name,
        'created_at': datetime.utcnow().isoformat(),
        'last_used': None,
        'usage_count': 0
    }
    
    with open(TOKENS_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    return token_hash

def validate_token(token):
    """Validate a token exists and return its info"""
    ensure_tokens_file()
    
    with open(TOKENS_FILE, 'r') as f:
        tokens = json.load(f)
    
    token_hash = hash_token(token)
    return tokens.get(token_hash)

def update_token_usage(token_hash):
    """Update token usage statistics"""
    ensure_tokens_file()
    
    with open(TOKENS_FILE, 'r') as f:
        tokens = json.load(f)
    
    if token_hash in tokens:
        tokens[token_hash]['last_used'] = datetime.utcnow().isoformat()
        tokens[token_hash]['usage_count'] += 1
        
        with open(TOKENS_FILE, 'w') as f:
            json.dump(tokens, f, indent=2)

def get_all_tokens():
    """Get all tokens (without the actual token values)"""
    ensure_tokens_file()
    
    with open(TOKENS_FILE, 'r') as f:
        tokens = json.load(f)
    
    # Return token info without the actual hashes
    result = []
    for token_hash, info in tokens.items():
        result.append({
            'name': info['name'],
            'created_at': info['created_at'],
            'last_used': info['last_used'],
            'usage_count': info['usage_count']
        })
    
    return result

def require_token(f):
    """Decorator to require valid API token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                scheme, token = auth_header.split(' ', 1)
                if scheme.lower() != 'bearer':
                    return jsonify({'error': 'Invalid authorization scheme'}), 401
            except ValueError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'API token required'}), 401
        
        token_info = validate_token(token)
        if not token_info:
            return jsonify({'error': 'Invalid API token'}), 401
        
        # Update usage statistics
        update_token_usage(hash_token(token))
        
        return f(*args, **kwargs)
    
    return decorated_function

@api_tokens_bp.route('/api/tokens', methods=['POST'])
def create_token():
    """Create a new API token"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Token name is required'}), 400
    
    name = data['name']
    if not name.strip():
        return jsonify({'error': 'Token name cannot be empty'}), 400
    
    token = generate_token()
    token_hash = store_token(name, token)
    
    return jsonify({
        'token': token,
        'name': name,
        'created_at': datetime.utcnow().isoformat()
    }), 201

@api_tokens_bp.route('/api/tokens', methods=['GET'])
@require_token
def list_tokens():
    """List all API tokens (requires authentication)"""
    tokens = get_all_tokens()
    return jsonify({'tokens': tokens})

@api_tokens_bp.route('/api/tokens/validate', methods=['POST'])
def validate_token_endpoint():
    """Validate an API token"""
    data = request.get_json()
    if not data or 'token' not in data:
        return jsonify({'error': 'Token is required'}), 400
    
    token = data['token']
    token_info = validate_token(token)
    
    if token_info:
        return jsonify({
            'valid': True,
            'name': token_info['name'],
            'created_at': token_info['created_at'],
            'last_used': token_info['last_used'],
            'usage_count': token_info['usage_count']
        })
    else:
        return jsonify({'valid': False}), 404