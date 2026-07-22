"""
Recommendation engine for matching students with relevant opportunities.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
from app.models.student import Student
from app.models.opportunity import Opportunity
from app.models.recommendation import Recommendation


def calculate_match_score(student: Student, opp: Opportunity) -> float:
    """Calculate a match score between a student profile and an opportunity."""
    student_tokens = set()

    if student.skills:
        student_tokens.update([s.strip().lower() for s in student.skills.split(",") if s.strip()])
    if student.interests:
        student_tokens.update([i.strip().lower() for i in student.interests.split(",") if i.strip()])
    if student.major:
        student_tokens.add(student.major.strip().lower())

    if not student_tokens:
        return 0.0

    opp_text = " ".join(
        filter(
            None,
            [
                opp.title,
                opp.description,
                opp.skills_required,
                opp.category,
                opp.company,
            ],
        )
    ).lower()

    matches = sum(1 for token in student_tokens if token in opp_text)
    score = round(matches / max(len(student_tokens), 1), 2)
    return score


async def generate_recommendations(
    student: Student,
    db: AsyncSession,
    refresh: bool = False,
    limit: int = 10,
) -> List[Opportunity]:
    """
    Generate personalized opportunity recommendations for a student
    based on their skills, interests, and profile, persisting scores to the database.

    Args:
        student: The student to generate recommendations for.
        db: Async database session.
        refresh: If True, regenerate even if cached results exist.
        limit: Maximum number of recommendations to return.

    Returns:
        A list of recommended Opportunity objects.
    """
    query = select(Opportunity)
    result = await db.execute(query)
    all_opportunities = result.scalars().all()

    if not all_opportunities:
        return []

    # Score each opportunity
    scored_opps = []
    for opp in all_opportunities:
        score = calculate_match_score(student, opp)
        scored_opps.append((score, opp))

    # Sort descending by score, then by newest
    scored_opps.sort(key=lambda x: (x[0], x[1].created_at or 0), reverse=True)
    top_items = scored_opps[:limit]

    # Save to recommendations table asynchronously
    try:
        await db.execute(
            delete(Recommendation).where(Recommendation.student_id == student.id)
        )
        for score, opp in top_items:
            rec = Recommendation(
                student_id=student.id,
                opportunity_id=opp.id,
                score=float(score),
            )
            db.add(rec)
        await db.commit()
    except Exception:
        await db.rollback()

    return [opp for _, opp in top_items]

