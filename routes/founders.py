from flask import Blueprint, request, jsonify
from schemas.founder_profile import FounderProfileInput, FounderProfile as FounderProfileSchema
from models import FounderProfile, User
from db import db
from utils.auth import require_auth

bp = Blueprint('founders', __name__)

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
            experience_level=req.experienceLevel,
            location=req.location,
            focus_areas=req.focusAreas,
            linkedin_url=req.linkedinUrl,
        )
        db.session.add(founder)
    else:
        founder.name = req.name
        founder.email = req.email
        founder.role = req.role
        founder.background = req.background
        founder.experience_level = req.experienceLevel
        founder.location = req.location
        founder.focus_areas = req.focusAreas
        founder.linkedin_url = req.linkedinUrl
    db.session.commit()
    return jsonify(FounderProfileSchema(
        id=founder.id,
        name=founder.name,
        email=founder.email,
        role=founder.role,
        background=founder.background,
        experienceLevel=founder.experience_level,
        location=founder.location,
        focusAreas=founder.focus_areas,
        linkedinUrl=founder.linkedin_url,
        createdAt=founder.created_at.isoformat() if founder.created_at else None,
        updatedAt=founder.updated_at.isoformat() if founder.updated_at else None
    ).model_dump(mode="json")), 201

@bp.route('/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    founder = FounderProfile.query.get(founder_id)
    if not founder:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(FounderProfileSchema(
        id=founder.id,
        name=founder.name,
        email=founder.email,
        role=founder.role,
        background=founder.background,
        experienceLevel=founder.experience_level,
        location=founder.location,
        focusAreas=founder.focus_areas,
        linkedinUrl=founder.linkedin_url,
        createdAt=founder.created_at.isoformat() if founder.created_at else None,
        updatedAt=founder.updated_at.isoformat() if founder.updated_at else None
    ).model_dump(mode="json")), 200

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
            experience_level=req.experienceLevel,
            location=req.location,
            focus_areas=req.focusAreas,
            linkedin_url=req.linkedinUrl,
        )
        db.session.add(founder)
    else:
        founder.name = req.name
        founder.email = req.email
        founder.role = req.role
        founder.background = req.background
        founder.experience_level = req.experienceLevel
        founder.location = req.location
        founder.focus_areas = req.focusAreas
        founder.linkedin_url = req.linkedinUrl
    db.session.commit()
    return jsonify(FounderProfileSchema(
        id=founder.id,
        name=founder.name,
        email=founder.email,
        role=founder.role,
        background=founder.background,
        experienceLevel=founder.experience_level,
        location=founder.location,
        focusAreas=founder.focus_areas,
        linkedinUrl=founder.linkedin_url,
        createdAt=founder.created_at.isoformat() if founder.created_at else None,
        updatedAt=founder.updated_at.isoformat() if founder.updated_at else None
    ).model_dump(mode="json")), 200
