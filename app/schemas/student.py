from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None


class StudentCreate(StudentBase):
    password: str


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
