from typing import List, Dict, Any, Optional, Tuple
from models import CandidateProfile, JobPosting, WorkExperience, Education, SavedSearch
from db import db
from sqlalchemy import and_, or_, func
from datetime import datetime
import re
import time

class HiringMatchingService:
    """Service for candidate matching and search functionality"""

    @staticmethod
    def normalize_skill(skill: str) -> str:
        """Normalize skill name for matching"""
        # Convert to lowercase and remove extra spaces
        normalized = skill.lower().strip()

        # Handle common variations
        variations = {
            'react': ['reactjs', 'react.js'],
            'javascript': ['js', 'javascript', 'java script'],
            'typescript': ['ts', 'typescript'],
            'node': ['nodejs', 'node.js'],
            'python': ['python3', 'py'],
            'css': ['css3'],
            'html': ['html5'],
            'postgresql': ['postgres', 'psql'],
            'mongodb': ['mongo'],
            'aws': ['amazon web services'],
            'gcp': ['google cloud platform'],
            'kubernetes': ['k8s'],
            'docker': ['containerization'],
            'machine learning': ['ml', 'machinelearning'],
            'artificial intelligence': ['ai']
        }

        # Check if the skill matches any variation
        for standard, variants in variations.items():
            if normalized in variants or normalized == standard:
                return standard

        return normalized

    @staticmethod
    def calculate_skill_match(candidate_skills: List[str], required_skills: List[str],
                            preferred_skills: Optional[List[str]] = None) -> Dict[str, Any]:
        """Calculate skill match score between candidate and job requirements"""
        if not candidate_skills or not required_skills:
            return {
                'score': 0,
                'matched_skills': [],
                'missing_skills': required_skills or [],
                'matched_count': 0,
                'total_required': len(required_skills) if required_skills else 0
            }

        # Normalize skills
        normalized_candidate = [HiringMatchingService.normalize_skill(skill) for skill in candidate_skills]
        normalized_required = [HiringMatchingService.normalize_skill(skill) for skill in required_skills]
        normalized_preferred = [HiringMatchingService.normalize_skill(skill) for skill in (preferred_skills or [])]

        # Find matches
        matched_required = []
        matched_preferred = []

        for req_skill in normalized_required:
            if req_skill in normalized_candidate:
                matched_required.append(req_skill)

        for pref_skill in normalized_preferred:
            if pref_skill in normalized_candidate:
                matched_preferred.append(pref_skill)

        # Calculate score
        required_match_rate = len(matched_required) / len(normalized_required) if normalized_required else 0
        preferred_bonus = min(len(matched_preferred) * 0.05, 0.2)  # Max 20% bonus for preferred skills

        score = min((required_match_rate + preferred_bonus) * 100, 100)

        return {
            'score': score,
            'matched_skills': matched_required + matched_preferred,
            'missing_skills': [skill for skill in normalized_required if skill not in matched_required],
            'matched_count': len(matched_required),
            'total_required': len(normalized_required)
        }

    @staticmethod
    def calculate_experience_match(candidate_level: str, required_level: str) -> Dict[str, Any]:
        """Calculate experience level match score"""
        level_hierarchy = {
            'entry': 1,
            'mid': 2,
            'senior': 3,
            'lead': 4,
            'principal': 5,
            'executive': 6
        }

        candidate_rank = level_hierarchy.get(candidate_level, 0)
        required_rank = level_hierarchy.get(required_level, 0)

        if candidate_rank == 0 or required_rank == 0:
            return {'score': 0, 'reasoning': 'Invalid experience level'}

        # Perfect match
        if candidate_rank == required_rank:
            return {'score': 100, 'reasoning': 'Perfect experience level match'}

        # Calculate distance penalty
        distance = abs(candidate_rank - required_rank)

        if distance == 1:
            score = 80
            reasoning = 'Close experience level match'
        elif distance == 2:
            score = 60
            reasoning = 'Moderate experience level difference'
        else:
            score = 30
            reasoning = 'Significant experience level difference'

        # Bonus for overqualified candidates (but not too much)
        if candidate_rank > required_rank:
            if distance == 1:
                score = 90
                reasoning = 'Slightly overqualified candidate'
            elif distance == 2:
                score = 70
                reasoning = 'Moderately overqualified candidate'

        return {'score': score, 'reasoning': reasoning}

    @staticmethod
    def calculate_location_match(candidate_location: str, job_location: str,
                               is_remote: bool = False) -> Dict[str, Any]:
        """Calculate location match score"""
        if is_remote:
            return {'score': 100, 'distance': None}

        # Simple city/state matching (can be enhanced with geolocation)
        candidate_clean = candidate_location.lower().strip()
        job_clean = job_location.lower().strip()

        if candidate_clean == job_clean:
            return {'score': 100, 'distance': 0}

        # Check if same city (different state format)
        candidate_parts = candidate_clean.split(',')
        job_parts = job_clean.split(',')

        if len(candidate_parts) >= 2 and len(job_parts) >= 2:
            if candidate_parts[0].strip() == job_parts[0].strip():
                return {'score': 90, 'distance': None}

        # Check if same state/region
        if len(candidate_parts) >= 2 and len(job_parts) >= 2:
            if candidate_parts[-1].strip() == job_parts[-1].strip():
                return {'score': 70, 'distance': None}

        # Default to moderate score for different locations
        return {'score': 40, 'distance': None}

    @staticmethod
    def calculate_availability_match(candidate_availability: str) -> Dict[str, Any]:
        """Calculate availability match score"""
        availability_scores = {
            'actively_looking': 100,
            'open_to_opportunities': 75,
            'not_looking': 30
        }

        score = availability_scores.get(candidate_availability, 50)
        return {'score': score, 'status': candidate_availability}

    @staticmethod
    def calculate_overall_match(candidate: CandidateProfile, job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall match score for a candidate"""
        # Extract job requirements
        required_skills = job_requirements.get('required_skills', [])
        preferred_skills = job_requirements.get('preferred_skills', [])
        experience_level = job_requirements.get('experience_level', '')
        location = job_requirements.get('location', '')
        is_remote = job_requirements.get('is_remote', False)

        # Calculate individual match scores
        skills_match = HiringMatchingService.calculate_skill_match(
            candidate.skills, required_skills, preferred_skills
        )
        experience_match = HiringMatchingService.calculate_experience_match(
            candidate.experience_level, experience_level
        )
        location_match = HiringMatchingService.calculate_location_match(
            candidate.location, location, is_remote
        )
        availability_match = HiringMatchingService.calculate_availability_match(
            candidate.availability
        )

        # Weighted overall score
        weights = {
            'skills': 0.4,
            'experience': 0.3,
            'location': 0.2,
            'availability': 0.1
        }

        overall_score = (
            skills_match['score'] * weights['skills'] +
            experience_match['score'] * weights['experience'] +
            location_match['score'] * weights['location'] +
            availability_match['score'] * weights['availability']
        )

        return {
            'match_score': round(overall_score, 2),
            'match_breakdown': {
                'skills_match': skills_match,
                'experience_match': experience_match,
                'location_match': location_match,
                'availability_match': availability_match
            }
        }

    @staticmethod
    def search_candidates(search_request: Dict[str, Any]) -> Dict[str, Any]:
        """Search and rank candidates based on job requirements"""
        start_time = time.time()

        # Extract search parameters
        job_requirements = search_request.get('job_requirements', {})
        filters = search_request.get('filters', {})
        matching_criteria = search_request.get('matching', {})
        pagination = search_request.get('pagination', {'page': 1, 'limit': 20})
        sort_config = search_request.get('sort', {'field': 'match_score', 'order': 'desc'})

        # Build base query
        query = db.session.query(CandidateProfile)

        # Apply filters
        if filters:
            if 'availability' in filters and filters['availability']:
                query = query.filter(CandidateProfile.availability.in_(filters['availability']))

            if 'work_auth_status' in filters and filters['work_auth_status']:
                query = query.filter(CandidateProfile.work_auth_status.in_(filters['work_auth_status']))

            if 'location' in filters and filters['location']:
                query = query.filter(CandidateProfile.location.ilike(f"%{filters['location']}%"))

            if 'salary_range' in filters and filters['salary_range']:
                salary_filter = filters['salary_range']
                # This would need more complex JSON query logic for salary expectations
                pass

        # Get all candidates (for now, we'll do matching in Python)
        all_candidates = query.all()

        # Calculate match scores
        candidates_with_scores = []
        min_match_score = matching_criteria.get('min_match_score', 60)
        skill_match_threshold = matching_criteria.get('skill_match_threshold', 70)

        for candidate in all_candidates:
            match_result = HiringMatchingService.calculate_overall_match(candidate, job_requirements)

            # Check if meets minimum thresholds
            if (match_result['match_score'] >= min_match_score and
                match_result['match_breakdown']['skills_match']['score'] >= skill_match_threshold):

                # Get recent work experience
                recent_experience = candidate.work_experience.order_by(WorkExperience.start_date.desc()).limit(3).all()

                candidates_with_scores.append({
                    'candidate': candidate,
                    'match_score': match_result['match_score'],
                    'match_breakdown': match_result['match_breakdown'],
                    'recent_experience': recent_experience
                })

        # Sort candidates
        reverse = sort_config.get('order', 'desc') == 'desc'

        if sort_config.get('field') == 'match_score':
            candidates_with_scores.sort(key=lambda x: x['match_score'], reverse=reverse)
        elif sort_config.get('field') == 'name':
            candidates_with_scores.sort(key=lambda x: x['candidate'].name, reverse=reverse)
        elif sort_config.get('field') == 'experience':
            level_order = {'entry': 1, 'mid': 2, 'senior': 3, 'lead': 4, 'principal': 5, 'executive': 6}
            candidates_with_scores.sort(
                key=lambda x: level_order.get(x['candidate'].experience_level, 0),
                reverse=reverse
            )

        # Pagination
        page = pagination.get('page', 1)
        limit = pagination.get('limit', 20)
        total = len(candidates_with_scores)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        paginated_candidates = candidates_with_scores[start_idx:end_idx]

        # Calculate search time
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return {
            'candidates': paginated_candidates,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit,
                'has_next': page * limit < total,
                'has_prev': page > 1
            },
            'search_metadata': {
                'total_matches': total,
                'search_time': search_time,
                'applied_filters': filters,
                'matching_criteria': matching_criteria
            }
        }

    @staticmethod
    def get_candidates_list(page: int = 1, limit: int = 20, sort: str = 'name',
                          order: str = 'asc') -> Dict[str, Any]:
        """Get paginated list of all candidates"""
        # Build query
        query = db.session.query(CandidateProfile)

        # Apply sorting
        if sort == 'name':
            query = query.order_by(CandidateProfile.name.asc() if order == 'asc' else CandidateProfile.name.desc())
        elif sort == 'experience':
            level_order = {'entry': 1, 'mid': 2, 'senior': 3, 'lead': 4, 'principal': 5, 'executive': 6}
            # This would need a custom sort in Python or a SQL CASE statement
            query = query.order_by(CandidateProfile.experience_level)
        elif sort == 'location':
            query = query.order_by(CandidateProfile.location.asc() if order == 'asc' else CandidateProfile.location.desc())
        elif sort == 'created_at':
            query = query.order_by(CandidateProfile.created_at.asc() if order == 'asc' else CandidateProfile.created_at.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        candidates = query.offset((page - 1) * limit).limit(limit).all()

        return {
            'candidates': candidates,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit,
                'has_next': page * limit < total,
                'has_prev': page > 1
            }
        }

    @staticmethod
    def get_job_postings_list(founder_id: str, page: int = 1, limit: int = 20,
                            status: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated list of job postings for a founder"""
        query = db.session.query(JobPosting).filter(JobPosting.founder_id == founder_id)

        if status:
            query = query.filter(JobPosting.status == status)

        query = query.order_by(JobPosting.posted_at.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        jobs = query.offset((page - 1) * limit).limit(limit).all()

        return {
            'jobs': jobs,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit,
                'has_next': page * limit < total,
                'has_prev': page > 1
            }
        }