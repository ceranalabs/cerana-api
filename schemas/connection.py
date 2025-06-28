from pydantic import BaseModel
from typing import Optional

class ConnectionRequestInput(BaseModel):
    matchId: str
    customMessage: Optional[str] = None

class ConnectionRequest(BaseModel):
    id: str
    founderId: str
    matchId: str
    matchType: str
    customMessage: Optional[str] = None
    status: str
    requestedAt: str
    respondedAt: Optional[str] = None
