from flask import Blueprint, jsonify

polly_bp = Blueprint('polly', __name__, url_prefix='/api/polly')

@polly_bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    return jsonify({'status': 'success', 'message': 'Synthesis placeholder'}), 200