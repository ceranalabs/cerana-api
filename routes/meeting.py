from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.meeting import MeetingRequestInputSchema, MeetingRequestSchema
from services.pipeline import get_meetings, request_meeting

bp = Blueprint('meeting', __name__)

# In-memory store for MVP
meetings = {}

@bp.route('/meetings', methods=['GET'])
@require_auth
def get_meetings_route():
    filters = request.args.to_dict()
    result = get_meetings(filters, meetings)
    return jsonify([MeetingRequestSchema().dump(m) for m in result]), 200

@bp.route('/meetings', methods=['POST'])
@require_auth
def request_meeting_route():
    data = request.get_json()
    validated = MeetingRequestInputSchema().load(data)
    meeting = request_meeting(validated, meetings)
    return jsonify(MeetingRequestSchema().dump(meeting)), 201
