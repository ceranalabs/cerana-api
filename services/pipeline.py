import uuid
from datetime import datetime
from models import PipelineDeal, FounderProfile, User
from db import db
from schemas import pipeline_deal_to_dict
from typing import Dict, List, Optional

def get_pipeline(filters: Dict, investor_id: str) -> List[Dict]:
    """Get pipeline deals for an investor with optional filters"""
    query = PipelineDeal.query.filter_by(investor_id=investor_id)

    # Apply filters if provided
    if 'stage' in filters:
        query = query.filter_by(stage=filters['stage'])
    if 'status' in filters:
        query = query.filter_by(status=filters['status'])

    deals = query.all()
    return [pipeline_deal_to_dict(deal) for deal in deals]

def add_to_pipeline(data, investor_id: str) -> Dict:
    """Add a founder to the pipeline"""
    # Get founder info to populate the deal
    founder = FounderProfile.query.get(data.founder_id)

    deal = PipelineDeal(
        investor_id=investor_id,
        founder_id=data.founder_id,
        founder_name=founder.name if founder else None,
        company_name=founder.company_name if founder else None,
        stage='sourced',  # Default initial stage
        status='active',
        match_score=None,
        key_metrics=None,
        risk_flags=None,
        opportunities=None,
        notes=None
    )

    db.session.add(deal)
    db.session.commit()
    return pipeline_deal_to_dict(deal)

def get_pipeline_deal(deal_id: str, investor_id: str) -> Optional[Dict]:
    """Get a specific pipeline deal"""
    deal = PipelineDeal.query.filter_by(id=deal_id, investor_id=investor_id).first()
    return pipeline_deal_to_dict(deal) if deal else None

def update_pipeline_deal(deal_id: str, data: Dict, investor_id: str) -> Optional[Dict]:
    """Update a pipeline deal"""
    deal = PipelineDeal.query.filter_by(id=deal_id, investor_id=investor_id).first()
    if not deal:
        return None

    # Update fields if provided
    if 'stage' in data:
        deal.stage = data['stage']
    if 'status' in data:
        deal.status = data['status']
    if 'next_action' in data:
        deal.next_action = data['next_action']
    if 'next_action_due' in data:
        deal.next_action_due = data['next_action_due']
    if 'match_score' in data:
        deal.match_score = data['match_score']
    if 'key_metrics' in data:
        deal.key_metrics = data['key_metrics']
    if 'risk_flags' in data:
        deal.risk_flags = data['risk_flags']
    if 'opportunities' in data:
        deal.opportunities = data['opportunities']
    if 'notes' in data:
        deal.notes = data['notes']

    deal.updated_at = datetime.utcnow()
    db.session.commit()
    return pipeline_deal_to_dict(deal)

def get_meetings(filters, meetings):
    # For MVP, ignore filters
    return list(meetings.values())

def request_meeting(data, meetings):
    meeting_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    meeting = {
        'id': meeting_id,
        'founderId': data['founderId'],
        'founderName': data.get('founderName', ''),
        'companyName': data.get('companyName', ''),
        'meetingType': data['meetingType'],
        'scheduledAt': None,
        'duration': data.get('duration', 30),
        'status': 'requested',
        'agenda': data.get('agenda', ''),
        'notes': data.get('customMessage', ''),
        'meetingUrl': None,
        'requestedAt': now
    }
    meetings[meeting_id] = meeting
    return meeting
