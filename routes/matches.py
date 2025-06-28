from flask import Blueprint, request, jsonify
from services import match as match_service
from utils.auth import require_auth

bp = Blueprint('matches', __name__)

@bp.route('/matches', methods=['GET'])
@require_auth
def get_matches():
    match_type = request.args.get('type')
    min_score = request.args.get('minScore', type=int)
    limit = request.args.get('limit', default=20, type=int)
    offset = request.args.get('offset', default=0, type=int)
    result = match_service.get_matches(match_type, min_score, limit, offset)
    return jsonify(result), 200

@bp.route('/matches/<match_id>', methods=['GET'])
@require_auth
def get_match(match_id):
    match = match_service.get_match(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(match), 200
