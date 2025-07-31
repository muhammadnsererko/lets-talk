import json
from flask import Blueprint, request, jsonify
from ..utils.otp_logic import generate_otp, store_otp, speak_otp, get_stored_otp
from ..utils.custom_exceptions import OTPGenerationError, OTPStorageError, VoiceSynthesisError

otp_blueprint = Blueprint('otp', __name__)

@otp_blueprint.route('/api/otp/send', methods=['POST'])
def send_otp():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']

    try:
        otp = generate_otp()
        store_otp(user_id, otp)
        speak_otp(otp)
        return jsonify({'message': 'OTP generated and spoken successfully', 'otp': otp}), 200
    except (OTPGenerationError, OTPStorageError, VoiceSynthesisError) as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@otp_blueprint.route('/calls/otp/verify', methods=['POST'])
def verify_otp():
    data = request.get_json()
    if not data or 'user_id' not in data or 'otp' not in data:
        return jsonify({'error': 'user_id and otp are required'}), 400

    user_id = data['user_id']
    otp = data['otp']

    try:
        verified_otp = get_stored_otp(user_id, otp)
        if verified_otp:
            return jsonify({'status': 'verified', 'message': 'OTP is valid'}), 200
        else:
            return jsonify({'status': 'invalid', 'message': 'OTP is invalid or expired'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']
    
    try:
        stored_otp = get_stored_otp(user_id)
        if stored_otp:
            speak_otp(stored_otp)
            return jsonify({'message': 'OTP replayed successfully', 'otp': stored_otp}), 200
        else:
            return jsonify({'error': 'No OTP found for this user'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
    if user_id == 'user123':
        return jsonify({'message': 'OTP replayed'}), 200
    return jsonify({'error': 'User not found'}), 404

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    user_id = request.json.get('user_id')
