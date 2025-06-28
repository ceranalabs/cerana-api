from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.investor import InvestorProfileInput, InvestorProfile as InvestorProfileSchema
from models import InvestorProfile, User
from db import db
import uuid
from datetime import datetime

bp = Blueprint('investor', __name__)

@bp.route('/investors', methods=['POST'])
@require_auth
def create_update_investor():
    data = request.get_json() or {}
    if 'linkedinUrl' in data and (data['linkedinUrl'] is None or str(data['linkedinUrl']).strip() == ''):
        del data['linkedinUrl']
    req = InvestorProfileInput.model_validate(data)
    user = User.query.get(request.user_id)
    if not user:
        user = User(id=request.user_id, email=req.email, role='investor')
        db.session.add(user)
    investor = InvestorProfile.query.get(request.user_id)
    thesis = req.investmentThesis
    if not investor:
        investor = InvestorProfile(
            id=request.user_id,
            name=req.name,
            email=req.email,
            firm_name=req.firmName,
            title=req.title,
            stage_focus=thesis.stageFocus,
            sector_preferences=thesis.sectorPreferences,
            geographic_focus=thesis.geographicFocus,
            check_size_range=thesis.checkSizeRange,
            investment_style=thesis.investmentStyle,
            deal_flow_preference=thesis.dealFlowPreference,
            due_diligence_style=thesis.dueDiligenceStyle,
            value_add_areas=thesis.valueAddAreas,
            investments_per_year=thesis.investmentsPerYear,
            linkedin_url=req.linkedinUrl,
            accredited=req.accredited,
        )
        db.session.add(investor)
    else:
        investor.name = req.name
        investor.email = req.email
        investor.firm_name = req.firmName
        investor.title = req.title
        investor.stage_focus = thesis.stageFocus
        investor.sector_preferences = thesis.sectorPreferences
        investor.geographic_focus = thesis.geographicFocus
        investor.check_size_range = thesis.checkSizeRange
        investor.investment_style = thesis.investmentStyle
        investor.deal_flow_preference = thesis.dealFlowPreference
        investor.due_diligence_style = thesis.dueDiligenceStyle
        investor.value_add_areas = thesis.valueAddAreas
        investor.investments_per_year = thesis.investmentsPerYear
        investor.linkedin_url = req.linkedinUrl
        investor.accredited = req.accredited
    db.session.commit()
    return jsonify(InvestorProfileSchema(
        id=investor.id,
        name=investor.name,
        email=investor.email,
        firmName=investor.firm_name,
        title=investor.title,
        investmentThesis={
            'stageFocus': investor.stage_focus,
            'sectorPreferences': investor.sector_preferences,
            'geographicFocus': investor.geographic_focus,
            'checkSizeRange': investor.check_size_range,
            'investmentStyle': investor.investment_style,
            'dealFlowPreference': investor.deal_flow_preference,
            'dueDiligenceStyle': investor.due_diligence_style,
            'valueAddAreas': investor.value_add_areas,
            'investmentsPerYear': investor.investments_per_year
        },
        linkedinUrl=investor.linkedin_url,
        accredited=investor.accredited,
        createdAt=investor.created_at.isoformat() if investor.created_at else None,
        updatedAt=investor.updated_at.isoformat() if investor.updated_at else None
    ).model_dump(mode="json")), 201

@bp.route('/investors/<investor_id>', methods=['GET'])
@require_auth
def get_investor_profile(investor_id):
    investor = InvestorProfile.query.get(investor_id)
    if not investor:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(InvestorProfileSchema(
        id=investor.id,
        name=investor.name,
        email=investor.email,
        firmName=investor.firm_name,
        title=investor.title,
        investmentThesis={
            'stageFocus': investor.stage_focus,
            'sectorPreferences': investor.sector_preferences,
            'geographicFocus': investor.geographic_focus,
            'checkSizeRange': investor.check_size_range,
            'investmentStyle': investor.investment_style,
            'dealFlowPreference': investor.deal_flow_preference,
            'dueDiligenceStyle': investor.due_diligence_style,
            'valueAddAreas': investor.value_add_areas,
            'investmentsPerYear': investor.investments_per_year
        },
        linkedinUrl=investor.linkedin_url,
        accredited=investor.accredited,
        createdAt=investor.created_at.isoformat() if investor.created_at else None,
        updatedAt=investor.updated_at.isoformat() if investor.updated_at else None
    ).model_dump(mode="json")), 200

@bp.route('/investors/<investor_id>', methods=['PUT'])
@require_auth
def update_investor_profile(investor_id):
    data = request.get_json() or {}
    if 'linkedinUrl' in data and (data['linkedinUrl'] is None or str(data['linkedinUrl']).strip() == ''):
        del data['linkedinUrl']
    req = InvestorProfileInput.model_validate(data)
    investor = InvestorProfile.query.get(investor_id)
    user = User.query.get(investor_id)
    if not user:
        user = User(id=investor_id, email=req.email, role='investor')
        db.session.add(user)
    if not investor:
        thesis = req.investmentThesis
        investor = InvestorProfile(
            id=investor_id,
            name=req.name,
            email=req.email,
            firm_name=req.firmName,
            title=req.title,
            stage_focus=thesis.stageFocus,
            sector_preferences=thesis.sectorPreferences,
            geographic_focus=thesis.geographicFocus,
            check_size_range=thesis.checkSizeRange,
            investment_style=thesis.investmentStyle,
            deal_flow_preference=thesis.dealFlowPreference,
            due_diligence_style=thesis.dueDiligenceStyle,
            value_add_areas=thesis.valueAddAreas,
            investments_per_year=thesis.investmentsPerYear,
            linkedin_url=req.linkedinUrl,
            accredited=req.accredited,
        )
        db.session.add(investor)
    else:
        thesis = req.investmentThesis
        investor.name = req.name
        investor.email = req.email
        investor.firm_name = req.firmName
        investor.title = req.title
        investor.stage_focus = thesis.stageFocus
        investor.sector_preferences = thesis.sectorPreferences
        investor.geographic_focus = thesis.geographicFocus
        investor.check_size_range = thesis.checkSizeRange
        investor.investment_style = thesis.investmentStyle
        investor.deal_flow_preference = thesis.dealFlowPreference
        investor.due_diligence_style = thesis.dueDiligenceStyle
        investor.value_add_areas = thesis.valueAddAreas
        investor.investments_per_year = thesis.investmentsPerYear
        investor.linkedin_url = req.linkedinUrl
        investor.accredited = req.accredited
    db.session.commit()
    return jsonify(InvestorProfileSchema(
        id=investor.id,
        name=investor.name,
        email=investor.email,
        firmName=investor.firm_name,
        title=investor.title,
        investmentThesis={
            'stageFocus': investor.stage_focus,
            'sectorPreferences': investor.sector_preferences,
            'geographicFocus': investor.geographic_focus,
            'checkSizeRange': investor.check_size_range,
            'investmentStyle': investor.investment_style,
            'dealFlowPreference': investor.deal_flow_preference,
            'dueDiligenceStyle': investor.due_diligence_style,
            'valueAddAreas': investor.value_add_areas,
            'investmentsPerYear': investor.investments_per_year
        },
        linkedinUrl=investor.linkedin_url,
        accredited=investor.accredited,
        createdAt=investor.created_at.isoformat() if investor.created_at else None,
        updatedAt=investor.updated_at.isoformat() if investor.updated_at else None
    ).model_dump(mode="json")), 200
