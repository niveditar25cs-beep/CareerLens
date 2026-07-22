from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class OpportunityType(str, enum.Enum):
    INTERNSHIP = "internship"
    JOB = "job"
    SCHOLARSHIP = "scholarship"
    COMPETITION = "competition"
    WORKSHOP = "workshop"
    OTHER = "other"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    opportunity_type = Column(Enum(OpportunityType), default=OpportunityType.OTHER)
    category = Column(String(100), nullable=True)
    skills_required = Column(Text, nullable=True)
    application_url = Column(String(500), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
