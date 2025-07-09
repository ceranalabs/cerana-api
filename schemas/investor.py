from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional

class InvestmentThesisInput(BaseModel):
    stage_focus: List[str] = Field(..., alias='stageFocus')
    sector_preferences: List[str] = Field(..., alias='sectorPreferences')
    geographic_focus: str = Field(..., alias='geographicFocus')
    check_size_range: str = Field(..., alias='checkSizeRange')
    investment_style: str = Field(..., alias='investmentStyle')
    deal_flow_preference: Optional[str] = Field(None, alias='dealFlowPreference')
    due_diligence_style: Optional[str] = Field(None, alias='dueDiligenceStyle')
    value_add_areas: Optional[List[str]] = Field(None, alias='valueAddAreas')
    investments_per_year: Optional[int] = Field(None, alias='investmentsPerYear')

    class Config:
        populate_by_name = True

class InvestorProfileInput(BaseModel):
    name: str
    email: EmailStr
    firm_name: Optional[str] = Field(None, alias='firmName')
    title: Optional[str] = None
    investment_thesis: InvestmentThesisInput = Field(..., alias='investmentThesis')
    linkedin_url: Optional[HttpUrl] = Field(None, alias='linkedinUrl')
    accredited: Optional[bool] = None

    class Config:
        populate_by_name = True

class InvestmentThesisOutput(BaseModel):
    stage_focus: List[str] = Field(..., alias='stageFocus')
    sector_preferences: List[str] = Field(..., alias='sectorPreferences')
    geographic_focus: str = Field(..., alias='geographicFocus')
    check_size_range: str = Field(..., alias='checkSizeRange')
    investment_style: str = Field(..., alias='investmentStyle')
    deal_flow_preference: Optional[str] = Field(None, alias='dealFlowPreference')
    due_diligence_style: Optional[str] = Field(None, alias='dueDiligenceStyle')
    value_add_areas: Optional[List[str]] = Field(None, alias='valueAddAreas')
    investments_per_year: Optional[int] = Field(None, alias='investmentsPerYear')

    class Config:
        populate_by_name = True

class InvestorProfileOutput(BaseModel):
    id: str
    name: str
    email: EmailStr
    firm_name: Optional[str] = Field(None, alias='firmName')
    title: Optional[str] = None
    investment_thesis: InvestmentThesisOutput = Field(..., alias='investmentThesis')
    linkedin_url: Optional[HttpUrl] = Field(None, alias='linkedinUrl')
    accredited: Optional[bool] = None
    created_at: str = Field(..., alias='createdAt')
    updated_at: str = Field(..., alias='updatedAt')

    class Config:
        populate_by_name = True

# For backwards compatibility
InvestmentThesis = InvestmentThesisOutput
InvestorProfile = InvestorProfileOutput
