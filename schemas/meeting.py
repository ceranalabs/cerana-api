from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class MeetingRequestInput(BaseModel):
    founderId: str
    meetingType: str
    preferredTimes: List[str]
    duration: Optional[int] = 30
    agenda: Optional[str] = None
    customMessage: Optional[str] = None

class MeetingRequest(BaseModel):
    id: str
    founderId: str
    founderName: Optional[str] = None
    companyName: Optional[str] = None
    meetingType: str
    scheduledAt: Optional[str] = None
    duration: Optional[int] = None
    status: str
    agenda: Optional[str] = None
    notes: Optional[str] = None
    meetingUrl: Optional[HttpUrl] = None
    requestedAt: str
