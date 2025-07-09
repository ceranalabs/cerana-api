from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.meeting import MeetingRequestInput, MeetingRequestOutput
from schemas import meeting_to_dict
from models import Meeting
from db import db
from datetime import datetime

bp = Blueprint('meeting', __name__)

@bp.route('/meetings', methods=['GET'])
@require_auth
def get_meetings_route():
    # Optionally add filters here
    meetings = Meeting.query.all()
    result = [meeting_to_dict(meeting) for meeting in meetings]
    return jsonify(result), 200

@bp.route('/meetings', methods=['POST'])
@require_auth
def request_meeting_route():
    data = request.get_json()
    validated = MeetingRequestInput.model_validate(data)
    meeting = Meeting(
        founder_id=validated.founder_id,
        meeting_type=validated.meeting_type,
        duration=validated.duration,
        agenda=validated.agenda,
        notes=validated.custom_message,
        status='requested',
        requested_at=datetime.utcnow()
    )
    db.session.add(meeting)
    db.session.commit()

    return jsonify(meeting_to_dict(meeting)), 201
