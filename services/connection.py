import uuid
from datetime import datetime

connections = {}

def create_connection(founder_id, match_id, match_type, custom_message):
    connection_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    connection = {
        'id': connection_id,
        'founderId': founder_id,
        'matchId': match_id,
        'matchType': match_type,
        'customMessage': custom_message,
        'status': 'pending',
        'requestedAt': now,
        'respondedAt': None
    }
    connections[connection_id] = connection
    return connection

def get_connections(founder_id, status=None, match_type=None):
    result = [c for c in connections.values() if c['founderId'] == founder_id]
    if status:
        result = [c for c in result if c['status'] == status]
    if match_type:
        result = [c for c in result if c['matchType'] == match_type]
    return result

def get_connection(connection_id):
    return connections.get(connection_id)

def update_connection(connection_id, status=None, custom_message=None):
    connection = connections.get(connection_id)
    if not connection:
        return None
    if status:
        connection['status'] = status
        if status in ['accepted', 'declined']:
            connection['respondedAt'] = datetime.utcnow().isoformat()
    if custom_message is not None:
        connection['customMessage'] = custom_message
    return connection
