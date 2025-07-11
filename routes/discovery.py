from flask import Blueprint, jsonify
from datetime import datetime
from models import FounderProfile
from schemas.founder import FounderDiscoveryCard, DetailedFounderProfile
from schemas import founder_profile_to_dict
from utils.auth import require_auth
from db import db

bp = Blueprint('discovery', __name__)

@bp.route('/discovery/founders', methods=['GET'])
@require_auth
def list_founders():
    # Query all founders from the database
    founders = FounderProfile.query.all()
    # Convert to discovery cards format
    result = []
    for f in founders:
        result.append({
            'id': f.id,
            'name': f.name,
            'title': f.title,
            'companyName': f.company_name,
            'matchScore': None,   # Add matchScore logic if needed
            'problemStatement': None,
            'fundingStage': f.funding_stage,
            'raisingAmount': None,
            'location': f.location,
            'traction': None,  # Add traction if you have it in your model
            'whyThisFits': None,
            'riskFlags': None,
            'opportunities': None,
            'avatarUrl': f.linkedin_url,
            'lastUpdated': f.updated_at.isoformat() if f.updated_at else None
        })
    return jsonify(result), 200

@bp.route('/discovery/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    founder = FounderProfile.query.get(founder_id)
    if not founder:
        return jsonify({'error': 'Not found'}), 404

    # Return detailed founder profile
    result = {
        'id': founder.id,
        'name': founder.name,
        'title': founder.title,
        'companyName': founder.company_name,
        'background': founder.background,
        'experienceLevel': founder.experience_level,
        'location': founder.location,
        'focusAreas': founder.focus_areas,
        'linkedinUrl': founder.linkedin_url,
        'startupIdea': None,
        'traction': None,
        'team': None,
        'fundraising': None,
        'references': None,
        'documents': None,
        'lastUpdated': founder.updated_at.isoformat() if founder.updated_at else None
    }
    return jsonify(result), 200
