from flask import Blueprint, request, jsonify
from schemas.founder_profile import FounderProfileInput, FounderProfile
from services import founder_profile as founder_service
from utils.auth import require_auth
from services.auth import users

bp = Blueprint('founders', __name__)

@bp.route('/founders', methods=['POST'])
@require_auth
def create_or_update_founder():
    data = request.get_json()
    req = FounderProfileInput.model_validate(data)
    profile = founder_service.create_or_update_founder_profile(request.user_id, req.model_dump())
    # Ensure user is present in users dict
    users[request.user_id] = {
        'id': request.user_id,
        'email': req.email,
        'role': 'founder',
        'createdAt': profile['createdAt'],
        'updatedAt': profile['updatedAt']
    }
    return jsonify(FounderProfile(**profile).model_dump(mode="json")), 201

@bp.route('/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    profile = founder_service.get_founder_profile(founder_id)
    if not profile:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(FounderProfile(**profile).model_dump(mode="json")), 200

@bp.route('/founders/<founder_id>', methods=['PUT'])
@require_auth
def update_founder(founder_id):
    data = request.get_json()
    req = FounderProfileInput.model_validate(data)
    profile = founder_service.create_or_update_founder_profile(founder_id, req.model_dump())
    # Ensure user is present in users dict
    users[founder_id] = {
        'id': founder_id,
        'email': req.email,
        'role': 'founder',
        'createdAt': profile['createdAt'],
        'updatedAt': profile['updatedAt']
    }
    return jsonify(FounderProfile(**profile).model_dump(mode="json")), 200
