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


class EmploymentType(str, enum.Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    TEMPORARY = "temporary"
    OTHER = "other"


class JobStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    company = Column(String(255), nullable=True)
    company_logo = Column(String(500), nullable=True)
    location = Column(String(255), nullable=True)
    opportunity_type = Column(Enum(OpportunityType), default=OpportunityType.OTHER)
    employment_type = Column(Enum(EmploymentType), default=EmploymentType.OTHER)
    experience_required = Column(String(100), nullable=True)
    salary = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    skills_required = Column(Text, nullable=True)
    eligibility = Column(Text, nullable=True)
    application_url = Column(String(500), nullable=True)
    original_url = Column(String(500), unique=True, index=True, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    posted_date = Column(DateTime(timezone=True), nullable=True)
    source = Column(String(255), nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
