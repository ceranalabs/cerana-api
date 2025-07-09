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
