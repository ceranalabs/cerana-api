import uuid
from datetime import datetime

def get_pipeline(filters, pipeline):
    # For MVP, ignore filters
    return list(pipeline.values())

def add_to_pipeline(data, pipeline):
    deal_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    deal = {
        'id': deal_id,
        'founderId': data['founderId'],
        'founderName': data.get('founderName', ''),
        'companyName': data.get('companyName', ''),
        'stage': data.get('initialStage', 'sourced'),
        'status': 'active',
        'daysInStage': 0,
        'nextAction': '',
        'nextActionDue': None,
        'matchScore': 0,
        'keyMetrics': {},
        'riskFlags': [],
        'opportunities': [],
        'notes': [],
        'addedAt': now,
        'updatedAt': now
    }
    pipeline[deal_id] = deal
    return deal

def get_pipeline_deal(deal_id, pipeline):
    return pipeline.get(deal_id)

def update_pipeline_deal(deal_id, data, pipeline):
    deal = pipeline.get(deal_id)
    if not deal:
        return None
    deal.update(data)
    deal['updatedAt'] = datetime.utcnow().isoformat()
    return deal

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
