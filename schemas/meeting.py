from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeetingRequestInput(BaseModel):
    founder_id: str = Field(..., alias='founderId')
    meeting_type: str = Field(..., alias='meetingType')
    duration: Optional[int] = 30
    agenda: Optional[str] = None
    custom_message: Optional[str] = Field(None, alias='customMessage')

    class Config:
        populate_by_name = True

class MeetingRequestOutput(BaseModel):
    id: str
    founder_id: str = Field(..., alias='founderId')
    founder_name: Optional[str] = Field(None, alias='founderName')
    company_name: Optional[str] = Field(None, alias='companyName')
    meeting_type: str = Field(..., alias='meetingType')
    scheduled_at: Optional[str] = Field(None, alias='scheduledAt')
    duration: Optional[int] = None
    status: str
    agenda: Optional[str] = None
    notes: Optional[str] = None
    meeting_url: Optional[str] = Field(None, alias='meetingUrl')
    requested_at: Optional[str] = Field(None, alias='requestedAt')

    class Config:
        populate_by_name = True

# For backwards compatibility
MeetingRequestInput = MeetingRequestInput
MeetingRequest = MeetingRequestOutput
