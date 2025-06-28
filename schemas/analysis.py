from pydantic import BaseModel
from typing import List, Dict

class AnalysisResult(BaseModel):
    id: str
    ideaId: str
    extractedInsights: Dict
    advisorMatches: List[Dict]
    designPartnerMatches: List[Dict]
    customerMatches: List[Dict]
    processedAt: str
