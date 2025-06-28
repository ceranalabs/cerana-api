from flask import Blueprint, request, jsonify
from schemas.auth import SignupRequest, SignupResponse, VerifyRequest, VerifyResponse
from services import auth as auth_service
from utils.auth import require_auth

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
    auth_token, user = auth_service.verify(req.token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 404
    resp = VerifyResponse(authToken=auth_token, user=user, userRole=user['role'])
    return jsonify(resp.model_dump()), 200

@bp.route('/auth/me', methods=['GET'])
@require_auth
def me():
    from services import founder_profile as founder_service
    from routes.investor import investors
    from schemas.founder_profile import FounderProfile
    from schemas.investor import InvestorProfile
    founder = founder_service.get_founder_profile(request.user_id)
    if founder:
        return jsonify(FounderProfile(**founder).model_dump(mode="json")), 200
    investor = investors.get(request.user_id)
    if investor:
        return jsonify(InvestorProfile(**investor).model_dump(mode="json")), 200
    return jsonify({'error': 'Profile not found'}), 404

@bp.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    # For MVP, do nothing (stateless JWT)
    return jsonify({'success': True}), 200
