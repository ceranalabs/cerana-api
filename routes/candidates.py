from flask import Blueprint, request, jsonify
from models import CandidateProfile, WorkExperience, Education
from schemas.hiring import CandidateSearchRequest, CandidateProfile as CandidateProfileSchema
from schemas import (
    candidate_profile_to_dict,
    detailed_candidate_profile_to_dict,
    work_experience_to_dict,
    create_pagination_dict
)
from services.hiring import HiringMatchingService
from utils.auth import require_auth
from db import db
from pydantic import ValidationError
import logging
import csv
import io
from datetime import datetime, date
import re

logger = logging.getLogger(__name__)

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/candidates', methods=['GET'])
@require_auth
def get_candidates():
    """Get paginated list of all candidates"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100)  # Cap at 100
        sort = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')

        # Validate parameters
        if page < 1:
            return jsonify({'error': 'Page must be >= 1'}), 400
        if limit < 1:
            return jsonify({'error': 'Limit must be >= 1'}), 400
        if sort not in ['name', 'experience', 'location', 'created_at']:
            return jsonify({'error': 'Invalid sort field'}), 400
        if order not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid order direction'}), 400

        # Get candidates using service
        result = HiringMatchingService.get_candidates_list(page, limit, sort, order)

        # Convert to API response format
        candidates_data = [candidate_profile_to_dict(c) for c in result['candidates']]

        response = {
            'candidates': candidates_data,
            'pagination': result['pagination']
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error getting candidates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@candidates_bp.route('/candidates/<candidate_id>', methods=['GET'])
@require_auth
def get_candidate(candidate_id):
    """Get detailed candidate profile by ID"""
    try:
        # Find candidate
        candidate = db.session.query(CandidateProfile).filter(
            CandidateProfile.id == candidate_id
        ).first()

        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404

        # Convert to detailed response format
        candidate_data = detailed_candidate_profile_to_dict(candidate)

        return jsonify(candidate_data), 200

    except Exception as e:
        logger.error(f"Error getting candidate {candidate_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@candidates_bp.route('/candidates/search', methods=['POST'])
@require_auth
def search_candidates():
    """Search and match candidates with AI-powered scoring"""
    try:
        # Parse request body
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate search request
        try:
            search_request = CandidateSearchRequest.parse_obj(data)
        except ValidationError as e:
            logger.error(f"Validation error in search request: {e}")
            return jsonify({'error': 'Invalid search request', 'details': e.errors()}), 400

        # Convert to dict for service
        search_dict = search_request.dict()

        # Perform search using service
        search_result = HiringMatchingService.search_candidates(search_dict)

        # Convert matched candidates to API format
        matched_candidates = []
        for item in search_result['candidates']:
            candidate = item['candidate']
            match_score = item['match_score']
            match_breakdown = item['match_breakdown']
            recent_experience = item['recent_experience']

            # Base candidate data
            candidate_data = candidate_profile_to_dict(candidate)

            # Add match information
            candidate_data['matchScore'] = match_score
            candidate_data['matchBreakdown'] = {
                'skillsMatch': {
                    'score': match_breakdown['skills_match']['score'],
                    'matchedSkills': match_breakdown['skills_match']['matched_skills'],
                    'missingSkills': match_breakdown['skills_match']['missing_skills'],
                    'matchedCount': match_breakdown['skills_match']['matched_count'],
                    'totalRequired': match_breakdown['skills_match']['total_required']
                },
                'experienceMatch': {
                    'score': match_breakdown['experience_match']['score'],
                    'reasoning': match_breakdown['experience_match']['reasoning']
                },
                'locationMatch': {
                    'score': match_breakdown['location_match']['score'],
                    'distance': match_breakdown['location_match']['distance']
                },
                'availabilityMatch': {
                    'score': match_breakdown['availability_match']['score'],
                    'status': match_breakdown['availability_match']['status']
                }
            }

            # Add recent experience
            candidate_data['recentExperience'] = [
                work_experience_to_dict(exp) for exp in recent_experience
            ]

            matched_candidates.append(candidate_data)

        # Format response
        response = {
            'candidates': matched_candidates,
            'pagination': search_result['pagination'],
            'searchMetadata': search_result['search_metadata']
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error searching candidates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@candidates_bp.route('/candidates/import', methods=['POST'])
@require_auth
def import_candidates_csv():
    """Import candidates from Bullhorn CSV export"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400

        # Read CSV content
        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))

        imported_count = 0
        error_count = 0
        errors = []

        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is headers
            try:
                # Map Bullhorn fields to our model
                candidate_data = map_bullhorn_to_candidate(row)

                # Check if candidate already exists (by email)
                existing_candidate = db.session.query(CandidateProfile).filter(
                    CandidateProfile.email == candidate_data['email']
                ).first()

                if existing_candidate:
                    logger.info(f"Candidate with email {candidate_data['email']} already exists, skipping")
                    continue

                # Create candidate profile
                candidate = CandidateProfile(**candidate_data['profile'])
                db.session.add(candidate)
                db.session.flush()  # Get the ID

                # Add work experience
                for exp_data in candidate_data['work_experience']:
                    exp_data['candidate_id'] = candidate.id
                    work_exp = WorkExperience(**exp_data)
                    db.session.add(work_exp)

                # Add education
                for edu_data in candidate_data['education']:
                    edu_data['candidate_id'] = candidate.id
                    education = Education(**edu_data)
                    db.session.add(education)

                imported_count += 1

            except Exception as e:
                error_count += 1
                error_msg = f"Row {row_num}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Error importing row {row_num}: {str(e)}")

        # Commit all changes
        db.session.commit()

        # Return import summary
        response = {
            'imported': imported_count,
            'errors': error_count,
            'total_rows': imported_count + error_count,
            'error_details': errors[:10]  # Limit to first 10 errors
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error importing candidates: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

def map_bullhorn_to_candidate(row):
    """Map Bullhorn CSV row to our candidate model"""

    # Helper functions for mapping
    def safe_get(key, default=''):
        return row.get(key, default) or default

    def parse_skills(skill_text):
        """Parse skills from text description"""
        if not skill_text:
            return []
        # Split by common separators and clean up
        skills = re.split(r'[,;\n\r\t]+', skill_text)
        return [skill.strip() for skill in skills if skill.strip()]

    def map_work_authorization(work_auth):
        """Map Bullhorn work authorization to our enum"""
        if not work_auth:
            return 'needs_sponsorship'

        work_auth_lower = str(work_auth).lower()
        if work_auth_lower in ['true', '1', 'yes', 'authorized']:
            return 'citizen'  # Assume citizen if authorized
        return 'needs_sponsorship'

    def map_availability(status):
        """Map Bullhorn status to our availability enum"""
        if not status:
            return 'not_looking'

        status_lower = str(status).lower()
        if 'active' in status_lower or 'looking' in status_lower:
            return 'actively_looking'
        elif 'available' in status_lower or 'open' in status_lower:
            return 'open_to_opportunities'
        return 'not_looking'

    def map_employment_status(employment_pref):
        """Map employment preference to our enum"""
        if not employment_pref:
            return 'employed'

        pref_lower = str(employment_pref).lower()
        if 'unemployed' in pref_lower or 'not working' in pref_lower:
            return 'unemployed'
        elif 'freelance' in pref_lower or 'contractor' in pref_lower:
            return 'freelancing'
        elif 'student' in pref_lower:
            return 'student'
        return 'employed'

    def map_experience_level(years_exp):
        """Map years of experience to our level enum"""
        if not years_exp:
            return 'entry'

        try:
            years = int(years_exp)
            if years < 2:
                return 'entry'
            elif years < 5:
                return 'mid'
            elif years < 10:
                return 'senior'
            elif years < 15:
                return 'lead'
            elif years < 20:
                return 'principal'
            else:
                return 'executive'
        except:
            return 'entry'

    def parse_address(address_obj):
        """Parse address composite into location string"""
        if not address_obj:
            return ''

        # If it's a string, return as-is
        if isinstance(address_obj, str):
            return address_obj

        # Try to parse as composite
        parts = []
        if isinstance(address_obj, dict):
            city = address_obj.get('city', '')
            state = address_obj.get('state', '')
            if city:
                parts.append(city)
            if state:
                parts.append(state)

        return ', '.join(parts) if parts else str(address_obj)

    def parse_salary_expectations(salary, salary_low):
        """Parse salary expectations"""
        try:
            min_salary = float(salary_low) if salary_low else None
            max_salary = float(salary) if salary else None

            if min_salary or max_salary:
                return {
                    'min': min_salary,
                    'max': max_salary,
                    'currency': 'USD'
                }
        except:
            pass
        return None

    # Build full name
    first_name = safe_get('firstName')
    last_name = safe_get('lastName')
    middle_name = safe_get('middleName')

    full_name = f"{first_name} {middle_name} {last_name}".strip()
    if not full_name:
        full_name = safe_get('name')

    # Get primary contact info
    email = safe_get('email')
    phone = safe_get('mobile') or safe_get('phone') or safe_get('workPhone')

    # Parse location
    location = parse_address(safe_get('address')) or safe_get('desiredLocations', 'Unknown')

    # Parse skills
    skills = parse_skills(safe_get('skillSet'))

    # Build candidate profile
    candidate_profile = {
        'name': full_name,
        'email': email,
        'phone': phone,
        'location': location,
        'work_auth_status': map_work_authorization(safe_get('workAuthorized')),
        'availability': map_availability(safe_get('status')),
        'employment_status': map_employment_status(safe_get('employmentPreference')),
        'salary_expectations': parse_salary_expectations(safe_get('salary'), safe_get('salaryLow')),
        'skills': skills,
        'experience_level': map_experience_level(safe_get('experience')),
        'bio': safe_get('description'),
        'linkedin_url': safe_get('companyURL') if 'linkedin' in safe_get('companyURL').lower() else None,
        'portfolio_url': safe_get('companyURL') if 'linkedin' not in safe_get('companyURL').lower() else None,
        'certifications': parse_skills(safe_get('certifications')),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    # Build work experience (if we have current company info)
    work_experience = []
    if safe_get('companyName') and safe_get('occupation'):
        work_experience.append({
            'title': safe_get('occupation'),
            'company': safe_get('companyName'),
            'role_description': safe_get('description', 'No description available'),
            'start_date': date.today(),  # We don't have start date, use today
            'end_date': None,
            'is_current': True,
            'skills': skills[:5] if skills else [],  # Use first 5 skills
            'created_at': datetime.utcnow()
        })

    # Build education
    education = []
    if safe_get('educationDegree'):
        education.append({
            'degree': safe_get('educationDegree'),
            'institution': 'Unknown',  # Bullhorn doesn't seem to have institution field
            'field_of_study': safe_get('degreeList', 'Unknown'),
            'graduation_year': None,
            'gpa': None,
            'created_at': datetime.utcnow()
        })

    return {
        'profile': candidate_profile,
        'work_experience': work_experience,
        'education': education
    }

@candidates_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': 'NOT_FOUND',
        'message': 'Resource not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@candidates_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'code': 'BAD_REQUEST',
        'message': 'Bad request',
        'timestamp': datetime.utcnow().isoformat()
    }), 400

@candidates_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': 'INTERNAL_ERROR',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500