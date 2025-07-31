import logging
from flask import Blueprint, request, jsonify, current_app
from utils.otp_logic import generate_otp, store_otp, speak_otp, get_stored_otp

logger = logging.getLogger(__name__)

otp_blueprint = Blueprint('otp', __name__)

@otp_blueprint.route('/api/otp/send', methods=['POST'])
def send_otp():
    """
    API endpoint to generate, store, and speak an OTP.
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    user_id = data['user_id']

    try:
        # Generate OTP
        otp = generate_otp()

        # Store OTP
        otp_id = store_otp(user_id, otp)

        # Speak OTP
        speak_otp(otp)

        return jsonify({"status": "success", "otp_id": otp_id, "otp": otp})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@otp_blueprint.route('/calls/otp/verify', methods=['POST'])
def verify_otp():
    """
    API endpoint to verify an OTP for a user.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'otp' not in data:
        return jsonify({"status": "error", "message": "user_id and otp are required"}), 400

    user_id = data['user_id']
    otp = data['otp']

    try:
        stored_otp = get_stored_otp(user_id)
        if stored_otp and str(stored_otp) == str(otp):
            return jsonify({"status": "success", "message": "OTP verified successfully"})
        else:
            return jsonify({"status": "error", "message": "Invalid or expired OTP"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@otp_blueprint.route('/calls/otp/replay', methods=['POST'])
def replay_otp():
    """
    API endpoint to replay the last OTP for a user.
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    user_id = data['user_id']

    try:
        stored_otp = get_stored_otp(user_id)
        if stored_otp:
            speak_otp(stored_otp)
            return jsonify({"status": "success", "message": "OTP replayed", "otp": stored_otp})
        else:
            return jsonify({"status": "error", "message": "No OTP found for this user"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500