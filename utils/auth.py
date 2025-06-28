import jwt
from functools import wraps
from flask import request, jsonify

CLERK_JWT_ISSUER = 'https://clerk.dev/'  # TODO: Set to your actual Clerk issuer
CLERK_JWT_AUDIENCE = None  # TODO: Set to your Clerk app's audience if needed

# For MVP, skip signature verification (DO NOT use in production)
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ', 1)[1]
        try:
            # TODO: In production, verify signature and claims
            payload = jwt.decode(token, options={"verify_signature": False})
            request.user_id = payload.get('sub')
            request.user_role = payload.get('role', 'founder')
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
        return f(*args, **kwargs)
    return decorated
