SECRET_KEY = 'cerana-mvp-secret-key'
import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/cerana')
SQLALCHEMY_TRACK_MODIFICATIONS = False
