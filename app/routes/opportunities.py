from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.database.database import get_db
from app.models.opportunity import Opportunity
from app.models.saved import SavedOpportunity
from app.models.student import Student
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse, OpportunityUpdate
from app.schemas.saved import SavedOpportunityResponse
from app.services.search import search_opportunities
from app.utils.jwt_handler import get_current_student

router = APIRouter()


@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    q: Optional[str] = Query(None, description="Search query string"),
    opportunity_type: Optional[str] = Query(None, description="Filter by opportunity type"),
    location: Optional[str] = Query(None, description="Filter by location"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List opportunities with keyword search, multi-field filtering, and pagination."""
    return await search_opportunities(
        db=db,
        query=q,
        opportunity_type=opportunity_type,
        location=location,
        category=category,
        skip=skip,
        limit=limit,
    )


@router.get("/saved/me", response_model=List[SavedOpportunityResponse])
async def list_saved_opportunities(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """List all saved opportunities for the authenticated student."""
    result = await db.execute(
        select(SavedOpportunity)
        .where(SavedOpportunity.student_id == current_student.id)
        .order_by(SavedOpportunity.saved_at.desc())
    )
    return result.scalars().all()


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single opportunity by ID."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
async def create_opportunity(data: OpportunityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new opportunity."""
    opportunity = Opportunity(**data.model_dump())
    db.add(opportunity)
    await db.commit()
    await db.refresh(opportunity)
    return opportunity


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: int,
    updates: OpportunityUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing opportunity."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(opportunity, field, value)

    await db.commit()
    await db.refresh(opportunity)
    return opportunity


@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an opportunity."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    await db.delete(opportunity)
    await db.commit()


@router.post("/{opportunity_id}/save", response_model=SavedOpportunityResponse, status_code=status.HTTP_201_CREATED)
async def save_opportunity(
    opportunity_id: int,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Save/bookmark an opportunity for the authenticated student."""
    # Check if opportunity exists
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Check if already saved
    existing = await db.execute(
        select(SavedOpportunity).where(
            SavedOpportunity.student_id == current_student.id,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Opportunity already saved")

    saved_item = SavedOpportunity(
        student_id=current_student.id,
        opportunity_id=opportunity_id,
    )
    db.add(saved_item)
    await db.commit()
    await db.refresh(saved_item)
    return saved_item


@router.delete("/{opportunity_id}/save", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_opportunity(
    opportunity_id: int,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Remove a saved opportunity for the authenticated student."""
    result = await db.execute(
        select(SavedOpportunity).where(
            SavedOpportunity.student_id == current_student.id,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
    )
    saved_item = result.scalar_one_or_none()
    if not saved_item:
        raise HTTPException(status_code=404, detail="Saved opportunity record not found")

    await db.delete(saved_item)
    await db.commit()

