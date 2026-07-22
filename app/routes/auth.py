from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models.student import Student
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.student import StudentCreate, StudentResponse
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()


@router.post("/register", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def register(student_data: StudentCreate, db: AsyncSession = Depends(get_db)):
    """Register a new student account."""
    result = await db.execute(select(Student).where(Student.email == student_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = Student(
        full_name=student_data.full_name,
        email=student_data.email,
        hashed_password=hash_password(student_data.password),
        phone=student_data.phone,
        university=student_data.university,
        major=student_data.major,
        skills=student_data.skills,
        interests=student_data.interests,
        bio=student_data.bio,
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a student and return a JWT token."""
    result = await db.execute(select(Student).where(Student.email == credentials.email))
    student = result.scalar_one_or_none()

    if not student or not verify_password(credentials.password, student.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(student.id)})
    return TokenResponse(access_token=access_token)
