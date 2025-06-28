import uuid
from datetime import datetime

users = {}
verification_tokens = {}
sessions = {}

def signup(email, role):
    user_id = str(uuid.uuid4())
    users[user_id] = {
        'id': user_id,
        'email': email,
        'role': role,
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    token = str(uuid.uuid4())
    verification_tokens[token] = user_id
    return user_id, token

def verify(token):
    user_id = verification_tokens.get(token)
    if not user_id:
        return None, None
    # Simulate auth token (MVP: just UUID)
    auth_token = str(uuid.uuid4())
    sessions[auth_token] = user_id
    user = users[user_id]
    return auth_token, user

def get_user_by_token(auth_token):
    user_id = sessions.get(auth_token)
    if not user_id:
        return None
    return users.get(user_id)
