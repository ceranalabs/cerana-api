from flask import Blueprint, request, jsonify
from schemas.connection import ConnectionRequestInput
from services import connection as connection_service
from utils.auth import require_auth

bp = Blueprint('connections', __name__)

@bp.route('/connections', methods=['POST'])
@require_auth
def create_connection():
    data = request.get_json()
    req = ConnectionRequestInput.model_validate(data)
    # For MVP, get match type from match service (simulate)
    match_id = req.matchId
    match_type = 'advisor'  # In real app, look up match type
    connection = connection_service.create_connection(request.user_id, match_id, match_type, req.customMessage)
    return jsonify(connection), 201

@bp.route('/connections', methods=['GET'])
@require_auth
def list_connections():
    status = request.args.get('status')
    match_type = request.args.get('type')
    connections = connection_service.get_connections(request.user_id, status, match_type)
    return jsonify(connections), 200

@bp.route('/connections/<connection_id>', methods=['GET'])
@require_auth
def get_connection(connection_id):
    connection = connection_service.get_connection(connection_id)
    if not connection:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(connection), 200

@bp.route('/connections/<connection_id>', methods=['PUT'])
@require_auth
def update_connection(connection_id):
    data = request.get_json()
    status = data.get('status')
    custom_message = data.get('customMessage')
    connection = connection_service.update_connection(connection_id, status, custom_message)
    if not connection:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(connection), 200
