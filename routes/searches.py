from flask import Blueprint, request, jsonify
from models import SavedSearch, User
from schemas.hiring import SavedSearchInput, SavedSearch as SavedSearchSchema
from schemas import saved_search_to_dict
from utils.auth import require_auth, get_current_user
from db import db
from pydantic import ValidationError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

searches_bp = Blueprint('searches', __name__)

@searches_bp.route('/searches', methods=['POST'])
@require_auth
def create_saved_search():
    """Save search criteria for quick reuse"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Parse request body
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate input
        try:
            search_input = SavedSearchInput.parse_obj(data)
        except ValidationError as e:
            logger.error(f"Validation error in saved search creation: {e}")
            return jsonify({'error': 'Invalid search data', 'details': e.errors()}), 400

        # Create saved search
        saved_search = SavedSearch(
            founder_id=current_user.id,
            name=search_input.name,
            search_criteria=search_input.search_criteria.dict(),
            created_at=datetime.utcnow(),
            last_used=None
        )

        # Save to database
        db.session.add(saved_search)
        db.session.commit()

        # Convert to API response format
        search_data = saved_search_to_dict(saved_search)

        return jsonify(search_data), 201

    except Exception as e:
        logger.error(f"Error creating saved search: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@searches_bp.route('/searches', methods=['GET'])
@require_auth
def get_saved_searches():
    """Get all saved searches for the current founder"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Get saved searches
        saved_searches = db.session.query(SavedSearch).filter(
            SavedSearch.founder_id == current_user.id
        ).order_by(SavedSearch.created_at.desc()).all()

        # Convert to API response format
        searches_data = [saved_search_to_dict(search) for search in saved_searches]

        return jsonify(searches_data), 200

    except Exception as e:
        logger.error(f"Error getting saved searches: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@searches_bp.route('/searches/<search_id>', methods=['GET'])
@require_auth
def get_saved_search(search_id):
    """Get details of a specific saved search"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Find saved search
        saved_search = db.session.query(SavedSearch).filter(
            SavedSearch.id == search_id,
            SavedSearch.founder_id == current_user.id
        ).first()

        if not saved_search:
            return jsonify({'error': 'Saved search not found'}), 404

        # Update last used timestamp
        saved_search.last_used = datetime.utcnow()
        db.session.commit()

        # Convert to API response format
        search_data = saved_search_to_dict(saved_search)

        return jsonify(search_data), 200

    except Exception as e:
        logger.error(f"Error getting saved search {search_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@searches_bp.route('/searches/<search_id>', methods=['DELETE'])
@require_auth
def delete_saved_search(search_id):
    """Delete a saved search"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Find saved search
        saved_search = db.session.query(SavedSearch).filter(
            SavedSearch.id == search_id,
            SavedSearch.founder_id == current_user.id
        ).first()

        if not saved_search:
            return jsonify({'error': 'Saved search not found'}), 404

        # Delete saved search
        db.session.delete(saved_search)
        db.session.commit()

        return '', 204

    except Exception as e:
        logger.error(f"Error deleting saved search {search_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@searches_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': 'NOT_FOUND',
        'message': 'Resource not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@searches_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'code': 'BAD_REQUEST',
        'message': 'Bad request',
        'timestamp': datetime.utcnow().isoformat()
    }), 400

@searches_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': 'INTERNAL_ERROR',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500