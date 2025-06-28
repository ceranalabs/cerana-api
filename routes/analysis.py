from flask import Blueprint, request, jsonify
from services import analysis as analysis_service
from utils.auth import require_auth

bp = Blueprint('analysis', __name__)

@bp.route('/analysis', methods=['POST'])
@require_auth
def start_analysis():
    data = request.get_json()
    idea_id = data.get('ideaId')
    if not idea_id:
        return jsonify({'error': 'Missing ideaId'}), 400
    analysis_id, result = analysis_service.start_analysis(idea_id)
    return jsonify({'analysisId': analysis_id, 'status': 'processing', 'estimatedCompletionTime': result['processedAt']}), 202

@bp.route('/analysis/<analysis_id>', methods=['GET'])
@require_auth
def get_analysis(analysis_id):
    result = analysis_service.get_analysis(analysis_id)
    if not result:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(result), 200
