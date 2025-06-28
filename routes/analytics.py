from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from schemas.analytics import PipelineAnalyticsSchema, MarketIntelligenceSchema
from services.analytics import get_pipeline_analytics, get_market_intelligence

bp = Blueprint('analytics', __name__)

@bp.route('/analytics/pipeline', methods=['GET'])
@require_auth
def get_pipeline_analytics_route():
    filters = request.args.to_dict()
    analytics = get_pipeline_analytics(filters)
    return jsonify(PipelineAnalyticsSchema().dump(analytics)), 200

@bp.route('/analytics/market', methods=['GET'])
@require_auth
def get_market_intelligence_route():
    filters = request.args.to_dict()
    market = get_market_intelligence(filters)
    return jsonify(MarketIntelligenceSchema().dump(market)), 200
