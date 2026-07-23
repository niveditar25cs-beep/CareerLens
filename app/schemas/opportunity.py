from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = None
    company: Optional[str] = None
    company_logo: Optional[str] = None
    location: Optional[str] = None
    opportunity_type: Optional[str] = "other"
    employment_type: Optional[str] = "other"
    experience_required: Optional[str] = None
    salary: Optional[str] = None
    category: Optional[str] = None
    skills_required: Optional[str] = None
    eligibility: Optional[str] = None
    application_url: Optional[str] = None
    original_url: Optional[str] = None
    deadline: Optional[datetime] = None
    posted_date: Optional[datetime] = None
    source: Optional[str] = None
    status: Optional[str] = "active"


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    company_logo: Optional[str] = None
    location: Optional[str] = None
    opportunity_type: Optional[str] = None
    employment_type: Optional[str] = None
    experience_required: Optional[str] = None
    salary: Optional[str] = None
    category: Optional[str] = None
    skills_required: Optional[str] = None
    eligibility: Optional[str] = None
    application_url: Optional[str] = None
    original_url: Optional[str] = None
    deadline: Optional[datetime] = None
    posted_date: Optional[datetime] = None
    source: Optional[str] = None
    status: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
