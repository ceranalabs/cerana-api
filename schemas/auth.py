from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class SignupRequest(BaseModel):
    email: EmailStr
    role: str

class SignupResponse(BaseModel):
    userId: str
    verificationSent: bool
    message: str

class VerifyRequest(BaseModel):
    token: str

class VerifyResponse(BaseModel):
    authToken: str
    user: Dict
    userRole: str
