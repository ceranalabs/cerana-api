import os
import jwt
from functools import wraps
from flask import request, jsonify

CLERK_JWT_ISSUER = 'https://exact-horse-66.clerk.accounts.dev'
CLERK_JWT_AUDIENCE = None  # TODO: Set to your Clerk app's audience if needed
CLERK_PUBLIC_KEY = os.environ.get('CLERK_PUBLIC_KEY', 'pk_test_ZXhhY3QtaG9yc2UtNjYuY2xlcmsuYWNjb3VudHMuZGV2JA')

# Now verify signature and claims

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ', 1)[1]
        try:
            payload = jwt.decode(
                token,
                CLERK_PUBLIC_KEY,
                algorithms=["RS256", "HS256"],
                issuer=CLERK_JWT_ISSUER,
                options={"require": ["exp", "sub"], "verify_aud": False}  # Set verify_aud True and audience if needed
            )
            request.user_id = payload.get('sub')
            request.user_role = payload.get('role', 'founder')
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
        return f(*args, **kwargs)
    return decorated
