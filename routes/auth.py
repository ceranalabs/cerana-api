from flask import Blueprint, request, jsonify
from schemas.auth import SignupRequest, SignupResponse, VerifyRequest, VerifyResponse
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
    auth_token, user = auth_service.verify(req.token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 404
    resp = VerifyResponse(authToken=auth_token, user=user, userRole=user['role'])
    return jsonify(resp.model_dump()), 200

@bp.route('/auth/me', methods=['GET'])
@require_auth
def me():
    founder = FounderProfile.query.get(request.user_id)
    if founder:
        from schemas.founder_profile import FounderProfile as FounderProfileSchema
        return jsonify(FounderProfileSchema(**{
            'id': founder.id,
            'name': founder.name,
            'email': founder.email,
            'role': founder.role,
            'background': founder.background,
            'experienceLevel': founder.experience_level,
            'location': founder.location,
            'focusAreas': founder.focus_areas,
            'linkedinUrl': founder.linkedin_url,
            'companyName': founder.company_name,
            'fundingStage': founder.funding_stage,
            'title': founder.title,
            'createdAt': founder.created_at.isoformat() if founder.created_at else None,
            'updatedAt': founder.updated_at.isoformat() if founder.updated_at else None
        }).model_dump(mode="json")), 200
    investor = InvestorProfile.query.get(request.user_id)
    if investor:
        from schemas.investor import InvestorProfile as InvestorProfileSchema
        return jsonify(InvestorProfileSchema(**{
            'id': investor.id,
            'name': investor.name,
            'email': investor.email,
            'firmName': investor.firm_name,
            'title': investor.title,
            'investmentThesis': {
                'stageFocus': investor.stage_focus,
                'sectorPreferences': investor.sector_preferences,
                'geographicFocus': investor.geographic_focus,
                'checkSizeRange': investor.check_size_range,
                'investmentStyle': investor.investment_style,
                'dealFlowPreference': investor.deal_flow_preference,
                'dueDiligenceStyle': investor.due_diligence_style,
                'valueAddAreas': investor.value_add_areas,
                'investmentsPerYear': investor.investments_per_year
            },
            'linkedinUrl': investor.linkedin_url,
            'accredited': investor.accredited,
            'createdAt': investor.created_at.isoformat() if investor.created_at else None,
            'updatedAt': investor.updated_at.isoformat() if investor.updated_at else None
        }).model_dump(mode="json")), 200
    return jsonify({'error': 'Profile not found'}), 404

@bp.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    # For MVP, do nothing (stateless JWT)
    return jsonify({'success': True}), 200
