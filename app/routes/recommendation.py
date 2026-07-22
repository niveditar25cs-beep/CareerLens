from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database.database import get_db
from app.models.recommendation import Recommendation
from app.models.student import Student
from app.schemas.opportunity import OpportunityResponse
from app.utils.jwt_handler import get_current_student
from app.services.recommendation_engine import generate_recommendations

router = APIRouter()


@router.get("/", response_model=List[OpportunityResponse])
async def get_recommendations(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Get personalized opportunity recommendations for the current student."""
    recommendations = await generate_recommendations(current_student, db)
    return recommendations


@router.post("/refresh")
async def refresh_recommendations(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Regenerate recommendations for the current student."""
    recommendations = await generate_recommendations(current_student, db, refresh=True)
    return {"message": "Recommendations refreshed", "count": len(recommendations)}
