from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class TractionHighlights(BaseModel):
    revenue: Optional[str] = None
    growth: Optional[str] = None
    customers: Optional[str] = None
    retention: Optional[str] = None
    partnerships: Optional[str] = None

class FounderDiscoveryCard(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    companyName: str
    matchScore: int
    problemStatement: Optional[str] = None
    fundingStage: Optional[str] = None
    raisingAmount: Optional[str] = None
    location: Optional[str] = None
    traction: Optional[TractionHighlights] = None
    whyThisFits: Optional[List[str]] = None
    riskFlags: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    avatarUrl: Optional[HttpUrl] = None
    lastUpdated: Optional[str] = None

class TeamMember(BaseModel):
    name: str
    title: str
    background: str
    linkedinUrl: Optional[HttpUrl] = None

class FundraisingDetails(BaseModel):
    stage: str
    targetAmount: float
    currentCommitments: Optional[float] = None
    valuation: Optional[float] = None
    useOfFunds: str
    timeline: Optional[str] = None
    leadInvestor: Optional[str] = None

class Reference(BaseModel):
    name: str
    title: str
    company: Optional[str] = None
    relationship: str
    contactInfo: Optional[str] = None

class FounderDocument(BaseModel):
    id: str
    name: str
    type: str
    url: HttpUrl
    uploadedAt: Optional[str] = None

class DetailedFounderProfile(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    companyName: str
    background: Optional[str] = None
    experienceLevel: Optional[str] = None
    location: Optional[str] = None
    linkedinUrl: Optional[HttpUrl] = None
    startupIdea: Optional[dict] = None
    traction: Optional[dict] = None
    team: Optional[List[TeamMember]] = None
    fundraising: Optional[FundraisingDetails] = None
    references: Optional[List[Reference]] = None
    documents: Optional[List[FounderDocument]] = None
