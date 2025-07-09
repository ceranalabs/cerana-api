from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.pipeline import PipelineDealOutput, DetailedPipelineDealOutput, AddToPipelineInput, UpdatePipelineDealInput
from services.pipeline import get_pipeline, add_to_pipeline, get_pipeline_deal, update_pipeline_deal

bp = Blueprint('pipeline', __name__)

@bp.route('/pipeline', methods=['GET'])
@require_auth
def get_pipeline_route():
    filters = request.args.to_dict()
    deals = get_pipeline(filters, request.user_id)
    return jsonify(deals), 200

@bp.route('/pipeline', methods=['POST'])
@require_auth
def add_to_pipeline_route():
    data = request.get_json()
    validated = AddToPipelineInput.model_validate(data)
    deal = add_to_pipeline(validated, request.user_id)
    return jsonify(deal), 201

@bp.route('/pipeline/<deal_id>', methods=['GET'])
@require_auth
def get_pipeline_deal_route(deal_id):
    deal = get_pipeline_deal(deal_id, request.user_id)
    if not deal:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(deal), 200

@bp.route('/pipeline/<deal_id>', methods=['PUT'])
@require_auth
def update_pipeline_deal_route(deal_id):
    data = request.get_json()
    validated = UpdatePipelineDealInput.model_validate(data)
    deal = update_pipeline_deal(deal_id, validated.model_dump(exclude_none=True), request.user_id)
    if not deal:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(deal), 200
