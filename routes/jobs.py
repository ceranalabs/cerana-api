from flask import Blueprint, request, jsonify
from models import JobPosting, User
from schemas.hiring import JobPostingInput, JobPosting as JobPostingSchema
from schemas import job_posting_to_dict, create_pagination_dict
from services.hiring import HiringMatchingService
from utils.auth import require_auth, get_current_user
from db import db
from pydantic import ValidationError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['POST'])
@require_auth
def create_job():
    """Create a new job posting"""
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
            job_input = JobPostingInput.parse_obj(data)
        except ValidationError as e:
            logger.error(f"Validation error in job creation: {e}")
            return jsonify({'error': 'Invalid job data', 'details': e.errors()}), 400

        # Create job posting
        job_posting = JobPosting(
            founder_id=current_user.id,
            title=job_input.title,
            job_description=job_input.job_description,
            required_skills=job_input.required_skills,
            preferred_skills=job_input.preferred_skills,
            experience_level=job_input.experience_level,
            location=job_input.location,
            is_remote=job_input.is_remote,
            salary_range=job_input.salary_range.dict(),
            equity=job_input.equity.dict() if job_input.equity else None,
            employment_type=job_input.employment_type,
            department=job_input.department,
            team=job_input.team,
            status='active',
            posted_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to database
        db.session.add(job_posting)
        db.session.commit()

        # Convert to API response format
        job_data = job_posting_to_dict(job_posting)

        return jsonify(job_data), 201

    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@jobs_bp.route('/jobs', methods=['GET'])
@require_auth
def get_jobs():
    """Get paginated list of job postings for the current founder"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 50)  # Cap at 50
        status = request.args.get('status')

        # Validate parameters
        if page < 1:
            return jsonify({'error': 'Page must be >= 1'}), 400
        if limit < 1:
            return jsonify({'error': 'Limit must be >= 1'}), 400
        if status and status not in ['active', 'paused', 'closed']:
            return jsonify({'error': 'Invalid status filter'}), 400

        # Get jobs using service
        result = HiringMatchingService.get_job_postings_list(
            founder_id=current_user.id,
            page=page,
            limit=limit,
            status=status
        )

        # Convert to API response format
        jobs_data = [job_posting_to_dict(job) for job in result['jobs']]

        response = {
            'jobs': jobs_data,
            'pagination': result['pagination']
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error getting jobs: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['GET'])
@require_auth
def get_job(job_id):
    """Get job posting details by ID"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Find job posting
        job_posting = db.session.query(JobPosting).filter(
            JobPosting.id == job_id,
            JobPosting.founder_id == current_user.id
        ).first()

        if not job_posting:
            return jsonify({'error': 'Job posting not found'}), 404

        # Convert to API response format
        job_data = job_posting_to_dict(job_posting)

        return jsonify(job_data), 200

    except Exception as e:
        logger.error(f"Error getting job {job_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['PUT'])
@require_auth
def update_job(job_id):
    """Update an existing job posting"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Find job posting
        job_posting = db.session.query(JobPosting).filter(
            JobPosting.id == job_id,
            JobPosting.founder_id == current_user.id
        ).first()

        if not job_posting:
            return jsonify({'error': 'Job posting not found'}), 404

        # Parse request body
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate input
        try:
            job_input = JobPostingInput.parse_obj(data)
        except ValidationError as e:
            logger.error(f"Validation error in job update: {e}")
            return jsonify({'error': 'Invalid job data', 'details': e.errors()}), 400

        # Update job posting
        job_posting.title = job_input.title
        job_posting.job_description = job_input.job_description
        job_posting.required_skills = job_input.required_skills
        job_posting.preferred_skills = job_input.preferred_skills
        job_posting.experience_level = job_input.experience_level
        job_posting.location = job_input.location
        job_posting.is_remote = job_input.is_remote
        job_posting.salary_range = job_input.salary_range.dict()
        job_posting.equity = job_input.equity.dict() if job_input.equity else None
        job_posting.employment_type = job_input.employment_type
        job_posting.department = job_input.department
        job_posting.team = job_input.team
        job_posting.updated_at = datetime.utcnow()

        # Save to database
        db.session.commit()

        # Convert to API response format
        job_data = job_posting_to_dict(job_posting)

        return jsonify(job_data), 200

    except Exception as e:
        logger.error(f"Error updating job {job_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['DELETE'])
@require_auth
def delete_job(job_id):
    """Delete a job posting"""
    try:
        # Get current user
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401

        # Find job posting
        job_posting = db.session.query(JobPosting).filter(
            JobPosting.id == job_id,
            JobPosting.founder_id == current_user.id
        ).first()

        if not job_posting:
            return jsonify({'error': 'Job posting not found'}), 404

        # Delete job posting
        db.session.delete(job_posting)
        db.session.commit()

        return '', 204

    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@jobs_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': 'NOT_FOUND',
        'message': 'Resource not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@jobs_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'code': 'BAD_REQUEST',
        'message': 'Bad request',
        'timestamp': datetime.utcnow().isoformat()
    }), 400

@jobs_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': 'INTERNAL_ERROR',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500