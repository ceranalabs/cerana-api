from flask import Flask
from flask_cors import CORS
from routes.auth import bp as auth_bp
from routes.founders import bp as founders_bp
from routes.ideas import bp as ideas_bp
from routes.uploads import bp as uploads_bp
from routes.analysis import bp as analysis_bp
from routes.matches import bp as matches_bp
from routes.connections import bp as connections_bp
from routes.investor import bp as investor_bp
from routes.discovery import bp as discovery_bp
from routes.pipeline import bp as pipeline_bp
from routes.meeting import bp as meeting_bp
from routes.candidates import candidates_bp
from routes.jobs import jobs_bp
from routes.searches import searches_bp
from db import db
import config

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Explicitly allow all origins on all routes
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(founders_bp)
    app.register_blueprint(ideas_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(connections_bp)
    app.register_blueprint(investor_bp)
    app.register_blueprint(discovery_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(meeting_bp)
    # Hiring platform blueprints
    app.register_blueprint(candidates_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(searches_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
