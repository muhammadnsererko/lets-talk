"""
API Token Management Blueprint
Handles secure API access token generation, listing, and revocation
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, session
from utils.security import generate_secure_token, encrypt_fernet, decrypt_fernet, generate_fernet_key

api_tokens_bp = Blueprint('api_tokens', __name__, url_prefix='/api/tokens')

# Token storage configuration
TOKEN_STORE_FILE = os.path.join('data', 'api_tokens.json.enc')
DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'letstalk123')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def get_fernet_key():
    """Get or create Fernet encryption key"""
    key_file = os.path.join('data', '.fernet_key')
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = generate_fernet_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

def load_tokens():
    """Load encrypted tokens from storage"""
    if not os.path.exists(TOKEN_STORE_FILE):
        return {}
    
    try:
        key = get_fernet_key()
        with open(TOKEN_STORE_FILE, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = decrypt_fernet(encrypted_data, key)
        return json.loads(decrypted_data.decode('utf-8'))
    except Exception:
        return {}

def save_tokens(tokens):
    """Save tokens to encrypted storage"""
    key = get_fernet_key()
    data = json.dumps(tokens, indent=2).encode('utf-8')
    encrypted_data = encrypt_fernet(data, key)
    
    with open(TOKEN_STORE_FILE, 'wb') as f:
        f.write(encrypted_data)

def validate_api_token(f):
    """Decorator to validate API tokens"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        tokens = load_tokens()
        
        # Find token by value (hashed for security)
        token_hash = hash_token(token)
        token_data = None
        
        for token_id, data in tokens.items():
            if data.get('token_hash') == token_hash:
                token_data = data
                break
        
        if not token_data or token_data.get('revoked', False):
            return jsonify({'error': 'Invalid or revoked token'}), 401
        
        # Update last used time
        token_data['last_used'] = datetime.now().isoformat()
        tokens[token_id] = token_data
        save_tokens(tokens)
        
        # Add token info to request context
        request.api_token = token_data
        request.token_id = token_id
        
        return f(*args, **kwargs)
    
    return decorated_function

def hash_token(token):
    """Hash token for secure storage"""
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()

# API Routes
@api_tokens_bp.route('', methods=['POST'])
def create_token():
    """Generate a new API token"""
    data = request.get_json() or {}
    user_id = data.get('user_id', 'default_user')
    scopes = data.get('scopes', ['read', 'write'])
    
    # Generate secure token
    token = generate_secure_token(32)
    token_id = str(uuid.uuid4())
    
    # Store token metadata
    tokens = load_tokens()
    tokens[token_id] = {
        'token_hash': hash_token(token),
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'last_used': None,
        'revoked': False,
        'scopes': scopes
    }
    save_tokens(tokens)
    
    return jsonify({
        'token_id': token_id,
        'token': token,
        'created_at': tokens[token_id]['created_at'],
        'scopes': scopes
    }), 201

@api_tokens_bp.route('', methods=['GET'])
def list_tokens():
    """List all tokens for a user"""
    user_id = request.args.get('user_id', 'default_user')
    tokens = load_tokens()
    
    user_tokens = []
    for token_id, data in tokens.items():
        if data['user_id'] == user_id and not data.get('revoked', False):
            user_tokens.append({
                'token_id': token_id,
                'created_at': data['created_at'],
                'last_used': data['last_used'],
                'scopes': data['scopes']
            })
    
    return jsonify({'tokens': user_tokens}), 200

@api_tokens_bp.route('/<token_id>', methods=['DELETE'])
def revoke_token(token_id):
    """Revoke a specific token"""
    tokens = load_tokens()
    
    if token_id not in tokens:
        return jsonify({'error': 'Token not found'}), 404
    
    tokens[token_id]['revoked'] = True
    tokens[token_id]['revoked_at'] = datetime.now().isoformat()
    save_tokens(tokens)
    
    return jsonify({'message': 'Token revoked successfully'}), 200

# Dashboard Routes
@api_tokens_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard_login():
    """Simple dashboard login"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == DASHBOARD_PASSWORD:
            session['dashboard_authenticated'] = True
            return redirect(url_for('api_tokens.dashboard'))
        else:
            return render_template('dashboard_login.html', error='Invalid password')
    
    return render_template('dashboard_login.html')

@api_tokens_bp.route('/dashboard/tokens')
def dashboard():
    """Web dashboard for token management"""
    if not session.get('dashboard_authenticated'):
        return redirect(url_for('api_tokens.dashboard_login'))
    
    tokens = load_tokens()
    token_list = []
    
    for token_id, data in tokens.items():
        if not data.get('revoked', False):
            token_list.append({
                'id': token_id,
                'user_id': data['user_id'],
                'created_at': data['created_at'],
                'last_used': data['last_used'],
                'scopes': ', '.join(data['scopes'])
            })
    
    return render_template('dashboard.html', tokens=token_list)

@api_tokens_bp.route('/dashboard/tokens/create', methods=['POST'])
def dashboard_create_token():
    """Create token via dashboard"""
    if not session.get('dashboard_authenticated'):
        return redirect(url_for('api_tokens.dashboard_login'))
    
    user_id = request.form.get('user_id', 'dashboard_user')
    scopes = request.form.get('scopes', 'read,write').split(',')
    scopes = [s.strip() for s in scopes]
    
    # Generate token
    token = generate_secure_token(32)
    token_id = str(uuid.uuid4())
    
    tokens = load_tokens()
    tokens[token_id] = {
        'token_hash': hash_token(token),
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'last_used': None,
        'revoked': False,
        'scopes': scopes
    }
    save_tokens(tokens)
    
    return render_template('token_created.html', token=token, token_id=token_id)

@api_tokens_bp.route('/dashboard/tokens/<token_id>/revoke', methods=['POST'])
def dashboard_revoke_token(token_id):
    """Revoke token via dashboard"""
    if not session.get('dashboard_authenticated'):
        return redirect(url_for('api_tokens.dashboard_login'))
    
    tokens = load_tokens()
    if token_id in tokens:
        tokens[token_id]['revoked'] = True
        tokens[token_id]['revoked_at'] = datetime.now().isoformat()
        save_tokens(tokens)
    
    return redirect(url_for('api_tokens.dashboard'))

@api_tokens_bp.route('/dashboard/logout')
def dashboard_logout():
    """Logout from dashboard"""
    session.pop('dashboard_authenticated', None)
    return redirect(url_for('api_tokens.dashboard_login'))