from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Optional

class FounderProfileInput(BaseModel):
    name: str
    role: str
    background: str
    experienceLevel: str
    location: str
    focusAreas: List[str]
    linkedinUrl: Optional[HttpUrl] = None
    email: EmailStr
    companyName: Optional[str] = None
    fundingStage: Optional[str] = None
    title: Optional[str] = None

class FounderProfile(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    background: str
    experienceLevel: str
    location: str
    focusAreas: List[str]
    linkedinUrl: Optional[HttpUrl] = None
    companyName: Optional[str] = None
    fundingStage: Optional[str] = None
    title: Optional[str] = None
    createdAt: str
    updatedAt: str
