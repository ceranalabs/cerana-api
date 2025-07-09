from flask import Blueprint, request, jsonify
from schemas.auth import SignupRequest, SignupResponse, VerifyRequest, VerifyResponse
from schemas import founder_profile_to_dict, investor_profile_to_dict
from services import auth as auth_service
from utils.auth import require_auth
from models import FounderProfile, InvestorProfile

bp = Blueprint('auth', __name__)

@bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    req = SignupRequest.model_validate(data)
    user_id, token = auth_service.signup(req.email, req.role)
    resp = SignupResponse(userId=user_id, verificationSent=True, message='Verification email sent (simulated)')
    return jsonify(resp.model_dump()), 201

@bp.route('/auth/verify', methods=['POST'])
def verify():
    data = request.get_json()
    req = VerifyRequest.model_validate(data)
    user_id, token = auth_service.verify(req.token)
    resp = VerifyResponse(userId=user_id, token=token, message='Verification successful')
    return jsonify(resp.model_dump()), 200

@bp.route('/auth/me', methods=['GET'])
@require_auth
def me():
    founder = FounderProfile.query.get(request.user_id)
    if founder:
        return jsonify(founder_profile_to_dict(founder)), 200

    investor = InvestorProfile.query.get(request.user_id)
    if investor:
        return jsonify(investor_profile_to_dict(investor)), 200

    return jsonify({'error': 'Profile not found'}), 404

@bp.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    # For MVP, do nothing (stateless JWT)
    return jsonify({'success': True}), 200
