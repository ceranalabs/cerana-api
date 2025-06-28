from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.investor import InvestorProfileInput, InvestorProfile
import uuid
from datetime import datetime
from services.auth import users

bp = Blueprint('investor', __name__)

# In-memory store for MVP
investors = {}

@bp.route('/investors', methods=['POST'])
@require_auth
def create_update_investor():
    data = request.get_json()
    req = InvestorProfileInput.model_validate(data)
    investor_id = request.user_id or str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    investor = investors.get(investor_id, {})
    investor.update(req.model_dump())
    investor['email'] = req.email
    investor['id'] = investor_id
    investor['createdAt'] = investor.get('createdAt', now)
    investor['updatedAt'] = now
    investors[investor_id] = investor
    # Ensure user is present in users dict
    users[investor_id] = {
        'id': investor_id,
        'email': req.email,
        'role': 'investor',
        'createdAt': investor['createdAt'],
        'updatedAt': investor['updatedAt']
    }
    return jsonify(InvestorProfile(**investor).model_dump(mode="json")), 201

@bp.route('/investors/<investor_id>', methods=['GET'])
@require_auth
def get_investor_profile(investor_id):
    investor = investors.get(investor_id)
    if not investor:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(InvestorProfile(**investor).model_dump(mode="json")), 200

@bp.route('/investors/<investor_id>', methods=['PUT'])
@require_auth
def update_investor_profile(investor_id):
    data = request.get_json()
    req = InvestorProfileInput.model_validate(data)
    investor = investors.get(investor_id)
    now = datetime.utcnow().isoformat()
    if not investor:
        # Create new investor if not found
        investor = req.model_dump()
        investor['id'] = investor_id
        investor['createdAt'] = now
    else:
        investor.update(req.model_dump())
    investor['email'] = req.email
    investor['updatedAt'] = now
    investors[investor_id] = investor
    # Ensure user is present in users dict
    users[investor_id] = {
        'id': investor_id,
        'email': req.email,
        'role': 'investor',
        'createdAt': investor.get('createdAt', now),
        'updatedAt': investor['updatedAt']
    }
    return jsonify(InvestorProfile(**investor).model_dump(mode="json")), 200
