from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models.student import Student
from app.schemas.student import StudentResponse, StudentUpdate
from app.utils.jwt_handler import get_current_student

router = APIRouter()


@router.get("/me", response_model=StudentResponse)
async def get_profile(
    current_student: Student = Depends(get_current_student),
):
    """Get the current authenticated student's profile."""
    return current_student


@router.put("/me", response_model=StudentResponse)
async def update_profile(
    updates: StudentUpdate,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Update the current authenticated student's profile."""
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_student, field, value)

    db.add(current_student)
    await db.commit()
    await db.refresh(current_student)
    return current_student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(student_id: int, db: AsyncSession = Depends(get_db)):
    """Get a student profile by ID."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
