from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.pipeline import PipelineDealSchema, DetailedPipelineDealSchema, AddToPipelineInputSchema, UpdatePipelineDealInputSchema
from services.pipeline import get_pipeline, add_to_pipeline, get_pipeline_deal, update_pipeline_deal

bp = Blueprint('pipeline', __name__)

# In-memory store for MVP
pipeline = {}

@bp.route('/pipeline', methods=['GET'])
@require_auth
def get_pipeline_route():
    filters = request.args.to_dict()
    deals = get_pipeline(filters, pipeline)
    return jsonify([PipelineDealSchema().dump(deal) for deal in deals]), 200

@bp.route('/pipeline', methods=['POST'])
@require_auth
def add_to_pipeline_route():
    data = request.get_json()
    validated = AddToPipelineInputSchema().load(data)
    deal = add_to_pipeline(validated, pipeline)
    return jsonify(PipelineDealSchema().dump(deal)), 201

@bp.route('/pipeline/<deal_id>', methods=['GET'])
@require_auth
def get_pipeline_deal_route(deal_id):
    deal = get_pipeline_deal(deal_id, pipeline)
    if not deal:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(DetailedPipelineDealSchema().dump(deal)), 200

@bp.route('/pipeline/<deal_id>', methods=['PUT'])
@require_auth
def update_pipeline_deal_route(deal_id):
    data = request.get_json()
    validated = UpdatePipelineDealInputSchema().load(data)
    deal = update_pipeline_deal(deal_id, validated, pipeline)
    if not deal:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(PipelineDealSchema().dump(deal)), 200
