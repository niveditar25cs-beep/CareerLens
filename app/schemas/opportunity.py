from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    opportunity_type: Optional[str] = "other"
    category: Optional[str] = None
    skills_required: Optional[str] = None
    application_url: Optional[str] = None
    deadline: Optional[datetime] = None
    source: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    opportunity_type: Optional[str] = None
    category: Optional[str] = None
    skills_required: Optional[str] = None
    application_url: Optional[str] = None
    deadline: Optional[datetime] = None


class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
