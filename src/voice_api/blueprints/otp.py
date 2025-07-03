from flask import Blueprint, request, jsonify

otp_bp = Blueprint('otp_bp', __name__)

@otp_bp.route('/calls/otp', methods=['POST'])
def send_otp():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    # For test, always return a fixed OTP
    return jsonify({'otp': '123456'})

@otp_bp.route('/calls/otp/verify', methods=['POST'])
def verify_otp():
    return jsonify({'status': 'verified'})

@otp_bp.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404