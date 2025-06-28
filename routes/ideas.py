from flask import Blueprint, request, jsonify
from schemas.idea import StartupIdeaInput, StartupIdea
from services import idea as idea_service
from utils.auth import require_auth

bp = Blueprint('ideas', __name__)

@bp.route('/ideas', methods=['POST'])
@require_auth
def submit_idea():
    data = request.get_json()
    req = StartupIdeaInput.model_validate(data)
    idea = idea_service.submit_idea(request.user_id, req.model_dump())
    return jsonify(StartupIdea(**idea).model_dump()), 201

@bp.route('/ideas/<idea_id>', methods=['GET'])
@require_auth
def get_idea(idea_id):
    idea = idea_service.get_idea(idea_id)
    if not idea:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(StartupIdea(**idea).model_dump()), 200

@bp.route('/ideas/<idea_id>', methods=['PUT'])
@require_auth
def update_idea(idea_id):
    data = request.get_json()
    req = StartupIdeaInput.model_validate(data)
    idea = idea_service.update_idea(idea_id, req.model_dump())
    if not idea:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(StartupIdea(**idea).model_dump()), 200
