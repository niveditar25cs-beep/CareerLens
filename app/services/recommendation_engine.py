"""
Recommendation engine for matching students with relevant opportunities.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.student import Student
from app.models.opportunity import Opportunity


async def generate_recommendations(
    student: Student,
    db: AsyncSession,
    refresh: bool = False,
    limit: int = 10,
) -> List[Opportunity]:
    """
    Generate personalized opportunity recommendations for a student
    based on their skills, interests, and profile.

    Args:
        student: The student to generate recommendations for.
        db: Async database session.
        refresh: If True, regenerate even if cached results exist.
        limit: Maximum number of recommendations to return.

    Returns:
        A list of recommended Opportunity objects.
    """
    # TODO: Implement ML-based or heuristic recommendation logic
    # Current placeholder: return latest opportunities matching student skills

    student_skills = (student.skills or "").lower().split(",")
    student_skills = [s.strip() for s in student_skills if s.strip()]

    query = select(Opportunity).order_by(Opportunity.created_at.desc()).limit(limit)
    result = await db.execute(query)
    opportunities = result.scalars().all()

    if not student_skills:
        return opportunities

    # Simple keyword matching (placeholder for a smarter engine)
    scored = []
    for opp in opportunities:
        opp_skills = (opp.skills_required or "").lower()
        score = sum(1 for skill in student_skills if skill in opp_skills)
        scored.append((score, opp))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [opp for _, opp in scored[:limit]]
