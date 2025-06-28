from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class MatchRecommendation(BaseModel):
    id: str
    type: str
    name: str
    title: str
    company: str
    location: str
    matchScore: int
    reasoning: List[str]
    valueAdd: str
    nextStep: str
    avatarUrl: Optional[HttpUrl] = None
    linkedinUrl: Optional[HttpUrl] = None
    expertise: Optional[List[str]] = None
