import uuid
from datetime import datetime

analyses = {}

def start_analysis(idea_id):
    analysis_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    result = {
        'id': analysis_id,
        'ideaId': idea_id,
        'extractedInsights': {
            'problemClarity': 90,
            'targetSegments': ['SMBs', 'Finance Teams'],
            'competitiveLandscape': ['Competitor A', 'Competitor B'],
            'technologyRequirements': ['AI/ML', 'OCR'],
            'teamNeeds': ['Tech Lead'],
            'marketSizeIndicators': ['Large TAM'],
            'fundingStage': 'seed'
        },
        'advisorMatches': [],
        'designPartnerMatches': [],
        'customerMatches': [],
        'processedAt': now
    }
    analyses[analysis_id] = result
    return analysis_id, result

def get_analysis(analysis_id):
    return analyses.get(analysis_id)
