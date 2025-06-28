from pydantic import BaseModel
from typing import Optional

class StartupIdeaInput(BaseModel):
    coreProblems: str
    targetCustomer: str
    proposedSolution: str
    industry: Optional[str] = None
    marketOpportunity: Optional[str] = None
    uniqueInsight: Optional[str] = None
    technologyApproach: Optional[str] = None
    technicalComplexity: Optional[str] = None
    businessModel: Optional[str] = None
    revenueModel: Optional[str] = None

class StartupIdea(BaseModel):
    id: str
    founderId: str
    coreProblems: str
    targetCustomer: str
    proposedSolution: str
    industry: Optional[str] = None
    marketOpportunity: Optional[str] = None
    uniqueInsight: Optional[str] = None
    technologyApproach: Optional[str] = None
    technicalComplexity: Optional[str] = None
    businessModel: Optional[str] = None
    revenueModel: Optional[str] = None
    completenessScore: int
    createdAt: str
    updatedAt: str
