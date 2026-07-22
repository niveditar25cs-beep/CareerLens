from pydantic import BaseModel
from datetime import datetime
from app.schemas.opportunity import OpportunityResponse


class SavedOpportunityBase(BaseModel):
    opportunity_id: int


class SavedOpportunityCreate(SavedOpportunityBase):
    pass


class SavedOpportunityResponse(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    saved_at: datetime
    opportunity: OpportunityResponse | None = None

    class Config:
        from_attributes = True
