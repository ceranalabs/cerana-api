from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.founder import FounderDiscoveryCard, DetailedFounderProfile
import uuid
from datetime import datetime
from services.matching import discover_founders, get_founder_profile

bp = Blueprint('discovery', __name__)

# In-memory store for MVP
founders = {}

# Example founder for demo
founder_id = str(uuid.uuid4())
founders[founder_id] = {
    'id': founder_id,
    'name': 'Sarah Chen',
    'title': 'CEO',
    'companyName': 'TechFlow AI',
    'matchScore': 94,
    'problemStatement': 'AI-powered invoice processing',
    'fundingStage': 'series-a',
    'raisingAmount': '$2M',
    'location': 'San Francisco',
    'traction': {
        'revenue': '$50K MRR',
        'growth': '15% monthly',
        'customers': '45 SMB clients',
        'retention': '95%',
        'partnerships': '3 major integrators'
    },
    'whyThisFits': [
        'B2B SaaS in your sweet spot',
        'Strong product-market fit signals',
        'Technical founder with domain expertise'
    ],
    'riskFlags': ['Competitive pressure'],
    'opportunities': ['Strong unit economics'],
    'avatarUrl': None,
    'lastUpdated': datetime.utcnow().isoformat()
}

@bp.route('/discovery/founders', methods=['GET'])
@require_auth
def discover_founders():
    founders_list = [FounderDiscoveryCard(**f).model_dump() for f in founders.values()]
    return jsonify({
        'founders': founders_list,
        'pagination': {
            'total': len(founders_list),
            'limit': 20,
            'offset': 0,
            'hasMore': False
        }
    }), 200

@bp.route('/discovery/founders/<founder_id>', methods=['GET'])
@require_auth
def get_founder(founder_id):
    founder = founders.get(founder_id)
    if not founder:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(DetailedFounderProfile(**founder).model_dump(mode="json")), 200
