"""
Search service for querying opportunities with filters and full-text search.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List, Optional
from app.models.opportunity import Opportunity


async def search_opportunities(
    db: AsyncSession,
    query: Optional[str] = None,
    opportunity_type: Optional[str] = None,
    location: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[Opportunity]:
    """
    Search opportunities with optional keyword and filter parameters.

    Args:
        db: Async database session.
        query: Free-text search term to match against title, description, company.
        opportunity_type: Filter by type (internship, job, scholarship, etc.).
        location: Filter by location.
        category: Filter by category.
        skip: Number of results to skip (pagination).
        limit: Maximum results to return.

    Returns:
        A list of matching Opportunity objects.
    """
    stmt = select(Opportunity)

    if query:
        search_term = f"%{query}%"
        stmt = stmt.where(
            or_(
                Opportunity.title.ilike(search_term),
                Opportunity.description.ilike(search_term),
                Opportunity.company.ilike(search_term),
                Opportunity.skills_required.ilike(search_term),
            )
        )

    if opportunity_type:
        stmt = stmt.where(Opportunity.opportunity_type == opportunity_type)

    if location:
        stmt = stmt.where(Opportunity.location.ilike(f"%{location}%"))

    if category:
        stmt = stmt.where(Opportunity.category == category)

    stmt = stmt.order_by(Opportunity.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()
