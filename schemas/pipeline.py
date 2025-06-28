from pydantic import BaseModel
from typing import List, Optional
from schemas.founder import TractionHighlights, FounderDocument, DetailedFounderProfile

class DealNote(BaseModel):
    id: str
    content: str
    author: str
    createdAt: str

class PipelineDeal(BaseModel):
    id: str
    founderId: str
    founderName: Optional[str] = None
    companyName: Optional[str] = None
    stage: str
    status: str
    daysInStage: Optional[int] = None
    nextAction: Optional[str] = None
    nextActionDue: Optional[str] = None
    matchScore: Optional[int] = None
    keyMetrics: Optional[TractionHighlights] = None
    riskFlags: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    notes: Optional[List[DealNote]] = None
    addedAt: Optional[str] = None
    updatedAt: Optional[str] = None

class DetailedPipelineDeal(PipelineDeal):
    founderProfile: Optional[DetailedFounderProfile] = None
    meetings: Optional[List[dict]] = None
    documents: Optional[List[FounderDocument]] = None

class AddToPipelineInput(BaseModel):
    founderId: str
    initialStage: Optional[str] = None
    notes: Optional[str] = None

class UpdatePipelineDealInput(BaseModel):
    stage: Optional[str] = None
    status: Optional[str] = None
    nextAction: Optional[str] = None
    nextActionDue: Optional[str] = None
    notes: Optional[str] = None

PipelineDealSchema = PipelineDeal
DetailedPipelineDealSchema = DetailedPipelineDeal
AddToPipelineInputSchema = AddToPipelineInput
UpdatePipelineDealInputSchema = UpdatePipelineDealInput
