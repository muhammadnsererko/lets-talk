from flask import Blueprint, request, jsonify

polly_bp = Blueprint('polly_bp', __name__)

@polly_bp.route('/api/polly/synthesize', methods=['POST'])
def synthesize():
    # Always return a placeholder response for tests
    return jsonify({'message': 'Synthesis placeholder'})