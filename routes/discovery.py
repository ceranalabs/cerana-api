from flask import Blueprint, jsonify
from datetime import datetime
from models import FounderProfile
from schemas.founder import FounderDiscoveryCard, DetailedFounderProfile
from utils.auth import require_auth
from db import db

bp = Blueprint('discovery', __name__)

@bp.route('/discovery/founders', methods=['GET'])
@require_auth
def list_founders():
    # Query all founders from the database
    founders = FounderProfile.query.all()
    # Convert to discovery cards (or just serialize as needed)
    result = [
        {
            'id': f.id,
            'name': f.name,
            'title': None,  # Add title if you have it in your model
            'companyName': None,  # Add companyName if you have it in your model
            'matchScore': None,   # Add matchScore logic if needed
            'problemStatement': None,
            'fundingStage': None,
            'raisingAmount': None,
            'location': f.location,
            'traction': None,  # Add traction if you have it in your model
            'whyThisFits': None,
            'riskFlags': None,
            'opportunities': None,
            'avatarUrl': f.linkedin_url,
            'lastUpdated': f.updated_at.isoformat() if f.updated_at else None
        }
        for f in founders
    ]
    return jsonify(result), 200

@bp.route('/discovery/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    founder = FounderProfile.query.get(founder_id)
    if not founder:
        return jsonify({'error': 'Not found'}), 404
    # You can expand this to a detailed profile as needed
    result = {
        'id': founder.id,
        'name': founder.name,
        'title': None,
        'companyName': None,
        'background': founder.background,
        'experienceLevel': founder.experience_level,
        'location': founder.location,
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
