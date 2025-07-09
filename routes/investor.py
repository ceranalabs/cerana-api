from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.investor import InvestorProfileInput, InvestorProfile as InvestorProfileSchema
from schemas import investor_profile_to_dict
from models import InvestorProfile, User
from db import db
import uuid
from datetime import datetime

bp = Blueprint('investor', __name__)

@bp.route('/investors', methods=['GET'])
@require_auth
def list_investors():
    """Get list of all investors with optional filtering"""
    # Get query parameters for filtering
    firm_name = request.args.get('firmName')
    geographic_focus = request.args.get('geographicFocus')
    investment_style = request.args.get('investmentStyle')
    stage_focus = request.args.get('stageFocus')
    limit = request.args.get('limit', type=int)

    # Build query
    query = InvestorProfile.query

    # Apply filters if provided
    if firm_name:
        query = query.filter(InvestorProfile.firm_name.ilike(f'%{firm_name}%'))
    if geographic_focus:
        query = query.filter_by(geographic_focus=geographic_focus)
    if investment_style:
        query = query.filter_by(investment_style=investment_style)
    if stage_focus:
        query = query.filter(InvestorProfile.stage_focus.contains([stage_focus]))

    # Apply limit if provided
    if limit:
        query = query.limit(limit)

    investors = query.all()
    result = [investor_profile_to_dict(investor) for investor in investors]

    return jsonify(result), 200

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
    thesis = req.investment_thesis
    if not investor:
        investor = InvestorProfile(
            id=request.user_id,
            name=req.name,
            email=req.email,
            firm_name=req.firm_name,
            title=req.title,
            stage_focus=thesis.stage_focus,
            sector_preferences=thesis.sector_preferences,
            geographic_focus=thesis.geographic_focus,
            check_size_range=thesis.check_size_range,
            investment_style=thesis.investment_style,
            deal_flow_preference=thesis.deal_flow_preference,
            due_diligence_style=thesis.due_diligence_style,
            value_add_areas=thesis.value_add_areas,
            investments_per_year=thesis.investments_per_year,
            linkedin_url=req.linkedin_url,
            accredited=req.accredited,
        )
        db.session.add(investor)
    else:
        investor.name = req.name
        investor.email = req.email
        investor.firm_name = req.firm_name
        investor.title = req.title
        investor.stage_focus = thesis.stage_focus
        investor.sector_preferences = thesis.sector_preferences
        investor.geographic_focus = thesis.geographic_focus
        investor.check_size_range = thesis.check_size_range
        investor.investment_style = thesis.investment_style
        investor.deal_flow_preference = thesis.deal_flow_preference
        investor.due_diligence_style = thesis.due_diligence_style
        investor.value_add_areas = thesis.value_add_areas
        investor.investments_per_year = thesis.investments_per_year
        investor.linkedin_url = req.linkedin_url
        investor.accredited = req.accredited
    db.session.commit()
    return jsonify(investor_profile_to_dict(investor)), 201

@bp.route('/investors/<investor_id>', methods=['GET'])
@require_auth
def get_investor_profile(investor_id):
    investor = InvestorProfile.query.get(investor_id)
    if not investor:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(investor_profile_to_dict(investor)), 200

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
        thesis = req.investment_thesis
        investor = InvestorProfile(
            id=investor_id,
            name=req.name,
            email=req.email,
            firm_name=req.firm_name,
            title=req.title,
            stage_focus=thesis.stage_focus,
            sector_preferences=thesis.sector_preferences,
            geographic_focus=thesis.geographic_focus,
            check_size_range=thesis.check_size_range,
            investment_style=thesis.investment_style,
            deal_flow_preference=thesis.deal_flow_preference,
            due_diligence_style=thesis.due_diligence_style,
            value_add_areas=thesis.value_add_areas,
            investments_per_year=thesis.investments_per_year,
            linkedin_url=req.linkedin_url,
            accredited=req.accredited,
        )
        db.session.add(investor)
    else:
        thesis = req.investment_thesis
        investor.name = req.name
        investor.email = req.email
        investor.firm_name = req.firm_name
        investor.title = req.title
        investor.stage_focus = thesis.stage_focus
        investor.sector_preferences = thesis.sector_preferences
        investor.geographic_focus = thesis.geographic_focus
        investor.check_size_range = thesis.check_size_range
        investor.investment_style = thesis.investment_style
        investor.deal_flow_preference = thesis.deal_flow_preference
        investor.due_diligence_style = thesis.due_diligence_style
        investor.value_add_areas = thesis.value_add_areas
        investor.investments_per_year = thesis.investments_per_year
        investor.linkedin_url = req.linkedin_url
        investor.accredited = req.accredited
    db.session.commit()
    return jsonify(investor_profile_to_dict(investor)), 200
