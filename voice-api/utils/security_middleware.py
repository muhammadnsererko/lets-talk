"""
Security middleware for API token validation with scope checking
"""

from functools import wraps
from flask import request, jsonify
import hashlib

import os
import json
from .security import decrypt_fernet, encrypt_fernet  # Assuming these are in security.py

TOKEN_STORE_FILE = os.path.join('data', 'api_tokens.json')

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

def load_tokens():
    if not os.path.exists(TOKEN_STORE_FILE):
        return {}
    with open(TOKEN_STORE_FILE, 'r') as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKEN_STORE_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)

def require_token(scopes=None):
    if scopes is None:
        scopes = []
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid authorization header'}), 401
            
            token = auth_header.split(' ')[1]
            tokens = load_tokens()
            
            token_data = None
            for token_id, data in tokens.items():
                if data.get('token_hash') == hash_token(token):
                    token_data = data
                    break
            
            if not token_data or token_data.get('revoked', False):
                return jsonify({'error': 'Invalid or revoked token'}), 401
            
            # Check scopes
            token_scopes = set(token_data.get('scopes', []))
            required_scopes = set(scopes)
            if not required_scopes.issubset(token_scopes):
                return jsonify({'error': 'Insufficient scopes'}), 403
            
            # Update last used
            from datetime import datetime
            token_data['last_used'] = datetime.now().isoformat()
            tokens[token_id] = token_data
            save_tokens(tokens)
            
            request.api_token = token_data
            request.token_id = token_id
            return f(*args, **kwargs)
        return decorated_function
    return decorator