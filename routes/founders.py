from flask import Blueprint, request, jsonify
from schemas.founder import FounderProfileInput, FounderProfile as FounderProfileSchema
from schemas import founder_profile_to_dict
from models import FounderProfile, User
from db import db
from utils.auth import require_auth

bp = Blueprint('founders', __name__)

@bp.route('/founders', methods=['GET'])
@require_auth
def list_founders():
    """Get list of all founders with optional filtering"""
    # Get query parameters for filtering
    funding_stage = request.args.get('fundingStage')
    location = request.args.get('location')
    background = request.args.get('background')
    limit = request.args.get('limit', type=int)

    # Build query
    query = FounderProfile.query

    # Apply filters if provided
    if funding_stage:
        query = query.filter_by(funding_stage=funding_stage)
    if location:
        query = query.filter(FounderProfile.location.ilike(f'%{location}%'))
    if background:
        query = query.filter_by(background=background)

    # Apply limit if provided
    if limit:
        query = query.limit(limit)

    founders = query.all()
    result = [founder_profile_to_dict(founder) for founder in founders]

    return jsonify(result), 200

@bp.route('/founders', methods=['POST'])
@require_auth
def create_or_update_founder():
    data = request.get_json() or {}
    if 'linkedinUrl' in data and (data['linkedinUrl'] is None or str(data['linkedinUrl']).strip() == ''):
        del data['linkedinUrl']
    req = FounderProfileInput.model_validate(data)
    user = User.query.get(request.user_id)
    if not user:
        user = User(id=request.user_id, email=req.email, role='founder')
        db.session.add(user)
    founder = FounderProfile.query.get(request.user_id)
    if not founder:
        founder = FounderProfile(
            id=request.user_id,
            name=req.name,
            email=req.email,
            role=req.role,
            background=req.background,
            experience_level=req.experience_level,
            location=req.location,
            focus_areas=req.focus_areas,
            linkedin_url=req.linkedin_url,
            company_name=req.company_name,
            funding_stage=req.funding_stage,
            title=req.title,
        )
        db.session.add(founder)
    else:
        founder.name = req.name
        founder.email = req.email
        founder.role = req.role
        founder.background = req.background
        founder.experience_level = req.experience_level
        founder.location = req.location
        founder.focus_areas = req.focus_areas
        founder.linkedin_url = req.linkedin_url
        founder.company_name = req.company_name
        founder.funding_stage = req.funding_stage
        founder.title = req.title
    db.session.commit()
    return jsonify(founder_profile_to_dict(founder)), 201

@bp.route('/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    founder = FounderProfile.query.get(founder_id)
    if not founder:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(founder_profile_to_dict(founder)), 200

@bp.route('/founders/<founder_id>', methods=['PUT'])
@require_auth
def update_founder(founder_id):
    data = request.get_json() or {}
    if 'linkedinUrl' in data and (data['linkedinUrl'] is None or str(data['linkedinUrl']).strip() == ''):
        del data['linkedinUrl']
    req = FounderProfileInput.model_validate(data)
    founder = FounderProfile.query.get(founder_id)
    user = User.query.get(founder_id)
    if not user:
        user = User(id=founder_id, email=req.email, role='founder')
        db.session.add(user)
    if not founder:
        # Create new founder profile if not found
        founder = FounderProfile(
            id=founder_id,
            name=req.name,
            email=req.email,
            role=req.role,
            background=req.background,
            experience_level=req.experience_level,
            location=req.location,
            focus_areas=req.focus_areas,
            linkedin_url=req.linkedin_url,
            company_name=req.company_name,
            funding_stage=req.funding_stage,
            title=req.title,
        )
        db.session.add(founder)
    else:
        founder.name = req.name
        founder.email = req.email
        founder.role = req.role
        founder.background = req.background
        founder.experience_level = req.experience_level
        founder.location = req.location
        founder.focus_areas = req.focus_areas
        founder.linkedin_url = req.linkedin_url
        founder.company_name = req.company_name
        founder.funding_stage = req.funding_stage
        founder.title = req.title
    db.session.commit()
    return jsonify(founder_profile_to_dict(founder)), 200
