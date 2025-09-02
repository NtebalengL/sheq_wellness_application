# models.py
# Pydantic models for request/response validation

from pydantic import BaseModel, Field
from typing import Optional, List

# --- Ask endpoint ---
class AskRequest(BaseModel):
    text: str = Field(..., min_length=3, description="User question text")
    user_id: Optional[str] = None
    channel: Optional[str] = "web"

class AskResponse(BaseModel):
    answer: str
    source: str
    confidence: float
    escalate: Optional[bool] = False

# --- Resources endpoint ---
class ResourceItem(BaseModel):
    name: str
    type: str
    phone: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None

# --- Authentication endpoints ---
class AuthRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
