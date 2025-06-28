from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class InvestmentThesisInput(BaseModel):
    stageFocus: List[str]
    sectorPreferences: List[str]
    geographicFocus: str
    checkSizeRange: str
    investmentStyle: str
    dealFlowPreference: Optional[str] = None
    dueDiligenceStyle: Optional[str] = None
    valueAddAreas: Optional[List[str]] = None
    investmentsPerYear: Optional[int] = None

class InvestorProfileInput(BaseModel):
    name: str
    email: EmailStr
    firmName: Optional[str] = None
    title: Optional[str] = None
    investmentThesis: InvestmentThesisInput
    linkedinUrl: Optional[HttpUrl] = None
    accredited: Optional[bool] = None

class InvestmentThesis(InvestmentThesisInput):
    pass

class InvestorProfile(BaseModel):
    id: str
    name: str
    email: EmailStr
    firmName: Optional[str] = None
    title: Optional[str] = None
    investmentThesis: InvestmentThesis
    linkedinUrl: Optional[HttpUrl] = None
    accredited: Optional[bool] = None
    createdAt: str
    updatedAt: str
