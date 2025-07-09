import os
import jwt
import requests
from functools import wraps
from flask import request, jsonify
from jwt import PyJWKClient

CLERK_JWT_ISSUER = 'https://exact-horse-66.clerk.accounts.dev'
CLERK_JWKS_URL = f"{CLERK_JWT_ISSUER}/.well-known/jwks.json"
PERMITTED_ORIGINS = os.environ.get('PERMITTED_ORIGINS', 'http://localhost:3000,http://localhost:5173,http://localhost:5001,https://cerana.netlify.app,https://zp1v56uxy8rdx5ypatb0ockcb9tr6a-oci3--5173--cb7c0bca.local-credentialless.webcontainer-api.io').split(',')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ', 1)[1]
        try:
            jwks_client = PyJWKClient(CLERK_JWKS_URL)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=CLERK_JWT_ISSUER,
                options={"require": ["exp", "sub"], "verify_aud": False}
            )
            # Optional: azp check for CSRF protection
            if "azp" in payload and payload["azp"] not in PERMITTED_ORIGINS:
                return jsonify({"error": "Invalid azp claim"}), 401
            request.user_id = payload.get('sub')
            request.user_role = payload.get('role', 'founder')
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    """Get the current authenticated user from the database"""
    from models import User
    from db import db

    # Get user_id from request (set by require_auth decorator)
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return None

    # Query database for user
    user = db.session.query(User).filter(User.id == user_id).first()
    return user
