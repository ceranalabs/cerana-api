from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AddToPipelineInput(BaseModel):
    founder_id: str = Field(..., alias='founderId')

    class Config:
        populate_by_name = True

class UpdatePipelineDealInput(BaseModel):
    stage: Optional[str] = None
    status: Optional[str] = None
    next_action: Optional[str] = Field(None, alias='nextAction')
    next_action_due: Optional[datetime] = Field(None, alias='nextActionDue')
    match_score: Optional[int] = Field(None, alias='matchScore')
    key_metrics: Optional[Dict[str, Any]] = Field(None, alias='keyMetrics')
    risk_flags: Optional[List[str]] = Field(None, alias='riskFlags')
    opportunities: Optional[List[str]] = None
    notes: Optional[List[str]] = None

    class Config:
        populate_by_name = True

class PipelineDealOutput(BaseModel):
    id: str
    investor_id: str = Field(..., alias='investorId')
    founder_id: str = Field(..., alias='founderId')
    founder_name: Optional[str] = Field(None, alias='founderName')
    company_name: Optional[str] = Field(None, alias='companyName')
    stage: str
    status: str
    next_action: Optional[str] = Field(None, alias='nextAction')
    next_action_due: Optional[str] = Field(None, alias='nextActionDue')
    match_score: Optional[int] = Field(None, alias='matchScore')
    key_metrics: Optional[Dict[str, Any]] = Field(None, alias='keyMetrics')
    risk_flags: Optional[List[str]] = Field(None, alias='riskFlags')
    opportunities: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    added_at: str = Field(..., alias='addedAt')
    updated_at: str = Field(..., alias='updatedAt')

    class Config:
        populate_by_name = True

class DetailedPipelineDealOutput(PipelineDealOutput):
    # Add additional fields that might be needed for detailed view
    pass

# For backwards compatibility
PipelineDealSchema = PipelineDealOutput
DetailedPipelineDealSchema = DetailedPipelineDealOutput
AddToPipelineInputSchema = AddToPipelineInput
UpdatePipelineDealInputSchema = UpdatePipelineDealInput
