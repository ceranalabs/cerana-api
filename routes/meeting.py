from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.meeting import MeetingRequestInput, MeetingRequest
from models import Meeting, db
from datetime import datetime

bp = Blueprint('meeting', __name__)

@bp.route('/meetings', methods=['GET'])
@require_auth
def get_meetings_route():
    # Optionally add filters here
    meetings = Meeting.query.all()
    result = [
        MeetingRequest(
            id=m.id,
            founderId=m.founder_id,
            founderName=m.founder_name,
            companyName=m.company_name,
            meetingType=m.meeting_type,
            scheduledAt=m.scheduled_at.isoformat() if m.scheduled_at else None,
            duration=m.duration,
            status=m.status,
            agenda=m.agenda,
            notes=m.notes,
            meetingUrl=m.meeting_url,
            requestedAt=m.requested_at.isoformat() if m.requested_at else None
        ).model_dump(mode="json")
        for m in meetings
    ]
    return jsonify(result), 200

@bp.route('/meetings', methods=['POST'])
@require_auth
def request_meeting_route():
    data = request.get_json()
    validated = MeetingRequestInput(**data)
    meeting = Meeting(
        founder_id=validated.founderId,
        meeting_type=validated.meetingType,
        duration=validated.duration,
        agenda=validated.agenda,
        notes=validated.customMessage,
        status='requested',
        requested_at=datetime.utcnow()
    )
    db.session.add(meeting)
    db.session.commit()
    response = MeetingRequest(
        id=meeting.id,
        founderId=meeting.founder_id,
        founderName=meeting.founder_name,
        companyName=meeting.company_name,
        meetingType=meeting.meeting_type,
        scheduledAt=meeting.scheduled_at.isoformat() if meeting.scheduled_at else None,
        duration=meeting.duration,
        status=meeting.status,
        agenda=meeting.agenda,
        notes=meeting.notes,
        meetingUrl=meeting.meeting_url,
        requestedAt=meeting.requested_at.isoformat() if meeting.requested_at else None
    )
    return jsonify(response.model_dump(mode="json")), 201
