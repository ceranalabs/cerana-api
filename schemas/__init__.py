from typing import Dict, Any, List, Optional
from datetime import datetime

def model_to_dict(model) -> Dict[str, Any]:
    """Convert SQLAlchemy model to dictionary"""
    if model is None:
        return {}

    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, datetime):
            result[column.name] = value.isoformat()
        else:
            result[column.name] = value
    return result

def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO string"""
    return dt.isoformat() if dt else None

# Helper functions for common conversions
def founder_profile_to_dict(founder_profile) -> Dict[str, Any]:
    """Convert FounderProfile model to API response dict"""
    if not founder_profile:
        return {}

    return {
        'id': founder_profile.id,
        'name': founder_profile.name,
        'email': founder_profile.email,
        'role': founder_profile.role,
        'background': founder_profile.background,
        'experienceLevel': founder_profile.experience_level,
        'location': founder_profile.location,
        'focusAreas': founder_profile.focus_areas,
        'linkedinUrl': founder_profile.linkedin_url,
        'companyName': founder_profile.company_name,
        'fundingStage': founder_profile.funding_stage,
        'title': founder_profile.title,
        'createdAt': format_datetime(founder_profile.created_at),
        'updatedAt': format_datetime(founder_profile.updated_at)
    }

def investor_profile_to_dict(investor_profile) -> Dict[str, Any]:
    """Convert InvestorProfile model to API response dict"""
    if not investor_profile:
        return {}

    return {
        'id': investor_profile.id,
        'name': investor_profile.name,
        'email': investor_profile.email,
        'firmName': investor_profile.firm_name,
        'title': investor_profile.title,
        'investmentThesis': {
            'stageFocus': investor_profile.stage_focus,
            'sectorPreferences': investor_profile.sector_preferences,
            'geographicFocus': investor_profile.geographic_focus,
            'checkSizeRange': investor_profile.check_size_range,
            'investmentStyle': investor_profile.investment_style,
            'dealFlowPreference': investor_profile.deal_flow_preference,
            'dueDiligenceStyle': investor_profile.due_diligence_style,
            'valueAddAreas': investor_profile.value_add_areas,
            'investmentsPerYear': investor_profile.investments_per_year
        },
        'linkedinUrl': investor_profile.linkedin_url,
        'accredited': investor_profile.accredited,
        'createdAt': format_datetime(investor_profile.created_at),
        'updatedAt': format_datetime(investor_profile.updated_at)
    }

def pipeline_deal_to_dict(pipeline_deal) -> Dict[str, Any]:
    """Convert PipelineDeal model to API response dict"""
    if not pipeline_deal:
        return {}

    return {
        'id': pipeline_deal.id,
        'investorId': pipeline_deal.investor_id,
        'founderId': pipeline_deal.founder_id,
        'founderName': pipeline_deal.founder_name,
        'companyName': pipeline_deal.company_name,
        'stage': pipeline_deal.stage,
        'status': pipeline_deal.status,
        'nextAction': pipeline_deal.next_action,
        'nextActionDue': format_datetime(pipeline_deal.next_action_due),
        'matchScore': pipeline_deal.match_score,
        'keyMetrics': pipeline_deal.key_metrics,
        'riskFlags': pipeline_deal.risk_flags,
        'opportunities': pipeline_deal.opportunities,
        'notes': pipeline_deal.notes,
        'addedAt': format_datetime(pipeline_deal.added_at),
        'updatedAt': format_datetime(pipeline_deal.updated_at)
    }

def meeting_to_dict(meeting) -> Dict[str, Any]:
    """Convert Meeting model to API response dict"""
    if not meeting:
        return {}

    return {
        'id': meeting.id,
        'founderId': meeting.founder_id,
        'founderName': meeting.founder_name,
        'companyName': meeting.company_name,
        'meetingType': meeting.meeting_type,
        'scheduledAt': format_datetime(meeting.scheduled_at),
        'duration': meeting.duration,
        'status': meeting.status,
        'agenda': meeting.agenda,
        'notes': meeting.notes,
        'meetingUrl': meeting.meeting_url,
        'requestedAt': format_datetime(meeting.requested_at)
    }

# Hiring Platform Helper Functions
def work_experience_to_dict(work_experience) -> Dict[str, Any]:
    """Convert WorkExperience model to API response dict"""
    if not work_experience:
        return {}

    return {
        'id': work_experience.id,
        'title': work_experience.title,
        'company': work_experience.company,
        'roleDescription': work_experience.role_description,
        'startDate': work_experience.start_date.isoformat() if work_experience.start_date else None,
        'endDate': work_experience.end_date.isoformat() if work_experience.end_date else None,
        'isCurrent': work_experience.is_current,
        'skills': work_experience.skills or []
    }

def education_to_dict(education) -> Dict[str, Any]:
    """Convert Education model to API response dict"""
    if not education:
        return {}

    return {
        'id': education.id,
        'degree': education.degree,
        'institution': education.institution,
        'fieldOfStudy': education.field_of_study,
        'graduationYear': education.graduation_year,
        'gpa': education.gpa
    }

def candidate_profile_to_dict(candidate_profile) -> Dict[str, Any]:
    """Convert CandidateProfile model to API response dict"""
    if not candidate_profile:
        return {}

    return {
        'id': candidate_profile.id,
        'name': candidate_profile.name,
        'email': candidate_profile.email,
        'phone': candidate_profile.phone,
        'location': candidate_profile.location,
        'workAuthStatus': candidate_profile.work_auth_status,
        'availability': candidate_profile.availability,
        'employmentStatus': candidate_profile.employment_status,
        'salaryExpectations': candidate_profile.salary_expectations,
        'skills': candidate_profile.skills or [],
        'experienceLevel': candidate_profile.experience_level,
        'createdAt': format_datetime(candidate_profile.created_at),
        'updatedAt': format_datetime(candidate_profile.updated_at)
    }

def detailed_candidate_profile_to_dict(candidate_profile) -> Dict[str, Any]:
    """Convert CandidateProfile model to detailed API response dict"""
    if not candidate_profile:
        return {}

    # Start with basic profile
    result = candidate_profile_to_dict(candidate_profile)

    # Add detailed fields
    result.update({
        'workExperience': [work_experience_to_dict(exp) for exp in candidate_profile.work_experience],
        'bio': candidate_profile.bio,
        'linkedinUrl': candidate_profile.linkedin_url,
        'portfolioUrl': candidate_profile.portfolio_url,
        'education': [education_to_dict(edu) for edu in candidate_profile.education],
        'certifications': candidate_profile.certifications or []
    })

    return result

def job_posting_to_dict(job_posting) -> Dict[str, Any]:
    """Convert JobPosting model to API response dict"""
    if not job_posting:
        return {}

    return {
        'id': job_posting.id,
        'founderId': job_posting.founder_id,
        'title': job_posting.title,
        'jobDescription': job_posting.job_description,
        'requiredSkills': job_posting.required_skills or [],
        'preferredSkills': job_posting.preferred_skills or [],
        'experienceLevel': job_posting.experience_level,
        'location': job_posting.location,
        'isRemote': job_posting.is_remote,
        'salaryRange': job_posting.salary_range,
        'equity': job_posting.equity,
        'employmentType': job_posting.employment_type,
        'department': job_posting.department,
        'team': job_posting.team,
        'status': job_posting.status,
        'postedAt': format_datetime(job_posting.posted_at),
        'updatedAt': format_datetime(job_posting.updated_at)
    }

def saved_search_to_dict(saved_search) -> Dict[str, Any]:
    """Convert SavedSearch model to API response dict"""
    if not saved_search:
        return {}

    return {
        'id': saved_search.id,
        'founderId': saved_search.founder_id,
        'name': saved_search.name,
        'searchCriteria': saved_search.search_criteria,
        'createdAt': format_datetime(saved_search.created_at),
        'lastUsed': format_datetime(saved_search.last_used)
    }

def create_pagination_dict(page: int, limit: int, total: int) -> Dict[str, Any]:
    """Create pagination metadata dict"""
    total_pages = (total + limit - 1) // limit  # Ceiling division
    return {
        'page': page,
        'limit': limit,
        'total': total,
        'totalPages': total_pages,
        'hasNext': page < total_pages,
        'hasPrev': page > 1
    }
