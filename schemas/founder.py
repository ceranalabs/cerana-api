from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import List, Optional

# Basic CRUD schemas for founder profiles
class FounderProfileInput(BaseModel):
    name: str
    role: str
    background: str
    experience_level: str = Field(..., alias='experienceLevel')
    location: str
    focus_areas: List[str] = Field(..., alias='focusAreas')
    linkedin_url: Optional[HttpUrl] = Field(None, alias='linkedinUrl')
    email: EmailStr
    company_name: Optional[str] = Field(None, alias='companyName')
    funding_stage: Optional[str] = Field(None, alias='fundingStage')
    title: Optional[str] = None

    class Config:
        populate_by_name = True

class FounderProfileOutput(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    background: str
    experience_level: str = Field(..., alias='experienceLevel')
    location: str
    focus_areas: List[str] = Field(..., alias='focusAreas')
    linkedin_url: Optional[HttpUrl] = Field(None, alias='linkedinUrl')
    company_name: Optional[str] = Field(None, alias='companyName')
    funding_stage: Optional[str] = Field(None, alias='fundingStage')
    title: Optional[str] = None
    created_at: str = Field(..., alias='createdAt')
    updated_at: str = Field(..., alias='updatedAt')

    class Config:
        populate_by_name = True

# For backwards compatibility
FounderProfile = FounderProfileOutput

# Discovery and detailed view schemas
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
