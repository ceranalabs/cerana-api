from pydantic import BaseModel
from typing import List, Dict, Optional

class PipelineAnalytics(BaseModel):
    overview: Optional[Dict] = None
    stageBreakdown: Optional[List[Dict]] = None
    sectorPerformance: Optional[List[Dict]] = None
    monthlyTrends: Optional[List[Dict]] = None

class MarketIntelligence(BaseModel):
    sectorTrends: Optional[List[Dict]] = None
    competitiveLandscape: Optional[List[Dict]] = None
    fundingTrends: Optional[Dict] = None
